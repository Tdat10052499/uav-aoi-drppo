# EXP-08a: PPO thua trên `ood_energy` vì hết pin sớm hay vì đi sai đường? (W4-LDN-03)

> **Thăm dò, chỉ mô tả.** Dữ liệu EXP-03 đã thấy; mọi nhận định dưới đây là tương quan, không phải nhân quả. Card: `notes/EXP-08_PG-TG-PPO_card.md`, mục "EXP-08a". Bảng: `results/processed/EXP-08a_diag.md`, sinh bởi `scripts/diag_exp08a.py` từ `results/raw/EXP-03/eval_*` và `heuristics_lock` (chỉ run `completed`). Second reader: FAO.
> LDN soạn (Claude hỗ trợ) ngày 06/11/2026, sớm hơn lịch (10–12/11) vì raw EXP-03 đã lên `main`.

## 1. Số chính (trích từ `results/processed/EXP-08a_diag.md`)

DR và Fixed là trung bình của 10 trung bình theo seed, kèm [min–max] các trung bình seed. Heuristic là trung bình 100 episode.

| Bộ | Nhánh | early_termination | t_end (khe) | fast (V_mr) | coverage | collections | Ā |
| --- | --- | --- | --- | --- | --- | --- | --- |
| id | DR | 0,65 | 292 | 0,15 | 0,96 | 81,2 | 52,1 |
| id | TSP | 0,95 | 255 | 0,58 | 1,00 | 107,0 | 28,6 |
| ood_energy | DR | 1,00 | 186 [149–209] | 0,14 [0,03–0,36] | 0,07 [0,01–0,21] | 20,6 | 147,6 |
| ood_energy | Fixed | 1,00 | 185 [169–211] | 0,13 | 0,13 | 25,5 | 145,1 |
| ood_energy | TSP | 1,00 | 153 | 0,58 | 1,00 | 64,3 | 60,5 |
| ood_energy | Greedy | 1,00 | 153 | 0,56 | 1,00 | 67,1 | 61,0 |
| ood_area | DR | 0,96 | 276 | 0,04 [0,01–0,06] | 0,46 | 78,4 | 123,3 |
| ood_area | TSP | 0,92 | 259 | 0,69 | 1,00 | 80,2 | 35,6 |

**Cách lấy `t_end`.** `events.csv` không có cột khe dừng. Theo `env.py`, `action_counts` đếm mỗi khe đã thực hiện một lần, nên t_end = số khe hover + V_me + V_mr. Chỉ dùng các tỉ lệ thì t_end mới xác định đến một ước chung, nên mỗi ứng viên được kiểm thêm bằng cân bằng năng lượng của `env.py`. Kết quả: 11 500/11 500 episode có đúng một nghiệm.

**Năng lượng mỗi mét** (`env.py`, preset `zeng2019_arxiv_v1`, δt = 3 s):
- V_me = 21,5 m/s, tốn 43,5 J/m;
- V_mr = 38,3 m/s, tốn **31,3 J/m**, ít hơn 28%.

V_mr là tốc độ tầm xa nhất (argmin P(V)/V); V_me là tốc độ bay lâu nhất (argmin P(V)).

## 2. Đối chiếu với dự đoán ghi trước

Dự đoán trong card: "trên ood_energy, PPO early_termination cao hơn rõ TSP và gần bằng id về fast_frac".

| Phần của dự đoán | Dữ kiện | Kết quả |
| --- | --- | --- |
| PPO hết pin sớm hơn rõ TSP | early_termination bằng nhau (1,00 ở mọi nhánh, chạm trần). PPO dừng **muộn hơn** TSP: t_end 186 so với 153 (DR), 185 (Fixed). Seed DR sớm nhất (149) cũng chỉ ngang TSP. | **Sai** |
| fast_frac của PPO trên `ood_energy` gần `id` | DR 0,14 so với 0,15; Fixed 0,13 so với 0,16 | Đúng |

Theo tiêu chí hành động của card, đây là nhánh **"Dự đoán sai (PPO không hết pin sớm hơn TSP) → xem lại G1 trước khi viết mã A; báo DAT."**

## 3. Mô tả (tương quan, không nhân quả)

1. **Đi sai đường khớp dữ kiện hơn là hết pin sớm.**
   - Trên `ood_energy`, PPO bay lâu hơn TSP khoảng 33 khe, nhưng chỉ thăm 7% (DR) đến 13% (Fixed) số cảm biến. TSP thăm 100%.
   - Số lần thu của PPO bằng khoảng một phần ba TSP (20,6 so với 64,3).
   - Trên `ood_area` cũng vậy: coverage 0,46 so với 1,00, dù t_end của DR (276) dài hơn TSP (259).
