# Workbook Forms — DR-PPO UAV–AoI

Bộ form thích ứng từ quy trình của dự án RIVF-Paper cho bài toán học tăng cường. Form A là `Project Agreement.md` ở gốc repo. Sao chép form vào file ghi chú tương ứng rồi điền dần khi có bằng chứng. Trường `<...>` là chỗ trống. **Điền form không có nghĩa là đã chạy thực nghiệm.**

Quy ước tên file:
| Loại | Tên file | Ví dụ |
| --- | --- | --- |
| Ghi chú đọc (B) | `notes/reading/<khoá-bib>_<NICK>.md` | `notes/reading/bayerlein2021multi_DAT.md` |
| Tái lập (C) | `notes/EXP-xx_reproduction.md` | `notes/EXP-01_reproduction.md` |
| Experiment card (D) | `notes/EXP-xx_<tên>_card.md` | `notes/EXP-02_pilot_card.md` |
| Run record (E) | tự sinh: `results/raw/<EXP>/<run-id>/run_record.json` | |
| Claim–evidence (F) | `results/analysis/claim_evidence.md` | |
| Quyết định gate (G) | `notes/<YYYY-MM-DD>_gate_<G#>_report.md` | `notes/2026-11-15_gate_G1_report.md` |
| Ghi chú ngày (H) | `notes/<YYYY-MM-DD>_<nick>.md` | `notes/2026-10-19_ldn.md` |
| Phản biện (I) | `notes/review_log.md` | |
| Ghi chú giảng viên | `notes/<YYYY-MM-DD>_gvhd.md` | |

---

## B. Ghi chú đọc — mỗi nguồn gần một file

```text
Tiêu đề / tác giả / năm / nơi công bố hoặc trạng thái preprint:
URL nguồn gốc và phiên bản/ngày truy cập:
Người đọc (NICK):

Bài báo trả lời câu hỏi gì:
Giả định hệ thống (số UAV, kênh, mô hình năng lượng, mục tiêu AoI hay dữ liệu):
Cơ chế, diễn đạt bằng lời của mình:
Bằng chứng mạnh nhất (mục/bảng/hình):
Đánh giá trên kịch bản khác tập huấn luyện? Loại dịch chuyển nào?
Số seed / cách báo cáo độ bất định:
Đối chứng gần nhất và độ công bằng của so sánh:
Giới hạn đã biết:
Khác biệt với đề tài (điền thẳng vào ma trận docs/04 §5):
Có mã nguồn/dữ liệu không:
Một câu hỏi cho nhóm:
```

## C. Bản ghi tái lập — trước khi đưa phương pháp đề xuất vào

```text
Thực nghiệm tham chiếu và nguồn (vd. results/raw/heuristics/heuristics_100ep_2026-10-16.csv):
Kết quả kỳ vọng và sai số chấp nhận:
Commit mã đã ghim:
Thay đổi so với tham chiếu:
Môi trường và phần cứng:
Manifest kịch bản (data/eval_manifest.json) — digest khớp? :
Checkpoint chính sách (nếu có) — nguồn và SHA256:
Lệnh chạy và cấu hình:
Seed và vai trò:
Ranh giới đo thời gian và warmup:
Đường dẫn raw:

Kết quả quan sát và số mẫu:
Chênh lệch so với tham chiếu:
Kiểm tra đã làm để giải thích chênh lệch:
Điều còn chưa chắc:
Second reader và ngày xác minh:
```

## D. Experiment card — viết TRƯỚC khi chạy

```text
Experiment ID:
Owner / second reader:
Thăm dò (exploratory) hay khẳng định (confirmatory):
Câu hỏi nghiên cứu và giả thuyết:

Biến thay đổi và các giá trị:
Điều kiện cố định:
Đối chứng (baseline):
Kiểm soát loại trừ giải thích khác:
Ngân sách tương đương giữa các phương pháp (bước huấn luyện, lượt Optuna, thông tin quan sát) và chênh lệch không tránh được:
Quy tắc chọn kịch bản/bộ đánh giá:
Công thức chỉ số, đơn vị, mẫu số:
Đơn vị lặp độc lập (seed huấn luyện):
Danh sách seed / ghép cặp / thứ tự chạy:
Kế hoạch phân tích và báo cáo độ bất định:
Xử lý thất bại / quá thời gian:
Thời gian pilot và ước lượng tổng chi phí:

Kết quả kỳ vọng nếu giả thuyết đúng:
Kết quả sẽ bác bỏ hoặc làm yếu giả thuyết:
Tiêu chí tiếp tục/dừng khai báo trước:
Trường raw cần cho hình dự kiến:
```

