# 05 — Kế hoạch chi tiết (3 thành viên)

> **Đây là kế hoạch hiện hành.** Thay thế mọi bản trước. Day 0 = thứ Hai 19/10/2026. Mốc lịch là mặc định; **kết quả tại gate quan trọng hơn lịch.**

| Nick | Họ tên | GitHub | Vai trò chính |
| --- | --- | --- | --- |
| **DAT** | Hồ Du Tuấn Đạt | `Tdat10052499` | Phương pháp DR-PPO, định vị đóng góp, điều phối, đo thời gian, chủ trì bản thảo |
| **LDN** | Dương Ngọc Linh Đan | `Yui-Mika` | Ma trận thực nghiệm, thống kê, gate report, claim–evidence, hình từ raw |
| **FAO** | Nguyễn Minh Chính | `F4ol4n` | Môi trường chạy và tái lập, chi phí tính toán, provenance checkpoint, DQN, quỹ đạo |

**Nguyên tắc chung**
- Mỗi kết quả có một **owner** và một **second reader**. Owner giải thích cho second reader trước khi kết quả vào bài.
- Mỗi ngày làm việc, mỗi người viết `notes/YYYY-MM-DD_<nick>.md`: 3 câu và 1 bằng chứng (run ID, hình hoặc commit) theo Form H.
- Experiment card viết **trước** khi chạy. Không sửa `results/raw/`; sửa phân tích thì sinh lại từ cùng dữ liệu raw.

---

## 1. Lịch tổng quan

| Tuần | Ngày | Mốc | Trọng tâm |
| --- | --- | --- | --- |
| W1 | 19–25/10 | — | Tái lập (EXP-01), đọc tài liệu, xác minh hội nghị |
| W2 | 26/10–01/11 | **G0 · 01/11** | Tổng quan hệ thống, ma trận định vị, công cụ phân tích |
| W3 | 02–08/11 | — | EXP-02 pilot: 4 lần huấn luyện |
| W4 | 09–15/11 | **G1 · 15/11** | Phân tích pilot, Optuna trên ID, khoá PREREG, chọn A/B |
| W5 | 16–22/11 | — | EXP-03 (10 seed × 2 learner), EXP-04 DQN |
| W6 | 23–29/11 | (A: nộp bài MVP) | EXP-03 tiếp, viết Setup/System Model |
| W7 | 30/11–06/12 | — | EXP-05 quét λ, EXP-06/07 ablation |
| W8 | 07–13/12 | — | Hoàn tất ablation, hình F3–F6, claim–evidence |
| W9 | 14–20/12 | **G2 · 20/12** | Đóng băng kết quả, tái lập độc lập |
| W10 | 21–27/12 | — | Viết bài đầy đủ |
| W11 | 28/12–03/01 | — | Đồ án, phản biện nội bộ vòng 1 |
| W12 | 04–10/01 | **G3 · 10/01** | Phản biện vòng 2, bàn giao artifact (Form J) |

---

## 2. Chi tiết tuần 1 (theo ngày)

