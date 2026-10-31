# Form B — `yi2020deep`

> Trạng thái: **nháp chờ LDN duyệt**, Claude soạn ngày 31/10/2026 từ toàn văn bản HTML ar5iv của arXiv:2003.00391v1 (6 trang). Người đọc: LDN. Second reader: DAT (W1-LDN-02). Phương trình đọc từ bản HTML; những chỗ ghi "cần đối chiếu PDF" có thể do lỗi chuyển đổi.

**Tiêu đề / tác giả / năm / nơi công bố hoặc trạng thái preprint:** *Deep Reinforcement Learning for Fresh Data Collection in UAV-assisted IoT Networks*, 2020.
- **Tác giả:** Mengjie Yi, Xijun Wang, Juan Liu, Yan Zhang, Bo Bai (ĐH Tây An Điện tử, ĐH Trung Sơn, ĐH Ninh Ba, Huawei).
- **Nơi công bố:** trang arXiv ghi "Accepted by IEEE INFOCOM 2020-AoI workshop". DOI và số trang trong kỷ yếu chưa kiểm ✱.

**URL nguồn gốc và phiên bản/ngày truy cập:** https://arxiv.org/abs/2003.00391 (v1, 01/03/2020); toàn văn đọc tại https://ar5iv.labs.arxiv.org/html/2003.00391, truy cập 31/10/2026.

**Người đọc (NICK):** LDN

**Bài báo trả lời câu hỏi gì:** Một UAV cánh quay phải bay từ điểm xuất phát tới điểm đích trong T khe, vừa thu gói cập nhật trạng thái từ các cảm biến, vừa giữ năng lượng còn lại không âm. Bài tìm quỹ đạo và lịch truyền của cảm biến để tối thiểu tổng AoI có trọng số trung bình theo thời gian (§I, bài toán P1, PT (6)–(9)).

**Giả định hệ thống:**
- **Quy mô:** một UAV, N cảm biến vị trí ngẫu nhiên; lưới 20 × 20 ô cạnh 25 m (vùng 500 m × 500 m); độ cao 120 m; T = 70 khe (§II-A, §IV, Bảng I). Độ dài khe τ không có trong Bảng I.
- **Chuyển động:** mỗi khe UAV treo hoặc bay sang một ô kề với **tốc độ hằng số V = 25 m/s** (§II-A, Bảng I). Không gian hành động: {Bắc, Nam, Đông, Tây, Treo} × {cảm biến được lập lịch} (§III-A2).
- **Năng lượng đẩy:** dạng P(V) của Zeng 2019, gồm thành phần cánh quạt, cảm ứng và ký sinh (PT (1)). Chỉ dùng trong **ràng buộc** năng lượng (PT (7)), không nằm trong mục tiêu. Vì V cố định nên năng lượng chỉ khác nhau giữa bay và treo (PT (13)).
- **Kênh:** LoS thuần, suy hao theo bình phương khoảng cách (PT (2)). Cảm biến truyền thành công trong một khe khi UAV ở trong bán kính phủ R (PT (3)); mỗi khe chỉ một cảm biến truyền.
- **AoI:** về 1 khi được thu, ngược lại tăng 1 (PT (4)–(5)). Mục tiêu là AoI có trọng số θ_n trung bình theo thời gian (PT (6)); mô phỏng dùng trọng số bằng nhau (§IV).

**Cơ chế, diễn đạt bằng lời của mình:**
- MDP hữu hạn bước. Trạng thái gồm ô hiện tại của UAV, AoI của mọi cảm biến, "thời gian dư" so với thời gian tối thiểu về đích, và "năng lượng dư" so với năng lượng tối thiểu cần để về đích (§III-A1).
- Phần thưởng là −J, cộng thưởng lớn khi về đúng đích với năng lượng không âm và phạt lớn khi vi phạm thời gian hoặc năng lượng (PT (10)).
- Thuật toán là DQN chuẩn có mạng đích và replay (§III-B, Algorithm 1); hai lớp ẩn 200 và 256 nơ-ron, 20 000 episode (Bảng II).
- **Trạng thái không chứa vị trí cảm biến** (§III-A1). Vì vậy chính sách chỉ có nghĩa với bố trí đã dùng khi huấn luyện; muốn đổi bố trí thì phải huấn luyện lại. Đây là suy luận từ định nghĩa trạng thái, bài không nói thẳng.

**Bằng chứng mạnh nhất (mục/bảng/hình):**
- **Fig. 2:** AoI trung bình theo bán kính phủ R với N = 3 cảm biến đặt ngẫu nhiên. DQN thấp hơn hai đối chứng; khi R lớn, đối chứng theo AoI gần bằng DQN (§IV).
- **Fig. 3:** AoI trung bình theo N với R = 4 (đơn vị ô). Khoảng cách giữa DQN và đối chứng lớn dần khi N tăng (§IV).
- Hai hình chỉ có một đường cho mỗi phương pháp, không có thanh lỗi. Bài không in bảng số.

**Đánh giá trên kịch bản khác tập huấn luyện? Loại dịch chuyển nào?** Không.
- Fig. 2 nói rõ "một kịch bản" với 3 cảm biến đặt ngẫu nhiên (§IV).
- Quét R và N (Fig. 2–3) là thay cấu hình rồi đánh giá. Với N khác nhau thì kích thước trạng thái và hành động khác nhau, nên chắc chắn phải huấn luyện lại; bài không nói rõ (suy luận).

**Số seed / cách báo cáo độ bất định:** Không báo số seed huấn luyện, số episode đánh giá hay số bố trí ngẫu nhiên được lấy trung bình. Không có thanh lỗi hay kiểm định (Fig. 2–3).

**Đối chứng gần nhất và độ công bằng của so sánh:**
- Hai heuristic (§IV): (a) bay tới cảm biến có AoI lớn nhất; (b) đi lần lượt cảm biến gần nhất chưa thăm theo từng vòng. Cả hai thu dữ liệu trên đường bay và quay về đích khi năng lượng hoặc thời gian dưới ngưỡng.
- Không có đối chứng TSP tối ưu hay lời giải tối ưu cho N nhỏ, dù với N = 3 có thể quy hoạch động được.
- Không có thông tin tinh chỉnh ngưỡng của heuristic.

**Giới hạn đã biết:**
1. **Tham số năng lượng trong Bảng I khác xa Zeng 2019 Bảng I:** v₀ = 0,002 m/s (Zeng: 4,03 m/s), độ đặc rotor s = 0,0001 (Zeng: 0,05), d₀ = 0,48 (Zeng: 0,6), đơn vị diện tích đĩa rotor ghi "s²". Có thể là lỗi in; không nên chép các giá trị này.
2. **Thành phần cảm ứng ở PT (1)** trên bản HTML là P₁(1 + V⁴/(4v₀⁴) − V²/(2v₀²))^{1/2}, thiếu một lớp căn so với PT (6) của Zeng. Cần đối chiếu PDF.
3. **Định nghĩa năng lượng dư Δ_t** (§III-A1) có tổng chạy tới N − t; nhiều khả năng là T − t (lỗi in).
4. Phần thưởng mỗi bước dùng J là AoI trung bình **trên cả chân trời T** (PT (10)), nên không rõ phần thưởng tức thời được tính thế nào trước khi kết thúc episode.
5. Độ dài khe τ không được nêu, nên không kiểm được ràng buộc năng lượng (7) với E_max = 2,2·10⁴ J.
6. Không công bố mã.

**Khác biệt với đề tài (điền thẳng vào ma trận docs/04 §5):**
- **Yi 2020:** một UAV, AoI có trọng số, có mô hình P(V) nhưng chỉ làm ràng buộc và tốc độ cố định (chỉ chọn bay/treo), một bố trí, không OOD, không báo seed.
- **Đề tài:** năng lượng đẩy nằm trong mục tiêu (λ) và tốc độ là biến quyết định; huấn luyện trên nhiều bố trí (DR); 4 bộ OOD có cấu trúc; 10 seed + CI.
- Yi 2020 là tiền thân trực tiếp về **bài toán** (UAV + AoI + năng lượng đẩy + DRL), nên nên trích ở phần mô hình hệ thống và Related Work. Bài không lấp được cột nào trong 3 cột cuối.

Hàng ma trận đề xuất (thay hàng "Yi 2020" hiện có 3 ô "Chưa rõ"):

| Công trình | Mục tiêu AoI | Năng lượng phụ thuộc tốc độ | Huấn luyện trên nhiều bố trí | Đánh giá OOD có cấu trúc | Nhiều seed + CI |
| --- | --- | --- | --- | --- | --- |
| Yi 2020 | Có (AoI có trọng số trung bình theo thời gian; PT (6)) | Không (P(V) dạng Zeng ở PT (1) chỉ trong ràng buộc (7); bay với V = 25 m/s cố định hoặc treo; §II-A, Bảng I) | Không (trạng thái không chứa vị trí cảm biến; §III-A1; Fig. 2 là một kịch bản) | Không (chỉ quét R và N; Fig. 2–3) | Không (không báo seed, không thanh lỗi; Fig. 2–3) |

**Có mã nguồn/dữ liệu không:** Không thấy liên kết mã hay dữ liệu trong bài.

**Một câu hỏi cho nhóm:** Yi 2020 và Abd-Elmagid 2019 đều để vị trí cảm biến ngoài trạng thái, nên chính sách gắn với một bố trí. Có nên nêu điều này trong Related Work như lý do cấu trúc khiến các bài AoI–DRL sớm không tổng quát hoá được, và lấy đó làm động cơ cho quan sát chứa bố trí của đề tài không?
