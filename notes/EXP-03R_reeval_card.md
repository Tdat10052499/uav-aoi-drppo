# EXP-03R — Đánh giá lại 2 model EXP-03 để kiểm tái lập (W5-FAO-04, second reader)

**Owner:** FAO · **Second reader:** DAT (đối chiếu model và SHA256)
**Viết:** 06/11/2026, trước khi chạy (Claude soạn cho FAO)
**Chạy:** trên laptop FAO, tại commit `prereg-lock` (b5cd784), sau khi viết card này

## D. Experiment card

```text
Experiment ID: EXP-03R
Owner / second reader: FAO / DAT
Thăm dò hay khẳng định: KIỂM TÁI LẬP. Không sinh số mới cho bài; không kiểm giả thuyết nào.
Câu hỏi: Đánh giá lại model EXP-03 trên máy khác, cùng mã khoá, có ra đúng events.csv gốc không?
Cách chọn model: cơ học, không xem kết quả (đề xuất của DAT, FAO chấp nhận 06/11):
  random.Random("641922ca31c32fc442a9ddd0f6fe19b9e04f9637") (commit raw EXP-03), gọi
  randrange(10) hai lần → DR seed 7, rồi Fixed seed 5. Claude đã chạy lại 06/11 và ra cùng kết quả.
Model:
  dr_ppo_mask_lam0.1_s7_20261105-234718     sha256 617efd7caa545dde2b0e47f395def741a0e135ca32fd08b9cd73c8c44d1b83d9
  fixed_ppo_mask_lam0.1_s5_20261105-194100  sha256 58733dd39e5bfd76a67b779f1cc1e886613d72a51fc0803e4997b30163cc9865
  (khớp checkpoint_digest của run train và run eval gốc; nhận qua Drive của DAT 06/11)
Điều kiện cố định: commit prereg-lock, cấu hình mặc định (--config không truyền, như run gốc),
  5 bộ id, ood_cluster, ood_density, ood_area, ood_energy; 100 episode, seed 100000–100099;
  nhãn dr_ppo / fixed_ppo, train_seed 7 / 5 (giống config.json của eval_dr_ppo_s7, eval_fixed_ppo_s5)
Đối chứng: results/raw/EXP-03/eval_dr_ppo_s7/events.csv, results/raw/EXP-03/eval_fixed_ppo_s5/events.csv
Khác biệt có chủ ý: máy (laptop FAO thay vì LAPTOP-21KJQDU4 của DAT); venv Python 3.12 riêng (xem
  "Sửa trước khi chạy"); phiên bản thư viện ghi trong environment.json. Run gốc: Python 3.12.0, numpy 2.5.4, torch 2.14.1+cpu, SB3 / sb3_contrib 2.9.0.
Chỉ số: so từng dòng bằng scripts/compare_events.py (khoá method, train_seed, suite, episode_seed;
  atol 1e-9, rtol 0), 500 dòng mỗi model.
Kết quả kỳ vọng: MATCH 500/500 cho cả hai model.
Kết quả làm yếu: có dòng lệch. Khi đó không chạy lại để "chữa"; ghi số dòng lệch, cột lệch và
  độ lệch lớn nhất, so phiên bản thư viện, rồi báo DAT và LDN trước khi số EXP-03 vào bài.
  Lệch chỉ ở số thực rất nhỏ (< 1e-6) mà các cột nguyên và chuỗi hành động khớp thì ghi là
  "khớp trong sai số dấu phẩy động", kèm atol đã dùng, không đổi tiêu chí sau khi xem.
Đơn vị lặp: không áp dụng (kiểm tái lập, không thống kê).
Thời gian: không dùng làm số đo thời gian (quy tắc 4 CLAUDE.md).
Raw: results/raw/EXP-03R/reeval_dr_ppo_s7/, results/raw/EXP-03R/reeval_fixed_ppo_s5/
Lưu ý phân tích: EXP-03R KHÔNG được đưa vào glob phân tích EXP-03. Lệnh chính thức dùng
  results/raw/EXP-03/*/events.csv; glob mẫu "EXP-0*" trong docstring analyze.py sẽ bắt cả
  EXP-03R, nên không dùng glob đó cho EXP-03.
Ghi kết quả: notes/review_log.md (cách chọn + kết quả), status W5-FAO-04.
```

