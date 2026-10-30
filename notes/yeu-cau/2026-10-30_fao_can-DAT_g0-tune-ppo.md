# FAO → DAT: G0 còn 2 ngày, tune_ppo.py chưa có — 30/10/2026

> Trả lời bằng dòng `DAT:` dưới mỗi mục (`notes/yeu-cau/README.md`, PR #28). Số liệu trạng thái lấy từ `python scripts/today.py --team --date 2026-10-30` tại commit 34a1e9f; FAO không tự dời hạn task nào (quy tắc 10).

## A1. `tune_ppo.py` (W2-DAT-02) chưa được đẩy lên, W2-FAO-04 bị chặn
- **Cần:** push nhánh `tune_ppo.py` (kể cả bản chưa xong) và mở PR, hoặc cho FAO ngày mới.
- **Để làm gì:** W2-FAO-04 (second reader `tune_ppo.py`: đọc mã, chạy 2 lượt nhỏ) có hạn 30–31/10 và nằm trên đường tới G1. W2-DAT-02 có hạn 29/10; W1-DAT-06 (khung `tune_ppo.py`, hạn 23/10) cũng chưa xong. Trên GitHub chưa có nhánh hay PR nào chứa `tune_ppo.py`.
- **Hạn mong muốn:** 31/10, để FAO kịp chạy 2 lượt nhỏ trước khi hết hạn W2-FAO-04.

## A2. G0 (CN 01/11): có giữ ngày không?
- **Tình trạng theo `today.py --team`:**
  - W2-DAT-03 (báo cáo G0, Form G) chờ W2-DAT-01 và W2-LDN-01; cả hai đã quá hạn (27/10).
  - W2-LDN-03 (second reader báo cáo G0) chờ W2-DAT-03.
  - Ma trận `docs/04` §5 còn ô "Chưa rõ" ở Yi 2020, Sarathchandra 2025, Lamenza 2025 và OH-DRL 2025 (tiêu chí G0 số 1: mỗi ô có nguồn).
- **FAO đã làm (30/10):** thêm vị trí nguồn (PT, mục, bảng, hình) vào mọi ô của 3 hàng FAO đọc: Abd-Elmagid 2019, Sun 2025, Liu 2024. Hàng OH-DRL ghi rõ "tóm tắt", vì chưa có toàn văn (A3 trong `notes/2026-10-21_fao_can-DAT.md`).
- **Cần DAT quyết:** giữ G0 ngày 01/11 hay áp dụng điều khoản "kéo dài tối đa 3 ngày" của tiêu chí 1 (`docs/05`, G0). Nếu kéo dài, ghi vào `docs/DECISIONS.md`.
- **FAO có thể giúp nếu DAT hoặc LDN đồng ý:** đọc toàn văn Yi 2020 (ar5iv) và viết Form B để điền hàng Yi. Đây là việc của LDN (W1-LDN-02), nên FAO chỉ làm khi được giao.

DAT: (30/10) Kéo dài G0 3 ngày, sang **T4 04/11/2026** (DECISIONS 2026-10-30, `docs/05` §5). G1 15/11 giữ nguyên. Lamenza đã có Form B và hàng ma trận đủ nguồn (commit 3105342). Việc đọc Yi 2020: chờ DAT hỏi LDN.

## A3. Việc đang chờ DAT review hoặc trả lời
- **PR #23** (cờ `single_speed` cho A5): đã merge `main` sau #29, 14/14 kiểm thử, smoke PASS. Phải merge trước khi khoá PREREG (G1).
- **PR #20** (EXP-04 card, DQN 10k): cần merge trước khi DAT đo DQN 100k bước (A1 của `notes/yeu-cau/2026-10-26_dat_can-FAO_steps-per-s.md`).
- PR #19, #22, #24, #25, #26, #27: chưa có review.
- Issue #15 (W1-FAO-05, ước lượng chi phí): chờ DAT duyệt.
- Câu hỏi chưa trả lời: A1–A5 trong `notes/2026-10-21_fao_can-DAT.md` (A4 là máy cố định) và C2–C5 trong `notes/2026-10-22_fao_can-DAT.md`.
- **PR #28** (quy trình mới) chưa merge, nên `today.py` trên `main` vẫn báo W1-ALL-01 quá hạn và chưa hiện mục *YÊU CẦU GỬI BẠN*.
