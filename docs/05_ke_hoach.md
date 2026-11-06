# 05 — Kế hoạch chi tiết (3 thành viên)

> **Đây là kế hoạch hiện hành.** Thay thế mọi bản trước. Bản máy đọc được, chia theo ngày, nằm ở `schedule/tasks.json` (bảng xem: `schedule/SCHEDULE.md`). Hai bản phải khớp nhau; khi đổi lịch, DAT sửa cả hai trong cùng một PR và ghi lý do vào `docs/DECISIONS.md`. Day 0 = thứ Hai 19/10/2026. Mốc lịch là mặc định; **kết quả tại gate quan trọng hơn lịch.**

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
| W2 | 26/10–01/11 | **G0 · 04/11** | Tổng quan hệ thống, ma trận định vị, công cụ phân tích |
| W3 | 02–08/11 | — | EXP-02b chẩn đoán, khoá PREREG gốc, EXP-03 (theo lịch nén FJCAI); 06/11 đổi phương pháp |
| W4 | 09–15/11 | — | Báo cáo EXP-03; EXP-08a; mã quan sát neo, wrapper tour-guided, TSP-eco/adaptive |
| W5 | 16–22/11 | **G1 · 20/11** | Pilot EXP-08p, khoá PREREG phụ lục B |
| W6 | 23–29/11 | — | EXP-08: 4 nhánh × 10 seed; viết System Model, Setup |
| W7 | 30/11–06/12 | — | Đánh giá EXP-08, second reader provenance |
| W8 | 07–13/12 | — | Hình F3–F6, claim–evidence, mục Method |
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

> **Sửa 06/11/2026** (DECISIONS 2026-11-06): sau EXP-03, nhóm đổi sang phương pháp PG-TG-PPO (quan sát neo vật lý + PPO tầng cao dẫn hướng theo tour TSP). W4–W9 dưới đây là lịch mới. EXP-04 đến EXP-07 hoãn. Nguồn sự thật vẫn là `schedule/tasks.json`.

