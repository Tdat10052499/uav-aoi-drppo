# EXP-08a: chẩn đoán từ raw EXP-03 (thăm dò, chỉ mô tả)

Sinh bởi `scripts/diag_exp08a.py` tại commit `a684265`. 11500 episode; t_end không suy ra được (0 hoặc nhiều nghiệm): 0.
Năng lượng mỗi khe (env.py): truyền 4264.0 J, treo không truyền 4114.0 J, V_me 2806.9 J, V_mr 3598.6 J; T = 300.
DR, Fixed: trung bình của 10 trung bình theo seed, [min–max] các trung bình seed. Heuristic: trung bình 100 episode.

| Bộ | Nhánh | n | early_termination | t_end (khe) | hover | slow (V_me) | fast (V_mr) | coverage | collections | Ā |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| id | DR | 10 | 0.65 [0.50–0.94] | 292 [284–295] | 0.30 | 0.55 | 0.15 [0.09–0.18] | 0.96 [0.92–0.98] | 81.2 | 52.1 |
| id | Fixed | 10 | 0.74 [0.57–0.89] | 278 [259–293] | 0.41 | 0.43 | 0.16 [0.06–0.33] | 0.61 [0.49–0.79] | 82.7 | 107.2 |
| id | TSP | 100 | 0.95 | 255 | 0.42 | 0.00 | 0.58 | 1.00 | 107.0 | 28.6 |
| id | Greedy | 100 | 0.95 | 254 | 0.43 | 0.00 | 0.57 | 1.00 | 109.4 | 29.0 |
| id | Random | 100 | 0.47 | 287 | 0.07 | 0.48 | 0.45 | 0.42 | 13.7 | 126.2 |
| ood_cluster | DR | 10 | 0.63 [0.47–0.92] | 290 [285–292] | 0.37 | 0.55 | 0.08 [0.06–0.11] | 0.98 [0.95–1.00] | 100.7 | 41.6 |
| ood_cluster | Fixed | 10 | 0.72 [0.56–0.79] | 281 [272–292] | 0.43 | 0.46 | 0.11 [0.06–0.21] | 0.81 [0.67–0.92] | 91.3 | 77.2 |
| ood_cluster | TSP | 100 | 0.99 | 249 | 0.61 | 0.00 | 0.39 | 1.00 | 151.2 | 22.9 |
| ood_cluster | Greedy | 100 | 1.00 | 248 | 0.64 | 0.00 | 0.36 | 1.00 | 158.7 | 23.8 |
| ood_cluster | Random | 100 | 0.44 | 288 | 0.06 | 0.48 | 0.45 | 0.30 | 7.6 | 134.7 |
| ood_density | DR | 10 | 0.65 [0.48–0.85] | 288 [278–295] | 0.33 | 0.51 | 0.15 [0.06–0.26] | 0.73 [0.66–0.81] | 93.5 | 92.9 |
| ood_density | Fixed | 10 | 0.73 [0.47–0.99] | 273 [249–291] | 0.43 | 0.37 | 0.20 [0.02–0.50] | 0.38 [0.28–0.54] | 104.8 | 128.6 |
| ood_density | TSP | 100 | 0.98 | 251 | 0.55 | 0.00 | 0.45 | 1.00 | 138.3 | 43.6 |
| ood_density | Greedy | 100 | 0.99 | 250 | 0.58 | 0.00 | 0.42 | 1.00 | 144.1 | 43.6 |
| ood_density | Random | 100 | 0.48 | 288 | 0.06 | 0.48 | 0.46 | 0.31 | 17.1 | 134.2 |
| ood_area | DR | 10 | 0.96 [0.91–1.00] | 276 [262–285] | 0.53 | 0.43 | 0.04 [0.01–0.06] | 0.46 [0.29–0.57] | 78.4 | 123.3 |
| ood_area | Fixed | 10 | 0.90 [0.82–0.97] | 270 [254–291] | 0.56 | 0.34 | 0.10 [0.00–0.27] | 0.24 [0.17–0.32] | 66.9 | 136.9 |
| ood_area | TSP | 100 | 0.92 | 259 | 0.31 | 0.00 | 0.69 | 1.00 | 80.2 | 35.6 |
| ood_area | Greedy | 100 | 0.92 | 259 | 0.31 | 0.00 | 0.69 | 1.00 | 81.2 | 36.9 |
| ood_area | Random | 100 | 0.46 | 287 | 0.06 | 0.48 | 0.46 | 0.23 | 7.8 | 137.9 |
| ood_energy | DR | 10 | 1.00 [1.00–1.00] | 186 [149–209] | 0.23 | 0.64 | 0.14 [0.03–0.36] | 0.07 [0.01–0.21] | 20.6 | 147.6 |
| ood_energy | Fixed | 10 | 1.00 [1.00–1.00] | 185 [169–211] | 0.24 | 0.63 | 0.13 [0.00–0.58] | 0.13 [0.01–0.26] | 25.5 | 145.1 |
| ood_energy | TSP | 100 | 1.00 | 153 | 0.42 | 0.00 | 0.58 | 1.00 | 64.3 | 60.5 |
| ood_energy | Greedy | 100 | 1.00 | 153 | 0.44 | 0.00 | 0.56 | 1.00 | 67.1 | 61.0 |
| ood_energy | Random | 100 | 1.00 | 182 | 0.07 | 0.48 | 0.45 | 0.30 | 8.5 | 133.9 |

