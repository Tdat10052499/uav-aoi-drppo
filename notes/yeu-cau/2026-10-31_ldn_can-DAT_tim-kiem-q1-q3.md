# LDN → DAT: kết quả tìm kiếm Q1–Q3 và các thay đổi giao thức — 31/10/2026

> Trả lời bằng dòng `DAT:` dưới mục. Quy ước: `notes/yeu-cau/README.md` (PR #28).
> Kết quả: `notes/reading/search_log_LDN.md`, danh sách đọc: `notes/reading/fulltext_list.md` (cả hai đang là nháp chờ LDN duyệt). Trả lời mục A2 trong `2026-10-26_dat_can-LDN_second-reader-bayerlein.md`.

## A1. Không truy cập được IEEE Xplore và Scopus; đề xuất thay bằng OpenAlex
- Dữ kiện (31/10): IEEE Xplore hiện trang lỗi trên máy LDN, kể cả trang chủ và khi không đăng nhập. Trường không đăng ký Scopus; tài khoản cá nhân của LDN chỉ có Scopus Preview (không tìm kiếm tài liệu).
- Đã làm: chạy Q1–Q3 trên arXiv, Google Scholar và **OpenAlex** (chỉ mục mở, tìm trong tiêu đề + tóm tắt, phủ bài IEEE và Elsevier).
- Cần DAT: đồng ý thay IEEE Xplore và Scopus bằng OpenAlex, và ghi vào `docs/DECISIONS.md`. Hoặc nếu DAT/GVHD vào được IEEE Xplore hay Scopus, chạy lại Q1–Q3 (chuỗi sẵn ở search_log §2) và gửi số.
- Để làm gì: số PRISMA cho tiêu chí G0 số 1 và chương 2.
- Hạn mong muốn: T2 02/11.

## A2. Hai điều chỉnh khác so với `docs/04` §6
- (a) arXiv API và OpenAlex không mở rộng `generaliz*`; đã thay bằng các dạng viết đầy đủ. Đã kiểm: với `generaliz*`, arXiv Q1 chỉ ra 5 bài thay vì 13.
- (b) Lọc chuyên mục arXiv (cs.NI, cs.LG, eess.SP) làm mất 2 bài liên quan trực tiếp (2311.06742 ở cs.IT, 2502.01268 ở cs.RO). LDN đề xuất **bỏ bộ lọc chuyên mục**; search_log ghi cả hai số.
- (c) Google Scholar chỉ sàng lọc 100 kết quả đầu mỗi truy vấn (Q1 khoảng 2 830, Q2 khoảng 1 580, Q3 khoảng 274 kết quả).
- Cần DAT: đồng ý (a)–(c) hoặc nêu cách khác. Hạn: T2 02/11.

## A3. Rủi ro định vị: các bài có thể đủ nhiều cột của ma trận
- Đọc tóm tắt (chưa đọc toàn văn), 9 bài nhóm A có AoI hoặc năng lượng UAV **và** có tổng quát hoá. Đáng chú ý nhất:
  - **Gong et al. 2024 (IEEE IoT-J):** AoI + năng lượng, tối ưu cả vận tốc bay của UAV, đánh giá trên môi trường chưa thấy. Có thể chạm cả 4 cột đầu của ma trận.
  - **Lu et al. 2025 (IEEE WCL):** AoI dưới ràng buộc năng lượng, số người dùng thay đổi, thích nghi kịch bản mới.
  - **Yi et al. 2023 (arXiv 2311.06742):** AoI + năng lượng UAV, meta-RL để tổng quát hoá.
- Cần DAT: biết trước để chuẩn bị câu định vị bản 2; nếu toàn văn cho thấy một bài đủ 5 cột thì áp dụng nhánh "không đạt" của tiêu chí G0 số 2.
- Hạn: trước họp G0 04/11.

## A4. Chia đọc toàn văn và mức đọc
- Đề xuất ở `fulltext_list.md`: nhóm A (DAT 5 bài, LDN 5 bài kể cả Yi 2020) đọc toàn văn + Form B **trước T3 03/11**; nhóm B (12) và C (36) chỉ đọc mục mô hình + thực nghiệm để điền hàng ma trận rút gọn, hạn T6 13/11.
- Bài chỉ có trên IEEE (A4 Chen–Hanzo, A6 Xiao, A7 Zhou): nhóm không vào được IEEE Xplore, cần thử bản tác giả hoặc nhờ GVHD/thư viện.
- Cần DAT: đồng ý cách chia và mức đọc, hoặc sửa. Hạn: T2 02/11 sáng, để kịp đọc nhóm A.
