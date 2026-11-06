# Lịch theo ngày (tự sinh — KHÔNG sửa tay)

> Sinh bởi `python scripts/today.py --render` từ `schedule/tasks.json` (chỉ DAT chạy lại khi lịch đổi).
> Trạng thái thực tế: `python scripts/today.py --team`. Việc của bạn hôm nay: hỏi Claude
> "hôm nay tôi cần làm gì?" trong repo này, hoặc chạy `python scripts/today.py`.

| Gate | Ngày | Nội dung |
| --- | --- | --- |
| **G0** | 2026-11-04 | Chốt định vị đóng góp |
| **G1** | 2026-11-20 | Pilot PG-TG-PPO (EXP-08p) đạt tiêu chí, khoá PREREG phụ lục B |
| **G2** | 2026-12-20 | Đóng băng kết quả |
| **G3** | 2027-01-10 | Bài báo và đồ án sẵn sàng |

## W0 (chuẩn bị)

| Bắt đầu | Ai | Task | Hạn | Second reader | Issue |
| --- | --- | --- | --- | --- | --- |
| T7 17/10/2026 | DAT | `W0-DAT-01` Chuẩn bị khởi động: mời collaborator, điền tên GVHD | CN 18/10/2026 |  | #9 |

## W1

| Bắt đầu | Ai | Task | Hạn | Second reader | Issue |
| --- | --- | --- | --- | --- | --- |
| T2 19/10/2026 | ALL | `W1-ALL-01` Họp khởi động 60' (DAT chủ trì) | T2 19/10/2026 |  |  |
| T2 19/10/2026 | DAT | `W1-DAT-01` Gửi Project Agreement Rev 0.1 cho GVHD | T2 19/10/2026 |  | #9 |
| T2 19/10/2026 | FAO | `W1-FAO-01` Clone repo, tạo venv, cài requirements | T2 19/10/2026 |  | #5 |
| T2 19/10/2026 | LDN | `W1-LDN-01` Chấp nhận lời mời repo, nắm quy ước file | T2 19/10/2026 |  |  |
| T3 20/10/2026 | DAT | `W1-DAT-02` Đọc toàn văn Bayerlein 2021 → Form B | T3 20/10/2026 | LDN | #10 |
| T3 20/10/2026 | DAT | `W1-DAT-03` Soạn và gửi email hỏi lịch FJCAI 2027, ICISN 2027 | T3 20/10/2026 |  | #7 |
| T3 20/10/2026 | FAO | `W1-FAO-02` EXP-01 bước 1–3: tests, smoke test, evaluate heuristic | T3 20/10/2026 | DAT | #5 |
| T3 20/10/2026 | LDN | `W1-LDN-02` Đọc Agarwal 2021 và Yi 2020 → Form B | T3 20/10/2026 | DAT | #12 |
| T4 21/10/2026 | DAT | `W1-DAT-04` Đọc Zeng 2019 và Lamenza 2025 → Form B; bắt đầu ma trận | T4 21/10/2026 | LDN | #10 |
| T4 21/10/2026 | FAO | `W1-FAO-03` EXP-01 bước 4: train_ppo.py 10k bước, sửa lỗi API | T4 21/10/2026 | DAT | #5 |
| T4 21/10/2026 | LDN | `W1-LDN-03` Smoke test trên máy LDN (máy thứ 2 cho EXP-01) | T4 21/10/2026 | FAO | #13 |
| T5 22/10/2026 | DAT | `W1-DAT-05` Second reader EXP-01: chạy lại trên máy cố định, đo 100k bước | T5 22/10/2026 |  | #5 |
| T5 22/10/2026 | FAO | `W1-FAO-04` Hoàn thành Form C của EXP-01, đóng issue #5 | T5 22/10/2026 | DAT | #5 |
| T5 22/10/2026 | LDN | `W1-LDN-04` Tìm kiếm Q1, lọc tiêu đề/tóm tắt | T5 22/10/2026 | DAT | #6 |
| T6 23/10/2026 | DAT | `W1-DAT-06` Khung scripts/tune_ppo.py (chưa chạy) | T6 23/10/2026 | FAO | #11 |
| T6 23/10/2026 | FAO | `W1-FAO-05` Ước lượng chi phí tính toán → Project Agreement §5 | T6 23/10/2026 | DAT | #15 |
| T6 23/10/2026 | LDN | `W1-LDN-05` Tìm kiếm Q2, Q3; danh sách đọc toàn văn | T6 23/10/2026 | DAT | #6 |
| T7 24/10/2026 | DAT | `W1-DAT-07` Tổng hợp góp ý GVHD về ngưỡng gate (hạn duyệt 25/10) | CN 25/10/2026 |  | #9 |
| T7 24/10/2026 | DAT | `W1-DAT-08` Chốt thông tin hội nghị đích, quy định cộng điểm, mốc 18–19/01 | CN 25/10/2026 |  | #7 |

## W2

| Bắt đầu | Ai | Task | Hạn | Second reader | Issue |
| --- | --- | --- | --- | --- | --- |
| T2 26/10/2026 | DAT | `W2-DAT-01` Đọc toàn văn nửa danh sách (phần DAT); câu định vị bản 2 | T3 27/10/2026 | LDN | #6 |
| T2 26/10/2026 | FAO | `W2-FAO-01` Form B: Abd-Elmagid 2019, OH-DRL 2025, Sun 2025, Liu 2024 | T3 27/10/2026 | LDN | #16 |
| T2 26/10/2026 | FAO | `W2-FAO-02` Viết scripts/plot_trajectory.py | T5 29/10/2026 | DAT | #17 |
| T2 26/10/2026 | LDN | `W2-LDN-01` Đọc toàn văn phần còn lại + Sarathchandra 2025; điền ma trận | T3 27/10/2026 | DAT | #12 |
| T4 28/10/2026 | DAT | `W2-DAT-02` Hoàn thiện tune_ppo.py | T5 29/10/2026 | FAO | #11 |
| T4 28/10/2026 | FAO | `W2-FAO-03` Chạy thử DR-DQN 10k bước; hoàn thiện script quỹ đạo | T5 29/10/2026 | DAT | #17 |
| T4 28/10/2026 | LDN | `W2-LDN-02` Mở rộng analyze.py: độ suy giảm OOD theo seed + hình F4 | T5 29/10/2026 | FAO | #14 |
| T6 30/10/2026 | DAT | `W2-DAT-03` Soạn báo cáo G0 (Form G) | T2 02/11/2026 | LDN | #1 |
| T6 30/10/2026 | FAO | `W2-FAO-04` Second reader tune_ppo.py: đọc mã, chạy 2 lượt nhỏ | T7 31/10/2026 |  | #11 |
| T6 30/10/2026 | LDN | `W2-LDN-03` Second reader báo cáo G0 + chốt số PRISMA | T3 03/11/2026 |  | #6 |

## W3

| Bắt đầu | Ai | Task | Hạn | Second reader | Issue |
| --- | --- | --- | --- | --- | --- |
| T2 02/11/2026 | DAT | `W3-DAT-01` EXP-02: huấn luyện seed 0 (DR và Fixed) trên máy cố định | T4 04/11/2026 | FAO |  |
| T3 03/11/2026 | LDN | `W3-LDN-01` Đánh giá từng model EXP-02 ngay khi xong; bảng mô tả tạm | CN 08/11/2026 | FAO |  |
| T4 04/11/2026 | ALL | `W2-ALL-01` GATE G0 — họp 45', gửi GVHD | T4 04/11/2026 |  | #1 |
| T5 05/11/2026 | DAT | `W3-DAT-02` EXP-02: huấn luyện seed 1 (DR và Fixed) | T7 07/11/2026 | FAO |  |
| T5 05/11/2026 | FAO | `W3-FAO-01` Manifest checkpoint EXP-02 + second reader quỹ đạo (≥ 3/model) | CN 08/11/2026 |  |  |
| T6 06/11/2026 | DAT | `W3-DAT-03` Đẩy dữ liệu thô EXP-03 lên main; merge PR #41, #42 | T7 07/11/2026 |  |  |
| T7 07/11/2026 | DAT | `W3-DAT-04` Nhắn GVHD: kết quả EXP-03, hướng PG-TG-PPO, ngưỡng δ, tên đề tài, hạn đăng ký | CN 08/11/2026 |  |  |
| T7 07/11/2026 | DAT | `W3-DAT-05` Đọc và chốt thiết kế PG-TG-PPO + card EXP-08 (bản nháp Claude soạn 06/11) | T2 09/11/2026 | LDN |  |

## W4

