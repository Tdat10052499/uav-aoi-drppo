# Form B — `theile2020`

> Trạng thái: **nháp Claude 06/11/2026, DAT chưa đọc lại.** Soạn từ toàn văn PDF arXiv:2003.02609, đọc qua công cụ tải trang của Claude (máy cloud không tải trực tiếp được file PDF). Vì vậy chưa có SHA256 và chưa ghi được số phiên bản arXiv. Mọi nhận định có kèm mục, bảng hoặc phương trình. Không có số nào đọc từ hình. Task W4-DAT-02; second reader: LDN.

**Tiêu đề / tác giả / năm / nơi công bố hoặc trạng thái preprint:** *UAV Coverage Path Planning under Varying Power Constraints using Deep Reinforcement Learning*.
- **Tác giả:** Mirco Theile, Harald Bayerlein, Richard Nai, David Gesbert, Marco Caccamo.
- **Năm và nơi công bố:** trang 1 của PDF không ghi hội nghị. Thông tin "IEEE/RSJ IROS 2020" và năm 2020 là **chưa kiểm** ✱ (cần mở trang abs của arXiv hoặc IEEE Xplore).

**URL nguồn gốc và phiên bản/ngày truy cập:** https://arxiv.org/pdf/2003.02609, truy cập 06/11/2026. Phiên bản chưa ghi ✱.

**Người đọc (NICK):** DAT (nháp Claude)

**Bài báo trả lời câu hỏi gì:** Học **một** chính sách bao phủ vùng (coverage path planning, CPP) cho UAV mà vẫn dùng được khi vị trí xuất phát và **ngân sách di chuyển** (mô hình hoá giới hạn pin) thay đổi, đồng thời tự chọn điểm hạ cánh (Abstract; §I, mục đóng góp).

**Giả định hệ thống:**
- **Không gian:** lưới N × N với ba kênh bản đồ Boolean: vùng xuất phát/hạ cánh, vùng mục tiêu cần bao phủ, vùng cấm bay (NFZ) (§II-B, §II-C). Bài không ghi kích thước ô bằng mét. Vùng quan sát là cửa sổ cố định 3 × 3 ô (§IV-A).
- **Hành động:** {bắc, đông, nam, tây, hạ cánh} (§II-C).
- **Năng lượng:** mỗi hành động tốn **1 đơn vị ngân sách di chuyển**, kể cả hành động bị từ chối, vì hover cũng tốn năng lượng (§IV-A). Không mô hình hoá tốc độ hay công suất đẩy.
- **Kết thúc episode:** khi ngân sách về 0 hoặc UAV đã hạ cánh (§III-C).
- **An toàn:** bộ điều khiển an toàn từ chối hành động không hợp lệ, ví dụ hạ cánh sai chỗ (§II-A).
- **Bản đồ tĩnh**, cố định cho mỗi tác nhân (§II-A, §IV).

**Cơ chế, diễn đạt bằng lời của mình:**
- **Trạng thái** (§II-C): tích của bản đồ 3 kênh, lưới bao phủ, vị trí, **ngân sách di chuyển còn lại (số tự nhiên)** và cờ an toàn.
- **Đầu vào mạng** (§III-C, Fig. 2):
  - vị trí UAV mã hoá one-hot 2D, xếp chồng với bản đồ và lưới bao phủ thành 5 kênh cho CNN;
  - **ngân sách còn lại là một số vô hướng, nối vào sau các lớp tích chập** ("The remaining movement budget is fed into the network after the convolutional layers"). Bài không nói ngân sách có được chuẩn hoá hay không.
- **Thưởng** (§II-C): thưởng bao phủ ô mục tiêu lần đầu; phạt khi bộ điều khiển an toàn từ chối; phạt hằng số cho mỗi đơn vị ngân sách dùng; phạt khi hết ngân sách mà chưa hạ cánh an toàn. Phần đã đọc không có giá trị số của các hệ số này.
- **Học:** DDQN, cập nhật mạng mục tiêu mềm τ = 0,005 (PT (7)–(9), Bảng I).
- **Siêu tham số** (Bảng I): N_max = 10 000 episode, buffer 50 000, minibatch 128, γ = 0,95, nhiệt độ softmax β = 0,1, Adam, 1 190 389 tham số.
- **Ngẫu nhiên hoá khi huấn luyện** (§III-C, §IV-A): mỗi episode lấy ngẫu nhiên điểm xuất phát trong vùng xuất phát và ngân sách đều trong [25, 75] đơn vị. Bản đồ cố định.

