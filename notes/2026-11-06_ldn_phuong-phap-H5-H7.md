# Cách kiểm H5–H7 và power analysis cho PREREG phụ lục B (nháp W4-LDN-04)

> Trạng thái: **nháp chờ LDN duyệt** (cập nhật 06/11 tối: §4b dùng CV đo trên raw EXP-03). Claude soạn ngày 06/11/2026 cho LDN, trước khi raw EXP-03 lên `main`. Mọi bảng power dưới đây dùng **lưới CV giả định**, không dùng số EXP-03. Khi có raw, chạy lại `scripts/power_b.py --from-exp03 ...` rồi thay bảng (nhánh `ldn/power-b`).
> Nguồn định nghĩa: `notes/2026-11-06_dat_PREREG-phu-luc-B_nhap.md` §4–5. Mốc S là Random, đã ký ở card EXP-08 ("Second reader LDN").

## 1. H5: so M1 với TSP-adaptive (heuristic tất định)

**Vấn đề.** TSP-adaptive tất định: trên bộ kịch bản cố định (seed 300000–300099), nó cho đúng một giá trị Ā_TSPa mỗi bộ. Không có "phân phối seed" để so hai mẫu.

| Cách | Mô tả | Đánh giá |
| --- | --- | --- |
| (a) **Đề xuất** | Với mỗi seed i: d_i = (Ā_TSPa − Ā_M1,i)/Ā_TSPa. Kiểm **sign-flip một mẫu chính xác**, một phía, trên 10 giá trị d_i (liệt kê đủ 2¹⁰ = 1 024 cách đổi dấu). | Đơn vị lặp là seed, đúng PREREG. Suy luận có điều kiện trên bộ 100 kịch bản chung, và Ā_TSPa coi là hằng số. Với n = 10, p nhỏ nhất là 1/1 024 ≈ 0,001, đủ cho Holm 2 bộ. |
| (b) Không dùng | Hai mẫu: 10 trung bình seed của M1 so với 100 episode của TSPa. | Trộn đơn vị lặp (seed so với episode), cùng lỗi đã ghi cho H2 ở PREREG §7. p sai. |
| (c) Báo kèm | Bootstrap hai tầng ghép cặp: lấy lại seed, rồi lấy lại 100 kịch bản chung cho cả M1 lẫn TSPa. | Cho CI của mức giảm tương đối khi kể cả biến thiên kịch bản. Chỉ để mô tả và kiểm độ nhạy; không dùng để quyết định. |

**Quy tắc đạt (giữ như bản nháp phụ lục B):** trên **cả hai** bộ `ood_energy_low` và `ood_combo`, p_Holm < 0,05 **và** mean(d) ≥ δ₅. Vì Ā_TSPa là hằng số nên mean(d) = 1 − mean(Ā_M1)/Ā_TSPa.

**Cần sửa chữ trong phụ lục B §4:** "20 000 hoán vị" chỉ áp dụng cho kiểm hai mẫu (H7). H5 dùng sign-flip chính xác 1 024 cách. Nếu n > 12 thì dùng Monte Carlo 4 096 cách (`power_b.signflip_matrix`).

## 2. H6: không thua trên id2 (non-inferiority)

- r_i = Ā_M1,i / Ā_TSPa. Đạt khi **cận trên CI 95% hai phía** của mean(r) < 1 + δ₆. CI 95% hai phía tương đương α = 0,025 một phía, đúng quy ước chặt của kiểm không thua.
- CI theo bootstrap phân vị trên 10 seed (10 000 mẫu, seed 0). Với n = 10, bootstrap phân vị thường hơi hẹp, nên báo kèm khoảng t để kiểm độ nhạy. Quyết định vẫn theo bootstrap, đúng như đã ghi.
- H6 là một phép thử đơn, không nằm trong họ Holm nào.

## 3. H7: vai trò của quan sát neo

