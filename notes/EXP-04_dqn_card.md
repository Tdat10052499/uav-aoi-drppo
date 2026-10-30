# EXP-04 — DR-DQN: đối chứng thuật toán (RQ3)

**Owner:** FAO (Nguyễn Minh Chính) · **Second reader:** DAT
**Viết:** 20/10/2026, trước khi chạy · **Pha 0 (kiểm tra pipeline):** W2-FAO-03, hạn 29/10, issue #17 · **Pha chính:** W5–W6 (16–29/11)

## D. Experiment card

```text
Experiment ID: EXP-04
Owner / second reader: FAO / DAT
Thăm dò hay khẳng định: Pha 0 = kiểm tra pipeline, không có con số nào vào bài.
  Pha chính = khẳng định (RQ3), cấu hình khoá trong docs/PREREG.md tại G1.

Câu hỏi: Ở cùng ngân sách bước và cùng quan sát, DQN (thuật toán off-policy) so với
DR-PPO thế nào trên id và 4 bộ OOD?
Giả thuyết: chưa đặt hướng; RQ3 chỉ so sánh (docs/01 §4). Ghi vào PREREG trước pha chính.

Biến thay đổi: thuật toán (DQN so với MaskablePPO), cùng TRAIN_DR
Điều kiện cố định: SmallCNN, quan sát 5×31×31, configs/env_default.json, λ = 0,1
Đối chứng: DR-PPO (EXP-03), TSP và Random (EXP-01)
Kiểm soát: cùng số bước, cùng seed huấn luyện, cùng 100 kịch bản đánh giá.
  Khác biệt đã biết: DQN không có action mask (SB3 DQN không hỗ trợ), nên hành động
  ra ngoài vùng bị kẹp tại biên kèm phạt μ. Phải báo cáo boundary_hits của DQN và nêu
  khác biệt này trong bài.
Ngân sách: pha chính bằng DR-PPO (chốt tại G1). Pha 0: 10k bước.
Bộ đánh giá: id, ood_cluster, ood_density, ood_area, ood_energy (seed 100000–100099)
Chỉ số: như EXP-03 (Ā, deg, năng lượng, tỷ lệ hover/chậm/nhanh, chạm biên)
Đơn vị lặp: seed huấn luyện (pha chính 10 seed)
Thứ tự chạy: pha 0 trước; pha chính sau khi PREREG khoá
Phân tích: scripts/analyze.py, như EXP-03
Thất bại: giữ run_record failed; hết RAM thì ghi lỗi và giảm --dqn-buffer-size, ghi lý do
Chi phí: bộ nhớ replay ≈ 2 × buffer × 4805 × 4 byte (obs và next_obs, float32):
  200k chuyển tiếp ≈ 7,7 GB; 20k ≈ 0,8 GB. Thời gian: đo ở pha 0.

Kỳ vọng nếu đúng (pha 0): chạy hết 10k bước, có cập nhật gradient (learning_starts < số bước),
  sinh model.zip + run_record; plot_trajectory.py vẽ được quỹ đạo từ model
Kết quả làm yếu: không áp dụng cho pha 0
Tiêu chí tiếp tục: pha 0 đạt → chốt buffer_size cho pha chính theo RAM của máy chạy
  (ghi vào PREREG và DECISIONS.md nếu khác 200k)
Trường raw cần: run_record.json (checkpoint_digest, steps_per_s), config.json (args)
```

## Câu hỏi mở cho DAT (trước G1)
- `buffer_size` cho pha chính: 200k (≈ 7,7 GB) có chạy được trên máy nào? Laptop FAO chỉ còn ≈ 3,4 GB trống (20/10), nên **không** chạy được 200k. Nếu giảm, giảm bao nhiêu và ghi vào DECISIONS.md.
- Siêu tham số DQN có tinh chỉnh bằng Optuna với cùng ngân sách như PPO không (docs/03: ngân sách tinh chỉnh bằng nhau)?

## Lệnh

```bash
# Pha 0: kiểm tra pipeline (buffer nhỏ, cập nhật bắt đầu sớm)
python scripts/train_ppo.py --experiment-id EXP-04 --algo dqn --train dr --seed 0 --timesteps 10000 \
       --dqn-buffer-size 20000 --dqn-learning-starts 1000
python scripts/plot_trajectory.py --model runs/EXP-04/<run-id>/model.zip --label dqn_10k --suite ood_cluster --seed 100000
```

## Kết quả pha 0 (FAO điền sau khi chạy — Form C)

```text
Máy: Laptop FAO (i7-8665U, 16 GB, không GPU) / Windows 11 / Python 3.14.3 / torch 2.14.1+cpu / SB3 2.9.0
train DQN 10k: OK — run EXP-04/dr_dqn_lam0.1_s0_20261020-094810 (buffer 20k, learning_starts 1000);
  10000 bước, ≈ 2050 cập nhật gradient; status completed; SHA256 model.zip trong run_record.json
wall_time_s = 511.5  steps_per_s = 19.5  (KHÔNG dùng cho bài; chậm hơn MaskablePPO ≈ 3,5 lần trên cùng máy)
RAM đỉnh (Task Manager, "In use"): 11,6 → 12,0 GB, tức ≈ +0,4 GB (buffer đầy 10k/20k ≈ 0,38 GB, khớp ước lượng)
Quỹ đạo: figures/traj_dqn_10k_ood_cluster_100000.png — vẽ được: có. Sau 10k bước chính sách chưa học:
  không hover lần nào (coverage 0, Ā = 151,50 > Random 132,09), 1 lần chạm biên (DQN không có mask).
  Chỉ là kiểm tra pipeline, không phải kết quả.
Second reader (DAT): ___  ngày: ___
```
