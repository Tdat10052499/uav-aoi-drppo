# LDN → DAT: kết quả tìm kiếm Q1–Q3 và các thay đổi giao thức — 31/10/2026

> Trả lời bằng dòng `DAT:` dưới mục. Quy ước: `notes/yeu-cau/README.md` (PR #28).
> Kết quả: `notes/reading/search_log_LDN.md`, danh sách đọc: `notes/reading/fulltext_list.md` (cả hai đang là nháp chờ LDN duyệt). Trả lời mục A2 trong `2026-10-26_dat_can-LDN_second-reader-bayerlein.md`.

## A1. Không truy cập được IEEE Xplore và Scopus; đề xuất thay bằng OpenAlex
- Dữ kiện (31/10): IEEE Xplore hiện trang lỗi trên máy LDN, kể cả trang chủ và khi không đăng nhập. Trường không đăng ký Scopus; tài khoản cá nhân của LDN chỉ có Scopus Preview (không tìm kiếm tài liệu).
- Đã làm: chạy Q1–Q3 trên arXiv, Google Scholar và **OpenAlex** (chỉ mục mở, tìm trong tiêu đề + tóm tắt, phủ bài IEEE và Elsevier).
- Cần DAT: đồng ý thay IEEE Xplore và Scopus bằng OpenAlex, và ghi vào `docs/DECISIONS.md`. Hoặc nếu DAT/GVHD vào được IEEE Xplore hay Scopus, chạy lại Q1–Q3 (chuỗi sẵn ở search_log §2) và gửi số.
- Để làm gì: số PRISMA cho tiêu chí G0 số 1 và chương 2.
- Hạn mong muốn: T2 02/11.

DAT: (01/11) Đồng ý dùng OpenAlex thay IEEE Xplore và Scopus, ghi trong DECISIONS 2026-11-01. Lưu ý: tìm `title_and_abstract` trên OpenAlex có thể sót bài thiếu tóm tắt trong chỉ mục (hiểu biết chung, chưa kiểm), nên DAT sẽ thử IEEE Xplore một lần từ mạng của DAT; nếu vào được, DAT chạy 3 chuỗi ở search_log §2 và gửi số. Trước khi đánh dấu W1-LDN-04/05 xong: thay các số "≈" trong PRISMA (§4) bằng số chính xác, vì chương 2 cần số đếm được.

## A2. Hai điều chỉnh khác so với `docs/04` §6
- (a) arXiv API và OpenAlex không mở rộng `generaliz*`; đã thay bằng các dạng viết đầy đủ. Đã kiểm: với `generaliz*`, arXiv Q1 chỉ ra 5 bài thay vì 13.
- (b) Lọc chuyên mục arXiv (cs.NI, cs.LG, eess.SP) làm mất 2 bài liên quan trực tiếp (2311.06742 ở cs.IT, 2502.01268 ở cs.RO). LDN đề xuất **bỏ bộ lọc chuyên mục**; search_log ghi cả hai số.
- (c) Google Scholar chỉ sàng lọc 100 kết quả đầu mỗi truy vấn (Q1 khoảng 2 830, Q2 khoảng 1 580, Q3 khoảng 274 kết quả).
- Cần DAT: đồng ý (a)–(c) hoặc nêu cách khác. Hạn: T2 02/11.

DAT: (01/11) Đồng ý (a), (b), (c). Với (a) LDN đã kiểm (5 so với 13 bài). Với (b), search_log ghi cả hai số; dùng cột "mọi chuyên mục" cho PRISMA. Với (c), ghi giới hạn "100 kết quả đầu mỗi truy vấn" trong chương 2. Ghi trong DECISIONS 2026-11-01.

## A3. Rủi ro định vị: các bài có thể đủ nhiều cột của ma trận
- Đọc tóm tắt (chưa đọc toàn văn), 9 bài nhóm A có AoI hoặc năng lượng UAV **và** có tổng quát hoá. Đáng chú ý nhất:
  - **Gong et al. 2024 (IEEE IoT-J):** AoI + năng lượng, tối ưu cả vận tốc bay của UAV, đánh giá trên môi trường chưa thấy. Có thể chạm cả 4 cột đầu của ma trận.
  - **Lu et al. 2025 (IEEE WCL):** AoI dưới ràng buộc năng lượng, số người dùng thay đổi, thích nghi kịch bản mới.
  - **Yi et al. 2023 (arXiv 2311.06742):** AoI + năng lượng UAV, meta-RL để tổng quát hoá.
- Cần DAT: biết trước để chuẩn bị câu định vị bản 2; nếu toàn văn cho thấy một bài đủ 5 cột thì áp dụng nhánh "không đạt" của tiêu chí G0 số 2.
- Hạn: trước họp G0 04/11.

DAT: (01/11) Đã nắm. Gong 2024 (A1) là bài DAT đọc đầu tiên, trước 03/11. Nếu toàn văn cho thấy đủ 5 cột thì báo cáo G0 áp dụng nhánh "không đạt" của tiêu chí 2.

## A5. (bổ sung 31/10 tối) Yi 2023 đã có cột "năng lượng phụ thuộc tốc độ" và "huấn luyện nhiều bố trí"
- Dữ kiện, từ toàn văn arXiv:2311.06742 (`notes/reading/yi2023meta_LDN.md`): AoI + năng lượng UAV trong mục tiêu (PT (15a)); công suất đẩy phụ thuộc tốc độ và gia tốc (PT (9)–(10)); **tốc độ và hướng là hành động liên tục** (§IV-A2); trạng thái chứa vị trí tương đối tới mọi cảm biến (§IV-A1); meta-training MAML trên nhiều nhiệm vụ khác số và vị trí cảm biến (§IV-B2).
- Bài **không** có: đánh giá không huấn luyện lại (Fig. 8 đo tốc độ thích nghi khi huấn luyện tiếp), dịch chuyển có cấu trúc, đối chứng huấn luyện trên bố trí cố định, nhiều seed + CI.
- Hệ quả: ma trận Yi 2023 = Có, Có, Có, Một phần, Không. Chưa có bài nào đủ 5 cột, nhưng **"năng lượng phụ thuộc tốc độ, tốc độ là hành động" và "huấn luyện nhiều bố trí" không còn là điểm mới**. Khác biệt còn đứng được nằm ở cách đánh giá: không huấn luyện lại, 4 dịch chuyển có cấu trúc, đối chứng Fixed, 10 seed + CI.
- Cần DAT: cân nhắc viết lại câu định vị bản 2 theo hướng này; cân nhắc thay cột "năng lượng phụ thuộc tốc độ" trong ma trận bằng cột "có đối chứng huấn luyện trên bố trí cố định". Tra ngược từ Yi 2023 thêm 5 bài về điều khiển tốc độ/chuyển giao (`fulltext_list.md`, mục "Tra ngược"), cần phân công sàng lọc.
- Hạn: trước họp G0 04/11.

DAT: (01/11) Đồng ý với đánh giá ma trận Yi 2023 và hướng câu định vị bản 2 (điểm mới nằm ở cách đánh giá). **Không** thay cột "năng lượng phụ thuộc tốc độ": bỏ một cột vì đối thủ đạt cột đó là đổi tiêu chí sau khi thấy kết quả, phản biện sẽ nhận ra. Thay vào đó, **thêm** cột thứ 6 "Đối chứng huấn luyện trên bố trí cố định" (DECISIONS 2026-11-01). Mỗi người đọc điền cột mới cho các hàng của mình, có mục/bảng, trước T3 03/11. Tra ngược từ Yi 2023: LDN sàng lọc tóm tắt, sau G0.

## A4. Chia đọc toàn văn và mức đọc
- Đề xuất ở `fulltext_list.md`: nhóm A (DAT 5 bài, LDN 5 bài kể cả Yi 2020) đọc toàn văn + Form B **trước T3 03/11**; nhóm B (12) và C (36) chỉ đọc mục mô hình + thực nghiệm để điền hàng ma trận rút gọn, hạn T6 13/11.
- Bài chỉ có trên IEEE (A4 Chen–Hanzo, A6 Xiao, A7 Zhou): nhóm không vào được IEEE Xplore, cần thử bản tác giả hoặc nhờ GVHD/thư viện.
- Cần DAT: đồng ý cách chia và mức đọc, hoặc sửa. Hạn: T2 02/11 sáng, để kịp đọc nhóm A.

DAT: (01/11) Đồng ý nhóm A (trước T3 03/11) và nhóm B (trước T6 13/11) như đề xuất. Nhóm C lùi hạn sang **CN 30/11**: nhóm này chủ yếu để kiểm cột tốc độ, mà Yi 2023 đã cho thấy cột đó không còn là điểm mới; tuần 02–13/11 DAT còn chạy EXP-02 và TUNE trên đường tới G1. Bài chỉ có trên IEEE (A4, A7) và OH-DRL: DAT nhờ GVHD hoặc thư viện. Ghi trong DECISIONS 2026-11-01.

## A6. (02/11) Second reader báo cáo G0 (W2-LDN-03): yêu cầu sửa
- LDN đã đọc `notes/2026-11-04_gate_G0_report.md` (bản cập nhật 01/11, commit c63ab0e) và kiểm lại ma trận `docs/04` §5. Phản biện ở `notes/review_log.md`, dòng G0-1 … G0-6. Bản 01/11 đã xử lý phần lớn: câu định vị bản 2, OpenAlex, cột 6, thứ tự đọc Gong 2024.
- Còn phải sửa trong báo cáo trước họp 04/11:
  1. Xoá hai chỗ còn nêu "tốc độ là biến quyết định" như điểm khác biệt (G0-1), cho khớp câu bản 2.
  2. Cập nhật các dòng cũ: cột "Hiện trạng (30/10)", tóm tắt "#2 ĐẠT TẠM (chỉ trong 9 công trình)", "5 cột" thành 6 cột, nhánh "chưa có kết quả tìm kiếm", hai gạch về Yi 2020 và PRISMA ở mục "Cần nói rõ" (G0-3).
  3. Thêm vào "Giải thích thay thế": Q1–Q3 thiếu từ khoá tốc độ/chuyển giao, tra ngược đã ra 5 bài bị sót (G0-5).
  4. Thêm cột 6 vào header bảng `docs/04` §5 để mọi người điền (G0-4).
- Kết luận hiện tại của LDN về tiêu chí: #1 **chưa đạt** (nhóm A phần DAT chưa đọc; OH-DRL ◐; cột 6 chưa điền); #2 **chưa kết luận được** (12 bài đã đọc chưa bài nào đủ; cao nhất Yi 2023; Gong 2024 chưa đọc); #3 chờ GVHD.
- PRISMA đã chốt (bỏ "≈") ở `search_log_LDN.md` §4, theo yêu cầu của DAT dưới A1.
- Hạn: T3 03/11. LDN đọc lại bản sửa trong ngày 03/11.
