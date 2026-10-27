# Nhật ký quyết định thiết kế

Ghi mọi thay đổi so với `00_HUONG_DAN_PROJECT.md` (bảng "Quyết định chuẩn") và `02_mo_hinh_he_thong.md`.

| Ngày | Quyết định | Lý do | Ảnh hưởng | Người duyệt |
| --- | --- | --- | --- | --- |
| 2026-10-16 | Khởi tạo bộ quyết định chuẩn (file 00) | Bộ khởi đầu | — | — |
| 2026-10-26 | Bỏ preset năng lượng `light` khỏi `src/uavaoi/energy.py` (và kiểm thử đi kèm) | Không có trong Bảng I của arXiv:1804.02238v1, không kiểm chứng được; chưa lần chạy nào trong `results/raw` dùng (cả 5 run dùng `zeng2019_arxiv_v1`) | Chỉ còn preset đã kiểm; test_core còn 13 kiểm thử; không ảnh hưởng kết quả đã có | DAT |
