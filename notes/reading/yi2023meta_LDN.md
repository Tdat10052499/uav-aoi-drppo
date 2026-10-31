# Form B — `yi2023meta`

> Trạng thái: **nháp chờ LDN duyệt**, Claude soạn ngày 31/10/2026 từ toàn văn bản HTML ar5iv của arXiv:2311.06742v1. Người đọc: LDN (nhóm A2 trong `fulltext_list.md`). Second reader: DAT. Bản tạp chí 2025 (Scholar ghi "IEEE Transactions on …", tiêu đề dùng "AAV") chưa đọc; số mục/hình theo bản arXiv.
> **Mức độ liên quan: cao.** Bài có cả AoI, năng lượng đẩy phụ thuộc tốc độ với tốc độ là hành động, và trạng thái chứa vị trí nút. Xem mục "Khác biệt với đề tài".

**Tiêu đề / tác giả / năm / nơi công bố hoặc trạng thái preprint:** *Meta-Reinforcement Learning for Timely and Energy-efficient Data Collection in Solar-powered UAV-assisted IoT Networks*, 2023.
- **Tác giả:** Mengjie Yi, Xijun Wang, Juan Liu, Yan Zhang, Ronghui Hou (ĐH Tây An Điện tử, ĐH Trung Sơn, ĐH Ninh Ba). Cùng nhóm với Yi 2020.
- **Trạng thái:** preprint arXiv:2311.06742v1 [cs.IT], 12/11/2023. Bản tạp chí 2025 ✱ (chưa kiểm tên tạp chí và DOI).

**URL nguồn gốc và phiên bản/ngày truy cập:** https://arxiv.org/abs/2311.06742 (v1); toàn văn https://ar5iv.labs.arxiv.org/html/2311.06742, truy cập 31/10/2026.

**Người đọc (NICK):** LDN

**Bài báo trả lời câu hỏi gì:** Một UAV cánh quay dùng pin mặt trời thu gói cập nhật từ các cảm biến lấy mẫu ngẫu nhiên, lưu trong bộ đệm rồi chuyển về trung tâm dữ liệu (DC). Bài tối ưu đồng thời vận tốc (tốc độ và hướng), lịch cảm biến và quyết định chuyển dữ liệu để tối thiểu tổng có trọng số giữa AoI trung bình tại DC và năng lượng tiêu thụ của UAV; sau đó dùng meta-learning để chính sách thích nghi nhanh khi số và vị trí cảm biến thay đổi (§I, bài toán P1, PT (15a)–(15e)).

**Giả định hệ thống:**
- **Quy mô:** một UAV, độ cao H = 100 m; cảm biến đặt ngẫu nhiên trong vùng 200 m × 200 m; DC ở (0, 160 m); T = 100 khe, τ₀ = 0,5 s (§V-A, Bảng I). Số cảm biến N thay đổi giữa các thí nghiệm (Fig. 5 quét N; Fig. 8 đổi 16 → 12).
- **Chuyển động:** vận tốc liên tục dạng cực (tốc độ v_s, hướng φ), gia tốc hằng trong khe, ràng buộc v_s ≤ 20 m/s và góc quay ≤ π/3 mỗi khe (§III, PT (15c)–(15e), Bảng I).
- **Năng lượng đẩy:** mô hình của Ding et al. 2020 (tham chiếu [6] trong bài) cho UAV 4 rotor, phụ thuộc **cả tốc độ và gia tốc** qua lực đẩy mỗi rotor (PT (9)–(10)). Đây không phải dạng P(V) của Zeng 2019 nhưng cùng tính chất: năng lượng phụ thuộc tốc độ. Năng lượng nằm **trong mục tiêu** với trọng số ω₂ (PT (15a)); mô phỏng dùng ω₁ : ω₂ = 1 : 10 (Bảng I).
- **Năng lượng thu:** năng lượng mặt trời đến theo quá trình Bernoulli (PT (12)–(13)). Pin dưới ngưỡng E_th1 thì UAV hạ cánh chờ sạc tới E_th2 (§III, PT (11), (14)).
- **Kênh:** xác suất LoS theo góc ngẩng (Al-Hourani) cộng fading nhỏ (PT (1)–(3)); thu thành công khi SNR vượt ngưỡng (PT (4)).
- **AoI:** tính tại DC, qua hai tầng bộ đệm (cảm biến → UAV → DC); cảm biến sinh gói theo Poisson với tốc độ λ₀ (PT (6)–(8)).

