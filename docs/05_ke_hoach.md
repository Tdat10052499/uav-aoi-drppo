# 05 — Kế hoạch thực hiện

Hai phương án dùng chung giai đoạn đầu (tuần 1–4). Chọn phương án tại gate G1 (15/11/2026), sau khi có câu trả lời về quy định cộng điểm và hạn nộp của hội nghị (`07` §2).

- **Phương án A — MVP 6 tuần (19/10 → 29/11/2026):** bài 6–8 trang, kịp hội nghị hạn khoảng cuối tháng 11 – đầu tháng 12 (FJCAI 2027 / ICISN 2027 nếu lịch xác nhận như dự kiến).
- **Phương án B — Đầy đủ 12 tuần (19/10/2026 → 10/01/2027):** bài 12–15 trang và đồ án hoàn chỉnh; hội nghị hạn sau 10/01/2027 (AIEI 2027, IEEE SMC 2027…).
- Có thể làm **A rồi B**: B là bản mở rộng đáng kể của A; bài thứ hai phải khác biệt rõ và trích dẫn bài thứ nhất.

## Lịch theo tuần

| Tuần | Ngày | Việc chính | Sản phẩm bàn giao |
| --- | --- | --- | --- |
| 1 | 19–25/10 | Học nhanh RL (Phase 9 của ai-engineering-from-scratch: MDP, DQN, PPO); đọc [B21], [Z19], Yi 2020; chạy `tests/` và `evaluate.py`; rà soát `env.py` | Mỗi thành viên tóm tắt 1 trang/bài; danh sách lỗi hoặc thắc mắc về môi trường |
| 2 | 26/10–01/11 | Tổng quan hệ thống (truy vấn Q1–Q3, `04` §6); điền ma trận định vị; huấn luyện thử 10k bước; đo tốc độ 100k bước | Ma trận `04` §5 đầy đủ; số đo tốc độ; **Gate G0** |
| 3 | 02–08/11 | Chạy thử DR-PPO và Fixed-PPO (1 seed, ~300k bước); vẽ quỹ đạo, kiểm tra reward hacking; Optuna nhỏ trên ID | Đường học sơ bộ; ảnh quỹ đạo; cấu hình siêu tham số ứng viên |
| 4 | 09–15/11 | Chốt siêu tham số; điền `PREREG.md`; khởi chạy 5–10 seed cho DR-PPO và Fixed-PPO | `PREREG.md` đã khoá; **Gate G1** (chọn A/B) |
| 5 | 16–22/11 | Đánh giá 5 bộ; `analyze.py`; vẽ hình F3, F4, F6; viết mục System Model và Method | Bảng kết quả chính; bản nháp 50% |
| 6 | 23–29/11 | **A:** viết Results/Discussion, 2 vòng phản biện nội bộ, nộp. **B:** chạy DR-DQN, bắt đầu ablation | **A:** bài nộp. **B:** kết quả DQN |
| 7 | 30/11–06/12 | B: ablation A4, A5; viết thêm mã quan sát A2/A3 | Kết quả ablation đợt 1 |
| 8 | 07–13/12 | B: ablation A2/A3; quét λ (RQ2) | Đường đánh đổi AoI–năng lượng (F5) |
| 9 | 14–20/12 | B: đủ 10 seed mọi phương pháp; chạy lại toàn bộ đánh giá từ commit đã khoá | **Gate G2** — đóng băng kết quả |
| 10 | 21–27/12 | B: viết bài đầy đủ; chương 1–3 đồ án | Bản nháp bài 80% |
| 11 | 28/12–03/01 | B: chương 4–5 đồ án; phản biện nội bộ vòng 1 | Bản nháp đồ án |
| 12 | 04–10/01 | B: phản biện vòng 2; kiểm tra danh sách `06` §3; đóng gói mã | **Gate G3** — bài và đồ án sẵn sàng |

## Gate (tiêu chí qua mốc)
1. **G0 — 01/11:** ma trận định vị xong. Nếu một công trình đã có đủ "AoI + năng lượng phụ thuộc tốc độ + huấn luyện nhiều bố trí + OOD có cấu trúc", **đổi trọng tâm**. Các hướng thay thế: (a) vai trò của lựa chọn tốc độ (A5) làm đóng góp chính; (b) chuyển sang đa UAV (MAPPO). Giảng viên quyết định.
2. **G1 — 15/11:** PPO học được trên ID (AoI thấp hơn Random rõ rệt, không phân kỳ); tốc độ huấn luyện đo được; `PREREG.md` khoá. Chọn A hay B.
3. **G2 — 20/12 (B):** đủ seed; mọi bảng và hình sinh lại được từ một lệnh. Không chạy thêm thực nghiệm mới sau mốc này.
4. **G3 — 10/01/2027 (B):** đúng giới hạn trang và template; đạt danh sách kiểm tra `06` §3.

## Phân công gợi ý (nhóm 3 sinh viên)
| Vai trò | Phụ trách | Sản phẩm chính |
| --- | --- | --- |
| SV1 — Môi trường & heuristic | `uavaoi/env.py`, `baselines.py`, biến thể quan sát A2/A3, kiểm thử | Môi trường ổn định, hình quỹ đạo |
| SV2 — Học tăng cường | `train_ppo.py`, Optuna, chạy seed, DQN, ablation | Mô hình đã huấn luyện, log |
| SV3 — Tài liệu & thống kê | Tổng quan hệ thống, `analyze.py`, hình F3–F5, bản thảo | Chương 2, bảng kết quả, bản thảo |
| Giảng viên | Duyệt tại mỗi gate, định vị đóng góp, phản biện nội bộ | Quyết định G0–G3 |

## Nhịp làm việc
- Họp 30 phút mỗi tuần: mỗi người trình bày 1 hình hoặc 1 bảng mới, không chỉ báo cáo bằng lời.
- Mọi lần chạy ghi `run_config.json` và commit hash; không sửa kết quả bằng tay.
- Thay đổi thiết kế sau G1 phải ghi vào `DECISIONS.md` kèm ngày và lý do.
