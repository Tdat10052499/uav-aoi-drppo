# Form B — `xiao2024meta`

> Trạng thái: **nháp chờ LDN duyệt, cần đối chiếu PDF.** Claude soạn ngày 31/10/2026. PDF toàn văn (6 trang) mở công khai ở thư viện IFIP, nhưng Claude chỉ đọc được qua công cụ trích xuất tự động (WebFetch), không đọc trực tiếp từng trang. Mọi số mục/PT/hình dưới đây lấy từ bản trích đó; **LDN mở PDF và kiểm từng dòng có dấu (†)** trước khi duyệt. Người đọc: LDN (nhóm A6). Second reader: DAT.

**Tiêu đề / tác giả / năm / nơi công bố hoặc trạng thái preprint:** *Meta-learning Deep Reinforcement Learning for Fresh Data Collection in UAV-assisted Wireless Sensor Networks*, 2024.
- **Tác giả:** Xiong Xiao, Mengjie Yi, Xijun Wang, Juan Liu, Yan Zhang, Ronghui Hou (ĐH Tây An Điện tử, ĐH Trung Sơn, ĐH Ninh Ba). Cùng nhóm với Yi 2020 và Yi 2023.
- **Nơi công bố:** 22nd International Symposium on Modeling and Optimization in Mobile, Ad Hoc, and Wireless Networks (WiOpt 2024), tr. 316–321, © IFIP ✱ (tên hội nghị lấy từ Google Scholar và đường dẫn thư viện IFIP; PDF không in tên hội nghị).

**URL nguồn gốc và phiên bản/ngày truy cập:** https://opendl.ifip-tc6.org/db/conf/wiopt2024/wiopt2024/1571072060.pdf, truy cập 31/10/2026 (tìm thấy qua Google Scholar).

**Người đọc (NICK):** LDN

**Bài báo trả lời câu hỏi gì:** Khi một số cảm biến bị dịch chuyển do thảm hoạ (sạt lở, động đất), UAV cần điều chỉnh quỹ đạo nhanh để tiếp tục thu dữ liệu tươi. Bài tối ưu quỹ đạo UAV để tối thiểu tổng có trọng số của AoI trung bình và AoI cực đại, và dùng meta-learning để thích nghi nhanh khi vị trí cảm biến đổi (tóm tắt; bài toán P1, PT (9)†).

**Giả định hệ thống:**
- **Quy mô:** một UAV, vùng 1000 m × 1000 m, N = 120 cảm biến (Fig. 2) hoặc 40–200 (Fig. 3); độ cao 62 m; thời lượng T = 1800 s (§IV, Bảng I†).
- **Gom cụm:** vùng chia thành các ô vuông; UAV treo trên tâm ô có cảm biến để thu theo TDMA (§II-A†). Bản trích ghi công thức cạnh ô (khoảng 102 m với r = 36 m) mâu thuẫn với mô tả lưới 20 × 20 ô 50 m ở §IV†.
- **Chuyển động:** 4 hướng; **tốc độ cố định v = 20 m/s** (Bảng I†).
- **Năng lượng:** **không có mô hình năng lượng UAV** trong mục tiêu hay ràng buộc; năng lượng chỉ được nhắc ở phần mở đầu (†).
- **Kênh:** xác suất LoS theo góc ngẩng (PT (1)†), suy hao LoS/NLoS (PT (2)†).

**Cơ chế, diễn đạt bằng lời của mình:**
- MDP với bước thời gian không đều (thời gian bay qua một ô + thời gian phục vụ cụm) (PT (16)†).
- Trạng thái: AoI của mọi cảm biến, hiệu toạ độ từ UAV tới các tâm ô, thời gian còn lại (§III-A1†). Vị trí từng cảm biến không có trực tiếp trong trạng thái; bố trí chỉ được phản ánh gián tiếp qua tập tâm ô có cảm biến.
- Thuật toán: chính sách dạng PPO/TRPO với GAE, bọc trong MAML (vòng trong PT (19)†, vòng ngoài PT (21)†, Algorithm 1). 20 nhiệm vụ mỗi vòng meta (Bảng I†). Cài đặt dùng stable-baselines3 (†).
- Nhiệm vụ: môi trường trước thảm hoạ là nhiệm vụ ban đầu; thảm hoạ dời một số cảm biến tạo nhiệm vụ mới. Cách sinh các nhiệm vụ huấn luyện không được nêu (†).