**Cơ chế, diễn đạt bằng lời của mình:**
- **Trạng thái** gồm vị trí tương đối từ UAV tới **mọi** nút (cảm biến và DC), tốc độ, hướng trước đó, tuổi gói ở cảm biến và ở UAV, AoI tại DC, và mức pin (§IV-A1). Như vậy trạng thái **có chứa bố trí cảm biến**, khác Yi 2020.
- **Hành động hỗn hợp:** tốc độ và hướng (liên tục) cộng lịch cảm biến và quyết định chuyển (rời rạc), kích thước phần rời rạc 2(N+1) (§IV-A2, §IV-B1).
- **CADRL:** actor–critic với hai đầu actor dùng chung các lớp đầu (một đầu softmax cho hành động rời rạc, một đầu Gauss cho hành động liên tục), cập nhật bằng TRPO và GAE (PT (18)–(21), Fig. 2, Algorithm 1).
- **MLCADRL:** MAML với vòng trong REINFORCE trên từng nhiệm vụ và vòng ngoài TRPO (PT (22)–(28), Algorithm 2). Mỗi vòng meta lấy I = 15 nhiệm vụ, K = 5 quỹ đạo mỗi nhiệm vụ, L_meta = 10 000 vòng (Bảng II). Bài nói CADRL chỉ dùng được cho một nhiệm vụ có số và vị trí cảm biến cố định, và meta-learning được thêm vào để xử lý khi nhiệm vụ đổi (§IV-B2).

**Bằng chứng mạnh nhất (mục/bảng/hình):**
- **Fig. 4:** CADRL hội tụ nhanh hơn DQN, DDPG và P-DQN; cuối cùng ngang P-DQN (§V-B).
- **Fig. 5:** theo N, CADRL có tổng có trọng số thấp nhất. Heuristic theo AoI tốn năng lượng nhất vì luôn tăng tốc tối đa, còn các phương pháp học điều chỉnh vận tốc nên tiết kiệm năng lượng (§V-B, Fig. 5b). Đây là bằng chứng trực tiếp rằng **lựa chọn tốc độ** làm giảm năng lượng trong bài toán AoI.
- **Fig. 6:** quét tốc độ lấy mẫu λ₀; năng lượng gần như không đổi theo λ₀ vì năng lượng bay lớn hơn nhiều so với năng lượng truyền (§V-B).
- **Fig. 7:** chất lượng hội tụ của MLCADRL tăng theo số nhiệm vụ I, bão hoà ở I = 15 (§V-C).
- **Fig. 8:** tại episode 1500, môi trường đổi từ 16 xuống 12 cảm biến và vị trí cảm biến cũng đổi; MLCADRL lấy lại phần thưởng nhanh hơn TLCADRL (học chuyển giao) và CADRL (§V-C).

**Đánh giá trên kịch bản khác tập huấn luyện? Loại dịch chuyển nào?** Có, một phần.
- Dịch chuyển: **số và vị trí cảm biến** (Fig. 8). Chỉ có **một** lần đổi nhiệm vụ được báo cáo.
- Cách đo: tốc độ thích nghi khi **tiếp tục huấn luyện** trên nhiệm vụ mới, không đo hiệu năng ngay khi gặp nhiệm vụ mới (không zero-shot).
- Không có dịch chuyển có cấu trúc (phân cụm, mật độ ngoại suy, vùng rộng hơn, ngân sách năng lượng khác). Phân phối nhiệm vụ p(M) dùng khi meta-training không được mô tả cụ thể (§IV-B2).
- Không rõ cách mạng xử lý N thay đổi, vì kích thước trạng thái và phần hành động rời rạc phụ thuộc N (§IV-A1, §IV-B1).

**Số seed / cách báo cáo độ bất định:** Không báo số seed. Mỗi hình một đường cho mỗi phương pháp, không có vùng tin cậy hay kiểm định (Fig. 4–8).

**Đối chứng gần nhất và độ công bằng của so sánh:**
- Năm đối chứng: DQN (rời rạc hoá hành động liên tục), DDPG (liên tục hoá hành động rời rạc), P-DQN, heuristic theo AoI, và TLCADRL (học chuyển giao) (§V-A).
- Heuristic theo AoI luôn bay với tốc độ và gia tốc tối đa (§V-B), nên so sánh năng lượng thiên về các phương pháp học. Không có heuristic có điều chỉnh tốc độ (ví dụ bay ở tốc độ tối thiểu năng lượng).
- Không có đối chứng "huấn luyện trên một bố trí cố định rồi đánh giá trên bố trí khác" như Fixed-PPO của đề tài.
- Không nêu ngân sách tinh chỉnh siêu tham số cho các đối chứng.

**Giới hạn đã biết:**
1. Không mô tả phân phối nhiệm vụ meta-training và cách xử lý số cảm biến thay đổi.
2. Fig. 8 chỉ một lần đổi nhiệm vụ, một lần chạy.
3. Phần văn bản Fig. 8 nhắc "SLCADRL", trong khi danh sách đối chứng gọi là TLCADRL (§V-A, §V-C); nhiều khả năng là lỗi in.
4. Phiên bản phần mềm (Torch 1.3.0, Python 3.6) được nêu, nhưng không công bố mã.

