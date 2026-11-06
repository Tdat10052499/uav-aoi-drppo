# Form B — `gong2024uav` (A1)

> Trạng thái: **NHÁP Claude soạn cho DAT 06/11/2026, chờ DAT đọc lại, rồi second reader.** Soạn từ toàn văn HTML ar5iv của arXiv 2312.00334 v1. Mục, phương trình và số liệu dưới đây đã đối chiếu với văn bản đó. Chưa đối chiếu với bản IEEE đã xuất bản.

**Tiêu đề / tác giả / năm / nơi công bố hoặc trạng thái preprint:** *UAV-Aided Lifelong Learning for AoI and Energy Optimization in Non-Stationary IoT Networks*. Zhenzhen Gong, Omar Hashash, Yingze Wang, Qimei Cui, Wei Ni, Walid Saad, Kei Sakaguchi.
- arXiv 01/12/2023 (15 trang, 14 hình).
- IEEE IoT-J 2024 ✱ (theo `search_log_LDN.md` A1; chưa kiểm trên trang nhà xuất bản).

**URL nguồn gốc và phiên bản/ngày truy cập:** https://ar5iv.labs.arxiv.org/html/2312.00334, truy cập 06/11/2026.

**Người đọc (NICK):** DAT (nháp Claude)

**Bài báo trả lời câu hỏi gì:** Thiết bị IoT sống trong môi trường không dừng cần cân bằng AoI và năng lượng CPU. Làm sao để UAV bay tới từng thiết bị và cập nhật chính sách CPU cho chúng, giúp chúng thích nghi nhanh, mà vẫn tiết kiệm năng lượng bay?

**Giả định hệ thống:**
- **Quy mô:** 1 UAV cánh quay, N thiết bị; mô phỏng N = 6 trong vùng 1 km × 1 km (§II-C, §V-A). Một ví dụ dùng 5 thiết bị (§V-B, Fig. 9); Fig. 14 quét N từ 5 đến 30.
- **Vị trí thiết bị:** ngẫu nhiên phân bố đều (§II-A); §V-A cũng nói thiết bị và môi trường của chúng được chọn ngẫu nhiên.
- **Vai trò UAV:** UAV bay tới thiết bị để lấy thông tin môi trường và cập nhật chiến lược (§II-C). AoI nảy sinh ở thiết bị, theo hàng đợi xử lý CPU (PT (2)). **UAV không phải kênh thu gói dữ liệu làm AoI giảm như trong đề tài.**
- **Kênh:** bỏ qua thời gian và năng lượng truyền lên, xuống (§II-C); không có mô hình kênh. Độ cao không ghi.
- **Năng lượng UAV:** công suất đẩy phụ thuộc tốc độ, gồm ba thành phần blade profile, induced, parasite (PT (4)); năng lượng mỗi chuyến theo quãng đường và tốc độ (PT (5)). Hover và cập nhật chiến lược coi là hằng số, bị bỏ khỏi tối ưu (§II-C).
- **Mục tiêu:** tối thiểu chi phí thiết bị + μ·năng lượng UAV (PT (6)), với chi phí mỗi thiết bị = β·AoI + (1−β)·năng lượng CPU (PT (3)). Tốc độ bị chặn 10–40 m/s (PT (9), §V-A). Nhiều lượt thăm trong một đoạn dài: episode 3000 khe (§V-A).

**Cơ chế, diễn đạt bằng lời của mình:**
- **Phía thiết bị:** RL suốt đời với cơ sở tri thức và cơ sở đặc trưng dùng chung (§III-B). Gặp môi trường mới thì dùng phương pháp zero-shot để suy ra chính sách khởi tạo tốt, rồi học tiếp (§III-C; chữ "warm-start" ở §V-A2 và §VI).
- **Phía UAV:** mạng actor-critic chọn thiết bị kế tiếp và tốc độ (§IV). Trạng thái gồm vị trí UAV và thời gian trôi qua từ khi môi trường hiện tại đến ở từng thiết bị (§IV). **Trạng thái không chứa toạ độ thiết bị.**
- **"Môi trường" trong bài** là bộ tham số hàng đợi và CPU: xác suất gói đến, kích thước gói, thời lượng môi trường, κ, ε_max (§II-B, §V-A). **Không phải bố trí không gian.**

**Bằng chứng mạnh nhất (mục/bảng/hình):**
- Fig. 7, §V-B: hội tụ nhanh hơn so với PG thường, 50% ở trường hợp tốt nhất, 25% ở xấu nhất; phần thưởng ban đầu tốt hơn khoảng 10% (số do bài nêu trong văn bản).
- Fig. 10, §V-B: so với PG thường, AoI giảm 21,42%, hàng đợi giảm 47,04%, đổi lại năng lượng CPU cao hơn.
- Fig. 11, §V-B: năng lượng UAV 2292 kJ, tiết kiệm 48,5% so với baseline random và force.
- Fig. 12–13, §V-B: quét tốc độ 10–40 m/s. Năng lượng giảm rồi tăng theo tốc độ, đúng dạng PT (4). AoI giảm 26,30% khi tốc độ tăng.
- Fig. 14, §V-B: quét N từ 5 đến 30, AoI trung bình tăng từ 4,81 lên 9,81.

**Đánh giá trên kịch bản khác tập huấn luyện? Loại dịch chuyển nào?**
- Có, nhưng dịch chuyển nằm ở **tham số hàng đợi và CPU của thiết bị** (§III-C, Fig. 7–8), kèm quét N (Fig. 14).
- Không thấy dịch chuyển phân bố không gian (phân cụm), diện tích, hay ngân sách năng lượng.
- Zero-shot ở đây chỉ cho **chính sách khởi tạo**; các hình Fig. 7–8 đo đường học sau đó, nên không phải triển khai không huấn luyện lại.
- Bài không nói Fig. 14 có huấn luyện lại actor-critic của UAV cho từng N hay không.

