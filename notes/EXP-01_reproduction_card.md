# EXP-01 — Tái lập môi trường & baseline trên máy nhóm

**Owner:** FAO (Nguyễn Minh Chính) · **Second reader:** DAT
**Viết:** 17/10/2026, trước khi chạy (Form D, `notes/workbook_forms.md`)
**Hạn:** 22/10/2026 · **Issue:** #5

## D. Experiment card

```text
Experiment ID: EXP-01
Owner / second reader: FAO / DAT
Thăm dò hay khẳng định: khẳng định (tái lập phải khớp tuyệt đối vì môi trường tất định)

Câu hỏi: Bộ mã có chạy và cho đúng cùng con số trên máy của nhóm như khi dựng không?
Giả thuyết: smoke test PASS; 14/14 kiểm thử đạt; heuristic 100 episode/bộ trùng từng
episode với results/raw/heuristics/heuristics_100ep_2026-10-16.csv.

Biến thay đổi: máy chạy (máy FAO; lặp lại trên máy DAT hoặc LDN)
Điều kiện cố định: commit đã ghim; configs/env_default.json; data/eval_manifest.json
Đối chứng: file tham chiếu 16/10/2026
Kiểm soát: digest kịch bản phải khớp manifest trước khi so sánh số
Ngân sách: không áp dụng
Bộ đánh giá: cả 5 bộ, seed 100000–100099
Chỉ số: mean_aoi từng episode; sai số chấp nhận 1e-9 (cùng NumPy) hoặc giải trình nếu khác phiên bản NumPy
Đơn vị lặp: episode (tất định, không có seed huấn luyện)
Thứ tự chạy: (1) tests  (2) smoke test  (3) evaluate heuristic  (4) train_ppo 10k bước  (5) đo 100k bước
Phân tích: so khớp từng dòng CSV với tham chiếu (diff), báo cáo số dòng lệch
Thất bại: lưu nguyên log + run_record status=failed; mở issue kèm ví dụ nhỏ nhất
Chi phí: ~2 phút cho (1)–(3); (4) vài phút; (5) đo thực tế

Kỳ vọng nếu đúng: 0 dòng lệch; train_ppo chạy hết 10k bước, sinh model.zip + run_record
Kết quả làm yếu: lệch số do khác phiên bản NumPy/Python → ghi Form C, không sửa số tham chiếu
Tiêu chí tiếp tục: (1)–(4) đạt trên ≥ 2 máy → mở EXP-02
Trường raw cần: events.csv, run_record.json (steps_per_s)
```

## Lệnh

```bash
pip install -r environment/requirements.txt
python tests/test_core.py
python scripts/run_smoke_test.py
python scripts/evaluate.py --experiment-id EXP-01 --method tsp greedy_aoi random --episodes 100
python scripts/train_ppo.py --experiment-id EXP-01 --train dr --seed 0 --timesteps 10000 --masked --n-envs 2
python scripts/train_ppo.py --experiment-id EXP-01 --train dr --seed 0 --timesteps 100000 --masked --n-envs 8
```

## Kết quả (FAO điền sau khi chạy — Form C)

```text
Máy / OS / Python / NumPy / torch: Laptop FAO (i7-8665U, 16 GB, không GPU) / Windows 11 10.0.26300 / 3.14.3 / 2.5.4 / 2.14.1+cpu
tests: 14/14   smoke: PASS (20/10/2026)
Số dòng lệch so với tham chiếu: 0/1500 (mean_aoi, sai số 1e-9) — run EXP-01/20261020-084218; NumPy 2.5.4 vẫn tái lập đúng tham chiếu sinh bằng 2.5.3
train_ppo 10k: OK, không cần sửa mã — run EXP-01/dr_ppo_mask_lam0.1_s0_20261020-090719; 10240 bước, 122 s (~84 bước/s, MaskablePPO, n_envs=2, laptop FAO, CPU; KHÔNG dùng cho bài); SHA256 model.zip trong run_record.json
100k bước: wall_time_s = ___  steps_per_s = ___  (n_envs=8)
Second reader (DAT) chạy lại trên máy: ___  ngày: ___
```