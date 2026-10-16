"""Kiểm thử lịch (schedule/tasks.json) và công cụ scripts/today.py. Chỉ thư viện chuẩn.

Chạy: python tests/test_schedule.py
"""
import datetime as dt
import io
import json
import os
import sys
import tempfile
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import today  # noqa: E402

D = dt.date.fromisoformat


def with_tmp_status(fn):
    def wrapped():
        old_status, old_nick = today.STATUS_DIR, today.NICK_FILE
        with tempfile.TemporaryDirectory() as tmp:
            today.STATUS_DIR = tmp
            today.NICK_FILE = os.path.join(tmp, ".nick")
            try:
                fn()
            finally:
                today.STATUS_DIR, today.NICK_FILE = old_status, old_nick
    wrapped.__name__ = fn.__name__
    return wrapped


def quiet(f, *a, **k):
    with redirect_stdout(io.StringIO()):
        return f(*a, **k)


S = today.load_schedule()


@with_tmp_status
def test_schedule_valid():
    assert today.check(S) == [], today.check(S)


def test_every_member_has_work_every_week():
    """Từ W1 đến W12, mỗi thành viên có ít nhất một task giao nhau với mỗi tuần."""
    day0 = D(S["meta"]["day0"])
    for w in range(12):
        lo, hi = day0 + dt.timedelta(days=7 * w), day0 + dt.timedelta(days=7 * w + 6)
        for n in today.NICKS:
            hit = [t for t in S["tasks"] if t["owner"] == n and D(t["start"]) <= hi and D(t["due"]) >= lo]
            assert hit, f"{n} không có việc trong W{w + 1}"


def test_gate_tasks_on_gate_dates():
    for g in S["gates"]:
        on = [t for t in S["tasks"] if t["owner"] == "ALL" and t["kind"] == "gate" and t["due"] == g["date"]]
        assert on, f"thiếu task họp gate {g['id']} ngày {g['date']}"


def test_issues_referenced_exist_in_range():
    for t in S["tasks"]:
        if t.get("issue") is not None:
            assert 1 <= t["issue"] <= 17, t["id"]


@with_tmp_status
def test_today_basic_and_overdue():
    r = today.build_today(S, "FAO", D("2026-10-20"))
    assert [t["id"] for t in r["today"]] == [] or all(t["owner"] in ("FAO", "ALL") for t in r["today"])
    assert "W1-FAO-01" in [t["id"] for t in r["overdue"]]
    # W1-FAO-02 bị chặn vì W1-FAO-01 chưa xong
    assert "W1-FAO-02" in [t["id"] for t in r["blocked"]]


@with_tmp_status
def test_done_requires_evidence_and_unblocks():
    try:
        quiet(today.set_state, S, "FAO", "W1-FAO-01", "done", None, None, D("2026-10-19"))
        raise AssertionError("phải từ chối --done thiếu evidence")
    except SystemExit:
        pass
    quiet(today.set_state, S, "FAO", "W1-FAO-01", "done", "machine_notes commit abc", None, D("2026-10-19"))
    r = today.build_today(S, "FAO", D("2026-10-20"))
    assert "W1-FAO-02" in [t["id"] for t in r["today"]]
    assert "W1-FAO-01" not in [t["id"] for t in r["overdue"]]


@with_tmp_status
def test_cannot_mark_others_task():
    try:
        quiet(today.set_state, S, "LDN", "W1-FAO-01", "done", "x", None, D("2026-10-19"))
        raise AssertionError("LDN không được đánh dấu task của FAO")
    except SystemExit:
        pass


@with_tmp_status
def test_review_queue_flow():
    quiet(today.set_state, S, "FAO", "W1-FAO-02", "done", "results/raw/EXP-01/r1", None, D("2026-10-20"))
    r = today.build_today(S, "DAT", D("2026-10-21"))
    assert "W1-FAO-02" in [t["id"] for t in r["reviews"]]
    try:
        quiet(today.approve, S, "LDN", "W1-FAO-02", "x", None, D("2026-10-21"), False)
        raise AssertionError("chỉ second reader được duyệt")
    except SystemExit:
        pass
    quiet(today.approve, S, "DAT", "W1-FAO-02", "review_log dòng 1", None, D("2026-10-21"), False)
    r = today.build_today(S, "DAT", D("2026-10-21"))
    assert "W1-FAO-02" not in [t["id"] for t in r["reviews"]]


@with_tmp_status
def test_waiting_on_me():
    r = today.build_today(S, "FAO", D("2026-10-21"))
    assert any(w["id"] == "W1-DAT-05" for w in r["waiting_on_me"])


@with_tmp_status
def test_plan_condition(tmp_decisions=None):
    old = today.DECISIONS
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write("# Decisions\n- PLAN: B\n")
    try:
        today.DECISIONS = f.name
        r = today.build_today(S, "DAT", D("2026-11-24"))
        assert "W6-DAT-02" not in [t["id"] for t in r["today"] + r["blocked"]]
        with open(f.name, "w", encoding="utf-8") as g:
            g.write("- PLAN: A\n")
        r = today.build_today(S, "DAT", D("2026-11-24"))
        assert "W6-DAT-02" in [t["id"] for t in r["today"] + r["blocked"]]
    finally:
        today.DECISIONS = old
        os.unlink(f.name)


@with_tmp_status
def test_nick_detection_file_and_json_cli():
    quiet(today.main, ["--set-nick", "LDN"])
    nick, how = today.detect_nick(S, None)
    assert (nick, how) == ("LDN", ".nick")
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = today.main(["--json", "--date", "2026-10-20"])
    assert rc == 0
    data = json.loads(buf.getvalue())
    assert data["nick"] == "LDN" and data["date"] == "2026-10-20"
    assert "W1-LDN-02" in [t["id"] for t in data["today"]]


@with_tmp_status
def test_render_contains_all_tasks():
    md = today.render(S)
    for t in S["tasks"]:
        assert f"`{t['id']}`" in md, t["id"]


if __name__ == "__main__":
    tests = [v for k, v in dict(globals()).items() if k.startswith("test_") and callable(v)]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS {t.__name__}")
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"FAIL {t.__name__}: {e!r}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)
