# FAO → DAT (cc LDN): các ô cần chốt cho PREREG phụ lục sau EXP-03 — 06/11/2026

> Trả lời bằng dòng `DAT:` (hoặc `LDN:`) dưới mỗi mục. Bối cảnh: DECISIONS 06/11 (PR #42) bỏ FJCAI và sửa phương pháp. Theo dòng đó, chỉ số mới là giả thuyết mới, cần PREREG phụ lục và seed mới. FAO soạn phụ lục (`docs/PREREG.md`, phần mới, khoá trước khi chạy) khi các ô dưới đây đã có câu trả lời. Đây là danh sách câu hỏi kèm đề xuất mặc định, chưa phải quyết định.
>
> **Lưu ý chung:** mọi lựa chọn ở đây đều được đưa ra *sau khi* đã thấy EXP-03. Bài phải ghi rõ điều này. Mỗi lựa chọn nên có lý do độc lập với kết quả EXP-03 (ví dụ một tính chất của chỉ số), không chỉ "vì EXP-03 không đạt".

## P1. Số bước mỗi trial Optuna (thẻ TUNE: 20 trial × 200k)
- **Vấn đề (dữ kiện):** ở 300k bước, DR-PPO có Ā(id) ≈ Random (126,1 và 123,4 so với 126,2; thẻ EXP-02b). Ở 2M bước là 49,80. Vì vậy trial 200k có thể chưa đủ để phân biệt các cấu hình: mục tiêu của các trial có thể chỉ là nhiễu quanh mức Random.
- **Đề xuất mặc định:** kiểm trước bằng đường học `ep_rew_mean` của EXP-02b và EXP-03 (log tensorboard). Nếu tới 200k mà đường còn phẳng thì tăng số bước mỗi trial (ví dụ 1M, giảm số trial để giữ ngân sách) hoặc dùng pruning theo đường học. **Cần DAT push log tb** của EXP-02b (`runs/` bị gitignore).
- DAT:

## P2. Seed huấn luyện mới
- **Đề xuất mặc định:** 10–19 cho cả hai nhánh. Seed 0–9 đã dùng cho EXP-03; trial Optuna dùng seed 1000.
- DAT:

## P3. Seed đánh giá mới cho phép thử khẳng định
- **Vấn đề:** 100 kịch bản test 100000–100099 đã được xem kết quả ở EXP-03. Nếu dùng lại chúng cho giả thuyết mới thì vẫn hợp lệ về mặt máy móc, nhưng khi chọn chỉ số người ta đã biết kết quả trên đúng các kịch bản đó.
- **Đề xuất mặc định:** bộ seed đánh giá mới 300000–300099, khác bộ kiểm định Optuna 200000–200019. `evaluate.py --seed-base 300000` đã có (PR #37). Cần thêm digest kịch bản cho bộ mới (`build_eval_manifest.py`) và kiểm ở smoke test. Bộ cũ 100000–100099 giữ để so sánh với EXP-03.
- DAT:

## P4. Chỉ số cho H1 mới (DAT, LDN)
Các lựa chọn, kèm tính chất. FAO không chọn thay nhóm:
- (a) **Ā tuyệt đối** trên từng bộ OOD: H1′ là Ā_DR(s) < Ā_Fixed(s). Đơn giản. Nhược điểm: đây là so sánh hiệu năng, không còn là "độ bền" khi dịch chuyển.
- (b) **Suy giảm tuyệt đối** Ā_ood − Ā_id: tránh chia cho Ā_id. Vẫn chịu hiệu ứng trần (Ā bị chặn khoảng 135–150 khi pin cạn sớm, theo `notes/2026-11-06_dat_EXP-03-so-bo.md` §4).
- (c) **Điểm chuẩn hoá theo heuristic** trên từng bộ, ví dụ (Ā_Random − Ā)/(Ā_Random − Ā_TSP), tương tự điểm chuẩn hoá trong Agarwal 2021. Khử thang đo và trần khác nhau giữa các bộ. Nhược điểm: phụ thuộc hai heuristic tham chiếu.
- (d) **deg so với phân phối huấn luyện của từng nhánh:** với Fixed, mốc là bố trí huấn luyện của nó (TRAIN_FIXED, fixed_seed 0), không phải `id`. Lý do độc lập với kết quả: `docs/03` §4 đã ghi rằng `id` là OOD với Fixed.
- **Dữ kiện cho cả 4 lựa chọn (FAO tính 06/11 từ `src/uavaoi/env.py`, dòng 87, 150, 178, 213):** AoI mỗi cảm biến bắt đầu bằng 1, mỗi khe tăng 1 và bị chặn ở Δ_max = T = 300. Ā tính trên toàn T, kể cả sau khi hết pin. Vì vậy một chính sách **không thu lần nào** có Ā = (Σ_{t=1..300} min(1+t, 300))/300 = **151,5 khe**, trên mọi bộ. Đây là trần cứng, không chỉ là "khoảng 135–150". EXP-02b DR s0 trên `ood_energy` đạt Ā = 146,36 với độ phủ 0,06, tức gần trần. Trên `ood_area` là 127,04 với độ phủ 0,39; 98% episode hết pin sớm (`events.csv`, 30913ce). Lựa chọn (c) có thể dùng 151,5 làm mốc "tệ nhất" thay cho Random, nên không phụ thuộc vào heuristic Random.
- **Ngưỡng ý nghĩa thực tiễn** cho chỉ số được chọn: LDN, chốt trước khi chạy, như §8.
- DAT/LDN:

## P5. Số bước huấn luyện chính
- **Đề xuất mặc định:** giữ 2M, trừ khi đường học (P1) cho thấy DR hoặc Fixed còn tăng rõ ở 2M. Nếu tăng thì cân nhắc 3–4M, nhưng chi phí tăng tuyến tính: 2M ≈ 22,8 h cho 20 run song song (thẻ EXP-03).
- DAT:

## P6. EXP-03 trong bài
- **Đề xuất mặc định:** báo cáo EXP-03 đầy đủ như kết quả khẳng định đã đăng ký và không đạt (DECISIONS 06/11). Phụ lục là một thực nghiệm mới, không thay EXP-03.
- DAT:
