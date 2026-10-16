#!/usr/bin/env python3
"""Trả lời "hôm nay tôi cần làm gì?" cho từng thành viên, từ schedule/tasks.json.

Chỉ dùng thư viện chuẩn. Ví dụ:
  python scripts/today.py                     # tự nhận nick, ngày hôm nay (giờ Việt Nam)
  python scripts/today.py --nick LDN --date 2026-10-21
  python scripts/today.py --json              # cho Claude đọc
  python scripts/today.py --team              # tình hình cả nhóm (DAT điều phối)
  python scripts/today.py --start W1-FAO-02
  python scripts/today.py --done W1-FAO-02 --evidence "results/raw/EXP-01/2026-10-20_x; commit abc123"
  python scripts/today.py --block W1-FAO-03 --note "SB3 lỗi import; chờ DAT"
  python scripts/today.py --approve W1-FAO-04 --evidence "review_log dòng 3"   # second reader duyệt
  python scripts/today.py --note-file         # tạo khung ghi chú ngày (Form H)
  python scripts/today.py --set-nick FAO      # lưu nick vào .nick (không commit)
  python scripts/today.py --render            # sinh schedule/SCHEDULE.md
  python scripts/today.py --check             # kiểm tra tính hợp lệ của lịch

Trạng thái mỗi người nằm ở schedule/status/<NICK>.json; mỗi người chỉ sửa file của mình,
nên không có xung đột khi merge.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TASKS = os.path.join(REPO, "schedule", "tasks.json")
STATUS_DIR = os.path.join(REPO, "schedule", "status")
NICK_FILE = os.path.join(REPO, ".nick")
DECISIONS = os.path.join(REPO, "docs", "DECISIONS.md")
NICKS = ("DAT", "LDN", "FAO")
STATES = ("todo", "doing", "done", "blocked", "skipped")
WEEKDAY_VI = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
UPCOMING_DAYS = 3

# Windows đôi khi thiếu tzdata; khi đó dùng UTC+7 cố định (Việt Nam không có giờ mùa hè).
try:
    from zoneinfo import ZoneInfo
    TZ = ZoneInfo("Asia/Ho_Chi_Minh")
except Exception:  # pragma: no cover
    TZ = dt.timezone(dt.timedelta(hours=7))

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# ---------------------------------------------------------------- dữ liệu
def d(s: str) -> dt.date:
    return dt.date.fromisoformat(s)


def fmt(day: dt.date) -> str:
    return f"{WEEKDAY_VI[day.weekday()]} {day:%d/%m/%Y}"


def load_schedule(path: str = TASKS) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def status_path(nick: str) -> str:
    return os.path.join(STATUS_DIR, f"{nick}.json")


def load_status(nick: str) -> dict:
    p = status_path(nick)
    if not os.path.exists(p):
        return {"nick": nick, "tasks": {}, "reviews": {}}
    with open(p, encoding="utf-8") as f:
        data = json.load(f)
    data.setdefault("tasks", {})
    data.setdefault("reviews", {})
    return data


def save_status(nick: str, data: dict) -> None:
    os.makedirs(STATUS_DIR, exist_ok=True)
    with open(status_path(nick), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def all_status() -> dict:
    return {n: load_status(n) for n in NICKS}


def task_state(task: dict, statuses: dict) -> str:
    """Trạng thái của task theo file status của owner (ALL: bất kỳ ai đánh dấu)."""
    owners = NICKS if task["owner"] == "ALL" else (task["owner"],)
    states = [statuses[o]["tasks"].get(task["id"], {}).get("state") for o in owners]
    for s in ("done", "skipped", "blocked", "doing"):
        if s in states:
            return s
    return "todo"


def is_finished(state: str) -> bool:
    return state in ("done", "skipped")


def review_state(task: dict, statuses: dict) -> str | None:
    r = task.get("reviewer")
    if not r:
        return None
    return statuses[r]["reviews"].get(task["id"], {}).get("state", "pending")


def decided_plan() -> str | None:
    if not os.path.exists(DECISIONS):
        return None
    with open(DECISIONS, encoding="utf-8") as f:
        m = re.findall(r"^\s*[-*]?\s*PLAN:\s*([AB])\b", f.read(), flags=re.M)
    return m[-1] if m else None


def applicable(task: dict, plan: str | None) -> tuple[bool, str | None]:
    cond = task.get("condition")
    if not cond:
        return True, None
    want = cond.split(":")[-1].strip()
    if plan is None:
        return True, f"chỉ áp dụng nếu G1 chọn phương án {want} (chưa quyết)"
    return plan == want, None


# ---------------------------------------------------------------- nhận diện thành viên
def git(*args: str) -> str:
    try:
        return subprocess.run(["git", "-C", REPO, *args], capture_output=True, text=True,
                              timeout=10).stdout.strip()
    except Exception:
        return ""


def detect_nick(sched: dict, explicit: str | None) -> tuple[str | None, str]:
    if explicit:
        return explicit.upper(), "--nick"
    env = os.environ.get("UAV_NICK")
    if env:
        return env.upper(), "biến môi trường UAV_NICK"
    if os.path.exists(NICK_FILE):
        with open(NICK_FILE, encoding="utf-8") as f:
            v = f.read().strip().upper()
        if v in NICKS:
            return v, ".nick"
    ids = {git("config", "user.name").lower(), git("config", "user.email").lower()} - {""}
    for nick, m in sched["members"].items():
        aliases = {a.lower() for a in m.get("aliases", [])} | {m["github"].lower()}
        if ids & aliases:
            return nick, "git config"
    return None, "không xác định"


# ---------------------------------------------------------------- tính toán "hôm nay"
def week_label(sched: dict, day: dt.date) -> str:
    n = (day - d(sched["meta"]["day0"])).days
    if n < 0:
        return f"trước Day 0 ({-n} ngày nữa khởi động)"
    return f"Day {n} · W{n // 7 + 1}"


def build_today(sched: dict, nick: str, day: dt.date) -> dict:
    statuses = all_status()
    plan = decided_plan()
    by_id = {t["id"]: t for t in sched["tasks"]}

    def view(t: dict) -> dict:
        ok, cond_note = applicable(t, plan)
        state = task_state(t, statuses)
        deps_open = [x for x in t.get("depends", []) if not is_finished(task_state(by_id[x], statuses))]
        st = statuses[t["owner"]]["tasks"].get(t["id"], {}) if t["owner"] != "ALL" else {}
        return {**t, "state": state, "deps_open": deps_open, "condition_note": cond_note,
                "applicable": ok, "days_left": (d(t["due"]) - day).days,
                "status_note": st.get("note"), "evidence": st.get("evidence"),
                "review_state": review_state(t, statuses)}

    mine = [view(t) for t in sched["tasks"] if t["owner"] in (nick, "ALL")]
    mine = [t for t in mine if t["applicable"]]

    today, overdue, upcoming, blocked = [], [], [], []
    for t in mine:
        if is_finished(t["state"]):
            continue
        s, e = d(t["start"]), d(t["due"])
        if e < day:
            overdue.append(t)
        elif s <= day <= e:
            (blocked if t["deps_open"] or t["state"] == "blocked" else today).append(t)
        elif day < s <= day + dt.timedelta(days=UPCOMING_DAYS):
            upcoming.append(t)

    reviews = []
    for t in sched["tasks"]:
        if t.get("reviewer") != nick:
            continue
        v = view(t)
        if v["state"] == "done" and v["review_state"] not in ("approved",):
            reviews.append(v)

    # Việc người khác đang chờ mình: task chưa xong của người khác phụ thuộc task chưa xong của mình
    waiting_on_me = []
    my_open = {t["id"] for t in mine if not is_finished(t["state"]) and t["owner"] == nick}
    for t in sched["tasks"]:
        if t["owner"] in (nick, "ALL"):
            continue
        v = view(t)
        if is_finished(v["state"]) or d(t["start"]) > day + dt.timedelta(days=UPCOMING_DAYS):
            continue
        hit = [x for x in v["deps_open"] if x in my_open]
        if hit:
            waiting_on_me.append({"id": t["id"], "owner": t["owner"], "title": t["title"],
                                  "start": t["start"], "needs": hit})

    recurring = []
    for r in sched.get("recurring", []):
        if not (d(r["from"]) <= day <= d(r["to"])):
            continue
        if r["every"] == "day" or (r["every"] == "monday" and day.weekday() == 0):
            recurring.append(r)

    note_path = os.path.join("notes", f"{day.isoformat()}_{nick.lower()}.md")
    next_gate = next((g for g in sched["gates"] if d(g["date"]) >= day), None)
    if next_gate:
        next_gate = {**next_gate, "days_left": (d(next_gate["date"]) - day).days}

    key = lambda t: (t["due"], t["id"])  # noqa: E731
    return {
        "nick": nick, "name": sched["members"][nick]["name"], "date": day.isoformat(),
        "date_label": fmt(day), "week": week_label(sched, day), "plan": plan,
        "next_gate": next_gate,
        "today": sorted(today, key=key), "overdue": sorted(overdue, key=key),
        "blocked": sorted(blocked, key=key), "reviews": sorted(reviews, key=key),
        "waiting_on_me": waiting_on_me, "upcoming": sorted(upcoming, key=lambda t: (t["start"], t["id"])),
        "recurring": recurring,
        "daily_note": {"path": note_path, "exists": os.path.exists(os.path.join(REPO, note_path))},
    }


# ---------------------------------------------------------------- in ra
def line_task(t: dict, verbose: bool = True) -> list[str]:
    span = t["start"] if t["start"] == t["due"] else f"{t['start']} → {t['due']}"
    tags = []
    if t["owner"] == "ALL":
        tags.append("cả nhóm")
    if t.get("issue"):
        tags.append(f"issue #{t['issue']}")
    if t.get("reviewer"):
        tags.append(f"second reader {t['reviewer']}")
    if t["state"] == "doing":
        tags.append("ĐANG LÀM")
    if t.get("days_left") is not None and t["days_left"] < 0:
        tags.append(f"TRỄ {-t['days_left']} ngày")
    elif t.get("days_left") == 0:
        tags.append("hạn HÔM NAY")
    out = [f"■ [{t['id']}] {t['title']}", f"    {span} · {' · '.join(tags)}" if tags else f"    {span}"]
    if t.get("condition_note"):
        out.append(f"    ⚠ {t['condition_note']}")
    if t.get("deps_open"):
        out.append(f"    ⛔ chờ: {', '.join(t['deps_open'])}")
    if t.get("status_note"):
        out.append(f"    ghi chú: {t['status_note']}")
    if verbose:
        for i, s in enumerate(t.get("steps", []), 1):
            out.append(f"    {i}. {s}")
        for c in t.get("commands", []):
            out.append(f"    $ {c}")
        if t.get("outputs"):
            out.append(f"    → sản phẩm: {', '.join(t['outputs'])}")
        out.append(f"    ✓ xong khi: {t['done_when']}")
    return out


def print_today(r: dict) -> None:
    print(f"=== {r['name']} ({r['nick']}) — {r['date_label']} — {r['week']} ===")
    if r["next_gate"]:
        g = r["next_gate"]
        print(f"Gate gần nhất: {g['id']} {g['title']} — {g['date']} (còn {g['days_left']} ngày)")
    print(f"Phương án (G1): {r['plan'] or 'chưa quyết'}")

    sections = [("QUÁ HẠN — làm trước", r["overdue"], True),
                ("HÔM NAY", r["today"], True),
                ("CẦN BẠN REVIEW (second reader)", r["reviews"], False),
                ("ĐANG BỊ CHẶN (chờ phụ thuộc)", r["blocked"], False),
                (f"SẮP TỚI ({UPCOMING_DAYS} ngày)", r["upcoming"], False)]
    for title, items, verbose in sections:
        if not items:
            continue
        print(f"\n## {title}")
        for t in items:
            print("\n".join(line_task(t, verbose)))
    if r["waiting_on_me"]:
        print("\n## NGƯỜI KHÁC ĐANG CHỜ BẠN")
        for w in r["waiting_on_me"]:
            print(f"- {w['owner']} [{w['id']}] {w['title']} (bắt đầu {w['start']}) cần: {', '.join(w['needs'])}")
    if not (r["overdue"] or r["today"] or r["reviews"]):
        print("\nKhông có việc theo lịch hôm nay. Gợi ý: xem mục SẮP TỚI, đọc thêm, hoặc hỗ trợ việc bị chặn.")
    print("\n## LẶP LẠI")
    for x in r["recurring"]:
        if x["id"] != "R-NOTE":
            print(f"- {x['title']} ({x['when']})")
    dn = r["daily_note"]
    print(f"- Ghi chú ngày: {dn['path']} — {'đã có' if dn['exists'] else 'CHƯA CÓ'}")


def print_team(sched: dict, day: dt.date) -> None:
    print(f"=== Cả nhóm — {fmt(day)} — {week_label(sched, day)} ===")
    for n in NICKS:
        r = build_today(sched, n, day)
        own = lambda xs: [t for t in xs if t["owner"] == n]  # noqa: E731
        print(f"\n{n} ({r['name']}): hôm nay {len(own(r['today']))} · quá hạn {len(own(r['overdue']))}"
              f" · bị chặn {len(own(r['blocked']))} · chờ review {len(r['reviews'])}"
              f" · ghi chú ngày {'✓' if r['daily_note']['exists'] else '✗'}")
        for t in own(r["overdue"]):
            print(f"   TRỄ  [{t['id']}] {t['title']} (hạn {t['due']}, {t['state']})")
        for t in own(r["today"]) + own(r["blocked"]):
            print(f"   nay  [{t['id']}] {t['title']} ({t['state']}{', chờ ' + ','.join(t['deps_open']) if t['deps_open'] else ''})")


# ---------------------------------------------------------------- cập nhật trạng thái
def set_state(sched: dict, nick: str, tid: str, state: str, evidence: str | None, note: str | None,
              day: dt.date) -> None:
    ids = {t["id"]: t for t in sched["tasks"]}
    if tid not in ids:
        sys.exit(f"Không có task {tid}.")
    t = ids[tid]
    if t["owner"] not in (nick, "ALL"):
        sys.exit(f"{tid} thuộc {t['owner']}, không phải {nick}. Second reader dùng --approve.")
    if state == "done" and not evidence:
        sys.exit("--done cần --evidence (run ID, commit, đường dẫn file hoặc link PR/issue).")
    st = load_status(nick)
    rec = st["tasks"].get(tid, {})
    rec.update({"state": state, "date": day.isoformat()})
    if evidence:
        rec["evidence"] = evidence
    if note:
        rec["note"] = note
    st["tasks"][tid] = rec
    save_status(nick, st)
    print(f"{nick}: {tid} → {state}. Nhớ commit schedule/status/{nick}.json.")


def approve(sched: dict, nick: str, tid: str, evidence: str | None, note: str | None,
            day: dt.date, changes: bool) -> None:
    ids = {t["id"]: t for t in sched["tasks"]}
    if tid not in ids:
        sys.exit(f"Không có task {tid}.")
    if ids[tid].get("reviewer") != nick:
        sys.exit(f"Second reader của {tid} là {ids[tid].get('reviewer')}, không phải {nick}.")
    if not evidence:
        sys.exit("--approve/--request-changes cần --evidence (dòng review_log, review PR, run ID chạy lại).")
    st = load_status(nick)
    st["reviews"][tid] = {"state": "changes_requested" if changes else "approved",
                          "date": day.isoformat(), "evidence": evidence, **({"note": note} if note else {})}
    save_status(nick, st)
    print(f"{nick}: review {tid} → {st['reviews'][tid]['state']}. Nhớ commit schedule/status/{nick}.json.")


def write_note(r: dict) -> None:
    p = os.path.join(REPO, r["daily_note"]["path"])
    if os.path.exists(p):
        print(f"Đã có {r['daily_note']['path']} — không ghi đè.")
        return
    touched = [f"{k} ({v.get('state')})" for k, v in sorted(load_status(r["nick"])["tasks"].items())
               if v.get("date") == r["date"]]
    touched += [f"{k} (review {v.get('state')})" for k, v in sorted(load_status(r["nick"])["reviews"].items())
                if v.get("date") == r["date"]]
    open_ = [t["id"] for t in r["overdue"] + r["today"]]
    ids = (f"đã cập nhật hôm nay: {', '.join(touched) or '—'}; "
           f"còn mở: {', '.join(open_) or '—'}")
    body = (f"# Ghi chú ngày — {r['date']} — {r['nick']}\n\n"
            f"Task theo lịch: {ids}\n\n"
            "```text\n"
            f"Ngày / NICK: {r['date']} / {r['nick']}\n"
            "Hôm nay biết thêm điều gì:\n"
            "Bằng chứng: <run ID, hình, hoặc commit>\n"
            "Điều còn chưa chắc:\n"
            "Thực nghiệm nhỏ nhất có tính quyết định cho ngày mai:\n"
            "Owner và second reader:\n"
            "Cần giúp gì, kèm ví dụ tái hiện nhỏ nhất:\n"
            "```\n")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(body)
    print(f"Đã tạo {r['daily_note']['path']}")


# ---------------------------------------------------------------- kiểm tra & render
def check(sched: dict) -> list[str]:
    errs = []
    ids = [t["id"] for t in sched["tasks"]]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        errs.append(f"id trùng: {sorted(dup)}")
    idset = set(ids)
    start0, end = d(sched["meta"]["day0"]) - dt.timedelta(days=7), d(sched["meta"]["end"])
    gates = {g["id"] for g in sched["gates"]}
    for t in sched["tasks"]:
        for k in ("id", "owner", "start", "due", "title", "steps", "done_when"):
            if k not in t:
                errs.append(f"{t.get('id')}: thiếu trường {k}")
        try:
            s, e = d(t["start"]), d(t["due"])
            if s > e:
                errs.append(f"{t['id']}: start > due")
            if s < start0 or e > end:
                errs.append(f"{t['id']}: ngoài khoảng dự án")
        except Exception as ex:
            errs.append(f"{t.get('id')}: ngày lỗi ({ex})")
            continue
        if t["owner"] not in NICKS + ("ALL",):
            errs.append(f"{t['id']}: owner lạ {t['owner']}")
        if t.get("reviewer") and (t["reviewer"] not in NICKS or t["reviewer"] == t["owner"]):
            errs.append(f"{t['id']}: reviewer không hợp lệ {t['reviewer']}")
        if t.get("gate") and t["gate"] not in gates:
            errs.append(f"{t['id']}: gate lạ {t['gate']}")
        if not t["id"].startswith("S-") and t["owner"] != "ALL" and f"-{t['owner']}-" not in t["id"]:
            errs.append(f"{t['id']}: id không chứa nick owner")
        for x in t.get("depends", []):
            if x not in idset:
                errs.append(f"{t['id']}: phụ thuộc không tồn tại {x}")
            elif d(sched["tasks"][ids.index(x)]["start"]) > d(t["due"]):
                errs.append(f"{t['id']}: phụ thuộc {x} bắt đầu sau hạn của task")
    for n in NICKS:
        st = load_status(n)
        for k, v in st["tasks"].items():
            if k not in idset:
                errs.append(f"status/{n}.json: task lạ {k}")
            if v.get("state") not in STATES:
                errs.append(f"status/{n}.json: {k} trạng thái lạ {v.get('state')}")
    return errs


def render(sched: dict) -> str:
    """Bảng tĩnh từ tasks.json (không chứa trạng thái, để không xung đột khi merge).
    Trạng thái thực tế: python scripts/today.py --team."""
    out = ["# Lịch theo ngày (tự sinh — KHÔNG sửa tay)", "",
           "> Sinh bởi `python scripts/today.py --render` từ `schedule/tasks.json` (chỉ DAT chạy lại khi lịch đổi).",
           "> Trạng thái thực tế: `python scripts/today.py --team`. Việc của bạn hôm nay: hỏi Claude",
           "> \"hôm nay tôi cần làm gì?\" trong repo này, hoặc chạy `python scripts/today.py`.", "",
           "| Gate | Ngày | Nội dung |", "| --- | --- | --- |"]
    out += [f"| **{g['id']}** | {g['date']} | {g['title']} |" for g in sched["gates"]]
    weeks: dict[str, list] = {}
    day0 = d(sched["meta"]["day0"])
    for t in sorted(sched["tasks"], key=lambda t: (t["start"], t["owner"], t["id"])):
        n = (d(t["start"]) - day0).days
        wk = "W0 (chuẩn bị)" if n < 0 else f"W{n // 7 + 1}"
        weeks.setdefault(wk, []).append(t)
    for wk, items in weeks.items():
        out += ["", f"## {wk}", "", "| Bắt đầu | Ai | Task | Hạn | Second reader | Issue |",
                "| --- | --- | --- | --- | --- | --- |"]
        for t in items:
            cond = f" _({t['condition']})_" if t.get("condition") else ""
            out.append(f"| {fmt(d(t['start']))} | {t['owner']} | `{t['id']}` {t['title']}{cond} "
                       f"| {fmt(d(t['due']))} | {t.get('reviewer') or ''} "
                       f"| {('#' + str(t['issue'])) if t.get('issue') else ''} |")
    out += ["", "Lặp lại: ghi chú ngày (Form H) mỗi ngày làm việc; họp nhóm thứ Hai 20:00."]
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- main
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--nick", choices=NICKS, type=str.upper)
    ap.add_argument("--date", help="YYYY-MM-DD (mặc định: hôm nay, giờ Việt Nam)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--team", action="store_true")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--start", metavar="ID")
    g.add_argument("--done", metavar="ID")
    g.add_argument("--block", metavar="ID")
    g.add_argument("--skip", metavar="ID")
    g.add_argument("--reopen", metavar="ID")
    g.add_argument("--approve", metavar="ID")
    g.add_argument("--request-changes", metavar="ID")
    ap.add_argument("--evidence")
    ap.add_argument("--note")
    ap.add_argument("--note-file", action="store_true", help="tạo khung ghi chú ngày Form H")
    ap.add_argument("--set-nick", choices=NICKS, type=str.upper)
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)

    sched = load_schedule()
    day = d(a.date) if a.date else dt.datetime.now(TZ).date()

    if a.check:
        errs = check(sched)
        print("\n".join(errs) if errs else f"OK: {len(sched['tasks'])} task hợp lệ.")
        return 1 if errs else 0
    if a.render:
        p = os.path.join(REPO, "schedule", "SCHEDULE.md")
        with open(p, "w", encoding="utf-8") as f:
            f.write(render(sched))
        print(f"Đã ghi {os.path.relpath(p, REPO)}")
        return 0
    if a.set_nick:
        with open(NICK_FILE, "w", encoding="utf-8") as f:
            f.write(a.set_nick + "\n")
        print(f"Đã lưu nick {a.set_nick} vào .nick (file này không được commit).")
        return 0
    if a.team:
        print_team(sched, day)
        return 0

    nick, how = detect_nick(sched, a.nick)
    if nick not in NICKS:
        msg = ("Không xác định được bạn là ai. Chạy một lần: python scripts/today.py --set-nick <DAT|LDN|FAO>"
               " hoặc thêm --nick.")
        if a.json:
            print(json.dumps({"error": "unknown_nick", "message": msg}, ensure_ascii=False))
        else:
            print(msg)
        return 2

    for flag, state in (("start", "doing"), ("done", "done"), ("block", "blocked"),
                        ("skip", "skipped"), ("reopen", "todo")):
        tid = getattr(a, flag)
        if tid:
            if state == "skipped" and not a.note:
                sys.exit("--skip cần --note (lý do, và ai đã đồng ý).")
            set_state(sched, nick, tid, state, a.evidence, a.note, day)
            return 0
    if a.approve or a.request_changes:
        approve(sched, nick, a.approve or a.request_changes, a.evidence, a.note, day,
                changes=bool(a.request_changes))
        return 0

    r = build_today(sched, nick, day)
    if a.note_file:
        write_note(r)
        return 0
    if a.json:
        r["nick_source"] = how
        print(json.dumps(r, ensure_ascii=False, indent=1))
    else:
        print_today(r)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:  # vd. khi pipe sang `head`
        sys.exit(0)
