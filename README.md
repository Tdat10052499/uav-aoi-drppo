# Generalizable AoI- and Energy-Aware UAV Trajectory Planning for IoT Data Collection via Domain-Randomized PPO

**Team:** Hồ Du Tuấn Đạt (DAT) · Dương Ngọc Linh Đan (LDN) · Nguyễn Minh Chính (FAO)
**Supervisor:** Dr. Nguyễn Trí Hải
**Target:** chưa chốt; ứng viên AIEI 2027 (hạn 15/02/2027), IEEE SMC 2027 (hạn 15/04/2027, chưa xác minh trang chính thức), FJCAI/ICISN 2027 (chưa công bố hạn)
**Working deadline:** bản thảo sẵn sàng **10/01/2027** (Gate G3)

> ### Status, 17/10/2026
> Bộ khởi đầu: môi trường mô phỏng, heuristic, thống kê, 13/13 kiểm thử, smoke test và kết quả heuristic tham chiếu. `scripts/train_ppo.py` **chưa từng chạy với PyTorch** (issue #5, FAO).
>
> ### Read this first
> - **Mỗi sáng:** `git pull`, mở Claude Code trong thư mục repo, hỏi **"hôm nay tôi cần làm gì?"** (hoặc chạy `python scripts/today.py`). Chi tiết ở mục *Daily workflow* bên dưới.
> - [`schedule/SCHEDULE.md`](schedule/SCHEDULE.md): lịch theo ngày của cả 3 người, sinh từ `schedule/tasks.json`.
> - [`docs/05_ke_hoach.md`](docs/05_ke_hoach.md) là **kế hoạch hiện hành**: lịch theo ngày/tuần cho DAT, LDN, FAO và tiêu chí gate G0–G3.
> - Ghi chú riêng: [`notes/NOTE_FOR_DAT.md`](notes/NOTE_FOR_DAT.md) · [`notes/NOTE_FOR_LDN.md`](notes/NOTE_FOR_LDN.md) · [`notes/NOTE_FOR_FAO.md`](notes/NOTE_FOR_FAO.md)
> - [`Project Agreement.md`](Project%20Agreement.md): GVHD góp ý bằng dòng `%%GVHD:`.

---

## Research question

Khi bố trí, mật độ cảm biến, diện tích hoặc năng lượng dịch chuyển khỏi phân phối huấn luyện, PPO huấn luyện với domain randomization có giữ tuổi thông tin (AoI) tốt hơn PPO huấn luyện trên một bố trí cố định không? Bài toán dùng AoI nhiều chu kỳ, năng lượng đẩy phụ thuộc tốc độ, và so sánh ở cùng ngân sách huấn luyện. Chi tiết: `docs/01_de_cuong.md`.

---

## Repository layout

```
uav-aoi-drppo/
  CLAUDE.md              hướng dẫn cho Claude (đọc tự động); skill .claude/skills/hom-nay, ket-thuc-ngay
  Project Agreement.md   Form A — câu hỏi, giả thuyết, tiêu chí dừng, phân công
  schedule/              tasks.json (lịch theo ngày), status/<NICK>.json, SCHEDULE.md (tự sinh)
  environment/           requirements.txt, machine_notes.md
  configs/               env_default.json (cấu hình môi trường đã khoá)
  src/uavaoi/            môi trường, năng lượng, kênh, kịch bản, heuristic, thống kê, run record
  scripts/               evaluate, train_ppo, analyze, run_smoke_test, build_eval_manifest
  tests/                 kiểm thử giả định khoa học (AoI, năng lượng, mask, chống dừng sớm, provenance)
  notes/                 forms, experiment cards, ghi chú ngày, gate report, ghi chú đọc
  data/                  eval_manifest.json (seed + SHA256 kịch bản), checkpoint_manifest.md
  results/
    raw/                 đầu ra gốc, CHỈ GHI THÊM (mỗi lần chạy một thư mục + run_record.json)
    processed/           tóm tắt sinh từ raw
    analysis/            claim_evidence.md, digest
  figures/               hình sinh từ script
  paper/                 main.tex, references.bib
  docs/                  đề cương, mô hình, giao thức, tài liệu, kế hoạch, dàn ý, rủi ro
```

**Quan trọng:** `results/raw/` chỉ ghi thêm. `new_run_dir()` từ chối ghi đè. Sửa script phân tích thì sinh lại kết quả từ cùng file raw.

---

## Environment setup

```bash
git clone https://github.com/Tdat10052499/uav-aoi-drppo.git
cd uav-aoi-drppo
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r environment/requirements.txt
```
Môi trường, heuristic, thống kê và kiểm thử chạy được chỉ với NumPy. Huấn luyện cần PyTorch, Gymnasium, Stable-Baselines3 và sb3-contrib.

## Daily workflow

**Thiết lập một lần** (sau khi clone và cài môi trường):
```bash
python scripts/today.py --set-nick LDN     # hoặc DAT / FAO; lưu vào .nick (không commit)
```
Cài [Claude Code](https://claude.com/claude-code) (CLI hoặc tab Code trong ứng dụng Claude desktop), rồi mở nó **trong thư mục repo**. Claude tự đọc `CLAUDE.md` và các skill trong `.claude/skills/`.

**Mỗi ngày**
1. Hỏi Claude: *"hôm nay tôi cần làm gì?"*. Claude sẽ:
   - `git pull`;
   - chạy `scripts/today.py`;
   - liệt kê việc quá hạn → cần review → hôm nay;
   - tách phần Claude làm với phần bạn tự làm;
   - hỏi bắt đầu từ đâu, rồi làm cùng bạn theo quy tắc RIVF (card trước khi chạy, run record, raw chỉ ghi thêm, PR cho `src/`).
2. Cuối ngày nói *"kết thúc ngày"*. Claude sẽ:
   - điền ghi chú ngày `notes/<ngày>_<nick>.md` (Form H);
   - đánh dấu task `--done` kèm bằng chứng;
   - commit và push.

Không dùng Claude Code? Chạy thẳng các lệnh:
```bash
python scripts/today.py                                  # việc của tôi hôm nay
python scripts/today.py --start W1-LDN-02                # bắt đầu task
python scripts/today.py --done W1-LDN-02 --evidence "notes/reading/agarwal2021deep_LDN.md"
python scripts/today.py --approve W1-FAO-02 --evidence "review_log dòng 2"   # second reader
python scripts/today.py --note-file                      # khung ghi chú ngày
python scripts/today.py --team                           # cả nhóm
```
Lịch (`schedule/tasks.json`) chỉ DAT sửa, qua PR. Trạng thái của mỗi người nằm ở file riêng `schedule/status/<NICK>.json`, nên không có xung đột khi merge.

## Smallest experiment (smoke test)

Lệnh này **phải báo lỗi rõ ràng** nếu thiếu file hoặc kết quả bị lệch:
```bash
python tests/test_core.py            # kỳ vọng 14/14 passed
python tests/test_schedule.py        # kỳ vọng 12/12 passed (lịch và today.py)
python scripts/run_smoke_test.py     # kỳ vọng SMOKE TEST PASSED
```
Smoke test kiểm tra ba điều:
1. các file bắt buộc có mặt;
2. bộ sinh kịch bản vẫn khớp SHA256 trong `data/eval_manifest.json`;
3. TSP tái lập đúng từng episode của kết quả tham chiếu.

## Experiments

| ID | Nội dung | Owner / second reader | Card |
| --- | --- | --- | --- |
| EXP-01 | Tái lập trên máy nhóm, đo tốc độ | FAO / DAT | `notes/EXP-01_reproduction_card.md` |
| EXP-02 | Pilot DR-PPO vs Fixed-PPO (2 seed) → G1 | DAT + LDN / FAO | `notes/EXP-02_pilot_card.md` |
| EXP-03 | Khẳng định chính, 10 seed | LDN / FAO | viết trước 15/11 |
| EXP-04 | DR-DQN | FAO / DAT | |
| EXP-05 | Quét λ (RQ2) | LDN / DAT | |
| EXP-06 | Ablation quan sát A2/A3 | DAT / FAO | |
| EXP-07 | Ablation mask/tốc độ A4/A5 | FAO / LDN | |

```bash
python scripts/train_ppo.py --experiment-id EXP-02 --train dr --seed 0 --timesteps 300000 --masked
python scripts/evaluate.py  --experiment-id EXP-02 --model runs/EXP-02/<run-id>/model.zip --label dr_ppo --train-seed 0
python scripts/analyze.py results/raw/EXP-02/*/events.csv --out results/processed/EXP-02_summary.md
```

## Provenance

- Mỗi lần chạy sinh `run_record.json` (Form E) gồm: commit, patch nếu working tree chưa commit, cấu hình, môi trường, seed, thời điểm, chỉ số, SHA256 checkpoint.
- Checkpoint chính sách nằm ngoài git (`runs/`); SHA256 ghi trong `data/checkpoint_manifest.md` (owner FAO).

## Key dates

| Ngày | Mốc |
| --- | --- |
| 19/10 (Day 0) | Khởi động; gửi Project Agreement cho GVHD |
| 22/10 | EXP-01 xong trên ≥ 2 máy |
| 25/10 | GVHD duyệt ngưỡng gate |
| **01/11** | **G0** — định vị đóng góp |
| **15/11** | **G1** — pilot; khoá PREREG; chọn phương án A/B |
| **20/12** | **G2** — đóng băng kết quả |
| **10/01/2027** | **G3** — bài báo và đồ án sẵn sàng |

### G1 kill gate (15/11) — tiếp tục **chỉ khi** đạt (chi tiết `docs/05` §5)
- Smoke test PASS trên ≥ 2 máy.
- DR-PPO trên `id`: Ā ≤ 63,1 khe (0,5 × Random) ở cả 2 seed.
- deg(DR) < deg(Fixed) trên `ood_cluster` và ≥ 1 bộ OOD khác, ở cả 2 seed.
- Không suy biến: chạm biên = 0 khi có mask; không loại hành động nào chiếm ≥ 90%.
- Ngân sách tính toán đủ cho EXP-03 đến EXP-07 trước 13/12.

## Measurement rules
- **Số đo thời gian:** chỉ từ một máy cố định (do DAT chỉ định). Không lấy từ Kaggle/Colab.
- **Ghép cặp:** mọi phương pháp đánh giá trên cùng 100 kịch bản (seed 100000–100099).
- **Đơn vị lặp:** seed huấn luyện. Kết quả chính ≥ 10 seed, CI bootstrap 95%, IQM, Holm.

## Student responsibilities

| Student | Primary tasks | Second reader |
| --- | --- | --- |
| Hồ Du Tuấn Đạt (DAT) | DR-PPO, Optuna, biến thể quan sát, định vị G0, điều phối, đo thời gian, chủ trì bản thảo | FAO hoặc LDN |
| Dương Ngọc Linh Đan (LDN) | Ma trận thực nghiệm, thống kê, gate report, claim–evidence, hình F3–F5, tổng quan hệ thống | FAO hoặc DAT |
| Nguyễn Minh Chính (FAO) | Môi trường & tái lập, chi phí tính toán, provenance checkpoint, DQN, quỹ đạo, tái lập độc lập tại G2 | DAT hoặc LDN |
