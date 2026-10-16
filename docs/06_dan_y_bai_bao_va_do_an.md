# 06 — Dàn ý bài báo & đồ án

## 1. Dàn ý bài báo (Springer LNICST/LNNS; IEEE 2 cột thì co lại theo tỷ lệ)

| Mục | Nội dung | Full 12–15 tr. | Short 6–8 tr. |
| --- | --- | --- | --- |
| Abstract | Bài toán, khoảng trống (tổng quát hoá dưới dịch chuyển có cấu trúc với mục tiêu AoI + năng lượng theo tốc độ), phương pháp, kết quả chính kèm số và CI | 150–200 từ | 150 từ |
| 1. Introduction | Động lực; giới hạn "một kịch bản một lần huấn luyện"; [B21] đã làm gì, chưa làm gì; RQ; 3 đóng góp | 1,5 | 1 |
| 2. Related Work | DRL thu dữ liệu UAV; AoI–DRL; tổng quát hoá (DR, meta-RL, bản đồ căn tâm); bảng định vị (`04` §5) | 1,5 | 0,75 |
| 3. System Model & Problem | Kịch bản, năng lượng [Z19], kênh, AoI, bài toán tối ưu | 2 | 1,25 |
| 4. MDP & DR-PPO | Quan sát căn tâm, 17 hành động, thưởng, chống dừng sớm, phân phối DR, mạng CNN | 2 | 1,25 |
| 5. Experimental Setup | Đối chứng, bộ ID/OOD, seed, ngân sách, thống kê, tham số | 1,5 | 1 |
| 6. Results | RQ1 (H1), RQ3 (H2), RQ2 (λ), ablation, quỹ đạo minh hoạ | 3 | 1,5 |
| 7. Discussion & Limitations | Khi nào DR giúp và không giúp; mô phỏng LoS/2D; một UAV | 0,75 | 0,5 |
| 8. Conclusion | Tóm tắt + hướng mở rộng đa UAV | 0,5 | 0,25 |

### Hình & bảng dự kiến
| Mã | Nội dung | Dạng |
| --- | --- | --- |
| F1 | Sơ đồ hệ thống: vùng, cảm biến, bán kính thu, UAV, hai mức tốc độ | Sơ đồ (vẽ tay, **không** dùng ảnh do AI tạo — chính sách Springer) |
| F2 | Quan sát 5 kênh căn tâm → CNN → actor/critic | Sơ đồ kiến trúc |
| F3 | Đường học (trung bình ± 95% CI theo seed) DR-PPO vs Fixed-PPO | Đường |
| F4 | Độ suy giảm OOD theo bộ, có CI, đánh dấu ý nghĩa sau Holm | Cột nhóm + thanh sai số |
| F5 | Đánh đổi AoI–năng lượng theo λ | Điểm + thanh sai số hai chiều |
| F6 | Quỹ đạo minh hoạ: TSP vs DR-PPO trên cùng kịch bản OOD-cluster | Bản đồ quỹ đạo |
| T1 | Tham số mô phỏng (từ `02` §2, §7) có cột nguồn | Bảng |
| T2 | Kết quả chính: Ā, peak AoI, năng lượng, tỷ lệ hết pin — 6 phương pháp × 5 bộ | Bảng |
| T3 | Ablation A2–A5 | Bảng |

Mọi hình phải có alt text (yêu cầu EAI/Springer). Nếu dùng LLM ngoài mục đích chỉnh sửa văn phong, khai báo trong phần Acknowledgements.

## 2. Dàn ý đồ án tốt nghiệp (ánh xạ từ bài báo)
| Chương | Nội dung | Nguồn trong Project |
| --- | --- | --- |
| Mở đầu | Lý do chọn đề tài, mục tiêu, phạm vi, đóng góp | `01` |
| 1. Cơ sở lý thuyết | UAV trong IoT; AoI; MDP; RL → DRL; PPO; domain randomization | `04` §4, tài liệu nền |
| 2. Tổng quan nghiên cứu | Tổng quan hệ thống (PRISMA rút gọn), ma trận định vị, khoảng trống | `04` |
| 3. Mô hình hệ thống & phương pháp đề xuất | Mô hình năng lượng, kênh, MDP, thiết kế thưởng, kiến trúc mạng | `02` |
| 4. Thực nghiệm & đánh giá | Thiết lập, kết quả RQ1–RQ3, ablation, thảo luận | `03`, `results/` |
| 5. Kết luận & hướng phát triển | Tóm tắt, giới hạn, mở rộng đa UAV / kênh che khuất / bay thực nghiệm | `01` §7 |
| Phụ lục | Hướng dẫn chạy mã, cấu hình, bảng tham số đầy đủ, kết quả theo từng seed | `code/README.md` |

Đồ án được phép chi tiết hơn bài báo: trình bày đầy đủ kiểm thử đơn vị, toàn bộ kết quả từng seed và các thử nghiệm thất bại (có giá trị phương pháp luận).

## 3. Danh sách kiểm tra trước khi nộp bài
- [ ] Ẩn danh hoàn toàn (tên, đơn vị, đường dẫn GitHub, metadata PDF)
- [ ] Đúng template và giới hạn trang của hội nghị đã chọn
- [ ] Mọi số liệu tham số có nguồn (T1); mọi giá trị "thiết kế" được ghi rõ là lựa chọn của tác giả
- [ ] Mọi kết quả chính: ≥10 seed (hoặc ghi rõ số seed nếu ít hơn), 95% CI, kiểm định đã hiệu chỉnh
- [ ] Câu định vị so với [B21] chính xác, không tuyên bố "đầu tiên" khi chưa kiểm chứng
- [ ] Phân biệt kết quả kiểm định (H1, H2) với kết quả thăm dò (H3)
- [ ] Mục giới hạn: mô phỏng, LoS, 2D, một UAV
- [ ] Mã nguồn và seed sẵn sàng công bố khi camera-ready
- [ ] Mục `[cần kiểm tra]` trong `02` và `VERIFY` trong `references.bib` đã xử lý hết
