# Form B — `sun2025aoi`

> Trạng thái: soạn từ toàn văn PDF (arXiv v1, 21 trang). FAO rà lại trước khi đánh dấu W2-FAO-01 xong; second reader: LDN. Các số "đọc từ hình" là xấp xỉ.

**Tiêu đề / tác giả / năm / nơi công bố hoặc trạng thái preprint:** *Age of Information Optimization in Laser-charged UAV-assisted IoT Networks: A Multi-agent Deep Reinforcement Learning Method*, 2025.
- **Tác giả:** Geng Sun, Likun Zhang, Jiahui Li, Jing Wu (tác giả liên hệ), Jiacheng Wang, Zemin Sun, Changyuan Zhao, Victor C. M. Leung (ĐH Cát Lâm, NTU, ĐH Thâm Quyến/UBC).
- **Trạng thái:** preprint arXiv:2507.08429v1 [cs.NI], 11/07/2025. PDF không ghi nơi công bố chính thức ✱.
- **Lưu ý:** `paper/references.bib` đang ghi `author = {Sun, Geng and others}`, nên bổ sung đủ danh sách tác giả.

**URL nguồn gốc và phiên bản/ngày truy cập:** https://arxiv.org/abs/2507.08429 (v1), truy cập ngày 20/10/2026.

**Người đọc (NICK):** FAO

**Bài báo trả lời câu hỏi gì:** Bài tìm cách tối thiểu peak AoI trong mạng IoT có nhiều UAV thu dữ liệu, khi UAV được sạc bằng laser (LBD) mỗi lần bay vào vùng sạc. Quỹ đạo và chiến lược sạc được tối ưu đồng thời (§I, §III-F, PT (5)).

**Giả định hệ thống:**
- **Quy mô:** N_U = 4 UAV, N_S = 50 IoT, độ cao H = 80 m, t_d = 1 s mỗi slot (Bảng IV, §III-A).
- **Tốc độ:** **hằng số**, v = 5 m/s (§III-A giả định 1, Bảng IV).
- **Kênh:** xác suất LoS/NLoS dạng sigmoid theo góc ngẩng (PT (1)).
- **Năng lượng đẩy:** mô hình công suất rotary-wing P(v) (PT (4)), cùng dạng với Zeng 2019, với các tham số trong Bảng IV (Pα = 14,75 W, Pβ = 41,54 W, v_tip = 80 m/s, v₀ = 5,05 m/s). Vì v cố định nên năng lượng đẩy chỉ phụ thuộc thời gian bay; tốc độ không phải biến quyết định. Đây là suy luận từ §III-A và Bảng IV.
- **Sạc laser:** công suất nhận theo khoảng cách tới LBD (PT (2)), trong bán kính R_c = 250 m. P_L = 1000 W và η_le = 0,15 (Bảng IV).
- **Mục tiêu:** peak AoI = max_i a_i (PT (3), (5a)).
- **Dữ liệu IoT:** lượng dữ liệu V_i tĩnh, và việc thu là tức thời khi UAV ở trong tầm (§III-A, các giả định).

**Cơ chế, diễn đạt bằng lời của mình:**
- **Bài toán học:** POMDP. Mỗi UAV quan sát vị trí, năng lượng của mình và AoI của các IoT ở gần (PT (7)).
- **Hành động:** chọn 1 trong 8 hướng bay (PT (9)).
- **Phần thưởng:** r_t = α·r_a + β·r_p + γ·r_s, trong đó r_p phạt khi năng lượng quá thấp hoặc đã đầy (PT (10)–(11)).
- **MAPPO-TM** = MAPPO (CTDE) cộng thêm hai thành phần:
  - LSTM trong actor để nhớ lịch sử quỹ đạo và năng lượng (PT (15)–(16));
  - hàm giá trị V_i = w_l·V_local + w_g·V_global với trọng số học được, tác giả gọi là "dual-attention" (PT (17), Fig. 2).
- **Quyết định sạc:** trong PT (5), biến sạc C là biến riêng, nhưng không gian hành động (9) chỉ có hướng bay. Sạc xảy ra khi UAV ở trong vùng R_c (§III-A), nên "chiến lược sạc" thực chất là quyết định bay vào vùng sạc (suy luận).

**Bằng chứng mạnh nhất (mục/bảng/hình):**
- **Fig. 4a (peak AoI cuối, đọc từ hình):** khoảng 575 (MAPPO-TM), 605 (MAPPO), 655 (MATD3) và 680 (MADDPG).
  - Con số "giảm tới 15,1%" trong tóm tắt khớp với phép so với MADDPG: (680 − 577)/680 ≈ 15%.
  - So với MAPPO chuẩn, mức giảm chỉ khoảng 5%.
  - Cả hai phép tính đều dùng số đọc từ hình nên chỉ là xấp xỉ.
