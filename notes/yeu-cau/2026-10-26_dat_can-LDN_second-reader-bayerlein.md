# DAT → LDN: second reader Form B Bayerlein 2021 — 26/10/2026

> Trả lời bằng dòng `LDN:` dưới mục. Quy ước: `notes/yeu-cau/README.md` (PR #28).

## A1. Đọc phản biện Form B `notes/reading/bayerlein2021multi_DAT.md` (W1-DAT-02, second reader LDN)
- Cần LDN: kiểm từng nhận định có đúng mục/PT/bảng trong toàn văn arXiv:2010.12461v3 không, nhất là hàng ma trận `docs/04` §5 và mục "Đối chứng gần nhất" (bài không có đối chứng huấn luyện trên kịch bản cố định, §VI-B; 1 lần huấn luyện mỗi bản đồ, §VI-A).
- Để làm gì: đầu vào chính của báo cáo G0 (W2-DAT-03, 30/10) và tiêu chí G0 #1–#2.
- Hạn mong muốn: trước T6 30/10. Duyệt xong: `python scripts/today.py --approve W1-DAT-02 --evidence "..."`.
- PDF: DAT có bản tải từ arXiv (SHA256 bắt đầu `44d03192`); nếu LDN không tải được, nhắn DAT.
LDN: (01/11) **Duyệt** (W1-DAT-02), kèm 3 góp ý nhỏ, không đổi hàng ma trận. Đã đối chiếu toàn văn arXiv:2010.12461v3 (bản HTML ar5iv) và trang abs. Mọi số liệu trong Form B khớp: bảng kết quả (99,4/88,0/87,5; 98,8/82,1/81,1), siêu tham số, khoảng tham số §VI-C/§VI-D, PT (1)–(19), câu "only two trained agents" (§VI-A), câu "would not yield meaningful results" (§VI-B), ngoại suy ở hình tham số (§VI-E); tham khảo [27] đúng là Liu, Sengupta, Kurzhanskiy, ICUAS 2017. Góp ý:
  (1) Trang arXiv có journal-ref: *IEEE Open Journal of the Communications Society*, vol. 2, pp. 1171–1187, 2021 (DOI 10.1109/OJCOMS.2021.3081996 theo OpenAlex). Nên sửa dòng "PDF không ghi nơi đăng bản mở rộng ✱" trong Form B và cập nhật `bayerlein2021multi` trong `paper/references.bib` (đang ghi arXiv, note VERIFY).
  (2) PT (45) (softmax khi huấn luyện) nằm ở §V-D, không phải §V-B.
  (3) Bản ar5iv đánh số hình/bảng lệch 1 so với Form B (ar5iv: MFLOPs = Bảng I, kết quả = Bảng III, hình tham số = Fig. 6) vì không đánh số hình lưới ví dụ và bảng chú giải; số trong Form B nhiều khả năng đúng theo PDF, LDN chưa mở PDF để xác nhận. "Phân bố đều" của cảm biến là suy diễn: bài chỉ viết "randomized throughout the unoccupied map space".

## A2. Danh sách tìm kiếm Q1–Q3 (W1-LDN-04, W1-LDN-05)
- W2-DAT-01 và W2-LDN-01 (đọc toàn văn, hạn 27/10) đang chờ danh sách này; G0 là CN 01/11.
- Cần LDN: đẩy danh sách đọc toàn văn (kể cả bản chưa hoàn chỉnh) lên repo sớm nhất có thể, để DAT và LDN chia đôi.
LDN: (31/10) Đã đẩy bản nháp: `notes/reading/search_log_LDN.md` (số kết quả, PRISMA rút gọn, sàng lọc) và `notes/reading/fulltext_list.md` (chia DAT/LDN). IEEE Xplore và Scopus không truy cập được; các điểm cần DAT quyết ở `notes/yeu-cau/2026-10-31_ldn_can-DAT_tim-kiem-q1-q3.md`.

## A3. Đọc phản biện Form B `notes/reading/zeng2019energy_DAT.md` (W1-DAT-04, second reader LDN)
- Cần LDN: kiểm bảng đối chiếu mã–bài (PT (1)–(2), (6), (10), (61), Bảng I) và hàng Zeng mới trong ma trận `docs/04` §5. Lưu ý: V_me, V_mr, P_h là số nhóm tự tính, bài không in.
- Để làm gì: mô hình năng lượng là trụ "năng lượng phụ thuộc tốc độ" trong định vị G0.
- Hạn mong muốn: trước T6 30/10. PDF arXiv:1804.02238v1 (SHA256 bắt đầu `f071ace9`); nếu không tải được, nhắn DAT.
- Mở: DAT chưa quyết xoá hay giữ preset `light` (không có trong Bảng I v1); LDN có ý kiến thì ghi ở đây.
LDN: (01/11) **Duyệt Zeng 2019** (W1-DAT-04), kèm 2 góp ý nhỏ. Đã đối chiếu arXiv:1804.02238 (chỉ có v1) qua ar5iv: PT (1)–(2), (6)–(10), (61), (65)–(66), Bảng I, §V (H = 100 m, B = 1 MHz, γ₀ = 60 dB, P_c = 50 W, V_max = 60 m/s, K = 3, Q̃ = 50/200 Mbit), mô tả Fig. 2–4, 6 đều khớp. Chạy lại `energy.py` (01/11): P₀ = 580,65 W, P_i = 790,67 W, P_h = 1371,32 W, v₀ = 7,188 m/s, V_me = 21,494 m/s (935,6 W; 43,5 J/m), V_mr = 38,266 m/s (1199,5 W; 31,3 J/m), S_FP = 0,01185, khớp bảng đối chiếu mã–bài. `env.py` cộng P_c chỉ khi hover có cảm biến được phục vụ (dòng 125–133), khớp PT (10). Góp ý:
  (1) Lemma 1 được phát biểu cho bài toán một GN (P2) ở §III-A; với nhiều GN, §V và Fig. 4 cho thấy FHC cũng chỉ bay ở V_mr hoặc hover. Nên ghi "§III-A, (P2); xem thêm §V, Fig. 4" thay vì "§III".
  (2) Mục "Mở" về preset `light`: đã quyết bỏ ở PR #29 (DECISIONS 26/10), LDN đồng ý. Nên thêm một dòng "Đã xử lý" vào Form B Zeng để người đọc sau không tưởng còn mở.
LDN: (01/11) **Duyệt Lamenza 2026** (phần còn lại của W1-DAT-04). Đối chiếu bản HTML Wiley (truy cập mở, First published 25/02/2026, tập 8 số 5): Bảng 1 khớp từng ô; 9 biến thể × 500 lần = 4500; ≥ 98% thành công; 200 lần đánh giá, ngưỡng 95%; ≈ 71 giờ/mô hình hợp tác, ≈ 700 000 và ≈ 80 000 000 bước; 9/3/1 mô hình; ≈ 50% chậm hơn; RTX 3090; GrADyS-SIM NextGen; tầm 20 m; danh mục [1]–[26] không có Bayerlein. Các số nằm trong công thức (200 m, 4 m, s ∈ [0, 15], hệ số +10) bị mất trong bản HTML nên dựa vào PDF của DAT. Góp ý nhỏ: câu hỏi cuối Form B (đổi khoá thành `lamenza2026`) đã được quyết là giữ khoá (DECISIONS 30/10), nên sửa thành "Đã quyết"; §2 vừa nói "constant speed" vừa cho hành động chọn tốc độ, có thể ghi thành mâu thuẫn nội tại của bài.
