# Form B — `lamenza2025`

> Trạng thái: **owner DAT đánh dấu xong 30/10 (W1-DAT-04), chờ second reader LDN**; soạn từ toàn văn PDF bản xuất bản (14 trang, SHA256 `8ccb22d7…54bc6993`, DAT tải từ Wiley Online Library ngày 29/10/2026 và gửi ngày 30/10/2026). Second reader: LDN. Mọi số liệu lấy từ văn bản và Bảng 1. **Phần lớn kết quả định lượng của bài chỉ có trên hình (Fig. 1, 4, 7, 8)**; Form B không đọc số từ hình.

**Tiêu đề / tác giả / năm / nơi công bố hoặc trạng thái preprint:** *Deep Reinforcement Learning Approaches for Sensor Data Collection by a Swarm of UAVs*.
- **Tác giả:** Thiago de Souza Lamenza, Bruno José Olivieri de Souza, Markus Endler (PUC-Rio, Brazil).
- **Nơi công bố:** Advanced Intelligent Systems, 2026, 8:e202501146, DOI 10.1002/aisy.202501146 (đầu trang 1). Nhận 25/09/2025, sửa 03/12/2025, chấp nhận 05/01/2026. Truy cập mở, CC BY. **Năm xuất bản là 2026**, không phải 2025. Khoá `lamenza2025` được giữ nguyên để không đổi các trích dẫn đã có; trường `year` trong `paper/references.bib` ghi 2026 (DECISIONS 2026-10-30).

**URL nguồn gốc và phiên bản/ngày truy cập:** https://doi.org/10.1002/aisy.202501146 (bản xuất bản, tập 8 số 5 theo chân trang tải về), DAT tải ngày 29/10/2026.

**Người đọc (NICK):** DAT (nháp Claude)

**Bài báo trả lời câu hỏi gì:** Một bầy UAV phân tán thu dữ liệu từ cảm biến mặt đất bằng DRL. Bài so sánh bốn biến thể MADDPG theo ba thước đo: tỉ lệ thành công, thời gian hoàn thành và **thời gian huấn luyện** (§1). Có hai câu hỏi chính: hợp tác có lợi không, và mô hình tổng quát hơn theo số cảm biến hoặc số UAV có giảm tổng chi phí huấn luyện mà ít mất hiệu năng không (§1, §3.4, §3.5).

**Giả định hệ thống:**
- **Số UAV:** N_a ∈ {2, 4, 8}, đồng nhất, dùng chung tham số mạng (parameter sharing) (§3.1, §4).
- **Không gian:** vùng vuông 200 m × 200 m, phẳng. UAV xuất phát ngẫu nhiên trong ô 4 m × 4 m ở tâm; cảm biến phân bố ngẫu nhiên trên toàn vùng (§2, §4). Độ cao cố định nhưng **không ghi giá trị**.
- **Hành động liên tục:** a = ⟨θ ∈ [0, 2π], s ∈ [0, 15]⟩, gồm hướng và tốc độ, chuẩn hoá về [0, 1] (PT (7), §3.2). Bài không ghi đơn vị của s; có thể là m/s, nhưng đó là suy đoán.
- **Di chuyển:** "constant speed and instant change in direction"; UAV đổi tốc độ và hướng tức thời (§2).
- **Năng lượng: không mô hình hoá.** Bài xếp "energy handling" vào việc tương lai (§6).
- **Kênh:** không có mô hình kênh. Thu được dữ liệu khi UAV cách cảm biến ≤ 20 m (§4); truyền qua hai thông điệp trên trình mô phỏng GrADyS-SIM NextGen (§3.2, §4).
- **Liên lạc giữa UAV:** giả định có kênh vệ tinh toàn cục, nên mỗi UAV biết vị trí các UAV khác và trạng thái đã thăm của cảm biến (§1, §2). Tác giả tự nhận đây là giới hạn.
- **Mục tiêu:** **thu một lần** (single-cycle): mỗi cảm biến chỉ cần thăm một lần (§1). Tác giả nêu rõ các công trình thu nhiều chu kỳ thường dùng AoI ([14]–[18] của bài) và **chủ ý không** chọn hướng đó.

**Cơ chế, diễn đạt bằng lời của mình:**
- **Khung học:** MADDPG với huấn luyện tập trung, thực thi phân tán (CLDE). Critic toàn cục nhận ghép các quan sát. Mọi UAV dùng chung một actor (§3.1).
- **Bốn biến thể:**
  1. **Không hợp tác** (§3.2): quan sát chỉ là toạ độ tương đối tới cảm biến chưa thăm gần nhất (PT (1)–(4)). Thưởng là tỉ lệ cảm biến đã thăm (PT (5)). Một mô hình dùng được cho mọi số UAV và cảm biến.
  2. **Hợp tác** (§3.3): quan sát gồm toạ độ tương đối của N*_s cảm biến chưa thăm gần nhất (thiếu thì điền 0), của N*_a UAV gần nhất, và định danh k (PT (8)–(9)). Thưởng = +10 × số cảm biến mới thăm; nếu không thăm thêm thì phạt theo tỉ lệ cảm biến còn lại (PT (10)–(11)). Mỗi cặp (N_a, N_s) phải huấn luyện một mô hình riêng.
  3. **Linh hoạt số cảm biến** (§3.4): giống biến thể hợp tác, nhưng mỗi episode huấn luyện lấy N_s ngẫu nhiên đều trong [min N_s, max N_s]. Đây là một dạng domain randomization trên **một** tham số; tác giả không dùng thuật ngữ này. **Bài không ghi giá trị min N_s, max N_s, N*_s, N*_a.**
  4. **Linh hoạt số UAV** (§3.5): huấn luyện với số UAV cố định, triển khai với số UAV khác (theo [25] của bài). Tác giả đã thử điền 0 hoặc nhân bản thông tin để giữ kích thước đầu vào critic, nhưng thấy "unsatisfactory".