## t_end chỉ trên các episode kết thúc sớm (gộp mọi seed)

| Bộ | DR | Fixed | TSP | Greedy | Random |
| --- | --- | --- | --- | --- | --- |
| id | 287 (n = 646) | 270 (n = 736) | 252 (n = 95) | 252 (n = 95) | 273 (n = 47) |
| ood_cluster | 285 (n = 632) | 274 (n = 720) | 249 (n = 99) | 248 (n = 100) | 272 (n = 44) |
| ood_density | 282 (n = 645) | 264 (n = 727) | 250 (n = 98) | 250 (n = 99) | 275 (n = 48) |
| ood_area | 275 (n = 957) | 267 (n = 900) | 256 (n = 92) | 255 (n = 92) | 272 (n = 46) |
| ood_energy | 186 (n = 1000) | 185 (n = 1000) | 153 (n = 100) | 153 (n = 100) | 182 (n = 100) |

## Tệp đầu vào (SHA256)

- `results/raw/EXP-03/eval_dr_ppo_s0/events.csv` `778a62d762d73c8d`
- `results/raw/EXP-03/eval_dr_ppo_s1/events.csv` `9c8480e3d3c05c41`
- `results/raw/EXP-03/eval_dr_ppo_s2/events.csv` `01bc63653e47c7df`
- `results/raw/EXP-03/eval_dr_ppo_s3/events.csv` `7acb12bdd3be2370`
- `results/raw/EXP-03/eval_dr_ppo_s4/events.csv` `2a4567b44620f099`
- `results/raw/EXP-03/eval_dr_ppo_s5/events.csv` `e9ebb38626d6d84c`
- `results/raw/EXP-03/eval_dr_ppo_s6/events.csv` `593235dc7bc2deff`
- `results/raw/EXP-03/eval_dr_ppo_s7/events.csv` `fc26063300a717a6`
- `results/raw/EXP-03/eval_dr_ppo_s8/events.csv` `7eb701a8aaeb6cc0`
- `results/raw/EXP-03/eval_dr_ppo_s9/events.csv` `9cd869ffc7925ac7`
- `results/raw/EXP-03/eval_fixed_ppo_s0/events.csv` `c1cacd51409d7110`
- `results/raw/EXP-03/eval_fixed_ppo_s1/events.csv` `298ea219267a7298`
- `results/raw/EXP-03/eval_fixed_ppo_s2/events.csv` `989251cfe8f44bd7`
- `results/raw/EXP-03/eval_fixed_ppo_s3/events.csv` `4b66a071cc9dd69f`
- `results/raw/EXP-03/eval_fixed_ppo_s4/events.csv` `64059eb4c0e5ce12`
- `results/raw/EXP-03/eval_fixed_ppo_s5/events.csv` `4301d3c69d150561`
- `results/raw/EXP-03/eval_fixed_ppo_s6/events.csv` `b2de7c7806a23cd4`
- `results/raw/EXP-03/eval_fixed_ppo_s7/events.csv` `c16c9e8b9d2bed0c`
- `results/raw/EXP-03/eval_fixed_ppo_s8/events.csv` `2ba78d9e3456290c`
- `results/raw/EXP-03/eval_fixed_ppo_s9/events.csv` `769e4d697ef35ae3`
- `results/raw/EXP-03/heuristics_lock/events.csv` `58412a7c1b846a98`