## Lệnh (PowerShell, laptop FAO)

Chạy trong một git worktree tại `prereg-lock` để `code_revision` ghi b5cd784 mà không đụng checkout chính.
Model đặt cạnh `config.json` của run train để `evaluate.py` kiểm `env_cfg` (tại `prereg-lock`, `results/raw/EXP-03` chưa có trong cây).

```powershell
cd C:\Users\nguye\Documents\uav-aoi-drppo
git pull --rebase
git fetch --tags
git worktree add ..\uav-lock prereg-lock
$dr = "dr_ppo_mask_lam0.1_s7_20261105-234718"; $fx = "fixed_ppo_mask_lam0.1_s5_20261105-194100"
foreach ($r in $dr, $fx) {
  New-Item -ItemType Directory -Force ..\uav-lock\runs\EXP-03\$r | Out-Null
  Copy-Item results\raw\EXP-03\$r\config.json ..\uav-lock\runs\EXP-03\$r\
}
# chép 2 file model.zip tải từ Drive vào ..\uav-lock\runs\EXP-03\<run>\model.zip
cd ..\uav-lock
$py = "..\uav-aoi-drppo\.venv\Scripts\python.exe"
& $py scripts\evaluate.py --experiment-id EXP-03R --run-id reeval_dr_ppo_s7 --model runs\EXP-03\$dr\model.zip --label dr_ppo --train-seed 7 --episodes 100
& $py scripts\evaluate.py --experiment-id EXP-03R --run-id reeval_fixed_ppo_s5 --model runs\EXP-03\$fx\model.zip --label fixed_ppo --train-seed 5 --episodes 100
& $py scripts\compare_events.py ..\uav-aoi-drppo\results\raw\EXP-03\eval_dr_ppo_s7\events.csv results\raw\EXP-03R\reeval_dr_ppo_s7\events.csv
& $py scripts\compare_events.py ..\uav-aoi-drppo\results\raw\EXP-03\eval_fixed_ppo_s5\events.csv results\raw\EXP-03R\reeval_fixed_ppo_s5\events.csv
```

## Sửa trước khi chạy (06/11, 20:30)

Lần chạy đầu trên venv chính của laptop FAO (Python 3.14.3) **không tạo run nào**: `MaskablePPO.load` làm Python dừng với "Windows fatal exception: access violation" (exit −1073741819 = 0xC0000005). `faulthandler` chỉ ra khung `D:\github\uav-aoi-drppo\scripts\train_ppo.py ... in __init__`, tức `SmallCNN.__init__`.
- Nguyên nhân (suy luận từ traceback, chưa kiểm trên máy khác): `SmallCNN` định nghĩa trong `scripts/train_ppo.py`, chạy dưới tên `__main__`, nên cloudpickle lưu lớp này **theo giá trị**, kèm bytecode của Python 3.12 (máy DAT). Bytecode không tương thích giữa các bản Python phụ, nên nạp bằng 3.14 thì sập.
- Hệ quả: model EXP-03 chỉ nạp được bằng Python 3.12. Laptop LDN (3.11.9) cũng sẽ gặp lỗi này.
- Cách xử lý cho EXP-03R: tạo venv Python 3.12 riêng với đúng phiên bản thư viện của run gốc (numpy 2.5.4, torch 2.14.1+cpu, gymnasium 1.4.0, SB3 và sb3_contrib 2.9.0, scipy 1.18.1). Mã và lệnh không đổi; chỉ đổi đường dẫn `$py`. Không sửa `evaluate.py` (phải chạy ở commit khoá).
- Không có thư mục raw nào được tạo ở lần lỗi: `evaluate.py` nạp model trước `new_run_dir`.

## Kết quả

(điền sau khi chạy)
