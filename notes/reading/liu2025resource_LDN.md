# Form B — `liu2025resource`

> Trạng thái: **LDN đã duyệt 03/11/2026.** Claude soạn ngày 03/11/2026 từ toàn văn bản thảo đã chấp nhận (accepted author manuscript, 18 trang kể cả trang bìa Aaltodoc). LDN tải PDF từ kho Aaltodoc của ĐH Aalto, rồi Claude đọc bằng trích văn bản (pdftotext) và kiểm Bảng I bằng ảnh trang. Số trang dưới đây theo bản thảo (trang 1 là trang đầu bài, sau trang bìa). Bản tạp chí có thể khác bản thảo về trình bày.
> Người đọc: LDN (nhóm **A10** trong `fulltext_list.md`; trước 03/11 là C1). Second reader: DAT.
> **Kết luận nhanh: bài không đe doạ định vị.** "Transferability" chỉ là một câu khẳng định ở §VII-A3, kèm link GitHub; bài không có thí nghiệm nào huấn luyện ở một kịch bản rồi đánh giá ở kịch bản khác mà không huấn luyện lại.

**Tiêu đề / tác giả / năm / nơi công bố hoặc trạng thái preprint:** *Resource Allocation for UAV-Enabled Spatio-Temporal Crowdsourcing in Smart Cities*.
- **Tác giả:** Yaxi Liu, Wencan Mao, Xulong Li, Wei Huangfu (tác giả liên hệ), Yu Xiao, Yusheng Ji, Haijun Zhang, Keping Long. Cơ quan: ĐH Khoa học và Công nghệ Bắc Kinh; Viện Tin học Quốc gia Nhật Bản; ĐH Aalto.
- **Nơi công bố:** *IEEE Transactions on Vehicular Technology*, 75(1), tr. 1233–1249, 2026; xuất bản trực tuyến 2025; DOI 10.1109/TVT.2025.3591850. Số tập và số trang lấy từ TRID và OpenAlex, chưa kiểm trên IEEE Xplore ✱.
- **Khoá BibTeX đề xuất:** `liu2025resource`. Chưa thêm vào `paper/references.bib` (sửa `paper/` phải qua PR).

**URL nguồn gốc và phiên bản/ngày truy cập:** https://doi.org/10.1109/TVT.2025.3591850. Bản đọc: bản thảo đã chấp nhận trên Aaltodoc, https://aaltodoc.aalto.fi/handle/123456789/138348, LDN tải ngày 03/11/2026.

**Người đọc (NICK):** LDN

**Bài báo trả lời câu hỏi gì:** Với nhiều UAV thu dữ liệu chất lượng không khí từ thiết bị IoT trong đô thị có vùng cấm bay, làm sao chọn quỹ đạo UAV và công suất phát của thiết bị để tối thiểu đồng thời AoI trung bình và năng lượng của UAV và thiết bị IoT (§III-A, bài toán (18a)–(18h)). Bài giải bằng ba thuật toán DRL có sẵn (TD3, PPO, SAC) và thử trên một kịch bản tổng hợp và một kịch bản thành phố thật (§V, §VI).

**Giả định hệ thống:**
- **Quy mô:**
  - Tổng hợp: 1 UAV; vùng 1000 m × 1000 m; M = 20 thiết bị; N = 100 khe; độ cao 100–200 m; 2 vùng cấm bay (khối hộp và trụ) (§V-A, Fig. 6).
  - Thành phố thật: khu trung tâm một thành phố lớn ở miền đông Trung Quốc; toà nhà là vùng cấm bay; 1–4 UAV, chọn 4 (§VI-A, Fig. 12–13).
- **Thời gian:** khe dài τ = Δt = 1 s (Bảng I). Mỗi khe UAV bay tới điểm đích rồi treo để thu (Fig. 2).
- **Chuyển động:** hành động là độ dời liên tục (Δx, Δy, Δz) của mỗi UAV, chặn |Δx|, |Δy| ≤ 50 m và |Δz| ≤ 5 m mỗi khe (PT (20)–(21), ràng buộc C5–C7, Bảng I).
- **Năng lượng UAV:** mô hình rotor cánh quay dạng Zeng 2019 (PT (13)–(15), trích [35]). Năng lượng bay bằng P(V_m) nhân thời gian bay ‖Δu‖/V_m, cộng năng lượng treo trong **cả khe** (giả định xấu nhất). **V_m = 16,67 m/s là hằng số** (Bảng I), nên tốc độ không phải biến quyết định; năng lượng bay tỉ lệ với quãng đường.
- **Năng lượng thiết bị:** p·min(T, τ) (PT (12)); công suất phát p ∈ [0,01; 0,1] W là biến quyết định (C4).
- **Kênh:** độ lợi g₀G₀/d² (PT (9)); OFDMA trong cùng UAV, nhiễu từ thiết bị gửi UAV khác (PT (7), (11)); phạm vi liên lạc hiệu dụng 180 m (tổng hợp) và 500 m (thành phố) (§V-A, §VI-A).
- **AoI:** tính bằng giây; bằng thời gian truyền T khi thu được, ngược lại tăng 1 mỗi khe, chặn tại A_max (PT (5), Fig. 3).
- **Mục tiêu:** Ā + κ₁Ē^I + κ₂Ē^U (PT (16)–(18a)).

