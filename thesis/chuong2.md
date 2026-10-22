# Chương 2. Tổng quan nghiên cứu

> **BẢN NHÁP W11-FAO-01, viết sớm ngày 22/10/2026 (FAO).** Second reader: DAT.
>
> **Nguồn được dùng:**
> - Chỉ dùng ma trận `docs/04` §5 và các Form B trong `notes/reading/`.
> - Câu dựa trên nguồn ◐ (chỉ tóm tắt) được đánh dấu **(◐)** và phải kiểm toàn văn trước khi nộp.
>
> **Phần còn thiếu:**
> - **Mục 2.1 chờ số PRISMA** trong `notes/reading/search_log_LDN.md` (task W2 của LDN, chốt ở W3 khi duyệt G0). FAO không tự điền số.
> - Mục 2.5 phải cập nhật sau G0 (01/11).
>
> **Quy tắc:** không viết "đầu tiên" (CLAUDE.md quy tắc 7).

## 2.1. Phương pháp tổng quan

### 2.1.1. Nguồn và khoảng thời gian
- **Cơ sở dữ liệu:** IEEE Xplore, Scopus, Google Scholar (tra thủ công) và arXiv (cs.NI, cs.LG, eess.SP).
- **Khoảng thời gian:** 2018–2026.
- **Chuỗi tìm kiếm:** Q1–Q3 trong `docs/04` §6, gồm ba nhóm từ khoá:
  - Q1: UAV + AoI + RL + tổng quát hoá;
  - Q2: UAV + thu dữ liệu + RL + số cảm biến thay đổi;
  - Q3: UAV + AoI + năng lượng đẩy + PPO.

### 2.1.2. Tiêu chí chọn và loại
- **Chọn:**
  - bài toán UAV thu dữ liệu từ cảm biến mặt đất;
  - có dùng DRL;
  - có đánh giá trên kịch bản khác tập huấn luyện, **hoặc** có cặp AoI + năng lượng đẩy.
- **Loại:**
  - chỉ dùng tối ưu lồi hoặc heuristic;
  - chỉ điều khiển bay mức thấp.

### 2.1.3. Sơ đồ PRISMA rút gọn
Số liệu chờ `notes/reading/search_log_LDN.md`:

| Bước | Số bài |
| --- | --- |
| Kết quả từ các cơ sở dữ liệu (Q1–Q3, trước khi bỏ trùng) | CHỜ |
| Sau khi bỏ trùng | CHỜ |
| Sau lọc tiêu đề/tóm tắt | CHỜ |
| Đọc toàn văn | CHỜ |
| Đưa vào ma trận định vị | CHỜ |

### 2.1.4. Ghi chú về truy cập toàn văn
Một số bài chỉ đọc được tóm tắt:
- OH-DRL 2025: không có bản arXiv, nhóm không có quyền IEEE Xplore;
- Lamenza 2025: không mở được toàn văn.

Những bài này được ghi rõ trong ma trận. Chúng không được dùng làm căn cứ cho bất kỳ khẳng định nào về khoảng trống nghiên cứu.

## 2.2. DRL cho UAV thu thập dữ liệu

### 2.2.1. Các tổng quan
Ba tổng quan khảo sát rộng việc dùng DRL trong truyền thông và mạng UAV (◐):
- Luong và cộng sự [luong2019applications];
- Zhao và cộng sự [zhao2025survey];
- Amodu và cộng sự [amodu2025survey], tập trung vào thu dữ liệu IoT.

Chương này chỉ dẫn các tổng quan như điểm vào lĩnh vực, không trích kết luận cụ thể của chúng.

### 2.2.2. Bayerlein và cộng sự (2021) [bayerlein2021multi]
Đây là công trình gần đề tài nhất (`docs/04` §1, đọc toàn văn).
- **Thuật toán:** DDQN đa tác tử cho 1–3 UAV.
- **Quan sát:** bản đồ toàn cục–cục bộ căn tâm theo UAV, trên bản đồ đô thị có che khuất.
- **Tổng quát hoá:** một chính sách phục vụ được dải tham số kịch bản: số UAV; số, vị trí và lượng dữ liệu của cảm biến; thời gian bay; điểm xuất phát. Bài có thử ngoại suy tham số.
- **Khác đề tài ở ba điểm:**
  1. Mục tiêu là tối đa lượng dữ liệu thu trong **một** nhiệm vụ, không phải độ tươi thông tin qua nhiều chu kỳ.
  2. Năng lượng mỗi bước là hằng số, với lập luận rằng bay ngang chỉ tốn hơn hover một ít. Vì vậy tốc độ không phải biến quyết định.
  3. Hiệu năng báo cáo là trung bình Monte Carlo trên kịch bản, không có phân tích theo seed huấn luyện.

