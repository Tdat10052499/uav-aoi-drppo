# DAT → FAO (cc LDN): khoá PREREG sớm, ngày 03/11 hoặc 04/11, để chạy EXP-03 — 03/11/2026

> Claude soạn cho DAT. Trả lời bằng dòng `FAO:` hoặc `LDN:` dưới mỗi mục. Quy ước: `notes/yeu-cau/README.md` (PR #28).
> Thay thế hạn "khoá 05/11" ở mục A1 của `2026-11-03_dat_can-FAO_FJCAI-lich-nen.md`.

## Vì sao cần khoá sớm
- Nhắm FJCAI 2027, hạn toàn văn 15/11. EXP-03 (2 nhánh × 10 seed × 2M bước) ước tính khoảng 29 giờ máy, hoặc 17–20 giờ nếu chạy 2 tiến trình song song. Đây là ước tính, chưa đo.
- Điều kiện dừng: đến 10/11 chưa đủ 5 seed mỗi nhánh thì bỏ FJCAI. Muốn kịp thì EXP-03 phải bắt đầu tối 03/11 hoặc sáng 04/11.
- PREREG phải khoá **trước** khi chạy EXP-03. Ngoài ra, mọi lần chạy có commit khác `prereg-lock` sẽ không được dùng (tiêu chí loại số 4, §9 của nháp).

## B1. Các ô của `docs/PREREG.md`: đề xuất giá trị (FAO chép, DAT và LDN duyệt)
| Ô | Đề xuất | Nguồn |
|---|---|---|
| Ngày khoá | 03/11/2026 (hoặc 04/11) | quyết định FJCAI 03/11 |
| Commit | commit của chính PR khoá, sau đó gắn tag `prereg-lock` | §9 nháp |
| EnvConfig | `configs/env_default.json` tại commit đó | docs/02 |
| Siêu tham số | mặc định của `scripts/train_ppo.py` (n_steps 1024, batch 256, 10 epoch, γ 0,99, GAE 0,95, clip 0,2, ent 0,01, lr 3e-4, 8 env, SmallCNN 32/64/64→256); **không** tinh chỉnh Optuna (ghi là giới hạn) | DECISIONS 03/11 |
| Số seed / số bước | 10 seed (0–9) mỗi nhánh / 2.000.000 bước | A1 = DAT |
| Bộ seed đánh giá | 100000–100099 | PREREG |
| Ngưỡng ý nghĩa thực tiễn H1 | **LDN đề xuất** (xem B2) | — |
| Tiêu chí loại | 4 tiêu chí §9, cộng "liệt kê mọi lần chạy bị loại hoặc chạy lại, kèm run ID và lý do"; NaN chạy lại tối đa 1 lần | A5 = DAT |
| Phạm vi bài FJCAI | H1, H2 và heuristic (Random, Greedy, TSP); λ = 0,1. RQ3 (DQN) và EXP-05, EXP-07 không thuộc bài FJCAI | DECISIONS 03/11 |

- **Cần FAO:** chép vào `docs/PREREG.md` và mở PR khoá. DAT duyệt PR, LDN là second reader.
- **Hạn:** 04/11, trước 12:00.

FAO: (03/11) Đã chép, PR #38: https://github.com/Tdat10052499/uav-aoi-drppo/pull/38. Theo B1, nhưng có thêm: (a) heuristic chạy lại tại commit khoá và so với EXP-01; (b) `steps_per_s` khi chạy song song không dùng cho bài; (c) seed thay thế khi NaN là `seed + 100`, đề xuất của FAO, chờ DAT duyệt; (d) đề nghị merge #33 và #37 trước khi khoá. `docs/DECISIONS.md` chưa có dòng 03/11 mà hai yêu cầu nhắc tới; nên thêm trước khi khoá.

## B2. LDN: ngưỡng ý nghĩa thực tiễn cho H1
- **Cần LDN:** một con số, ví dụ "deg(Fixed) − deg(DR) ≥ 0,10 (10 điểm phần trăm) trên bộ OOD, xét theo IQM qua 10 seed". Con số này phải khoá trước khi thấy kết quả EXP-03.
- Số pilot EXP-02 (2 seed, 300k bước) được dùng để kiểm tra pipeline, **không** dùng để chọn ngưỡng.
- **Hạn:** 04/11, trước 12:00.

LDN: (03/11) Chốt **δ = 0,10**, tính theo **hiệu tuyệt đối của trung bình**, áp trên chính các bộ có ý nghĩa. LDN chọn lúc 15:35 ngày 03/11, khi **chưa thấy số nào** của pilot EXP-02 hay EXP-03. DAT đã thấy kết quả pilot (commit f1b3c7c, 15:36 cùng ngày, ghi "pilot không đạt G1 sớm") nhưng không tham gia chọn ngưỡng. GVHD chưa được hỏi về ngưỡng; đề nghị DAT gửi GVHD cùng PR khoá. Đề xuất chép vào §8 của PR #38:

> **Ngưỡng ý nghĩa thực tiễn cho H1.** Với mỗi bộ OOD s, Δ_s = mean_i deg_Fixed,i(s) − mean_i deg_DR,i(s), trung bình qua 10 seed mỗi nhánh (deg theo `docs/03` §5). Bộ s **đạt H1** khi (a) p sau Holm < 0,05 (kiểm định hoán vị một phía trên hiệu trung bình, `stats.permutation_test`), **và** (b) Δ_s ≥ **0,10**, tức DR suy giảm ít hơn Fixed ít nhất 10 điểm phần trăm AoI `id` của chính nó. **"Ủng hộ H1"** khi có ≥ 3/4 bộ đạt. Luôn báo kèm 95% CI bootstrap của Δ_s, IQM của deg từng nhánh và Cliff's δ; CI và IQM là thông tin, không phải điều kiện quyết định. Ngưỡng do LDN chọn ngày 03/11/2026, trước khi LDN thấy bất kỳ số nào của EXP-02 hoặc EXP-03. DAT đã thấy kết quả pilot EXP-02 (không đạt G1 sớm) nhưng không tham gia chọn ngưỡng. Ngưỡng không được đổi sau khi khoá.

- **Vì sao hiệu tuyệt đối, không phải "giảm ≥ 10% độ suy giảm" (`docs/03` §6):** deg có thể ≤ 0, khi đó tỉ lệ không xác định hoặc đổi dấu. Ví dụ heuristic tham chiếu: TSP trên `ood_cluster` có deg ≈ (22,94 − 28,64)/28,64 ≈ −0,20 (`results/processed/heuristics_summary_2026-10-16.md`).
- **Vì sao trung bình, không phải IQM như ví dụ trong B2:** kiểm định hoán vị dùng hiệu trung bình, nên ngưỡng áp lên cùng đại lượng. Với n = 10, IQM chỉ giữ 5 giá trị giữa.
- **Vì sao điểm ước lượng, không phải cận dưới CI ≥ 0,10:** với 10 seed, điều kiện CI đòi hiệu ứng rất lớn. Ý nghĩa thống kê đã được kiểm bằng (a); (b) chỉ chặn hiệu ứng có ý nghĩa thống kê nhưng nhỏ về thực tiễn. CI của Δ_s vẫn báo, theo khuyến nghị Agarwal 2021 (`notes/reading/agarwal2021deep_LDN.md`).
- **Vì sao 0,10:** khớp ví dụ ở `docs/03` §6. Để đối chiếu thang đo (đây là số **heuristic** tham chiếu, không phải learner, không phải EXP-02 hay EXP-03): deg của TSP là +0,24 (`ood_area`), −0,20 (`ood_cluster`), +0,52 (`ood_density`), +1,11 (`ood_energy`). So với độ lớn các dịch chuyển, 0,10 là mức khiêm tốn.
- **Việc cho `analyze.py` (LDN, A3):** thêm cột Δ_s, CI bootstrap của Δ_s và cột "đạt (a) và (b)" vào bảng H1.

## B3. Thẻ EXP-03
- Thẻ: `notes/EXP-03_main_card.md` (đã đưa lên main 03/11).
- **Cần FAO:** duyệt thẻ như đã làm với EXP-02.

FAO: (03/11) Đã đọc, góp ý ghi ở cuối `notes/EXP-03_main_card.md`. Duyệt khi DAT thêm 3 trường Form D còn thiếu (kỳ vọng, làm yếu, tiếp tục/dừng); 6 góp ý khác không chặn.

## B4. Điều kiện để bắt đầu EXP-03
1. "G1 sớm" từ pilot đạt: Ā(DR, id) ≤ 63,1 ở cả 2 seed (DAT gửi số).
2. PR khoá PREREG đã merge và tag `prereg-lock` đã có.
3. Thẻ EXP-03 đã duyệt.

Nếu điều kiện 1 không đạt: không chạy EXP-03, và cả nhóm họp lại về FJCAI (đây là điều kiện dừng).
