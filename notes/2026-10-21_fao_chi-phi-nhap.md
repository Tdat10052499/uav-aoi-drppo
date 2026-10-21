# Bản nháp ước lượng chi phí tính toán (chuẩn bị cho W1-FAO-05) — 21/10/2026

> FAO soạn trước, khi chưa có số đo. **Chưa có số đo thời gian nào trong file này**: steps/s phải lấy từ máy cố định của DAT (W1-DAT-05, quy tắc 4). Khi có số, FAO điền cột cuối và chuyển bảng sang `Project Agreement.md` §5.

## 1. Tổng số bước theo thực nghiệm (Phương án B, `docs/03` §3, §7, §8)

Giả định đang dùng: 2 triệu bước mỗi lần huấn luyện chính (`docs/03` §3, "điểm xuất phát, chốt sau đo đạc tuần 3"); pilot 300k bước (`notes/EXP-02_pilot_card.md`); Optuna 20 lượt × 200k bước cho mỗi nhánh (`docs/03` §3, "gợi ý").

| Thực nghiệm | Cấu hình | Số lần huấn luyện | Bước/lần | Tổng bước |
| --- | --- | --- | --- | --- |
| EXP-02 pilot | DR, Fixed × seed {0, 1} | 4 | 300k | 1,2 M |
| Optuna (W4) | DR, Fixed × 20 lượt | 40 | 200k | 8 M |
| EXP-03 | DR-PPO, Fixed-PPO × 10 seed | 20 | 2 M | 40 M |
| EXP-04 | DR-DQN × 10 seed | 10 | 2 M | 20 M |
| EXP-05 (RQ2) | 5 λ × 5 seed | 25 | 2 M | 50 M |
| EXP-06 | A2, A3 × 5 seed | 10 | 2 M | 20 M |
| EXP-07 | A4, A5 × 5 seed | 10 | 2 M | 20 M |
| **Tổng** | | **119** | | **159,2 M** |

Nếu EXP-05 dùng lại 5 seed DR-PPO λ = 0,1 của EXP-03 (seed 0–4), tổng giảm còn 149,2 M. Việc dùng lại phải được ghi trong PREREG.

Chưa tính: tinh chỉnh cho DQN (câu hỏi A2 trong `notes/2026-10-21_fao_can-DAT.md`), chạy lại khi lỗi, đánh giá (`evaluate.py`, nhẹ hơn nhiều).

## 2. Giờ máy theo tốc độ (chỉ là phép tính, không phải số đo)

Giờ máy = tổng bước / steps_per_s / 3600, với 159,2 M bước, nếu chạy tuần tự trên **một** máy:

| steps/s giả định | Giờ máy | Ngày máy (24 h) |
| --- | --- | --- |
| 100 | 442 | 18,4 |
| 200 | 221 | 9,2 |
| 400 | 111 | 4,6 |
| 800 | 55 | 2,3 |
| **số đo của DAT (W1-DAT-05)** | ___ | ___ |

Mốc so sánh:
- EXP-03 đến EXP-07 phải xong trước 13/12 (`docs/05`, tiêu chí G1 số 6).
- Từ 16/11 đến 13/12 là khoảng 27 ngày, tức khoảng 648 giờ cho mỗi máy nếu chạy liên tục.
- Có thể chia seed cho 3 laptop và Kaggle (W4-FAO-02). Nhưng số thời gian báo cáo trong bài vẫn chỉ lấy từ máy cố định.

## 3. Điều cần DAT đo (đề xuất cho W1-DAT-05)

- **steps/s riêng cho PPO và cho DQN.** Trên laptop FAO, DQN chậm hơn PPO khoảng 3,5 lần mỗi bước. Hai lần chạy 10k bước: 68,2 so với 19,5 bước/s (run EXP-01/dr_ppo_mask_lam0.1_s0_20261020-090719 và EXP-04/dr_dqn_lam0.1_s0_20261020-094810).
  - Đây chỉ là **tỉ lệ** để lập kế hoạch. Số tuyệt đối của máy FAO **không** dùng cho bài.
  - Hai lần chạy cũng không cùng cấu hình: PPO dùng `--n-envs 2`, DQN thì learning_starts gần hết 10k bước.
  - Nếu tỉ lệ này đúng trên máy DAT, EXP-04 sẽ chiếm phần lớn ngân sách.
- **CPU hay GPU:** đo trên thiết bị nào thì chạy thật trên thiết bị đó (`docs/03` §8.1 có ghi "CPU và GPU nếu có").
- **100k bước với `--n-envs 8`**, đúng lệnh cuối trong `notes/EXP-01_reproduction_card.md`.
