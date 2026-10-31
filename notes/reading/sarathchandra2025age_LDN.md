# Form B — `sarathchandra2025age`

> Trạng thái: **nháp chờ LDN duyệt**, Claude soạn ngày 31/10/2026 từ toàn văn bản HTML arXiv:2501.14603v1. Người đọc: LDN (W2-LDN-01). Second reader: DAT. Bản tạp chí (IEEE TVT 2025, tiêu đề đổi "UAV" thành "AAV") chưa đọc; mọi số mục/hình dưới đây theo bản arXiv v1.

**Tiêu đề / tác giả / năm / nơi công bố hoặc trạng thái preprint:** *Age and Power Minimization via Meta-Deep Reinforcement Learning in UAV Networks*, 2025.
- **Tác giả:** Sankani Sarathchandra, Eslam Eldeeb, Mohammad Shehab, Hirley Alves, Konstantin Mikhaylov, Mohamed-Slim Alouini (ĐH Oulu, KAUST).
- **Trạng thái:** preprint arXiv:2501.14603v1 [cs.LG], 24/01/2025. Theo OpenAlex, bản tạp chí là *IEEE Transactions on Vehicular Technology*, 2025, DOI 10.1109/TVT.2025.3579626, tiêu đề dùng "AAV" ✱ (chưa kiểm trên trang IEEE).

**URL nguồn gốc và phiên bản/ngày truy cập:** https://arxiv.org/abs/2501.14603 (v1); toàn văn HTML https://arxiv.org/html/2501.14603v1, truy cập 31/10/2026.

**Người đọc (NICK):** LDN

**Bài báo trả lời câu hỏi gì:** Khi trọng số giữa AoI và công suất phát của thiết bị IoT thay đổi, có thể dùng meta-learning (MAML) để một chính sách DQN cho UAV thích nghi nhanh với trọng số mới, thay vì huấn luyện lại từ đầu, hay không (§I-B, bài toán P1, PT (4a)–(4b)).

**Giả định hệ thống:**
- **Quy mô:** một UAV, độ cao 100 m, lưới 10 × 10 ô trên vùng 1000 m × 1000 m; 5 hoặc 10 thiết bị đặt ngẫu nhiên (§II, §V, Bảng II).
- **Chuyển động:** mỗi bước UAV sang một ô kề (Bắc, Nam, Đông, Tây) hoặc treo (PT (7)). Không có lựa chọn tốc độ.
- **Kênh:** LoS, suy hao theo bình phương khoảng cách (PT (1)). Công suất phát của thiết bị là công suất tối thiểu để gửi gói M = 5 Mb trong một bước (PT (2)).
- **Năng lượng:** chỉ có **công suất phát của thiết bị IoT**. **Không có mô hình năng lượng bay của UAV** (§II, PT (4a), (6)).
- **AoI:** về 1 khi thiết bị được lập lịch, ngược lại tăng 1, bị chặn trên A_max = 30 (PT (3), Bảng II).
- **Mục tiêu:** AoI trung bình + λ × tổng công suất phát (PT (4a), phần thưởng PT (6)). Mỗi giá trị λ là một "nhiệm vụ" (§II-A, §IV).

**Cơ chế, diễn đạt bằng lời của mình:**
- Trạng thái: vị trí UAV và vector AoI của các thiết bị, kích thước 2 + D (§III-A1). **Vị trí thiết bị không có trong trạng thái.**
- Hành động: chọn thiết bị được phục vụ × hướng bay, tổng D × 5 hành động (§III-A2).
- Meta-training: MAML trên mạng Q của DQN (Algorithm 3). Mỗi nhiệm vụ cập nhật trọng số riêng theo PT (9), rồi tổng tổn thất trên các nhiệm vụ cập nhật trọng số khởi tạo chung theo PT (10)–(11). Có 10 nhiệm vụ huấn luyện với λ khác nhau, 500 epoch (§V).
- Meta-testing: từ trọng số khởi tạo đã học, tinh chỉnh vài chục episode trên nhiệm vụ mới (§III-C, §IV). Đây là **thích nghi có tinh chỉnh (few-shot)**, không phải dùng ngay chính sách đã học (zero-shot).

**Bằng chứng mạnh nhất (mục/bảng/hình):**
- **Fig. 4:** với λ = 300, khởi tạo MAML hội tụ sau khoảng 100 episode, khởi tạo ngẫu nhiên cần cả 500 episode, ở cả 5 và 10 thiết bị.
- **Fig. 5:** phần thưởng sau 30 episode tinh chỉnh, trên 11 môi trường kiểm thử, tăng theo số nhiệm vụ huấn luyện. Với 10 thiết bị cần ít nhất 6 nhiệm vụ huấn luyện.
- **Fig. 6:** cặp (AoI, công suất phát) theo λ; MAML thấp hơn khởi tạo ngẫu nhiên ở mọi λ. Chính tác giả ghi rằng khởi tạo ngẫu nhiên đạt cùng vùng nếu huấn luyện thêm (§V, đoạn cuối). Vì vậy lợi ích được chứng minh là **hiệu quả mẫu**, không phải chất lượng chính sách cuối.
- Bài không in bảng số; mọi kết quả là hình.

