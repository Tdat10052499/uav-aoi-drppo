# Summary (mean_aoi, lower is better)

| Method | Suite | n | Mean [95% CI] | IQM |
| --- | --- | --- | --- | --- |
| dr_ppo | id | 10 | 52.15 [50.04, 54.35] | 51.97 |
| dr_ppo | ood_area | 10 | 123.29 [119.88, 126.92] | 123.07 |
| dr_ppo | ood_cluster | 10 | 41.58 [40.25, 42.87] | 41.62 |
| dr_ppo | ood_density | 10 | 92.86 [88.91, 96.46] | 93.85 |
| dr_ppo | ood_energy | 10 | 147.63 [145.58, 149.42] | 148.27 |
| fixed_ppo | id | 10 | 107.24 [102.00, 112.13] | 108.23 |
| fixed_ppo | ood_area | 10 | 136.93 [135.32, 138.47] | 137.00 |
| fixed_ppo | ood_cluster | 10 | 77.20 [71.86, 82.50] | 76.89 |
| fixed_ppo | ood_density | 10 | 128.63 [124.54, 132.54] | 129.06 |
| fixed_ppo | ood_energy | 10 | 145.10 [142.32, 147.63] | 145.56 |
| greedy_aoi | id | 100 | 29.04 [27.83, 30.24] | 28.76 |
| greedy_aoi | ood_area | 100 | 36.88 [35.40, 38.40] | 36.25 |
| greedy_aoi | ood_cluster | 100 | 23.81 [22.45, 25.21] | 23.26 |
| greedy_aoi | ood_density | 100 | 43.59 [42.65, 44.57] | 43.33 |
| greedy_aoi | ood_energy | 100 | 61.03 [59.38, 62.68] | 60.87 |
| random | id | 100 | 126.24 [124.72, 127.77] | 126.98 |
| random | ood_area | 100 | 137.90 [136.52, 139.22] | 138.36 |
| random | ood_cluster | 100 | 134.71 [132.61, 136.74] | 135.60 |
| random | ood_density | 100 | 134.15 [133.23, 135.07] | 134.25 |
| random | ood_energy | 100 | 133.87 [132.49, 135.21] | 134.34 |
| tsp | id | 100 | 28.64 [27.45, 29.84] | 28.43 |
| tsp | ood_area | 100 | 35.61 [34.33, 36.88] | 35.52 |
| tsp | ood_cluster | 100 | 22.94 [21.72, 24.18] | 22.61 |
| tsp | ood_density | 100 | 43.58 [42.66, 44.55] | 43.35 |
| tsp | ood_energy | 100 | 60.53 [58.89, 62.15] | 60.45 |

## H1 — OOD degradation (DR vs fixed), one-sided permutation test, Holm

| Suite | deg DR (mean) | deg fixed (mean) | p | p_Holm | Cliff's δ |
| --- | --- | --- | --- | --- | --- |
| ood_cluster | -0.200 | -0.281 | 0.9963 | 1.0000 | 0.70 |
| ood_density | 0.786 | 0.203 | 1.0000 | 1.0000 | 1.00 |
| ood_area | 1.371 | 0.283 | 1.0000 | 1.0000 | 1.00 |
| ood_energy | 1.845 | 0.362 | 1.0000 | 1.0000 | 1.00 |

## H2 — DR-PPO vs heuristic on ood_cluster

permutation p (one-sided, DR < tsp) = 1.0000; Cliff's δ = 1.00. Note: compare at equal energy budget (same suite).

## Runs

Evaluated (method, train_seed): dr_ppo/0, dr_ppo/1, dr_ppo/2, dr_ppo/3, dr_ppo/4, dr_ppo/5, dr_ppo/6, dr_ppo/7, dr_ppo/8, dr_ppo/9, fixed_ppo/0, fixed_ppo/1, fixed_ppo/2, fixed_ppo/3, fixed_ppo/4, fixed_ppo/5, fixed_ppo/6, fixed_ppo/7, fixed_ppo/8, fixed_ppo/9, greedy_aoi/-1, random/-1, tsp/-1.
No CSV excluded.

## H1 — decision per PREREG sec. 8 (delta = 0.10)

