# Form B — `eldeeb2026resilient`

> Trạng thái: **nháp chờ LDN duyệt**, Claude soạn ngày 31/10/2026 từ toàn văn HTML arXiv:2502.01268v1. Người đọc: LDN (nhóm A8 trong `fulltext_list.md`). Second reader: DAT. Bản tạp chí (IEEE TMLCN 2026, DOI 10.1109/TMLCN.2026.3656262 theo OpenAlex ✱) có tóm tắt viết lại; chưa đọc. Số mục/hình theo bản arXiv.

**Tiêu đề / tác giả / năm / nơi công bố hoặc trạng thái preprint:** *Resilient UAV Trajectory Planning via Few-Shot Meta-Offline Reinforcement Learning*, Eslam Eldeeb, Hirley Alves (ĐH Oulu), 2025 (arXiv) / 2026 (tạp chí, tiêu đề dùng "AAV") ✱. Cùng nhóm và cùng mô hình hệ thống với Sarathchandra 2025.

**URL nguồn gốc và phiên bản/ngày truy cập:** https://arxiv.org/abs/2502.01268 (v1, 03/02/2025); toàn văn https://arxiv.org/html/2502.01268v1, truy cập 31/10/2026.

**Người đọc (NICK):** LDN

**Bài báo trả lời câu hỏi gì:** Có thể học chính sách quỹ đạo và lập lịch cho UAV chỉ từ một tập dữ liệu ngoại tuyến nhỏ (không tương tác trực tuyến), rồi thích nghi nhanh với mục tiêu mới hoặc với vùng mất kết nối (mưa lớn) chưa thấy hay không, bằng cách kết hợp CQL với MAML (§I-D, bài toán P1, PT (5a)–(5c)).

**Giả định hệ thống:**
- **Quy mô:** một UAV cánh quay **bay với vận tốc cố định U**, độ cao 100 m; vùng 1000 m × 1000 m chia 10 × 10 ô; K = 10 thiết bị IoT đặt ngẫu nhiên ở tâm ô; T = 100 bước; UAV xuất phát ở vị trí ngẫu nhiên mỗi episode (§II, §V-A, Bảng I).
- **Chuyển động:** 4 hướng hoặc đứng yên (PT (1)).
- **Kênh:** LoS (PT (2)); công suất phát tối thiểu của thiết bị theo khoảng cách (PT (3)); thêm suy hao do mưa γ_R = φR^ϕ với R = 12,5 mm/h trong vùng mưa (§II).
- **Năng lượng:** chỉ công suất phát của thiết bị; **không có năng lượng bay của UAV** (PT (5a)).
- **Mục tiêu:** AoI có trọng số + λ × công suất phát trung bình (PT (5a), phần thưởng PT (6)). Mỗi giá trị λ là một nhiệm vụ.

**Cơ chế, diễn đạt bằng lời của mình:**
- Trạng thái: vị trí UAV + vector AoI, độ dài 2 + K; hành động: hướng × thiết bị, 5K hành động (§III-A). **Vị trí thiết bị không có trong trạng thái.**
- Dữ liệu ngoại tuyến cho mỗi môi trường lấy từ replay buffer của một tác tử DQN trực tuyến (§V-A).
- CQL thêm số hạng phạt các hành động ngoài dữ liệu vào tổn thất DQN (PT (9)). MAML học trọng số khởi tạo trên nhiều nhiệm vụ (λ khác nhau), rồi tinh chỉnh vài epoch CQL trên nhiệm vụ mới (PT (13)–(15), Algorithm 4).

**Bằng chứng mạnh nhất (mục/bảng/hình):**
- **Fig. 5:** trên một λ mới, CQL-MAML (khởi tạo meta, 8 nhiệm vụ huấn luyện, 500 mẫu) hội tụ trong dưới 40 epoch; CQL khởi tạo ngẫu nhiên cần hơn 100 epoch; DQN và DQN-MAML ngoại tuyến không hội tụ (§V-B).
- **Fig. 7:** cần ít nhất 8 nhiệm vụ meta-training để vượt DQN trực tuyến sau 40 epoch (§V-B).
- **Fig. 8:** với λ = 300 sau 50 epoch, CQL-MAML đạt AoI khoảng 6 và công suất khoảng 1,6 mW, so với CQL (28; 6 mW) và DQN trực tuyến (7; 2,2 mW) (§V-B). Một lần chạy, không thanh lỗi.
- **Fig. 9:** meta-train không có vùng mưa, kiểm thử trên 5 nhiệm vụ có vùng mưa thay đổi vị trí; sau khoảng 100 epoch, CQL-MAML gần như không vào vùng mưa, CQL vẫn khoảng 20 lần (§V-C). Fig. 9b lấy trung bình trên 1000 vòng Monte Carlo qua 5 nhiệm vụ.

