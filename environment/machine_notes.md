# Machine Notes

Owner: **FAO**. Điền sau lần chạy thành công đầu tiên trên mỗi máy (EXP-01).

```bash
python --version
python -c "import numpy, torch; print(numpy.__version__, torch.__version__, torch.cuda.is_available())"
python -c "import platform; print(platform.platform(), platform.machine())"
```

| Máy | Chủ | CPU / RAM | GPU | OS | Python | NumPy | torch | Dùng cho |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Laptop DAT (máy cố định đo thời gian ✱ chờ DAT xác nhận) | DAT | Intel i7-13620H (10C/16T, 2.4–4.9 GHz) / 16 GB DDR5-5200 | NVIDIA RTX 5060 8 GB GDDR7 + Intel Graphics | chờ DAT | chờ DAT | chờ DAT | chờ DAT | **Mọi số đo thời gian** + huấn luyện |
| Laptop FAO | FAO | Intel i7-8665U (4C/8T, 1.9 GHz) / 16 GB | Intel UHD 620 (không CUDA) | Windows 11 (10.0.26300) | 3.14.3 | 2.5.4 | 2.14.1+cpu | Tái lập, huấn luyện CPU |
| Laptop LDN (danduong) | LDN | Intel i7-13620H (10C/16T) / 15,6 GB | RTX 4060 Laptop + Intel UHD (torch bản CPU, chưa dùng GPU) | Windows 11 (10.0.26200) | 3.11.9 | 2.4.6 | 2.14.1+cpu | Phân tích, huấn luyện thêm seed |
| Kaggle T4 (nếu dùng) | FAO | — | T4 ×1 | Linux | | | | Chỉ chạy thêm seed; **không** lấy số thời gian |

FAO, 20/10/2026: cấu hình Laptop DAT do DAT cung cấp (thêm SSD 512 GB NVMe); OS và phiên bản phần mềm chờ DAT chạy 3 lệnh ở trên. RTX 5060 (thế hệ Blackwell) có thể cần bản torch dựng với CUDA ≥ 12.8 — cần kiểm khi cài.

FAO, 19/10/2026: gymnasium 1.4.0, stable-baselines3 2.9.0, sb3-contrib 2.9.0; pip.exe bị Application Control chặn, dùng python -m pip.

## Quy tắc đo
- Số thời gian (steps/s, thời gian suy luận) chỉ lấy từ **một máy cố định**, không chạy tác vụ nặng khác cùng lúc.
- Cùng một bảng so sánh phải từ cùng một máy.

## Môi trường dựng bộ mã (16–17/10/2026, tham chiếu)
Python 3.13, NumPy 2.5.3, không có Gymnasium/PyTorch (lớp tương thích `_compat.py`). Tham chiếu heuristic sinh ra trên môi trường này.