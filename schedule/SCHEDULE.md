# Lịch theo ngày (tự sinh — KHÔNG sửa tay)

> Sinh bởi `python scripts/today.py --render` từ `schedule/tasks.json` (chỉ DAT chạy lại khi lịch đổi).
> Trạng thái thực tế: `python scripts/today.py --team`. Việc của bạn hôm nay: hỏi Claude
> "hôm nay tôi cần làm gì?" trong repo này, hoặc chạy `python scripts/today.py`.

| Gate | Ngày | Nội dung |
| --- | --- | --- |
| **G0** | 2026-11-01 | Chốt định vị đóng góp |
| **G1** | 2026-11-15 | Pilot: PPO học được, khoá PREREG, chọn phương án A/B |
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
| T6 30/10/2026 | DAT | `W2-DAT-03` Soạn báo cáo G0 (Form G) | T6 30/10/2026 | LDN | #1 |
| T6 30/10/2026 | FAO | `W2-FAO-04` Second reader tune_ppo.py: đọc mã, chạy 2 lượt nhỏ | T7 31/10/2026 |  | #11 |
| T6 30/10/2026 | LDN | `W2-LDN-03` Second reader báo cáo G0 + chốt số PRISMA | T7 31/10/2026 |  | #6 |
| CN 01/11/2026 | ALL | `W2-ALL-01` GATE G0 — họp 45', gửi GVHD | CN 01/11/2026 |  | #1 |

## W3

| Bắt đầu | Ai | Task | Hạn | Second reader | Issue |
| --- | --- | --- | --- | --- | --- |
| T2 02/11/2026 | DAT | `W3-DAT-01` EXP-02: huấn luyện seed 0 (DR và Fixed) trên máy cố định | T4 04/11/2026 | FAO |  |
| T3 03/11/2026 | LDN | `W3-LDN-01` Đánh giá từng model EXP-02 ngay khi xong; bảng mô tả tạm | CN 08/11/2026 | FAO |  |
| T5 05/11/2026 | DAT | `W3-DAT-02` EXP-02: huấn luyện seed 1 (DR và Fixed) | T7 07/11/2026 | FAO |  |
| T5 05/11/2026 | FAO | `W3-FAO-01` Manifest checkpoint EXP-02 + second reader quỹ đạo (≥ 3/model) | CN 08/11/2026 |  |  |

## W4

| Bắt đầu | Ai | Task | Hạn | Second reader | Issue |
| --- | --- | --- | --- | --- | --- |
| T2 09/11/2026 | DAT | `W4-DAT-01` Optuna trên id (DR và Fixed, cùng số trial); đề xuất siêu tham số EXP-03 | T6 13/11/2026 | FAO | #11 |
| T2 09/11/2026 | FAO | `W4-FAO-01` Điền docs/PREREG.md (cấu hình, seed, ngân sách) | T6 13/11/2026 | LDN |  |
| T2 09/11/2026 | LDN | `W4-LDN-01` Báo cáo G1 (Form G) — nộp trước 14/11 | T7 14/11/2026 | FAO | #2 |
| T5 12/11/2026 | FAO | `W4-FAO-02` Lập lịch phân seed giữa các máy | T7 14/11/2026 | DAT |  |
| T5 12/11/2026 | LDN | `W4-LDN-02` Viết EXP-03 card (10 seed × 2 learner) | T7 14/11/2026 | FAO |  |
| CN 15/11/2026 | ALL | `W4-ALL-01` GATE G1 — chọn A/B, khoá PREREG (ghi commit) | CN 15/11/2026 |  | #2 |

## W5

