# EXP-07 — Ablation A4 (bỏ action mask) và A5 (một mức tốc độ V_me)

**Owner:** FAO (Nguyễn Minh Chính) · **Second reader:** LDN
**Viết:** 22/10/2026, trước khi chạy, viết sớm so với lịch (W6-FAO-02, hạn 29/11) · **Chạy:** W7, 30/11–06/12 (W7-FAO-01) · **Gate:** G2 (20/12)
**Phụ thuộc:**
- PR #23 (`fao/a5-single-speed`) phải merge **trước khi khoá PREREG tại G1**, vì sau mốc khoá `src/` không được sửa.
- Cần EXP-03 seed 0–4 của DR-PPO (W5-DAT-01) để làm nhóm đối chứng.
- Siêu tham số lấy từ PREREG (W4-DAT-01).

## D. Experiment card

```text
Experiment ID: EXP-07
Owner / second reader: FAO / LDN
Thăm dò hay khẳng định: THĂM DÒ. docs/03 §7 xếp A4, A5 vào "độ nhạy thiết kế" và "vai trò
  của lựa chọn tốc độ", không có giả thuyết kiểm định. Chỉ báo mô tả: trung bình, 95% CI
  bootstrap, IQM, Cliff's δ. Không tuyên bố ý nghĩa thống kê; nếu bảng có p-value thì
  ghi rõ là thăm dò, không hiệu chỉnh, không dùng để kết luận.

Câu hỏi nghiên cứu:
  A4: Action mask (MaskablePPO) đóng góp gì so với PPO thường dùng cơ chế kẹp biên kèm phạt μ,
      xét về Ā, độ suy giảm OOD và số lần chạm biên?
  A5: Việc cho chính sách chọn giữa hai tốc độ (V_me, V_mr) có giúp gì so với chỉ có V_me,
      xét về Ā, năng lượng và độ suy giảm OOD? (gắn với RQ2, phần "chính sách sử dụng hai mức
      tốc độ ra sao", docs/01 §4)
Giả thuyết (định hướng, không kiểm định):
  A4: PPO không mask có boundary_hits > 0 và Ā trên id không thấp hơn DR-PPO có mask.
  A5: DR-PPO hai tốc độ có Ā thấp hơn DR-PPO một tốc độ trên ít nhất bộ id; khác biệt rõ nhất
      ở ood_area (vùng rộng, quãng bay dài hơn).

Biến thay đổi và các giá trị:
  A4: thuật toán/mask: PPO thường (train_ppo.py KHÔNG có --masked), 17 hành động; khi hành động
      đưa UAV ra ngoài vùng, môi trường kẹp vị trí tại biên và phạt μ = 0,1 (env.py, step()).
  A5: MaskablePPO với configs/a5_single_speed.json (single_speed = true): hành động 9–16 (V_mr)
      luôn bị che trong action_masks(); step() báo lỗi nếu chính sách vẫn chọn V_mr (PR #23).
Điều kiện cố định: TRAIN_DR, SmallCNN (features_dim 256), quan sát 5×31×31, λ = 0,1, μ = 0,1,
  configs/env_default.json (A5 chỉ thêm single_speed), siêu tham số PPO khoá trong PREREG,
  cùng số bước như EXP-03, cùng commit (prereg-lock hoặc con của nó, không sửa src/).
Đối chứng (baseline): DR-PPO có mask, seed 0–4 của EXP-03 (nhãn dr_ppo). Không huấn luyện lại.
  Tham khảo: TSP, Random từ EXP-01.
Kiểm soát loại trừ giải thích khác:
  - Cùng seed huấn luyện {0..4} với nhóm đối chứng, nên so sánh được ghép cặp theo seed.
  - Cùng 100 kịch bản đánh giá cố định (seed 100000–100099) trên 5 bộ.
  - A4 dùng nguyên siêu tham số đã tinh chỉnh cho MaskablePPO, không tinh chỉnh lại (xem
    "chênh lệch không tránh được" bên dưới).
  - A5 giữ nguyên thang thưởng: worst_step_cost và rho_max vẫn tính trên cả hai tốc độ, nên
    chỉ tập hành động thay đổi.
Ngân sách tương đương và chênh lệch không tránh được:
  - Bước huấn luyện: bằng EXP-03 (giá trị trong PREREG).
  - Lượt Optuna: 0 cho cả A4 và A5. Siêu tham số được tinh chỉnh cho MaskablePPO hai tốc độ,
    nên có thể bất lợi cho A4/A5. Đây là giới hạn phải ghi trong bài; kết quả "A4/A5 kém hơn"
    vì vậy là cận trên của tác hại, không phải ước lượng không chệch.
  - A4: PPO không mask có thể chọn hành động không đủ năng lượng; khi đó episode dừng sớm và
    bị phạt (env.py, _terminate_early). Chênh lệch này là một phần tác dụng của mask, không
    phải lỗi thực nghiệm; báo cáo riêng tỷ lệ early_termination.
  - A5: bỏ V_mr làm không gian hành động hiệu dụng nhỏ hơn (9 thay vì 17), có thể làm việc
    học dễ hơn. Không tách được hiệu ứng này khỏi "vai trò của tốc độ"; ghi rõ khi diễn giải.
Quy tắc chọn kịch bản/bộ đánh giá: cả 5 bộ (id, ood_cluster, ood_density, ood_area,
  ood_energy), 100 episode mỗi bộ, không chọn lọc theo kết quả.
Công thức chỉ số, đơn vị, mẫu số:
  - Ā (khe), tính trên toàn T kể cả khi dừng sớm (docs/03 §5).
  - deg_i(s) = (Ā_i(s) − Ā_i(id)) / Ā_i(id), theo từng seed i.
  - Phụ: energy_used_J, energy_frac, boundary_hits (số lần/episode), early_termination (tỷ lệ
    episode), hover_frac / slow_frac / fast_frac, coverage.
  - Hiệu ghép cặp theo seed: Ā(biến thể, seed i) − Ā(dr_ppo, seed i), mỗi bộ.
Đơn vị lặp độc lập: seed huấn luyện (n = 5 mỗi biến thể; trung bình trên 100 episode đánh giá).
Danh sách seed / ghép cặp / thứ tự chạy: seed 0–4. Thứ tự xen kẽ: s0-A4, s0-A5, s1-A4, s1-A5, …
  Ghép cặp với dr_ppo seed cùng số của EXP-03.
Kế hoạch phân tích và báo cáo độ bất định: scripts/analyze.py (bảng Mean [95% CI] và IQM theo
  phương pháp × bộ) cho mean_aoi, energy_used_J, boundary_hits, fast_frac. Thêm bảng hiệu ghép
  cặp và Cliff's δ cho từng bộ (LDN). Bảng T3 trong bài (docs/06 §1): A4, A5 cạnh dr_ppo.
Xử lý thất bại / quá thời gian: giữ run_record failed. Nếu phân kỳ (NaN), ghi rõ và chạy lại
  một lần với seed mới (theo quy tắc EXP-02); seed thay thế phá ghép cặp nên báo riêng.
  Nếu hết thời gian W7: ưu tiên A5 (gắn RQ2) trước A4; báo DAT ngay, không âm thầm dời hạn.
Thời gian pilot và ước lượng tổng chi phí: 10 lần huấn luyện × số bước PREREG (2M thì 20M bước,
  notes/2026-10-21_fao_chi-phi-nhap.md). Thời gian = 20M / steps_per_s; steps_per_s chỉ lấy từ
  máy cố định (W1-DAT-05). Đánh giá: 10 model × 5 bộ × 100 episode.

Kết quả kỳ vọng nếu giả thuyết đúng:
  A4: boundary_hits > 0 ở PPO không mask (DR-PPO có mask phải bằng 0, tiêu chí G1 số 5);
      Ā(id) bằng hoặc cao hơn dr_ppo.
  A5: Ā(dr_ppo) < Ā(1 tốc độ) ở id, rõ hơn ở ood_area; fast_frac của dr_ppo > 0.
Kết quả sẽ bác bỏ hoặc làm yếu giả thuyết:
  A4: PPO không mask đạt Ā tương đương và boundary_hits gần 0. Khi đó mask chỉ là tiện ích,
      không phải thành phần cần; viết đúng như vậy.
  A5: Ā tương đương, hoặc A5 tốt hơn. Kiểm tra trước: nếu fast_frac của dr_ppo ở EXP-03 ≈ 0
      (chính sách gần như không dùng V_mr) thì A5 gần như trùng dr_ppo; ghi nhận rằng lựa chọn
      tốc độ không được khai thác, và điều này ảnh hưởng tới câu chữ của RQ2.
  Lưu ý: TSP không dùng V_me trên các quỹ đạo đã vẽ (notes/2026-10-21_fao_can-DAT.md, A7),
      nên không suy ra vai trò tốc độ từ heuristic.
Tiêu chí tiếp tục/dừng khai báo trước:
  - Trước khi chạy A5 seed 1–4: kiểm A5 seed 0 có slow_frac + hover_frac = 1 và fast_frac = 0
    trên mọi episode (xác nhận cờ có hiệu lực). Sai thì dừng, debug.
  - Trước khi chạy A4 seed 1–4: kiểm config.json của run A4 có args.masked = false và
    run_id không có "_mask". Sai thì dừng.
  - Mỗi model: FAO vẽ ≥ 3 quỹ đạo (plot_trajectory.py), ghi suy biến vào notes/review_log.md.
Trường raw cần cho hình dự kiến: events.csv (mean_aoi, energy_used_J, boundary_hits,
  early_termination, hover_frac, slow_frac, fast_frac, coverage), run_record.json
  (checkpoint_digest, steps_per_s, model_path), config.json (args.masked, env_cfg.single_speed).
```