- **Fig. 3a–c:** đường huấn luyện 3000 episode, có vùng tô "variance" (§V-B1).
- **Fig. 4b:** quét η_le ∈ {0,1; 0,15; 0,2; 0,25; 0,3}.
  - Tác giả viết MAPPO-TM có peak AoI thấp hơn 5–10% ở mọi η_le (§V-B2).
  - Trên hình, tại η_le = 0,25 hai đường MAPPO-TM và MAPPO gần như trùng nhau (khoảng 655 và 660).

**Đánh giá trên kịch bản khác tập huấn luyện? Loại dịch chuyển nào?** Không.
- Vị trí IoT và vị trí đầu của UAV đều cố định (§V-A).
- Quét η_le (Fig. 4b) chỉ là thay một tham số vật lý, và bài không nói có huấn luyện lại cho mỗi giá trị hay không.
- §VI-A gọi thuật toán là "robust" với η_le, nhưng chỉ dựa trên Fig. 4b.
- **Đáng chú ý:** tác giả nêu domain randomization là **hướng tương lai** để cải thiện tổng quát hoá (§VII, đoạn cuối), tức bài này chưa làm.

**Số seed / cách báo cáo độ bất định:**
- Bài không báo số seed huấn luyện.
- Vùng tô trên Fig. 3 được gọi là "variance" nhưng không nói tính trên bao nhiêu lần chạy (§V-B1).
- Fig. 4a và 4b không có thanh lỗi, và không có kiểm định thống kê.

**Đối chứng gần nhất và độ công bằng của so sánh:**
- Đối chứng chỉ gồm các thuật toán MADRL: MAPPO, MATD3 và MADDPG (§V-A).
- Không có heuristic (TSP, greedy), dù chính bài quy bài toán về TSP để chứng minh NP-hard (§III-F).
- Không có thông tin tinh chỉnh tham số cho các đối chứng.
- MATD3 và MADDPG là thuật toán cho hành động liên tục, nhưng không gian hành động ở đây là 8 hướng rời rạc. Bài không nói cách ánh xạ giữa hai loại này.

**Giới hạn đã biết:**
1. **Không nhất quán về số LBD:** Bảng IV ghi N_D = 10, nhưng §V-A và Fig. 4c chỉ có một vùng sạc ở tâm.
2. **Ký hiệu γ trùng nghĩa:** γ vừa là hệ số chiết khấu (PT (13)) vừa là trọng số thưởng (PT (11)).
3. **§VI-B "Robustness"** mô tả cơ chế xử lý lỗi (IoT hỏng, UAV hỏng) nhưng không có thực nghiệm nào đi kèm.
4. **Không công bố mã.**

**Khác biệt với đề tài (điền thẳng vào ma trận docs/04 §5):**
- **Sun 2025:** đa UAV, sạc laser, mục tiêu peak AoI, tốc độ cố định, một bố trí cố định, không báo seed.
- **Đề tài:** một UAV, năng lượng đẩy phụ thuộc tốc độ với lựa chọn tốc độ trong hành động, DR trên bố trí, 4 bộ OOD, 10 seed + CI.
- **Cách trích:** có thể dẫn §VII của Sun làm bằng chứng rằng tổng quát hoá bằng DR cho bài AoI–UAV vẫn được chính các tác giả gần đây xem là việc còn để ngỏ. Không viết "đầu tiên" (quy tắc 7, CLAUDE.md).

Hàng ma trận đề xuất:

| Công trình | Mục tiêu AoI | Năng lượng phụ thuộc tốc độ | Huấn luyện trên nhiều bố trí | Đánh giá OOD có cấu trúc | Nhiều seed + CI |
| --- | --- | --- | --- | --- | --- |
| Sun 2025 | Có (peak AoI, đa UAV) | Có mô hình P(v) nhưng v cố định 5 m/s, nên không là biến quyết định | Không (IoT cố định) | Không (chỉ quét η_le) | Không (không báo seed; vùng "variance" không rõ n) |

**Có mã nguồn/dữ liệu không:** Không thấy liên kết mã hay dữ liệu trong bài.

**Một câu hỏi cho nhóm:** `env.py` đã tính `peak_aoi`. Có nên báo peak AoI như một chỉ số phụ (không đưa vào giả thuyết PREREG) để so được với nhóm bài dùng peak AoI như Sun 2025 không?
