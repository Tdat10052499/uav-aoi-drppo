# EXP-03 — Thí nghiệm chính DR-PPO vs Fixed-PPO, 10 seed (bằng chứng cho H1, H2 — bài FJCAI)

**Owner:** DAT (huấn luyện) · **Phân tích:** LDN · **Second reader:** FAO
**Viết:** 03/11/2026, trước khi chạy (Claude soạn cho DAT, DAT duyệt 03/11)
**Chạy:** sau khi khoá PREREG (tag `prereg-lock`), 04/11–10/11/2026

## D. Experiment card

```text
Experiment ID: EXP-03
Owner / second reader: DAT (train) + LDN (analysis) / FAO
Thăm dò hay khẳng định: KHẲNG ĐỊNH. Giả thuyết, ngưỡng và phân tích theo docs/PREREG.md
  (khoá trước khi chạy). Không xem kết quả từng phần để đổi phân tích.

Câu hỏi: DR có làm giảm độ suy giảm OOD của PPO so với cùng learner huấn luyện trên một
  bố trí cố định không, khi không huấn luyện lại?
Giả thuyết: theo PREREG (H1: deg(DR) < deg(Fixed) trên các bộ OOD; H2 theo PREREG).

Biến thay đổi: phân phối huấn luyện {TRAIN_DR, TRAIN_FIXED}
Điều kiện cố định: MaskablePPO, SmallCNN, siêu tham số mặc định train_ppo.py, λ=0,1,
  configs/env_default.json, 2.000.000 bước, commit = prereg-lock
Đối chứng: Fixed-PPO; Random, Greedy, TSP (cùng 100 seed đánh giá)
Kiểm soát: cùng kiến trúc, ngân sách, seed huấn luyện {0..9} cho hai nhánh; đánh giá
  trên 100 kịch bản cố định (seed 100000–100099)
Bộ đánh giá: id, ood_cluster, ood_density, ood_area, ood_energy
Chỉ số: Ā (khe), deg = (Ā_ood − Ā_id)/Ā_id theo từng seed; phụ: năng lượng, tỷ lệ hết pin,
  tỷ lệ hover/chậm/nhanh, chạm biên, peak AoI (mô tả)
Đơn vị lặp: seed huấn luyện (n = 10/nhánh)
Thống kê: bootstrap 95% CI, IQM, kiểm định hoán vị một phía, Holm trên 4 bộ OOD, Cliff's δ
Thứ tự chạy: 2 tiến trình song song, một tiến trình DR và một tiến trình Fixed, seed tăng dần
  0→9 (cả hai nhánh luôn ở cùng seed, tránh trôi máy lệch một nhánh)
Thất bại: theo tiêu chí loại của PREREG; mọi lần chạy hỏng hoặc chạy lại được liệt kê
Chi phí: 20 × 2M = 40M bước; ước tính 17–29 giờ máy trên laptop DAT (chưa đo ở 2M)
Mốc: ≥ 5 seed/nhánh trước 10/11 (điều kiện dừng FJCAI)
Phân tích: scripts/analyze.py → results/processed/EXP-03_summary.md; LDN
Trường raw cần: events.csv, run_record.json (checkpoint_digest, steps_per_s)

Kết quả kỳ vọng nếu H1 đúng: ≥ 3/4 bộ OOD có p sau Holm < 0,05 và Δ_s ≥ δ = 0,10
  (PREREG §8) → "ủng hộ H1".
Kết quả làm yếu / bác bỏ: < 3/4 bộ đạt, hoặc có ý nghĩa thống kê nhưng Δ_s < 0,10 → bài
  báo cáo mô tả (CI, IQM, Cliff's δ), không tuyên bố H1. Δ_s ≤ 0 trên đa số bộ → báo cáo
  là bằng chứng ngược H1 (bản đồ căn tâm tự tổng quát hoá; xem kết quả làm yếu EXP-02).
Tiêu chí tiếp tục/dừng khai báo trước: PREREG §10 — đến 10/11 chưa đủ ≥ 5 seed/nhánh
  hoàn tất thì bỏ FJCAI; run hỏng xử lý theo §9 (NaN → chạy lại 1 lần với seed + 100).
```

(3 trường cuối thêm 03/11 theo góp ý 1 của FAO, dùng đúng đề xuất của FAO và PREREG §8, §10.)

## Lệnh (PowerShell, mỗi cửa sổ một nhánh)

