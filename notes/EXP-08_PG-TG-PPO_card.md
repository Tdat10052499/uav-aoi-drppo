# EXP-08: PG-TG-PPO (quan sát neo vật lý + PPO tầng cao trên nền tour)

> **Nháp.** Claude soạn 06/11/2026; chưa ai duyệt.
> **Owner (đề xuất):**
> - DAT: huấn luyện, máy cố định.
> - FAO: mã môi trường và wrapper.
> - LDN: thống kê.
>
> **Second reader:** FAO cho mã, LDN cho số.
> **Thiết kế:** `notes/2026-11-06_dat_thiet-ke_PG-TG-PPO.md`.
> **Quy tắc 1:** không chạy phần nào khi card chưa được duyệt. Phần khẳng định cần PREREG phụ lục B khoá trước.

Card chia ba phần, mỗi phần có tiêu chí hành động ghi trước.

## EXP-08a: chẩn đoán từ dữ liệu EXP-03 (thăm dò, không tốn máy)

```text
Experiment ID: EXP-08a
Thăm dò hay khẳng định: THĂM DÒ. Dữ liệu đã thấy; chỉ mô tả.
Câu hỏi: trên ood_energy và ood_area, PPO thua vì hết pin sớm (hành vi "tiêu theo phần trăm pin")
  hay vì đi sai đường?
Dữ liệu: results/raw/EXP-03/*/events.csv và episode_metrics (cần DAT push raw trước),
  heuristics_lock của EXP-03.
Chỉ số: tỉ lệ early_termination, khe dừng trung bình, hover_frac, slow_frac, fast_frac,
  coverage, theo bộ × nhánh (DR, Fixed, TSP, Greedy).
Dự đoán nếu G1 đúng: trên ood_energy, PPO early_termination cao hơn rõ TSP và gần bằng id
  về fast_frac (không giảm tốc khi ngân sách nhỏ).
Hành động:
- Dự đoán đúng → giữ thành phần A như thiết kế.
- Dự đoán sai (PPO không hết pin sớm hơn TSP) → xem lại G1 trước khi viết mã A; báo DAT.
Lưu ý: tương quan, không phải nhân quả.
```

## EXP-08p: pilot (thăm dò, 2 seed)

```text
Experiment ID: EXP-08p
Thăm dò hay khẳng định: THĂM DÒ. 2 seed, chỉ mô tả, không p-value (quy tắc 5).
Câu hỏi: wrapper tour-guided có học được không, tốc độ máy bao nhiêu, cần bao nhiêu bước?
Nhánh: M1 (DR, quan sát neo, tour-guided) và M4 (DR, quan sát neo, phẳng); seed 0, 1.
  (seed 0–9 đã dùng ở EXP-03 cho nhánh khác; pilot dùng lại 0–1 được vì là thăm dò.)
Số bước: M4 2M; M1 theo số quyết định tương đương ✱ (FAO đề xuất sau khi đo).
Bộ đánh giá: CHỈ bộ cũ (id + 4 OOD), seed 100000–100099. KHÔNG chạy bộ OOD mới ở pilot.
Đo thêm: bước/s và thời gian huấn luyện trên máy DAT (quy tắc 4).
Tiêu chí hành động (ghi trước):
- M1 trên id có Ā ≤ 1,2 × Ā(TSP-adaptive) VÀ điểm chuẩn hoá trên ood_energy > 0,2
    → khoá PREREG phụ lục B, chạy EXP-08.
- M1 học được nhưng chưa đạt → một vòng chỉnh siêu tham số (ghi DECISIONS), pilot lại 1 lần.
- M1 không học được (Ā ≈ Random) → dừng B, quay về phương án A thuần (CG-DR-PPO); báo DAT.
Thất bại: run_record failed được giữ.
```

## EXP-08: thực nghiệm chính (khẳng định)