- S = (Ā_Random − Ā)/(Ā_Random − Ā_TSPa) cho từng seed của M1 và M3; các seed độc lập nhờ scheme `spaced` (PR #45).
- Kiểm **hoán vị hai mẫu** một phía trên mean(S_M1) − mean(S_M3), 20 000 hoán vị, Holm qua 2 bộ (`ood_energy_low`, `ood_area_2000`). Đạt khi p_Holm < 0,05 **và** hiệu ≥ δ₇ trên cả hai bộ.
- Vì Ā_Random và Ā_TSPa là hằng số trong một bộ, kiểm trên S tương đương kiểm trên Ā. δ₇ đặt trên thang S.
- **Độ nhạy của S:** SD(S) = CV · Ā_M / (Ā_Random − Ā_TSPa). Nếu khoảng Random→TSPa hẹp so với Ā của M, S rất nhiễu. Theo card EXP-08 (chữ ký LDN), khi Ā_Random − Ā_TSPa < 10 khe thì gắn cờ.

## 4. Power (mô phỏng, `scripts/power_b.py`; lưới CV giả định, chưa có số EXP-03)

**Tính chất không phụ thuộc dữ liệu.** Quy tắc "có ý nghĩa **và** điểm ước lượng ≥ δ" chỉ có khoảng 50% power cho mỗi bộ khi hiệu ứng thật **đúng bằng** δ, bất kể bao nhiêu seed, vì điểm ước lượng rơi dưới δ một nửa số lần. Với hai bộ cùng phải đạt, con số này còn khoảng 25%; mô phỏng cho 0,24–0,26 ở mọi dòng. Như vậy:
- Power phải đọc ở một **hiệu ứng mục tiêu** lớn hơn δ.
- **Nhóm cần ghi hiệu ứng mục tiêu vào phụ lục B trước khi khoá**, ví dụ "power ≥ 0,8 tại hiệu ứng thật 1,5δ". Nếu không, mọi con số power đều vô nghĩa.

Bảng (2 000 mô phỏng, seed 0, δ = 0,10, gap = (Ā_Random − Ā_TSPa)/Ā_M1 = 1,0):

**H5: power theo mức giảm tương đối thật ρ (cả 2 bộ phải đạt)**

| n | CV | ρ = 0,10 | 0,15 | 0,20 | 0,30 |
| --- | --- | --- | --- | --- | --- |
| 10 | 0,10 | 0,26 | 0,94 | 1,00 | 1,00 |
| 10 | 0,20 | 0,18 | 0,61 | 0,93 | 1,00 |
| 15 | 0,20 | 0,24 | 0,76 | 0,98 | 1,00 |
| 20 | 0,20 | 0,25 | 0,82 | 0,99 | 1,00 |

**H6: power theo tỉ số thật Ā_M1/Ā_TSPa trên id2 (biên 1,10)**

| n | CV | 0,90 | 0,95 | 1,00 | 1,05 |
| --- | --- | --- | --- | --- | --- |
| 10 | 0,10 | 1,00 | 1,00 | 0,90 | 0,37 |
| 10 | 0,20 | 0,94 | 0,74 | 0,41 | 0,16 |
| 15 | 0,20 | 0,99 | 0,89 | 0,53 | 0,18 |
| 20 | 0,20 | 1,00 | 0,94 | 0,64 | 0,22 |

**H7: power theo hiệu thật S_M1 − S_M3 (cả 2 bộ phải đạt; SD(S) = CV/gap)**

| n | CV | 0,10 | 0,15 | 0,20 | 0,30 |
| --- | --- | --- | --- | --- | --- |
| 10 | 0,10 | 0,26 | 0,72 | 0,97 | 1,00 |
| 10 | 0,20 | 0,06 | 0,20 | 0,48 | 0,87 |
| 15 | 0,20 | 0,11 | 0,39 | 0,71 | 0,98 |
| 20 | 0,20 | 0,19 | 0,54 | 0,85 | 1,00 |

**Đọc bảng (vẫn là giả định):**
- **H5:** n = 10 đủ nếu CV ≤ 0,10 và hiệu ứng thật ≥ 1,5δ. Nếu CV khoảng 0,20 thì cần hiệu ứng ≥ 2δ hoặc 20 seed.
- **H6:** khó nhất khi M1 ngang TSPa. Với CV 0,20, cả 20 seed cũng chỉ cho 0,64. Nếu nhóm kỳ vọng M1 xấp xỉ TSPa trên id2 thì H6 cần CV thấp hoặc nhiều seed.
- **H7:** yếu nhất, vì S khuếch đại nhiễu khi gap nhỏ. Với CV 0,20 và gap 1, n = 10 chỉ có 0,48 ở hiệu 2δ. Trên các bộ cũ, gap ước lượng từ heuristic (TSP thay TSPa, Ā_M1 = Ā_TSP) là 1,2 (`ood_energy`) đến 4,9 (`ood_cluster`). Riêng `ood_energy_low` chưa biết và có thể nhỏ hơn.

## 4b. Cập nhật 06/11 tối: CV đo trên raw EXP-03

Chạy `power_b.py --from-exp03 'results/raw/EXP-03/eval_*/events.csv'` (nhánh `ldn/power-b`, b7535aa). Kết quả là CV của trung bình Ā theo seed, 10 seed mỗi nhánh:

| Bộ | DR | Fixed |
| --- | --- | --- |
| id | 0,070 | 0,081 |
| ood_cluster | 0,054 | **0,118** |
| ood_density | 0,068 | 0,053 |
| ood_area | 0,049 | 0,020 |
| ood_energy | 0,022 | 0,031 |

**CV dùng cho power: 0,10 (điển hình) và 0,15 (thận trọng).** 0,15 ≈ 1,25 × 0,118, tức CV lớn nhất đo được, nhân thêm vì CV của DR có thể bị đánh giá thấp (7/8 chuỗi kịch bản dùng chung). Lưu ý: M1 là phương pháp khác, trên bộ khác, nên CV của nó có thể khác; pilot EXP-08p cho thêm 2 điểm để kiểm.

Bảng (2 000 mô phỏng, seed 0, δ = 0,10; tệp đầy đủ do `power_b.py --n 10 15 20 --cv 0.10 0.15 --gap {1.0, 0.6}` sinh ra):

**H5** (cả 2 bộ phải đạt), power tại mức giảm thật ρ:

| n | CV | ρ = 0,15 | ρ = 0,20 |
| --- | --- | --- | --- |
| 10 | 0,10 | 0,94 | 1,00 |
| 10 | 0,15 | 0,79 | 0,99 |
| 15 | 0,15 | 0,88 | 1,00 |

**H6**, power tại tỉ số thật Ā_M1/Ā_TSPa:

| n | CV | 0,95 | 1,00 | 1,05 |
| --- | --- | --- | --- | --- |
| 10 | 0,10 | 1,00 | 0,90 | 0,37 |
| 10 | 0,15 | 0,93 | 0,59 | 0,24 |
| 20 | 0,15 | 1,00 | 0,87 | 0,34 |

**H7** (cả 2 bộ), power tại hiệu thật S_M1 − S_M3:

| n | CV | gap | 0,15 | 0,20 | 0,30 |
| --- | --- | --- | --- | --- | --- |
| 10 | 0,10 | 1,0 | 0,72 | 0,97 | 1,00 |
| 10 | 0,15 | 1,0 | 0,44 | 0,78 | 0,99 |
| 10 | 0,15 | 0,6 | 0,10 | 0,28 | 0,68 |
| 20 | 0,15 | 1,0 | 0,73 | 0,96 | 1,00 |
| 20 | 0,15 | 0,6 | 0,34 | 0,64 | 0,95 |

**Gap trên dữ liệu cũ.** gap = (Ā_Random − Ā_TSP)/Ā_M1. Nếu M1 chỉ ngang TSP: `ood_energy` (133,9 − 60,5)/60,5 = 1,21; `ood_area` (137,9 − 35,6)/35,6 = 2,87. Nếu M1 chỉ ngang DR-PPO cũ trên `ood_energy` (147,6), gap = 0,50. Bộ `ood_energy_low` còn ít pin hơn nên gap có thể nhỏ hơn 1.

**Đề xuất của LDN (nhóm quyết định trước khi khoá phụ lục B):**
1. **Hiệu ứng mục tiêu 1,5δ = 0,15** cho H5, H7; tỉ số thật 0,95 cho H6.
2. **H5:** n = 10 đủ (0,79–0,94 tại ρ = 0,15).
3. **H6:** n = 10 đủ nếu M1 tốt hơn TSPa ít nhất 5% trên id2 (0,93–1,00). Nếu M1 chỉ ngang TSPa thì power 0,59–0,90; ghi rõ là giới hạn.
4. **H7:** n = 10 chỉ đủ khi CV ≤ 0,10 và gap ≥ 1. Với CV 0,15 thì kể cả 20 seed cũng chỉ 0,73 tại 0,15. Đề xuất ghi power thấp của H7 vào phụ lục B và báo cáo H7 kèm CI, không tăng seed trước pilot. Sau pilot, nếu gap của `ood_energy_low` < 1, nhóm chọn giữa 15–20 seed cho M1 và M3, hoặc hạ H7 xuống thăm dò. Việc chọn phải xong **trước** khoá.

## 5. Việc khi có raw EXP-03 (W4-LDN-04)

> 06/11 tối: bước 1 đã làm (§4b). Bước 2 chờ nhóm trả lời §6. Bước 3 chờ pilot.


1. Chạy `python scripts/power_b.py --from-exp03 'results/raw/EXP-03/*/events.csv' --n 10 15 20 --cv <CV đo được>`.
   - Lấy **CV lớn hơn** giữa nhánh DR và Fixed. CV của DR có thể bị đánh giá thấp vì 7/8 chuỗi kịch bản dùng chung (DECISIONS 06/11).
   - Cân nhắc nhân thêm 1,25 lần cho an toàn.
2. Ghi vào phụ lục B: CV dùng, hiệu ứng mục tiêu, power ở mỗi H, và số seed đề xuất nếu power < 0,8.
3. Gap của `ood_energy_low` và `ood_area_2000` chỉ biết sau pilot (Random và TSPa chạy trên bộ cũ trong pilot; bộ B bị chặn trước khoá). Dùng `--probe-b` cho heuristic nếu cần, và khai báo trong phụ lục B §1 như PR #45 yêu cầu.

## 6. Câu hỏi cho nhóm (trước khi khoá phụ lục B)

1. **Hiệu ứng mục tiêu** để tính power: 1,5δ hay 2δ?
2. Nếu H7 thiếu power: tăng seed cho riêng M1 và M3, gộp hai bộ thành một phép thử, hay chấp nhận H7 có power thấp và ghi rõ?
3. GVHD xác nhận δ₅–δ₇ = 0,10 (G1 #6).
