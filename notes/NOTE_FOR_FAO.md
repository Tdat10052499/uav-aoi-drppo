# Ghi chú cho FAO (Nguyễn Minh Chính)

> Viết ngày 17/10/2026. Đọc kèm `docs/05_ke_hoach.md` (kế hoạch hiện hành) và `Project Agreement.md`.

> **Mỗi sáng:** mở Claude Code trong repo và hỏi *"hôm nay tôi cần làm gì?"*. Lần đầu chạy `python scripts/today.py --set-nick FAO`. Lịch của bạn: `python scripts/today.py` hoặc lọc cột *Ai = FAO* trong `schedule/SCHEDULE.md`.

Chào FAO! Vai trò của bạn giống phần bạn làm ở RIVF-Paper: **môi trường chạy, tái lập và provenance**. Mọi con số trong bài đều đứng trên nền bạn dựng, nên tuần 1 là tuần quan trọng nhất của bạn.

## Bạn sở hữu
| File / việc | Ghi chú |
| --- | --- |
| `environment/requirements.txt`, `environment/machine_notes.md` | Ghi phiên bản thật sau lần chạy đầu tiên |
| `notes/EXP-01_reproduction_card.md` | Đã viết sẵn phần card; bạn điền phần kết quả (Form C) |
| `data/checkpoint_manifest.md` | Mỗi model dùng trong bài có một dòng, kèm SHA256 lấy từ `run_record.json` |
| EXP-04 (DR-DQN), EXP-07 (A4 bỏ mask, A5 một tốc độ) | Card viết trước khi chạy |
| `scripts/plot_trajectory.py` (chưa có — bạn viết) | Vẽ quỹ đạo một episode ra `figures/`, dùng cho F6 và kiểm tra suy biến |
| Tái lập độc lập tại G2 | Chạy lại toàn bộ đánh giá từ commit khoá trên máy khác |

## Ba ngày đầu
1. **19/10:** chấp nhận lời mời repo, clone, tạo venv, `pip install -r environment/requirements.txt`.
2. **20/10:** `python tests/test_core.py` (kỳ vọng 14/14), rồi `python scripts/run_smoke_test.py` (kỳ vọng PASS). Sau đó chạy `evaluate.py` heuristic và so khớp với `results/raw/heuristics/heuristics_100ep_2026-10-16.csv`.
3. **21/10:** chạy `train_ppo.py` 10k bước. Script này **chưa từng chạy với PyTorch**, nên lỗi API là chuyện bình thường. Sửa trên nhánh `fao/train-smoke` và mở PR cho DAT review.

## Lưu ý
- Smoke test được thiết kế để **báo lỗi rõ ràng**. Nếu nó fail vì lệch số, đừng sửa file tham chiếu: ghi khác biệt vào Form C (có thể do khác phiên bản NumPy).
- Số đo thời gian chỉ lấy từ máy cố định của DAT. Kaggle chỉ dùng để chạy thêm seed.
- Second reader của bạn: DAT (EXP-01, EXP-04), LDN (EXP-07).