**Cơ chế, diễn đạt bằng lời của mình:**
- **Trạng thái** chứa vị trí mọi UAV; vị trí, công suất, AoI và kích thước dữ liệu của mọi thiết bị; và chỉ báo liên kết (PT (19)). Như vậy trạng thái **có chứa vị trí thiết bị**, nhưng ở dạng vector có độ dài cố định theo M và K.
- **Phần thưởng** mỗi khe: −ω·O_n + H_n + c, với O_n là mục tiêu tính trong khe và H_n là phạt −h khi vi phạm biên hay vùng cấm bay (PT (22)–(24)).
- **Thuật toán:** TD3, PPO, SAC, mô tả chung một khung (Fig. 5); chỉ TD3 có giả mã (Algorithm 1–2). Siêu tham số chung ở Bảng II: γ = 0,98, bộ nhớ 10⁵, 10⁴ vòng huấn luyện, lô 256, bước 0,01, Adam. Không nêu siêu tham số riêng của từng thuật toán.
- **Vị trí xuất phát UAV** sinh ngẫu nhiên cả khi huấn luyện lẫn khi chạy (§V-B5).

**Bằng chứng mạnh nhất (mục/bảng/hình):**
- **Fig. 7 (tổng hợp):** cả ba thuật toán hội tụ; SAC có phần thưởng tích luỹ cao nhất và AoI trung bình thấp nhất (§V-B1–B2).
- **Fig. 10:** AoI hội tụ tăng theo mật độ thiết bị, 20–40 thiết bị/km² (§V-B6). Mỗi mật độ là một lần huấn luyện riêng.
- **Fig. 11:** đường Pareto giữa AoI và năng lượng khi đổi κ (§V-B7).
- **Fig. 13–14 (thành phố):** AoI giảm khi tăng số UAV và gần bão hoà từ 4 UAV; số thiết bị không được phục vụ là 6, 1, 1, 0 với 1–4 UAV (§VI-A).
- **Fig. 15:** TD3, PPO, SAC tốt hơn DDPG (không hội tụ), PSO, GA và chiến lược ngẫu nhiên (§VI-B). Fig. 15 là đường **huấn luyện** của DRL so với kết quả suy luận của các heuristic.

**Đánh giá trên kịch bản khác tập huấn luyện? Loại dịch chuyển nào?** **Không** có thí nghiệm như vậy trong bài.
- Kịch bản tổng hợp và kịch bản thành phố được huấn luyện riêng; Fig. 7 và Fig. 15 đều là đường huấn luyện.
- Các phép quét mật độ (Fig. 10), số UAV (Fig. 13) và κ (Fig. 11) đều là huấn luyện lại cho từng cấu hình.
- Biến thiên duy nhất giữa huấn luyện và chạy là vị trí xuất phát UAV, sinh ngẫu nhiên ở cả hai pha (§V-B5).
- "Transferability" chỉ xuất hiện ở tóm tắt, phần đóng góp và §VII-A3: "The proposed UAV-enabled spatio-temporal crowdsourcing framework has good generalization under various city topologies". Câu này kèm chú thích dẫn tới một kho GitHub có hình động của quá trình phân bổ. Bài không mô tả quy trình huấn luyện và đánh giá nào đứng sau câu đó.
- Vị trí thiết bị được sinh ngẫu nhiên (§V-A, §VI-A), nhưng bài chỉ vẽ một bố trí (Fig. 6, 12) và không nói có sinh lại bố trí mỗi episode hay không.

**Số seed / cách báo cáo độ bất định:** Không báo số seed hay số lần huấn luyện. Mỗi thuật toán một đường (Fig. 7, 10, 11, 13, 15); vùng mờ ở Fig. 7 có vẻ là đường thô chưa làm trơn, không phải khoảng tin cậy. PSO và GA được lấy trung bình 5 lần suy luận (chú thích Fig. 15). Không có kiểm định.

