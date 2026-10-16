# 01 — Đề cương nghiên cứu

**Tên (EN):** Generalizable AoI- and Energy-Aware UAV Trajectory Planning for IoT Data Collection via Domain-Randomized Proximal Policy Optimization
**Tên (VI):** Hoạch định quỹ đạo UAV thu thập dữ liệu IoT có khả năng tổng quát hoá, tối ưu tuổi thông tin và năng lượng bằng PPO với domain randomization
**Phiên bản:** 16/10/2026 · Trạng thái: bản khởi tạo, chờ giảng viên duyệt

---

## 1. Tóm tắt (≈150 từ, dùng làm nháp abstract)
Một UAV cánh quay thu dữ liệu định kỳ từ mạng cảm biến IoT không có hạ tầng mặt đất. Mục tiêu là giữ tuổi thông tin (AoI) thấp với ngân sách năng lượng giới hạn. Năng lượng đẩy phụ thuộc phi tuyến vào tốc độ, nên chính sách phải chọn cả hướng bay lẫn tốc độ. Bố trí và số lượng cảm biến thay đổi giữa các lần triển khai. Vì vậy chính sách học được phải hoạt động trên bố trí chưa thấy, không cần huấn luyện lại. Đề tài huấn luyện PPO với domain randomization trên bố trí, mật độ cảm biến và ngân sách năng lượng. Quan sát là bản đồ lưới căn tâm theo UAV, không phụ thuộc số cảm biến. Đánh giá dùng một tập ID và bốn bộ OOD có cấu trúc, ≥10 seed, khoảng tin cậy bootstrap và kiểm định có hiệu chỉnh đa so sánh. Đối chứng gồm PPO huấn luyện trên bố trí cố định, DQN và các heuristic TSP, tham lam theo AoI.

## 2. Bối cảnh & động lực
- UAV thu dữ liệu IoT là chủ đề dày đặc; DRL được dùng vì bài toán quỹ đạo–lập lịch phi lồi, NP-khó trong nhiều biến thể (xem `04` §1).
- Phần lớn công trình DRL tối ưu cho **một bộ tham số kịch bản** và phải huấn luyện lại khi kịch bản đổi. Bayerlein và cộng sự (2021) chỉ ra hạn chế này và đề xuất chính sách tổng quát hoá trên không gian tham số (`04`, [B21]).
- Ứng dụng gợi ý cho bối cảnh Việt Nam: giám sát môi trường, nông nghiệp, cảnh báo sớm ở vùng thiếu hạ tầng viễn thông. Đây chỉ là động lực, **không** dùng số liệu thực địa nào trong bài.

## 3. Định vị so với công trình gần nhất

| Khía cạnh | Bayerlein et al. 2021 [B21] | Đề tài này |
| --- | --- | --- |
| Mục tiêu | Tối đa **lượng dữ liệu** thu một lần (data harvesting) | Tối thiểu **AoI trung bình nhiều chu kỳ** + năng lượng |
| Năng lượng | Hằng số mỗi bước (giả định hover chiếm ưu thế) | Công suất đẩy **phụ thuộc tốc độ** (Zeng et al.), chính sách chọn tốc độ |
| Số UAV | 1–3 (MARL, DDQN) | 1 (mở rộng đa UAV ở bản tạp chí) |
| Môi trường | Bản đồ đô thị, ray-tracing che khuất | Vùng mở, kênh LoS (đơn giản hơn — giới hạn cần nêu) |
| Tổng quát hoá | Ngẫu nhiên tham số trong khoảng; có thử ngoại suy tham số | Domain randomization + **4 bộ OOD có cấu trúc** (phân bố không gian, mật độ, diện tích, năng lượng) |
| Thống kê | Trung bình Monte Carlo | ≥10 seed, CI bootstrap, IQM, kiểm định hiệu chỉnh Holm |
| Thuật toán | DDQN | PPO (+ DQN làm đối chứng) |

**Câu định vị dùng trong bài (nháp):** *"While parameter generalization has been shown for single-shot data harvesting [B21], it remains unclear whether such policies stay robust under structured distribution shifts when the objective is continual information freshness and the propulsion energy depends on speed."*
Câu này phải được kiểm chứng lại sau tổng quan hệ thống ở tuần 1–2 (gate G0, `05`).

## 4. Câu hỏi nghiên cứu
1. **RQ1 (tổng quát hoá):** Domain randomization có làm giảm độ suy giảm hiệu năng OOD của PPO so với huấn luyện trên một bố trí cố định không?
2. **RQ2 (đánh đổi):** Đường đánh đổi AoI–năng lượng thay đổi thế nào theo trọng số λ, và chính sách sử dụng hai mức tốc độ ra sao?
3. **RQ3 (so sánh):** Ở cùng ngân sách năng lượng, DR-PPO so với DQN và heuristic (TSP, tham lam AoI) thế nào trên ID và OOD?

## 5. Giả thuyết
- **H1 (kiểm định):** Độ suy giảm OOD (định nghĩa ở `03` §5) của DR-PPO nhỏ hơn PPO-fixed trên ít nhất 3/4 bộ OOD. H0: không khác biệt. Kiểm định hoán vị một phía, α = 0,05, hiệu chỉnh Holm trên 4 bộ.
- **H2 (kiểm định):** DR-PPO có AoI trung bình thấp hơn heuristic TSP trên bộ OOD-cluster. H0: không khác biệt.
- **H3 (thăm dò):** Quan sát dạng bản đồ căn tâm là điều kiện cần cho H1 (ablation: thay bằng vector có padding). Chỉ báo cáo mô tả, không tuyên bố ý nghĩa thống kê.

Ngưỡng "khác biệt có ý nghĩa thực tiễn" chưa được xác định — cần nhóm thống nhất **trước** khi chạy thực nghiệm chính (`03` §8).

## 6. Đóng góp dự kiến
- **C1.** Công thức MDP cho thu dữ liệu UAV tối ưu AoI với năng lượng phụ thuộc tốc độ, quan sát bản đồ căn tâm bất biến theo số cảm biến.
- **C2.** Giao thức đánh giá OOD có cấu trúc kèm phân tích thống kê, trả lời khi nào domain randomization thực sự giúp.
- **C3.** Môi trường mô phỏng mã nguồn mở (`src/uavaoi/`), có kiểm thử đơn vị và bộ seed cố định.

## 7. Phạm vi & giới hạn chấp nhận trước
- Chỉ mô phỏng; 2D, độ cao cố định; một UAV; kênh LoS không che khuất; không bay thực nghiệm.
- Không có ràng buộc quay về điểm sạc trong bản MVP (thêm ở bản đầy đủ nếu kịp).
- Kết quả nhân quả chỉ đúng trong mô phỏng; không ngoại suy trực tiếp sang triển khai thực tế.

## 8. Đầu ra
| Đầu ra | Phương án A (MVP 6 tuần) | Phương án B (đầy đủ 12 tuần) |
| --- | --- | --- |
| Bài báo | 6–8 trang (hội nghị trong nước, kỷ yếu ISBN/Springer) | 12–15 trang (Springer LNICST/LNNS, IEEE) |
| Thực nghiệm | ID + OOD-cluster + OOD-density; PPO-fixed, DR-PPO, TSP, tham lam; 10 seed | Đủ 4 bộ OOD, DQN, ablation H3, quét λ |
| Đồ án | Chương 1–3 + kết quả sơ bộ | Đồ án hoàn chỉnh |

Hội nghị đích **chưa chốt** — phụ thuộc quy định cộng điểm của trường (xem `07` §2).
