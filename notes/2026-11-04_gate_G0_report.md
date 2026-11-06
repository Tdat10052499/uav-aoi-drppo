# Báo cáo gate G0 — định vị đóng góp (Form G)

> **Trạng thái: NHÁP** do Claude soạn cho DAT ngày 30/10/2026, cập nhật 01/11 theo kết quả Q1–Q3 của LDN, và 02/11 theo phản biện của LDN (`notes/review_log.md` G0-1 … G0-6). Owner: DAT. Second reader: LDN (W2-LDN-03). Gate dời từ 01/11 sang **T4 04/11/2026** (DECISIONS 2026-10-30). Đây là lần kéo dài duy nhất được phép.
> **Cập nhật 06/11/2026 (Claude soạn cho DAT, chờ DAT và LDN đọc lại):** sửa theo A7 của LDN (`notes/review_log.md` G0-7) và thêm kết quả đọc Gong, Lu, Toure. Lịch ghi họp G0 ngày 04/11, nhưng repo chưa có biên bản; mục "Quyết định" vẫn để trống, nhóm phải tự điền. EXP-02b, PREREG và EXP-03 đã diễn ra trong lúc G0 chưa đóng; đây là dữ kiện cần nêu tại buổi chốt.
> Mọi nhận định dưới đây đều có nguồn (mục/PT/bảng của Form B, hoặc commit). Báo cáo không đưa thêm số liệu thực nghiệm nào ngoài các số đã có trong repo.

