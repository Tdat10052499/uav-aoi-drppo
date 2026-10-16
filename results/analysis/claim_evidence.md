# Claim–Evidence Table (Form F)

Mọi câu có con số trong bài phải trỏ tới một dòng ở đây với trạng thái **independently checked**. Second reader ghi tên và ngày.

| Claim ID | Câu dự kiến trong bài | Experiment/run IDs | Raw evidence & script | Ước lượng & độ bất định | Phạm vi & phản chứng | Trạng thái / second reader |
| --- | --- | --- | --- | --- | --- | --- |
| C0 | The simulator is deterministic and reproducible from the released seeds. | EXP-01 | `results/raw/EXP-01/*/events.csv`, `scripts/run_smoke_test.py` | Số dòng lệch: <pending> | Chỉ đúng với cùng phiên bản NumPy? | proposed / FAO→DAT |
| C1 | Domain randomization reduces OOD degradation relative to fixed-layout training on ≥3 of 4 structured shifts. | EXP-03 (pilot: EXP-02) | `results/raw/EXP-03/*/events.csv`, `scripts/analyze.py` (H1) | deg DR vs Fixed, 95% CI, p_Holm, Cliff's δ: <pending> | Có thể chỉ đúng với quan sát căn tâm (A2/A3) | proposed / LDN→FAO |
| C2 | DR-PPO attains lower mean AoI than a full-information TSP heuristic on clustered layouts at equal energy budget. | EXP-03 | idem (H2) | <pending> | Heuristic có thông tin đầy đủ; có thể bác bỏ | proposed / LDN→DAT |
| C3 | Increasing λ trades AoI for energy along a monotone frontier, and the policy shifts from V_mr to V_me. | EXP-05 (RQ2) | `results/raw/EXP-05/*` | <pending> | Có thể không đơn điệu | proposed / DAT→LDN |
| C4 | (Ablation) The centred-map observation is necessary for the C1 effect. | EXP-06 (A2/A3) | `results/raw/EXP-06/*` | Mô tả, không kiểm định | Thăm dò (H3) | proposed / DAT→FAO |

Danh mục experiment ID dự kiến: EXP-01 tái lập · EXP-02 pilot G1 · EXP-03 khẳng định chính (10 seed) · EXP-04 DR-DQN · EXP-05 quét λ · EXP-06 ablation quan sát A2/A3 · EXP-07 ablation mask/tốc độ A4/A5.
