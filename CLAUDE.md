# CLAUDE.md — hướng dẫn cho Claude trong repo uav-aoi-drppo

Đề tài: *Generalizable AoI- and Energy-Aware UAV Trajectory Planning for IoT Data Collection via Domain-Randomized PPO*. Đây vừa là bài báo, vừa là đồ án tốt nghiệp của 3 sinh viên. Quy trình làm việc lấy theo repo RIVF-Paper.

Giao tiếp bằng **tiếng Việt**, văn phong học thuật, súc tích. Không bịa số liệu hay trích dẫn. Phân biệt rõ tương quan với nhân quả, và dữ kiện thực nghiệm với giả thuyết.

| Nick | Họ tên | GitHub | Vai trò |
| --- | --- | --- | --- |
| DAT | Hồ Du Tuấn Đạt | Tdat10052499 | DR-PPO, định vị, điều phối, máy cố định đo thời gian, chủ trì bản thảo |
| LDN | Dương Ngọc Linh Đan | Yui-Mika | Ma trận thực nghiệm, thống kê, gate report, claim–evidence, hình |
| FAO | Nguyễn Minh Chính | F4ol4n | Môi trường, tái lập, chi phí tính toán, provenance, DQN, quỹ đạo |

## Khi được hỏi "hôm nay tôi cần làm gì?"
Dùng skill **`hom-nay`** (`.claude/skills/hom-nay/SKILL.md`). Nếu skill không tự nạp, đọc file đó và làm theo. Tóm tắt:
1. Nếu working tree sạch thì `git pull --rebase`.
2. Chạy `python scripts/today.py --json`, đúng ngày giờ Việt Nam. Nếu chưa biết nick, hỏi một lần rồi chạy `--set-nick`.
3. Trình bày kế hoạch theo thứ tự: quá hạn → cần review → hôm nay → bị chặn. Tách rõ phần Claude làm và phần thành viên phải tự làm. Hỏi một câu: "Bắt đầu với … nhé?"
4. Thực hiện theo quy tắc dưới. Bắt đầu task thì `--start <ID>`. Xong task thì `--done <ID> --evidence "..."`. Second reader dùng `--approve`.
5. Cuối ngày dùng skill **`ket-thuc-ngay`**: ghi chú Form H, cập nhật status, commit, push.

## Cách làm việc của nhóm (từ 25/10/2026)
- Khoảng 80% công việc làm qua Claude. Nhóm gặp mặt làm việc **thứ Ba, thứ Tư, thứ Sáu** và **không ghi biên bản họp**.
- **Trao đổi giữa thành viên qua GitHub.** Khi thành viên cần câu trả lời, số liệu hay việc từ người khác, Claude soạn file `notes/yeu-cau/<YYYY-MM-DD>_<nick>_can-<NICK>_<chủ-đề>.md` (mỗi việc một mục `## A1. ...`), thành viên đọc lại, rồi commit và push lên `main`. Quy ước: `notes/yeu-cau/README.md`.
- **Yêu cầu gửi cho thành viên** hiện trong `today.py` ở mục *YÊU CẦU GỬI BẠN* (cả các file cũ `notes/*_can-<NICK>.md`). Trình bày chúng cùng mức ưu tiên với việc quá hạn. Trả lời bằng dòng `<NICK>:` ngay dưới mục; quyết định do thành viên đưa ra, Claude chỉ soạn và ghi lại.

Khi **không có shell** (ví dụ Claude trên web, repo chỉ đồng bộ dạng file), làm như sau:
- Đọc `schedule/tasks.json` và `schedule/status/<NICK>.json`.
- Lấy ngày hôm nay theo giờ Việt Nam. Hỏi thành viên nếu không chắc.
- Lọc task theo các điều kiện:
  - `owner` ∈ {NICK, ALL};
  - `start ≤ hôm nay ≤ due` (hôm nay), hoặc `due < hôm nay` mà chưa `done` (quá hạn);
  - task có `reviewer == NICK` mà owner đã `done` (cần review).
- Sau đó trình bày như bước 3. Đưa lệnh `today.py` để thành viên tự chạy cập nhật trạng thái.

## Bản đồ repo
- `schedule/tasks.json`: **lịch theo ngày, nguồn sự thật**. Chỉ DAT sửa, qua PR. `schedule/SCHEDULE.md` sinh từ đó.
- `schedule/status/<NICK>.json`: trạng thái của từng người. Mỗi người chỉ ghi file của mình, thông qua `today.py`.
- `docs/05_ke_hoach.md`: kế hoạch và **tiêu chí gate G0–G3**. `Project Agreement.md` là Form A.
- `notes/workbook_forms.md`: Form B–J và quy ước tên file. `notes/EXP-*_card.md`: experiment card.
- `results/raw/`: **chỉ ghi thêm**. `results/processed/` và `results/analysis/claim_evidence.md` sinh từ raw.
- `src/uavaoi/`: môi trường, năng lượng, kênh, kịch bản, heuristic, thống kê, run record.
- `scripts/`: các script chính.
  - `train_ppo.py` và `evaluate.py`: bắt buộc truyền `--experiment-id`.
  - `analyze.py`, `run_smoke_test.py`, `today.py`.
- `tests/`: chạy `python tests/test_core.py` (14 kiểm thử) và `python tests/test_schedule.py`.

## Quy tắc không được vi phạm
1. **Experiment card trước, chạy sau.** Không chạy thực nghiệm không có card. Không sửa hay xoá `results/raw/`.
2. **Provenance.** Mọi lần chạy đi qua script để có `run_record.json`, gồm commit, patch, cấu hình, seed và SHA256 checkpoint.
3. **Owner và second reader.** Một con số chỉ vào bài khi second reader đã kiểm, tức claim–evidence ở trạng thái *independently checked*.
4. **Số đo thời gian** chỉ lấy từ máy cố định của DAT.
5. **Thống kê.**
   - Đơn vị lặp là seed huấn luyện.
   - Pilot 2 seed thì chỉ mô tả, không p-value.
   - PREREG khoá tại G1; sau đó không đổi giả thuyết hay ngưỡng.
6. **Tài liệu.** Form B chỉ viết từ văn bản thật, mỗi nhận định có mục, bảng hoặc hình. Không truy cập được toàn văn thì nói rõ. Thông tin xuất bản chưa kiểm thì đánh dấu ✱.
7. **Định vị.** Bayerlein et al. 2021 đã làm tổng quát hoá theo tham số kịch bản, nên **không** viết "đầu tiên tổng quát hoá" (xem `docs/01` §3).
8. **Git.**
   - Mã trong `src/` và `scripts/` đi qua nhánh `<nick>/<chủ-đề>` và PR có second reader review.
   - `notes/` và `schedule/status/` được commit thẳng `main`.
   - Message theo mẫu `[NICK] YYYY-MM-DD: ...`.
9. **Không thay mặt người.** Không tự gửi email, mời collaborator, nộp bài hay chấp nhận điều khoản. Chỉ soạn nháp.
10. **Gate quan trọng hơn lịch.** Task trễ trên đường tới gate thì báo DAT ngay, không âm thầm dời hạn.

## Lệnh nhanh
```bash
python scripts/today.py                 # việc hôm nay (dạng đọc)
python scripts/today.py --team          # cả nhóm (DAT dùng để điều phối)
python scripts/today.py --date 2026-11-03
python tests/test_core.py && python scripts/run_smoke_test.py
```
