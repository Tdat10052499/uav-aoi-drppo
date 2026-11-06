# DAT cần FAO, LDN: pull raw EXP-03 và xem lại hai PR (06/11/2026)

1. **Raw EXP-03 đã lên `main`** (commit 641922c, 147 file, 2,41 MB). Mọi run ở commit `prereg-lock` (b5cd784).
   - 42 run: 21 run train (DR 11, Fixed 10), 20 run eval (DR và Fixed, mỗi nhánh seed 0–9), cộng `heuristics_lock`. 41 run `completed`, 1 run `running`. (Đính chính 06/11: báo cáo đầu ghi nhầm 41 run.)
   - **DR seed 3 có hai run train.** Chỉ dùng `dr_ppo_mask_lam0.1_s3_20261105-140316` (completed). Run `..._s3_20261104-202500` vẫn ghi `running`: DAT đóng cửa sổ terminal khoảng 20:26 ngày 04/11, ở bước 16 384. Run này loại khỏi phân tích nhưng phải liệt kê trong bài (PREREG §9 mục 1, 5; card EXP-03 cuối file).
   - Không có file `episode_metrics` riêng; chỉ số theo episode nằm trong `events.csv` của các run eval.
   - **Tb log đã lên `main`** (c834009, cập nhật 06/11): `results/raw_tb/EXP-02b/` (1 run) và `results/raw_tb/EXP-03/` (21 run, gồm run s3 dở), mỗi thư mục có `SHA256SUMS.txt`. Để ngoài `results/raw/` để không lẫn vào các glob `results/raw/EXP-03/*`. FAO dùng để kiểm đường học (yêu cầu P1). EXP-08a không cần tb log.
   - `model.zip` không có trên git. 2 model cho W5-FAO-04, DAT gửi qua Drive (link: DAT điền):
     - Đề xuất chọn cơ học, không xem kết quả: `random.Random("641922ca31c32fc442a9ddd0f6fe19b9e04f9637")`, gọi `randrange(10)` hai lần, ra DR seed 7 rồi Fixed seed 5.
     - `dr_ppo_mask_lam0.1_s7_20261105-234718`: SHA256 `617efd7caa545dde2b0e47f395def741a0e135ca32fd08b9cd73c8c44d1b83d9`.
     - `fixed_ppo_mask_lam0.1_s5_20261105-194100`: SHA256 `58733dd39e5bfd76a67b779f1cc1e886613d72a51fc0803e4997b30163cc9865`.
     - Hai SHA256 khớp `checkpoint_digest` trong `run_record.json`. FAO kiểm lại sau khi tải.
     - W5-FAO-04 giao FAO chọn ngẫu nhiên. FAO muốn chọn cách khác thì nhắn DAT gửi model khác, và ghi cách chọn vào `review_log`.
     - Đánh giá lại tại commit `prereg-lock` (DECISIONS 06/11, ngoại lệ PREREG §1), rồi so với `eval_dr_ppo_s7`, `eval_fixed_ppo_s5` bằng `scripts/compare_events.py`.
   - LDN: EXP-08a (W4-LDN-03) và W4-LDN-04 bắt đầu được ngay.
2. **PR #41** (DECISIONS sau khoá): FAO đã duyệt bản e56173a. Sau đó có thêm dòng đính chính giờ dừng và nguyên nhân của run DR seed 3. Nhờ FAO hoặc LDN duyệt lại để DAT merge.
3. **PR #46** đã merge (7a06bff) **trước khi LDN review**. Nhờ LDN xem lại sau merge. Phát hiện gì thì DAT sửa qua PR mới.
   - Phụ thuộc lịch theo review #44 của LDN.
   - Bỏ các task hỏi GVHD (DAT quyết: GVHD duyệt ở bản thảo), nên `docs/05` §5 G0 #2, G0 #3, G1 #6 đổi thành "nhóm chốt".
   - Ghi chú định vị thành phần A: Bayerlein 2021 và Theile 2020 đã có ngân sách tuyệt đối trong quan sát (`notes/reading/theile2020_DAT.md`).
4. **PR #45** (mã pilot) đã merge theo ngoại lệ PREREG §1 (DECISIONS). Commit cd62a0b (sửa L1) chưa được approve lại; nhờ FAO, LDN xem diff `0c207f2..cd62a0b`.