**Bằng chứng mạnh nhất (mục/bảng/hình):**
- **Fig. 2†:** phần thưởng tích luỹ trên nhiệm vụ mới (N = 120) theo episode; MLDRL hội tụ nhanh nhất và cao nhất so với DQN, A2C, PPO có học chuyển giao. Văn bản không nêu số cụ thể.
- **Fig. 3†:** AoI trung bình và AoI cực đại theo N (40–200) sau 10 000 episode huấn luyện thêm trên nhiệm vụ mới; MLDRL thấp nhất, các phương pháp học đều tốt hơn heuristic theo AoI.

**Đánh giá trên kịch bản khác tập huấn luyện? Loại dịch chuyển nào?** Có, nhưng có huấn luyện tiếp.
- Dịch chuyển: **vị trí cảm biến đổi** sau thảm hoạ. Không có dịch chuyển có cấu trúc khác (mật độ, vùng, năng lượng).
- Cách đo: tốc độ thích nghi khi tiếp tục huấn luyện trên nhiệm vụ mới (Fig. 2) và kết quả sau 10 000 episode huấn luyện thêm (Fig. 3). Không đánh giá zero-shot (†).

**Số seed / cách báo cáo độ bất định:** Không báo số seed hay số lần chạy. Fig. 2 có vùng tô "phương sai" nhưng không rõ trên bao nhiêu lần chạy; Fig. 3 không có thanh lỗi (†).

**Đối chứng gần nhất và độ công bằng của so sánh:** DQN (thực ra trích Rainbow), A2C và PPO có học chuyển giao, cùng heuristic bay tới ô có AoI lớn nhất (§IV†). Không có đối chứng huấn luyện trên bố trí cố định rồi đánh giá trên bố trí mới mà không huấn luyện tiếp.

**Giới hạn đã biết:**
1. Mâu thuẫn kích thước ô giữa §II-A và §IV (†).
2. Bảng I ghi α₁ = 0,99, α₂ = 0,95 như tốc độ học, giá trị bất thường; có thể nhầm nhãn (†).
3. Phần thưởng mỗi bước (PT (14)†) không phải dạng phân rã của mục tiêu (9).
4. Không công bố mã.

**Khác biệt với đề tài (điền thẳng vào ma trận docs/04 §5):**
- **Xiao 2024:** AoI (trung bình + cực đại), tốc độ cố định, không năng lượng, meta-learning để thích nghi khi cảm biến dời chỗ, có huấn luyện tiếp, không seed/CI.
- **Đề tài:** năng lượng đẩy phụ thuộc tốc độ, DR không cần huấn luyện lại, 4 dịch chuyển có cấu trúc, đối chứng Fixed-PPO, 10 seed + CI.
- Đáng chú ý: động cơ "cảm biến dời chỗ sau thảm hoạ" gần với bộ `ood_cluster` của đề tài và có thể trích làm ví dụ ứng dụng cho dịch chuyển bố trí.

Hàng ma trận đề xuất (hàng mới):

| Công trình | Mục tiêu AoI | Năng lượng phụ thuộc tốc độ | Huấn luyện trên nhiều bố trí | Đánh giá OOD có cấu trúc | Nhiều seed + CI |
| --- | --- | --- | --- | --- | --- |
| Xiao 2024 (WiOpt) | Có (AoI trung bình + AoI cực đại; PT (9)†) | Không (tốc độ cố định 20 m/s, không mô hình năng lượng UAV; Bảng I†) | Một phần (MAML trên nhiều nhiệm vụ có vị trí cảm biến đổi; cách sinh nhiệm vụ không nêu; §III, Algorithm 1†) | Không (dời vị trí cảm biến rồi huấn luyện tiếp tới 10 000 episode, không zero-shot; Fig. 2–3†) | Không (không báo seed; Fig. 2 vùng tô không rõ n; Fig. 3 không thanh lỗi†) |

**Có mã nguồn/dữ liệu không:** Không thấy liên kết mã (†).

**Một câu hỏi cho nhóm:** Ba bài cùng nhóm Yi–Wang (2020, 2023, 2024) cho thấy một dòng nghiên cứu liên tục về AoI + UAV + DRL, và hai bài sau đều dùng meta-learning để xử lý thay đổi bố trí. Related Work có nên dành một đoạn riêng cho dòng "meta/transfer learning theo bố trí" (Yi 2023, Xiao 2024, Lu 2025) và nêu rõ điểm khác của DR là không cần huấn luyện lại không?