**Khác biệt với đề tài (điền thẳng vào ma trận docs/04 §5):**
- **Trùng với đề tài:** AoI + năng lượng đẩy phụ thuộc tốc độ trong mục tiêu, **tốc độ là biến quyết định**, trạng thái chứa vị trí cảm biến, huấn luyện trên nhiều bố trí (qua meta-learning). Vì vậy đề tài **không** thể nêu "năng lượng phụ thuộc tốc độ với tốc độ là hành động" như điểm mới, và không thể nêu "huấn luyện trên nhiều bố trí" như điểm mới.
- **Khác biệt còn kiểm chứng được:**
  1. Đánh giá **không tinh chỉnh** trên bố trí mới, so với Yi 2023 đo tốc độ thích nghi có huấn luyện tiếp (Fig. 8).
  2. Bốn dịch chuyển **có cấu trúc** và có tên (cụm, mật độ ngoại suy, vùng rộng, năng lượng thấp), so với một lần đổi N và vị trí.
  3. Đối chứng huấn luyện trên bố trí cố định (Fixed-PPO) để cô lập tác dụng của DR; Yi 2023 không có.
  4. Nhiều seed + CI + kiểm định có hiệu chỉnh Holm; Yi 2023 không báo seed.
  5. Phương pháp đơn giản hơn (DR + PPO, không meta-learning); có thể nêu như điểm thực dụng, không phải đóng góp chính.
- **Đề nghị cho câu định vị bản 2:** dời trọng tâm từ "có năng lượng phụ thuộc tốc độ" sang "đánh giá tổng quát hoá theo bố trí một cách có kiểm soát (đối chứng Fixed, OOD có cấu trúc, nhiều seed + CI)". DAT quyết.

Hàng ma trận đề xuất (hàng mới):

| Công trình | Mục tiêu AoI | Năng lượng phụ thuộc tốc độ | Huấn luyện trên nhiều bố trí | Đánh giá OOD có cấu trúc | Nhiều seed + CI |
| --- | --- | --- | --- | --- | --- |
| Yi 2023 (arXiv 2311.06742) | Có (AoI trung bình tại DC + ω₂·năng lượng UAV; PT (15a)) | Có (công suất đẩy phụ thuộc tốc độ và gia tốc, PT (9)–(10); tốc độ và hướng là hành động liên tục, §IV-A2) | Có (meta-training MAML trên nhiều nhiệm vụ khác số và vị trí cảm biến, §IV-B2, Bảng II; trạng thái chứa vị trí tương đối tới mọi nút, §IV-A1) | Một phần (một lần đổi N 16 → 12 và vị trí, đo tốc độ thích nghi khi huấn luyện tiếp, không zero-shot, không dịch chuyển có cấu trúc; Fig. 8) | Không (không báo seed, mỗi hình một đường; Fig. 4–8) |

**Có mã nguồn/dữ liệu không:** Không thấy liên kết mã hay dữ liệu.

**Tài liệu tra ngược đáng đọc (không ra trong Q1–Q3):**
- Chu, Hoang, Nguyen, Van Huynh, Dutkiewicz, *Joint Speed Control and Energy Replenishment Optimization for UAV-assisted IoT Data Collection with Deep Reinforcement Transfer Learning*, IEEE IoT-J 2022 ✱ (tham chiếu [17]): điều khiển tốc độ + DRL + chuyển giao sang nhiệm vụ mới.
- Sun, Xu, Qin, Zhang, *AoI-Energy-Aware UAV-Assisted Data Collection for IoT Networks: A DRL Method*, IEEE IoT-J 8(24), 2021 (tham chiếu [39]).
- Li, Ni, Tovar, Guizani, *Joint Flight Cruise Control and Data Collection in UAV-Aided IoT: An Onboard DRL Approach*, IEEE IoT-J 8(12), 2021 (tham chiếu [40]): điều khiển tốc độ hành trình.
- Yi et al., *Multi-Task Transfer DRL for Timely Data Collection in Rechargeable-UAV-aided IoT Networks*, IEEE IoT-J 2023 ✱ (tham chiếu [45]).
- Lu, Wang, Gursoy, *Trajectory Design for UAVs via Meta-Reinforcement Learning*, INFOCOM Workshops 2023 (tham chiếu [46]).

**Một câu hỏi cho nhóm:** Yi 2023 cho thấy cột "năng lượng phụ thuộc tốc độ" không còn là khoảng trống. Có nên bỏ cột này khỏi ma trận định vị (giữ trong bảng mô tả hệ thống) và thay bằng cột "có đối chứng huấn luyện trên bố trí cố định" để ma trận phản ánh đúng điểm khác biệt còn lại không?
