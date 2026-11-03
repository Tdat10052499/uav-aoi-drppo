# DAT → LDN: nhắm FJCAI 2027 (hạn 15/11), lịch nén — 03/11/2026

> Trả lời bằng dòng `LDN:` dưới mỗi mục. Quy ước: `notes/yeu-cau/README.md` (PR #28). Lịch đầy đủ và lý do: `docs/DECISIONS.md` (các dòng 03/11).

## A1. Đánh giá pilot EXP-02 ngày 04/11 (W3-LDN-01, kéo sớm)
- **Cần:** đánh giá 4 model pilot (s0-DR, s0-Fixed, s1-DR, s1-Fixed) trên 5 bộ × 100 episode bằng `scripts/evaluate.py`. Run ID ghi trong `notes/EXP-02_pilot_card.md`.
- **Để làm gì:** "G1 sớm" ngày 05/11 kiểm tiêu chí #2: DR-PPO trên `id` có ≤ 63,1 khe ở cả 2 seed không. Nếu không đạt, nhóm bỏ FJCAI.
- **Hạn:** tối 04/11.

## A2. Đánh giá EXP-03 dần trong 06–08/11
- **Cần:** đánh giá từng model EXP-03 ngay khi có `run_record.json` (2 nhánh × 10 seed).
- **Hạn:** xong tất cả trước sáng 09/11.

## A3. `analyze.py` và Results (09–10/11)
- **Cần:** chạy `analyze.py` để ra deg theo seed, CI bootstrap, IQM, kiểm định hoán vị một phía + Holm cho H1 (4 bộ OOD), H2 (TSP trên `ood_cluster`), và Cliff's δ. Vẽ hình F3, F4 (bản rút gọn). Sau đó viết mục **Experimental Setup** (06–08/11) và **Results** (10/11).
- **Hạn:** bảng chính 09/11; Results 10/11.

## A4. Ngưỡng ý nghĩa thực tiễn cho H1 (ô PREREG của LDN)
- **Cần:** chốt ngưỡng trước khi khoá PREREG ngày **05/11**, thay vì 13/11 như trước.

LDN: (03/11) Đã chốt δ = 0,10 (hiệu tuyệt đối của trung bình deg, áp trên các bộ có ý nghĩa sau Holm). Chi tiết và đoạn đề xuất cho §8 PREREG ở B2 của `2026-11-03_dat_can-FAO_khoa-PREREG-som.md`. LDN theo hạn 04/11 trước 12:00 của file đó, vì file đó thay hạn 05/11 ở đây.
