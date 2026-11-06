# FAO đọc thiết kế PG-TG-PPO, card EXP-08 và PREREG phụ lục B (góc môi trường) — 06/11/2026

> Đọc tại fceadac: `notes/2026-11-06_dat_thiet-ke_PG-TG-PPO.md`, `notes/EXP-08_PG-TG-PPO_card.md`, `notes/2026-11-06_dat_PREREG-phu-luc-B_nhap.md`. Đối chiếu với `src/uavaoi/env.py`, `baselines.py`, `scenarios.py` trên `main`. FAO chỉ xét phần môi trường, quan sát và bộ đánh giá; phần thống kê do LDN xét. Mục 1 và 2 nên sửa trước khi DAT duyệt card (W3-DAT-05). Các mục còn lại không chặn.

## 1. Kênh thời gian đã có (sửa bảng §2 của thiết kế)
`env.py` dòng 205: `obs[4] = (T − t)/T`. Quan sát hiện tại đã có 5 kênh: AoI, số cảm biến, mặt nạ ngoài vùng, năng lượng, thời gian. Dòng "Kênh thời gian (thêm): hiện tại không có" là sai. Hệ quả tốt: chế độ `grounded` vẫn giữ 5 kênh và SmallCNN không đổi, chỉ đổi hai thứ là kích thước ô (dòng 191) và kênh 3 (dòng 204). Vì vậy M3 (quan sát cũ) và M1 (neo) khác nhau đúng ở hai điểm này, đây là điều H7 cần.

## 2. Đơn vị của ρ_E: bay ở V_me rẻ hơn thu dữ liệu
Với `configs/env_default.json`:
- một khe bay ở V_me (21,49 m/s) tốn **2 806,9 J**;
- một khe ở V_mr (38,27 m/s) tốn 3 598,6 J;
- một khe hover có truyền (thu dữ liệu) tốn **4 264,0 J**, tức gấp 1,52 lần một khe V_me.

Thu dữ liệu bắt buộc phải hover (hành động 0, `env.py` dòng 129–135). Nếu ρ_E đếm số khe bay ở V_me, thì "ρ_E = 1" chưa có nghĩa là đủ năng lượng để vừa bay vừa thu tới cuối chu kỳ. Có hai lựa chọn, DAT chọn và ghi vào thiết kế:
- (a) giữ e_Vme như thiết kế (= `E_min_action`, dòng 62, đã có sẵn). Đây là "số khe tối đa còn sống được"; ý nghĩa rõ, nhưng phải mô tả đúng như vậy trong bài;
- (b) dùng `E_hover_tx` làm đơn vị, nghĩa là "số khe thu còn trả được".

**FAO đề xuất mặc định (a)**, vì nó là giới hạn vật lý thật của thời gian sống và không cần giả định tỉ lệ thu/bay. Câu "vừa đủ bay tới hết chu kỳ" trong thiết kế đã đúng với (a).

Dải giá trị ρ_E lúc t = 0 theo (a), cho thấy OOD có nằm trong vùng đã gặp khi huấn luyện không:

| Bộ | E_max (MJ) | ρ_E(t = 0) |
| --- | --- | --- |
| TRAIN_DR | 0,8–1,2 | 0,95–1,43 |
| ood_energy | 0,5–0,7 | 0,59–0,83 |
| ood_energy_low | 0,35–0,45 | 0,42–0,53 |

Trong huấn luyện, ρ_E giảm dần theo năng lượng nên các giá trị 0,4–0,9 đều được gặp, chỉ là ở giữa episode chứ không phải lúc bắt đầu. Điều này ủng hộ lập luận ở thiết kế §2 (giả thuyết, chưa kiểm). Kênh cũ E/E_max luôn bằng 1,0 lúc t = 0 ở mọi bộ.

## 3. Mệnh đề về E_max: đúng với mã hiện tại
Ba thứ chỉ phụ thuộc năng lượng tuyệt đối, không phụ thuộc E_max:
- mask năng lượng (dòng 105, 109);
- điều kiện kết thúc sớm (dòng 162);
- phần thưởng: e/(P_hover·δt) (dòng 159).

