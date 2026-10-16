# Ghi chú cho LDN (Dương Ngọc Linh Đan)

> Viết ngày 17/10/2026. Đọc kèm `docs/05_ke_hoach.md` (kế hoạch hiện hành) và `Project Agreement.md`.

Chào LDN! Vai trò của bạn tương ứng với phần bạn làm ở RIVF-Paper: **ma trận thực nghiệm, thống kê và gate report**. Bạn là người quyết định một con số có đủ bằng chứng để vào bài hay chưa.

## Bạn sở hữu
| File / việc | Ghi chú |
| --- | --- |
| `scripts/analyze.py`, `src/uavaoi/stats.py` | Bootstrap CI, IQM, kiểm định hoán vị, Cliff's δ, Holm. Tuần 2 mở rộng thêm bảng độ suy giảm theo seed và hình F4 |
| Báo cáo gate G1 (`notes/2026-11-15_gate_G1_report.md`) | Form G, nộp trước 14/11; tiêu chí ở `docs/05` §5 |
| `results/analysis/claim_evidence.md` | Cập nhật trạng thái từng claim; không có dòng *independently checked* thì không vào bài |
| EXP-03 card (khẳng định, 10 seed) và EXP-05 (quét λ) | Viết card trước khi chạy |
| Hình F3, F4, F5 | Sinh từ `results/raw/` bằng script, không chỉnh tay |
| Tổng quan hệ thống (truy vấn Q1–Q3) | Ghi số kết quả mỗi truy vấn để làm sơ đồ PRISMA rút gọn |

## Ba ngày đầu
1. **19/10:** họp khởi động; đọc `notes/workbook_forms.md` (quy ước tên file).
2. **20/10:** đọc Agarwal et al. 2021 ("Deep RL at the Edge of the Statistical Precipice"), cơ sở của quy tắc thống kê. Đọc Yi et al. 2020. Viết Form B cho mỗi bài vào `notes/reading/`.
3. **21/10:** chạy smoke test trên máy bạn (máy thứ 2 cho EXP-01, cần ≥ 2 máy để qua G1).

## Lưu ý
- Đơn vị lặp là **seed huấn luyện**, không phải episode. 100 episode của cùng một seed không phải 100 lần lặp độc lập.
- EXP-02 (pilot) chỉ có 2 seed: chỉ mô tả, không đưa p-value vào bài.
- Ngưỡng ý nghĩa thực tiễn cho H1 phải chốt trong `docs/PREREG.md` **trước** EXP-03.
- Second reader của bạn: FAO (EXP-03), DAT (EXP-05).
