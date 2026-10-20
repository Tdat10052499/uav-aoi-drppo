# Project Agreement

> Form A của `notes/workbook_forms.md`. Điền chung ngày đầu (19/10/2026), sửa khi có bằng chứng mới, ghi số revision.
> **Quy ước góp ý:** giảng viên hướng dẫn chèn dòng `%%GVHD:` ngay dưới mục cần góp ý; thành viên trả lời bằng `%%Reply-LDN:`, `%%Reply-FAO:`, `%%Reply-DAT:`. Giải quyết xong thì xoá cả cặp và ghi vào `docs/DECISIONS.md` nếu là quyết định thiết kế.

## Section 1: Project Metadata

- **Project title:** Generalizable AoI- and Energy-Aware UAV Trajectory Planning for IoT Data Collection via Domain-Randomized Proximal Policy Optimization
- **Tên tiếng Việt:** Hoạch định quỹ đạo UAV thu thập dữ liệu IoT có khả năng tổng quát hoá, tối ưu tuổi thông tin và năng lượng bằng PPO với domain randomization
- **Date / revision:** 17/10/2026 — Rev 0.1 (bản nháp, chờ duyệt)
- **Team members and supervisor:**
  - Hồ Du Tuấn Đạt — **DAT** — GitHub `Tdat10052499`
  - Dương Ngọc Linh Đan — **LDN** — GitHub `Yui-Mika`
  - Nguyễn Minh Chính — **FAO** — GitHub `F4ol4n`
  - Giảng viên hướng dẫn: **Dr. Nguyễn Trí Hải**
