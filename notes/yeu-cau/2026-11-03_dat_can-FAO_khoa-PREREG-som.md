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

## B3. Thẻ EXP-03
- Thẻ: `notes/EXP-03_main_card.md` (đã đưa lên main 03/11).
- **Cần FAO:** duyệt thẻ như đã làm với EXP-02.

FAO: (03/11) Đã đọc, góp ý ghi ở cuối `notes/EXP-03_main_card.md`. Duyệt khi DAT thêm 3 trường Form D còn thiếu (kỳ vọng, làm yếu, tiếp tục/dừng); 6 góp ý khác không chặn.

## B4. Điều kiện để bắt đầu EXP-03
1. "G1 sớm" từ pilot đạt: Ā(DR, id) ≤ 63,1 ở cả 2 seed (DAT gửi số).
2. PR khoá PREREG đã merge và tag `prereg-lock` đã có.
3. Thẻ EXP-03 đã duyệt.

Nếu điều kiện 1 không đạt: không chạy EXP-03, và cả nhóm họp lại về FJCAI (đây là điều kiện dừng).
