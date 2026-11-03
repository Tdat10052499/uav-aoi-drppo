# Đăng ký trước thực nghiệm chính (khoá trước EXP-03)

> **Trạng thái: chờ khoá.** FAO chép từ `notes/2026-10-22_fao_PREREG-nhap.md` (cập nhật 03/11) và từ các dòng `DAT:` trong `notes/yeu-cau/2026-11-03_fao_can-DAT_prereg-cho.md` và `notes/yeu-cau/2026-11-03_dat_can-FAO_khoa-PREREG-som.md` (B1). DAT duyệt PR khoá, LDN là second reader. Sau khi merge, DAT gắn tag `prereg-lock` vào commit merge. Từ đó mọi thay đổi ghi vào `docs/DECISIONS.md` kèm lý do (§11).
>
> Phạm vi: **EXP-03** (bài FJCAI 2027). EXP-04 đến EXP-07 (RQ2, RQ3, H3, ablation) **không** thuộc lần khoá này. Mỗi thực nghiệm đó cần một phụ lục PREREG khoá trước khi chạy.

## Mẫu `docs/03` §9

```text
Ngày khoá: 04/11/2026 (ngày merge PR khoá)  Commit: commit merge của PR khoá, gắn tag prereg-lock
Cấu hình môi trường (EnvConfig): configs/env_default.json (SHA256 ở §2)
Siêu tham số cuối: mặc định của scripts/train_ppo.py, KHÔNG tinh chỉnh Optuna (§6)
Số seed: 10 (0–9) mỗi nhánh  Số bước: 2 000 000  Bộ seed đánh giá: 100000–100099
Ngưỡng ý nghĩa thực tiễn cho H1: CHỜ LDN (§8)
Tiêu chí loại một lần chạy: §9
Bất kỳ thay đổi nào sau ngày khoá: ghi vào DECISIONS.md kèm lý do
```

## 1. Khoá

| Mục | Giá trị |
| --- | --- |
| Ngày khoá | Ngày merge PR khoá (dự kiến 04/11/2026) |
| Commit | Commit merge của PR khoá, gắn tag `prereg-lock` (DAT) |
| PR đã merge trước khoá | #18, #20, #23, #29, #30, #31, #32, #35 |
| PR còn mở | #33 (chỉ sửa `tests/`) và #37 (thêm `evaluate.py --seed-base`, mặc định không đổi). Nên merge cả hai **trước** khi khoá; nếu không thì để sau EXP-03 (§9 tiêu chí 4) |
| Sau khoá | Không sửa `src/`. Không sửa `scripts/train_ppo.py`, `scripts/evaluate.py`, `scripts/analyze.py`, `src/uavaoi/stats.py` cho đến khi EXP-03 phân tích xong |

## 2. Cấu hình môi trường

- File: `configs/env_default.json`, SHA256 `1b271b22598850b75ce5634130135a66450329e0f0c5fb12979eb4a5becc65fb` (kiểm lại 03/11).

| Tham số | Giá trị | Nguồn |
| --- | --- | --- |
| T, δt | 300 khe, 3,0 s | thiết kế (`docs/02` §7) |
| H | 100 m | [Z19] mục V |
| B, γ₀ | 1 MHz, 60 dB | [Z19] mục V |
| S (packet_bits) | 15 Mbit | thiết kế |
| P_c | 50 W | [Z19] mục V |
| rotor_preset | `zeng2019_arxiv_v1` | [Z19] Bảng I |
| G | 16 (quan sát 5 × 31 × 31) | thiết kế |
| λ | 0,1 | thiết kế |
| μ | 0,1 | thiết kế |
| count_norm | 3,0 | thiết kế |
| single_speed | false (mặc định `EnvConfig`) | PR #23 |
| use_action_mask_clip | true, **không có tác dụng** (giữ để SHA256 không đổi) | DECISIONS 30/10, PR #35 |

## 3. Phân phối huấn luyện và bộ đánh giá

| Tên | Thông số (`src/uavaoi/scenarios.py`) |
| --- | --- |
| TRAIN_DR | đều; N ~ U{10..30}; L = 1000 m; E_max ~ U[0,8; 1,2] MJ; xuất phát ngẫu nhiên |
| TRAIN_FIXED | đều; N = 20; L = 1000 m; E_max = 1,0 MJ; xuất phát cố định; fixed_seed = 0 |

