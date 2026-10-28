# FAO → DAT: việc mới cần DAT xử lý — 22/10/2026

> Bổ sung cho `notes/2026-10-21_fao_can-DAT.md` (các mục A1–A7 ở đó vẫn mở). Trả lời bằng dòng `DAT:` dưới mỗi mục, hoặc trên PR tương ứng.

## C1. PR #23 (`fao/a5-single-speed`) phải merge trước khi khoá PREREG (G1, 15/11)
- Ablation A5 (một tốc độ V_me, EXP-07) cần cờ `single_speed` trong `EnvConfig`. Mã hiện tại không có cách tắt V_mr.
- Sau mốc khoá `src/` không được sửa (W5-DAT-01), nên nếu PR này không vào trước G1 thì A5 không chạy được.
- Kiểm tra trong container: 15/15 kiểm thử, smoke PASS. Mặc định `False`, nên mọi cấu hình hiện có không đổi.
- https://github.com/Tdat10052499/uav-aoi-drppo/pull/23

## C2. `use_action_mask_clip` trong `EnvConfig` không được dùng ở đâu
- Trường có trong `configs/env_default.json` (giá trị `true`) nhưng `env.py` không đọc nó. Kẹp biên + phạt μ luôn chạy khi hành động ra ngoài vùng.
- Đề xuất: xoá, hoặc ghi chú "không có tác dụng", trước khi khoá PREREG để người đọc config không hiểu nhầm. FAO không tự sửa vì đổi file cấu hình sẽ đổi SHA256 đang ghi trong PREREG nháp.

## C3. A4, A5 có tinh chỉnh riêng không
`notes/EXP-07_ablation_card.md` mặc định **dùng nguyên siêu tham số DR-PPO, không tinh chỉnh**, và ghi là giới hạn. Nếu DAT muốn tinh chỉnh riêng thì phải cộng ngân sách vào PREREG.

## C4. `paper/references.bib` thiếu `liu2024generalizable`
Bài đã có Form B và nằm trong ma trận `docs/04` §5, nhưng chưa có mục BibTeX. Mục đề xuất ở cuối `notes/2026-10-22_fao_related-work-limitations-nhap.tex`.

## C5. Seed đánh giá trong lúc tinh chỉnh (W4-DAT-01)
Phải tách khỏi bộ 100000–100099. PREREG nháp đề xuất `id`, seed 200000–200099. DAT chốt khi viết `tune_ppo.py`.
