# EXP-02b — Chẩn đoán: DR-PPO seed 0 với 2M bước (pilot không đạt "G1 sớm")

**Owner:** DAT (huấn luyện) · **Phân tích:** Claude/DAT, LDN đọc lại · **Second reader:** FAO
**Viết:** 03/11/2026, trước khi chạy (Claude soạn, DAT chọn "Giữ FJCAI đến 05/11")
**Chạy:** tối 03/11 · **Quyết định:** 05/11 (điều kiện dừng FJCAI)

## Bối cảnh (dữ kiện, không phải giả thuyết)
- EXP-02 (300k bước), đánh giá trên laptop DAT tại commit 9152d06 (PR #39), 100 episode mỗi bộ:
  Ā(DR, id) = 126,1 (s0), 123,4 (s1); Ā(Fixed, id) = 113,6 (s0), 106,5 (s1); Random 126,2; Greedy 29,0; TSP 28,6.
  Số khớp từng chữ số với lần đánh giá độc lập trên Linux/torch 2.15.
- Hành vi DR s1 trên id: phủ 35% cảm biến, 0% bước bay nhanh, 113 lần thu (Greedy: 110 lần thu, 57% bay nhanh).
- Hết pin trước khe 300 là bình thường: Greedy và TSP hết pin 30/30 episode.

## D. Experiment card

```text
Experiment ID: EXP-02b
Thăm dò hay khẳng định: THĂM DÒ (chẩn đoán). Không đưa vào bài. Không thay EXP-03.

Câu hỏi: Ā(DR, id) ≈ Random ở 300k bước là do thiếu bước huấn luyện (H-a) hay do
  kẹt cục bộ / thiết kế khám phá-phần thưởng (H-b)?
Dự đoán nếu H-a đúng: ep_rew_mean còn tăng ở 300k trong log EXP-02, và ở 2M bước
  Ā(DR, id) giảm rõ (≤ 63,1 là đạt ngưỡng G1 #2).
Dự đoán nếu H-b đúng: ep_rew_mean đi ngang sớm; ở 2M Ā(DR, id) vẫn > 90.

Biến thay đổi: số bước 300k → 2M (một biến duy nhất)
Điều kiện cố định: như EXP-02 (MaskablePPO, SmallCNN, siêu tham số mặc định, λ=0,1,
  configs/env_default.json, TRAIN_DR, seed 0)
Đối chứng: EXP-02 DR s0 (300k), cùng seed
Bộ đánh giá: id (bắt buộc) + 4 bộ OOD (mô tả); seed 100000–100099
Chỉ số: Ā, độ phủ, tỷ lệ hover/chậm/nhanh; đường học ep_rew_mean từ log tb
Đơn vị lặp: 1 seed — chỉ mô tả, không kiểm định, không kết luận về H1
Thất bại: run_record failed được giữ
Chi phí: 2M bước ≈ 90 phút trên laptop DAT (ước tính từ 380 bước/s, chưa đo ở 2M)

Kết quả và hành động:
- Ā(DR, id) ≤ 63,1 → H-a được ủng hộ; xin khoá PREREG và chạy EXP-03 (2M) ngay.
- 63,1 < Ā ≤ 90 → học có tiến nhưng chậm; 05/11 cả nhóm cân nhắc (FJCAI rủi ro cao).
- Ā > 90 → H-b được ủng hộ; bỏ FJCAI theo điều kiện dừng, chẩn đoán thiết kế theo lịch gốc.
Lưu ý: kết quả 1 seed chỉ là tương quan giữa số bước và Ā, không chứng minh nguyên nhân.
```

## Lệnh (PowerShell, ở nhánh DAT/fix-model-load-windows hoặc main sau khi PR #39 merge)

```powershell
python scripts/train_ppo.py --experiment-id EXP-02b --train dr --masked --seed 0 --timesteps 2000000
# sau khi xong (thay <run> bằng thư mục mới trong runs\EXP-02b):
python scripts/evaluate.py --experiment-id EXP-02b --run-id eval_dr_s0_2M --model runs\EXP-02b\<run>\model.zip --label dr_ppo --train-seed 0 --episodes 100
```

## Kết quả (03/11/2026, đánh giá trên laptop DAT, commit 9152d06 — nhánh PR #39)
Huấn luyện: `runs/EXP-02b/dr_ppo_mask_lam0.1_s0_20261103-153705`. Đánh giá: `results/raw/EXP-02b/eval_dr_s0_2M` (100 episode mỗi bộ).

| Bộ | DR s0 300k (EXP-02) | DR s0 2M (EXP-02b) | deg 2M |
|---|---|---|---|
| id | 126,08 | **49,80** | — |
| ood_cluster | 124,03 | 40,98 | −0,18 |
| ood_density | 129,50 | 93,24 | +0,87 |
| ood_area | 138,91 | 127,04 | +1,55 |
| ood_energy | 147,69 | 146,36 | +1,94 |

- Theo tiêu chí ghi trước: Ā(DR, id) = 49,80 ≤ 63,1 → **H-a được ủng hộ**; hành động: khoá PREREG, chạy EXP-03 (2M).
- Giới hạn: 1 seed, mô tả; tương quan số bước–Ā, chưa phải nhân quả; không kết luận H1 (chưa có Fixed 2M). DR vẫn kém TSP/Greedy (~29) khoảng 1,7 lần.
