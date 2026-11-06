# Form B — `toure2026optimizing` (A5)

> Trạng thái: **NHÁP Claude soạn cho DAT 06/11/2026, chờ DAT đọc lại, rồi second reader.** Soạn từ toàn văn HTML ar5iv của arXiv 2601.14092 v1. Mục, phương trình và số liệu dưới đây đã đối chiếu với văn bản đó. Chưa đối chiếu với bản IEEE đã xuất bản.

**Tiêu đề / tác giả / năm / nơi công bố hoặc trạng thái preprint:** *Optimizing Energy and Data Collection in UAV-aided IoT Networks using Attention-based Multi-Objective Reinforcement Learning*. Babacar Toure, Dimitrios Tsilimantos, Omid Esrafilian, Marios Kountouris.
- arXiv 20/01/2026.
- IEEE IoT-J 2026 ✱ (theo `search_log_LDN.md` A5; chưa kiểm trên trang nhà xuất bản).

**URL nguồn gốc và phiên bản/ngày truy cập:** https://ar5iv.labs.arxiv.org/html/2601.14092, truy cập 06/11/2026.

**Người đọc (NICK):** DAT (nháp Claude)

**Bài báo trả lời câu hỏi gì:** Làm sao có một chính sách UAV dùng được cho mọi mức đánh đổi giữa thu dữ liệu và năng lượng, và vẫn tổng quát hoá sang môi trường có số thiết bị và pin khác, không cần huấn luyện lại?

**Giả định hệ thống:**
- **Quy mô:** 1 UAV, độ cao cố định 60 m, K thiết bị tĩnh, bản đồ đô thị 800 m × 600 m có toà nhà (§II-A, §V-A).
- **Kênh:** LoS/NLoS có che khuất (§II-B, §V-A).
- **Năng lượng:** rời rạc, treo tốn 0,5 đơn vị/khe, di chuyển tốn 1 đơn vị/khe (PT (4)). **Không có mô hình công suất theo tốc độ.**
- **Hành động:** 5 hành động rời rạc: treo và 4 hướng, mỗi bước một ô (PT (2)). **Không chọn tốc độ.**
- **Mục tiêu:** hai mục tiêu, tổng dữ liệu thu được và âm tổng pin dùng (PT (9a)), trong một nhiệm vụ từ điểm đầu đến vùng kết thúc (PT (9b)). **Không có AoI**; AoI chỉ xuất hiện ở tổng quan (§I-A).

**Cơ chế, diễn đạt bằng lời của mình:** Soft Actor-Critic đa mục tiêu, nhận vector ưu tiên w làm đầu vào, dùng self-attention trên tập đặc trưng của UAV và thiết bị thay cho bản đồ không gian (§III-C, §IV). Nhờ đó một mạng dùng được cho nhiều số thiết bị và mức ưu tiên.

**Bằng chứng mạnh nhất (mục/bảng/hình):**
- §V-A: huấn luyện với K = 6, pin B = 80, vị trí thiết bị và dữ liệu ban đầu ngẫu nhiên mỗi episode, 1,5 triệu bước.
- §V-D, Fig. 6: K ∈ {3, 5, 6, 9, 10}, mỗi giá trị 100 lần hiện thực môi trường cố định. Với 10 thiết bị và pin 100: MOSAC-ATT thu khoảng 80% dữ liệu, MOSAC-CGL 72%.
- §V-D: khả năng thất bại của baseline tăng theo mức lệch giữa tập thử và tập huấn luyện.
- Bảng I, §V-C: chính sách ít bị ảnh hưởng khi thêm fading.

**Đánh giá trên kịch bản khác tập huấn luyện? Loại dịch chuyển nào?**
- Có, không huấn luyện lại, trên **số thiết bị và pin ban đầu** (§V-A, §V-D, Fig. 6). Pin chỉ đổi ở trường hợp 10 thiết bị (80 → 100).
- Không thấy dịch chuyển phân bố không gian (phân cụm) hay diện tích bản đồ.

**Số seed / cách báo cáo độ bất định:**
- 3 seed huấn luyện (§V-A; chú thích Fig. 4 "averaged across 3 seeds").
- Không thấy khoảng tin cậy hay kiểm định theo seed.
- Độ lệch chuẩn ở Bảng I và §V-D là theo hiện thực môi trường hoặc lần lặp, không phải theo seed.

**Đối chứng gần nhất và độ công bằng của so sánh:** GREEDY, DDQN-CGL, MOSAC-CGL, MOSAC-FTV (§V-B), đều huấn luyện trong cùng thiết lập ngẫu nhiên vị trí. **Không có đối chứng huấn luyện trên bố trí cố định.**

**Giới hạn đã biết:** Bài nêu hướng tiếp theo là đa UAV, quan sát một phần, nhiễu không dây (§VI). Năng lượng theo mô hình rời rạc đơn giản, bài tự nhận mức tiêu thụ thực phụ thuộc nhiều yếu tố (§II-A).

**Khác biệt với đề tài (điền thẳng vào ma trận docs/04 §5):**
- Mục tiêu AoI: **Không** (dữ liệu thu + pin, PT (9a); AoI chỉ ở §I-A).
- Năng lượng phụ thuộc tốc độ: **Không** (PT (4); hành động không có tốc độ, PT (2)).
- Huấn luyện trên nhiều bố trí: **Có** (vị trí và dữ liệu ngẫu nhiên mỗi episode, bản đồ và K, B cố định; §V-A).
- Đánh giá OOD có cấu trúc: **Một phần** (K và pin, không huấn luyện lại; không có dịch chuyển không gian hay diện tích; §V-D, Fig. 6).
- Nhiều seed + CI: **Một phần** (3 seed, không CI; §V-A, Fig. 4).
- Đối chứng bố trí cố định: **Không** (§V-B).

**Kết luận cho G0 #2 (đánh giá của người soạn, chờ DAT và nhóm xác nhận):** Không đủ 6 cột. Bài cùng dòng với Bayerlein 2021 về đánh giá không huấn luyện lại trên tham số kịch bản, và có báo 3 seed; đề tài vẫn khác ở AoI, năng lượng theo tốc độ, dịch chuyển không gian, đối chứng Fixed và CI.

**Có mã nguồn/dữ liệu không:** Không thấy liên kết mã nguồn trong văn bản đã đọc.
