# DAT → FAO: nhắm FJCAI 2027 (hạn 15/11), lịch nén — 03/11/2026

> Trả lời bằng dòng `FAO:` dưới mỗi mục. Quy ước: `notes/yeu-cau/README.md` (PR #28). Lịch đầy đủ và lý do: `docs/DECISIONS.md` (các dòng 03/11).

## A1. Trả lời 5 ô PREREG (`notes/yeu-cau/2026-11-03_fao_can-DAT_prereg-cho.md`)
- **DAT:**
  - A1 = 2M bước, 10 seed mỗi nhánh.
  - A2: dùng lại seed (không áp dụng cho bài FJCAI vì không có EXP-05).
  - A3: chỉ mô tả.
  - A4: đồng ý peak AoI là chỉ số mô tả.
  - A5: đồng ý 4 tiêu chí, thêm "liệt kê mọi lần chạy bị loại".
  - Chi tiết lý do: các dòng `DAT:` trong file yêu cầu của FAO (đã ghi 03/11).
- **Cần FAO:** chép sang `docs/PREREG.md` và khoá cùng DAT ngày **05/11** (sớm hơn W4-FAO-01), kèm siêu tham số mặc định (DECISIONS 03/11).

FAO: (03/11) Đã chép vào `docs/PREREG.md`, PR #38 (DAT và LDN là reviewer). Còn trống ngưỡng H1 (§8) chờ LDN. Thay hạn khoá 05/11 bằng 04/11 theo yêu cầu khoá sớm.

## A2. Second reader quỹ đạo pilot (W3-FAO-01, kéo sớm sang 04/11)
- **Cần:** xem ≥ 3 quỹ đạo mỗi model pilot. Kiểm tiêu chí G1 #5: chạm biên = 0 khi có mask; không hành động nào chiếm ≥ 90%.
- **Hạn:** 04/11, để "G1 sớm" ngày 05/11 có đủ bằng chứng.

FAO: (03/11) Nhận. `runs/` bị gitignore, nên FAO cần **model.zip của 4 model pilot** để vẽ quỹ đạo trên laptop FAO: DAT gửi qua Drive hoặc cách khác, kèm run ID. FAO cũng cần `results/raw/EXP-02/` đã push lên `main`. Khi có, FAO vẽ ≥ 3 quỹ đạo mỗi model (`plot_trajectory.py`), chạy `check_degenerate.py` và ghi vào `notes/review_log.md` trong ngày. Một cách khác: DAT tự chạy `plot_trajectory.py` rồi push PNG, FAO xem và ghi nhận. Cách này nhanh hơn nhưng FAO không kiểm được SHA256 của model.

## A3. Related Work cho bài FJCAI (06–08/11)
- **Cần:** viết mục Related Work (≤ 1 trang IEEE) từ ma trận `docs/04` §5. Nhóm A đã thêm Gong 2024, Lu 2025, Toure 2026. Dùng câu định vị bản 3 ở `docs/01` §3.
- Nháp `notes/2026-10-22_fao_related-work-limitations-nhap.tex` của FAO có thể dùng làm điểm xuất phát.
- **Hạn:** 08/11.

FAO: (03/11) Nhận, hạn 08/11, từ nháp `notes/2026-10-22_fao_related-work-limitations-nhap.tex`. Hai điểm chưa có trên `main` (03/11): (1) ma trận `docs/04` §5 chưa có hàng Gong 2024, Lu 2025, Toure 2026; (2) `docs/01` §3 mới có câu định vị bản 2, chưa có bản 3. FAO cập nhật phần đã có trước (Yi 2020, Yi 2023, Sarathchandra, Xiao, Eldeeb), để chỗ cho 3 bài còn lại.

## A4. Phản biện nội bộ toàn bài ngày 12/11
- **Cần:** đọc toàn bài, kiểm định dạng IEEE ≤ 8 trang, và kiểm mọi số liệu có nguồn.

FAO: (03/11) Nhận phản biện nội bộ ngày 12/11: kiểm định dạng IEEE ≤ 8 trang và nguồn của mọi số liệu (đối chiếu `results/analysis/claim_evidence.md`).

FAO: (06/11) DECISIONS 06/11 (PR #42) bỏ FJCAI, nên A3 (Related Work hạn 08/11) và A4 (phản biện 12/11) dừng. Bản Related Work 03/11 giữ trong `notes/2026-10-22_fao_related-work-limitations-nhap.tex` cho hội nghị sau.