2. **PPO chủ yếu bay ở V_me.** Tỉ lệ slow là 0,64 trên `ood_energy` và 0,43–0,55 trên các bộ khác; TSP gần như không dùng V_me. Như vậy PPO tối ưu theo năng lượng mỗi khe, không theo năng lượng mỗi mét. Cách này kéo dài thời gian bay nhưng mỗi joule đi được ít hơn 28% quãng đường. Trên `ood_area` (L lớn hơn), fast_frac của DR còn **giảm** xuống 0,04, ngược với điều mà tầm bay xa đòi hỏi.
3. **Tiền đề của G3 cần xem lại.** Thiết kế viết "TSP bay nhanh khi còn xa mục tiêu … TSP vì vậy không tiết kiệm năng lượng" (`notes/2026-11-06_dat_thiet-ke_PG-TG-PPO.md` §1). Theo chính mô hình năng lượng của repo, V_mr là tốc độ tiết kiệm nhất để **di chuyển**, nên TSP đã chọn đúng tốc độ khi bay xa. Chỗ để thắng TSP khi pin thấp (G3) có thể nằm ở **thứ tự**, bỏ điểm hay thời gian treo, không nằm ở tốc độ bay.
4. **Giả thuyết cơ chế (từ mã, chưa kiểm).** Phần thưởng phạt năng lượng **theo khe**: λ·e/(P_hover·δt), λ = 0,1 (`env.py` dòng 169). Mỗi khe V_me tốn 2 807 J, V_mr tốn 3 599 J, nên số hạng này luôn nghiêng về V_me. Nó không tính quãng đường đi được, nên có thể đẩy policy về V_me. Kiểm được rẻ khi đọc lại EXP-05 (quét λ, đã hoãn) hoặc bằng nhánh λ = 0 trong pilot. Đây là giả thuyết, chưa phải kết luận.
5. **Quan sát legacy (G1) không bị bác bỏ, nhưng cũng không được củng cố.** Dữ kiện trên không cho biết policy có "thấy" ngân sách hay không. Hành vi trên `ood_energy` gần như giống `id` (fast_frac, slow_frac), và điều đó khớp với G1. Tuy vậy, hành vi đó cũng khớp với một policy đã thấy ngân sách mà vẫn chọn V_me do phần thưởng.

## 4. Đề xuất cho DAT (DAT quyết định)

- **Thành phần B** (tour-guided, đánh vào G2) được dữ kiện ủng hộ gián tiếp: PPO thua chủ yếu vì phủ kém, không phải vì hết pin sớm. B giữ nguyên.
- **Thành phần A** (quan sát neo): theo card, "xem lại G1 trước khi viết mã A". LDN đề xuất **không bỏ A**, mà sửa hai chỗ trước khi khoá phụ lục B:
  1. Ghi lại G3 cho khớp với mô hình năng lượng (V_mr đã tiết kiệm nhất khi di chuyển). Không viết "TSP không tiết kiệm năng lượng" trong bài.
  2. Cân nhắc đưa vào pilot EXP-08p một phép kiểm rẻ cho giả thuyết phần thưởng (mục 3.4). Ví dụ: chỉ số "năng lượng mỗi mét" của M1 và M4; hoặc một nhánh phụ λ = 0, chỉ thăm dò. Nếu thêm nhánh thì phải sửa card trước khi chạy.
- TSP-adaptive (baseline mạnh hơn) nên giữ V_mr khi di chuyển xa. Nếu TSP-adaptive giảm tốc về V_me khi pin thấp, nó có thể **yếu** hơn TSP thường. Như vậy mốc S (Random → TSP-adaptive) sẽ dễ hơn thực tế. Nên kiểm Ā(TSP-adaptive) ≤ Ā(TSP) trên `ood_energy` bằng `--probe-b` trước khi khoá.

## 5. Giới hạn

- Thăm dò trên dữ liệu đã thấy; không p-value (quy tắc 5). Các khoảng [min–max] chỉ mô tả độ phân tán giữa seed.
- 10 seed DR dùng chung 7/8 chuỗi kịch bản huấn luyện (DECISIONS 06/11), nên phân tán giữa seed DR có thể bị đánh giá thấp.
- t_end là đại lượng suy ra; cách suy dựa trên mô hình năng lượng ở `env.py` tại `main`. Sau khoá, `src/` có thêm mã (PR #45: quan sát neo, wrapper tour), nhưng `git diff prereg-lock main` không chạm các dòng năng lượng hay `action_counts`. Với EXP-08 nên thêm cột `t_end` trực tiếp vào `events.csv`.