```text
Experiment ID: EXP-08
Thăm dò hay khẳng định: KHẲNG ĐỊNH cho H5–H7 (PREREG phụ lục B); phần còn lại thăm dò.
Nhánh (mỗi nhánh 10 seed huấn luyện, seed 10–19):
  M1 DR + neo + tour-guided (đề xuất)   M2 Fixed + neo + tour-guided
  M3 DR + cũ + tour-guided              M4 DR + neo + phẳng
  Tái dùng EXP-03: DR + cũ + phẳng, Fixed + cũ + phẳng (seed 0–9; chỉ dùng mô tả).
Baseline không học: Random, Greedy-AoI, TSP, TSP-eco, TSP-adaptive, tầng cao greedy.
Bộ đánh giá chính (mới, khoá trước, seed 300000–300099):
  ood_energy_low (E_max 0,35–0,45 MJ), ood_area_2000 (L = 2000 m ✱), ood_combo (cụm + 0,5–0,7 MJ),
  cộng id mới (cùng phân phối TRAIN_DR, seed mới).
Bộ phụ (cũ): id, ood_cluster, ood_density, ood_area, ood_energy, seed 100000–100099.
Chỉ số chính: Ā; điểm chuẩn hoá S = (Ā_Random − Ā)/(Ā_Random − Ā_TSP-adaptive) theo bộ.
Chỉ số phụ: năng lượng dùng, early_termination, coverage, peak AoI; deg tương đối (để so EXP-03).
Đơn vị lặp: seed huấn luyện. Thống kê: 95% CI bootstrap, IQM, Cliff's δ, hoán vị một phía,
  Holm trong mỗi họ giả thuyết.
Chi phí: ≈ 40–55 giờ máy (ước tính; đo lại ở pilot).
Kết quả và hành động: theo PREREG phụ lục B §5.
```

## Cài đặt trong mã (PR `DAT/pilot-pg-tg-ppo`, 06/11/2026) — cần duyệt cùng card

Các điểm dưới đây là lựa chọn lúc viết mã. Thiết kế để ngỏ hoặc đánh ✱ ở những chỗ này. DAT và LDN xác nhận khi ký card. Muốn đổi thì đổi trước khi chạy pilot.

1. **Không gian hành động là Discrete(2K + 1) = 11**, không phải 2K + 2.
   - Hành động "kết thúc sớm có chủ đích" bị bỏ.
   - Lý do: env đã phạt chi phí xấu nhất cho mọi khe mất khi kết thúc sớm, nên hành động này không bao giờ có lợi.
2. **Phần thưởng một quyết định là tổng phần thưởng các khe, không chiết khấu bên trong.** Đây là lựa chọn (b) của thiết kế §3. PPO dùng γ = 0,99 cho mỗi quyết định.
3. **"Chờ" là hover một khe** (hành động 0 của env). Nếu có cảm biến trong tầm thì env vẫn thu.
4. **Mask:**
   - ứng viên × tốc độ được phép khi năng lượng còn ≥ năng lượng bay tới mép tầm r_eff ở tốc độ đó, cộng một khe hover + truyền;
   - ô ứng viên trống (N < K) luôn bị che;
   - "chờ" luôn được phép.
5. **Ứng viên:**
   - c₁, c₂ là hai điểm kế tiếp trên tour.
   - c₃–c₅ là ba cảm biến có AoI / (số khe bay ở V_me + 1) cao nhất.
   - Tour tiến khi thu được c₁, hoặc thu được c₂ (khi đó c₁ bị bỏ qua). Rẽ sang c₃–c₅ không làm tour tiến.
6. **Đặc trưng ứng viên (K × 4):**
   - Nhánh **grounded** (M1, M2, M4) dùng số khe bay ở V_me / T, AoI/Δmax, năng lượng cần / năng lượng còn (cắt ở 2), cờ tour.
   - Nhánh **legacy** (M3) dùng khoảng cách / (L√2) và năng lượng cần / E_max, để M3 không nhận thông tin ngân sách tuyệt đối qua vector ứng viên. Đây là lựa chọn quan trọng cho H7, cần LDN đồng ý.
