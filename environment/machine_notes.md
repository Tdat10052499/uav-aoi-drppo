# Machine Notes

Owner: **FAO**. Điền sau lần chạy thành công đầu tiên trên mỗi máy (EXP-01).

```bash
python --version
python -c "import numpy, torch; print(numpy.__version__, torch.__version__, torch.cuda.is_available())"
python -c "import platform; print(platform.platform(), platform.machine())"
```

| Máy | Chủ | CPU / RAM | GPU | OS | Python | NumPy | torch | Dùng cho |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Laptop DAT — Acer Nitro ANV16S-61 (máy cố định đo thời gian ✱ chờ DAT xác nhận) | DAT | AMD Ryzen AI 7 350 w/ Radeon 860M (2,00 GHz) / 32 GB, 5600 MT/s (31,3 GB dùng được) | NVIDIA GeForce RTX 5060 Laptop 8 GB + AMD Radeon 860M | Windows 11 (10.0.26300) AMD64 | 3.12.0 | 2.5.4 | 2.14.1+cpu (CUDA chưa cài) | **Mọi số đo thời gian** + huấn luyện |
| Laptop FAO | FAO | Intel i7-8665U (4C/8T, 1.9 GHz) / 16 GB | Intel UHD 620 (không CUDA) | Windows 11 (10.0.26300) | 3.14.3 | 2.5.4 | 2.14.1+cpu | Tái lập, huấn luyện CPU |
| Laptop LDN (danduong) | LDN | Intel i7-13620H (10C/16T) / 15,6 GB | RTX 4060 Laptop + Intel UHD (torch bản CPU, chưa dùng GPU) | Windows 11 (10.0.26200) | 3.11.9 | 2.4.6 | 2.14.1+cpu | Phân tích, huấn luyện thêm seed |
| Kaggle T4 (nếu dùng) | FAO | — | T4 ×1 | Linux | | | | Chỉ chạy thêm seed; **không** lấy số thời gian |

DAT, 25/10/2026: sửa cấu hình Laptop DAT theo ảnh Settings → System → About (trước đó ghi nhầm i7-13620H / 16 GB): AMD Ryzen AI 7 350, 32 GB RAM, RTX 5060 Laptop 8 GB, SSD 954 GB. Đã chạy 3 lệnh trong venv: Python 3.12.0, NumPy 2.5.4, torch 2.14.1+cpu (`cuda.is_available()` = False), gymnasium 1.4.0, SB3 2.9.0, sb3-contrib 2.9.0; `tests/test_core.py` 14/14, smoke test PASS (`results/raw/SMOKE/20261025-114538`, thư mục không commit). Bản torch có CUDA cho RTX 5060 chưa cài; cài khi đo GPU ở W1-DAT-05.

FAO, 20/10/2026: cấu hình Laptop DAT do DAT cung cấp (thêm SSD 512 GB NVMe); OS và phiên bản phần mềm chờ DAT chạy 3 lệnh ở trên. RTX 5060 (thế hệ Blackwell) có thể cần bản torch dựng với CUDA ≥ 12.8 — cần kiểm khi cài.

FAO, 19/10/2026: gymnasium 1.4.0, stable-baselines3 2.9.0, sb3-contrib 2.9.0; pip.exe bị Application Control chặn, dùng python -m pip.

## Quy tắc đo
- Số thời gian (steps/s, thời gian suy luận) chỉ lấy từ **một máy cố định**, không chạy tác vụ nặng khác cùng lúc.
- Cùng một bảng so sánh phải từ cùng một máy.

## Môi trường dựng bộ mã (16–17/10/2026, tham chiếu)
Python 3.13, NumPy 2.5.3, không có Gymnasium/PyTorch (lớp tương thích `_compat.py`). Tham chiếu heuristic sinh ra trên môi trường này.