**Bằng chứng mạnh nhất (mục/bảng/hình):**
- **Bảng II:** tỉ lệ hạ cánh an toàn trên toàn dải ngân sách và mọi điểm xuất phát là 99,37% (bản đồ A), 99,78% (B), 98,26% (C).
- **Fig. 4:** tỉ lệ bao phủ theo ngân sách (không ghi số trong văn bản, nên không trích số).
- **Fig. 5:** đường cong thưởng tích luỹ trên bản đồ C có ba pha.

**Đánh giá trên kịch bản khác tập huấn luyện? Loại dịch chuyển nào?** **Không.** Đánh giá chỉ trong dải ngân sách [25, 75] và các điểm xuất phát đã dùng khi huấn luyện (§IV-B). Không thử ngân sách ngoài dải huấn luyện, không thử bản đồ mới. Mỗi bản đồ có một tác nhân riêng.

**Số seed / cách báo cáo độ bất định:** Bài không ghi số lần huấn luyện độc lập hay seed. Không có phương sai, CI hay kiểm định (Bảng II, Fig. 4).

**Đối chứng gần nhất và độ công bằng của so sánh:** Không có baseline định lượng. Các phương pháp CPP trước chỉ được bàn định tính (§I, §II).

**Giới hạn đã biết:**
1. Năng lượng hằng số theo bước, không có tốc độ (§IV-A).
2. Mục tiêu bao phủ, không phải AoI hay thu dữ liệu.
3. Không đánh giá OOD; không có baseline; không báo số seed.
4. Tác giả tự nêu: bộ điều khiển an toàn có thể cần ép quay về khi tác nhân lỡ thời điểm hạ cánh; hiệu năng nhạy với chiến lược khám phá (§IV-B, §V).

**Khác biệt với đề tài (điền vào ma trận docs/04 §5):**
- **Điểm trùng quan trọng:** bài **đã đưa ngân sách pin còn lại, ở dạng tuyệt đối (số bước), vào quan sát** dưới dạng số vô hướng, và huấn luyện trên dải ngân sách khác nhau (§II-C, §III-C, §IV-A). Đây chính là ý "policy phải biết ngân sách tuyệt đối" của thành phần A trong PG-TG-PPO. Xem mục "Hệ quả cho định vị" trong `bayerlein2021multi_DAT.md`.
- **Khác:** đề tài có năng lượng đẩy phụ thuộc tốc độ, nên số bước còn lại không còn tương đương với năng lượng còn lại. Đề tài dùng ρ_E (năng lượng còn lại quy ra số khe bay ở V_me, chia cho số khe còn lại). Ngoài ra đề tài có mục tiêu AoI, bộ OOD có cấu trúc, ≥ 10 seed kèm CI và đối chứng huấn luyện cố định.

Hàng ma trận đề xuất:

| Công trình | Mục tiêu AoI | Năng lượng phụ thuộc tốc độ | Huấn luyện trên nhiều bố trí | Đánh giá OOD có cấu trúc | Nhiều seed + CI |
| --- | --- | --- | --- | --- | --- |
| Theile 2020 ✱ | Không (bao phủ vùng, §II-C) | Không (1 đơn vị/bước, kể cả hover; §IV-A) | Một phần (ngẫu nhiên điểm xuất phát và ngân sách [25, 75]; bản đồ cố định; §IV-A) | Không (chỉ trong dải huấn luyện; §IV-B) | Không (không ghi số seed, không CI; Bảng II) |

**Có mã nguồn/dữ liệu không:** Phần đã đọc không nhắc mã nguồn ✱.

**Một câu hỏi cho nhóm:** Với cả Theile 2020 và Bayerlein 2021 đã có ngân sách tuyệt đối trong quan sát, thành phần A nên được trình bày là **mở rộng** ý này sang năng lượng phụ thuộc tốc độ, kèm phép đo vai trò của nó (H7), thay vì là một đóng góp riêng?
