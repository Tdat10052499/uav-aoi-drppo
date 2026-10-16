# uavaoi — môi trường & mã khởi đầu cho đề tài DR-PPO UAV–AoI

Mô hình chi tiết: `../docs/02_mo_hinh_he_thong.md`. Giao thức thực nghiệm: `../docs/03_giao_thuc_thuc_nghiem.md`.

## Cấu trúc
```
uavaoi/
  energy.py      # công suất đẩy UAV cánh quay (Zeng et al., Eq. 6), V_me, V_mr
  channel.py     # kênh LoS, tốc độ truyền, bán kính thu hiệu dụng
  scenarios.py   # phân phối huấn luyện (DR, fixed) và 5 bộ đánh giá (ID + 4 OOD)
  env.py         # UAVAoIEnv (Gymnasium API), quan sát bản đồ căn tâm 5x31x31, 17 hành động
  baselines.py   # random, greedy-AoI, TSP (NN + 2-opt)
  stats.py       # bootstrap CI, IQM, kiểm định hoán vị, Cliff's delta, Holm
scripts/
  evaluate.py    # đánh giá heuristic hoặc mô hình SB3 -> CSV
  train_ppo.py   # huấn luyện PPO / MaskablePPO / DQN (cần PyTorch)
  analyze.py     # tổng hợp CSV, kiểm định H1/H2 -> bảng Markdown
tests/test_core.py
results/         # kết quả heuristic tham chiếu (100 episode/bộ)
```

## Cài đặt
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt          # numpy là bắt buộc; phần còn lại để huấn luyện
```
Môi trường, heuristic, thống kê và kiểm thử chạy được **chỉ với NumPy** (có lớp tương thích khi thiếu Gymnasium).

## Chạy nhanh
```bash
python tests/test_core.py                       # hoặc: pytest -q
python scripts/evaluate.py --method tsp greedy_aoi random --episodes 100 --out results/heuristics.csv
python scripts/analyze.py results/heuristics.csv
```

## Huấn luyện (máy có PyTorch)
```bash
for s in 0 1 2 3 4 5 6 7 8 9; do
  python scripts/train_ppo.py --train dr    --seed $s --timesteps 2000000 --masked
  python scripts/train_ppo.py --train fixed --seed $s --timesteps 2000000 --masked
done
python scripts/evaluate.py --model runs/dr_ppo_mask_lam0.1_s0/model.zip --label dr_ppo --train-seed 0 --out results/dr_s0.csv
python scripts/analyze.py results/*.csv --out results/summary.md
```
`--timesteps 2000000` là điểm xuất phát, **chưa được hiệu chỉnh**: đo thời gian 100k bước ở tuần 3 rồi quyết định ngân sách (`docs/03` §7).

## Trạng thái kiểm chứng (16/10/2026)
- 12/12 kiểm thử đơn vị đạt (NumPy 2.5.3, Python 3.13).
- Đánh giá heuristic 100 episode × 5 bộ đã chạy; kết quả trong `results/`.
- `train_ppo.py` **chưa được chạy** trong môi trường dựng bộ mã này (không truy cập được PyPI/PyTorch). Cần chạy thử 10k bước để phát hiện lỗi API trước khi chạy dài.