## E. Run record — tự sinh với mỗi lần chạy

`src/uavaoi/runrecord.py` ghi `run_record.json` vào `results/raw/<EXP>/<run-id>/` cho mọi lần chạy `evaluate.py`, `train_ppo.py`, `run_smoke_test.py`:

```json
{
  "run_id": "<duy-nhất>",
  "experiment_id": "<EXP-xx>",
  "status": "<completed|failed|timed_out|running>",
  "code_revision": "<commit>",
  "uncommitted_patch_path": "<uncommitted.patch nếu working tree bẩn>",
  "config_path": "config.json",
  "environment_path": "environment.json",
  "data_manifest_path": "data/eval_manifest.json",
  "checkpoint_digest": "<sha256:... | not-applicable>",
  "seeds": {},
  "started_at": "<+07:00>",
  "finished_at": "<+07:00>",
  "counts": {},
  "metrics": {},
  "raw_events_path": "events.csv",
  "warnings": [],
  "failure_reason": null
}
```

Không mã hoá phép đo thiếu thành 0. Không âm thầm loại bỏ lần chạy thất bại: lần chạy lỗi vẫn giữ thư mục và `status: failed`.

## F. Bảng claim–evidence — duy trì trong lúc phân tích

Ở `results/analysis/claim_evidence.md`. Trạng thái: proposed → measured → independently checked → narrowed/removed.

## G. Quyết định tại gate

```text
Ngày và gate:
Bằng chứng xem xét, kể cả lần chạy thất bại (run ID):
Baseline có chạy đúng không? Bằng chứng:
Hiệu ứng chính có đạt tiêu chí khai báo trước không? Bằng chứng (bảng tiêu chí):
Giải thích thay thế mạnh nhất còn đứng vững:
Trùng lặp với công trình gần nhất còn chưa giải quyết:
Nhu cầu tính toán/thời gian còn lại:

Quyết định: tiếp tục / debug vấn đề cụ thể / thu hẹp / dừng
Lý do:
Phạm vi tuyên bố được duyệt:
Thực nghiệm tiếp theo và owner:
Ngày quyết định tiếp theo:
Ý kiến giảng viên:
```

## H. Ghi chú ngày — 3 câu + 1 bằng chứng

```text
Ngày / NICK:
Hôm nay biết thêm điều gì:
Bằng chứng: <run ID, hình, hoặc commit>
Điều còn chưa chắc:
Thực nghiệm nhỏ nhất có tính quyết định cho ngày mai:
Owner và second reader:
Cần giúp gì, kèm ví dụ tái hiện nhỏ nhất:
```
"Đã làm mô hình" không phải ghi chú; đồng đội cần biết họ có thể dựa vào điều gì.

## I. Nhật ký phản biện

| Phản biện | Vì sao có thể làm mất hiệu lực tuyên bố | Bằng chứng hoặc thực nghiệm cần làm | Sửa đổi và owner | Đã giải quyết? |
| --- | --- | --- | --- | --- |
| <ví dụ: "Bayerlein 2021 đã làm tổng quát hoá"> | <đóng góp không mới> | <ma trận docs/04 §5, câu định vị docs/01 §3> | <DAT> | Không |

## J. Bàn giao bản thảo & artifact

Dùng danh sách kiểm tra ở `docs/06_dan_y_bai_bao_va_do_an.md` §3, cộng thêm:
- [ ] Một thành viên khác người chạy chính đã chạy smoke test và kiểm tra lại ít nhất một con số chủ chốt theo README.
- [ ] Mọi con số trong bài trỏ tới một dòng claim–evidence đã được kiểm tra độc lập.
- [ ] Lần chạy thất bại, bị loại, chạy muộn đều được giải trình.
- [ ] Bản PDF nộp, commit mã, cấu hình và manifest bằng chứng được lưu trữ cùng nhau (tag git `submission-<venue>`).
