# Checkpoint Manifest — chính sách đã huấn luyện

Owner: **FAO**. Mỗi checkpoint dùng cho bất kỳ con số nào trong bài phải có một dòng ở đây. File model nằm ngoài git (`runs/`, gitignored). Khi cần chia sẻ, đưa vào GitHub Release của repo, và SHA256 phải khớp.

| Experiment | Run ID | Learner | Train dist. | Seed | Steps | SHA256 (từ run_record.json) | Vị trí lưu | Máy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| <EXP-02> | <run-id> | MaskablePPO | dr | 0 | 300000 | <sha256> | <release/asset hoặc runs/...> | <máy> |

Kiểm tra: `python -c "import sys;sys.path.insert(0,'src');from uavaoi.runrecord import sha256_file;print(sha256_file('runs/EXP-02/<run-id>/model.zip'))"`.
