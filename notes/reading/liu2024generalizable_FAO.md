# Form B — `liu2024generalizable`

> Trạng thái: soạn từ toàn văn PDF (arXiv v1). FAO rà lại trước khi đánh dấu W2-FAO-01 xong; second reader: LDN.

**Tiêu đề / tác giả / năm / nơi công bố hoặc trạng thái preprint:** *Learning Generalizable Policy for Obstacle-Aware Autonomous Drone Racing*. Yueqian Liu (MAVLab, TU Delft; bài là một phần luận văn thạc sĩ), 2024. Preprint arXiv:2411.04246v1 [cs.RO], 06/11/2024. PDF không ghi nơi công bố chính thức ✱.

**URL nguồn gốc và phiên bản/ngày truy cập:** https://arxiv.org/abs/2411.04246 (v1), truy cập ngày 20/10/2026.

**Người đọc (NICK):** FAO

**Bài báo trả lời câu hỏi gì:** Bài hỏi liệu có thể huấn luyện **một** chính sách duy nhất, không cần tinh chỉnh sau huấn luyện, bay qua nhiều đường đua có chướng ngại chưa từng thấy, bằng cách ngẫu nhiên hoá (domain randomization) đường đua và chướng ngại hay không (§I).

**Giả định hệ thống:** Đây không phải bài toán truyền thông.
- **Drone:** một quadrotor với động lực học thân cứng, mô hình rotor bậc nhất và lực cản (PT (1)–(3)).
- **Hành động:** liên tục, 4 kênh (3 tốc độ góc và lực đẩy), đi qua bộ điều khiển kiểu Betaflight (§III-B).
- **Quan sát:** ảnh độ sâu 270 × 480, trạng thái 18 chiều và thông tin 2 waypoint kế tiếp (PT (9)–(11)). Quan sát được giả định không nhiễu (§III-B5).
- **Phần thưởng:** tổ hợp 8 thành phần (PT (5)–(8)).
- **Không có:** AoI, mô hình năng lượng.

**Cơ chế, diễn đạt bằng lời của mình:**
- **Thuật toán:** PPO (RL-Games). Encoder ảnh DCE được huấn luyện trước rồi đóng băng, nối với một MLP (§III-B6).
- **Domain randomization gồm bốn phần:**
  1. Bộ sinh waypoint ngẫu nhiên, tham số hoá tư thế tương đối giữa hai waypoint bằng 5 bậc tự do (PT (13)); bộ quản lý chướng ngại đặt chướng ngại neo theo đường đua (Fig. 3).
  2. Huấn luyện trên đoạn ngắn 4 waypoint thay vì đường đua đầy đủ (§III-C2).
  3. **Sinh lại một bộ môi trường ngẫu nhiên mới cho mỗi rollout**, với 512 môi trường song song (§III-C3, §III-D).
  4. Ngẫu nhiên hoá trạng thái đầu và tư thế camera (§III-C4).
- **Chi phí huấn luyện:** 1000 vòng lặp, khoảng 520 triệu bước trên 512 000 môi trường khác nhau, khoảng 50 giờ trên i9-13900K + RTX 4090 (§III-D).

**Bằng chứng mạnh nhất (mục/bảng/hình):**
- **Fig. 10 (§IV-B):** 4 mức độ khó, mỗi mức gồm 100 đường đua ngẫu nhiên × 10 episode. Tỉ lệ thành công khoảng 0,9 ở mức 1 (giống huấn luyện) và giảm còn khoảng 0,4 ở mức 4.
- **Fig. 6 (§IV-A):** 4 đường đua thiết kế tay, 100 episode mỗi đường. Thành công 98% ở "Kebab" (giống huấn luyện), rồi 55%, 37% và 26% khi đường đua khác dần.
- **Fig. 11 (§IV-C):** trên các đường đua khó, tỉ lệ thành công dưới 0,01.

**Đánh giá trên kịch bản khác tập huấn luyện? Loại dịch chuyển nào?** Có, và có cấu trúc (§IV-A, §IV-B). Các loại dịch chuyển gồm:
- hình học đường đua: số waypoint, tư thế tương đối giữa các waypoint;
- số lượng và kiểu chướng ngại:
  - mức 2 gấp đôi số chướng ngại;
  - mức 3 thêm 60 chướng ngại quay quanh waypoint;
  - mức 4 nới rộng biên tham số waypoint;
- phạm vi trạng thái đầu rộng hơn khi huấn luyện.

Hiệu năng giảm đơn điệu khi môi trường lệch xa phân phối huấn luyện.

**Số seed / cách báo cáo độ bất định:**
- Bài chỉ báo cáo một chính sách. Không nêu số seed huấn luyện và không có CI.
- Biến thiên chỉ được thể hiện ở mức episode (100 hoặc 1000 episode mỗi điều kiện) (§IV).

**Đối chứng gần nhất và độ công bằng của so sánh:** **Không có đối chứng nào.**
- Không so với chính sách huấn luyện trên môi trường cố định, cũng không so với planner hay phương pháp tối ưu hoá.
- §III-C3 khẳng định rằng dùng một bộ môi trường ngẫu nhiên cố định khiến chính sách học "chiến lược trung bình", nhưng bài không có ablation để chứng minh.

**Giới hạn đã biết:**
- Tác giả thừa nhận chính sách chỉ tổng quát hoá tốt khi môi trường gần phân phối huấn luyện, và thất bại trên đường đua khó (§IV-C, §V).
- Chỉ có mô phỏng, quan sát không nhiễu.
- Một seed, không ablation.

**Khác biệt với đề tài (điền thẳng vào ma trận docs/04 §5):**
- **Phạm vi:** miền khác hẳn (điều khiển bay mức thấp, không AoI, không năng lượng). Theo tiêu chí loại ở docs/04 §6, bài nằm ngoài tổng quan hệ thống và chỉ dùng làm tài liệu tham khảo cho phương pháp DR.
- **Điểm giống:** PPO + DR, với môi trường mới ở mỗi reset hoặc rollout, và đánh giá theo mức lệch phân phối.
- **Phần đề tài làm mà bài thiếu:** so DR với Fixed, nhiều seed + CI.
- **Lưu ý:** kết quả "hiệu năng giảm theo độ lệch phân phối" là một kịch bản phải chuẩn bị. DR-PPO của ta cũng có thể chỉ tốt trong phân phối huấn luyện (cùng nhận định với `robustquad2021`).

Hàng ma trận đề xuất:

| Công trình | Mục tiêu AoI | Năng lượng phụ thuộc tốc độ | Huấn luyện trên nhiều bố trí | Đánh giá OOD có cấu trúc | Nhiều seed + CI |
| --- | --- | --- | --- | --- | --- |
| Liu 2024 (tham khảo DR, ngoài phạm vi) | Không (đua drone) | Không | Có (môi trường mới mỗi rollout) | Có (4 mức khó + 4 đường đua thiết kế tay) | Không (1 chính sách, không seed/CI) |

**Có mã nguồn/dữ liệu không:** Có: https://github.com/ErcBunny/IsaacGymEnvs (theo tóm tắt). Chưa kiểm tra nội dung repo.

**Một câu hỏi cho nhóm:** Liu cho rằng một pool môi trường ngẫu nhiên cố định dẫn tới "chiến lược trung bình", nhưng không kiểm chứng. Có nên thêm một ablation trung gian giữa Fixed và DR, ví dụ một pool cố định K bố trí, để kiểm tra điều này trong bài toán của ta không? Đây chỉ là đề xuất; nếu làm thì phải khoá trước G1.