| Bắt đầu | Ai | Task | Hạn | Second reader | Issue |
| --- | --- | --- | --- | --- | --- |
| T2 09/11/2026 | DAT | `W4-DAT-02` Kiểm lại Bayerlein 2021 (pin b₀ có trong quan sát?) + Form B Theile ~2020 'Varying Power Constraints' | T4 11/11/2026 | LDN |  |
| T2 09/11/2026 | DAT | `W4-DAT-03` PR dat/tour-guided: wrapper semi-MDP tour-guided + tầng cao greedy + train_ppo.py --policy options | T7 14/11/2026 | FAO |  |
| T2 09/11/2026 | FAO | `W4-FAO-01` Điền docs/PREREG.md (cấu hình, seed, ngân sách) | T6 13/11/2026 | LDN |  |
| T2 09/11/2026 | FAO | `W4-FAO-03` PR fao/grounded-obs: obs_mode 'grounded' (ô 62,5 m, kênh ρ_E, kênh thời gian) + kiểm thử | T5 12/11/2026 | DAT |  |
| T2 09/11/2026 | LDN | `W4-LDN-04` Báo cáo chính thức H1/H2 của EXP-03 (PR #43) + power analysis cho δ₅–δ₇ | T6 13/11/2026 | DAT |  |
| T3 10/11/2026 | LDN | `W4-LDN-03` EXP-08a: chẩn đoán từ dữ liệu EXP-03 (hết pin sớm hay đi sai đường?) | T5 12/11/2026 | FAO |  |
| T5 12/11/2026 | FAO | `W4-FAO-04` PR fao/tsp-manh: TSP-eco, TSP-adaptive + bộ đánh giá mới (seed 300000–300099, chưa ai chạy) | T7 14/11/2026 | LDN |  |

## W5

| Bắt đầu | Ai | Task | Hạn | Second reader | Issue |
| --- | --- | --- | --- | --- | --- |
| T2 16/11/2026 | DAT | `W5-DAT-03` EXP-08p: pilot M1 và M4, seed 0–1, đo bước/s trên máy cố định | T4 18/11/2026 | LDN |  |
| T2 16/11/2026 | FAO | `W5-FAO-03` Đưa PREREG phụ lục B vào docs/PREREG.md (PR): cấu hình, SHA256, bộ đánh giá, seed theo máy, siêu tham số, số bước | T5 19/11/2026 | LDN |  |
| T2 16/11/2026 | FAO | `W5-FAO-04` Second reader EXP-03: chạy lại đánh giá 2 model bất kỳ, so khớp events.csv | T5 19/11/2026 |  |  |
| T4 18/11/2026 | DAT | `W5-DAT-02` Viết mục System Model (paper/main.tex) | CN 22/11/2026 | FAO |  |
| T4 18/11/2026 | LDN | `W5-LDN-03` Báo cáo G1 mới (Form G): pilot EXP-08p, EXP-08a, power, sẵn sàng khoá PREREG phụ lục B | T5 19/11/2026 | FAO |  |
| T6 20/11/2026 | ALL | `W5-ALL-01` GATE G1 — duyệt pilot EXP-08p, khoá PREREG phụ lục B (tag prereg-B-lock) | T6 20/11/2026 |  | #2 |
| T7 21/11/2026 | DAT | `W6-DAT-03` EXP-08: huấn luyện M1 (DR + neo + tour) và M2 (Fixed + neo + tour), seed 10–19, laptop DAT | T4 02/12/2026 | FAO |  |
| T7 21/11/2026 | FAO | `W6-FAO-03` EXP-08: huấn luyện M3 (DR + quan sát cũ + tour) và M4 (DR + neo + phẳng), seed 10–19 | T4 02/12/2026 | DAT |  |
| T7 21/11/2026 | LDN | `W5-LDN-02` Viết mục Experimental Setup | T6 27/11/2026 | DAT |  |

## W6

| Bắt đầu | Ai | Task | Hạn | Second reader | Issue |
| --- | --- | --- | --- | --- | --- |
| T2 23/11/2026 | LDN | `W6-LDN-03` analyze.py cho EXP-08: H5–H7 đúng PREREG phụ lục B (PR) | CN 29/11/2026 | FAO |  |
| T7 28/11/2026 | DAT | `S-GVHD-1` Họp GVHD định kỳ (2 tuần/lần) | CN 29/11/2026 |  |  |

## W7

| Bắt đầu | Ai | Task | Hạn | Second reader | Issue |
| --- | --- | --- | --- | --- | --- |
| T2 30/11/2026 | LDN | `W7-LDN-03` Mô tả tạm EXP-08 (≥ 5 seed mỗi nhánh) và phân tích thăm dò (M1 so M2, M4, tầng cao greedy) | CN 06/12/2026 | DAT |  |
| T3 01/12/2026 | DAT | `W7-DAT-02` Đánh giá mọi model EXP-08 trên bộ chính (seed 300000–300099) và bộ phụ; push raw | CN 06/12/2026 | LDN |  |
| T3 01/12/2026 | FAO | `W7-FAO-02` Second reader EXP-08: provenance từng run + chạy lại đánh giá 2 model | CN 06/12/2026 |  |  |

## W8

| Bắt đầu | Ai | Task | Hạn | Second reader | Issue |
| --- | --- | --- | --- | --- | --- |
| T2 07/12/2026 | DAT | `W8-DAT-03` Second reader phân tích EXP-08: chạy lại analyze.py từ raw, so bảng | T4 09/12/2026 |  |  |
| T2 07/12/2026 | FAO | `W8-FAO-03` Hình F6: quỹ đạo TSP-adaptive và M1 trên ood_energy_low, ood_combo; bảng hành vi (chờ, tốc độ, rẽ) | T6 11/12/2026 | LDN |  |
| T2 07/12/2026 | LDN | `W8-LDN-01` Hình F3 (đường học), F4, F5 từ raw (EXP-03 và EXP-08) | T6 11/12/2026 | DAT |  |
| T4 09/12/2026 | DAT | `W8-DAT-02` Viết mục Method: quan sát neo vật lý, semi-MDP tour-guided, DR, baseline TSP-eco/adaptive | CN 13/12/2026 | FAO |  |
| T4 09/12/2026 | FAO | `W8-FAO-02` Hoàn tất data/checkpoint_manifest.md | CN 13/12/2026 | DAT |  |
| T6 11/12/2026 | LDN | `W8-LDN-03` Cập nhật claim–evidence → measured | CN 13/12/2026 | FAO |  |
| T7 12/12/2026 | DAT | `S-GVHD-2` Họp GVHD định kỳ (2 tuần/lần) | CN 13/12/2026 |  |  |

## W9

| Bắt đầu | Ai | Task | Hạn | Second reader | Issue |
| --- | --- | --- | --- | --- | --- |
| T2 14/12/2026 | DAT | `W9-DAT-01` Khoá commit kết quả (tag results-freeze) | T2 14/12/2026 |  | #3 |
| T2 14/12/2026 | FAO | `W9-FAO-01` Tái lập độc lập: chạy lại toàn bộ evaluate.py từ commit khoá trên máy khác | T6 18/12/2026 |  |  |
| T2 14/12/2026 | LDN | `W9-LDN-01` Phân tích cuối từ commit khoá: H5–H7 (PREREG phụ lục B) và H1/H2 của EXP-03 (Holm) | T6 18/12/2026 | FAO |  |
| T4 16/12/2026 | DAT | `W9-DAT-02` Báo cáo G2 (Form G) | T7 19/12/2026 | FAO | #3 |
| CN 20/12/2026 | ALL | `W9-ALL-01` GATE G2 — đóng băng kết quả | CN 20/12/2026 |  | #3 |

## W10

| Bắt đầu | Ai | Task | Hạn | Second reader | Issue |
| --- | --- | --- | --- | --- | --- |
| T2 21/12/2026 | DAT | `W10-DAT-01` Viết Introduction, Method (hoàn thiện), Discussion | CN 27/12/2026 | LDN |  |
| T2 21/12/2026 | FAO | `W10-FAO-01` Viết Related Work (từ ma trận), Limitations | CN 27/12/2026 | LDN |  |
| T2 21/12/2026 | LDN | `W10-LDN-01` Viết Results, hoàn thiện Experimental Setup | CN 27/12/2026 | DAT |  |

## W11

| Bắt đầu | Ai | Task | Hạn | Second reader | Issue |
| --- | --- | --- | --- | --- | --- |
| T2 28/12/2026 | DAT | `W11-DAT-01` Đồ án Chương 3 (phương pháp); phản biện mục của LDN | CN 03/01/2027 | LDN |  |
| T2 28/12/2026 | FAO | `W11-FAO-01` Đồ án Chương 1 (lý thuyết), Chương 2 (tổng quan); phản biện mục của DAT | CN 03/01/2027 | DAT |  |
| T2 28/12/2026 | LDN | `W11-LDN-01` Đồ án Chương 4 (thực nghiệm); phản biện mục của FAO | CN 03/01/2027 | FAO |  |
| T7 02/01/2027 | DAT | `S-GVHD-3` Họp GVHD định kỳ (2 tuần/lần) | CN 03/01/2027 |  |  |

## W12

| Bắt đầu | Ai | Task | Hạn | Second reader | Issue |
| --- | --- | --- | --- | --- | --- |
| T2 04/01/2027 | DAT | `W12-DAT-01` Abstract (viết cuối), kiểm tra định dạng hội nghị, gửi GVHD | T7 09/01/2027 | LDN | #4 |
| T2 04/01/2027 | LDN | `W12-LDN-01` Đối chiếu mọi con số trong bài với claim–evidence | T6 08/01/2027 |  | #4 |
| T4 06/01/2027 | FAO | `W12-FAO-01` Bàn giao artifact (Form J): smoke test từ clone sạch, tag submission | T7 09/01/2027 | LDN | #4 |
| CN 10/01/2027 | ALL | `W12-ALL-01` GATE G3 — bài báo và đồ án sẵn sàng | CN 10/01/2027 |  | #4 |

Lặp lại: ghi chú ngày (Form H) mỗi ngày làm việc; họp nhóm thứ Hai 20:00.
