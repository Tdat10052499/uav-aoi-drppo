# PREREG phụ lục B: EXP-08 (PG-TG-PPO)

> **Nháp, chưa khoá.** Claude soạn ngày 06/11/2026.
> - **Quy trình khoá:** LDN là second reader, FAO kiểm cấu hình. DAT merge PR khoá rồi gắn tag `prereg-B-lock`.
> - **Sau khi khoá:** không đổi giả thuyết, ngưỡng hay bộ đánh giá. Mọi thay đổi ghi vào `docs/DECISIONS.md`.
> - **Quan hệ với EXP-03:** phụ lục này **không** thay PREREG gốc. EXP-03 vẫn được báo cáo đúng như đã đăng ký: H1 và H2 không đạt.

## 1. Nguồn gốc giả thuyết (khai báo minh bạch)

H5–H7 được hình thành **sau khi** đã xem kết quả EXP-03 và đọc lại mã môi trường. Chi tiết ở `notes/2026-11-06_dat_EXP-03-so-bo.md` (PR #42) và báo cáo rà soát tài liệu 2023–2026 (Claude Doc của DAT, chưa đưa vào repo; DAT gửi link khi cần).

Để kiểm tra đúng nghĩa khẳng định, phụ lục này dùng ba điều kiện mới:
- seed huấn luyện mới 10–19;
- bộ đánh giá mới, chưa ai chạy, với seed 300000–300099 (khác bộ kiểm định Optuna 200000–200019; câu P3 trong `notes/yeu-cau/2026-11-06_fao_can-DAT_prereg-phu-luc.md`);
- ngưỡng chốt trước khi chạy.

Bài báo phải ghi rõ nguồn gốc này.

**Những gì đã chạy trên phân phối bộ mới trước khi khoá** (khai báo, cập nhật đến lúc khoá):
- FAO, 06/11: phép thử độ khả thi T = 300 bằng heuristic, seed 900000–900029, mã ngoài `evaluate.py` (`notes/2026-11-06_fao_review_PG-TG-PPO.md` §5). Không learner nào được chạy.
- Mọi lần `evaluate.py --probe-b`: liệt kê run ID tại đây (run record có cảnh báo `--probe-b`).

## 2. Cấu hình

- Commit: commit merge của PR khoá.
- Môi trường: `configs/env_default.json` cộng `obs_mode` (SHA256 điền khi khoá).
- Siêu tham số: điền sau pilot EXP-08p, áp dụng chung cho mọi nhánh PPO.
- Bước huấn luyện: điền sau pilot.
- Không chỉnh thêm sau khi khoá.

## 3. Bộ đánh giá

Bộ chính:

| Bộ | Thông số | Seed |
|---|---|---|
| id2 | TRAIN_DR | 300000–300099 |
| ood_energy_low | E_max ~ U[0,35; 0,45] MJ, còn lại như TRAIN_DR | 300000–300099 |
| ood_area_2000 | L = 2000 m ✱ (kiểm T = 300 có đủ thu hết không; nếu không thì ghi rõ) | 300000–300099 |
| ood_combo | 2–4 cụm (σ = 80 m) + E_max ~ U[0,5; 0,7] MJ | 300000–300099 |

Bộ phụ: 5 bộ của PREREG gốc, seed 100000–100099, chỉ dùng để mô tả.

## 4. Giả thuyết (khẳng định)

Cả ba giả thuyết dùng chung các điều kiện sau:
- đơn vị lặp là seed huấn luyện, n = 10 mỗi nhánh;
- kiểm định hoán vị một phía, 20 000 hoán vị;
- α = 0,05;
- hiệu chỉnh Holm trong từng họ.

**H5 (thắng heuristic mạnh khi ngân sách đổi).** Ā(M1) < Ā(TSP-adaptive) trên ood_energy_low và ood_combo.
- Họ Holm gồm 2 bộ.
- Đạt khi p_Holm < 0,05 **và** mức giảm tương đối ≥ δ₅ trên cả 2 bộ.
- Mức giảm tương đối = (Ā_TSPa − Ā_M1)/Ā_TSPa.
- TSP-adaptive là heuristic tất định, nên được so với phân phối 10 giá trị seed của M1 (✱ LDN chốt cách kiểm).

**H6 (không kém trên id).** Ā(M1, id2) ≤ (1 + δ₆) · Ā(TSP-adaptive, id2).
- Kiểm không thua (non-inferiority): cận trên của CI 95% bootstrap phải nằm dưới ngưỡng.

**H7 (vai trò của quan sát neo).** S(M1) − S(M3) ≥ δ₇ và p_Holm < 0,05 trên ood_energy_low và ood_area_2000.
- S = (Ā_ref − Ā)/(Ā_ref − Ā_TSP-adaptive), lựa chọn (c) của câu P4. Mốc "tệ nhất" Ā_ref là Random hoặc trần 151,5 khe khi không thu (FAO tính từ `env.py`); ✱ LDN chốt trước khi khoá.
- Họ Holm gồm 2 bộ.

**Thăm dò, không kiểm định:**
- M1 so với M2 (tác dụng DR);
- M1 so với M4 (tác dụng tầng tour);
- M1 so với tầng cao greedy;
- bộ phụ cũ.

## 5. Ngưỡng (nhóm chốt, có lý do độc lập với dữ liệu)

| Ngưỡng | Đề xuất của Claude | Lý do cần nhóm xác nhận |
|---|---|---|
| δ₅ | 0,10 | Giảm 10% AoI so với heuristic là mức thường được xem là có ý nghĩa vận hành ✱. Nhóm xác nhận trước khi khoá (DECISIONS 06/11: GVHD duyệt ở bản thảo). |
| δ₆ | 0,10 | Cho phép thua TSP tối đa 10% trên phân phối huấn luyện. |
| δ₇ | 0,10 | Thu hẹp thêm 10% khoảng Random→TSP. |

Các ngưỡng phải được biện minh bằng ý nghĩa thực tế, ví dụ số giây AoI. **Không** được chọn theo số EXP-03. LDN chạy power analysis bằng độ lệch chuẩn theo seed của EXP-03: nếu power < 0,8 thì tăng số seed trước khi khoá.

## 6. Kết quả và hành động (ghi trước)

| Kết quả | Câu chuyện của bài |
|---|---|
| H5, H6, H7 đều đạt | Phương pháp thắng heuristic mạnh khi pin thay đổi, không kém trên id; quan sát neo là nguyên nhân (trong mô phỏng) |
| H5, H6 đạt; H7 không | Thắng heuristic; vai trò của quan sát neo chưa được chứng minh, nên chỉ báo cáo dưới dạng thăm dò |
| H7 đạt; H5 không | Đóng góp về cơ chế: làm lộ ngữ cảnh giúp zero-shot; chưa thắng TSP-adaptive |
| Không giả thuyết nào đạt | Kết quả âm có kiểm soát lần hai; báo cáo đầy đủ; nhóm xem lại hướng |

## 7. Tiêu chí loại một lần chạy

Như PREREG gốc §9. Run hỏng thì chạy lại với seed + 100 và ghi DECISIONS.
