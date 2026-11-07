# LDN → DAT, FAO: power cho H5–H7 và baseline của H5 (06/11/2026)

> Trả lời bằng dòng `DAT:` / `FAO:` dưới mỗi mục. **Hạn:** trước khi khoá PREREG phụ lục B (G1, 20/11). Các mục B1–B3 cần trả lời sớm, vì `W5-FAO-03` (đưa phụ lục B vào `docs/PREREG.md`) phụ thuộc `W4-LDN-04`.
> Căn cứ:
> - `notes/2026-11-06_ldn_phuong-phap-H5-H7.md` §4b: power dùng CV đo trên raw EXP-03; script ở PR #51.
> - `notes/2026-11-06_ldn_EXP-08a_chan-doan.md`: EXP-08a, PR #50.

## B1. Hiệu ứng mục tiêu để tính power

- **Vì sao phải chọn.** Quy tắc "p_Holm < 0,05 **và** ước lượng ≥ δ" chỉ cho khoảng 25% power khi hiệu ứng thật **đúng bằng** δ, dù dùng bao nhiêu seed. Lý do: cả hai bộ phải đạt, và ở mỗi bộ ước lượng rơi dưới δ một nửa số lần. Vì vậy power chỉ có nghĩa khi đọc ở một hiệu ứng mục tiêu lớn hơn δ, và hiệu ứng đó phải ghi vào phụ lục B trước khi khoá.
- **LDN đề xuất:**
  - H5, H7: hiệu ứng thật **1,5δ = 0,15**;
  - H6: tỉ số thật Ā_M1/Ā_TSPa = **0,95**.
  - Mục tiêu power: ≥ 0,8.

DAT: Đồng ý. H5, H7 tính power tại hiệu ứng thật 1,5δ = 0,15; H6 tại tỉ số thật 0,95; mục tiêu power ≥ 0,8. Ghi cả lý do (quy tắc kép p_Holm và ước lượng ≥ δ ở hai bộ cho power ≈ 25% khi hiệu ứng thật đúng bằng δ) vào phụ lục B. (06/11/2026)

FAO: (06/11) Đồng ý. Đã chạy lại `scripts/power_b.py` (nhánh `ldn/power-b`, b7535aa) trên raw EXP-03: CV đo được 0,020–0,118, khớp. Lý do "≈ 25%" đúng: mỗi bộ có khoảng 50% khi hiệu ứng thật bằng δ (docstring của script), và hai bộ phải cùng đạt. Mô phỏng cho 0,24–0,26 ở cột ρ = δ.

## B2. Số seed cho H5 và H6

CV đo trên EXP-03 nằm trong 0,02–0,12. Power tính với CV 0,10 và 0,15 (0,15 ≈ 1,25 × CV lớn nhất).

| | n = 10 |
| --- | --- |
| H5, ρ = 0,15 | 0,79–0,94 |
| H6, tỉ số thật 0,95 | 0,93–1,00 |
| H6, nếu M1 chỉ ngang TSPa (tỉ số 1,00) | 0,59–0,90 |

- **LDN đề xuất:** giữ **10 seed** (10–19) cho H5 và H6.
- Nếu M1 chỉ ngang TSPa trên id2 thì H6 thiếu power; ghi điều này là giới hạn.

DAT: Đồng ý giữ 10 seed (10–19) cho H5 và H6. Ghi vào giới hạn của phụ lục B: nếu M1 chỉ ngang TSP-adaptive trên id2 thì H6 có power 0,59–0,90. (06/11/2026)

FAO: (06/11) Đồng ý 10 seed. Chạy lại với n = 10:
  - H5 ρ = 0,15: 0,94 (CV 0,10) và 0,79 (CV 0,15). Khớp.
  - H6 tỉ số 0,95: 1,00 và 0,90–0,92. H6 tỉ số 1,00: 0,90 và 0,60–0,67. Thay seed mô phỏng thì lệch ±0,03 ở 2000 lượt mô phỏng, nên 0,93 của LDN nằm trong sai số.
  - Đề xuất ghi vào phụ lục B: số lượt mô phỏng, seed mô phỏng và commit script, để bảng power tái lập được.
  - Lưu ý: CV của nhánh DR trong EXP-03 có thể thấp hơn thật, vì 7/8 luồng kịch bản dùng chung giữa các seed (DECISIONS 06/11). EXP-08 dùng `spaced`, nên dùng CV 0,15 là hợp lý.

## B3. H7 thiếu power khi gap nhỏ

- **Định nghĩa.** gap = (Ā_Random − Ā_TSPa)/Ā_M1. Với CV 0,15, power tại hiệu 0,15 là:
  - n = 10: 0,44 (gap 1,0) và 0,10 (gap 0,6);
  - n = 20: 0,73 (gap 1,0).
- **Chưa biết gap thật.** Gap của `ood_energy_low` chỉ có sau pilot. Trên `ood_energy` cũ, gap ≈ 1,2 nếu M1 ngang TSP, và ≈ 0,5 nếu M1 chỉ ngang DR-PPO cũ.
- **LDN đề xuất:**
  - ghi power thấp của H7 vào phụ lục B;
  - sau pilot, nếu gap < 1 thì nhóm chọn **trước khi khoá**: tăng lên 15–20 seed cho M1 và M3, hoặc hạ H7 xuống thăm dò.

DAT: Đồng ý. Ghi power thấp của H7 vào phụ lục B. Sau pilot, nếu gap < 1 thì nhóm chọn trước khi khoá: 15–20 seed cho M1 và M3, hoặc hạ H7 xuống thăm dò; ghi lựa chọn vào DECISIONS. (06/11/2026)

FAO: (06/11) Đồng ý. Chạy lại khớp: n = 10, gap 1,0, CV 0,15 cho 0,44; n = 20 cho 0,73. Ngưỡng gap < 1 và hai lựa chọn phải chốt trước khi khoá, kèm cách đo gap (trung bình 2 seed pilot, chỉ trên bộ cũ hay có `--probe-b`).

## B4. (mới, từ EXP-08a) H5 có thể thắng một baseline đã bị làm yếu

