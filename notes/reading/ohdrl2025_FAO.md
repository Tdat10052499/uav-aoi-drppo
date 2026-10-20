# Form B — `ohdrl2025`

> **Ghi chú này CHỈ dựa trên tóm tắt và siêu dữ liệu, KHÔNG có toàn văn.** Ngày 20/10/2026, FAO không truy cập được PDF: không có bản arXiv, trường không có quyền IEEE Xplore, và trang của tác giả không đăng PDF. Mọi ô ghi "Chưa rõ" chỉ được điền khi có toàn văn. Không đưa bất kỳ chi tiết nào của bài này vào bản thảo ngoài những gì có trong tóm tắt. Second reader: LDN.

**Tiêu đề / tác giả / năm / nơi công bố hoặc trạng thái preprint:** *OH-DRL: An AoI-Guaranteed Energy-Efficient Approach for UAV-Assisted IoT Data Collection*. Bowen Yang, Yao Yu, Xin Hao, Phee Lep Yeoh, Junxiong Zhang, Lei Guo, Yonghui Li, 2025.
- **Nơi công bố:** IEEE Transactions on Wireless Communications, 24(6):5009–5022. DOI 10.1109/TWC.2025.3545451.
- **Nguồn kiểm tra:** danh sách tác giả và thông tin xuất bản lấy từ trang lưu trữ của UniSC (bên dưới), chưa đối chiếu với IEEE Xplore ✱.
- **Lưu ý:** `paper/references.bib` đang ghi `note = {VERIFY author list}`, nên bổ sung danh sách tác giả ở trên.

**URL nguồn gốc và phiên bản/ngày truy cập:**
- Trang UniSC Research Bank, có tóm tắt nhưng không có PDF: https://research.usc.edu.au/esploro/outputs/journalArticle/OH-DRL-An-AoI-Guaranteed-Energy-Efficient-Approach-for/991127505202621. Truy cập ngày 20/10/2026.
- Trang của Yao Yu tại ĐH Đông Bắc (NEU), chỉ có trích dẫn: https://faculty.neu.edu.cn/yuyao/en/lwcg/45587/content/35257.htm.

**Người đọc (NICK):** FAO

**Bài báo trả lời câu hỏi gì (theo tóm tắt):** Bài tìm cách tối thiểu năng lượng bay của UAV khi thu dữ liệu IoT, với ràng buộc đảm bảo AoI trung bình tối đa. Hệ thống có thêm một STAR-RIS (bề mặt thông minh vừa truyền qua vừa phản xạ). Các biến tối ưu là quỹ đạo UAV, lịch truyền của thiết bị IoT và beamforming của STAR-RIS.

**Giả định hệ thống:**
- **Theo tóm tắt:** một UAV (tóm tắt dùng số ít), có STAR-RIS. AoI là **ràng buộc** (AoI trung bình tối đa), còn năng lượng bay là **mục tiêu**, tức ngược vai trò so với đề tài.
- **Chưa rõ:** mô hình năng lượng bay (có phụ thuộc tốc độ không), mô hình kênh, số thiết bị IoT.

**Cơ chế, diễn đạt bằng lời của mình (theo tóm tắt):** Bài toán được tách thành hai tầng:
- tầng cao học chính sách thăm của UAV (chọn nơi bay tới) bằng DRL;
- tầng thấp tối ưu lịch truyền IoT và beamforming bằng semidefinite relaxation (SDR).

Chưa rõ: thuật toán DRL cụ thể, không gian hành động, phần thưởng.

**Bằng chứng mạnh nhất (mục/bảng/hình):** Không xác định được mục, bảng hay hình vì không có toàn văn. Tóm tắt nêu hai kết quả:
- năng lượng bay thấp hơn 14,4%;
- số episode huấn luyện để hội tụ ít hơn 66%.

Cả hai đều so với "một thuật toán DRL hiện đại"; tóm tắt không nêu tên thuật toán đó.

**Đánh giá trên kịch bản khác tập huấn luyện? Loại dịch chuyển nào?** Chưa rõ. Tóm tắt không nhắc tới tổng quát hoá hay kịch bản chưa thấy.

**Số seed / cách báo cáo độ bất định:** Chưa rõ.

**Đối chứng gần nhất và độ công bằng của so sánh:** Theo tóm tắt, đối chứng là "một thuật toán DRL hiện đại" chưa nêu tên. Chưa đánh giá được độ công bằng.

**Giới hạn đã biết:** Chưa đánh giá được. Không có toàn văn.

**Khác biệt với đề tài (điền thẳng vào ma trận docs/04 §5):**
- **Khác biệt (theo tóm tắt):**
  - OH-DRL coi AoI là ràng buộc và năng lượng là mục tiêu; đề tài tối thiểu tổng có trọng số AoI + λ·năng lượng.
  - OH-DRL có STAR-RIS và tầng tối ưu SDR; đề tài thuần DRL, không có RIS.
- **Điểm giống:** cùng xét đồng thời AoI và năng lượng bay của UAV, nên đây là công trình gần nhất về **cặp mục tiêu** trong nhóm §2.
- **Chưa rõ:** OH-DRL có huấn luyện hay đánh giá trên nhiều bố trí không. Cần toàn văn trước khi dùng bài này để định vị đóng góp C2.

Hàng ma trận đề xuất:

| Công trình | Mục tiêu AoI | Năng lượng phụ thuộc tốc độ | Huấn luyện trên nhiều bố trí | Đánh giá OOD có cấu trúc | Nhiều seed + CI |
| --- | --- | --- | --- | --- | --- |
| OH-DRL 2025 (chỉ tóm tắt) | Có (ràng buộc AoI trung bình tối đa; mục tiêu là năng lượng bay) | Chưa rõ (có tối thiểu năng lượng bay; mô hình chưa kiểm) | Chưa rõ | Chưa rõ | Chưa rõ |

**Có mã nguồn/dữ liệu không:** Chưa rõ.

**Một câu hỏi cho nhóm:** DAT hoặc LDN có tải được bài này qua quyền IEEE Xplore của trường hay một nguồn khác không? Nếu không, có nên gửi email xin bản tác giả (FAO soạn và tự gửi), hay chấp nhận để `ohdrl2025` ở mức ◐ trong bài?