```powershell
# Cửa sổ 1 — DR
foreach ($s in 0..9) { python scripts/train_ppo.py --experiment-id EXP-03 --train dr --masked --seed $s --timesteps 2000000 }
# Cửa sổ 2 — Fixed
foreach ($s in 0..9) { python scripts/train_ppo.py --experiment-id EXP-03 --train fixed --masked --seed $s --timesteps 2000000 }
```

Đánh giá (góp ý 5 của FAO), mỗi model một lệnh, nhãn đúng nhánh, `--run-id` riêng để 2 cửa sổ không trùng thư mục:

```powershell
python scripts/evaluate.py --experiment-id EXP-03 --run-id eval_dr_s<s> --model runs\EXP-03\<run-id>\model.zip --label dr_ppo --train-seed <s> --episodes 100
python scripts/evaluate.py --experiment-id EXP-03 --run-id eval_fixed_s<s> --model runs\EXP-03\<run-id>\model.zip --label fixed_ppo --train-seed <s> --episodes 100
python scripts/analyze.py results/raw/EXP-03/*/events.csv --proposed dr_ppo --fixed fixed_ppo --heuristic tsp --out results/processed/EXP-03_summary.md
```

## Second reader (FAO), 03/11/2026

Đã đọc card và đối chiếu với `docs/PREREG.md` (PR #38), `notes/EXP-02_pilot_card.md`, `scripts/train_ppo.py` và `scripts/analyze.py` tại 7923c39. Lệnh, ngân sách, seed và bộ đánh giá khớp PREREG. **Duyệt khi DAT xử lý mục 1.** Các mục 2–7 không chặn.

1. **Thiếu 3 trường của Form D** (`notes/workbook_forms.md`, có trong EXP-02): "Kết quả kỳ vọng nếu đúng", "Kết quả làm yếu" và "Tiêu chí tiếp tục/dừng". Card khẳng định nên phải nói trước kết quả nào làm yếu H1. Đề xuất: kỳ vọng = H1 có ý nghĩa sau Holm ở ≥ 3/4 bộ OOD và đạt ngưỡng PREREG §8; làm yếu = < 3/4 bộ, hoặc đạt thống kê nhưng dưới ngưỡng (khi đó bài báo cáo mô tả, không tuyên bố H1); dừng = điều kiện 10/11 ở PREREG §10.
2. **Chi phí:** 40 M / 358,4 bước/s = 31,0 h nếu chạy tuần tự (`Project Agreement.md` §5), không phải 29 h. Mức 17–20 h khi chạy 2 tiến trình song song chưa đo, vì hai tiến trình × 8 env cùng chia CPU.
3. **Thời gian:** `steps_per_s` của các lần chạy song song không dùng làm số đo thời gian cho bài (PREREG §5, quy tắc 4 CLAUDE.md).
4. **Heuristic:** đánh giá lại Random, Greedy-AoI, TSP tại commit `prereg-lock` với `--experiment-id EXP-03`, rồi so với EXP-01 bằng `scripts/compare_events.py`. Lý do: PREREG §9 tiêu chí 4 loại số liệu ở commit khác commit khoá.
5. **Lệnh đánh giá** nên ghi rõ thay cho "theo mẫu EXP-02", để nhãn không lẫn giữa hai nhánh:
   `python scripts/evaluate.py --experiment-id EXP-03 --model runs/EXP-03/<run-id>/model.zip --label dr_ppo --train-seed <s>` (Fixed: `--label fixed_ppo`), và
   `python scripts/analyze.py results/raw/EXP-03/*/events.csv --proposed dr_ppo --fixed fixed_ppo --heuristic tsp --out results/processed/EXP-03_summary.md`.
6. **PowerShell:** chạy trong venv đã kích hoạt, hoặc thay `python` bằng `.\.venv\Scripts\python.exe`. Vòng `foreach` vẫn chạy tiếp khi một seed lỗi, đúng ý "giữ record failed"; seed thay thế theo PREREG §9 (`seed + 100`).
7. **Seed 0 và 1 trùng pilot EXP-02** (300k bước). Không gộp model pilot vào EXP-03. Quyết định chạy EXP-03 dựa trên Ā(id) của pilot, không dựa trên deg, nên không ảnh hưởng H1.

Second reader (FAO) đã đọc card: có, chờ mục 1  ngày: 03/11/2026
