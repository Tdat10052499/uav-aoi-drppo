# Nhật ký quyết định thiết kế

Ghi mọi thay đổi so với `00_HUONG_DAN_PROJECT.md` (bảng "Quyết định chuẩn") và `02_mo_hinh_he_thong.md`.

| Ngày | Quyết định | Lý do | Ảnh hưởng | Người duyệt |
| --- | --- | --- | --- | --- |
| 2026-10-16 | Khởi tạo bộ quyết định chuẩn (file 00) | Bộ khởi đầu | — | — |
| 2026-10-26 | Bỏ preset năng lượng `light` khỏi `src/uavaoi/energy.py` (và kiểm thử đi kèm) | Không có trong Bảng I của arXiv:1804.02238v1, không kiểm chứng được; chưa lần chạy nào trong `results/raw` dùng (cả 5 run dùng `zeng2019_arxiv_v1`) | Chỉ còn preset đã kiểm; test_core còn 13 kiểm thử; không ảnh hưởng kết quả đã có | DAT |
| 2026-10-30 | Lùi G0 từ CN 01/11 sang T4 04/11/2026 (dùng điều khoản "kéo dài tối đa 3 ngày" của tiêu chí G0 số 1, `docs/05` §5) | Ma trận `docs/04` §5 còn ô "Chưa rõ" ở Yi 2020, Sarathchandra 2025, OH-DRL 2025; W2-DAT-01, W2-LDN-01 quá hạn (yêu cầu FAO 30/10, mục A2) | Báo cáo G0 và second reader lùi theo; G1 (15/11) **không đổi**. Không được kéo dài thêm lần nữa | DAT |
| 2026-10-30 | DQN (EXP-04, RQ3) được tinh chỉnh bằng Optuna với **cùng ngân sách** như PPO: cùng số trial (20), cùng số bước mỗi trial (200k), cùng sampler seed, chỉ đánh giá trên `id` | Tránh nhiễu "PPO được chỉnh, DQN thì không" khi so sánh RQ3 (`docs/03` §3) | `tune_ppo.py` thêm `--algo dqn` (PR #30); thêm ≈ 10 giờ máy ở W4 (ước lượng từ tốc độ DQN pha 0, 19,5 bước/s trên laptop FAO, chưa đo trên máy DAT) | DAT |
