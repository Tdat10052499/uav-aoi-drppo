# FAO cần DAT: model chỉ nạp được bằng đúng bản Python lúc huấn luyện (06/11/2026)

> Trả lời bằng dòng `DAT:` dưới mỗi mục. Claude soạn cho FAO. **Mục 2 cần quyết trước pilot EXP-08p**, vì M3, M4 sẽ huấn luyện trên Kaggle.

1. **Phát hiện (W5-FAO-04).** Trên laptop FAO (Python 3.14.3), `MaskablePPO.load` với model EXP-03 DR s7 (SHA256 khớp) làm Python sập: "Windows fatal exception: access violation", exit 0xC0000005, không in traceback Python. `-X faulthandler` chỉ khung `D:\github\uav-aoi-drppo\scripts\train_ppo.py ... in __init__`.
   - Nguyên nhân (suy luận, chưa kiểm trên máy khác): `SmallCNN` nằm trong `scripts/train_ppo.py`, chạy dưới tên `__main__`, nên cloudpickle lưu lớp theo giá trị, kèm bytecode Python 3.12 của máy DAT. Bytecode không chuyển được giữa các bản Python phụ (3.11, 3.12, 3.14).
   - Hệ quả: 20 model EXP-03 chỉ nạp được bằng Python 3.12. Laptop LDN (3.11.9) cũng sẽ lỗi. Máy cài Python khác bản thì không thể tự tái lập.
   - FAO xử lý EXP-03R bằng venv Python 3.12 riêng, không sửa mã (`notes/EXP-03R_reeval_card.md`, mục "Sửa trước khi chạy").
   - Đề xuất: DAT ghi một dòng DECISIONS và ghi vào `environment/machine_notes.md`: "model EXP-01..03 cần Python 3.12".
   - DAT:
2. **EXP-08 (quyết trước pilot).** `MapCandExtractor` của EXP-08 cũng nằm trong `scripts/train_ppo.py`, nên gặp đúng lỗi này. M3, M4 huấn luyện trên Kaggle. Bản Python của image Kaggle chưa kiểm ✱. Nếu khác 3.12, model Kaggle sẽ không nạp được trên máy DAT để đánh giá.
   - Đề xuất (a), FAO chọn: chuyển `SmallCNN` và `MapCandExtractor` sang `src/uavaoi/nets.py`, rồi `train_ppo.py` và `tune_ppo.py` import từ đó. cloudpickle khi đó lưu lớp theo tên module, nên model nạp được trên mọi bản Python có cùng mã. Kiến trúc không đổi.
     - Kiểm thử: cùng seed thì trọng số khởi tạo trùng bản cũ, và nạp chéo được giữa hai bản Python.
     - FAO mở PR `fao/nets-module`, DAT review, trước EXP-08p.
     - Không áp dụng cho model EXP-03 đã có.
   - (b) Ghim Python 3.12 trên mọi máy, kể cả Kaggle. Rẻ hơn, nhưng phụ thuộc image Kaggle.
   - DAT:
3. **Ghim bản Python.** `environment/requirements.txt` không ghi bản Python. Đề xuất thêm dòng chú thích "Python 3.12 (model EXP-01..03)", kèm bản thư viện của run EXP-03: numpy 2.5.4, torch 2.14.1+cpu, gymnasium 1.4.0, SB3 và sb3_contrib 2.9.0, scipy 1.18.1.
   - DAT:
4. **W3-FAO-01 bước 2 (quỹ đạo ≥ 3/model) cần model EXP-02**, nhưng 4 model pilot chưa có trên Drive.
   - Đã xong bước 1: `data/checkpoint_manifest.md` có 4 dòng EXP-02 và 20 dòng EXP-03, lấy SHA256 từ `run_record.json`. Chỉ s7 và s5 của EXP-03 được FAO băm lại từ file thật.
   - Bước 3 (suy biến) đã làm từ `events.csv`: `results/processed/EXP-02_degenerate.md`.
   - Đề xuất, DAT chọn:
     - (a) EXP-02 đã bị EXP-03 thay, nên bước 2 dùng 2 model EXP-03 FAO đang có (DR s7, Fixed s5), 3 bộ mỗi model;
     - (b) DAT gửi 4 `model.zip` EXP-02 qua Drive.
   - FAO làm (a) trước, vì đã có model và venv Python 3.12.
   - DAT:
