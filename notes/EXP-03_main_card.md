# EXP-03 — Thí nghiệm chính DR-PPO vs Fixed-PPO, 10 seed (bằng chứng cho H1, H2 — bài FJCAI)

**Owner:** DAT (huấn luyện) · **Phân tích:** LDN · **Second reader:** FAO
**Viết:** 03/11/2026, trước khi chạy (Claude soạn cho DAT, DAT duyệt 03/11)
**Chạy:** sau khi khoá PREREG (tag `prereg-lock`), 04/11–10/11/2026

## D. Experiment card

```text
Experiment ID: EXP-03
Owner / second reader: DAT (train) + LDN (analysis) / FAO
Thăm dò hay khẳng định: KHẲNG ĐỊNH. Giả thuyết, ngưỡng và phân tích theo docs/PREREG.md
  (khoá trước khi chạy). Không xem kết quả từng phần để đổi phân tích.

Câu hỏi: DR có làm giảm độ suy giảm OOD của PPO so với cùng learner huấn luyện trên một
  bố trí cố định không, khi không huấn luyện lại?
Giả thuyết: theo PREREG (H1: deg(DR) < deg(Fixed) trên các bộ OOD; H2 theo PREREG).

Biến thay đổi: phân phối huấn luyện {TRAIN_DR, TRAIN_FIXED}
Điều kiện cố định: MaskablePPO, SmallCNN, siêu tham số mặc định train_ppo.py, λ=0,1,
  configs/env_default.json, 2.000.000 bước, commit = prereg-lock
Đối chứng: Fixed-PPO; Random, Greedy, TSP (cùng 100 seed đánh giá)
Kiểm soát: cùng kiến trúc, ngân sách, seed huấn luyện {0..9} cho hai nhánh; đánh giá
  trên 100 kịch bản cố định (seed 100000–100099)
Bộ đánh giá: id, ood_cluster, ood_density, ood_area, ood_energy
Chỉ số: Ā (khe), deg = (Ā_ood − Ā_id)/Ā_id theo từng seed; phụ: năng lượng, tỷ lệ hết pin,
  tỷ lệ hover/chậm/nhanh, chạm biên, peak AoI (mô tả)
Đơn vị lặp: seed huấn luyện (n = 10/nhánh)
Thống kê: bootstrap 95% CI, IQM, kiểm định hoán vị một phía, Holm trên 4 bộ OOD, Cliff's δ
Thứ tự chạy: 2 tiến trình song song, một tiến trình DR và một tiến trình Fixed, seed tăng dần
  0→9 (cả hai nhánh luôn ở cùng seed, tránh trôi máy lệch một nhánh)
Thất bại: theo tiêu chí loại của PREREG; mọi lần chạy hỏng hoặc chạy lại được liệt kê
Chi phí: 20 × 2M = 40M bước; ước tính 17–29 giờ máy trên laptop DAT (chưa đo ở 2M)
Mốc: ≥ 5 seed/nhánh trước 10/11 (điều kiện dừng FJCAI)
Phân tích: scripts/analyze.py → results/processed/EXP-03_summary.md; LDN
Trường raw cần: events.csv, run_record.json (checkpoint_digest, steps_per_s)
```

## Lệnh (PowerShell, mỗi cửa sổ một nhánh)

```powershell
# Cửa sổ 1 — DR
foreach ($s in 0..9) { python scripts/train_ppo.py --experiment-id EXP-03 --train dr --masked --seed $s --timesteps 2000000 }
# Cửa sổ 2 — Fixed
foreach ($s in 0..9) { python scripts/train_ppo.py --experiment-id EXP-03 --train fixed --masked --seed $s --timesteps 2000000 }
```

Đánh giá từng model theo mẫu lệnh của EXP-02, với `--experiment-id EXP-03`.