- **Siêu tham số:** không có trong bài; tác giả trỏ tới mã nguồn (§4).

**Bằng chứng mạnh nhất (mục/bảng/hình):**
- **Thiết kế thí nghiệm:** 9 biến thể kịch bản = N_a ∈ {2, 4, 8} × N_s ∈ {12, 24, 36}. Mỗi biến thể chạy 500 lần, tổng 4500 lần (§4, §5.2).
- **Tỉ lệ thành công:** mọi thuật toán ≥ 98% (§5.1, Fig. 1). Chỉ số này là trung bình gộp cả 9 biến thể.
- **Bảng 1, tổng quát hoá theo số UAV** (biến thể 4; hàng là số UAV khi huấn luyện, cột là khi triển khai):

  | Huấn luyện \ Triển khai | 2 | 4 | 8 |
  | --- | --- | --- | --- |
  | 2 | 100,00% | 96,53% | 98,93% |
  | 4 | 0,60% | 100,00% | 98,93% |
  | 8 | 0,00% | 0,00% | 99,93% |

  Mô hình gần như **sụp hoàn toàn khi triển khai với ít UAV hơn lúc huấn luyện**, còn khi nhiều UAV hơn thì vẫn giữ được (§5.1). Mọi số liệu khác của biến thể 4 dùng mô hình huấn luyện với 2 UAV.
- **Thời gian hoàn thành** (§5.2, Fig. 4): ba biến thể hợp tác nhanh hơn rõ rệt so với không hợp tác. Linh hoạt số cảm biến chỉ mất "insignificant loss" so với hợp tác. Linh hoạt số UAV chậm hơn linh hoạt số cảm biến khoảng 50%. Ngoài con số 50%, văn bản không cho số tuyệt đối.
- **Thời gian huấn luyện** (§5.3, Fig. 8):
  - Ngưỡng coi là "đã huấn luyện": tỉ lệ thành công ≥ 95% trên 200 lần đánh giá.
  - Một mô hình hợp tác mất khoảng 71 giờ, gần 10 lần mô hình không hợp tác. Biến thể hợp tác cần 9 mô hình.
  - Số bước huấn luyện: không hợp tác khoảng 700 000; hợp tác tổng cộng khoảng 80 000 000.
  - Linh hoạt số cảm biến cần 3 mô hình; linh hoạt số UAV cần 1 mô hình.
  - Tất cả chạy trên một máy RTX 3090 (§4).
- **Lợi ích biên giảm dần theo số UAV** (§5.2, Fig. 6i, Fig. 7): khoảng cách thời gian hoàn thành giữa 2 và 4 UAV lớn hơn nhiều so với giữa 4 và 8 UAV.

**Đánh giá trên kịch bản khác tập huấn luyện? Loại dịch chuyển nào?** **Một phần, chỉ theo số UAV** (Bảng 1).
- Vị trí cảm biến luôn ngẫu nhiên nên mọi lần đánh giá đều là bố trí mới, nhưng **cùng phân phối** với lúc huấn luyện (đều trên vùng 200 m × 200 m).
- Biến thể linh hoạt số cảm biến chỉ được đánh giá **trong** khoảng số cảm biến đã thấy khi huấn luyện (§3.4).
- **Những dịch chuyển bài không thử** (suy ra từ §2, §4):
  - không đổi kích thước vùng;
  - không đổi phân phối không gian của cảm biến (không có kịch bản phân cụm);
  - không đổi bán kính liên lạc;
  - không có năng lượng.

**Số seed / cách báo cáo độ bất định:**
- **Không báo số seed huấn luyện.** Mỗi cấu hình có vẻ chỉ có một lần huấn luyện; đây là suy luận từ cách đếm 9/3/1 mô hình ở §5.3, bài không nói thẳng.
- Kết quả là trung bình trên 500 lần đánh giá mỗi biến thể. **Không có CI, độ lệch chuẩn hay kiểm định thống kê**, kể cả khi bài viết "insignificant loss" (§5.2).
- Thời gian huấn luyện tính từ một lần chạy mỗi mô hình. Bài không thử lại để xem độ biến thiên.