7. **Kênh thời gian (T − t)/T đã có sẵn trong quan sát cũ** (kênh 4 của `env.py`). Bảng ở thiết kế §2 ghi "không có" là nhầm. Quan sát neo vì vậy chỉ đổi kích thước ô và kênh năng lượng.
8. **Giá trị ρ_E đo được** ở cấu hình mặc định, tính từ mã:
   - năng lượng một khe ở V_me (21,5 m/s) là 2,81 kJ;
   - E_max = 1 MJ cho ρ_E ≈ 1,19 lúc bắt đầu;
   - TRAIN_DR (0,8–1,2 MJ) có ρ_E ban đầu khoảng 0,95–1,43;
   - ood_energy (0,5–0,7 MJ) khoảng 0,59–0,83;
   - ood_energy_low (0,35–0,45 MJ) khoảng 0,42–0,53.

   Như vậy bộ pin thấp nằm **ngoài** dải ρ_E ban đầu lúc huấn luyện. ρ_E giảm dần trong episode nên policy vẫn gặp các giá trị nhỏ, nhưng ở cuối episode, không phải ở đầu. Đây là rủi ro cho H5 (giả thuyết, chưa kiểm). Pilot sẽ cho dấu hiệu đầu tiên.
9. **Số quyết định cho M1** (card để ✱):
   - M4 2M bước tương đương khoảng 6 700 episode.
   - Tầng cao greedy cần khoảng 60–180 quyết định mỗi episode trên các bộ cũ (đo trên 20 episode mỗi bộ, kiểm tra mã, không phải kết quả).
   - Đề xuất M1 = 700 000 quyết định, tức khoảng 5 000–10 000 episode. FAO điều chỉnh sau khi đo bước/s.
10. **Chặn bộ khẳng định trong mã:** `evaluate.py` từ chối seed 300000–300099 nếu thiếu `--confirmatory` hoặc chưa có tag `prereg-B-lock`.

## Lệnh pilot EXP-08p trên laptop DAT (chỉ chạy sau khi card được ký và PR mã đã merge)

Chạy từ thư mục repo trên `main` sau khi merge. Mỗi lệnh một dòng, dùng được trong PowerShell.

```text
# 0. kiểm tra
git pull
python tests/test_core.py
python scripts/run_smoke_test.py

# 1. baseline không học, trên bộ cũ (seed 100000–100099)
python scripts/evaluate.py --experiment-id EXP-08p --method random greedy_aoi tsp tsp_eco tsp_adaptive hl_greedy --config configs/env_grounded.json

# 2. M4: DR + quan sát neo + PPO phẳng, seed 0 và 1 (2M bước)
python scripts/train_ppo.py --experiment-id EXP-08p --masked --train dr --seed 0 --timesteps 2000000 --config configs/env_grounded.json
python scripts/train_ppo.py --experiment-id EXP-08p --masked --train dr --seed 1 --timesteps 2000000 --config configs/env_grounded.json

# 3. M1: DR + quan sát neo + tour-guided, seed 0 và 1 (700 000 quyết định ✱)
python scripts/train_ppo.py --experiment-id EXP-08p --policy options --masked --train dr --seed 0 --timesteps 700000 --config configs/env_grounded.json
python scripts/train_ppo.py --experiment-id EXP-08p --policy options --masked --train dr --seed 1 --timesteps 700000 --config configs/env_grounded.json

# 4. đánh giá từng model trên bộ cũ (thay <run-id> và seed)
python scripts/evaluate.py --experiment-id EXP-08p --model runs/EXP-08p/<run-id>/model.zip --label m1 --train-seed 0 --config configs/env_grounded.json
```

- Ghi run ID vào card này.
- Bước/s nằm trong `results/raw/EXP-08p/<run-id>/run_record.json` (`metrics.steps_per_s`).
- Push `results/raw/EXP-08p/` sau khi xong.
- **Không** chạy bộ id2, ood_energy_low, ood_area_2000, ood_combo trên seed 300000–300099 ở pilot. `evaluate.py` sẽ từ chối.