p and p_Holm are copied from the H1 table above (locked code). Delta_s = mean deg_Fixed - mean deg_DR; 95% CI by two-sample bootstrap (10000 resamples, seed 0). A suite passes when p_Holm < 0.05 and Delta_s >= 0.10.

| Suite | n DR / n Fixed | deg DR mean [95% CI] | IQM | deg Fixed mean [95% CI] | IQM | Delta_s [95% CI] | p_Holm | Pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ood_cluster | 10 / 10 | -0.200 [-0.236; -0.158] | -0.213 | -0.281 [-0.313; -0.248] | -0.285 | -0.081 [-0.134; -0.031] | 1.0000 | no |
| ood_density | 10 / 10 | +0.786 [+0.700; +0.859] | +0.817 | +0.203 [+0.167; +0.243] | +0.195 | -0.582 [-0.665; -0.489] | 1.0000 | no |
| ood_area | 10 / 10 | +1.371 [+1.282; +1.463] | +1.373 | +0.283 [+0.235; +0.338] | +0.266 | -1.088 [-1.192; -0.982] | 1.0000 | no |
| ood_energy | 10 / 10 | +1.845 [+1.706; +1.974] | +1.858 | +0.362 [+0.291; +0.438] | +0.351 | -1.484 [-1.631; -1.324] | 1.0000 | no |

**H1: 0/4 suites pass -> NOT supported** (rule: >= 3/4 suites).

## Per-seed A_id and deg (issue #14)

| Method | Seed | A_id | deg cluster | deg density | deg area | deg energy |
| --- | --- | --- | --- | --- | --- | --- |
| dr_ppo | 0 | 49.80 | -0.177 | +0.872 | +1.551 | +1.939 |
| dr_ppo | 1 | 54.57 | -0.266 | +0.888 | +1.130 | +1.739 |
| dr_ppo | 2 | 51.80 | -0.247 | +0.791 | +1.358 | +1.915 |
| dr_ppo | 3 | 52.74 | -0.181 | +0.820 | +1.213 | +1.869 |
| dr_ppo | 4 | 59.09 | -0.249 | +0.597 | +1.293 | +1.391 |
| dr_ppo | 5 | 53.31 | -0.276 | +0.517 | +1.336 | +1.684 |
| dr_ppo | 6 | 47.60 | -0.102 | +0.908 | +1.582 | +2.149 |
| dr_ppo | 7 | 55.44 | -0.214 | +0.751 | +1.265 | +1.665 |
| dr_ppo | 8 | 47.51 | -0.073 | +0.778 | +1.436 | +2.100 |
| dr_ppo | 9 | 49.62 | -0.210 | +0.932 | +1.551 | +2.000 |
| fixed_ppo | 0 | 101.01 | -0.285 | +0.188 | +0.342 | +0.455 |
| fixed_ppo | 1 | 108.79 | -0.300 | +0.261 | +0.257 | +0.334 |
| fixed_ppo | 2 | 91.75 | -0.202 | +0.314 | +0.450 | +0.611 |
| fixed_ppo | 3 | 96.86 | -0.362 | +0.231 | +0.399 | +0.450 |
| fixed_ppo | 4 | 105.43 | -0.318 | +0.285 | +0.262 | +0.432 |
| fixed_ppo | 5 | 107.39 | -0.343 | +0.182 | +0.277 | +0.283 |
| fixed_ppo | 6 | 115.70 | -0.266 | +0.152 | +0.215 | +0.272 |
| fixed_ppo | 7 | 118.78 | -0.273 | +0.131 | +0.167 | +0.171 |
| fixed_ppo | 8 | 113.45 | -0.189 | +0.157 | +0.221 | +0.321 |
| fixed_ppo | 9 | 113.30 | -0.268 | +0.131 | +0.241 | +0.288 |

## Secondary metrics (descriptive only, PREREG sec. 7; mean over all episodes and seeds)