## Lệnh (chạy sau khi PREREG khoá; `<PREREG>` = số bước đã khoá)

PowerShell, mỗi seed một vòng:

```powershell
foreach ($s in 0..4) {
  # A4: PPO thường, không --masked
  python scripts/train_ppo.py --experiment-id EXP-07 --train dr --seed $s --timesteps <PREREG>
  # A5: MaskablePPO, một tốc độ
  python scripts/train_ppo.py --experiment-id EXP-07 --train dr --seed $s --timesteps <PREREG> --masked --config configs/a5_single_speed.json
}
```

Đánh giá, với mỗi `model.zip` in ra ở cuối lần huấn luyện. A5 **bắt buộc** truyền cùng `--config`; nếu quên, `step()` báo lỗi thay vì cho số sai:

```powershell
python scripts/evaluate.py --experiment-id EXP-07 --model runs/EXP-07/<run-id-A4-s0>/model.zip --label dr_ppo_nomask --train-seed 0
python scripts/evaluate.py --experiment-id EXP-07 --model runs/EXP-07/<run-id-A5-s0>/model.zip --label dr_ppo_1spd --train-seed 0 --config configs/a5_single_speed.json
```

Run_id dự kiến:
- A4: `dr_ppo_lam0.1_s<s>_<thời điểm>` (không có `_mask`).
- A5: `dr_ppo_mask_1spd_lam0.1_s<s>_<thời điểm>`.