**Số seed / cách báo cáo độ bất định:** Từ "seed" không xuất hiện trong toàn văn. Không thấy khoảng tin cậy hay dải sai số theo seed.

**Đối chứng gần nhất và độ công bằng của so sánh:** PG thường cho từng môi trường, UAV bay ngẫu nhiên 20 m/s, phương pháp force 20 m/s, và bộ điều khiển dựa trên giá trị (§V-A2). **Không có đối chứng cùng learner huấn luyện trên một bố trí cố định.**

**Giới hạn đã biết:**
- Bài không có mục nêu hạn chế; §VI chỉ tóm tắt kết quả.
- Ghi chú của người đọc: §V-A ghi 6 thiết bị, ví dụ Fig. 9 ghi 5.
- Ghi chú của người đọc: phần thưởng là trị tuyệt đối của chi phí từ §V-B nên "thấp hơn" là tốt hơn; dễ đọc nhầm.

**Khác biệt với đề tài (điền thẳng vào ma trận docs/04 §5):**
- Mục tiêu AoI: **Có** (PT (2), (3), (6)); AoI theo hàng đợi CPU ở thiết bị, UAV chỉ cập nhật chính sách (§II-C).
- Năng lượng phụ thuộc tốc độ: **Có** (PT (4)–(5); tốc độ là biến quyết định, PT (9), §IV).
- Huấn luyện trên nhiều bố trí: **Không rõ** (vị trí ngẫu nhiên đều §II-A, §V-A; "môi trường" là tham số hàng đợi §II-B; bài không nói đổi vị trí giữa các lần huấn luyện; trạng thái UAV không chứa toạ độ thiết bị §IV).
- Đánh giá OOD có cấu trúc: **Một phần** (môi trường mới theo tham số hàng đợi, có khởi tạo zero-shot rồi học tiếp, §III-C, Fig. 7–8; quét N, Fig. 14; không có dịch chuyển không gian, diện tích, năng lượng).
- Nhiều seed + CI: **Không** (không báo seed).
- Đối chứng bố trí cố định: **Không** (§V-A2).

**Kết luận cho G0 #2 (đánh giá của người soạn, chờ DAT và nhóm xác nhận):** Bài này không đủ 6 cột. Đây vẫn là bài gần nhất về **mô hình** cùng Yi 2023: có cả AoI lẫn năng lượng phụ thuộc tốc độ với tốc độ là hành động. Không dùng các điểm đó làm điểm mới.

**Có mã nguồn/dữ liệu không:** Không thấy liên kết mã nguồn trong văn bản đã đọc.

**Câu hỏi đặt cho nhóm:** Ô "Không rõ" ở cột nhiều bố trí có cần kiểm thêm bằng bản IEEE không? Bản arXiv là v1 duy nhất; bản xuất bản có thể khác.

**Đối chiếu với PDF (06/11/2026).** DAT tải lên bản PDF arXiv 2312.00334v1 (dấu "arXiv:2312.00334v1 [cs.NI] 1 Dec 2023", 15 trang). Đây cùng phiên bản với bản HTML đã dùng, chưa phải bản IEEE. Claude đối chiếu lại các chỗ còn nghi vấn:
- **"Môi trường" (§II-B, Definition 1, tr. 4):** z_{i,t} = (λ_{i,t}, ā_{i,t}, σ²_{i,t}, κ_i, ε_{i,max}), tức tham số đến gói, kích thước gói và CPU. Không có vị trí. Khớp với nhận định ở trên.
- **Trạng thái UAV (§IV, tr. 10):** X^u ∈ ℝ^{N+2} = {l_m, ϖ_0, ϖ_1, …, ϖ_N}, gồm vị trí UAV và thời gian từ khi môi trường hiện tại đến ở từng thiết bị. Không có toạ độ thiết bị. Ký hiệu tự mâu thuẫn nhẹ: l_m có 2 chiều, cộng N+1 giá trị ϖ thì ra N+3 chiều, không phải N+2.
- **Hành động UAV (§IV, tr. 10; §V-A1, tr. 11):** Y^u = {v_m, l_{m+1}}. Đầu ra Softmax chọn thiết bị kế tiếp, tốc độ bị kẹp trong [v_min, v_max] = [10, 40] m/s. Fig. 12–13 lại vẽ kết quả *theo* tốc độ 10–40 m/s như một tham số quét. Bài không nói rõ khi đó tốc độ do AC chọn hay bị cố định, nên kết luận "tốc độ là biến quyết định" đúng ở mức bài toán (PT (9)), còn ở mức thực nghiệm thì chưa rõ.
- **Bố trí (§V-A, tr. 11):** "N = 6 IoT devices distributed within a square region with a side length of 1km". Ở pha kiểm thử: "the devices and their associated environment are considered to be randomly chosen", câu này có thể hiểu là chọn ngẫu nhiên thiết bị và môi trường được thăm, không nhất thiết là sinh lại vị trí. Không có câu nào nói sinh lại vị trí giữa các episode. Giữ **Không rõ**.
- **Đối chứng (§V-A2, tr. 11–12):** regular PG; Random và Force đều bay cố định 20 m/s; Q-learning hai lớp. Khớp.
- **Seed và CI:** không có trong §V. Khớp.
- **Câu tự nhận của tác giả (§I-B, tr. 2):** "To the best of our knowledge, this is the first work that considers the joint optimization of both IoT devices and UAV in non-stationary environments." Chỉ ghi lại để biết, không dùng làm bằng chứng.

Kết luận: các ô ở ma trận docs/04 không cần sửa. DAT vẫn cần tự xác nhận các điểm trên.