| Bộ | Dịch chuyển so với huấn luyện | SHA256 kịch bản (`data/eval_manifest.json`) |
| --- | --- | --- |
| id | không | `a458ec9e4f66a8408c331b80711168134e4887786d912d19c97ce76ca3f36f0c` |
| ood_cluster | 2–4 cụm Gauss, σ = 80 m | `8105f8949f49e785242ecc0bd98c20dc85e8b9707afbe501b3eda5a481d2c87a` |
| ood_density | N ∈ {40, 50} | `6a94b01d5819d6abddcf2085ff018efdab50240890b771d1e846963be075ac23` |
| ood_area | L = 1500 m | `18002d1d04ae1274e8918d6b5e75a3133f00d432524ea8f56cbae53b45f56a3f` |
| ood_energy | E_max ~ U[0,5; 0,7] MJ | `a59dd528bd3245a93c56407f8332649a700ceca6beba4e610b931e7b7c68605c` |

`scripts/run_smoke_test.py` kiểm lại các digest này mỗi lần chạy. Với Fixed-PPO, mọi bộ kể cả `id` đều ngoài phân phối huấn luyện của nó (`docs/03` §4).

## 4. Seed

| Mục | Giá trị |
| --- | --- |
| Seed huấn luyện | 0–9 cho mỗi nhánh (DR-PPO, Fixed-PPO) |
| Seed reset môi trường khi huấn luyện | `seed × 1000 + rank`, rank < n_envs (`train_ppo.py`) |
| Seed đánh giá | 100 episode, 100000–100099 (`scenarios.eval_seeds`), chung cho mọi phương pháp, nên so sánh ghép cặp theo kịch bản |
| Chính sách khi đánh giá | tất định (`deterministic=True`), có action mask với MaskablePPO (`SB3Policy`) |

Seed 0 và 1 trùng với pilot EXP-02 (300k bước). Pilot chỉ dùng cho quyết định "G1 sớm" (§10), không gộp vào phân tích EXP-03.

## 5. Learner và ngân sách

| Nhánh | Learner | Phân phối huấn luyện | Seed | Bước/lần |
| --- | --- | --- | --- | --- |
| DR-PPO | MaskablePPO (`--masked`) | TRAIN_DR | 0–9 | 2 000 000 |
| Fixed-PPO | MaskablePPO (`--masked`) | TRAIN_FIXED | 0–9 | 2 000 000 |
| Random, Greedy-AoI, TSP | heuristic (`src/uavaoi/baselines.py`, `HEURISTICS`) | — | — | — |

- `n_envs` = 8 (mặc định `train_ppo.py`). Tổng 20 × 2 M = 40 M bước.
- Lệnh (`notes/EXP-03_main_card.md`): `python scripts/train_ppo.py --experiment-id EXP-03 --train {dr|fixed} --masked --seed <s> --timesteps 2000000`.
- Heuristic được đánh giá lại tại commit khoá (`evaluate.py --method random greedy_aoi tsp --experiment-id EXP-03`), và phải khớp EXP-01 từng dòng (`scripts/compare_events.py`). Lý do: tiêu chí loại số 4 (§9).
- Máy: laptop DAT, CPU (DECISIONS 01/11). Hai tiến trình chạy song song (một DR, một Fixed), seed tăng dần. `steps_per_s` của các lần chạy song song **không** dùng làm số đo thời gian cho bài. Nếu bài cần số thời gian, đo riêng một lần chạy đơn trên cùng máy.

## 6. Siêu tham số (cố định, không tinh chỉnh)

Mặc định của `scripts/train_ppo.py` cho cả hai nhánh. Không tinh chỉnh Optuna cho bài FJCAI. Ghi là giới hạn: cả hai nhánh dùng cùng bộ, nên so sánh H1 vẫn cân bằng, nhưng không nhánh nào được chứng minh là tối ưu.

