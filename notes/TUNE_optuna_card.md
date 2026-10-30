# TUNE — Tinh chỉnh siêu tham số bằng Optuna, cùng ngân sách cho DR-PPO, Fixed-PPO và DR-DQN

**Owner:** DAT · **Second reader:** FAO · **Task:** W4-DAT-01 (09–13/11/2026), issue #11 · **Gate:** G1 (15/11)
**Viết:** 30/10/2026, trước khi chạy. **Trạng thái: nháp**, Claude soạn theo yêu cầu của DAT. Cần FAO đọc và DAT duyệt trước khi chạy (quy tắc 1). Giao thức lấy từ `docs/03` §3, `docs/DECISIONS.md` (30/10) và mã `scripts/tune_ppo.py` (PR #30, #32).

## D. Experiment card

```text
Experiment ID: TUNE
Owner / second reader: DAT / FAO
Thăm dò hay khẳng định: THỦ TỤC. Không kiểm định giả thuyết nào. Kết quả duy nhất là bộ
siêu tham số cho mỗi learner, ghi vào docs/PREREG.md trước khi khoá tại G1. Không đưa
giá trị mục tiêu của Optuna vào bài như một kết quả.

Câu hỏi: Với cùng ngân sách tinh chỉnh, bộ siêu tham số nào cho AoI trung bình thấp nhất
trên tập kiểm định id, cho từng learner?

Learner (mỗi learner một study):
  1. DR-PPO     --train dr    --masked
  2. Fixed-PPO  --train fixed --masked
  3. DR-DQN     --algo dqn --train dr  (không mask; n_envs = 1; buffer 200k, learning_starts 20k)
  Không tinh chỉnh riêng A4, A5 (DECISIONS 30/10, câu C3 của FAO); chúng dùng bộ của DR-PPO.

Ngân sách (bằng nhau cho cả ba, DECISIONS 30/10):
  20 trial hoàn thành × 200 000 bước/trial; cùng --sampler-seed 0 (TPE); không pruning.
  Trial lỗi được ghi "failed" và không tính vào 20; script dừng nếu số lỗi vượt 20.
  Trial có batch_size không chia hết n_steps × n_envs bị loại (TrialPruned) và không tính.

Không gian tìm kiếm (mã: sample_params, sample_dqn_params trong tune_ppo.py):
  PPO: learning_rate log[1e-5, 1e-3]; n_steps {256, 512, 1024, 2048};
       batch_size {64, 128, 256, 512}; ent_coef log[1e-4, 5e-2];
       gamma {0.95, 0.98, 0.99, 0.995}; clip_range {0.1, 0.2, 0.3}
  DQN: learning_rate; batch_size {64, 128, 256}; gamma; train_freq {1, 4, 8};
       target_update_interval {1000, 5000, 10000}; exploration_fraction {0.1, 0.2, 0.3}

Seed:
  Huấn luyện: --seed 1000 cho mọi trial (seed 0–9 của kết quả chính bị script từ chối).
  Kiểm định: id, 20 episode, seed 200000–200019 (VAL_SEED_BASE + i).
  Không dùng bộ test 100000–100099 và không dùng bộ OOD nào.

Mục tiêu: mean AoI (khe) trên 20 episode kiểm định id; nhỏ hơn là tốt hơn.
Chọn cấu hình: best_trial của mỗi study (best_params.json). Không chọn lại bằng tay.

Máy: laptop DAT, CPU, tuần tự (DQN buffer 200k cần ≈ 7,7 GB RAM).
Chi phí ước lượng (Project Agreement §5, chưa đo DQN trên máy DAT):
  PPO 2 × 4 M bước ≈ 6,2 giờ (358,4 bước/s); DQN 4 M bước ≈ 3,1–10,9 giờ.
  Thời gian của TUNE không phải số đo cho bài.

Thất bại: giữ mọi run_record "failed" trong results/raw/TUNE/; Ctrl+C đóng cả record
  của trial và của study (PR #30).
Trường raw cần: trials.csv, best_params.json, run_record.json của study và từng trial
  (kèm SHA256 checkpoint).

Giới hạn phải ghi trong bài (góp ý số 3 của FAO ở PR #30):
  - Mỗi trial chỉ có 1 seed huấn luyện và 20 episode kiểm định, nên giá trị mục tiêu
    có nhiễu. Thứ hạng giữa các trial gần nhau có thể không ổn định.
  - Tinh chỉnh ở 200k bước, còn kết quả chính chạy khoảng 2 M bước, nên Optuna có thể
    ưu tiên cấu hình học nhanh lúc đầu.
  - Hai nhược điểm trên áp dụng như nhau cho cả ba learner, nên không làm lệch so sánh
    giữa chúng. Nhưng chúng không chứng minh mỗi learner đạt cấu hình tốt nhất có thể.

Kết quả kỳ vọng: ba file best_params.json; giá trị mục tiêu tốt nhất của mỗi learner
  thấp hơn Random trên id (126,24 khe, EXP-01). Nếu không study nào thấp hơn Random,
  dừng lại và báo DAT trước G1, vì có thể chính sách suy biến (kiểm bằng
  check_degenerate.py và plot_trajectory.py trên model của best_trial).
```

## Lệnh

```bash
python scripts/tune_ppo.py --experiment-id TUNE --train dr    --n-trials 20 --masked
python scripts/tune_ppo.py --experiment-id TUNE --train fixed --n-trials 20 --masked
python scripts/tune_ppo.py --experiment-id TUNE --algo dqn --train dr --n-trials 20
```

Lưu ý: W4-DAT-01 trong `schedule/tasks.json` ghi lệnh PPO **thiếu `--masked`** và chưa có lệnh DQN. Kết quả chính dùng MaskablePPO, nên card này dùng lệnh có `--masked`; PR #34 sửa lịch cho khớp.

## Second reader

FAO: đọc card, xác nhận lệnh khớp `docs/03` §3 và DECISIONS 30/10, ký dòng dưới trước khi DAT chạy.

Second reader (FAO) đã đọc card: ____  ngày: ____
