# DAT → FAO: số đo EXP-01 trên laptop DAT — 26/10/2026

> Trả lời bằng dòng `FAO:` dưới mỗi mục. Quy ước: `notes/yeu-cau/README.md` (PR #28).

## A1. Cập nhật ước lượng chi phí (W1-FAO-05) bằng steps/s đo trên laptop DAT
- Run `results/raw/EXP-01/dr_ppo_mask_lam0.1_s0_20261026-132835` (commit ff6d658, không có uncommitted patch): MaskablePPO, `--train dr --seed 0 --timesteps 100000 --masked --n-envs 8`, **CPU** (torch 2.14.1+cpu), `wall_time_s = 279.0`, **`steps_per_s = 358.4`** (theo `run_record.json`).
- Run 10k (`dr_ppo_mask_lam0.1_s0_20261025-115314`, `--n-envs 2`): 43.6 s, 229.2 bước/s. So với laptop FAO cùng cấu hình: 68.2 bước/s.
- Máy: Laptop DAT, Ryzen AI 7 350, 32 GB, Windows 11 10.0.26300, Python 3.12.0, NumPy 2.5.4 (`environment/machine_notes.md`).
- Chưa đo: GPU (chưa cài torch CUDA), và DQN trên máy DAT. Laptop DAT là máy cố định **chưa được DAT xác nhận chính thức** (mục A4 trong `notes/2026-10-21_fao_can-DAT.md` vẫn mở), nên ghi số này là "đo trên laptop DAT, CPU" cho tới khi A4 được trả lời.
- Cần FAO: điền bảng §2 trong `notes/2026-10-21_fao_chi-phi-nhap.md` với 358,4 bước/s cho PPO và cho biết có cần DAT đo thêm DQN không.

FAO: Đã điền, 26/10. Bảng giờ máy theo thực nghiệm ở `notes/2026-10-21_fao_chi-phi-nhap.md` §2 và §4, chép sang `Project Agreement.md` §5; số ghi là "đo trên laptop DAT, CPU". Tổng 159,2 M bước cần 123,4 giờ máy nếu mọi learner chạy 358,4 bước/s, hoặc 162,1 giờ nếu DQN chậm 3,5 lần như trên laptop FAO. Cả hai đều kịp trước 13/12.
FAO: **Có, nên đo DQN.** Tỉ lệ 3,5 lần lấy từ máy khác và cấu hình khác, mà EXP-04 là phần dễ lệch ước lượng nhất (15,5 hay 54,3 giờ). Đề xuất đo sau khi PR #20 merge, vì card EXP-04 chỉ có trên nhánh đó: `python scripts/train_ppo.py --experiment-id EXP-04 --algo dqn --train dr --seed 0 --timesteps 100000`, CPU, cùng commit với lần đo PPO nếu được. Việc này không chặn G0.

## A2. Kết quả so khớp heuristic (cho Form C của W1-FAO-04)
- Run `results/raw/EXP-01/20261025-115153` (laptop DAT) so với run của FAO `20261020-084218`: 1500/1500 dòng cùng khoá (method, suite, episode_seed), **0 dòng lệch ở mọi cột số** (sai số tương đối 1e-9; chênh lệch lớn nhất bằng 0).
- Dòng "Second reader (DAT)" trong `notes/EXP-01_reproduction_card.md` sẽ được điền sau khi PR #18 merge, để tránh xung đột với phần Form C của PR đó.

FAO: Đã kiểm lại độc lập bằng `scripts/compare_events.py` (PR #27): `results/raw/EXP-01/20261020-084218/events.csv` so với `results/raw/EXP-01/20261025-115153/events.csv` cho 1500 dòng so sánh, 0 dòng lệch, 0 dòng thiếu, kết quả MATCH. Đồng ý điền dòng second reader sau khi PR #18 merge; W1-FAO-04 chờ tới lúc đó.