| Method | Suite | n episodes | peak_aoi | energy_frac | early_termination | coverage | collections | hover_frac | slow_frac | fast_frac | boundary_hits |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| dr_ppo | id | 1000 | 182.573 | 0.993 | 0.646 | 0.955 | 81.158 | 0.303 | 0.547 | 0.151 | 0.000 |
| dr_ppo | ood_area | 1000 | 299.051 | 0.998 | 0.957 | 0.457 | 78.438 | 0.531 | 0.429 | 0.040 | 0.000 |
| dr_ppo | ood_cluster | 1000 | 162.370 | 0.993 | 0.632 | 0.980 | 100.695 | 0.368 | 0.549 | 0.083 | 0.000 |
| dr_ppo | ood_density | 1000 | 277.240 | 0.987 | 0.645 | 0.729 | 93.517 | 0.332 | 0.515 | 0.154 | 0.000 |
| dr_ppo | ood_energy | 1000 | 300.000 | 0.998 | 1.000 | 0.070 | 20.624 | 0.226 | 0.637 | 0.137 | 0.000 |
| fixed_ppo | id | 1000 | 287.344 | 0.987 | 0.736 | 0.612 | 82.694 | 0.410 | 0.427 | 0.163 | 0.000 |
| fixed_ppo | ood_area | 1000 | 299.808 | 0.995 | 0.900 | 0.242 | 66.919 | 0.555 | 0.345 | 0.100 | 0.000 |
| fixed_ppo | ood_cluster | 1000 | 245.204 | 0.987 | 0.720 | 0.809 | 91.287 | 0.429 | 0.458 | 0.114 | 0.000 |
| fixed_ppo | ood_density | 1000 | 300.000 | 0.981 | 0.727 | 0.384 | 104.798 | 0.427 | 0.369 | 0.204 | 0.000 |
| fixed_ppo | ood_energy | 1000 | 300.000 | 0.998 | 1.000 | 0.126 | 25.515 | 0.240 | 0.626 | 0.134 | 0.000 |
| greedy_aoi | id | 100 | 103.960 | 0.998 | 0.950 | 1.000 | 109.390 | 0.431 | 0.001 | 0.568 | 0.000 |
| greedy_aoi | ood_area | 100 | 121.280 | 0.997 | 0.920 | 1.000 | 81.230 | 0.314 | 0.001 | 0.685 | 0.000 |
| greedy_aoi | ood_cluster | 100 | 93.060 | 0.999 | 1.000 | 0.999 | 158.740 | 0.641 | 0.001 | 0.358 | 0.000 |
| greedy_aoi | ood_density | 100 | 155.880 | 0.999 | 0.990 | 1.000 | 144.140 | 0.576 | 0.001 | 0.423 | 0.000 |
| greedy_aoi | ood_energy | 100 | 203.100 | 0.998 | 1.000 | 1.000 | 67.060 | 0.440 | 0.002 | 0.558 | 0.000 |
| random | id | 100 | 300.000 | 0.952 | 0.470 | 0.425 | 13.730 | 0.067 | 0.481 | 0.452 | 0.000 |
| random | ood_area | 100 | 300.000 | 0.950 | 0.460 | 0.228 | 7.770 | 0.063 | 0.479 | 0.458 | 0.000 |
| random | ood_cluster | 100 | 300.000 | 0.944 | 0.440 | 0.300 | 7.560 | 0.065 | 0.485 | 0.451 | 0.000 |
| random | ood_density | 100 | 300.000 | 0.948 | 0.480 | 0.307 | 17.100 | 0.065 | 0.477 | 0.458 | 0.000 |
| random | ood_energy | 100 | 300.000 | 0.998 | 1.000 | 0.297 | 8.520 | 0.067 | 0.481 | 0.453 | 0.000 |
| tsp | id | 100 | 95.510 | 0.998 | 0.950 | 1.000 | 106.960 | 0.420 | 0.001 | 0.579 | 0.000 |
| tsp | ood_area | 100 | 106.820 | 0.996 | 0.920 | 1.000 | 80.250 | 0.310 | 0.001 | 0.689 | 0.000 |
| tsp | ood_cluster | 100 | 86.290 | 0.999 | 0.990 | 1.000 | 151.200 | 0.607 | 0.001 | 0.392 | 0.000 |
| tsp | ood_density | 100 | 144.110 | 0.999 | 0.980 | 1.000 | 138.340 | 0.550 | 0.002 | 0.448 | 0.000 |
| tsp | ood_energy | 100 | 195.700 | 0.998 | 1.000 | 1.000 | 64.340 | 0.420 | 0.003 | 0.577 | 0.000 |

Figure F4 written to `figures/F4_deg.pdf` (alt text: `figures/F4_deg.pdf.alt.txt`).