Vì vậy, với quan sát neo, hai kịch bản chỉ khác E_max có cùng quan sát và cùng động lực học tại mọi trạng thái (vị trí, AoI, E tuyệt đối, t). Mệnh đề §2 đúng. FAO sẽ viết một kiểm thử cho điều này ở PR `fao/grounded-obs` (W4-FAO-03).

## 4. Ô 62,5 m: giống hệt quan sát cũ ở L = 1000 m
Với L = 1000 m, cell = L/G = 62,5 m và chỉ số ô 0..15 đều nằm trọn trong cửa sổ 31 × 31. Do đó chế độ `grounded` cho cùng kênh 0–2 và 4 như `legacy`. Kiểm thử sẽ so từng phần tử trên các bộ L = 1000.

Với L > 1000 m (ood_area 1500, ood_area_2000), vùng có 24 hoặc 32 ô, nhiều hơn nửa cửa sổ (±15 ô = ±968,75 m). FAO đề xuất: cảm biến ngoài cửa sổ dồn lên ô biên theo hướng, đúng như thiết kế; kênh 2 bằng 1 cho các ô ngoài vùng nằm trong cửa sổ.

## 5. ood_area_2000: T = 300 đủ (kiểm thử độ khả thi, không phải thực nghiệm)
Đây là phép thử độ khả thi môi trường (✱ ở thiết kế §6 và phụ lục B §3). Chỉ chạy heuristic, trên seed 900000–900029, **không** dùng bộ 300000–300099 sẽ khoá. Số chỉ để kiểm môi trường, không vào raw, không vào bài. Mã: `ScenarioSpec(L=2000)`, `ScenarioSpec(E_range=(0.35e6, 0.45e6))`, `ScenarioSpec(layout="clustered", E_range=(0.5e6, 0.7e6))`.

| Bộ thử | TSP Ā / độ phủ | Greedy Ā / độ phủ | Random Ā / độ phủ |
| --- | --- | --- | --- |
| L = 2000 | 40,4 / 1,00 | 43,7 / 1,00 | 141,1 / 0,18 |
| E 0,35–0,45 | 87,4 / 1,00 | 87,8 / 1,00 | 141,3 / 0,25 |
| cụm + E 0,5–0,7 | 55,2 / 1,00 | 55,5 / 1,00 | 138,9 / 0,26 |
| id (so sánh) | 26,9 / 1,00 | 27,3 / 1,00 | 124,9 / 0,44 |

TSP thăm đủ mọi cảm biến trên L = 2000 m, nên T = 300 đủ và có thể bỏ ✱. Random gần trần 151,5 ở cả ba bộ mới. Với S lấy Random làm mốc tệ nhất, khoảng Random→TSP vẫn rộng: khoảng 100 khe trên L = 2000 m.

## 6. Phụ lục B §7 khác PREREG gốc §9
Phụ lục B viết "Run hỏng thì chạy lại với seed + 100". PREREG gốc §9 chỉ dùng `seed + 100` cho NaN. Còn DECISIONS 05/11 (PR #41) chạy lại **cùng seed** khi máy ngắt mà chưa có model. Đề xuất viết lại §7: "Như PREREG gốc §9: NaN thì `seed + 100`, tối đa một lần; ngắt do máy trước khi có model thì chạy lại cùng seed; mọi lần chạy lại đều liệt kê."

## 7. Nhỏ
- Phụ lục B §3: bộ `id2` dùng `ScenarioSpec(name="id2")` với seed 300000–300099. Digest phải khác `id` dù cùng phân phối. FAO làm cùng manifest ở W4-FAO-04.
- Thẻ EXP-08p, "M1 theo số quyết định tương đương ✱": FAO đề xuất cho M1 dùng cùng **số khe môi trường** với M4 (2M khe). Lý do: ngân sách mô phỏng bằng nhau thì so sánh M1–M4 công bằng về tính toán. Số quyết định PPO sẽ ít hơn. Ghi rõ đơn vị này vào card.
- TSP-eco, TSP-adaptive (W4-FAO-04) chỉ cần thêm một tham số ép tốc độ vào `_move_towards` (`baselines.py` dòng 11). Tầng thấp của wrapper `options.py` (DAT) có thể dùng chung hàm này. FAO sẽ làm hàm này trước để DAT dùng.