### 2.2.3. de Souza Lamenza và cộng sự (2025) [lamenza2025] (◐)
- Hướng tới một mô hình dùng được cho số cảm biến và số tác tử bất kỳ ("flexible sensor count"), trong bài toán thăm mỗi cảm biến một lần.
- Chưa đọc được toàn văn nên chưa xác định được cách đánh giá tổng quát hoá.

## 2.3. AoI, năng lượng và DRL

### 2.3.1. Abd-Elmagid và cộng sự (2019) [abdelmagid2019deep]
Nguồn: `notes/reading/abdelmagid2019deep_FAO.md`.
- **Bài toán:** chọn đồng thời nước đi của UAV và lịch cập nhật để tối thiểu tổng AoI có trọng số, mô hình hoá thành MDP chân trời hữu hạn và giải bằng DQN.
- **Mô hình:**
  - lưới 11 × 11, mỗi ô 100 m;
  - UAV đi một ô mỗi khe;
  - có tối đa 3 nút mặt đất;
  - năng lượng chỉ là pin của nút; UAV chỉ bị ràng buộc thời gian bay.
- **Đánh giá:**
  - mỗi kịch bản có vị trí nút cố định, và các biến thiên chỉ là quét tham số;
  - số liệu là trung bình 1000 episode, không báo seed hay khoảng tin cậy;
  - so với hai heuristic, DRL đạt sum-AoI thấp hơn khoảng 50% so với heuristic theo khoảng cách (Fig. 5b, theo tác giả).

### 2.3.2. Yi và cộng sự (2020) [yi2020deep] (◐)
- Kết hợp quyết định quỹ đạo và lập lịch để giảm AoI có trọng số dưới ràng buộc năng lượng.
- Cần toàn văn để biết:
  - ràng buộc năng lượng là của UAV hay của cảm biến;
  - bố trí có thay đổi giữa lúc huấn luyện và lúc đánh giá hay không.

### 2.3.3. Sun và cộng sự (2025) [sun2025aoi]
Nguồn: `notes/reading/sun2025aoi_FAO.md`.
- **Bài toán:** tối thiểu peak AoI trong mạng 4 UAV được sạc bằng laser.
- **Phương pháp:** MAPPO có bộ nhớ LSTM và hàm giá trị kết hợp cục bộ–toàn cục.
- **Năng lượng:** có mô hình công suất đẩy dạng Zeng, nhưng tốc độ cố định 5 m/s. Năng lượng vì vậy chỉ phụ thuộc thời gian bay.
- **Đánh giá:**
  - vị trí IoT cố định;
  - "độ bền" chỉ được xét qua quét hiệu suất sạc η_le;
  - không báo số seed;
  - không có đối chứng heuristic, dù bài quy bài toán về TSP để chứng minh NP-khó.
- **Điểm đáng chú ý:** ở §VII, các tác giả nêu domain randomization là hướng tương lai để cải thiện tổng quát hoá.

### 2.3.4. OH-DRL (2025) [ohdrl2025] (◐, chỉ tóm tắt)
Nguồn: `notes/reading/ohdrl2025_FAO.md`.
- **Vai trò hai đại lượng đảo ngược so với đề tài:** tối thiểu năng lượng bay với ràng buộc AoI trung bình tối đa.
- **Thiết kế phân cấp:**
  - DRL chọn chính sách thăm của UAV;
  - semidefinite relaxation xử lý lịch truyền và beamforming của STAR-RIS.
- **Kết quả theo tóm tắt:** năng lượng bay thấp hơn 14,4% và số episode hội tụ ít hơn 66% so với một thuật toán DRL không nêu tên.
- **Chưa biết:** bài có đánh giá trên bố trí khác tập huấn luyện hay không.

### 2.3.5. Sarathchandra và cộng sự (2025) [sarathchandra2025age] (◐)
- Dùng DQN kết hợp meta-learning (MAML) để thích nghi khi **hàm mục tiêu** (trọng số giữa tuổi và công suất phát) thay đổi.
- Dịch chuyển được xét nằm ở mục tiêu, không phải ở bố trí triển khai.

### 2.3.6. Các bài khác chưa đưa vào ma trận
Hai bài sau chỉ được ghi nhận ở mức tóm tắt (`docs/04` §2), chưa đưa vào ma trận:
- Huang và cộng sự: SCA cho lập lịch, A3C phân cấp cho đường bay;
- Kumari và cộng sự [kumari2024aoi]: phân cụm kết hợp PPO.

## 2.4. Tổng quát hoá trong DRL

### 2.4.1. Domain randomization
Domain randomization [tobin2017domain ✱] huấn luyện trên phân phối môi trường mô phỏng để chính sách chuyển được sang điều kiện chưa thấy.

