# DAT cần FAO, LDN: pull raw EXP-03 và xem lại hai PR (06/11/2026)

1. **Raw EXP-03 đã lên `main`** (commit 641922c, 147 file, 2,41 MB). Mọi run ở commit `prereg-lock` (b5cd784).
   - 41 run: 20 run train, 20 run eval (DR và Fixed, mỗi nhánh seed 0–9), cộng `heuristics_lock`.
   - **DR seed 3 có hai run train.** Chỉ dùng `dr_ppo_mask_lam0.1_s3_20261105-140316` (completed). Run `..._s3_20261104-202500` vẫn ghi `running`: DAT đóng cửa sổ terminal khoảng 20:26 ngày 04/11, ở bước 16 384. Run này loại khỏi phân tích nhưng phải liệt kê trong bài (PREREG §9 mục 1, 5; card EXP-03 cuối file).
   - Không có file `episode_metrics` riêng; chỉ số theo episode nằm trong `events.csv` của các run eval.
   - **Chưa có tb log** (nằm trong `runs/EXP-03/*/tb/` trên máy DAT, `runs/` bị gitignore). EXP-08a không cần tb log.
   - `model.zip` không có trên git. FAO cần 2 model cho W5-FAO-04 thì nhắn DAT gửi qua Drive.
   - LDN: EXP-08a (W4-LDN-03) và W4-LDN-04 bắt đầu được ngay.
2. **PR #41** (DECISIONS sau khoá): FAO đã duyệt bản e56173a. Sau đó có thêm dòng đính chính giờ dừng và nguyên nhân của run DR seed 3. Nhờ FAO hoặc LDN duyệt lại để DAT merge.
3. **PR #46** đã merge (7a06bff) **trước khi LDN review**. Nhờ LDN xem lại sau merge. Phát hiện gì thì DAT sửa qua PR mới.
   - Phụ thuộc lịch theo review #44 của LDN.
   - Bỏ các task hỏi GVHD (DAT quyết: GVHD duyệt ở bản thảo), nên `docs/05` §5 G0 #2, G0 #3, G1 #6 đổi thành "nhóm chốt".
   - Ghi chú định vị thành phần A: Bayerlein 2021 và Theile 2020 đã có ngân sách tuyệt đối trong quan sát (`notes/reading/theile2020_DAT.md`).
4. **PR #45** (mã pilot) đã merge theo ngoại lệ PREREG §1 (DECISIONS). Commit cd62a0b (sửa L1) chưa được approve lại; nhờ FAO, LDN xem diff `0c207f2..cd62a0b`.
