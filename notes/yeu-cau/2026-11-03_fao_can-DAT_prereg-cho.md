# FAO → DAT: các ô PREREG còn chờ DAT quyết, trước W4-FAO-01 (09/11) — 03/11/2026

> Trả lời bằng dòng `DAT:` dưới mỗi mục (`notes/yeu-cau/README.md`, PR #28). Mỗi mục là một ô `CHỜ` trong `notes/2026-10-22_fao_PREREG-nhap.md` (cập nhật 03/11). FAO chép sang `docs/PREREG.md` ở W4-FAO-01 (09–13/11), LDN là second reader. Các ô siêu tham số (W4-DAT-01) và ngưỡng H1 (LDN) không nằm ở đây.

## A1. Số bước mỗi lần huấn luyện
- **Cần:** chốt số bước cho EXP-03 đến EXP-07 (điểm xuất phát `docs/03` §3 là 2 M).
- **Để làm gì:** §5 của nháp. Ước lượng chi phí ở 2 M và Phương án B là 126,5–173,0 giờ máy, kịp trước 13/12 (`Project Agreement.md` §5). Tiêu chí G1 số 6 cần con số này.
- **Đề xuất mặc định của FAO:** 2 M, nếu pilot EXP-02 (W3) không cho thấy lý do đổi.
- **Hạn mong muốn:** sau pilot EXP-02, trước 13/11.

## A2. EXP-05: λ = 0,1 có dùng lại seed 0–4 DR-PPO của EXP-03 không?
- **Cần:** có hoặc không.
- **Để làm gì:** §5 của nháp. Dùng lại thì tổng là 149,2 M thay vì 159,2 M bước (cộng 4 M Optuna DQN), tiết kiệm khoảng 10 M bước, tức khoảng 7,8 h trên laptop DAT (`notes/2026-10-21_fao_chi-phi-nhap.md`). Hai lựa chọn đều hợp lệ nếu ghi trong PREREG trước khi chạy.
- **Đề xuất mặc định của FAO:** dùng lại. Cùng cấu hình, cùng seed và cùng ngân sách, nên đó chính là điểm λ = 0,1 của đường quét.
- **Hạn mong muốn:** trước 13/11.

## A3. RQ3 (DR-DQN so với DR-PPO): có đặt hướng không?
- **Cần:** một trong hai: (a) giả thuyết có hướng kèm kiểm định, hoặc (b) "chỉ mô tả" (trung bình, CI, Cliff's δ, không p-value).
- **Để làm gì:** §7 của nháp và `notes/EXP-04_dqn_card.md` ("Giả thuyết: chưa đặt hướng").
- **Đề xuất mặc định của FAO:** (b) chỉ mô tả. `docs/01` §4 nêu RQ3 là so sánh. Card TUNE cũng ghi rằng sai lệch khi tinh chỉnh có thể bất lợi cho DQN, nên một kiểm định có hướng sẽ khó diễn giải.
- **Hạn mong muốn:** trước 13/11.

## A4. Peak AoI làm chỉ số phụ mô tả
- **Cần:** đồng ý hoặc không.
- **Để làm gì:** §7 của nháp. `env.py` đã tính `peak_aoi`. Báo cáo mô tả cho phép so với các bài dùng peak AoI (Sun 2025). Không đưa vào giả thuyết.
- **Đề xuất mặc định của FAO:** đồng ý, chỉ mô tả.
- **Hạn mong muốn:** trước 13/11.

## A5. Tiêu chí loại một lần chạy (§9 của nháp)
- **Cần:** DAT và LDN duyệt 4 tiêu chí ở §9 (failed thì loại và liệt kê; NaN thì chạy lại một lần với seed mới; không loại vì kết quả kém; commit khác `prereg-lock` thì không dùng).
- **Để làm gì:** ô "Tiêu chí loại một lần chạy" trong `docs/PREREG.md`.
- **Hạn mong muốn:** trước 13/11.
