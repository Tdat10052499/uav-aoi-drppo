# FAO kiểm raw EXP-03, tb log và PR #41, #45 (06/11/2026, second reader)

Trả lời `notes/yeu-cau/2026-11-06_dat_can-FAO-LDN_raw-EXP-03.md`. Claude chạy kiểm trong container trên `main` (sau c834009); FAO duyệt.

## 1. Provenance 42 run EXP-03 (commit 641922c)

- 42 thư mục: 21 train (DR 11, Fixed 10), 20 eval, `heuristics_lock`. Khớp dòng đính chính của DAT.
- Cả 42 `run_record.json` có `code_revision` = b5cd784 (`prereg-lock`) và `uncommitted_patch_path` = null.
- 20 run eval: `checkpoint_digest` khớp từng run train cùng nhánh, cùng seed (run DR s3 dùng là `..._s3_20261105-140316`).
- Mỗi run eval có đủ 5 bộ × 100 episode, seed 100000–100099, nhãn đúng nhánh.
- `heuristics_lock` so với EXP-01 `20261025-115153` bằng `scripts/compare_events.py`: **MATCH 1500/1500 dòng** (Random, Greedy-AoI, TSP). PREREG §9 tiêu chí 4 thoả cho heuristic.
- `heuristics_lock` và run dở DR s3 ghi `checkpoint_digest` = "not-applicable", đúng vì không có model.
- Run dở `dr_ppo_mask_lam0.1_s3_20261104-202500`: `status` = running, `started_at` 20:25:00, `finished_at` trống, `metrics` = {}, không có model. Không có dấu hiệu chọn lọc theo kết quả.

## 2. Tb log (c834009)

- `SHA256SUMS.txt` của `results/raw_tb/EXP-02b` và `results/raw_tb/EXP-03`: tất cả file OK.
- Tb log của run dở s3: sự kiện đầu 20:25:06, cuối 20:25:36 (+07), bước lớn nhất 16 384. Khớp dòng đính chính ở PR #41.
- Đường cong EXP-02b s0 trùng EXP-03 DR s0, khớp việc cùng mã huấn luyện giữa 9152d06 và b5cd784.

## 3. Đường học (yêu cầu P1, thăm dò, chỉ mô tả)

`ep_rew_mean`, trung bình 10 seed mỗi nhánh, đọc từ tb log (Claude viết bộ đọc TFRecord riêng, không cài tensorboard):

| Nhánh | 100k | 200k | 300k | 500k | 1M | 1,5M | 2M |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DR | −145,9 | −140,4 | −129,3 | −96,4 | −79,4 | −72,6 | −73,0 |
| Fixed | −131,9 | −112,0 | −87,9 | −68,7 | −63,8 | −63,5 | −62,1 |

- DR gần như phẳng tới 200k; tăng mạnh nhất trong 300k–1M; gần như không đổi từ 1,5M tới 2M.
- Hệ quả (suy luận, chưa kiểm): trial Optuna 200k bước cho DR khó phân biệt cấu hình. Thêm bước sau 2M khó cứu H1 với cùng thiết kế.
- `ep_rew_mean` là reward huấn luyện (có phạt năng lượng λ), không phải Ā trên bộ đánh giá. Không dùng bảng này làm số cho bài.

## 4. PR #41 (đã merge 5e09aa1)

Diff thật của PR sau bản FAO duyệt (e56173a) chỉ là dòng đính chính run DR s3 trong `docs/DECISIONS.md` (5b27de8, be8ae59, 10650e4). Các thay đổi khác đến từ merge `main`.
- Giờ bắt đầu, giờ log cuối và bước 16 384 khớp raw và tb log (mục 1, 2).
- "Không bắt được Exception thì không ghi failed" khớp `scripts/train_ppo.py` tại `prereg-lock` (dòng 145–146).
- Không kiểm được system log trên máy DAT (Kernel-Power 42, 19:15–02:30). Phần này dựa vào DAT.
- Ghi thêm, không chặn: Ctrl+C (`KeyboardInterrupt`) cũng để lại `running`, nên `running` không phân biệt được đóng cửa sổ hay Ctrl+C. Kết luận không đổi: run dở bị loại, chạy lại cùng seed.
- **Duyệt.**

## 5. PR #45 (đã merge cb018c9), diff 0c207f2..cd62a0b

- A1: tour tiến theo cảm biến thật sự được phục vụ (`n_served`). Đã sửa.
- A2: `check_confirmatory` chặn 4 bộ mới trước tag; `--probe-b` chỉ cho heuristic và ghi vào run_record. Đã sửa.
- Biên năng lượng: `_flight_slots` chia cos(π/8); `_energy_need` thêm 1 khe dự phòng.
- cd62a0b (L1): `RESERVED_EVAL_SEEDS`, `train_reset_seeds`, `reserved_overlap`, `--reset-seed-scheme spaced|sb3`, kiểm danh sách seed reset dự kiến khớp seed thật.
- Test 27/27, smoke PASS.
- **Duyệt sau merge.** W4-FAO-03 và W4-FAO-04 đánh dấu xong với bằng chứng là review này, theo mục 5 của `notes/yeu-cau/2026-11-06_dat_can-FAO-LDN_phuong-phap-moi.md`.

## 6. W5-FAO-04

- Chấp nhận cách chọn của DAT. Claude chạy lại `random.Random("641922ca…9637")`, `randrange(10)` × 2 và ra 7, 5.
- Card: `notes/EXP-03R_reeval_card.md`. Chạy trên laptop FAO tại `prereg-lock`, experiment id riêng EXP-03R để không lẫn vào glob `results/raw/EXP-03/*`.
- **Kết quả (06/11 tối):** DR s7 và Fixed s5 MATCH 500/500, `events.csv` trùng từng byte với run gốc (raw c9b1896). Venv Python 3.12.10, vì model không nạp được bằng 3.14. Một run DR dở (67/500, cửa sổ bị đóng) được giữ lại và loại. Theo quy tắc 3, số EXP-03 qua được bước second reader này.

## 7. Số chính thức EXP-03 của LDN (7de532d)

Chạy lại `scripts/analyze.py results/raw/EXP-03/*/events.csv` trên `main`: `results/processed/EXP-03_summary.md` trùng từng dòng với bản LDN commit (SHA256 fb14d4b2…), trừ dòng đường dẫn hình. Cùng với W5-FAO-04 (§6), số EXP-03 đã được kiểm độc lập. LDN chuyển C1, C2 trong `results/analysis/claim_evidence.md` sang *independently checked* khi điền số; C1 và C2 đều **không được ủng hộ**.