| Bắt đầu | Ai | Task | Hạn | Second reader | Issue |
| --- | --- | --- | --- | --- | --- |
| T2 16/11/2026 | DAT | `W5-DAT-01` EXP-03 seed 0–4 trên máy cố định | CN 22/11/2026 | LDN |  |
| T2 16/11/2026 | FAO | `W5-FAO-01` EXP-03 seed 5–9 (Kaggle hoặc máy FAO) | CN 22/11/2026 | LDN |  |
| T2 16/11/2026 | LDN | `W5-LDN-01` Pipeline phân tích EXP-03 (H1/H2, IQM, Holm, Cliff's δ) | T6 20/11/2026 | FAO |  |
| T4 18/11/2026 | DAT | `W5-DAT-02` Viết mục System Model (paper/main.tex) | CN 22/11/2026 | FAO |  |
| T4 18/11/2026 | FAO | `W5-FAO-02` EXP-04 card + bắt đầu DR-DQN 10 seed | CN 22/11/2026 | DAT |  |
| T5 19/11/2026 | LDN | `W5-LDN-02` Viết mục Experimental Setup | CN 22/11/2026 | DAT |  |

## W6

| Bắt đầu | Ai | Task | Hạn | Second reader | Issue |
| --- | --- | --- | --- | --- | --- |
| T2 23/11/2026 | DAT | `W6-DAT-01` Cài biến thể quan sát A2 (lưới tuyệt đối), A3 (vector padding) + EXP-06 card | CN 29/11/2026 | FAO |  |
| T2 23/11/2026 | DAT | `W6-DAT-02` [Chỉ phương án A] Hoàn thiện và nộp bản MVP 6–8 trang _(PLAN: A)_ | CN 29/11/2026 | LDN |  |
| T2 23/11/2026 | FAO | `W6-FAO-01` EXP-04 tiếp: DR-DQN seed 5–9 | CN 29/11/2026 | DAT |  |
| T2 23/11/2026 | LDN | `W6-LDN-01` Phân tích tạm EXP-03 (≥ 5 seed): bảng H1/H2, CI | T6 27/11/2026 | FAO |  |
| T4 25/11/2026 | FAO | `W6-FAO-02` Hình F6: quỹ đạo TSP vs DR-PPO trên cùng kịch bản cụm; EXP-07 card | CN 29/11/2026 | LDN |  |
| T5 26/11/2026 | LDN | `W6-LDN-02` Viết EXP-05 card (quét λ) | CN 29/11/2026 | DAT |  |
| T7 28/11/2026 | DAT | `S-GVHD-1` Họp GVHD định kỳ (2 tuần/lần) | CN 29/11/2026 |  |  |

## W7

| Bắt đầu | Ai | Task | Hạn | Second reader | Issue |
| --- | --- | --- | --- | --- | --- |
| T2 30/11/2026 | DAT | `W7-DAT-01` Chạy EXP-06 (5 seed/biến thể) | CN 06/12/2026 | FAO |  |
| T2 30/11/2026 | FAO | `W7-FAO-01` Chạy EXP-07 (A4 bỏ mask, A5 một tốc độ), 5 seed | CN 06/12/2026 | LDN |  |
| T2 30/11/2026 | LDN | `W7-LDN-01` Chạy EXP-05 quét λ (5 λ × 5 seed) | CN 06/12/2026 | DAT |  |
| T5 03/12/2026 | FAO | `W7-FAO-02` Second reader EXP-03: chạy lại đánh giá 2 model bất kỳ, so khớp events.csv | CN 06/12/2026 |  |  |

## W8

| Bắt đầu | Ai | Task | Hạn | Second reader | Issue |
| --- | --- | --- | --- | --- | --- |
| T2 07/12/2026 | DAT | `W8-DAT-01` Second reader EXP-05 và EXP-04 | T4 09/12/2026 |  |  |
| T2 07/12/2026 | FAO | `W8-FAO-01` Second reader EXP-06 | T4 09/12/2026 |  |  |
| T2 07/12/2026 | LDN | `W8-LDN-01` Hình F3 (đường học), F4, F5 từ raw | T6 11/12/2026 | DAT |  |
| T2 07/12/2026 | LDN | `W8-LDN-02` Second reader EXP-07 | T4 09/12/2026 |  |  |
| T4 09/12/2026 | DAT | `W8-DAT-02` Viết mục Method (MDP, quan sát, thưởng, DR) | CN 13/12/2026 | FAO |  |
| T4 09/12/2026 | FAO | `W8-FAO-02` Hoàn tất data/checkpoint_manifest.md | CN 13/12/2026 | DAT |  |
| T6 11/12/2026 | LDN | `W8-LDN-03` Cập nhật claim–evidence → measured | CN 13/12/2026 | FAO |  |
| T7 12/12/2026 | DAT | `S-GVHD-2` Họp GVHD định kỳ (2 tuần/lần) | CN 13/12/2026 |  |  |

## W9

| Bắt đầu | Ai | Task | Hạn | Second reader | Issue |
| --- | --- | --- | --- | --- | --- |
| T2 14/12/2026 | DAT | `W9-DAT-01` Khoá commit kết quả (tag results-freeze) | T2 14/12/2026 |  | #3 |
| T2 14/12/2026 | FAO | `W9-FAO-01` Tái lập độc lập: chạy lại toàn bộ evaluate.py từ commit khoá trên máy khác | T6 18/12/2026 |  |  |
| T2 14/12/2026 | LDN | `W9-LDN-01` Phân tích cuối từ commit khoá; kiểm định H1/H2 (Holm) | T6 18/12/2026 | FAO |  |
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

Lặp lại: ghi chú ngày (Form H) mỗi ngày làm việc; gặp mặt làm việc T3, T4, T6 (không biên bản).