```text
Ngày và gate: G0 — định vị đóng góp. Họp gate T4 04/11/2026 (gốc CN 01/11).

Bằng chứng xem xét, kể cả lần chạy thất bại (run ID):
  - Tìm kiếm Q1–Q3 (notes/reading/search_log_LDN.md, LDN duyệt sàng lọc 03/11, §7): arXiv 17 +
    OpenAlex 23 + Scholar 300 bản ghi; 279 bản ghi duy nhất (PRISMA đã chốt, search_log §4);
    giữ 58 bài đọc toàn văn (nhóm A 10, B 13, C 35), loại 29 ở bước tóm tắt; thêm 5 bài từ tra
    ngược Yi 2023. IEEE Xplore và Scopus thay bằng OpenAlex (DECISIONS 2026-11-01).
  - Ma trận định vị docs/04 §5: 13 hàng trên main (không kể "Đề tài này", đã gồm Liu 2025, PR #40); thêm
    Gong, Lu, Toure qua PR #49, tổng 16 hàng. Cột 6 "đối chứng huấn luyện cố định" (DECISIONS 01/11).
  - Form B toàn văn đã duyệt: bayerlein2021multi_DAT, zeng2019energy_DAT, lamenza2025_DAT
    (LDN second reader 01/11); abdelmagid2019deep_FAO, sun2025aoi_FAO, liu2024generalizable_FAO.
    Form B phần LDN: yi2020deep, sarathchandra2025age, yi2023meta, eldeeb2026, xiao2024meta,
    liu2025resource (LDN duyệt phần của mình; DAT chưa second reader).
    Form B nháp Claude 06/11, chờ DAT đọc lại: gong2024uav_DAT, lu2025attention_DAT,
    toure2026optimizing_DAT (toàn văn ar5iv, đã đối chiếu mục và PT với văn bản).
    Form B chỉ có tóm tắt (1): ohdrl2025_FAO.
    Nhóm A phần DAT chưa đọc (2): Chen–Hanzo 2024, Zhou 2024 (chỉ có trên IEEE; tìm arXiv 06/11
    theo tiêu đề không thấy bản công khai).
  - Câu định vị nháp: docs/01 §3.
  - G0 không có thực nghiệm. Không có lần chạy nào là bằng chứng của gate này.

Baseline có chạy đúng không? Bằng chứng:
  Không phải tiêu chí của G0. Tham khảo: EXP-01 (heuristic) tái lập bit-identical trên
  laptop DAT, 0/1500 dòng lệch (run EXP-01/20261025-115153 so với 20261020-084218;
  Form C ở notes/EXP-01_reproduction_card.md; FAO kiểm lại bằng compare_events.py: MATCH).

Hiệu ứng chính có đạt tiêu chí khai báo trước không? Bằng chứng (bảng tiêu chí):
  Xem bảng "Đối chiếu tiêu chí G0" bên dưới.
  Tóm tắt (06/11): #1 CHƯA ĐẠT (còn A4, A7, OH-DRL chưa có toàn văn); #2 KHÔNG BÀI NÀO ĐỦ 6 CỘT
  trong 16 hàng, nhưng chưa loại trừ được do 3 bài còn thiếu và G0-5; #3 CHỜ NHÓM THỐNG NHẤT.

Giải thích thay thế mạnh nhất còn đứng vững:
  Tìm kiếm đã chạy (01/11), nên "khoảng trống" không còn chỉ dựa trên 9 bài. Nhưng:
  (1) Yi 2023 đã có AoI + năng lượng phụ thuộc tốc độ với tốc độ là hành động + huấn luyện
  nhiều bố trí (Có, Có, Có, Một phần, Không); điểm mới về mô hình không còn. (2) Gong 2024 cũng
  có AoI + P(v) + tốc độ là hành động (PT (4)–(6), (9)), dù "môi trường" là tham số hàng đợi chứ
  không phải bố trí. (3) "Không huấn luyện lại" một mình không còn là điểm khác biệt: Lu 2025
  (không cập nhật θ, có prompt trực tuyến; §IV, Fig. 3–4) và Toure 2026 (§V-D, Fig. 6) đã làm trên
  số người dùng hoặc thiết bị. (4) A4, A7, OH-DRL chưa có toàn văn. (5) OpenAlex có thể sót bài IEEE
  thiếu tóm tắt trong chỉ mục (chưa kiểm). (6) Q1–Q3 không có từ khoá tốc độ (speed, velocity)
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
  - Gong 2024 (A1, gong2024uav_DAT, nháp): Có / Có / Không rõ / Một phần / Không / Không. Trùng ở mô
    hình; khác ở chỗ UAV cập nhật chính sách CPU cho thiết bị, dịch chuyển là tham số hàng đợi (§II-B,
    §II-C, §III-C), không báo seed, không có đối chứng bố trí cố định (§V-A2).
  - Lu 2025 (A3, lu2025attention_DAT, nháp): Có / Không / Một phần / Một phần / Không / Không.
  - Toure 2026 (A5, toure2026optimizing_DAT, nháp): Không / Không / Có / Một phần / Một phần (3 seed,
    không CI) / Không.
  - Liu 2025 (A10, liu2025resource_LDN): Có / Không / Không rõ / Không / Không / Không; LDN kết luận
    không phải rủi ro cho tiêu chí #2 (yêu cầu LDN→DAT A7 mục 5).
  - OH-DRL 2025: chỉ có tóm tắt, 3 ô "Chưa rõ"; OpenAlex ghi đóng truy cập (G0-6). Cùng A4, A7, đây là
    rủi ro trùng lặp còn mở.

Nhu cầu tính toán/thời gian còn lại:
  Ước lượng 163,2 M bước (Phương án B) không còn áp dụng. Kế hoạch đã đổi hai lần sau khi báo cáo này
  được viết: lịch FJCAI và PREREG khoá 03/11 (DECISIONS 03/11), rồi PG-TG-PPO, EXP-08 ≈ 40–55 giờ máy,
  ước tính (DECISIONS 06/11).

Quyết định: [nhóm chọn tại họp G0, chưa có biên bản; đề xuất bên dưới]
Lý do:
Phạm vi tuyên bố được duyệt:
Thực nghiệm tiếp theo và owner: EXP-08a (LDN), EXP-08p (DAT), theo `notes/EXP-08_PG-TG-PPO_card.md`.
Ngày quyết định tiếp theo: G1 — T6 20/11/2026.
Ý kiến giảng viên: GVHD góp ý ở bản nháp bài (DECISIONS 06/11).
```

## Đối chiếu tiêu chí G0 (`docs/05` §5)

