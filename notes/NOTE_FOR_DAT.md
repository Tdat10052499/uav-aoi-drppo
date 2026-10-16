# Ghi chú cho DAT (Hồ Du Tuấn Đạt)

> Viết ngày 17/10/2026. Đọc kèm `docs/05_ke_hoach.md` (kế hoạch hiện hành) và `Project Agreement.md`.

> **Mỗi sáng:** mở Claude Code trong repo và hỏi *"hôm nay tôi cần làm gì?"*. Lần đầu chạy `python scripts/today.py --set-nick DAT`. Lịch của bạn: `python scripts/today.py` hoặc lọc cột *Ai = DAT* trong `schedule/SCHEDULE.md`.

Vai trò: **phương pháp DR-PPO, định vị đóng góp và điều phối**. Bạn là đầu mối với giảng viên và hội nghị, đồng thời giữ máy cố định dùng cho mọi số đo thời gian.

## Bạn sở hữu
| File / việc | Ghi chú |
| --- | --- |
| `Project Agreement.md` | Gửi GVHD ngày 19/10; nhận và giải quyết các dòng `%%GVHD:` |
| Gate G0 (01/11) | Ma trận `docs/04` §5, câu định vị `docs/01` §3, báo cáo Form G |
| `scripts/train_ppo.py`, `scripts/tune_ppo.py` (chưa có — bạn viết) | Optuna với ngân sách bằng nhau cho DR và Fixed, chỉ đánh giá trên ID |
| EXP-02 (huấn luyện), EXP-06 (biến thể quan sát A2/A3) | EXP-02 card đã viết sẵn |
| Bản thảo | Intro, Method, Discussion, Abstract; kiểm tra định dạng hội nghị |
| Issue #7 | Hội nghị đích, quy định cộng điểm, ý nghĩa mốc 18–19/01 |

## Việc ngay
1. **Mời LDN (`Yui-Mika`) và FAO (`F4ol4n`)** làm collaborator của repo (Settings → Collaborators).
2. Điền tên giảng viên hướng dẫn vào `Project Agreement.md` §1 và gửi bản Rev 0.1.
3. **Trước 25/10:** xin GVHD duyệt bảng ngưỡng gate trong `docs/05` §5.

## Lưu ý định vị
Bayerlein et al. 2021 đã tổng quát hoá theo tham số kịch bản. Đề tài **không** được viết "đầu tiên tổng quát hoá". Điểm khác biệt là:
- AoI nhiều chu kỳ;
- năng lượng phụ thuộc tốc độ;
- OOD có cấu trúc;
- thống kê theo seed.

Nếu G0 tìm thấy công trình đủ cả 5 cột của ma trận, đề xuất GVHD hướng A5 hoặc đa UAV.