| Tham số | Giá trị |
| --- | --- |
| learning_rate | 3e-4 (hằng) |
| n_steps / batch_size / n_epochs | 1024 / 256 / 10 |
| gamma / gae_lambda | 0,99 / 0,95 |
| clip_range / ent_coef | 0,2 / 0,01 |
| Mạng | SmallCNN: Conv 32 (3×3, s1), Conv 64 (3×3, s2), Conv 64 (3×3, s2), Linear → 256; `normalize_images=False` |

## 7. Giả thuyết và kiểm định (`docs/01` §5, `docs/03` §6)

| Mã | Phát biểu | Kiểm định | n |
| --- | --- | --- | --- |
| H1 | deg(DR-PPO) < deg(Fixed-PPO) trên từng bộ OOD | Hoán vị một phía, 20 000 hoán vị; Holm trên 4 bộ; α = 0,05. "Ủng hộ H1" nếu ≥ 3/4 bộ có ý nghĩa sau hiệu chỉnh **và** đạt ngưỡng §8 | 10 seed/nhánh |
| H2 | Ā(DR-PPO) < Ā(TSP) trên `ood_cluster` | Hoán vị một phía; Cliff's δ | 10 trung bình theo seed so với 100 episode TSP |

- deg_i(s) = (Ā_i(s) − Ā_i(id)) / Ā_i(id), tính theo từng seed. Ā tính trên toàn T, kể cả khi dừng sớm (`docs/02` §6).
- Luôn báo: trung bình kèm 95% CI bootstrap (10 000 mẫu), IQM, Cliff's δ. Welch t-test chỉ là kiểm tra phụ.
- Mã: `scripts/analyze.py` và `src/uavaoi/stats.py` tại commit khoá (`n_perm = 20 000`, `n_boot = 10 000`, seed 0).
- Chỉ số phụ, **chỉ mô tả**, không vào giả thuyết: peak AoI, năng lượng đã dùng, tỷ lệ hết pin, tỷ lệ hover/chậm/nhanh, chạm biên, độ phủ (DAT 03/11).
- Không thuộc lần khoá này: H3, RQ2 (EXP-05), RQ3 (EXP-04). RQ3 khi chạy sẽ **chỉ mô tả**, không p-value (DAT 03/11).

## 8. Ngưỡng ý nghĩa thực tiễn cho H1

**CHỜ LDN** (`notes/yeu-cau/2026-11-03_dat_can-FAO_khoa-PREREG-som.md` B2). Phải điền trước khi merge PR khoá, và chọn khi chưa thấy kết quả EXP-03. Số pilot EXP-02 không được dùng để chọn ngưỡng.

Ngưỡng: ____

## 9. Tiêu chí loại một lần chạy

1. Lần chạy có `status = failed` trong `run_record.json` (lỗi, hết RAM, phân kỳ NaN) không vào phân tích.
2. Phân kỳ NaN: chạy lại **tối đa một** lần với seed mới, `seed + 100` (ví dụ seed 3 → 103; quy tắc seed thay thế do FAO đề xuất, DAT duyệt trong PR), và báo cáo seed thay thế. Nếu lần chạy lại vẫn NaN thì ghi failed, không chạy lần ba.
3. Không loại lần chạy nào vì kết quả kém. Một model đã `completed` luôn vào phân tích.
4. Lần chạy có commit khác `prereg-lock`, hoặc khác commit con của nó mà không sửa `src/` và các script ở §1, không dùng cho bài.
5. Mọi lần chạy bị loại hoặc được chạy lại đều được liệt kê trong bài, kèm run ID và lý do (DAT 03/11).

## 10. Điều kiện để bắt đầu EXP-03

1. "G1 sớm" từ pilot EXP-02 đạt: Ā(DR-PPO, `id`) ≤ 63,1 khe ở cả 2 seed (tiêu chí G1 số 2, `docs/05` §5).
2. PR khoá này đã merge và tag `prereg-lock` đã có.
3. Thẻ `notes/EXP-03_main_card.md` đã được FAO duyệt.

Nếu điều kiện 1 không đạt thì không chạy EXP-03, và nhóm họp lại về FJCAI. Điều kiện dừng: đến 10/11 chưa đủ 5 seed mỗi nhánh thì bỏ FJCAI.

## 11. Thay đổi sau ngày khoá

Ghi vào `docs/DECISIONS.md`: ngày, quyết định, lý do, ảnh hưởng, người duyệt.
