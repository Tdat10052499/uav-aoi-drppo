# FAO → DAT: việc cần DAT xử lý — 21/10/2026

> Ghi chú từ FAO. Phần A là các vấn đề **ngoài lịch** (`schedule/tasks.json` chưa có task), cần DAT quyết định hoặc đưa vào lịch. Phần B là việc đã có trong lịch đang chờ DAT. Trả lời ngay trong file này (thêm dòng `DAT:` dưới mỗi mục), hoặc trên issue/PR tương ứng.

## A. Ngoài lịch: cần DAT quyết định

### A1. `buffer_size` của DQN cho pha chính EXP-04 (trước G1)
- RAM của replay buffer ≈ 2 × buffer × 4805 × 4 byte:
  - 200k (mặc định cũ) ≈ 7,7 GB;
  - 100k ≈ 3,8 GB;
  - 50k ≈ 1,9 GB.
- Laptop FAO không chạy được 200k: lúc chạy chỉ còn khoảng 3,4 GB trống.
- PR #20 đã thêm `--dqn-buffer-size` và `--dqn-learning-starts`, mặc định vẫn là 200k / 20k.
- Câu hỏi: giữ 200k và chỉ chạy DQN trên máy đủ RAM, hay giảm buffer cho mọi seed? Giá trị này phải khoá trong PREREG tại G1.
- Chi tiết: `notes/EXP-04_dqn_card.md`, mục câu hỏi mở.

DAT: (30/10) Giữ 200k, chỉ chạy DQN trên laptop DAT (DECISIONS 2026-10-30). Lịch đổi theo phương án (a) ở `notes/2026-10-30_fao_phan-seed-nhap.md` §3: DAT chạy (W5-DAT-03), FAO chốt card và kiểm; PR #34.

### A2. Tinh chỉnh siêu tham số cho DQN
DQN có được tinh chỉnh (Optuna) với ngân sách bằng PPO không, hay dùng mặc định SB3? Điều này ảnh hưởng tới độ công bằng khi so DR-DQN với DR-PPO. Xem `notes/EXP-04_dqn_card.md`.

