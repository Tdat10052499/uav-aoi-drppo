# EXP-03: kết quả chính thức H1/H2 (W4-LDN-04, phần số liệu)

> LDN, 06/11/2026 (Claude hỗ trợ). Second reader: DAT. Số sinh từ raw, tại commit `e9d5110` (`main`, sau khi PR #43 merge):
>
> ```bash
> python scripts/analyze.py results/raw/EXP-03/*/events.csv \
>     --out results/processed/EXP-03_summary.md --fig figures/F4_deg.pdf
> ```
>
> `results/processed/EXP-03_summary.md` (SHA256 `fb14d4b2a4274832…`) trùng từng dòng với bản chạy thử trên nhánh PR #43, trừ dòng đường dẫn hình.

## 1. Quyết định theo PREREG §8

| Bộ | Δ_s = deg_Fixed − deg_DR [95% CI] | p_Holm | Đạt (p_Holm < 0,05 và Δ_s ≥ 0,10) |
| --- | --- | --- | --- |
| ood_cluster | −0,081 [−0,134; −0,031] | 1,0000 | không |
| ood_density | −0,582 [−0,665; −0,489] | 1,0000 | không |
| ood_area | −1,088 [−1,192; −0,982] | 1,0000 | không |
| ood_energy | −1,484 [−1,631; −1,324] | 1,0000 | không |

- **H1: 0/4 bộ đạt, nên KHÔNG được ủng hộ** (cần ≥ 3/4). Δ_s âm ở cả 4 bộ, tức DR suy giảm tương đối **nhiều hơn** Fixed.
- **H2: KHÔNG được ủng hộ.** Trên `ood_cluster`: Ā(DR) = 41,58 [40,25; 42,87] (10 seed), Ā(TSP) = 22,94 [21,72; 24,18] (100 episode). Hoán vị một phía p = 1,0000, Cliff's δ = 1,00.
- Kết luận khớp với số sơ bộ của DAT (`notes/2026-11-06_dat_EXP-03-so-bo.md`).

## 2. Kiểm tra đi kèm

- **Heuristic tại commit khoá** (PREREG §5): `scripts/compare_events.py` so `results/raw/EXP-03/heuristics_lock/events.csv` với `results/raw/EXP-01/20261020-084218` và `20261025-115153`. Kết quả **MATCH**: 1 500/1 500 dòng, 0 lệch (atol 1e-9). Cột TSP của H2 vì vậy dùng được.
- **Run đưa vào phân tích:** 10 seed DR, 10 seed Fixed, cùng heuristic Random, Greedy-AoI và TSP; mọi `run_record` đều `completed`. Không CSV nào bị loại.
- **Run hỏng** (liệt kê trong bài theo PREREG §9 mục 5):

  | Run ID | Trạng thái | Lý do | Xử lý |
  | --- | --- | --- | --- |
  | `dr_ppo_mask_lam0.1_s3_20261104-202500` | `running`, không có model hay `events.csv` | Người chạy đóng cửa sổ terminal khoảng 20:26 ngày 04/11, ở bước 16 384; không do NaN hay kết quả (DECISIONS 05/11 và 06/11, PR #41) | Chạy lại cùng seed 3: `..._s3_20261105-140316` (`completed`, checkpoint `sha256:bfe09…`) |

  Hai lần ngắt Fixed seed 2 (04/11) xảy ra trước khi run kịp tạo thư mục, nên không để lại dữ liệu.

## 3. Giới hạn cần ghi trong bài

1. **Seed DR không độc lập hoàn toàn.** Env reset bằng seed + rank, nên hai seed liền nhau dùng chung 7/8 chuỗi kịch bản (DECISIONS 06/11). Phương sai giữa các seed DR có thể bị đánh giá thấp: CI của nhánh DR hẹp hơn thực tế, và p-value của các phép so sánh có DR có thể quá lạc quan. Kết luận H1 và H2 không đổi, vì sai lệch kiểu này chỉ làm kết quả trông có ý nghĩa hơn, mà ở đây p = 1. Các so sánh Ā thăm dò giữa DR và Fixed có p rất nhỏ thì phải kèm cảnh báo này.
2. **H2 so hai đơn vị khác nhau.** Một bên là 10 trung bình theo seed (DR), bên kia là 100 episode TSP tất định (PREREG §7).
3. **Siêu tham số mặc định**, không tinh chỉnh Optuna (DECISIONS 03/11), như nhau cho cả hai nhánh.

## 4. Hình

`figures/F4_deg.pdf`: deg theo seed của DR và Fixed trên 4 bộ OOD. Văn bản thay thế ở `figures/F4_deg.pdf.alt.txt`.