**Dữ kiện** (EXP-08a, PR #50; thăm dò, tương quan):
- Theo mô hình năng lượng của repo, V_mr tốn 31,3 J/m, V_me tốn 43,5 J/m. V_mr là tốc độ tiết kiệm nhất khi di chuyển.
- PPO thua TSP trên `ood_energy` vì phủ kém (coverage 0,07 so với 1,00) và chủ yếu bay ở V_me. PPO **không** hết pin sớm hơn TSP: khe dừng 186 so với 153.

**Từ mã** (`src/uavaoi/baselines.py`, `TSPAdaptivePolicy`): TSP-adaptive bay ở V_mr khi ρ_E > 1, và **chuyển sang V_me** khi pin thấp. Đây đúng là chiều tốn năng lượng hơn trên mỗi mét.

**Rủi ro (suy luận, chưa đo):**
- Trên bộ pin thấp, TSP-adaptive có thể **yếu hơn TSP thường**.
- Khi đó H5 ("M1 thắng TSP-adaptive khi pin thấp") có thể đạt nhờ baseline yếu. Reviewer sẽ hỏi vì sao không so với TSP thường.
- Mốc S (Random → TSP-adaptive) cũng làm điểm S của M1 bị thổi phồng.
- Rủi ro này đánh thẳng vào kết quả "rõ ràng" mà EXP-08 cần.

**LDN đề xuất** (nhóm chọn):
1. **Kiểm trước.** Chạy Random, TSP, TSP-eco và TSP-adaptive trên `ood_energy` cũ (seed 100000–100099; chỉ heuristic, vài phút). Phép kiểm này phải **ghi vào card trước khi chạy** (quy tắc 1), ví dụ thêm mục "EXP-08a-b" vào card EXP-08. DAT hoặc FAO thêm, vì nằm ngoài phạm vi EXP-08a hiện tại. Nếu cần đo trên `ood_energy_low` thì dùng `--probe-b` và khai báo ở phụ lục B §1.
2. **Sửa H5 cho chặt hơn.** So M1 với **heuristic tốt nhất trên từng bộ**, tức min Ā của TSP, TSP-eco và TSP-adaptive. Tương tự, mốc S dùng heuristic tốt nhất. Cách kiểm sign-flip của H5 giữ nguyên, vì heuristic tốt nhất vẫn là một hằng số trên mỗi bộ.
3. Nếu giữ TSP-adaptive làm baseline chính, thì sửa nó để giữ V_mr khi di chuyển, và chỉ dùng thêm thời gian chờ hoặc bỏ điểm khi pin thấp. Việc sửa phải xong và được ghi DECISIONS trước khi khoá.
4. **Sửa câu G3 ở thiết kế §1.** Câu "TSP vì vậy không tiết kiệm năng lượng" mâu thuẫn với mô hình năng lượng của repo. Không đưa câu này vào bài.

LDN nghiêng về (1) + (2): chặt nhất, và không cần sửa mã baseline.

DAT: Chọn (1) + (2) + (4), không làm (3). (06/11/2026)
- (1) Đã thêm mục **EXP-08a-b** vào `notes/EXP-08_PG-TG-PPO_card.md` (thăm dò, chỉ heuristic), có tiêu chí hành động ghi trước. LDN chạy, FAO đọc lại.
- (2) H5 và mốc S dùng **heuristic tốt nhất trên từng bộ** = argmin Ā của {TSP, TSP-eco, TSP-adaptive}. Đề xuất chốt trong phụ lục B: heuristic tốt nhất được chọn trên **chính các seed khẳng định** (300000–300099) và **chỉ từ kết quả heuristic**, trước khi xem số của M1. Lấy min trên ba baseline nghiêng về phía baseline, tức là bảo thủ cho H5. LDN xem giúp cách này có làm thay đổi phép kiểm sign-flip không.
- (4) Bỏ câu "TSP vì vậy không tiết kiệm năng lượng" ở thiết kế §1; G3 sẽ viết lại theo kết quả EXP-08a-b (chỗ thắng nằm ở thứ tự, bỏ điểm, treo, không ở tốc độ bay). Không đưa câu cũ vào bài.

FAO: (06/11) Đồng ý (1) + (2) + (4). Đã kiểm dữ kiện từ mã:
  - Năng lượng mỗi mét từ số của repo: một khe V_me 2806,9 J / (21,49 m/s × 3 s) = 43,5 J/m; một khe V_mr 3598,6 J / (38,27 × 3) = 31,3 J/m. Khớp.
  - `TSPAdaptivePolicy._speed` trả "fast" (V_mr) khi ρ_E > 1, ngược lại "slow" (V_me) (`baselines.py:152–153`). Đúng như LDN nêu.
  - `TSPEcoPolicy` luôn bay V_me, nên theo mô hình này cũng tốn năng lượng nhất trên mỗi mét. Docstring "the obvious energy-saving fix" chỉ đúng theo công suất, không đúng theo năng lượng trên quãng đường. Bài không nên gọi TSP-eco là "tiết kiệm năng lượng".
  - Hết pin sớm không giúp gì cho Ā: `env.py` cộng AoI cho mọi khe còn lại tới T (dòng 173–186). Vì vậy dự đoán Ā(TSP-adaptive) ≥ Ā(TSP) có cơ sở (suy luận, chưa đo).
  - Về (2): heuristic tốt nhất nên chốt là argmin của **Ā trung bình theo bộ** (100 episode), không phải min theo từng episode. Min theo từng episode là oracle theo kịch bản, không phải một baseline. Thứ tự chạy sau tag: heuristic trước, ghi lựa chọn vào DECISIONS, rồi mới đánh giá M1. Baseline vẫn là hằng số trên mỗi bộ, nên phép sign-flip của H5 không đổi (`power_b.py` cũng mô phỏng như vậy).
  - Góp ý cho card EXP-08a-b: ghi ở cuối mục đó trong `notes/EXP-08_PG-TG-PPO_card.md`.
