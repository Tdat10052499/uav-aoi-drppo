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
