# Degeneracy check (G1 criterion 5)

Threshold for one action type: 0.9. Masked methods: dr_ppo, fixed_ppo.

| Method | Train seed | Episodes | Hover | Slow | Fast | Boundary hits | Episodes with 0 coverage | Early termination | Flags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| dr_ppo | 0 | 500 | 0.43 | 0.57 | 0.00 | 0 | 114 | 0.99 | OK |
| dr_ppo | 1 | 500 | 0.60 | 0.40 | 0.00 | 0 | 36 | 0.99 | OK |
| fixed_ppo | 0 | 500 | 0.75 | 0.22 | 0.03 | 0 | 40 | 0.96 | OK |
| fixed_ppo | 1 | 500 | 0.66 | 0.12 | 0.22 | 0 | 16 | 0.97 | OK |
