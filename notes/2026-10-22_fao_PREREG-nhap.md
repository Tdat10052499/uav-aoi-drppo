# Bản nháp PREREG (chuẩn bị cho W4-FAO-01) — 22/10/2026

> FAO soạn trước, khi chưa có kết quả pilot và tinh chỉnh. **Chưa khoá, chưa có hiệu lực.** Mọi giá trị dưới đây chép từ `docs/01`, `docs/03`, `configs/env_default.json`, `data/eval_manifest.json` và mã nguồn tại commit 63fca04. Không có giá trị nào là số đo mới.
>
> Ô `CHỜ` là phần FAO không được tự quyết: mỗi ô ghi người quyết và task tương ứng. Tại W4 (09–13/11), FAO chép phần đã chốt sang `docs/PREREG.md` theo mẫu `docs/03` §9. Second reader: LDN. Tại G1, DAT tạo tag `prereg-lock`.

## 1. Khoá

| Mục | Giá trị |
| --- | --- |
| Ngày khoá | CHỜ: G1, 15/11/2026 |
| Commit | CHỜ: commit mang tag `prereg-lock` (DAT, W4-ALL-01) |
| Phương án | CHỜ: A hoặc B, quyết tại G1 và ghi `PLAN: A/B` vào `docs/DECISIONS.md` |
| PR phải merge trước khi khoá | #18, #20 (train_ppo, tham số DQN), #23 (cờ `single_speed` cho A5) và PR `tune_ppo` của DAT. Sau mốc khoá không sửa `src/` (W5-DAT-01). |

## 2. Cấu hình môi trường (EnvConfig)

- File: `configs/env_default.json`, SHA256 `1b271b22598850b75ce5634130135a66450329e0f0c5fb12979eb4a5becc65fb` tại 63fca04. Nếu PR #23 merge thì file này không đổi; A5 dùng `configs/a5_single_speed.json`.
- Giá trị:

| Tham số | Giá trị | Nguồn |
| --- | --- | --- |
| T, δt | 300 khe, 3,0 s | thiết kế (`docs/02` §7) |
| H | 100 m | [Z19] mục V |
| B, γ₀ | 1 MHz, 60 dB | [Z19] mục V |
| S (packet_bits) | 15 Mbit | thiết kế |
| P_c | 50 W | [Z19] mục V |
| rotor_preset | `zeng2019_arxiv_v1` | [Z19] Bảng I |
| G | 16 (quan sát 5 × 31 × 31) | thiết kế |
| λ | 0,1 (EXP-05 quét {0; 0,05; 0,1; 0,2; 0,5}) | thiết kế |
| μ | 0,1 | thiết kế |
| count_norm | 3,0 | thiết kế |
| single_speed | false (chỉ A5 = true) | PR #23 |

- `use_action_mask_clip` có trong file cấu hình nhưng mã không dùng. CHỜ DAT: xoá trước khi khoá, hoặc ghi chú là trường không có tác dụng.

## 3. Phân phối huấn luyện và bộ đánh giá

| Tên | Thông số (`data/eval_manifest.json`, `src/uavaoi/scenarios.py`) |
| --- | --- |
| TRAIN_DR | đều; N ~ U{10..30}; L = 1000 m; E_max ~ U[0,8; 1,2] MJ; xuất phát ngẫu nhiên |
| TRAIN_FIXED | đều; N = 20; L = 1000 m; E_max = 1,0 MJ; xuất phát cố định; fixed_seed = 0 |

| Bộ | Dịch chuyển | SHA256 kịch bản (12 ký tự đầu) |
| --- | --- | --- |
| id | không | a458ec9e4f66 |
| ood_cluster | 2–4 cụm Gauss, σ = 80 m | 8105f8949f49 |
| ood_density | N ∈ {40, 50} | 6a94b01d5819 |
| ood_area | L = 1500 m | 18002d1d04ae |
| ood_energy | E_max ~ U[0,5; 0,7] MJ | a59dd528bd32 |