**Đối chứng gần nhất và độ công bằng của so sánh:**
- Chỉ so sánh nội bộ giữa bốn biến thể MADDPG. **Không có heuristic** (TSP, tham lam) hay lời giải tối ưu, dù bài toán thăm một lần rất gần TSP/mTSP.
- So sánh "hợp tác vs không hợp tác" bị lẫn yếu tố: biến thể hợp tác đổi **đồng thời** quan sát (thêm UAV khác và định danh), số cảm biến quan sát (1 → N*_s) và hàm thưởng (PT (5) → PT (10)). Vì vậy không tách được phần lợi do "hợp tác" với phần lợi do thưởng có phạt thời gian. Đây là suy luận của DAT từ §3.2–§3.3, bài không thảo luận.
- So sánh "hợp tác vs linh hoạt số cảm biến" là cặp đối chứng sạch nhất: cùng quan sát và thưởng, chỉ khác việc ngẫu nhiên hoá N_s khi huấn luyện (§3.4). Nhưng kết luận dựa trên một lần huấn luyện mỗi mô hình.

**Giới hạn đã biết:**
1. **Không năng lượng, không mô hình kênh** (§2, §4, §6).
2. **Mục tiêu thu một lần**, không áp dụng trực tiếp cho thu định kỳ hay AoI (§1).
3. **Không báo seed, không CI** (§5); "insignificant" là nhận định định tính.
4. **Thiếu tham số để tái lập từ văn bản:** độ cao, giới hạn thời gian episode, min/max N_s, N*_s, N*_a và siêu tham số đều không có trong bài, chỉ có trong mã.
5. **Kênh vệ tinh toàn cục** cho mọi UAV (§2), do tác giả tự nêu.
6. **Phần tổng quan không trích Bayerlein et al.** Danh mục tham khảo [1]–[26] không có công trình này, dù đó là công trình DRL đa UAV đã làm tổng quát hoá theo số UAV và số cảm biến.

**Khác biệt với đề tài (điền thẳng vào ma trận docs/04 §5):**
- **Lamenza 2026:**
  - đa UAV (2–8), MADDPG, hành động liên tục;
  - mục tiêu thu một lần (thời gian hoàn thành);
  - không năng lượng;
  - ngẫu nhiên hoá vị trí cảm biến, và ở một biến thể là số cảm biến;
  - OOD chỉ theo số UAV;
  - không seed hay CI;
  - không heuristic.
- **Đề tài:**
  - một UAV;
  - AoI trung bình nhiều chu kỳ;
  - năng lượng đẩy theo tốc độ [Z19];
  - DR trên bố trí, mật độ và năng lượng;
  - 4 bộ OOD có cấu trúc;
  - ≥ 10 seed với CI;
  - đối chứng PPO-fixed, DQN và heuristic.
- **Điểm dùng được cho bài báo:**
  - Cặp "hợp tác vs linh hoạt số cảm biến" là bằng chứng độc lập (khác nhóm, khác thuật toán, khác bài toán) rằng ngẫu nhiên hoá một tham số kịch bản khi huấn luyện chỉ mất ít hiệu năng mà giảm số mô hình phải huấn luyện. Nó cùng hướng với lập luận của đề tài, nhưng **chưa có seed hay CI**, nên chỉ nên trích ở mức "reported".
  - Bảng 1 là ví dụ cụ thể về việc chính sách sụp khi dịch chuyển ra ngoài điều kiện huấn luyện. Nó ủng hộ việc đề tài đánh giá OOD có cấu trúc thay vì chỉ đánh giá trong phân phối.
  - §1 của bài tự phân biệt "single-cycle" với "multicycle (AoI)". Câu này hữu ích khi định vị: đề tài thuộc nhóm multicycle, khác bài này.

Hàng ma trận đề xuất (thay hàng hiện có):

| Công trình | Mục tiêu AoI | Năng lượng phụ thuộc tốc độ | Huấn luyện trên nhiều bố trí | Đánh giá OOD có cấu trúc | Nhiều seed + CI |
| --- | --- | --- | --- | --- | --- |
| Lamenza 2026 | Không (thu một lần, thời gian hoàn thành; §1) | Không (không mô hình năng lượng; tốc độ liên tục s ∈ [0, 15] nhưng không có chi phí; PT (7), §6) | Có (vị trí cảm biến ngẫu nhiên; biến thể "flexible sensor count" lấy N_s ngẫu nhiên; §3.4, §4) | Một phần (chỉ số UAV khi triển khai, sụp khi ít UAV hơn huấn luyện; Bảng 1) | Không (không báo seed; trung bình 500 lần đánh giá, không CI; §5) |

**Có mã nguồn/dữ liệu không:** Có: https://github.com/Project-GrADyS/gradys-data-collection/tree/journal (§4) và bản phát hành tag `journal` (Data Availability Statement). Trình mô phỏng GrADyS-SIM NextGen là mã mở (§4). Chưa kiểm tra mã có chạy được hay không.

**Một câu hỏi cho nhóm:** Khoá trích dẫn đang là `lamenza2025` nhưng bài xuất bản năm 2026 (tập 8). Nhóm có đổi khoá thành `lamenza2026` trong `docs/04` và `paper/references.bib` không? Khuyến nghị là đổi ngay khi chưa bài viết nào trích khoá này, để tránh ghi sai năm trong bài báo.
