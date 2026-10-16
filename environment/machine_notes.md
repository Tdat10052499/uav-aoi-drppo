# Machine Notes

Owner: **FAO**. Điền sau lần chạy thành công đầu tiên trên mỗi máy (EXP-01).

```bash
python --version
python -c "import numpy, torch; print(numpy.__version__, torch.__version__, torch.cuda.is_available())"
python -c "import platform; print(platform.platform(), platform.machine())"
```

| Máy | Chủ | CPU / RAM | GPU | OS | Python | NumPy | torch | Dùng cho |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| <máy cố định đo thời gian> | DAT | | | | | | | **Mọi số đo thời gian** + huấn luyện |
| <máy FAO> | FAO | | | | | | | Tái lập, huấn luyện |
| <máy LDN> | LDN | | | | | | | Phân tích, huấn luyện thêm seed |
| Kaggle T4 (nếu dùng) | FAO | — | T4 ×1 | Linux | | | | Chỉ chạy thêm seed; **không** lấy số thời gian |

## Quy tắc đo
- Số thời gian (steps/s, thời gian suy luận) chỉ lấy từ **một máy cố định**, không chạy tác vụ nặng khác cùng lúc.
- Cùng một bảng so sánh phải từ cùng một máy.

## Môi trường dựng bộ mã (16–17/10/2026, tham chiếu)
Python 3.13, NumPy 2.5.3, không có Gymnasium/PyTorch (lớp tương thích `_compat.py`). Tham chiếu heuristic sinh ra trên môi trường này.