Digest đầy đủ nằm trong `data/eval_manifest.json`, sinh ngày 17/10/2026. `run_smoke_test.py` kiểm lại mỗi lần chạy.

## 4. Seed

| Mục | Giá trị |
| --- | --- |
| Seed huấn luyện | 0–9 cho EXP-03, EXP-04; 0–4 cho EXP-05, EXP-06, EXP-07 (Phương án B, `docs/03` §3, §7) |
| Seed reset môi trường khi huấn luyện | `seed × 1000 + rank`, rank < n_envs (`train_ppo.py`) |
| Seed đánh giá | 100 episode, 100000–100099, dùng chung mọi phương pháp, nên so sánh được ghép cặp theo kịch bản |
| Seed đánh giá trong lúc tinh chỉnh | CHỜ DAT (W4-DAT-01): phải tách khỏi 100000–100099. Đề xuất mặc định: bộ `id`, seed 200000–200099. |

## 5. Learner, thực nghiệm và ngân sách

| Thực nghiệm | Learner / biến thể | Seed | Bước/lần | Ghi chú |
| --- | --- | --- | --- | --- |
| EXP-03 | DR-PPO (MaskablePPO), Fixed-PPO (MaskablePPO) | 0–9 | CHỜ | H1, H2 |
| EXP-04 | DR-DQN | 0–9 | CHỜ, bằng EXP-03 | RQ3; không mask, kẹp biên + μ |
| EXP-05 | DR-PPO, λ ∈ {0; 0,05; 0,1; 0,2; 0,5} | 0–4 | CHỜ | RQ2. CHỜ DAT: λ = 0,1 dùng lại seed 0–4 của EXP-03 hay chạy riêng (149,2 M so với 159,2 M bước, `notes/2026-10-21_fao_chi-phi-nhap.md`) |
| EXP-06 | A2 (lưới tuyệt đối), A3 (vector padding) | 0–4 | CHỜ | H3, chỉ mô tả; mã do DAT viết ở W6 |
| EXP-07 | A4 (bỏ mask), A5 (một tốc độ) | 0–4 | CHỜ | chỉ mô tả, `notes/EXP-07_ablation_card.md` |

- **Bước mỗi lần huấn luyện:** CHỜ. Điểm xuất phát là 2 M (`docs/03` §3). Chốt theo steps/s của W1-DAT-05 và tiêu chí G1 số 6 (xong EXP-03 đến EXP-07 trước 13/12). Nếu phải giảm thì giảm bước trước, giảm seed sau, tối thiểu 5 seed (`docs/03` §8).
- **n_envs:** 8 cho PPO (mặc định `train_ppo.py`); 1 cho DQN (script buộc như vậy).
- **Ngân sách tinh chỉnh:** CHỜ DAT (W4-DAT-01). `docs/03` §3 gợi ý 20 lượt × 200k bước cho mỗi nhánh DR, Fixed; chỉ đánh giá trên `id`.
- **DQN:** CHỜ DAT, câu hỏi A1, A2 trong `notes/2026-10-21_fao_can-DAT.md`: buffer_size (200k cần ≈ 7,7 GB RAM) và có tinh chỉnh DQN hay không.
- **Ablation:** mặc định không tinh chỉnh riêng; dùng siêu tham số của DR-PPO. Ghi là giới hạn.

## 6. Siêu tham số cuối

CHỜ DAT (W4-DAT-01). Chép bảng từ kết quả Optuna trên `id` vào đây, mỗi learner một cột. Giá trị khởi đầu hiện có trong `train_ppo.py`, chỉ để đối chiếu:

| Tham số | MaskablePPO / PPO (khởi đầu) | DQN (khởi đầu) |
| --- | --- | --- |
| learning_rate | 3e-4 | 1e-4 |
| n_steps / batch_size / n_epochs | 1024 / 256 / 10 | — / 128 / — |
| gamma, gae_lambda | 0,99, 0,95 | 0,99, — |
| clip_range, ent_coef | 0,2, 0,01 | — |
| buffer_size, learning_starts | — | 200 000, 20 000 (CHỜ A1) |
| train_freq, target_update_interval | — | 4, 10 000 |
| exploration_fraction, exploration_final_eps | — | 0,2, 0,02 |
| Mạng | SmallCNN, features_dim 256 | như PPO |

## 7. Giả thuyết và kiểm định (chép từ `docs/01` §5, `docs/03` §6; không đổi)

| Mã | Phát biểu | Kiểm định | n |
| --- | --- | --- | --- |
| H1 | deg(DR-PPO) < deg(Fixed-PPO) trên từng bộ OOD | Hoán vị một phía, 20 000 hoán vị; Holm trên 4 bộ; α = 0,05. "Ủng hộ H1" nếu ≥ 3/4 bộ có ý nghĩa sau hiệu chỉnh | 10 seed/nhóm |
| H2 | Ā(DR-PPO) < Ā(TSP) trên `ood_cluster` | Hoán vị một phía; Cliff's δ | 10 seed so với 100 episode |
| H3 | Quan sát căn tâm cần cho H1 | Chỉ mô tả (EXP-06) | 5 seed |
| RQ3 | DR-DQN so với DR-PPO | Chưa đặt hướng (`notes/EXP-04_dqn_card.md`). CHỜ: viết hướng trước EXP-04 hoặc ghi rõ là chỉ mô tả | 10 seed |

- deg_i(s) = (Ā_i(s) − Ā_i(id)) / Ā_i(id), tính theo từng seed. Ā tính trên toàn T, kể cả khi dừng sớm.
- Luôn báo: trung bình kèm 95% CI bootstrap (10 000 mẫu), IQM, Cliff's δ. Welch t-test chỉ là kiểm tra phụ.
- Mã: `scripts/analyze.py` tại commit khoá. `src/uavaoi/stats.py` mặc định `n_perm = 20 000`, `n_boot = 10 000`, khớp `docs/03`.
- Chỉ số phụ peak AoI: báo cáo mô tả, không vào giả thuyết. CHỜ nhóm xác nhận (câu hỏi trong `notes/reading/sun2025aoi_FAO.md`).

## 8. Ngưỡng ý nghĩa thực tiễn cho H1

CHỜ LDN và nhóm (`notes/NOTE_FOR_LDN.md`), phải chốt trước EXP-03. `docs/03` §6 nêu ví dụ "giảm ≥ 10% độ suy giảm OOD". FAO không đề xuất số, vì số này phải do nhóm và GVHD chọn khi chưa thấy kết quả EXP-03.

## 9. Tiêu chí loại một lần chạy

Đề xuất của FAO, LDN và DAT duyệt:
1. Lần chạy có `status = failed` trong `run_record.json` (lỗi, hết RAM, phân kỳ NaN) không vào phân tích. Mọi lần như vậy được liệt kê kèm lý do (tiêu chí G2 số 4).
2. Phân kỳ NaN: chạy lại **một** lần với seed mới, như quy tắc EXP-02 và EXP-07, và báo cáo seed thay thế.
3. Không loại lần chạy nào vì kết quả kém. Một model đã `completed` luôn vào phân tích.
4. Lần chạy có commit khác `prereg-lock` (hoặc con không sửa `src/`) không dùng cho bài.

## 10. Phân bổ máy (W4-FAO-02)

CHỜ steps/s của W1-DAT-05. Nguyên tắc từ `docs/05`: DAT chạy EXP-03 seed 0–4 trên máy cố định; seed 5–9 chạy trên Kaggle hoặc máy FAO. Máy chạy được ghi trong `run_record` và `data/checkpoint_manifest.md`. Số thời gian trong bài chỉ lấy từ máy cố định.

## 11. Thay đổi sau ngày khoá

Ghi vào `docs/DECISIONS.md`: ngày, quyết định, lý do, ảnh hưởng, người duyệt.
