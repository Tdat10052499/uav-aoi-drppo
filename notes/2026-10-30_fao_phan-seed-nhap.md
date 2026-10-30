# Bản nháp phân seed giữa các máy (chuẩn bị cho W4-FAO-02) — 30/10/2026

> FAO soạn sớm, trước pilot và trước khi chọn Phương án A/B tại G1. **Chưa có hiệu lực.** Tại W4 (12–14/11), FAO cập nhật theo phương án đã chọn, số bước đã chốt và steps/s mới nhất, rồi chép sang `environment/machine_notes.md`. Second reader: DAT.

## 1. Giả định (đều là giả định lập kế hoạch, không phải số đo cho bài)

| Mục | Giá trị | Nguồn |
| --- | --- | --- |
| Phương án | B: 10 seed cho EXP-03, EXP-04; 5 seed cho EXP-05, EXP-06, EXP-07 | `docs/03` §3, §7; chưa chốt (G1) |
| Bước mỗi lần | 2 M | `docs/03` §3, chưa chốt |
| PPO trên laptop DAT | 358,4 bước/s (`--n-envs 8`, CPU) | `results/raw/EXP-01/dr_ppo_mask_lam0.1_s0_20261026-132835` |
| DQN trên laptop DAT | 102 bước/s, tức chậm 3,5 lần so với PPO | **giả định**: tỉ lệ đo trên laptop FAO, cấu hình khác (`notes/2026-10-21_fao_chi-phi-nhap.md` §3) |
| PPO trên laptop FAO | 68,2 bước/s (`--n-envs 2`, 10k bước) | `results/raw/EXP-01/dr_ppo_mask_lam0.1_s0_20261020-090719`; chưa đo với `--n-envs 8` |
| Laptop LDN | chưa đo | — |
| DQN buffer 200k chỉ chạy trên laptop DAT | quyết định | `docs/DECISIONS.md` 30/10 |

Các máy chạy song song với nhau; trên mỗi máy, các lần huấn luyện chạy tuần tự (quy tắc đo, `environment/machine_notes.md`).

## 2. Bảng phân máy theo tuần trong lịch (`schedule/tasks.json`)

| Thực nghiệm | Seed | Máy | Cửa sổ trong lịch | Giờ máy ước lượng |
| --- | --- | --- | --- | --- |
| EXP-03 DR-PPO, Fixed-PPO | 0–4 | Laptop DAT | W5-DAT-01, 16–22/11 | 15,5 |
| EXP-03 DR-PPO, Fixed-PPO | 5–9 | Laptop FAO | W5-FAO-01, 16–22/11 | 81,5 (≈ 3,4 ngày) |
| EXP-04 DR-DQN | 0–9 | **Laptop DAT** (xem §3) | sau EXP-03 seed 0–4, 18–29/11 | 15,5–54,3 |
| EXP-05 λ sweep | 0–4 | Laptop LDN | W7-LDN-01, 30/11–06/12 | chưa biết (31,0–38,8 nếu nhanh như laptop DAT; 163–204 nếu chậm như laptop FAO) |
| EXP-06 A2, A3 | 0–4 | Laptop DAT | W7-DAT-01, 30/11–06/12 | 15,5 |
| EXP-07 A4, A5 | 0–4 | Laptop FAO | W7-FAO-01, 30/11–06/12 | 81,5 (≈ 3,4 ngày) |

Từng seed của EXP-03 và EXP-04 (điều kiện "xong" của W4-FAO-02):
- EXP-03, laptop DAT: seed 0–4, mỗi seed 2 lần chạy (DR, Fixed) × khoảng 1,6 giờ, từ 16/11, xong khoảng 17/11.
- EXP-03, laptop FAO: seed 5–9, mỗi seed 2 lần × khoảng 8,1 giờ, từ 16/11. Thứ tự seed 5, 6, 7, 8, 9; xong khoảng 19/11.
- EXP-04, laptop DAT: seed 0–9, mỗi lần khoảng 1,6–5,4 giờ, từ khoảng 18/11. Xong khoảng 20/11 (nếu DQN nhanh như PPO) hoặc 21/11 (nếu chậm 3,5 lần).

**Kết luận:** kịp trước 13/12 (tiêu chí G1 số 6) với cả hai mức tốc độ DQN. Laptop DAT gánh EXP-03 seed 0–4, EXP-04 và EXP-06, khoảng 47–85 giờ (15,5 + 15,5…54,3 + 15,5). Con số này nằm trong khoảng 648 giờ từ 16/11 đến 13/12, nếu laptop không phải dùng cho việc khác.

**Rủi ro:** EXP-05 (40–50 M bước) trên laptop LDN chưa có số đo. Nếu laptop LDN chậm như laptop FAO thì cần 163–204 giờ, vượt tuần W7 (168 giờ), dù vẫn kịp trước 13/12 (khoảng 312 giờ từ 30/11). Vì vậy cần đo laptop LDN (§4 mục 3) trước G1.

## 3. Xung đột với lịch hiện tại (cần DAT quyết tại G1)

- `schedule/tasks.json` giao W5-FAO-02 ("bắt đầu DR-DQN 10 seed") và W6-FAO-01 ("DR-DQN seed 5–9") cho FAO.
- `docs/DECISIONS.md` ngày 30/10 quyết rằng mọi run DQN với buffer 200k chạy trên laptop DAT, vì laptop FAO chỉ có 16 GB.
- Vì vậy bảng §2 đặt toàn bộ EXP-04 lên laptop DAT. Có hai cách xử lý:
  - (a) FAO giữ phần card, theo dõi và kiểm tra (manifest, `check_degenerate.py`), còn DAT chạy. Lịch W5-FAO-02 và W6-FAO-01 đổi tên cho đúng.
  - (b) Đổi máy cho DQN, ví dụ laptop LDN 16 GB. Cách này vướng cùng giới hạn RAM.
- FAO đề xuất (a). Chỉ DAT sửa `schedule/tasks.json`.

## 4. Cần đo trước W4

1. PPO 100k bước `--n-envs 8` trên laptop FAO. Số 68,2 đo với `--n-envs 2` trên 10k bước. Laptop FAO có 4 nhân/8 luồng, nên tốc độ với 8 env có thể khác.
2. DQN 100k bước trên laptop DAT (đã đề xuất ở A1 của `notes/yeu-cau/2026-10-26_dat_can-FAO_steps-per-s.md`).
3. PPO 100k bước `--n-envs 8` trên laptop LDN, vì LDN chạy EXP-05 (W7-LDN-01).