**Đánh giá trên kịch bản khác tập huấn luyện? Loại dịch chuyển nào?** Có, nhưng có tinh chỉnh.
- Dịch chuyển: (a) trọng số mục tiêu λ mới (§V-B); (b) vùng mất kết nối do mưa, chưa có khi meta-training, vị trí thay đổi (§V-C).
- Mọi đánh giá đều sau một số epoch tinh chỉnh ngoại tuyến trên dữ liệu của nhiệm vụ mới; không có đánh giá ngay khi gặp nhiệm vụ mới.
- Không thay đổi bố trí hay số thiết bị.

**Số seed / cách báo cáo độ bất định:** Không báo số seed huấn luyện. Fig. 4–8 một đường mỗi phương pháp. Fig. 9b có trung bình 1000 vòng Monte Carlo nhưng không có khoảng tin cậy và không rõ đó là vòng đánh giá hay vòng huấn luyện độc lập.

**Đối chứng gần nhất và độ công bằng của so sánh:**
- DQN, DQN-MAML, CQL (đều ngoại tuyến) và DQN trực tuyến (§V-A).
- Như Sarathchandra 2025: không có đối chứng huấn luyện chung trên mọi nhiệm vụ không dùng MAML, nên không tách được tác dụng của MAML với việc thấy nhiều nhiệm vụ.
- Tập dữ liệu ngoại tuyến sinh từ replay của chính DQN trực tuyến; không nói DQN trực tuyến được huấn luyện bao lâu, nên so sánh "ngoại tuyến tốt hơn trực tuyến" (Fig. 5, 8) phụ thuộc vào điều kiện không được nêu.

**Giới hạn đã biết:**
1. Mục I-D gọi khung là "meta-offline MARL" dù hệ thống chỉ có một UAV.
2. Ký hiệu γ dùng cho cả hệ số chiết khấu và suy hao do mưa; Bảng I liệt kê γ hai lần.
3. Ràng buộc (5c) viết |𝒟| ≤ D_const nhưng lời giải thích nói kích thước tập dữ liệu "lớn hơn hoặc bằng" ngưỡng.
4. Không công bố mã.

**Khác biệt với đề tài (điền thẳng vào ma trận docs/04 §5):**
- **Eldeeb 2026:** học ngoại tuyến + meta-learning, thích nghi có tinh chỉnh theo λ và theo vùng mất kết nối; không có năng lượng bay; một bố trí; không seed/CI.
- **Đề tài:** học trực tuyến PPO với DR theo bố trí, đánh giá không tinh chỉnh trên 4 dịch chuyển bố trí/tài nguyên, có năng lượng đẩy phụ thuộc tốc độ, 10 seed + CI.
- Bài không đe doạ định vị; có thể trích ở Related Work cùng Sarathchandra 2025 như nhóm "thích nghi theo mục tiêu/điều kiện kênh bằng meta-learning".

Hàng ma trận đề xuất (hàng mới):

| Công trình | Mục tiêu AoI | Năng lượng phụ thuộc tốc độ | Huấn luyện trên nhiều bố trí | Đánh giá OOD có cấu trúc | Nhiều seed + CI |
| --- | --- | --- | --- | --- | --- |
| Eldeeb 2026 (arXiv 2502.01268) | Có (AoI có trọng số + λ·công suất phát; PT (5a)) | Không (UAV vận tốc cố định U, không năng lượng bay; §II) | Không (nhiệm vụ khác nhau theo λ; trạng thái không chứa vị trí thiết bị; §III-A, §V-A) | Một phần (λ mới và vùng mưa chưa thấy, 5 nhiệm vụ; có tinh chỉnh 40–200 epoch; §V-B, §V-C, Fig. 5, 9) | Không (không báo seed; Fig. 9b trung bình 1000 vòng Monte Carlo, không CI) |

**Có mã nguồn/dữ liệu không:** Không thấy liên kết mã hay dữ liệu.

**Một câu hỏi cho nhóm:** Dịch chuyển "vùng mất kết nối" (§V-C) không có trong 4 bộ OOD của đề tài. Có nên ghi vào Limitations rằng đề tài chỉ xét dịch chuyển về bố trí và năng lượng, không xét dịch chuyển kênh (kênh vẫn LoS cố định) không?
