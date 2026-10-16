# EXP-02 — Pilot DR-PPO vs Fixed-PPO (bằng chứng cho Gate G1)

**Owner:** DAT (huấn luyện) · **Phân tích:** LDN · **Second reader:** FAO
**Viết:** 17/10/2026, trước khi chạy · **Chạy:** 02/11–12/11/2026 · **Gate:** G1 (15/11), issue #2

## D. Experiment card

```text
Experiment ID: EXP-02
Owner / second reader: DAT (train) + LDN (analysis) / FAO
Thăm dò hay khẳng định: THĂM DÒ (pilot). Chỉ dùng để quyết định tại G1, không đưa
p-value vào bài. Kết quả khẳng định đến từ EXP-03 với 10 seed.

Câu hỏi: Domain randomization có tạo tín hiệu giảm độ suy giảm OOD so với huấn luyện
trên một bố trí cố định không, và PPO có học được bài toán ở mức hợp lý không?
Giả thuyết: deg(DR-PPO) < deg(Fixed-PPO) trên ood_cluster và ít nhất 1 bộ OOD khác,
ở cả 2 seed; DR-PPO trên id đạt AoI ≤ 0,5 × Random.

Biến thay đổi: phân phối huấn luyện {TRAIN_DR, TRAIN_FIXED}
Điều kiện cố định: MaskablePPO, SmallCNN, siêu tham số mặc định train_ppo.py, λ=0,1,
  configs/env_default.json, cùng số bước (mặc định 300k; chỉnh theo số đo EXP-01)
Đối chứng: Fixed-PPO; TSP và Random (lấy từ EXP-01, cùng seed đánh giá)
Kiểm soát: cùng kiến trúc, cùng ngân sách bước, cùng seed huấn luyện {0, 1} cho hai
  nhánh; đánh giá trên cùng 100 kịch bản cố định
Ngân sách: bằng nhau; chưa tinh chỉnh Optuna (ghi là giới hạn của pilot)
Bộ đánh giá: id, ood_cluster, ood_density, ood_area, ood_energy
Chỉ số: Ā (khe), deg = (Ā_ood − Ā_id)/Ā_id theo từng seed; phụ: năng lượng, tỷ lệ hết pin,
  tỷ lệ hover/chậm/nhanh, chạm biên
Đơn vị lặp: seed huấn luyện (n = 2/nhánh — chỉ mô tả, không kiểm định)
Thứ tự chạy: s0-DR, s0-Fixed, s1-DR, s1-Fixed (xen kẽ để tránh trôi máy)
Phân tích: scripts/analyze.py → bảng mô tả; LDN viết gate report G1
Thất bại: run_record failed được giữ; nếu phân kỳ (NaN) ghi rõ và chạy lại 1 lần với seed mới
Chi phí: 4 lần huấn luyện × 300k bước; thời gian = 4 × 300k / steps_per_s (EXP-01)

Kết quả kỳ vọng nếu đúng: deg(DR) < deg(Fixed) rõ trên ood_cluster; Fixed-PPO tốt trên
  bố trí của chính nó nhưng suy giảm mạnh ở bố trí khác
Kết quả làm yếu: Fixed-PPO suy giảm ít bằng DR (bản đồ căn tâm tự tổng quát hoá) →
  đóng góp chuyển sang ablation quan sát (A2/A3) và tốc độ (A5)
Tiêu chí tiếp tục/dừng: bảng tiêu chí Gate G1 trong docs/05_ke_hoach.md
Trường raw cần: events.csv (mọi trường), run_record.json (checkpoint_digest, steps_per_s)
```

## Lệnh

```bash
for s in 0 1; do
  python scripts/train_ppo.py --experiment-id EXP-02 --train dr    --seed $s --timesteps 300000 --masked
  python scripts/train_ppo.py --experiment-id EXP-02 --train fixed --seed $s --timesteps 300000 --masked
done
# với mỗi model.zip (đường dẫn in ra ở cuối mỗi lần huấn luyện); nhãn phải đúng nhánh:
python scripts/evaluate.py --experiment-id EXP-02 --model runs/EXP-02/<run-id-dr-s0>/model.zip    --label dr_ppo    --train-seed 0
python scripts/evaluate.py --experiment-id EXP-02 --model runs/EXP-02/<run-id-fixed-s0>/model.zip --label fixed_ppo --train-seed 0
# ... tương tự cho seed 1
python scripts/analyze.py results/raw/EXP-01/*/events.csv results/raw/EXP-02/*/events.csv \
  --proposed dr_ppo --fixed fixed_ppo --out results/processed/EXP-02_summary.md
```