DAT: (30/10) Có. DQN được tinh chỉnh bằng Optuna với cùng ngân sách như PPO (20 trial × 200k bước, cùng sampler seed, chỉ `id`); DECISIONS 2026-10-30; `tune_ppo.py --algo dqn` (PR #30, đã merge).

### A3. OH-DRL 2025: không truy cập được toàn văn
- FAO không tải được PDF: không có bản arXiv, không có quyền IEEE Xplore, không mua được.
- `notes/reading/ohdrl2025_FAO.md` hiện chỉ dựa trên tóm tắt.
- Đây là công trình gần nhất về **cặp AoI + năng lượng bay**, nên cột "huấn luyện trên nhiều bố trí" và cột "OOD" của nó quan trọng cho G0.
- Nhờ DAT (hoặc LDN) thử qua IEEE Xplore của trường, hoặc quyết định gửi email xin bản tác giả.
- DOI: 10.1109/TWC.2025.3545451.

DAT: (30/10) Chưa lấy được toàn văn. DAT sẽ thử IEEE Xplore qua thư viện trường hoặc nhờ GVHD trước họp G0 (04/11). Nếu không được, hàng ma trận giữ "chỉ tóm tắt" và báo cáo G0 ghi đây là rủi ro trùng lặp lớn nhất còn mở (`notes/2026-11-04_gate_G0_report.md`).

### A4. Máy cố định đo thời gian
- Chưa có xác nhận chính thức laptop DAT là máy cố định (biên bản họp 19/10 trong `notes/2026-10-19_hop-nhom.md` còn trống).
- Nhờ DAT chạy 3 lệnh trong `environment/machine_notes.md` và gửi kết quả, gồm OS, Python, NumPy, torch.
- Cần chốt: số đo thời gian lấy trên CPU hay GPU? Hai cách cho bảng chi phí khác nhau.
- RTX 5060 (thế hệ Blackwell) có thể cần bản torch dựng với CUDA ≥ 12.8. Đây là hiểu biết chung, chưa kiểm trên máy DAT.

DAT: (30/10) Laptop DAT là máy cố định đo thời gian; số 358,4 bước/s (CPU, `--n-envs 8`) đã đo trên máy này (W1-DAT-05, `notes/EXP-01_reproduction_card.md`). CPU hay GPU: chờ DAT chốt; đề xuất CPU vì mọi ước lượng chi phí hiện dựa trên CPU. Phần chạy 3 lệnh trong `environment/machine_notes.md` và đo DQN 100k bước: DAT tự chạy trên máy mình.

### A5. `paper/references.bib`
Danh sách tác giả đầy đủ đã có trong Form B:
- `sun2025aoi` đang ghi `Sun, Geng and others`; danh sách đủ ở `notes/reading/sun2025aoi_FAO.md`.
- `ohdrl2025` đang ghi `VERIFY author list`; danh sách đủ ở `notes/reading/ohdrl2025_FAO.md`. Nguồn là trang UniSC, chưa đối chiếu IEEE ✱.

DAT: (30/10) Đã xử lý ở PR #24 (merge 30/10): `sun2025aoi` và `ohdrl2025` có đủ tác giả; `ohdrl2025` vẫn ghi VERIFY với IEEE Xplore ✱.

### A6. Thông tin cho G0 (không cần trả lời, chỉ để DAT nắm)
- Trong 4 bài FAO đọc, chưa bài nào đủ cả 5 cột của ma trận `docs/04` §5. OH-DRL còn "Chưa rõ" ở 3 cột.
- Sun 2025 §VII nêu domain randomization là **hướng tương lai**, tức bài đó chưa làm. Có thể trích làm bằng chứng khoảng trống, nhưng không viết "đầu tiên".
- Liu 2024 dùng DR nhưng không có đối chứng Fixed và chỉ 1 seed. Bài cho thấy hiệu năng giảm dần khi lệch xa phân phối huấn luyện, và DR-PPO của ta có thể gặp điều tương tự.
- Liu 2024 gợi ý một ablation "pool cố định K bố trí" (giữa Fixed và DR). Có thêm vào ma trận không? Nếu có thì phải khoá trước G1. Đề xuất mặc định của FAO: **không thêm**, để giữ phạm vi.

DAT: (30/10) Đồng ý mặc định của FAO: không thêm ablation "pool cố định K bố trí", để giữ phạm vi (DECISIONS 2026-10-30).

### A7. Quan sát từ `plot_trajectory.py` (PR #19)
Trên các quỹ đạo đã vẽ, TSP không lần nào dùng tốc độ chậm V_me. Cần lưu ý khi viết về baseline và ablation A5 (một tốc độ).

DAT: (30/10) Đã ghi nhận. Khi viết về TSP và A5 phải nói rõ TSP không dùng V_me trên các quỹ đạo đã vẽ (PR #19); đây là quan sát định tính, chưa đo tỉ lệ.

## B. Trong lịch: đang chờ DAT

| Việc | Hạn | Chặn việc của FAO |
| --- | --- | --- |
| Chạy lại EXP-01 bước 1–3 trên máy DAT (second reader) | 22/10 | W1-FAO-04, đóng issue #5 |
| Review PR #18 (train_ppo 10k) | — | W1-FAO-04 (dòng train_ppo trong Form C nằm trên PR này) |
| Review PR #19 (plot_trajectory.py) | — | hình F6 về sau |
| Review PR #20 (EXP-04 card, tham số DQN) | — | A1, A2 |
| W1-DAT-05: steps/s trên máy cố định | trước 23/10 | W1-FAO-05 (ước lượng chi phí) |
| Điền biên bản họp 19/10 (W1-ALL-01) | quá hạn | — |

Kết quả FAO đã có trên máy mình: 14/14 kiểm thử, smoke PASS, 0/1500 dòng lệch (run `EXP-01/20261020-084218`).
