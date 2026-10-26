# Bản nháp ước lượng chi phí tính toán (chuẩn bị cho W1-FAO-05) — 21/10/2026

> FAO soạn trước, khi chưa có số đo. **Cập nhật 26/10:** đã điền số đo của DAT ở §2 và §4 (laptop DAT, CPU; máy cố định chưa được xác nhận chính thức, mục A4 trong `notes/2026-10-21_fao_can-DAT.md`). Bảng đã chuyển sang `Project Agreement.md` §5.

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
| **358,4: số đo của DAT, laptop DAT, CPU (26/10)** | **123,4** | **5,1** |

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

## 4. Ước lượng theo số đo của DAT (cập nhật 26/10/2026)

Số đo: run `results/raw/EXP-01/dr_ppo_mask_lam0.1_s0_20261026-132835`, commit ff6d658, không có uncommitted patch. MaskablePPO, `--train dr --masked --n-envs 8`, 100k bước, CPU (torch 2.14.1+cpu), `wall_time_s = 279.0`, `steps_per_s = 358.4` (đọc từ `run_record.json`). Ghi là **"đo trên laptop DAT, CPU"** cho tới khi DAT xác nhận máy cố định (A4).

Giờ máy = tổng bước / steps/s / 3600, chạy tuần tự, một lần huấn luyện tại một thời điểm, trên một máy. Cột DQN là giả định, **không** phải số đo: DQN chậm hơn PPO 3,5 lần như tỉ lệ trên laptop FAO (§3), tức khoảng 102 bước/s.

| Thực nghiệm | Tổng bước | Giờ máy, mọi learner 358,4 bước/s | Giờ máy, DQN giả định chậm 3,5 lần |
| --- | --- | --- | --- |
| EXP-02 pilot | 1,2 M | 0,9 | 0,9 |
| Optuna (W4) | 8 M | 6,2 | 6,2 |
| EXP-03 | 40 M | 31,0 | 31,0 |
| EXP-04 (DQN) | 20 M | 15,5 | 54,3 |
| EXP-05 | 50 M | 38,8 | 38,8 |
| EXP-06 | 20 M | 15,5 | 15,5 |
| EXP-07 | 20 M | 15,5 | 15,5 |
| **Tổng (159,2 M)** | | **123,4 h ≈ 5,1 ngày** | **162,1 h ≈ 6,8 ngày** |
| Tổng nếu EXP-05 dùng lại seed EXP-03 (149,2 M) | | 115,6 h ≈ 4,8 ngày | 154,4 h ≈ 6,4 ngày |
| Riêng EXP-03 đến EXP-07 (sau G1) | 150 M | 116,3 h | 155,0 h |

**Kết luận:** kịp trước 13/12 (tiêu chí G1 số 6). Trường hợp xấu nhất trong bảng, 155 h cho EXP-03 đến EXP-07, chiếm khoảng 24% của 648 h máy có được từ 16/11 đến 13/12, dù chỉ dùng một máy. Vẫn còn dư nếu tốc độ thật thấp hơn số đo khoảng 4 lần.

Các giả định có thể làm sai ước lượng (chưa kiểm):
1. Tốc độ đo trên 100k bước có thể khác khi chạy 2M bước (nhiệt độ, chế độ nguồn của laptop).
2. Chạy song song nhiều lần huấn luyện trên cùng máy sẽ chia CPU, nên tốc độ mỗi lần giảm.
3. DQN chưa đo trên máy DAT; tỉ lệ 3,5 lần lấy từ máy khác và cấu hình khác (§3).
4. Chưa tính tinh chỉnh DQN, chạy lại khi lỗi và đánh giá.
5. GPU chưa đo. Nếu chạy thật trên GPU thì phải đo lại trên GPU (§3).

Đề xuất cho DAT: đo thêm DQN 100k bước trên laptop DAT, CPU, để thay giả định ở cột cuối bằng số đo. Card `notes/EXP-04_dqn_card.md` hiện chỉ có trên nhánh của PR #20, nên nên đo sau khi PR #20 merge (quy tắc 1), bằng lệnh `python scripts/train_ppo.py --experiment-id EXP-04 --algo dqn --train dr --seed 0 --timesteps 100000`. Việc này không chặn G0 hay W1-FAO-05.