**Đánh giá trên kịch bản khác tập huấn luyện? Loại dịch chuyển nào?** Có, nhưng hẹp.
- Loại dịch chuyển: **trọng số mục tiêu λ** (11 môi trường kiểm thử với λ mới; §V, Fig. 3, 5, 6).
- §IV viết rằng môi trường kiểm thử khác cả vị trí thiết bị lẫn λ, nhưng §V chỉ mô tả việc thay λ. Không rõ vị trí thiết bị có thật sự đổi giữa các môi trường hay không.
- Mọi đánh giá đều có tinh chỉnh trước khi đo; không có đánh giá zero-shot. Không có dịch chuyển có cấu trúc về phân bố không gian của thiết bị.

**Số seed / cách báo cáo độ bất định:** Không báo số seed. Fig. 3–6 là một đường cho mỗi cấu hình, không có vùng tin cậy hay kiểm định. Fig. 3 có trung bình meta-loss trên lô 6 môi trường, nhưng đó là trung bình trong một lần chạy.

**Đối chứng gần nhất và độ công bằng của so sánh:**
- Đối chứng duy nhất là cùng DQN với khởi tạo ngẫu nhiên, tinh chỉnh cùng số episode (§V).
- So sánh này thiên về meta-learning: khởi tạo MAML đã được tiếp xúc nhiều nhiệm vụ trong 500 epoch meta-training, còn khởi tạo ngẫu nhiên chỉ có ngân sách tinh chỉnh. Bài không có đối chứng "huấn luyện chung trên mọi λ" (multi-task không MAML) hay đối chứng có λ trong trạng thái, nên không tách được tác dụng của MAML với tác dụng của việc thấy nhiều nhiệm vụ.
- Không có heuristic.

**Giới hạn đã biết:**
1. Mâu thuẫn §IV và §V về việc vị trí thiết bị có đổi giữa các môi trường.
2. Bảng ký hiệu (Bảng I) dùng I cho cả số nhiệm vụ và số epoch; ràng buộc (4b) về ngân sách few-shot E_max không được nêu giá trị.
3. Bảng II ghi g₀ = 30 dB (dương) cho độ lợi kênh tại 1 m; thường là giá trị âm. Có thể là lỗi in.
4. Phần thưởng (6) chia AoI cho D nhưng không chia công suất cho D, khác với PT (4a).
5. Không công bố mã.

**Khác biệt với đề tài (điền thẳng vào ma trận docs/04 §5):**
- **Sarathchandra 2025:** thay đổi **hàm mục tiêu** (λ giữa AoI và công suất phát thiết bị), thích nghi có tinh chỉnh; không có năng lượng bay của UAV; không có lựa chọn tốc độ.
- **Đề tài:** λ cố định cho mỗi lần huấn luyện (quét λ là RQ2, EXP-05), năng lượng **đẩy của UAV** phụ thuộc tốc độ, tổng quát hoá **theo bố trí**, đánh giá thẳng mô hình đã huấn luyện trên 4 bộ OOD mà không tinh chỉnh (`docs/03` §4), 10 seed + CI.
- Có thể trích bài này ở Related Work như ví dụ "tổng quát hoá theo mục tiêu" khác với "tổng quát hoá theo bố trí".

Hàng ma trận đề xuất (thay hàng hiện có):

| Công trình | Mục tiêu AoI | Năng lượng phụ thuộc tốc độ | Huấn luyện trên nhiều bố trí | Đánh giá OOD có cấu trúc | Nhiều seed + CI |
| --- | --- | --- | --- | --- | --- |
| Sarathchandra 2025 | Có (AoI + λ·công suất phát thiết bị; PT (4a), (6)) | Không (không có năng lượng bay của UAV; chỉ công suất phát thiết bị, PT (2)) | Không rõ (meta-training trên 10 giá trị λ; §IV nói vị trí thiết bị cũng thay đổi nhưng §V không mô tả; trạng thái không chứa vị trí thiết bị, §III-A1) | Không (chỉ thay λ, có tinh chỉnh 30–500 episode, không zero-shot; Fig. 4–6) | Không (không báo seed, không vùng tin cậy; Fig. 3–6) |

**Có mã nguồn/dữ liệu không:** Không thấy liên kết mã hay dữ liệu trong bài.

**Một câu hỏi cho nhóm:** Bài cho thấy MAML chủ yếu tiết kiệm số episode tinh chỉnh. Đề tài có cần thêm một đối chứng "tinh chỉnh vài episode trên bộ OOD" cho Fixed-PPO (để so với DR-PPO zero-shot) không, hay giữ cách đánh giá không tinh chỉnh của `docs/03` §4 và ghi đây là giới hạn?