### 2.4.2. Liu (2024) [liu2024generalizable]
Nguồn: `notes/reading/liu2024generalizable_FAO.md`. Bài thuộc miền đua drone, ngoài tiêu chí chọn ở 2.1, nên chỉ dùng làm tham khảo phương pháp.
- **Cách làm:** áp dụng DR cho PPO bằng cách sinh lại đường đua và chướng ngại cho mỗi rollout.
- **Đánh giá:** trên 4 mức khó và 4 đường đua thiết kế tay.
- **Kết quả:** tỷ lệ thành công giảm dần khi đường đua thử lệch xa phân phối huấn luyện, từ khoảng 0,9 ở mức 1 xuống khoảng 0,4 ở mức 4 (Fig. 10).
- **Thiếu sót:** không có đối chứng huấn luyện trên môi trường cố định, chỉ một chính sách, không seed hay CI.

Kết quả này cho thấy DR không bảo đảm ngoại suy. Đề tài vì vậy phải đo, không giả định, mức suy giảm trên từng loại dịch chuyển.

### 2.4.3. Báo cáo thống kê
Agarwal và cộng sự [agarwal2021deep] chỉ ra rằng báo cáo điểm đơn lẻ từ ít lần chạy dễ dẫn tới kết luận sai. Họ đề xuất khoảng tin cậy bootstrap và IQM (Chương 1, mục 1.7). Trong các bài AoI–UAV đã đọc toàn văn, không bài nào báo cáo theo seed huấn luyện kèm khoảng tin cậy (ma trận 2.5).

## 2.5. Ma trận định vị

Nguồn: `docs/04` §5, cập nhật ngày 21/10/2026.

| Công trình | Mục tiêu AoI | Năng lượng phụ thuộc tốc độ | Huấn luyện trên nhiều bố trí | Đánh giá OOD có cấu trúc | Nhiều seed + CI |
| --- | --- | --- | --- | --- | --- |
| Bayerlein 2021 | Không (dữ liệu thu) | Không (hằng số/bước) | Có | Một phần (ngoại suy tham số) | Monte Carlo trên kịch bản |
| Yi 2020 (◐) | Có | Có ràng buộc năng lượng | Chưa rõ | Chưa rõ | Chưa rõ |
| Sarathchandra 2025 (◐) | Có | Công suất phát | Không (thay mục tiêu) | Không | Chưa rõ |
| Lamenza 2025 (◐) | Không (thăm một lần) | Chưa rõ | Có (số cảm biến linh hoạt) | Chưa rõ | Chưa rõ |
| Abd-Elmagid 2019 | Có (tổng AoI có trọng số) | Không | Không | Không | Không |
| Sun 2025 | Có (peak AoI, đa UAV) | Có P(v) nhưng v cố định | Không | Không | Không |
| OH-DRL 2025 (◐) | Có (ràng buộc) | Chưa rõ | Chưa rõ | Chưa rõ | Chưa rõ |
| Liu 2024 (ngoài phạm vi) | Không | Không | Có | Có | Không |
| **Đề tài** | Có | Có (Zeng 2019) | Có | Có (4 bộ) | Có (10 seed, CI, Holm) |

## 2.6. Khoảng trống và vị trí của đề tài

### 2.6.1. Khoảng trống
Từ ma trận, trong các công trình đã đọc toàn văn:
- **Bayerlein 2021** đã giải quyết tổng quát hoá theo tham số kịch bản, nhưng với mục tiêu thu dữ liệu một lần và năng lượng hằng số.
- **Các bài AoI** (Abd-Elmagid 2019, Sun 2025) huấn luyện và đánh giá trên bố trí cố định. Sun 2025 có mô hình công suất đẩy nhưng giữ tốc độ cố định.
- **Phân tích theo seed:** không bài nào trong nhóm này báo cáo theo seed huấn luyện kèm khoảng tin cậy.

### 2.6.2. Câu hỏi đề tài theo đuổi
Câu hỏi còn để ngỏ (câu định vị nháp, `docs/01` §3): chính sách học được có còn bền vững dưới các dịch chuyển phân phối có cấu trúc hay không, khi mục tiêu là độ tươi thông tin liên tục và năng lượng đẩy phụ thuộc tốc độ.

Đề tài không khẳng định là công trình đầu tiên tổng quát hoá cho UAV thu dữ liệu: Bayerlein 2021 đã làm điều đó theo tham số kịch bản. Đóng góp nằm ở **tổ hợp** ba yếu tố:
1. mục tiêu AoI cùng năng lượng phụ thuộc tốc độ, với tốc độ là biến quyết định;
2. so sánh có kiểm soát giữa DR và huấn luyện trên bố trí cố định, trên bốn loại dịch chuyển có cấu trúc;
3. phân tích thống kê theo seed huấn luyện.

### 2.6.3. Điều kiện để giữ nguyên nhận định
Nhận định này chỉ đúng cho các bài đã đọc toàn văn. Nếu OH-DRL, Yi 2020 hoặc Lamenza 2025 hoá ra có đủ năm cột "Có", đóng góp C2 phải viết lại (gate G0, `docs/05`).
