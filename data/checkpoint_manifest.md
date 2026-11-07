# Checkpoint Manifest — chính sách đã huấn luyện

Owner: **FAO**. Mỗi checkpoint dùng cho bất kỳ con số nào trong bài phải có một dòng ở đây. File model nằm ngoài git (`runs/`, gitignored). Khi cần chia sẻ, đưa vào GitHub Release của repo, và SHA256 phải khớp.

| Experiment | Run ID | Learner | Train dist. | Seed | Steps | SHA256 (từ run_record.json) | Vị trí lưu | Máy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| <EXP-02> | <run-id> | MaskablePPO | dr | 0 | 300000 | <sha256> | <release/asset hoặc runs/...> | <máy> |
| EXP-02 | dr_ppo_mask_lam0.1_s0_20261103-131752 | MaskablePPO | dr | 0 | 300000 | b6f9a2f7e7812788e9029d07bae81f88047ab7cce6b1413424a3a220ffe3b8b0 | runs/EXP-02/dr_ppo_mask_lam0.1_s0_20261103-131752/model.zip | LAPTOP-21KJQDU4 |
| EXP-02 | dr_ppo_mask_lam0.1_s1_20261103-142030 | MaskablePPO | dr | 1 | 300000 | 56cec52a791051965d31e2f35af614514a87ae1a407a88d49cccf101cecc1cac | runs/EXP-02/dr_ppo_mask_lam0.1_s1_20261103-142030/model.zip | LAPTOP-21KJQDU4 |
| EXP-02 | fixed_ppo_mask_lam0.1_s0_20261103-133603 | MaskablePPO | fixed | 0 | 300000 | 1b20097ce2926390b694ec07a555748df57eb714041b5f00b5264914b0b7a8f4 | runs/EXP-02/fixed_ppo_mask_lam0.1_s0_20261103-133603/model.zip | LAPTOP-21KJQDU4 |
| EXP-02 | fixed_ppo_mask_lam0.1_s1_20261103-142041 | MaskablePPO | fixed | 1 | 300000 | dece55a88d47d6ee2f83d55f862521a032b635d06b18c3f4650fb316f82bf527 | runs/EXP-02/fixed_ppo_mask_lam0.1_s1_20261103-142041/model.zip | LAPTOP-21KJQDU4 |
| EXP-03 | dr_ppo_mask_lam0.1_s0_20261104-143805 | MaskablePPO | dr | 0 | 2000000 | 13f9346caa31431f789ed5eae10e5e858a7ba55e9e29d2163ef745658b27e0b6 | runs/EXP-03/dr_ppo_mask_lam0.1_s0_20261104-143805/model.zip | LAPTOP-21KJQDU4 |
| EXP-03 | dr_ppo_mask_lam0.1_s1_20261104-163112 | MaskablePPO | dr | 1 | 2000000 | 64c333ba35755a1e8c1ed5e3ff17a5696d5c3a05fe6062add628a7a84f2304b7 | runs/EXP-03/dr_ppo_mask_lam0.1_s1_20261104-163112/model.zip | LAPTOP-21KJQDU4 |
| EXP-03 | dr_ppo_mask_lam0.1_s2_20261104-182814 | MaskablePPO | dr | 2 | 2000000 | 6d63dbb54cb7c8c316bf340c9b601e65a81e1b0c6f984917569df2c0ae4a3a7a | runs/EXP-03/dr_ppo_mask_lam0.1_s2_20261104-182814/model.zip | LAPTOP-21KJQDU4 |
| EXP-03 | dr_ppo_mask_lam0.1_s3_20261105-140316 | MaskablePPO | dr | 3 | 2000000 | bfe09d6169b88fdbc301c278a04ab265ea33a0f2ec07985fd1c935cc871fedd8 | runs/EXP-03/dr_ppo_mask_lam0.1_s3_20261105-140316/model.zip | LAPTOP-21KJQDU4 |
| EXP-03 | dr_ppo_mask_lam0.1_s4_20261105-163015 | MaskablePPO | dr | 4 | 2000000 | f17ff4d1c92998d3c4d152efaf9324a1ccdccc5a6d7be621efffc94e208ce86b | runs/EXP-03/dr_ppo_mask_lam0.1_s4_20261105-163015/model.zip | LAPTOP-21KJQDU4 |
| EXP-03 | dr_ppo_mask_lam0.1_s5_20261105-185715 | MaskablePPO | dr | 5 | 2000000 | 93503858682f8b338c0737f485813b3eb87ab140553e4302124003560eed7e95 | runs/EXP-03/dr_ppo_mask_lam0.1_s5_20261105-185715/model.zip | LAPTOP-21KJQDU4 |
| EXP-03 | dr_ppo_mask_lam0.1_s6_20261105-212432 | MaskablePPO | dr | 6 | 2000000 | a3979958c5b022c587693bd10aa73bfa799f46669f05ff53987c0a4227a49a6a | runs/EXP-03/dr_ppo_mask_lam0.1_s6_20261105-212432/model.zip | LAPTOP-21KJQDU4 |
| EXP-03 | dr_ppo_mask_lam0.1_s7_20261105-234718 | MaskablePPO | dr | 7 | 2000000 | 617efd7caa545dde2b0e47f395def741a0e135ca32fd08b9cd73c8c44d1b83d9 | runs/EXP-03/dr_ppo_mask_lam0.1_s7_20261105-234718/model.zip | LAPTOP-21KJQDU4 |
| EXP-03 | dr_ppo_mask_lam0.1_s8_20261106-020134 | MaskablePPO | dr | 8 | 2000000 | 73eafe62f25812726cb9f30549b5a006c72fabb95d549a0657b23d2e2f7a0423 | runs/EXP-03/dr_ppo_mask_lam0.1_s8_20261106-020134/model.zip | LAPTOP-21KJQDU4 |
| EXP-03 | dr_ppo_mask_lam0.1_s9_20261106-042816 | MaskablePPO | dr | 9 | 2000000 | 40eee25809e8213bccf14bf73a7c016266c07a1811b1a638174e981819cf6760 | runs/EXP-03/dr_ppo_mask_lam0.1_s9_20261106-042816/model.zip | LAPTOP-21KJQDU4 |
| EXP-03 | fixed_ppo_mask_lam0.1_s0_20261104-143753 | MaskablePPO | fixed | 0 | 2000000 | 0cfa72340d4c5e51778fb3b7b30a60943261e76414be8d1d5b9f3136a88a8675 | runs/EXP-03/fixed_ppo_mask_lam0.1_s0_20261104-143753/model.zip | LAPTOP-21KJQDU4 |
| EXP-03 | fixed_ppo_mask_lam0.1_s1_20261104-170517 | MaskablePPO | fixed | 1 | 2000000 | 0f8965aef2060e2dd00a1550ad6f5cd0c4b05704e817d0ed7a0ba789ff4737f4 | runs/EXP-03/fixed_ppo_mask_lam0.1_s1_20261104-170517/model.zip | LAPTOP-21KJQDU4 |
| EXP-03 | fixed_ppo_mask_lam0.1_s2_20261105-140320 | MaskablePPO | fixed | 2 | 2000000 | e8c4c8e5a583b5934aab51edd38246f288c0960c40f308f269e81dbb186dd99e | runs/EXP-03/fixed_ppo_mask_lam0.1_s2_20261105-140320/model.zip | LAPTOP-21KJQDU4 |
| EXP-03 | fixed_ppo_mask_lam0.1_s3_20261105-155538 | MaskablePPO | fixed | 3 | 2000000 | 1ecd0e1d460ed77c339f07e1909db89281103ef5a3cdae75fa46b25a1516488a | runs/EXP-03/fixed_ppo_mask_lam0.1_s3_20261105-155538/model.zip | LAPTOP-21KJQDU4 |
| EXP-03 | fixed_ppo_mask_lam0.1_s4_20261105-174806 | MaskablePPO | fixed | 4 | 2000000 | 3a5ac433ecf81646b1903d1ef4726b3d2a1d589acdca4b9abcb710b711d5c5b0 | runs/EXP-03/fixed_ppo_mask_lam0.1_s4_20261105-174806/model.zip | LAPTOP-21KJQDU4 |
| EXP-03 | fixed_ppo_mask_lam0.1_s5_20261105-194100 | MaskablePPO | fixed | 5 | 2000000 | 58733dd39e5bfd76a67b779f1cc1e886613d72a51fc0803e4997b30163cc9865 | runs/EXP-03/fixed_ppo_mask_lam0.1_s5_20261105-194100/model.zip | LAPTOP-21KJQDU4 |
| EXP-03 | fixed_ppo_mask_lam0.1_s6_20261105-213358 | MaskablePPO | fixed | 6 | 2000000 | 5e2c581438067df5688370f02f376a4c152bdea1ff39949a1684f98c634794c0 | runs/EXP-03/fixed_ppo_mask_lam0.1_s6_20261105-213358/model.zip | LAPTOP-21KJQDU4 |
| EXP-03 | fixed_ppo_mask_lam0.1_s7_20261105-234214 | MaskablePPO | fixed | 7 | 2000000 | a0b6f40236125771f38c8dbd10e550dea077922518aaa9fbb883977e393c7014 | runs/EXP-03/fixed_ppo_mask_lam0.1_s7_20261105-234214/model.zip | LAPTOP-21KJQDU4 |
| EXP-03 | fixed_ppo_mask_lam0.1_s8_20261106-015541 | MaskablePPO | fixed | 8 | 2000000 | 0867619be068021e07045d35acb5afc46706d3a5910ed25ed906287e28b5718c | runs/EXP-03/fixed_ppo_mask_lam0.1_s8_20261106-015541/model.zip | LAPTOP-21KJQDU4 |
| EXP-03 | fixed_ppo_mask_lam0.1_s9_20261106-035041 | MaskablePPO | fixed | 9 | 2000000 | 40dff521f238200ea141a980d8f75fee9932cf889ff14e9266a803c0ee4a039a | runs/EXP-03/fixed_ppo_mask_lam0.1_s9_20261106-035041/model.zip | LAPTOP-21KJQDU4 |

Sinh dòng từ run record (kiểm SHA256, bỏ qua run đã có): `python scripts/manifest_row.py results/raw/<EXP>/<run-id> --verify --append`.

Kiểm tra thủ công: `python -c "import sys;sys.path.insert(0,'src');from uavaoi.runrecord import sha256_file;print(sha256_file('runs/EXP-02/<run-id>/model.zip'))"`.