| # | Tiêu chí | Hiện trạng (02/11) | Bằng chứng | Kết luận |
| --- | --- | --- | --- | --- |
| 1 | Ma trận `docs/04` §5 đủ các công trình gần nhất; mỗi ô có nguồn (mục/bảng) | Tìm kiếm Q1–Q3 xong; PRISMA chốt 02/11; LDN duyệt sàng lọc 03/11. Nhóm A: 3/5 bài phần DAT có Form B nháp và hàng ma trận (PR #49); phần LDN đủ (Liu 2025, PR #40 đã merge). Cột 6 đủ ở các hàng trên main. Còn thiếu: A4, A7 (IEEE), OH-DRL (chỉ tóm tắt). | `notes/reading/search_log_LDN.md`, `fulltext_list.md`; `docs/04` §5 | **Chưa đạt (06/11).** Phần còn lại phụ thuộc quyền truy cập toàn văn. Nếu không có thì ghi rõ là giới hạn; nhóm quyết định có chấp nhận không. Không được kéo dài lần hai. |
| 2 | Không công trình nào đủ cả 6 cột (DECISIONS 2026-11-01) | Gần nhất về mô hình: **Yi 2023** (Có, Có, Có, Một phần, Không, Không) và **Gong 2024** (Có, Có, Không rõ, Một phần, Không, Không; nháp). Không hàng nào "Có" ở cột OOD có cấu trúc trừ Liu 2024 (đua drone, ngoài phạm vi). Về thống kê, cao nhất là Toure 2026: 3 seed, không CI. | Form B tương ứng | **Không bài nào đủ 6 cột trong 16 hàng (06/11; 3 hàng mới chờ DAT duyệt).** Chưa loại trừ hẳn: A4, A7, OH-DRL chưa đọc; Q4 (G0-5) chưa chạy. Điểm mới về mô hình (tốc độ là hành động, nhiều bố trí) **không còn**. |
| 3 | Câu định vị `docs/01` §3 được cả nhóm thống nhất (đổi 06/11; GVHD góp ý ở bản nháp bài) | Có câu bản 2 (nháp 01/11), viết cho DR-PPO; sẽ được thay khi chốt bản cho PG-TG-PPO (`docs/01` §3, ghi chú 06/11). Đọc Lu và Toure cho thấy không được nêu "không huấn luyện lại" như điểm khác biệt riêng. | `docs/01` §3 | **Chờ nhóm.** Cần nhóm xem đóng góp nặng về đánh giá có đủ cho hội nghị đích không. |

## Việc còn lại để đóng G0

| Việc | Owner | Trạng thái (06/11) |
| --- | --- | --- |
| Đọc Gong 2024, Lu 2025, Toure 2026, Form B + hàng ma trận | DAT (W2-DAT-01) | Nháp xong; DAT đọc lại, rồi second reader |
| Chen–Hanzo 2024 (A4), Zhou 2024 (A7), OH-DRL 2025: toàn văn qua thư viện; nếu không được thì giữ "chỉ tóm tắt" và ghi rủi ro | DAT | Chưa có; không thấy bản arXiv của A4, A7 |
| Merge PR #49 (hàng Gong, Lu, Toure) | LDN review | Đang mở; PR #40 đã merge 06/11 (cột 6, hàng Liu 2025) |
| Truy vấn bổ sung Q4 (G0-5) | Nhóm chốt owner | Chưa chạy |
| Chốt câu định vị cho PG-TG-PPO | DAT, nhóm | Chưa chốt |
| Họp G0, điền mục "Quyết định" (W2-ALL-01) | Cả nhóm | Chưa có biên bản |

## Đề xuất quyết định (để nhóm cân nhắc)

- **Đề xuất với hiện trạng 06/11: *tiếp tục có điều kiện*.** Lý do: 16 hàng không bài nào đủ 6 cột, nhưng A4, A7, OH-DRL chưa đọc. Mọi câu khẳng định "khoảng trống" bị khoá cho tới khi đọc xong hoặc ghi rõ giới hạn và chạy Q4. Phải ghi vào DECISIONS, vì G0 không được kéo dài lần hai.
- **Phạm vi tuyên bố khi tiếp tục:** điểm khác biệt nằm ở tổ hợp, không ở từng yếu tố: AoI nhiều chu kỳ với P(v) và tốc độ là hành động, 4 dịch chuyển có cấu trúc gồm cả phân bố không gian, đối chứng cùng learner trên bố trí cố định, ≥ 10 seed kèm CI. Không dùng riêng "tốc độ là biến quyết định" (Yi 2023, Gong 2024) hay riêng "không huấn luyện lại" (Lu 2025, Toure 2026).
- **Nếu một bài đủ 6 cột:** áp dụng nhánh "không đạt" của tiêu chí 2: đổi trọng tâm sang A5 (vai trò lựa chọn tốc độ) hoặc đa UAV; nhóm quyết.

## Cần nói rõ trong buổi họp

- Ma trận và kết luận #2 là **dữ kiện từ các bài đã đọc** trong 58 bài sau sàng lọc (PRISMA ở `search_log_LDN.md` §4), không phải kết luận về toàn bộ tài liệu. Q1–Q3 thiếu từ khoá tốc độ/chuyển giao (G0-5).
- Hàng Yi 2020 đã có Form B (LDN, e7c652a; DAT chưa second reader vì chưa có PDF).
- Khoá `lamenza2025` giữ nguyên dù bài xuất bản 2026 (tập 8); trường `year` đã đúng (DECISIONS 2026-10-30).