- **Hình thức:** bài báo hội nghị + đồ án tốt nghiệp
- **Submission track, verified deadline, and source:** **chưa chốt.** Ứng viên đã kiểm tra ngày 16/10/2026 (`docs/04` §7):
  - AIEI 2027 (ĐH Văn Lang): hạn 15/02/2027 (đã xác minh trên trang chính thức).
  - IEEE SMC 2027 (TP.HCM): hạn 15/04/2027 (theo trang tổng hợp, chưa có trang chính thức).
  - FJCAI 2027 và ICISN 2027: chưa công bố hạn.
  - Working assumption: bản thảo sẵn sàng **10/01/2027** (Gate G3). Owner xác minh: DAT, trước 25/10 (issue #7).

## Section 2: Core Research Problem

- **Concrete deployment example:**
  - Một UAV cánh quay thu dữ liệu định kỳ từ mạng cảm biến môi trường ở vùng không có hạ tầng viễn thông.
  - Mỗi đợt triển khai, vị trí và số lượng cảm biến khác nhau: thêm hoặc bớt trạm, thay đổi theo mùa vụ hoặc địa hình.
  - Huấn luyện lại một chính sách DRL cho từng bố trí là không thực tế. Vì vậy chính sách cần chạy được trên bố trí chưa từng thấy, đồng thời giữ dữ liệu "tươi" (AoI thấp) với pin giới hạn.
  - Tốc độ bay ảnh hưởng phi tuyến đến công suất, nên chính sách phải tự chọn tốc độ.
- **Research question:** Khi bố trí, mật độ cảm biến, diện tích hoặc ngân sách năng lượng dịch chuyển khỏi phân phối huấn luyện, chính sách PPO huấn luyện với domain randomization có giữ AoI tốt hơn (độ suy giảm OOD nhỏ hơn) so với PPO huấn luyện trên một bố trí cố định không? Câu hỏi này đặt trong bài toán AoI nhiều chu kỳ, năng lượng đẩy phụ thuộc tốc độ, và so sánh ở cùng ngân sách huấn luyện và tinh chỉnh.
- **Hypothesis:** DR-PPO có độ suy giảm OOD nhỏ hơn Fixed-PPO trên ít nhất 3/4 bộ OOD. Lợi thế lớn nhất được kỳ vọng ở dịch chuyển cấu trúc không gian (bố trí phân cụm), nhỏ nhất ở dịch chuyển tài nguyên (năng lượng thấp).
- **Proposed contribution (still unverified):**
  - Phép đo định lượng độ bền của chính sách DRL dưới dịch chuyển phân phối có cấu trúc, cho bài toán AoI + năng lượng theo tốc độ.
  - Ablation chỉ ra thành phần nào cần thiết: domain randomization, quan sát bản đồ căn tâm, lựa chọn tốc độ.
  - Môi trường mở, tái lập được.
- **Closest prior work and exact remaining difference:**
  - Bayerlein et al. 2021 (arXiv:2010.12461): chính sách DDQN đa UAV tổng quát hoá theo tham số kịch bản (số UAV, số/vị trí cảm biến, thời gian bay), có thử ngoại suy. **Difference:** mục tiêu của họ là lượng dữ liệu thu một lần và năng lượng hằng số mỗi bước. Ở đây là AoI nhiều chu kỳ, năng lượng phụ thuộc tốc độ, và đánh giá OOD có cấu trúc kèm thống kê theo seed.
  - Yi et al. 2020 (INFOCOM Wksp): DRL giảm AoI có ràng buộc năng lượng. **Difference:** chưa xác định họ có đánh giá trên bố trí chưa thấy hay không (cần đọc toàn văn, gate G0).
  - Sarathchandra et al. 2025 (arXiv:2501.14603): meta-RL thích nghi khi **hàm mục tiêu** thay đổi. **Difference:** ở đây là dịch chuyển **bố trí và tài nguyên**, không phải mục tiêu, và không cần bước thích nghi.
  - de Souza Lamenza et al. 2025 (Adv. Intell. Syst.): số cảm biến linh hoạt, bài toán thăm một lần. **Difference:** cần đọc toàn văn.
  - Zeng, Xu, Zhang 2019: nguồn của mô hình năng lượng và giao thức fly–hover–communicate. Đây không phải công trình DRL; dùng làm mô hình hệ thống.

## Section 3: Kịch bản & giả định hệ thống (thay cho threat model)

- **Hệ thống:** 1 UAV cánh quay, độ cao cố định H = 100 m; vùng L × L; N cảm biến tĩnh; fly–hover–communicate; TDMA một cảm biến mỗi khe (`docs/02`).
- **Thông tin chính sách nhận được:** bản đồ căn tâm 5 kênh (AoI, số cảm biến, mặt nạ biên, năng lượng còn lại, thời gian còn lại). Chính sách không biết N trước và không được huấn luyện lại khi triển khai.
- **Heuristic đối chứng:** biết trạng thái đầy đủ (vị trí, AoI) ở độ phân giải gốc. Đây là đối chứng **có lợi** cho heuristic.
- **Ngoài phạm vi:** kênh che khuất, đa UAV, gió/nhiễu động lực học, bay thực nghiệm, sạc giữa nhiệm vụ, cảm biến di động.

## Section 4: Evaluation & Metrics

- **Primary outcome and denominator:**
  - AoI trung bình Ā = (1/(T·N)) Σ_t Σ_n Δ_n(t), đơn vị khe.
  - Mẫu số là T·N, tính trên **toàn chân trời T** kể cả khi hết pin sớm (AoI tiếp tục tăng sau đó).
  - Độ suy giảm OOD của seed i trên bộ s: deg_i(s) = (Ā_i(s) − Ā_i(id)) / Ā_i(id).
- **Utility and resource-cost metrics:** peak AoI; năng lượng đã dùng (J và tỷ lệ E_max); tỷ lệ hết pin sớm; độ phủ (tỷ lệ cảm biến được thu ≥ 1 lần); tỷ lệ hover/chậm/nhanh; chạm biên; số bước huấn luyện; thời gian suy luận mỗi bước (đo trên một máy cố định).
- **Strongest necessary baseline:**
  - (a) **Fixed-PPO**: cùng kiến trúc, cùng ngân sách bước và tinh chỉnh. Đây là đối chứng cô lập hiệu ứng của DR.
  - (b) **TSP** (NN + 2-opt, thông tin đầy đủ).
  - (c) DR-DQN (đối chứng thuật toán).
  - (d) Random có mask (cận dưới, phát hiện lỗi).
- **Smallest experiment (EXP-02, `notes/EXP-02_pilot_card.md`):**
  - DR-PPO và Fixed-PPO, mỗi bên 2 seed, khoảng 300k bước.
  - Đánh giá trên `id` và `ood_cluster`, 100 episode cố định.
  - So sánh độ suy giảm OOD và đối chiếu với TSP.
- **What result would make us stop (Gate G1, 15/11):** xem tiêu chí đầy đủ trong `docs/05_ke_hoach.md`. Tóm tắt:
  - nếu cả 2 seed của DR-PPO không đạt AoI trên `id` ≤ 0,5 × Random, thì **debug**, không mở rộng;
  - nếu không có tín hiệu DR-PPO suy giảm ít hơn Fixed-PPO trên ≥ 2/4 bộ OOD ở cả 2 seed, thì **thu hẹp hoặc đổi trọng tâm** (hướng A5: vai trò của lựa chọn tốc độ; hoặc chuyển sang đa UAV).
- **What observation would indicate a bug:**
  - smoke test không tái lập kết quả TSP tham chiếu;
  - mã băm kịch bản (`data/eval_manifest.json`) không khớp;
  - Random có AoI thấp hơn PPO đã huấn luyện;
  - AoI > T hoặc năng lượng âm;
  - chính sách dùng ≥ 90% một loại hành động;
  - tỷ lệ chạm biên > 0 khi đã bật mask;
  - kết quả hai seed lệch nhau hơn khoảng biến thiên giữa các episode.

## Section 5: Logistics & Execution

- **Available hardware / datasets / checkpoints:** **[cần điền — FAO trước 21/10]**: máy của từng thành viên (CPU, RAM, GPU), Kaggle T4 (30 GPU-giờ/tuần, như dự án RIVF). Không cần dataset ngoài: mọi kịch bản sinh từ seed (`data/eval_manifest.json`). Checkpoint chính sách lưu ngoài git (`runs/`); SHA256 ghi trong `data/checkpoint_manifest.md`.
- **Missing prerequisites, owner, and resolution date:**
  - `train_ppo.py` chưa từng chạy với PyTorch — FAO — 22/10 (issue #5).
  - Xác nhận giảng viên hướng dẫn, quy định cộng điểm và hội nghị đích — DAT — 25/10 (issue #7).
  - Đọc toàn văn các công trình gần nhất — cả nhóm — 01/11 (Gate G0, issue #1).
- **Estimated pilot compute cost:** **[cần đo — FAO, 23/10]**: thời gian 100k bước MaskablePPO trên từng máy. Sau đó tính chi phí: (số learner) × (số seed) × (số bước). Mốc tham chiếu: môi trường chạy khoảng 4 300 bước/giây trên 1 nhân CPU (đo khi dựng bộ mã), chưa tính cập nhật mạng.
- **Measurement rule:** mọi số đo thời gian (huấn luyện, suy luận) chạy trên **một máy cố định, đứng yên** do DAT chỉ định. Không lấy số thời gian từ Kaggle/Colab. Kaggle chỉ dùng để chạy thêm seed.
- **Student responsibilities and second readers:**
  - **FAO — Nguyễn Minh Chính:** môi trường chạy và tái lập, smoke test trên máy nhóm, đo chi phí tính toán, provenance checkpoint (`data/checkpoint_manifest.md`), DQN, script vẽ quỹ đạo. Second reader: DAT hoặc LDN.
  - **LDN — Dương Ngọc Linh Đan:** ma trận thực nghiệm và thống kê (experiment card, `analyze.py`, gate report, nhân bản theo seed), bảng claim–evidence, hình F3–F5 sinh từ raw. Second reader: FAO hoặc DAT.
  - **DAT — Hồ Du Tuấn Đạt:** phương pháp DR-PPO (huấn luyện, Optuna, biến thể quan sát cho ablation A2/A3), định vị đóng góp (Gate G0), điều phối với giảng viên và hội nghị, đo thời gian trên máy cố định, chủ trì bản thảo. Second reader: FAO hoặc LDN.
  - Mọi kết quả phải có second reader ký tên trong bảng claim–evidence trước khi vào bài.
- **Day-0 và các gate:** Day 0 = **thứ Hai 19/10/2026**.
  - G0 (Day 13) = CN 01/11
  - G1 (Day 27) = CN 15/11
  - G2 (Day 62) = CN 20/12
  - G3 (Day 83) = CN 10/01/2027
  - Lịch chi tiết: `docs/05_ke_hoach.md`.
