# Báo cáo gate G0 — định vị đóng góp (Form G)

> **Trạng thái: NHÁP** do Claude soạn cho DAT ngày 30/10/2026, cập nhật 01/11 theo kết quả Q1–Q3 của LDN, và 02/11 theo phản biện của LDN (`notes/review_log.md` G0-1 … G0-6). Owner: DAT. Second reader: LDN (W2-LDN-03). Gate dời từ 01/11 sang **T4 04/11/2026** (DECISIONS 2026-10-30). Đây là lần kéo dài duy nhất được phép.
> Mọi nhận định dưới đây đều có nguồn (mục/PT/bảng của Form B, hoặc commit). Báo cáo không đưa thêm số liệu thực nghiệm nào ngoài các số đã có trong repo.

```text
Ngày và gate: G0 — định vị đóng góp. Họp gate T4 04/11/2026 (gốc CN 01/11).

Bằng chứng xem xét, kể cả lần chạy thất bại (run ID):
  - Tìm kiếm Q1–Q3 (notes/reading/search_log_LDN.md, nháp chờ LDN duyệt): arXiv 17 +
    OpenAlex 23 + Scholar 300 bản ghi; 279 bản ghi duy nhất (PRISMA đã chốt, search_log §4);
    giữ 57 bài đọc toàn văn (nhóm A 9, B 12, C 36); thêm 5 bài từ tra ngược Yi 2023. IEEE Xplore và Scopus thay bằng
    OpenAlex (DECISIONS 2026-11-01).
  - Ma trận định vị docs/04 §5: thêm Yi 2020, Sarathchandra 2025, Yi 2023, Xiao 2024,
    Eldeeb 2026 (LDN, 31/10). Thêm cột 6 "đối chứng huấn luyện cố định" (DECISIONS 01/11).
  - Form B toàn văn đã duyệt: bayerlein2021multi_DAT, zeng2019energy_DAT, lamenza2025_DAT
    (LDN second reader 01/11); abdelmagid2019deep_FAO, sun2025aoi_FAO, liu2024generalizable_FAO.
    Form B nháp (LDN, chờ duyệt): yi2020deep, sarathchandra2025age, yi2023meta, eldeeb2026,
    xiao2024meta (đọc qua bản trích tự động, phải đối chiếu PDF).
    Form B chỉ có tóm tắt (1): ohdrl2025_FAO.
    Nhóm A phần DAT chưa đọc (5): Gong 2024, Lu 2025, Toure 2026 (arXiv); Chen–Hanzo 2024,
    Zhou 2024 (chỉ có trên IEEE).
  - Câu định vị nháp: docs/01 §3.
  - G0 không có thực nghiệm. Không có lần chạy nào là bằng chứng của gate này.

Baseline có chạy đúng không? Bằng chứng:
  Không phải tiêu chí của G0. Tham khảo: EXP-01 (heuristic) tái lập bit-identical trên
  laptop DAT, 0/1500 dòng lệch (run EXP-01/20261025-115153 so với 20261020-084218;
  Form C ở notes/EXP-01_reproduction_card.md; FAO kiểm lại bằng compare_events.py: MATCH).

Hiệu ứng chính có đạt tiêu chí khai báo trước không? Bằng chứng (bảng tiêu chí):
  Xem bảng "Đối chiếu tiêu chí G0" bên dưới.
  Tóm tắt (02/11): #1 CHƯA ĐẠT; #2 CHƯA KẾT LUẬN ĐƯỢC (14 bài trong ma trận chưa bài nào đủ 6 cột,
  nhưng Gong 2024 chưa đọc); #3 CHỜ GVHD.

Giải thích thay thế mạnh nhất còn đứng vững:
  Tìm kiếm đã chạy (01/11), nên "khoảng trống" không còn chỉ dựa trên 9 bài. Nhưng:
  (1) Yi 2023 đã có AoI + năng lượng phụ thuộc tốc độ với tốc độ là hành động + huấn luyện
  nhiều bố trí (Có, Có, Có, Một phần, Không); điểm mới về mô hình không còn. (2) 5 bài nhóm
  A phần DAT chưa đọc, trong đó Gong 2024 (AoI + năng lượng, tối ưu vận tốc, đánh giá trên
  môi trường chưa thấy, theo tóm tắt) có thể đủ nhiều cột. (3) OpenAlex có thể sót bài IEEE
  thiếu tóm tắt trong chỉ mục (chưa kiểm). (4) Q1–Q3 không có từ khoá tốc độ (speed, velocity)
  hay chuyển giao (transfer); tra ngược từ Yi 2023 đã ra 5 bài Q1–Q3 bỏ sót, ví dụ Chu 2022
  (điều khiển tốc độ + DRL chuyển giao). Đề xuất truy vấn bổ sung Q4 trước G1 (G0-5).
  Vì vậy chưa loại trừ được khả năng một bài đủ 6 cột.

Trùng lặp với công trình gần nhất còn chưa giải quyết:
  - Bayerlein 2021 đã tổng quát hoá theo tham số kịch bản và có thử ngoại suy tham số
    (§VI-E, Fig. 7). Đề tài không được viết "đầu tiên tổng quát hoá" (quy tắc 7).
    Khác biệt kiểm chứng được: mục tiêu thu một lần (PT (13)), năng lượng −1/bước với một
    tốc độ (PT (5)), 1 lần huấn luyện mỗi bản đồ (§VI-A), không có đối chứng huấn luyện
    trên kịch bản cố định (§VI-B).
  - Sun 2025 có AoI và mô hình P(v) (PT (4)), nhưng v cố định 5 m/s (§III-A, Bảng IV).
    Cùng với Yi 2023 (tốc độ là hành động), cột "năng lượng phụ thuộc tốc độ" không còn là
    điểm khác biệt của đề tài (G0-1).
  - Yi 2023 (arXiv 2311.06742, Form B nháp LDN): trùng ở mô hình (AoI + năng lượng đẩy theo
    tốc độ và gia tốc, PT (9)–(10); tốc độ là hành động, §IV-A2; MAML trên nhiều nhiệm vụ,
    §IV-B2). Không có: đánh giá không huấn luyện lại (Fig. 8 là thích nghi khi huấn luyện
    tiếp), dịch chuyển có cấu trúc, đối chứng Fixed, nhiều seed + CI.
  - Gong 2024 (nhóm A1): chưa đọc toàn văn; rủi ro trùng lặp lớn nhất còn mở cùng OH-DRL 2025
    (chỉ có tóm tắt, 3 ô "Chưa rõ"; OpenAlex ghi đóng truy cập; chưa có toàn văn qua GVHD hoặc thư viện, G0-6).

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

| # | Tiêu chí | Hiện trạng (02/11) | Bằng chứng | Kết luận |
| --- | --- | --- | --- | --- |
| 1 | Ma trận `docs/04` §5 đủ các công trình gần nhất; mỗi ô có nguồn (mục/bảng) | Tìm kiếm Q1–Q3 xong (nháp, chờ LDN duyệt; PRISMA còn số "≈"). Nhóm A: 5/10 bài phần LDN có Form B nháp và hàng ma trận; 0/5 bài phần DAT đã đọc. Cột 6 mới chưa điền. OH-DRL vẫn chỉ có tóm tắt. | `notes/reading/search_log_LDN.md`, `fulltext_list.md`; `docs/04` §5 | **Chưa đạt (01/11).** Đạt được nếu trước 03/11: DAT đọc Gong, Lu, Toure; LDN duyệt sàng lọc và 5 Form B; điền cột 6. Không được kéo dài lần hai. |
| 2 | Không công trình nào đủ cả 6 cột (DECISIONS 2026-11-01) | Gần nhất: **Yi 2023** (Có, Có, Có, Một phần, Không; cột 6 Không theo Form B nháp). Các hàng khác đều thiếu từ 2 cột trở lên. Cột "Nhiều seed + CI" là Không ở mọi bài đã đọc toàn văn. | Form B tương ứng | **Chưa kết luận được (02/11, theo LDN).** Trong 14 bài đã có hàng ma trận, không bài nào đủ 6 cột; Gong 2024, Lu 2025, Toure 2026 chưa đọc. Điểm mới về mô hình (tốc độ là hành động, nhiều bố trí) **không còn**. |
| 3 | Câu định vị `docs/01` §3 được GVHD đồng ý | Có câu bản 2 (nháp 01/11): điểm mới chuyển sang cách đánh giá (không huấn luyện lại, 4 dịch chuyển có cấu trúc, đối chứng Fixed, ≥ 10 seed + CI). Chưa gửi GVHD. | `docs/01` §3 | **Chờ GVHD.** Hỏi GVHD: đóng góp nặng về đánh giá có đủ cho hội nghị đích không. |

## Việc phải xong trước họp 04/11 để tiêu chí 1 đạt

| Việc | Owner | Phụ thuộc |
| --- | --- | --- |
| ~~Đẩy kết quả tìm kiếm Q1–Q3~~ | LDN | Xong 31/10 (nháp). Còn: LDN duyệt sàng lọc, thay số "≈" trong PRISMA |
| ~~Form B Yi 2020, Sarathchandra 2025~~ | LDN | Nháp 31/10; DAT second reader cần PDF (mạng Claude chặn arXiv) |
| Đọc Gong 2024 (A1), Lu 2025 (A3), Toure 2026 (A5), Form B + hàng ma trận | DAT (W2-DAT-01) | DAT tải PDF arXiv, Claude soạn nháp. **Hạn 03/11** |
| Chen–Hanzo 2024 (A4), Zhou 2024 (A7), OH-DRL 2025: toàn văn qua GVHD hoặc thư viện; nếu không được thì giữ "chỉ tóm tắt" và ghi rủi ro | DAT | Quyền IEEE Xplore |
| Duyệt 5 Form B nháp phần LDN; đối chiếu PDF Xiao 2024 | LDN (W2-LDN-01) | Hạn 03/11 |
| Điền cột 6 "đối chứng huấn luyện cố định" cho mọi hàng | Người đọc từng hàng | Hạn 03/11 |
| Câu định vị bản 2 (nháp đã có ở `docs/01` §3), sửa sau khi đọc nhóm A, gửi GVHD | DAT | Nhóm A đọc xong |

## Đề xuất quyết định (để DAT và GVHD cân nhắc)

- **Nếu trước 04/11 đọc xong nhóm A (Gong, Lu, Toure) mà vẫn không bài nào đủ 6 cột:** *tiếp tục*. Phạm vi tuyên bố giữ C1–C3 như `docs/01` §6, dùng câu định vị bản 2 (`docs/01` §3): điểm khác biệt là cách đánh giá (không huấn luyện lại; 4 dịch chuyển có cấu trúc; đối chứng huấn luyện trên bố trí cố định, điều Bayerlein 2021 §VI-B và Yi 2023 không có; ≥ 10 seed kèm CI). Không dùng "tốc độ là biến quyết định" làm điểm khác biệt (Yi 2023 đã có, G0-1).
- **Nếu đến 04/11 nhóm A phần DAT chưa đọc xong hoặc A4, A7, OH-DRL vẫn không có toàn văn:** *tiếp tục có điều kiện*. EXP-02 (W3) không phụ thuộc định vị nên vẫn chạy. Mọi câu khẳng định "khoảng trống" bị khoá cho tới khi đọc xong và chạy truy vấn bổ sung Q4, hạn trước G1 (15/11). Phải ghi vào DECISIONS, vì G0 không được kéo dài lần hai.
- **Nếu một bài đủ 6 cột:** áp dụng nhánh "không đạt" của tiêu chí 2. Đổi trọng tâm sang A5 (vai trò lựa chọn tốc độ) hoặc đa UAV; GVHD quyết.

## Cần nói rõ trong buổi họp

- Ma trận và kết luận #2 là **dữ kiện từ các bài đã đọc** trong 57 bài sau sàng lọc (PRISMA ở `search_log_LDN.md` §4), không phải kết luận về toàn bộ tài liệu. Q1–Q3 thiếu từ khoá tốc độ/chuyển giao (G0-5).
- Hàng Yi 2020 đã có Form B (LDN, e7c652a; DAT chưa second reader vì chưa có PDF).
- Khoá `lamenza2025` giữ nguyên dù bài xuất bản 2026 (tập 8); trường `year` đã đúng (DECISIONS 2026-10-30).
