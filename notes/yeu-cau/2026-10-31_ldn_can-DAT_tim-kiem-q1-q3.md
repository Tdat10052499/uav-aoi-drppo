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
- (02/11 tối) LDN đọc lại trên `main` 7e3c752. Báo cáo G0 vẫn là bản c63ab0e, chưa có bản sửa. Ý 4 đã xong: FAO thêm cột 6 vào header `docs/04` §5 và điền 4 hàng của FAO (8b1b5a3). LDN điền 5 hàng của LDN qua PR. Ý 1–3 còn mở; G0-2 (Gong, Lu, Toure) và G0-6 (OH-DRL) chưa có cập nhật; 3 hàng DAT (Bayerlein, Zeng, Lamenza) chưa điền cột 6. Kết luận tiêu chí không đổi. LDN đọc lại sau khi DAT push bản sửa.

DAT: (02/11) Đã sửa báo cáo G0 theo ý 1–3: bỏ "tốc độ là biến quyết định" ở mục Trùng lặp và Đề xuất quyết định (G0-1); cột "Hiện trạng (02/11)", tóm tắt #2 "chưa kết luận được", 6 cột, bỏ nhánh "chưa có kết quả tìm kiếm", cập nhật hai gạch Yi 2020 và PRISMA (G0-3); thêm giải thích thay thế về từ khoá tốc độ/chuyển giao và Q4 (G0-5). Đã điền cột 6 cho 3 hàng DAT (Bayerlein: Không, §VI-B; Zeng: Không áp dụng; Lamenza: Một phần, §5.2). Ý 4 FAO đã làm (8b1b5a3). G0-2 (đọc Gong, Lu, Toure) và G0-6 (OH-DRL) vẫn chờ DAT có PDF.

## A7. (03/11) Đọc lại báo cáo G0 bản a656d71: còn 4 chỗ cần sửa trước họp 04/11
- LDN đọc lại `notes/2026-11-04_gate_G0_report.md` tại a656d71, trên `main` 851ed1f. G0-1 và G0-5 đã xử lý; G0-3 mới xử lý một phần. Chi tiết ở `notes/review_log.md`, dòng G0-7.
- Cần sửa:
  1. Bảng "Đối chiếu tiêu chí G0", hàng #1: tiêu đề cột đã đổi thành "Hiện trạng (02/11)" nhưng nội dung vẫn là bản cũ ("PRISMA còn số ≈", "Cột 6 mới chưa điền", "Chưa đạt (01/11)"). Cập nhật: PRISMA chốt 02/11; cột 6 đủ 12/12 hàng khi PR #40 merge; còn Gong, Lu, Toure và OH-DRL.
  2. Số bài: hàng #2 và dòng tóm tắt ghi "14 bài trong ma trận", nhưng `docs/04` §5 có **12 hàng** (không kể "Đề tài này").
  3. Bảng "Việc phải xong trước họp 04/11": dòng PRISMA vẫn ghi "thay số ≈" (đã xong); dòng cột 6 nên ghi trạng thái (FAO 4, DAT 3, LDN 5 qua PR #40).
  4. Quyết định 03/11 (FJCAI, DECISIONS trong PR #38) chưa vào báo cáo. Báo cáo vẫn ghi "Optuna TUNE (W4)", "Ngày quyết định tiếp theo: G1 15/11" và 163,2 M bước theo Phương án B. GVHD sẽ đọc thấy kế hoạch cũ. Đề xuất: thêm một dòng nêu kế hoạch FJCAI, PREREG khoá 04/11 và điều kiện EXP-02b, hoặc ghi rằng phần tính toán được thay bằng `docs/PREREG.md`.
  5. (bổ sung 03/11 chiều) LDN đã duyệt sàng lọc (`search_log_LDN.md` §7). Có 2 thay đổi cần đưa vào báo cáo:
     - Số giữ lại là **58** (A 10, B 13, C 35), loại ở bước tóm tắt **29**. Báo cáo đang ghi 57 (A 9, B 12, C 36).
     - **A10 Liu et al. 2025 (IEEE TVT)**, trước đây là C1, có AoI, năng lượng UAV và nêu "transferability" trên kịch bản tổng hợp và thành phố thật. Nên thêm vào mục "Giải thích thay thế" và "Trùng lặp" như một rủi ro còn mở cho tiêu chí #2, cạnh Gong 2024. LDN đề xuất tự đọc A10; DAT có thể đổi người đọc.
     - **Cập nhật 03/11, 17:30: LDN đã đọc toàn văn A10** (`notes/reading/liu2025resource_LDN.md`, bản thảo đã chấp nhận trên Aaltodoc). Chữ "transferability" chỉ là một câu khẳng định ở §VII-A3; bài không có thí nghiệm huấn luyện ở một kịch bản rồi đánh giá ở kịch bản khác mà không huấn luyện lại. Tốc độ cố định 16,67 m/s. Hàng ma trận: Có / Không / Không rõ / Không / Không / Không. **A10 không phải rủi ro cho tiêu chí #2**; báo cáo chỉ cần ghi đã đọc, không cần thêm vào mục "Trùng lặp".
- Còn mở, không do báo cáo: G0-2 (Gong, Lu, Toure chưa có Form B; hạn 03/11) và G0-6 (OH-DRL).
- Kết luận của LDN không đổi: #1 **chưa đạt**; #2 **chưa kết luận được**; #3 chờ GVHD. Theo đề xuất trong báo cáo, buổi họp 04/11 rơi vào nhánh "tiếp tục có điều kiện".
- **Hạn:** trước họp 04/11.