**Đối chứng gần nhất và độ công bằng của so sánh:**
- DDPG, PSO, GA (giải từng khe một cách tham lam) và chiến lược ngẫu nhiên (§VI-B1).
- So sánh khác loại: DRL được so bằng đường huấn luyện, còn heuristic bằng giá trị suy luận trung bình, rồi "giả sử áp dụng cho mọi episode" (§VI-B4).
- PSO và GA tối ưu từng khe nên không tính tác động lên các khe sau; bài tự nêu đây là lý do DRL tốt hơn (§VI-B4).
- Không có đối chứng huấn luyện trên bố trí cố định so với nhiều bố trí, và không có đối chứng TSP hay heuristic theo AoI.

**Giới hạn đã biết:**
1. "Transferability" không có thí nghiệm hỗ trợ trong bài (§VII-A3).
2. **Không khớp giữa độ dời và tốc độ:** độ dời tối đa mỗi khe 50 m theo x và y (‖Δu‖ tới khoảng 71 m) trong khe 1 s, nhưng năng lượng tính với V_m = 16,67 m/s, tức thời gian bay ‖Δu‖/V_m có thể tới khoảng 4,3 s, dài hơn khe. Thêm vào đó, năng lượng treo tính cho cả khe (PT (13), Bảng I).
3. Một số hằng số chọn "để giúp hội tụ" (ω, c, h, κ₁, κ₂; §V-A, §VI-A). κ₂ phụ thuộc E₀, nhưng E₀ chỉ xuất hiện đúng một lần trong bài, không được định nghĩa. Giá trị A_max cũng không được nêu (Bảng I không có).
4. Siêu tham số chung cho cả ba thuật toán (Bảng II), không có tinh chỉnh riêng.
5. Tên thành phố và nguồn dữ liệu toà nhà không được nêu (§VI-A). Không công bố mã huấn luyện; kho GitHub ở chú thích 1 chỉ có hình động.

**Khác biệt với đề tài (điền thẳng vào ma trận docs/04 §5):**
- **Liu 2025:** nhiều UAV; AoI + năng lượng UAV và thiết bị; tốc độ cố định; mỗi cấu hình huấn luyện riêng; không đánh giá zero-shot; không seed/CI.
- **Đề tài:** một UAV; năng lượng đẩy phụ thuộc tốc độ với tốc độ là hành động; DR theo bố trí; 4 bộ OOD có cấu trúc; đối chứng Fixed-PPO; 10 seed + CI.
- Bài **không** làm tiêu chí G0 #2 thất bại: chỉ đạt cột AoI. Có thể trích ở Related Work trong nhóm "AoI + năng lượng UAV, đánh giá trên kịch bản huấn luyện", và như ví dụ về việc khẳng định khả năng tổng quát hoá mà không có thí nghiệm có kiểm soát.

Hàng ma trận đề xuất (hàng mới):

| Công trình | Mục tiêu AoI | Năng lượng phụ thuộc tốc độ | Huấn luyện trên nhiều bố trí | Đánh giá OOD có cấu trúc | Nhiều seed + CI | Đối chứng huấn luyện trên bố trí cố định |
| --- | --- | --- | --- | --- | --- | --- |
| Liu 2025 (IEEE TVT; `notes/reading/liu2025resource_LDN.md`) | Có (Ā + κ₁Ē^I + κ₂Ē^U; PT (16)–(18a)) | Không (P(V) rotor PT (13)–(15) nhưng V_m = 16,67 m/s cố định, Bảng I; năng lượng bay tỉ lệ quãng đường) | Không rõ (vị trí thiết bị "randomly generated", chỉ vẽ một bố trí, Fig. 6, 12; không nói sinh lại mỗi episode; trạng thái chứa vị trí thiết bị, PT (19)) | Không (mỗi kịch bản, mật độ và số UAV huấn luyện riêng, Fig. 7, 10, 13, 15; "transferability" chỉ là câu khẳng định ở §VII-A3) | Không (không báo seed, một đường mỗi thuật toán; Fig. 7, 15) | Không (không có đối chứng theo tập huấn luyện; §V, §VI) |

**Có mã nguồn/dữ liệu không:** Không có mã huấn luyện. Chú thích 1 (§VII-A3) dẫn tới https://github.com/ustb-yaxi/Dynamicprocedure-of-resource-allocation.git, theo bài là nơi xem "quá trình phân bổ theo thời gian dưới các cấu trúc thành phố khác nhau". Chưa mở kho này.

**Một câu hỏi cho nhóm:** Bài dùng chữ "transferability" và "generalization" mà không có thí nghiệm huấn luyện–kiểm thử tách biệt. Related Work có nên nêu thẳng điều này (một câu, trích §VII-A3) để làm rõ vì sao đề tài cần đối chứng Fixed-PPO và bộ OOD có cấu trúc, hay chỉ trích bài như công trình AoI + năng lượng thông thường?
