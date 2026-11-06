# DAT → FAO, LDN: đổi phương pháp sang PG-TG-PPO, nhiệm vụ mới W3–W8 — 06/11/2026

> Trả lời bằng dòng `FAO:` hoặc `LDN:` dưới mỗi mục. Claude soạn theo yêu cầu của DAT ngày 06/11.
> - **Lịch mới:** PR `DAT/phuong-phap-moi` (LDN review). Sau khi merge, `python scripts/today.py` sẽ hiện đúng việc mới. Trước khi merge, xem `schedule/SCHEDULE.md` trên nhánh đó.
> - **Lý do:** `docs/DECISIONS.md` (ba dòng 06/11 trên nhánh đó).
> - **Nháp cần đọc trước:**
>   - `notes/2026-11-06_dat_thiet-ke_PG-TG-PPO.md`: thiết kế;
>   - `notes/EXP-08_PG-TG-PPO_card.md`: card EXP-08a, 08p, 08;
>   - `notes/2026-11-06_dat_PREREG-phu-luc-B_nhap.md`: H5–H7.
>
>   Cả ba là **nháp, chưa ai duyệt**. Quy tắc 1: không chạy phần nào trước khi card được duyệt.
> - **Câu P1–P6 của FAO** đã có dòng `DAT:` trong `notes/yeu-cau/2026-11-06_fao_can-DAT_prereg-phu-luc.md`. Ô P4 còn chờ `LDN:`.

## 0. Tóm tắt phương pháp mới (một đoạn)

EXP-03 không đạt H1, H2. Theo chẩn đoán từ mã (giả thuyết, chưa kiểm), lý do có thể là:
- quan sát chuẩn hoá pin theo E_max và lưới theo L, nên policy không thấy ngân sách thật;
- TRAIN_DR không đổi L;
- PPO phẳng phải tự học tìm đường từng ô.

PG-TG-PPO gồm hai thành phần:
- **A, quan sát neo vật lý:** ô 62,5 m cố định; kênh pin ρ_E = số khe còn bay được ở V_me chia số khe còn lại; kênh thời gian.
- **B, PPO tầng cao trên tour TSP:** chọn một trong K = 5 ứng viên × 2 tốc độ, hoặc "chờ". Tầng thấp bay tất định.

Baseline mạnh hơn: TSP-eco, TSP-adaptive, tầng cao greedy. Thực nghiệm khẳng định EXP-08:
- 4 nhánh M1–M4 × seed 10–19;
- đánh giá trên bộ mới seed 300000–300099, khoá tại G1 (T6 20/11).

Bài phải trích Gao et al. 2026 (arXiv 2611.03884) và không nhận "phân tầng" là điểm mới.

## 1. Nhiệm vụ của FAO

| Task | Ngày | Việc | Second reader |
| --- | --- | --- | --- |
| W3-FAO-01 | đến 08/11 | Giữ nguyên (manifest EXP-02 + quỹ đạo) | — |
| W4-FAO-03 | 09–12/11 | PR `fao/grounded-obs`: `obs_mode` legacy/grounded, mặc định legacy, kiểm thử | DAT |
| W4-FAO-04 | 12–14/11 | PR `fao/tsp-manh`: TSP-eco, TSP-adaptive trong `baselines.py`; bộ id2, ood_energy_low, ood_area_2000, ood_combo (seed 300000–300099) + manifest; kiểm T = 300 cho L = 2000 m | LDN |
| W5-FAO-03 | 16–19/11 | Đưa PREREG phụ lục B vào `docs/PREREG.md` (PR mở đến G1) | LDN |
| W5-FAO-04 | 16–19/11 | Second reader EXP-03: chạy lại đánh giá 2 model, so `events.csv` | — |
| W6-FAO-03 | 21/11–02/12 | EXP-08: M3, M4 seed 10–19 (máy FAO hoặc Kaggle) | DAT |
| W7-FAO-02 | 01–06/12 | Second reader EXP-08: provenance, `check_degenerate.py`, chạy lại 2 model | — |
| W8-FAO-03 | 07–11/12 | Hình F6 (TSP-adaptive và M1) + bảng hành vi | LDN |

- **Cần FAO xác nhận:**
  - Có kịp hai PR mã trong W4 không? Nếu không, đề xuất đổi TSP-adaptive sang DAT.
  - Máy FAO hoặc Kaggle có chạy được M3, M4 (20 run) không? Quan sát Dict của M3/M4 nhỏ, không dùng buffer lớn như DQN.
- FAO: (06/11) Đã đọc cả ba nháp ở góc môi trường: `notes/2026-11-06_fao_review_PG-TG-PPO.md`, 7 mục. Mục 1 (kênh thời gian đã có sẵn) và mục 2 (đơn vị ρ_E) nên sửa trước khi duyệt card. T = 300 đủ cho L = 2000 m (mục 5), nên có thể bỏ ✱. Nhận lịch W3–W8.
  - Hai PR mã trong W4: kịp. FAO làm W4-FAO-03 (`obs_mode`) trước, rồi W4-FAO-04. Tham số ép tốc độ của `_move_towards` sẽ có sớm để DAT dùng cho `options.py`.
  - Máy cho M3, M4 (W6-FAO-03): **Kaggle** (FAO chọn 06/11). Điều kiện provenance:
    - notebook clone repo đúng tag khoá phụ lục B và chạy qua `train_ppo.py`, để `run_record.json` ghi commit, cấu hình, seed và SHA256 checkpoint;
    - tải về cả `runs/EXP-08/<run>/` và `results/raw/EXP-08/<run>/`;
    - FAO kiểm `code_revision` và digest trước khi push.

    Giới hạn thời gian mỗi phiên và số CPU của Kaggle chưa kiểm (✱); FAO kiểm trước W6. Một run 2M bước phải xong trong một phiên, vì `train_ppo.py` chưa có resume. Nếu không kịp thì báo DAT ngay. Lưu ý: số thời gian chỉ lấy từ máy DAT (quy tắc 4); run trên máy FAO chỉ cho kết quả, không cho số đo thời gian.

