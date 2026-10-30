# Báo cáo gate G0 — định vị đóng góp (Form G)

> **Trạng thái: NHÁP** do Claude soạn cho DAT ngày 30/10/2026. Owner: DAT. Second reader: LDN (W2-LDN-03). Gate dời từ 01/11 sang **T4 04/11/2026** (DECISIONS 2026-10-30). Đây là lần kéo dài duy nhất được phép.
> Mọi nhận định dưới đây đều có nguồn (mục/PT/bảng của Form B, hoặc commit). Báo cáo không đưa thêm số liệu thực nghiệm nào ngoài các số đã có trong repo.

```text
Ngày và gate: G0 — định vị đóng góp. Họp gate T4 04/11/2026 (gốc CN 01/11).

Bằng chứng xem xét, kể cả lần chạy thất bại (run ID):
  - Ma trận định vị docs/04 §5 tại commit f6a3d57: 9 công trình.
  - Form B toàn văn (6): bayerlein2021multi_DAT, zeng2019energy_DAT, lamenza2025_DAT,
    abdelmagid2019deep_FAO, sun2025aoi_FAO, liu2024generalizable_FAO.
    Form B chỉ có tóm tắt (1): ohdrl2025_FAO.
    Chưa có Form B (2): Yi 2020, Sarathchandra 2025.
  - Câu định vị nháp: docs/01 §3.
  - G0 không có thực nghiệm. Không có lần chạy nào là bằng chứng của gate này.

Baseline có chạy đúng không? Bằng chứng:
  Không phải tiêu chí của G0. Tham khảo: EXP-01 (heuristic) tái lập bit-identical trên
  laptop DAT, 0/1500 dòng lệch (run EXP-01/20261025-115153 so với 20261020-084218;
  Form C ở notes/EXP-01_reproduction_card.md; FAO kiểm lại bằng compare_events.py: MATCH).

Hiệu ứng chính có đạt tiêu chí khai báo trước không? Bằng chứng (bảng tiêu chí):
  Xem bảng "Đối chiếu tiêu chí G0" bên dưới.
  Tóm tắt: #1 CHƯA ĐẠT; #2 ĐẠT TẠM (chỉ trong 9 công trình đã có); #3 CHỜ GVHD.

Giải thích thay thế mạnh nhất còn đứng vững:
  "Khoảng trống" trong ma trận có thể chỉ do tìm kiếm chưa đủ, không phải do chưa ai làm.
  Tìm kiếm hệ thống Q1–Q3 (docs/04 §6; W1-LDN-04, W1-LDN-05) chưa có kết quả trên repo,
  nên chưa có số PRISMA. Có ít nhất 3 hàng còn "Chưa rõ" (Yi 2020, Sarathchandra 2025,
  OH-DRL 2025), và cả ba đều có AoI. Vì vậy chưa loại trừ được khả năng một bài đã có
  đủ 5 cột.

Trùng lặp với công trình gần nhất còn chưa giải quyết:
  - Bayerlein 2021 đã tổng quát hoá theo tham số kịch bản và có thử ngoại suy tham số
    (§VI-E, Fig. 7). Đề tài không được viết "đầu tiên tổng quát hoá" (quy tắc 7).
    Khác biệt kiểm chứng được: mục tiêu thu một lần (PT (13)), năng lượng −1/bước với một
    tốc độ (PT (5)), 1 lần huấn luyện mỗi bản đồ (§VI-A), không có đối chứng huấn luyện
    trên kịch bản cố định (§VI-B).
  - Sun 2025 có AoI và mô hình P(v) (PT (4)), nhưng v cố định 5 m/s (§III-A, Bảng IV).
    Đây là bài gần nhất ở cột "năng lượng phụ thuộc tốc độ". Câu định vị phải nói rõ
    tốc độ là biến quyết định của chính sách.
  - OH-DRL 2025 (AoI + năng lượng bay, IEEE TWC): chỉ có tóm tắt, chưa xác định được
    3/5 cột. Đây là rủi ro trùng lặp lớn nhất còn mở.

Nhu cầu tính toán/thời gian còn lại:
  Ước lượng của FAO (notes/2026-10-21_fao_chi-phi-nhap.md §2, §4; Project Agreement §5):
  163,2 M bước (Phương án B, đã gồm Optuna DQN 4 M bước, cập nhật FAO 30/10 tại c9da329).
  Cần 126,5 giờ máy (≈ 5,3 ngày) nếu mọi learner chạy 358,4 bước/s (PPO, CPU, laptop DAT),
  hoặc 173,0 giờ (≈ 7,2 ngày) nếu DQN chậm 3,5 lần. FAO kết luận kịp trước 13/12.
  Tỉ lệ 3,5 lần lấy từ laptop FAO; DQN 100k trên máy DAT chưa đo.

Quyết định: [DAT/GVHD chọn tại họp 04/11 — đề xuất bên dưới]
Lý do:
Phạm vi tuyên bố được duyệt:
Thực nghiệm tiếp theo và owner: EXP-02 pilot (W3, DAT huấn luyện trên laptop DAT); Optuna TUNE (W4, DAT; `tune_ppo.py` đã merge ở PR #30, FAO đã duyệt).
Ngày quyết định tiếp theo: G1 — CN 15/11/2026.
Ý kiến giảng viên:
```

## Đối chiếu tiêu chí G0 (`docs/05` §5)

| # | Tiêu chí | Hiện trạng (30/10) | Bằng chứng | Kết luận |
| --- | --- | --- | --- | --- |
| 1 | Ma trận `docs/04` §5 đủ các công trình gần nhất; mỗi ô có nguồn (mục/bảng) | 6 hàng có nguồn cho mọi ô. Zeng có hàng riêng nhưng là nguồn mô hình, không phải đối thủ. Còn 3 hàng có ô "Chưa rõ" hoặc chưa có nguồn: Yi 2020 (3 ô, 2 ô "Có" chưa có nguồn), Sarathchandra 2025 (1 ô, các ô còn lại chưa có nguồn), OH-DRL 2025 (3 ô; chỉ có tóm tắt). Tìm kiếm Q1–Q3 chưa có kết quả, nên chưa biết "đủ" hay chưa. | `docs/04` §5; `notes/reading/`; status LDN | **Chưa đạt.** Đã dùng hết lần kéo dài 3 ngày. |
| 2 | Không công trình nào đủ cả 5 cột | Trong 9 công trình đã có, không bài nào đủ 5 cột "Có". Gần nhất: Liu 2024 (DR + OOD có cấu trúc, nhưng không AoI, không năng lượng), Bayerlein 2021 (DR + một phần OOD), Sun 2025 (AoI + mô hình P(v) nhưng tốc độ cố định). Cột "Nhiều seed + CI" là "Không" ở mọi bài đã đọc toàn văn. | Các hàng ma trận và Form B tương ứng | **Đạt tạm**, có điều kiện: chỉ trong phạm vi đã đọc. 3 hàng "Chưa rõ" đều có cột AoI = Có. |
| 3 | Câu định vị `docs/01` §3 được GVHD đồng ý | Câu nháp chưa gửi GVHD. Câu hiện tại khớp với dữ kiện Bayerlein (§I-B, §VI-E). Chưa nhắc Sun 2025 (đã có P(v)) và chưa nhắc cột seed/CI. | `docs/01` §3; Form B Bayerlein mục "Một câu hỏi cho nhóm" | **Chờ GVHD.** |

## Việc phải xong trước họp 04/11 để tiêu chí 1 đạt

| Việc | Owner | Phụ thuộc |
| --- | --- | --- |
| Đẩy kết quả tìm kiếm Q1–Q3: số kết quả mỗi truy vấn, số bài sau lọc, danh sách đọc toàn văn | LDN (W1-LDN-04, W1-LDN-05) | Không. **Đang trễ 7–8 ngày, chặn W2-DAT-01 và W2-LDN-01** |
| Form B Yi 2020 (arXiv 2003.00391) | LDN (W1-LDN-02). Claude có thể soạn nháp nếu có PDF | PDF; mạng của Claude chặn arXiv |
| Form B Sarathchandra 2025 (arXiv 2501.14603) | LDN (W2-LDN-01). Claude có thể soạn nháp nếu có PDF | PDF |
| OH-DRL 2025: thử lấy toàn văn qua thư viện trường hoặc GVHD; nếu không được thì giữ "chỉ tóm tắt" và ghi rủi ro | DAT | Quyền IEEE Xplore |
| Đọc toàn văn các bài mới từ Q1–Q3 (chia đôi DAT/LDN) | DAT (W2-DAT-01), LDN (W2-LDN-01) | Danh sách Q1–Q3 |
| Câu định vị bản 2, gửi GVHD | DAT | Ma trận đủ |

## Đề xuất quyết định (để DAT và GVHD cân nhắc)

- **Nếu trước 04/11 có danh sách Q1–Q3 và 3 hàng "Chưa rõ" được điền, mà vẫn không bài nào đủ 5 cột:** *tiếp tục*. Phạm vi tuyên bố giữ C1–C3 như `docs/01` §6. Câu định vị bản 2 thêm hai ý kiểm chứng được:
  1. tốc độ là biến quyết định của chính sách (khác Sun 2025, nơi v cố định);
  2. có đối chứng huấn luyện trên kịch bản cố định và nhiều seed kèm CI, là điều Bayerlein 2021 và Lamenza 2026 không có (§VI-A, §VI-B; §5).
- **Nếu đến 04/11 vẫn chưa có kết quả tìm kiếm:** *tiếp tục có điều kiện*. EXP-02 (W3) không phụ thuộc định vị nên vẫn chạy. Nhưng mọi câu khẳng định "khoảng trống" bị khoá cho tới khi tìm kiếm xong, và phải xong trước G1 (15/11). Phải ghi vào DECISIONS, vì G0 không được kéo dài lần hai.
- **Nếu một bài đủ 5 cột:** áp dụng nhánh "không đạt" của tiêu chí 2. Đổi trọng tâm sang A5 (vai trò lựa chọn tốc độ) hoặc đa UAV; GVHD quyết.

## Cần nói rõ trong buổi họp

- Ma trận và kết luận #2 là **dữ kiện từ các bài đã đọc**, không phải kết luận về toàn bộ tài liệu, cho tới khi có số PRISMA.
- Hàng Yi 2020 hiện ghi "Có" ở cột AoI và năng lượng nhưng **chưa có nguồn**. Hai ô này không được dùng cho tới khi có Form B.
- Khoá `lamenza2025` giữ nguyên dù bài xuất bản 2026 (tập 8); trường `year` đã đúng (DECISIONS 2026-10-30).
