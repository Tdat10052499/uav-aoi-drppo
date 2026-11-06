# Form B — `lu2025attention` (A3)

> Trạng thái: **NHÁP Claude soạn cho DAT 06/11/2026, chờ DAT đọc lại, rồi second reader.** Soạn từ toàn văn HTML ar5iv của arXiv 2505.22170 v1. Mục, phương trình và số liệu dưới đây đã đối chiếu với văn bản đó. Chưa đối chiếu với bản IEEE đã xuất bản.

**Tiêu đề / tác giả / năm / nơi công bố hoặc trạng thái preprint:** *Attention-Enhanced Prompt Decision Transformers for UAV-Assisted Communications with AoI*. Chi Lu, Yiyang Ni, Zhe Wang, Xiaoli Shi, Jun Li, Shi Jin.
- arXiv 28/05/2025.
- IEEE WCL 2025 ✱ (theo `search_log_LDN.md` A3, tên ghi "UAV/AAV"; chưa kiểm trên trang nhà xuất bản).

**URL nguồn gốc và phiên bản/ngày truy cập:** https://ar5iv.labs.arxiv.org/html/2505.22170, truy cập 06/11/2026.

**Người đọc (NICK):** DAT (nháp Claude)

**Bài báo trả lời câu hỏi gì:** Khi số người dùng trong vùng phục vụ thay đổi, làm sao để chính sách UAV giảm AoI dưới ràng buộc năng lượng dài hạn mà không phải huấn luyện lại từ đầu?

**Giả định hệ thống:**
- **Quy mô:** 1 UAV, độ cao H = 60 m, vùng 500 m × 500 m, T = 100 khe, mỗi khe 5 s (§V).
- **Người dùng:** di động mặt đất, số lượng đổi theo thời gian; vị trí khởi tạo ngẫu nhiên rồi theo mô hình Gauss–Markov (§II, §V). Đây là người dùng di động, không phải cảm biến cố định.
- **Năng lượng UAV:** hai mức công suất hằng số P_f = 110 W khi bay và P_h = 80 W khi treo (§II-A, §V). **Không có mô hình công suất theo tốc độ.**
- **Ràng buộc:** tổng năng lượng dưới E_max = 90 kJ (PT (4f), §V).
- **Hành động:** quãng đường bay, góc bay, người dùng được chọn (§III); quãng đường bị chặn d_max = 90 m mỗi khe (PT (4d), §V).
- **Mục tiêu:** tối thiểu AoI trung bình theo thời gian (PT (2), (4a)). Thưởng là âm AoI, chi phí là năng lượng (§III).

**Cơ chế, diễn đạt bằng lời của mình:**
- **Học ngoại tuyến:** Decision Transformer có attention; dữ liệu là quỹ đạo của TD3-Lag đã hội tụ, 100 000 bước mỗi bộ, từ các kịch bản 11, 13, 15 người dùng cố định (§V).
- **Thích nghi:** ghép một đoạn minh hoạ ngắn (prompt K bước, K = 5, lấy từ bộ đệm trực tuyến 500) vào đầu chuỗi để mô hình nhận ra kịch bản mới mà không phải huấn luyện lại tham số θ (§IV, §V).
- **Ràng buộc năng lượng:** dùng token return và cost-to-go (§IV).

**Bằng chứng mạnh nhất (mục/bảng/hình):**
- Fig. 3, §V (mật độ ρ = 20): so với DRL thường, hội tụ nhanh hơn 4,5 lần và AoI trung bình giảm hơn 15%; so với DT, AoI thấp hơn khoảng 8% và hội tụ nhanh gấp 2.
- Fig. 4, §V (ρ từ 15 đến 25): khoảng cách với DRL thường và DT rộng dần khi số người dùng tăng.
- Bài chỉ nêu số tương đối trong văn bản; không có bảng giá trị AoI tuyệt đối.

**Đánh giá trên kịch bản khác tập huấn luyện? Loại dịch chuyển nào?**
- Có, nhưng chỉ theo **số người dùng và mật độ** (Fig. 3–4).
- APDT không cập nhật θ khi triển khai, nhưng có dùng prompt trực tuyến (§IV, Algorithm 1). DT đối chứng thì tinh chỉnh trực tuyến (§V).
- Không thấy dịch chuyển phân bố không gian, diện tích, hay ngân sách năng lượng (E_max giữ cố định, §V).

**Số seed / cách báo cáo độ bất định:** Từ "seed" không xuất hiện trong toàn văn. Không thấy khoảng tin cậy.

**Đối chứng gần nhất và độ công bằng của so sánh:** DT, SAC-Lag, TD3-Lag, IPO (§V). Mọi thuật toán trừ APDT đệm trạng thái bằng số 0 để khớp số chiều (§V), nên một phần lợi thế của APDT đến từ cách xử lý này. **Không có đối chứng huấn luyện trên một bố trí cố định** theo nghĩa của đề tài; các bộ dữ liệu cố định về *số* người dùng.

**Giới hạn đã biết:** §VI chỉ nêu mở rộng đa UAV là hướng tiếp theo. Ghi chú của người đọc: dữ liệu "chuyên gia" lấy từ TD3-Lag, nên chất lượng APDT phụ thuộc agent đó.

**Khác biệt với đề tài (điền thẳng vào ma trận docs/04 §5):**
- Mục tiêu AoI: **Có** (PT (2), (4a)); dưới ràng buộc năng lượng (PT (4f)).
- Năng lượng phụ thuộc tốc độ: **Không** (P_f, P_h hằng số; §II-A, §V; tốc độ không nằm trong hành động, §III).
- Huấn luyện trên nhiều bố trí: **Một phần** (11, 13, 15 người dùng, vị trí ngẫu nhiên + Gauss–Markov; §V).
- Đánh giá OOD có cấu trúc: **Một phần** (chỉ số người dùng và mật độ ρ 15–25; không cập nhật θ, có prompt trực tuyến; Fig. 3–4).
- Nhiều seed + CI: **Không** (không báo seed).
- Đối chứng bố trí cố định: **Không** (§V).

**Kết luận cho G0 #2 (đánh giá của người soạn, chờ DAT và nhóm xác nhận):** Không đủ 6 cột. Bài cho thấy "không huấn luyện lại tham số khi gặp kịch bản mới" đã có người làm với AoI, nên đề tài không được nhận riêng điều này là mới; cần nói rõ dịch chuyển nào và thống kê thế nào.

**Có mã nguồn/dữ liệu không:** Không thấy liên kết mã nguồn trong văn bản đã đọc.
