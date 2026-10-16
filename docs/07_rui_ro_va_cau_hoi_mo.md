# 07 — Rủi ro & câu hỏi mở

## 1. Rủi ro
| Rủi ro | Khả năng | Tác động | Giảm thiểu |
| --- | --- | --- | --- |
| Tính mới bị đánh giá thấp vì [B21] đã tổng quát hoá theo tham số | Cao | Cao | Định vị hẹp và chính xác (`01` §3); gate G0; nhấn mạnh AoI + tốc độ + OOD có cấu trúc + thống kê |
| PPO không vượt được heuristic TSP (heuristic có thông tin đầy đủ) | Trung bình | Trung bình | Kết quả âm vẫn có giá trị nếu trình bày trung thực; tập trung RQ1 (DR vs fixed) thay vì "thắng heuristic" |
| Huấn luyện không hội tụ hoặc nhạy siêu tham số | Trung bình | Cao | Bắt đầu từ cấu hình SB3 chuẩn; curriculum từ N nhỏ; Optuna trên ID |
| Reward hacking (cạn pin sớm, hover vô ích, chạm biên) | Trung bình | Cao | Phạt dừng sớm có cận dưới (đã kiểm thử); action mask; trực quan hoá quỹ đạo hằng tuần |
| Thiếu tài nguyên tính toán cho 10 seed × nhiều phương pháp | Trung bình | Trung bình | Đo ở tuần 2–3; giảm số bước trước, giữ ≥5 seed |
| `train_ppo.py` có lỗi API (chưa chạy được khi dựng bộ mã) | Trung bình | Thấp | Chạy thử 10k bước ngay tuần 1 |
| Lỡ hạn hội nghị | Phụ thuộc lựa chọn | Cao | Chọn phương án A/B tại G1 theo hạn đã xác nhận |
| Tham số "nhẹ" hoặc hệ số LoS dùng sai nguồn | Thấp | Trung bình | Chỉ dùng bộ tham số đã đối chiếu làm mặc định; xử lý hết mục `[cần kiểm tra]` |

## 2. Câu hỏi cần giảng viên trả lời (ảnh hưởng trực tiếp đến kế hoạch)
- [ ] **Quy định cộng điểm:** cần *thư chấp nhận* hay bài *đã xuất bản*? Kỷ yếu trong nước có ISBN có được tính, hay bắt buộc Scopus/IEEE/Springer?
- [ ] **Mốc 18–19/01/2027:** là hạn chốt hồ sơ, ngày bảo vệ, hay ngày bắt đầu nhận đề tài?
- [ ] **Nhóm:** số thành viên, trình độ, kinh nghiệm Python/RL?
- [ ] **Tính toán:** máy có GPU nào; có cụm tính toán của trường không?
- [ ] **Đầu ra:** chỉ bài hội nghị, hay thêm bản mở rộng tạp chí (đa UAV)?
- [ ] **Bay thực nghiệm:** có yêu cầu không? Nếu có, cần thêm kế hoạch an toàn bay và giấy phép, và phạm vi sẽ thay đổi lớn.

## 3. Việc cần xác minh (tồn đọng)
- [ ] Hạn nộp FJCAI 2027 và ICISN 2027: hỏi qua fisu.vietnam@gmail.com (địa chỉ trên CFP FJCAI 2026) và icisnconf@gmail.com.
- [ ] Bộ tham số "light" của [Z19] so với bản IEEE TWC chính thức.
- [ ] Hệ số mô hình LoS của Al-Hourani (2014) nếu dùng mở rộng kênh.
- [ ] Toàn văn Lamenza et al. (2025) và Yi et al. (2020) để điền ma trận định vị.
- [ ] Thông tin xuất bản các mục `VERIFY` trong `references.bib`.