Ghi manifest (W8-FAO-02):

```powershell
python scripts/manifest_row.py "results/raw/EXP-07/dr_ppo_*" --verify --append
```

Phân tích (đặt `--fixed none --heuristic none` để bỏ phần H1, H2, vì EXP-07 không kiểm định). PowerShell không tự mở rộng `*` cho Python, nên lấy danh sách file bằng `Get-ChildItem`:

```powershell
$csv = @((Get-ChildItem results/raw/EXP-03/*/events.csv).FullName) + @((Get-ChildItem results/raw/EXP-07/*/events.csv).FullName)
python scripts/analyze.py $csv --proposed dr_ppo --fixed none --heuristic none --out results/processed/EXP-07_summary.md
python scripts/analyze.py $csv --metric boundary_hits --proposed dr_ppo --fixed none --heuristic none --out results/processed/EXP-07_boundary.md
python scripts/analyze.py $csv --metric fast_frac --proposed dr_ppo --fixed none --heuristic none --out results/processed/EXP-07_fast_frac.md
```

## Câu hỏi mở (trước G1)
1. A4 và A5 có dùng nguyên siêu tham số của DR-PPO không, hay cần lượt Optuna riêng? Card này mặc định là **dùng nguyên, không tinh chỉnh**, ghi là giới hạn. Nếu DAT muốn tinh chỉnh riêng thì phải cộng ngân sách vào PREREG.
2. Trường `use_action_mask_clip` trong `EnvConfig` không được dùng ở đâu trong mã. A4 không phụ thuộc trường này, nhưng nên xoá hoặc ghi chú trước khi khoá PREREG để người đọc config không hiểu nhầm.

## Kết quả (FAO điền sau khi chạy)

```text
Commit: ___  Máy: ___
A4 seed 0–4 run_id: ___
A5 seed 0–4 run_id: ___
Kiểm cờ A5 (fast_frac = 0 mọi episode): ___
Kiểm A4 (args.masked = false): ___
Second reader (LDN): ___  ngày: ___
```