| Ngày | DAT | LDN | FAO |
| --- | --- | --- | --- |
| **T2 19/10** (Day 0) | Chủ trì họp khởi động 60'. Gửi `Project Agreement.md` cho GVHD. Mời 2 thành viên vào repo. | Họp khởi động. Lập thư mục `notes/reading/`; nắm quy ước file (`notes/workbook_forms.md`). | Họp khởi động. Clone repo, tạo venv, `pip install -r environment/requirements.txt`. |
| **T3 20/10** | Đọc toàn văn Bayerlein 2021 → Form B. Email hỏi lịch FJCAI 2027 và ICISN 2027 (issue #7). | Đọc Agarwal 2021 (thống kê RL) và Yi 2020 → Form B. | EXP-01 bước 1–3: tests, smoke test, `evaluate.py` heuristic → so khớp với file tham chiếu. |
| **T4 21/10** | Đọc Zeng 2019 (mô hình năng lượng) và Lamenza 2025 → Form B. Bắt đầu ma trận `docs/04` §5. | Chạy smoke test trên máy mình (máy thứ 2 cho EXP-01). | EXP-01 bước 4: `train_ppo.py` 10k bước; sửa lỗi API nếu có (PR, DAT review). Điền `environment/machine_notes.md`. |
| **T5 22/10** | **Second reader EXP-01**: chạy lại trên máy cố định. Đo 100k bước trên máy cố định (quy tắc đo). | Tìm kiếm Q1 (`docs/04` §6): ghi số kết quả, lọc tiêu đề/tóm tắt. | Hoàn thành Form C trong `notes/EXP-01_reproduction_card.md`. Đóng issue #5. |
| **T6 23/10** | Viết khung Optuna (`scripts/tune_ppo.py`) — chưa chạy. | Tìm kiếm Q2, Q3; tổng hợp danh sách đọc toàn văn. | Ước lượng chi phí tính toán → `Project Agreement.md` §5. Thiết lập Kaggle (nếu dùng). |
| **T7–CN 24–25/10** | Dự phòng. Tổng hợp góp ý GVHD về ngưỡng gate (**hạn duyệt 25/10**). | Dự phòng / đọc thêm. | Dự phòng. |

## 3. Chi tiết tuần 2 (→ G0)

| Ngày | DAT | LDN | FAO |
| --- | --- | --- | --- |
| T2–T3 26–27/10 | Đọc toàn văn các bài LDN chọn (chia đôi với LDN). Viết câu định vị bản 2. | Đọc toàn văn phần còn lại; điền ma trận. Đọc Sarathchandra 2025. | Đọc Abd-Elmagid 2019, OH-DRL 2025, Sun 2025 → Form B. Bắt đầu `scripts/plot_trajectory.py` (vẽ quỹ đạo một episode ra `figures/`). |
| T4–T5 28–29/10 | Hoàn thiện `tune_ppo.py`: không gian tìm kiếm, ngân sách bằng nhau, chỉ đánh giá trên ID. | Mở rộng `analyze.py`: bảng độ suy giảm theo seed và hình F4 (cột + CI). Kiểm thử bằng dữ liệu heuristic. | Chạy thử DR-DQN 10k bước (`--algo dqn`). Hoàn thiện script quỹ đạo. |
| T6 30/10 | Soạn báo cáo G0 (Form G) `notes/2026-11-01_gate_G0_report.md`. | **Second reader báo cáo G0**: kiểm tra từng dòng ma trận có nguồn. | **Second reader** `tune_ppo.py` (đọc mã, chạy 2 lượt nhỏ). |
| CN 01/11 | **Gate G0** — họp 45' cả nhóm, gửi GVHD. | | |

---

## 4. Tuần 3–12 theo thành viên

| Tuần | DAT | LDN | FAO |
| --- | --- | --- | --- |
| **W3** 02–08/11 | Huấn luyện EXP-02 trên máy cố định: s0-DR, s0-Fixed, s1-DR, s1-Fixed. | Chạy `evaluate.py` cho từng model ngay khi xong. Viết bảng mô tả tạm. | Ghi `data/checkpoint_manifest.md` cho 4 model. Second reader quỹ đạo: xem ≥ 3 quỹ đạo mỗi model, tìm hành vi suy biến. |
| **W4** 09–15/11 | Optuna trên ID (DR và Fixed, cùng số lượt). Đề xuất siêu tham số cho EXP-03. | Báo cáo G1 (Form G) `notes/2026-11-15_gate_G1_report.md` trước 14/11. Viết EXP-03 card. | Điền `docs/PREREG.md` (cấu hình, seed, ngân sách). Lập lịch phân seed giữa các máy. |
| | **Gate G1 · CN 15/11** — chọn phương án A/B, khoá PREREG (ghi commit). | | |
| **W5** 16–22/11 | Chạy EXP-03 seed 0–4 trên máy cố định. Viết mục System Model (từ `docs/02`). | Hoàn thiện pipeline phân tích EXP-03; viết mục Experimental Setup. | Chạy EXP-03 seed 5–9 (Kaggle hoặc máy FAO); bắt đầu EXP-04 DR-DQN 10 seed. |
| **W6** 23–29/11 | Cài biến thể quan sát A2 (lưới tuyệt đối) và A3 (vector padding) cho EXP-06; viết card. | Phân tích tạm EXP-03 (≥ 5 seed): bảng H1/H2, CI. | EXP-04 tiếp; vẽ F6 (quỹ đạo TSP vs DR-PPO trên cùng kịch bản cụm). |
| **W7** 30/11–06/12 | Chạy EXP-06 (5 seed/biến thể). | Chạy EXP-05 quét λ ∈ {0; 0,05; 0,1; 0,2; 0,5}, 5 seed mỗi λ. | Chạy EXP-07 (A4 bỏ mask, A5 một tốc độ), 5 seed. |
| **W8** 07–13/12 | Second reader EXP-05; viết mục Method. | Hình F3 (đường học), F4, F5 từ raw; cập nhật claim–evidence → *measured*. | Second reader EXP-06; cập nhật manifest checkpoint đầy đủ. |
| **W9** 14–20/12 | Báo cáo G2. | Phân tích cuối từ commit khoá; kiểm định H1/H2 (Holm). | **Tái lập độc lập**: chạy lại toàn bộ `evaluate.py` từ commit khoá trên máy khác, so khớp `events.csv`. |
| | **Gate G2 · CN 20/12** — đóng băng kết quả. | | |
| **W10** 21–27/12 | Viết Introduction, Method, Discussion. | Viết Results, Experimental Setup. | Viết Related Work (từ ma trận), Limitations. |
| **W11** 28/12–03/01 | Đồ án: Chương 3 (phương pháp). Phản biện mục của LDN. | Đồ án: Chương 4 (thực nghiệm). Phản biện mục của FAO. | Đồ án: Chương 1 (lý thuyết), Chương 2 (tổng quan). Phản biện mục của DAT. |
| **W12** 04–10/01 | Abstract (viết cuối). Kiểm tra định dạng hội nghị. Nộp cho GVHD. | Đối chiếu mọi con số với claim–evidence (*independently checked*). | Bàn giao artifact (Form J): smoke test từ clone sạch, tag `submission-<venue>`. |
| | **Gate G3 · CN 10/01/2027** | | |

**Phương án A (MVP)**, nếu chọn tại G1 vì có hội nghị hạn cuối tháng 11 – đầu tháng 12:
- Tuần W5–W6 dùng EXP-03 với ≥ 5 seed.
- Viết bài 6–8 trang (DAT chủ trì; LDN viết Results; FAO viết Related Work).
- Phần còn lại của lịch giữ nguyên cho bản đầy đủ và đồ án. Bản đầy đủ phải mở rộng đáng kể và trích dẫn bản MVP.

---

## 5. Tiêu chí gate (khai báo trước — **đề xuất, GVHD duyệt trước 25/10**)

### G0 · 01/11 — định vị đóng góp (owner DAT, second reader LDN)
| # | Điều kiện | Nếu không đạt |
| --- | --- | --- |
| 1 | Ma trận `docs/04` §5 đủ các công trình gần nhất; mỗi ô có nguồn (mục/bảng) | Kéo dài tối đa 3 ngày |
| 2 | Không có công trình nào đủ cả 5 cột: AoI, năng lượng theo tốc độ, huấn luyện nhiều bố trí, OOD có cấu trúc, nhiều seed + CI | Đổi trọng tâm: A5 (vai trò lựa chọn tốc độ) hoặc đa UAV — GVHD quyết |
| 3 | Câu định vị (`docs/01` §3) được GVHD đồng ý | Viết lại |

### G1 · 15/11 — pilot (owner LDN viết báo cáo, DAT huấn luyện, FAO second reader)
Ngưỡng tính từ kết quả tham chiếu: Random trên `id` = 126,24 khe; TSP trên `id` = 28,64 khe (`results/processed/heuristics_summary_2026-10-16.md`).

| # | Điều kiện | Ngưỡng | Nếu không đạt |
| --- | --- | --- | --- |
| 1 | Tái lập | Smoke test PASS trên ≥ 2 máy; EXP-01 không lệch dòng nào | **Dừng mọi thứ**, debug |
| 2 | PPO học được | Ā(DR-PPO, `id`) ≤ 63,1 khe (0,5 × Random) ở **cả 2 seed** | Debug reward/quan sát/siêu tham số; không mở rộng |
| 3 | Mức cạnh tranh | Ā(DR-PPO, `id`) ≤ 43,0 khe (1,5 × TSP) ở ≥ 1 seed | Không chặn; bỏ claim C2 "thắng heuristic" |
| 4 | Tín hiệu hiệu ứng chính | deg(DR) < deg(Fixed) trên `ood_cluster` và ≥ 1 bộ OOD khác, ở **cả 2 seed** | Thu hẹp hoặc đổi trọng tâm (A5 / đa UAV) — GVHD quyết |
| 5 | Không suy biến | Chạm biên = 0 khi có mask; không loại hành động nào chiếm ≥ 90%; FAO đã xem ≥ 3 quỹ đạo mỗi model | Debug |
| 6 | Ngân sách | steps/s đo được cho phép EXP-03 đến EXP-07 xong trước 13/12 | Giảm số bước trước; giảm seed sau (tối thiểu 5, ghi rõ) |

Đây là pilot **thăm dò** (2 seed): chỉ mô tả, không đưa p-value vào bài.

### G2 · 20/12 — đóng băng (owner DAT, second reader FAO)
| # | Điều kiện |
| --- | --- |
| 1 | EXP-03 và EXP-04 đủ 10 seed mỗi learner; EXP-05 đến EXP-07 đủ 5 seed |
| 2 | FAO tái lập toàn bộ đánh giá từ commit khoá và `events.csv` khớp |
| 3 | Mọi claim ở trạng thái *measured*; hình sinh từ script, không chỉnh tay |
| 4 | Lần chạy thất bại được liệt kê kèm lý do |

### G3 · 10/01/2027 — sẵn sàng nộp (owner DAT)
Danh sách `docs/06` §3 + Form J (`notes/workbook_forms.md`). Mọi claim *independently checked*.

---

## 6. Nhịp làm việc
- **Họp nhóm:** thứ Hai 20:00, 30'. Mỗi người mang 1 hình hoặc 1 bảng mới.
- **Họp GVHD:** 2 tuần/lần và tại mỗi gate. Mang theo 1 kết quả, 1 diễn giải, 1 câu hỏi chưa giải quyết, 1 đề xuất bước tiếp. Nếu bị chặn, mang ví dụ lỗi nhỏ nhất.
- **Git:** nhánh `<nick>/<chủ-đề>`, ví dụ `ldn/analyze-deg`. Mọi thay đổi trong `src/` qua PR, second reader review. Không push thẳng `main` trừ `notes/`.
- **Issue:** mỗi công việc tuần có issue gắn milestone gate; người nhận tự gán khi bắt đầu.
- **Nghỉ ngơi:** thực nghiệm dài chạy qua đêm chỉ với cấu hình đã kiểm tra; lần chạy đầu của cấu hình mới phải có người theo dõi.