| Tuần | DAT | LDN | FAO |
| --- | --- | --- | --- |
| **W3** 02–08/11 | Huấn luyện EXP-02 trên máy cố định: s0-DR, s0-Fixed, s1-DR, s1-Fixed. | Chạy `evaluate.py` cho từng model ngay khi xong. Viết bảng mô tả tạm. | Ghi `data/checkpoint_manifest.md` cho 4 model. Second reader quỹ đạo: xem ≥ 3 quỹ đạo mỗi model, tìm hành vi suy biến. |
| **W4** 09–15/11 | Kiểm lại Bayerlein 2021 (pin trong quan sát) + Form B Theile ~2020. PR `dat/tour-guided`: wrapper semi-MDP, tầng cao greedy, `train_ppo.py --policy options`. | EXP-08a: chẩn đoán từ dữ liệu EXP-03. Báo cáo chính thức H1/H2 của EXP-03 (PR #43). Power analysis cho δ₅–δ₇. | PR `fao/grounded-obs` (`obs_mode`). PR `fao/tsp-manh`: TSP-eco, TSP-adaptive, bộ đánh giá mới seed 300000–300099. |
| **W5** 16–22/11 | Pilot EXP-08p (M1, M4; seed 0–1) trên máy cố định, đo bước/s. Viết mục System Model. | Báo cáo G1 (Form G) `notes/2026-11-20_gate_G1_report.md`. Bắt đầu mục Experimental Setup. | Đưa PREREG phụ lục B vào `docs/PREREG.md` (PR). Second reader EXP-03. |
| | **Gate G1 · T6 20/11** — duyệt pilot, khoá PREREG phụ lục B (tag `prereg-B-lock`). | | |
| **W6** 23–29/11 | EXP-08: huấn luyện M1, M2 (seed 10–19) trên laptop DAT (21/11–02/12). | `analyze.py` cho H5–H7 (PR). Experimental Setup. | EXP-08: huấn luyện M3, M4 (seed 10–19) trên máy FAO hoặc Kaggle (21/11–02/12). |
| **W7** 30/11–06/12 | Đánh giá 40 model + 6 baseline trên bộ chính và bộ phụ; push raw. | Mô tả tạm EXP-08 và phân tích thăm dò. | Second reader EXP-08: provenance từng run, chạy lại đánh giá 2 model. |
| **W8** 07–13/12 | Second reader phân tích EXP-08; viết mục Method. | Hình F3, F4, F5 từ raw; cập nhật claim–evidence → *measured*. | Hình F6 (quỹ đạo TSP-adaptive và M1), bảng hành vi; manifest checkpoint đầy đủ. |
| **W9** 14–20/12 | Báo cáo G2. | Phân tích cuối từ commit khoá: H5–H7 và H1/H2 của EXP-03. | **Tái lập độc lập**: chạy lại toàn bộ `evaluate.py` từ commit khoá trên máy khác, so khớp `events.csv`. |
| | **Gate G2 · CN 20/12** — đóng băng kết quả. | | |
| **W10** 21–27/12 | Viết Introduction, Method, Discussion. | Viết Results, Experimental Setup. | Viết Related Work (từ ma trận), Limitations. |
| **W11** 28/12–03/01 | Đồ án: Chương 3 (phương pháp). Phản biện mục của LDN. | Đồ án: Chương 4 (thực nghiệm). Phản biện mục của FAO. | Đồ án: Chương 1 (lý thuyết), Chương 2 (tổng quan). Phản biện mục của DAT. |
| **W12** 04–10/01 | Abstract (viết cuối). Kiểm tra định dạng hội nghị. Nộp cho GVHD. | Đối chiếu mọi con số với claim–evidence (*independently checked*). | Bàn giao artifact (Form J): smoke test từ clone sạch, tag `submission-<venue>`. |
| | **Gate G3 · CN 10/01/2027** | | |

**Phương án dự phòng** (quyết định tại G1 nếu pilot EXP-08p cho thấy M1 không học được, Ā ≈ Random): bỏ tầng tour, chỉ giữ quan sát neo vật lý với PPO phẳng (nhánh M4). Lịch W6–W12 giữ nguyên; thay M1 bằng M4 trong H5–H7 và ghi DECISIONS trước khi khoá.

---

## 5. Tiêu chí gate (khai báo trước; GVHD góp ý khi review bản nháp bài, xem DECISIONS 06/11)

### G0 · 01/11 — định vị đóng góp (owner DAT, second reader LDN)
> **Đã kéo dài sang T4 04/11/2026** theo điều khoản của tiêu chí 1 (DECISIONS 2026-10-30). Đây là lần kéo dài duy nhất được phép.
| # | Điều kiện | Nếu không đạt |
| --- | --- | --- |
| 1 | Ma trận `docs/04` §5 đủ các công trình gần nhất; mỗi ô có nguồn (mục/bảng) | Kéo dài tối đa 3 ngày |
| 2 | Không có công trình nào đủ cả 5 cột: AoI, năng lượng theo tốc độ, huấn luyện nhiều bố trí, OOD có cấu trúc, nhiều seed + CI | Đổi trọng tâm: A5 (vai trò lựa chọn tốc độ) hoặc đa UAV — GVHD quyết |
| 3 | Câu định vị (`docs/01` §3) được cả nhóm thống nhất | Viết lại |

### G1 · T6 20/11 — pilot PG-TG-PPO (owner LDN viết báo cáo, DAT huấn luyện, FAO second reader)
> **Thay ngày 06/11/2026.** Tiêu chí G1 cũ (pilot EXP-02, ngày 15/11) không còn áp dụng vì EXP-03 đã chạy theo lịch nén FJCAI; xem lịch sử git của file này. Ngưỡng 1,2 × TSP-adaptive và 0,2 lấy từ `notes/EXP-08_PG-TG-PPO_card.md` (EXP-08p), là ngưỡng hành động của pilot, **không** phải ngưỡng giả thuyết.

| # | Điều kiện | Ngưỡng | Nếu không đạt |
| --- | --- | --- | --- |
| 1 | Tái lập | Smoke test PASS trên ≥ 2 máy; EXP-01 chạy lại với `obs_mode = legacy` không lệch dòng nào | **Dừng mọi thứ**, debug |
| 2 | Chẩn đoán EXP-08a | Đã chạy; kết luận khớp hoặc không khớp dự đoán của card đều được ghi | Không khớp: xem lại thành phần A trước khi pilot |
| 3 | Tour-guided học được | Ā(M1, `id`) ≤ 1,2 × Ā(TSP-adaptive, `id`) **và** S(M1, `ood_energy`) > 0,2 (cách gộp 2 seed: LDN chốt trước khi chạy pilot ✱) | Học được nhưng chưa đạt: một vòng chỉnh siêu tham số, pilot lại 1 lần. Ā ≈ Random: phương án dự phòng (§4) |
| 4 | Không suy biến | Không loại quyết định nào chiếm ≥ 90%; FAO đã xem ≥ 3 quỹ đạo mỗi model | Debug |
| 5 | Ngân sách | bước/s đo trên laptop DAT cho phép EXP-08 (40 model) xong trước 06/12 | Giảm số bước trước; giảm seed sau (tối thiểu theo power analysis, ghi rõ) |
| 6 | PREREG phụ lục B đầy đủ | δ₅–δ₇ có lý do độc lập với số EXP-03 (nhóm xác nhận); power ≥ 0,8 hoặc đã tăng seed; SHA256 cấu hình và manifest bộ đánh giá đã điền | Không khoá; dời G1 tối đa 3 ngày, báo DAT |

Đây là pilot **thăm dò** (2 seed): chỉ mô tả, không đưa p-value vào bài. Bộ đánh giá mới (seed 300000–300099) không được chạy trước khi khoá.

### G2 · 20/12 — đóng băng (owner DAT, second reader FAO)
| # | Điều kiện |
| --- | --- |
| 1 | EXP-03 đủ 10 seed mỗi nhánh (đã có); EXP-08 đủ 10 seed mỗi nhánh M1–M4 (hoặc số seed theo power analysis ghi trong PREREG phụ lục B) |
| 2 | FAO tái lập toàn bộ đánh giá từ commit khoá và `events.csv` khớp |
| 3 | Mọi claim ở trạng thái *measured*; hình sinh từ script, không chỉnh tay |
| 4 | Lần chạy thất bại được liệt kê kèm lý do |

### G3 · 10/01/2027 — sẵn sàng nộp (owner DAT)
Danh sách `docs/06` §3 + Form J (`notes/workbook_forms.md`). Mọi claim *independently checked*.

---

## 6. Nhịp làm việc
- **Họp nhóm:** thứ Hai 20:00, 30'. Mỗi người mang 1 hình hoặc 1 bảng mới.
- **GVHD:** góp ý và review bản nháp bài, nhóm chỉnh sửa thành bản cuối (W12-DAT-01). Lịch không có việc hỏi GVHD hay họp định kỳ (DECISIONS 06/11).
- **Git:** nhánh `<nick>/<chủ-đề>`, ví dụ `ldn/analyze-deg`. Mọi thay đổi trong `src/` qua PR, second reader review. Không push thẳng `main` trừ `notes/`.
- **Issue:** mỗi công việc tuần có issue gắn milestone gate; người nhận tự gán khi bắt đầu.
- **Nghỉ ngơi:** thực nghiệm dài chạy qua đêm chỉ với cấu hình đã kiểm tra; lần chạy đầu của cấu hình mới phải có người theo dõi.