## 2. Nhiệm vụ của LDN

| Task | Ngày | Việc | Second reader |
| --- | --- | --- | --- |
| W4-LDN-03 | 10–12/11 | EXP-08a: chẩn đoán từ raw EXP-03 (hết pin sớm hay đi sai đường?), chỉ mô tả | FAO |
| W4-LDN-04 | 09–13/11 | Hoàn tất PR #43, báo cáo chính thức H1/H2 của EXP-03; power analysis cho δ₅–δ₇ (n = 10); đề xuất cách kiểm H5 và mốc "tệ nhất" của S (Random hay 151,5) | DAT |
| W5-LDN-03 | 18–19/11 | Báo cáo G1 mới (6 điều kiện, `docs/05` §5) | FAO |
| W5-LDN-02 | 21–27/11 | Experimental Setup (theo PREREG phụ lục B) | DAT |
| W6-LDN-03 | 23–29/11 | PR `analyze.py` cho H5–H7 (hoán vị, Holm, bootstrap CI, IQM, Cliff's δ, S) | FAO |
| W7-LDN-03 | 30/11–06/12 | Mô tả tạm EXP-08 + phân tích thăm dò | DAT |
| W8-LDN-01, W8-LDN-03 | 07–13/12 | Hình F3–F5, claim–evidence (giữ, đổi phụ thuộc) | DAT, FAO |

- **Cần LDN:**
  - Review PR `DAT/phuong-phap-moi` (lịch).
  - Ký second reader card EXP-08 cùng DAT trước 09/11, để EXP-08a chạy được từ 10/11.
  - Chốt cách gộp 2 seed cho tiêu chí pilot (`docs/05` §5 G1 #3) trước khi pilot chạy.
- LDN:

## 3. Nhiệm vụ của DAT (để hai bạn biết đang chờ gì)

| Task | Ngày | Việc |
| --- | --- | --- |
| W3-DAT-03 | 06–07/11 | Push raw EXP-03 và log tb; merge PR #41, #42; đóng PR #34 |
| W3-DAT-04 | 07–08/11 | Nhắn GVHD (kết quả, hướng mới, δ, tên đề tài, hạn đăng ký) |
| W3-DAT-05 | 07–09/11 | Chốt thiết kế và card EXP-08 (LDN ký) |
| W4-DAT-02 | 09–11/11 | Kiểm lại Bayerlein 2021 (pin trong quan sát?) + Form B Theile ~2020 |
| W4-DAT-03 | 09–14/11 | PR `dat/tour-guided`: `src/uavaoi/options.py`, tầng cao greedy, `train_ppo.py --policy options` (FAO review) |
| W5-DAT-03 | 16–18/11 | Pilot EXP-08p (M1, M4; seed 0–1), đo bước/s |
| W6-DAT-03 | 21/11–02/12 | EXP-08: M1, M2 seed 10–19 |
| W7-DAT-02 | 01–06/12 | Đánh giá 40 model + baseline, push raw |
| W8-DAT-03 | 07–09/12 | Second reader phân tích EXP-08 |

**Thứ tự phụ thuộc chính:**
1. Raw EXP-03 (W3-DAT-03) và card đã ký (W3-DAT-05) → EXP-08a.
2. Ba PR mã (W4-DAT-03, W4-FAO-03, W4-FAO-04) và EXP-08a → pilot.
3. Pilot → báo cáo G1 → G1 (20/11) → EXP-08.

## 4. Việc dọn trạng thái (mỗi người tự làm trên file của mình)

Các task cũ đã bỏ khỏi lịch không cần đánh dấu. Một số task cũ vẫn còn trong lịch và đang hiện "TRỄ". Ai làm gì thì tự đánh dấu bằng `today.py`: `--done <ID> --evidence "..."` nếu đã làm, hoặc `--skip <ID>` nếu không còn cần.
- **FAO:** W3-FAO-01.
- **LDN:** W2-LDN-02, W2-LDN-03, W3-LDN-01.
- **DAT:** W1-DAT-07, W1-DAT-08, W2-DAT-01, W2-DAT-03, W3-DAT-01, W3-DAT-02.

## 5. Cập nhật 06/11 chiều: mã pilot đã có ở PR #45

DAT chọn để Claude viết luôn ba phần mã của W4 (W4-FAO-03, W4-FAO-04, W4-DAT-03) trong **PR #45** (`DAT/pilot-pg-tg-ppo`), nhằm kéo pilot sớm lên khoảng 10–11/11.
- **FAO:** không cần viết `fao/grounded-obs` và `fao/tsp-manh` nữa. Thay vào đó, review PR #45 với vai trò second reader mã.
- **LDN:** đọc mục "Cài đặt trong mã" ở cuối `notes/EXP-08_PG-TG-PPO_card.md`, nhất là mục 6 (đặc trưng ứng viên của M3), rồi ký card cùng DAT.
- Lệnh pilot nằm ở cuối card. Chỉ chạy sau khi card được ký và PR #45 đã merge.
- FAO:
- LDN:
