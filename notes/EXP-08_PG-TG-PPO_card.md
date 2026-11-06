# EXP-08: PG-TG-PPO (quan sát neo vật lý + PPO tầng cao trên nền tour)

> **Đã duyệt 06/11/2026:** DAT (thiết kế), LDN (thống kê), FAO (mã, PR #45). Claude soạn. Chữ ký ở cuối card.
> **Owner:**
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

## EXP-08a-b: kiểm heuristic trước pilot (thăm dò, chỉ heuristic; thêm 06/11/2026)

> Thêm sau khi card đã ký, theo B4 (1) trong `notes/yeu-cau/2026-11-06_ldn_can-DAT-FAO_power-va-H5.md` (DAT chọn 06/11). **LDN và FAO cần xác nhận mục này trước khi chạy.** Owner chạy: LDN. Second reader: FAO.

```text
Experiment ID: EXP-08a-b
Thăm dò hay khẳng định: THĂM DÒ. Chỉ heuristic, không có policy học; chỉ mô tả, không p-value.
Câu hỏi: TSP-adaptive (chuyển sang V_me khi ρ_E ≤ 1) có yếu hơn TSP thường khi pin thấp không?
  Heuristic nào tốt nhất trên từng bộ?
Bối cảnh: EXP-08a (PR #50): V_mr 31,3 J/m < V_me 43,5 J/m theo preset zeng2019_arxiv_v1, nên
  giảm tốc về V_me làm mỗi joule đi được ít quãng đường hơn.
Phương pháp: random, tsp, tsp_eco, tsp_adaptive; config configs/env_grounded.json; 100 episode.
  (a) Bộ cũ id + 4 OOD, seed 100000–100099 (đã dùng ở EXP-01/03; không phải seed khẳng định).
  (b) ood_energy_low (SUITES_B), cờ --probe-b, seed 100000–100099; KHÔNG dùng 300000–300099.
Lệnh:
  python scripts/evaluate.py --experiment-id EXP-08a-b --method random tsp tsp_eco tsp_adaptive \
         --config configs/env_grounded.json
  python scripts/evaluate.py --experiment-id EXP-08a-b --method random tsp tsp_eco tsp_adaptive \
         --suites ood_energy_low --probe-b --config configs/env_grounded.json
Chỉ số: Ā, coverage, early_termination, slow_frac, fast_frac, năng lượng mỗi mét, theo bộ × heuristic.
Dự đoán (từ mô hình năng lượng, chưa đo): trên ood_energy và ood_energy_low,
  Ā(TSP-adaptive) ≥ Ā(TSP).
Hành động (ghi trước):
- Dù kết quả thế nào: H5 và mốc S dùng heuristic tốt nhất trên từng bộ = argmin Ā của
  {TSP, TSP-eco, TSP-adaptive}, chọn trên chính seed khẳng định và chỉ từ kết quả heuristic,
  trước khi xem số của M1 (B4 (2); chốt trong PREREG phụ lục B).
- Nếu Ā(TSP-adaptive) > Ā(TSP) trên một bộ pin thấp: ghi vào phụ lục B rằng TSP-adaptive không
  phải baseline mạnh nhất trên bộ đó; G3 viết lại theo thứ tự, bỏ điểm, treo (B4 (4)).
- Nếu Ā(TSP-adaptive) ≤ Ā(TSP): giữ mô tả TSP-adaptive là baseline mạnh; G3 vẫn bỏ câu
  "TSP không tiết kiệm năng lượng".
- Không sửa mã baseline (B4 (3) không chọn).
Lưu ý: kết quả (b) là dữ liệu đã thấy trên bộ OOD mới, chỉ để đặt baseline; ghi vào run_record
  (--probe-b) và phụ lục B §1.
```

## EXP-08p: pilot (thăm dò, 2 seed)

```text
Experiment ID: EXP-08p
Thăm dò hay khẳng định: THĂM DÒ. 2 seed, chỉ mô tả, không p-value (quy tắc 5).
Câu hỏi: wrapper tour-guided có học được không, tốc độ máy bao nhiêu, cần bao nhiêu bước?
Nhánh: M1 (DR, quan sát neo, tour-guided) và M4 (DR, quan sát neo, phẳng); seed 0, 1.
  (seed 0–9 đã dùng ở EXP-03 cho nhánh khác; pilot dùng lại 0–1 được vì là thăm dò.)
Số bước: M4 2M; M1 700 000 quyết định (mục 9; DAT chốt khi ký 06/11). Số bước của EXP-08 chính chốt sau pilot.
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
11. **Rà soát mã 06/11 (commit 7d60d5e):**
    - **Seed reset lúc huấn luyện.** SB3 tự gọi `venv.seed(seed)` khi tạo model, nên env rank r reset bằng seed + r, không phải seed·1000 + r như `make_env` và run record ghi. Claude đã kiểm bằng cách dựng lại kịch bản đầu tiên của từng env.
      - **Hệ quả cho EXP-01 đến EXP-03:** với n_envs = 8, hai seed huấn luyện liền nhau dùng chung 7/8 chuỗi kịch bản DR. Ví dụ seed 1 rank 0 lặp lại chuỗi của seed 0 rank 1. Các seed vẫn khác nhau ở khởi tạo mạng và ở hành động lấy mẫu. Nhánh Fixed không bị ảnh hưởng vì kịch bản cố định. Mức ảnh hưởng tới CI của nhánh DR chưa định lượng.
      - **Việc cần làm:** ghi vào DECISIONS và phần giới hạn của bài. Không chạy lại EXP-03.
      - **Từ EXP-08:** `--reset-seed-scheme spaced` (mặc định mới) reset đúng seed·1000 + r, và run record ghi danh sách seed thật.
    - **Mask năng lượng.** Số khe bay được ước lượng theo tiến độ xấu nhất của 8 hướng. Mask cộng thêm 1 khe dự phòng: đo trên 1 600 macro-action, số khe thật vượt ước lượng tối đa 1 khe.
    - **Tiến tour.** Tour chỉ tiến khi chính điểm đó được thu. Env có thể phục vụ một cảm biến khác cũ hơn trong cùng tầm. *(Đã thay bằng mục 12: tour tiến theo cảm biến được thu thật.)*
    - **Chặn seed khẳng định.** `plot_trajectory.py` và `plot_f6.py` cũng từ chối seed 300000–300099.
12. **Sau review của FAO và LDN trên PR #45** (0c207f2, cd62a0b):
    - **Tiến tour.** Tour tiến theo cảm biến được thu thật: thu c₂ thì bỏ qua c₁; thu một cảm biến ngoài tour thì tour đứng yên.
    - **Chặn bộ mới.** Bốn bộ mới bị chặn trên **mọi** seed khi chưa có tag. `--probe-b` chỉ cho heuristic và được ghi vào run record. Phép thử độ khả thi của FAO (heuristic, seed 900000–900029, mã ngoài `evaluate.py`) và mọi lần dùng `--probe-b` phải khai trong PREREG phụ lục B §1.
    - **Seed huấn luyện thay thế phải tránh dải đánh giá.** `train_ppo.py` từ chối seed khiến env reset rơi vào 100000–100099, 200000–200019 hoặc 300000–300099. Với scheme `spaced`, đó là seed 100, 200 và 300 (với n_envs = 8, seed 100 chạm 100000–100007). Vì vậy quy tắc "seed + 100" của PREREG §9 không dùng được cho pilot seed 0, 1: dùng **seed + 1000** cho pilot. EXP-08 (seed 10–19 → 110–119) vẫn an toàn.
    - **Yếu tố gây nhiễu đã biết giữa M1–M3 và M4.** γ = 0,99 tính theo quyết định. Mỗi quyết định trung bình khoảng 2,7 khe (hl_greedy trên id), nên tầm nhìn hiệu dụng của nhánh tour dài hơn M4. Ngân sách tính toán cũng khác nhau (mục 9). H7 (M1 so M3) không bị ảnh hưởng vì cùng tầng tour và cùng γ. M1 so M4 là thăm dò và phải ghi kèm hai yếu tố này.

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

# 3. M1: DR + quan sát neo + tour-guided, seed 0 và 1 (700 000 quyết định)
python scripts/train_ppo.py --experiment-id EXP-08p --policy options --masked --train dr --seed 0 --timesteps 700000 --config configs/env_grounded.json
python scripts/train_ppo.py --experiment-id EXP-08p --policy options --masked --train dr --seed 1 --timesteps 700000 --config configs/env_grounded.json

# 4. đánh giá từng model trên bộ cũ (thay <run-id> và seed)
python scripts/evaluate.py --experiment-id EXP-08p --model runs/EXP-08p/<run-id>/model.zip --label m1 --train-seed 0 --config configs/env_grounded.json
```

- Ghi run ID vào card này.
- Bước/s nằm trong `results/raw/EXP-08p/<run-id>/run_record.json` (`metrics.steps_per_s`).
- Push `results/raw/EXP-08p/` sau khi xong.
- **Không** chạy bộ id2, ood_energy_low, ood_area_2000, ood_combo trên seed 300000–300099 ở pilot. `evaluate.py` sẽ từ chối.

## Second reader LDN (thống kê), 06/11/2026

> LDN ký **phần thống kê** của card: chỉ số, tiêu chí pilot, cách kiểm và mục "Cài đặt trong mã" ở góc ảnh hưởng tới H5–H7. Phần mã do FAO review ở PR #45; phần thiết kế do DAT chốt (W3-DAT-05). Ký tại `main` 188565d.

**Quyết định 1: mốc "tệ nhất" của S là Random** (câu P4 của FAO; W4-LDN-04).
- S = (Ā_Random − Ā)/(Ā_Random − Ā_TSP-adaptive), tính theo từng bộ. Ā_Random đo trên **cùng** các seed đánh giá của bộ đó. Random tất định khi đã cố định seed, nên không thêm phương sai.
- **Lý do, độc lập với số EXP-03:**
  - khớp định nghĩa S đã ghi sẵn trong card (EXP-08, "Chỉ số chính");
  - khớp lý do của δ₇ trong PREREG phụ lục B §5 ("thu hẹp thêm 10% khoảng Random→TSP");
  - giữ nghĩa cho ngưỡng pilot S > 0,2. Với mốc trần 151,5, một policy ngang Random đã có S ≈ 0,19 trên `ood_energy`; con số này tính bằng Random 133,9 và TSP 60,5 của EXP-01, TSP thay tạm cho TSP-adaptive.
- **Hệ quả cần ghi khi báo cáo:**
  - S có thể âm, nghĩa là kém hơn Random.
  - Nếu Ā_Random − Ā_TSP-adaptive < 10 khe trên một bộ thì S không ổn định. Khi đó vẫn báo S nhưng kèm cờ, và đọc Ā là chính.
  - S theo mốc 151,5 chỉ báo như **phân tích độ nhạy**, không dùng để kiểm định.

**Quyết định 2: gộp 2 seed cho tiêu chí pilot (G1 #3) = cả hai seed đều phải đạt.**
- Mỗi seed i ∈ {0, 1} phải thoả **cả hai** điều kiện: Ā(M1_i, `id`) ≤ 1,2 × Ā(TSP-adaptive, `id`) và S(M1_i, `ood_energy`) > 0,2.
- Ánh xạ sang nhánh hành động của card:
  - cả 2 seed đạt → khoá phụ lục B và chạy EXP-08;
  - đúng 1 seed đạt, hoặc cả 2 có Ā rõ ràng thấp hơn Random nhưng chưa đạt → "học được nhưng chưa đạt": một vòng chỉnh siêu tham số, pilot lại 1 lần;
  - cả 2 seed có Ā ≈ Random → phương án dự phòng.
- **Lý do:** tránh khoá PREREG và chạy 40 model (khoảng 40–55 giờ máy) chỉ nhờ một seed may mắn. Cái giá nếu quá chặt chỉ là thêm một vòng pilot.
- Pilot là thăm dò: chỉ mô tả, không p-value (quy tắc 5).
- **Cần sửa theo:** `docs/05` §5 G1 #3 (PR #44) đang ghi "cách gộp 2 seed: LDN chốt trước khi chạy pilot ✱". DAT thay ✱ bằng quy tắc trên.

**Nhận xét về "Cài đặt trong mã" (góc thống kê):**
- **Mục 6 (đặc trưng ứng viên của M3): đồng ý.** Dùng khoảng cách/(L√2) và năng lượng cần/E_max giữ M3 ở cùng kiểu chuẩn hoá với quan sát legacy, nên so M1 với M3 (H7) đúng là so hai cách quan sát.
  - Cần ghi rõ giới hạn trong PREREG phụ lục B §4 (H7): M3 **vẫn** có một phần thông tin ngân sách. Có hai đường:
    - (a) **mask** che ứng viên theo năng lượng tuyệt đối, và mask áp dụng cho mọi nhánh;
    - (b) policy có thể tự suy ra năng lượng cần/năng lượng còn bằng cách chia (năng lượng cần/E_max) cho kênh E/E_max.
  - Vì vậy H7 kiểm "quan sát neo (ô cố định + ρ_E + đặc trưng neo) **khi đã có cùng mask và cùng tầng tour**". H7 không kiểm "có hay không có thông tin ngân sách". Câu kết luận của H7 trong bài phải giữ đúng phạm vi này.
- **Mục 8 (ρ_E ban đầu của `ood_energy_low` nằm ngoài dải huấn luyện): đồng ý ghi là rủi ro cho H5.** Không đổi giả thuyết vì điều này. Nếu H5 không đạt, phần thảo luận phải nêu dải ρ_E ban đầu như một giải thích khả dĩ (giả thuyết, không phải nhân quả).
- **Mục 9 (M1 700 000 quyết định so với M4 2M bước):** hai nhánh không cùng ngân sách tính toán. So M1 với M4 chỉ là thăm dò (đúng như PREREG phụ lục B §4). Khi báo cáo, ghi kèm số episode và thời gian máy của từng nhánh.
- **Mục 1–5, 7, 10: không có ý kiến thống kê.** Mục 10 (chặn bộ khẳng định trong mã) đúng ý PREREG phụ lục B §3.

**Việc thống kê còn mở, không chặn pilot** (W4-LDN-04, hạn 13/11):
- cách kiểm H5 (heuristic tất định so với 10 giá trị seed);
- kiểm không thua cho H6;
- power cho δ₅–δ₇ từ độ lệch chuẩn theo seed của EXP-03 (cần raw EXP-03).

Chữ ký: **LDN (Dương Ngọc Linh Đan), second reader thống kê, 06/11/2026.**

**Xác nhận lại (LDN, 06/11 tối, `main` ab2faaf):** đã đọc mục 11, 12 và phần ký thiết kế của DAT. Đồng ý cả hai mục:
- Mục 12, seed thay thế pilot = seed + 1000: khớp việc chặn dải seed đánh giá trong `train_ppo.py` (cd62a0b). LDN đã đọc diff `0c207f2..cd62a0b`; sửa đúng và có kiểm thử.
- Mục 12, γ theo quyết định: H7 không bị ảnh hưởng; khi so M1 với M4 phải ghi kèm yếu tố gây nhiễu, như ghi ở mục 9 phần LDN.

Card không còn mục thống kê nào chờ LDN. W3-DAT-05 được LDN approve trong `schedule/status/LDN.json`.

## DAT (thiết kế), 06/11/2026

DAT xác nhận:
1. **Tiêu chí hành động ghi trước** của EXP-08a và EXP-08p, gồm Quyết định 2 của LDN: pilot chỉ đạt khi **cả hai seed** cùng đạt. Dấu ✱ ở `docs/05` §5 G1 #3 được thay bằng quy tắc này qua PR #46 (LDN review).
2. **Lựa chọn thiết kế** ở "Cài đặt trong mã", các mục 1–5 và 7.
3. **Hai con số của pilot:**
   - M1 = 700 000 quyết định (mục 9). Dấu ✱ đã bỏ.
   - Seed thay thế của pilot = seed + 1000 (mục 12). Quy tắc này chỉ thay `seed + 100` của PREREG §9 trong pilot.
4. **Hai yếu tố gây nhiễu khi so M1 với M4** (γ tính theo quyết định, ngân sách tính toán khác nhau; mục 9 và 12) được ghi kèm mỗi khi báo cáo phép so sánh này. H7 (M1 so M3) không bị ảnh hưởng.

**Còn ✱:** L = 2000 m của `ood_area_2000` thuộc EXP-08 chính, chốt khi khoá phụ lục B tại G1.

**Điều kiện chạy còn lại:**
- EXP-08a (W4-LDN-03) cần raw EXP-03 trên `main` (W3-DAT-03).
- EXP-08p chạy sau khi EXP-08a không bác bỏ thành phần A.
- EXP-08 chính chạy sau khi có tag `prereg-B-lock`.

**Thay đổi sau chữ ký của LDN** (ký tại 188565d):
- LDN đồng ý mục 11 trong review PR #45 (góp ý 3).
- Mục 12 viết theo review của FAO và LDN; LDN chưa xác nhận lại trên card.
- Lần ký này chỉ đổi chữ và thứ tự (mục 10 đặt trước mục 11), không đổi nội dung đã ký.

Chữ ký: **DAT (Hồ Du Tuấn Đạt), thiết kế, 06/11/2026** (xác nhận qua Claude).
