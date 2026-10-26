# Form B — `bayerlein2021multi`

> Trạng thái: **nháp do Claude soạn từ toàn văn PDF** (arXiv:2010.12461v3, 15 trang, SHA256 `44d03192…dcbb3`, DAT tải và gửi ngày 26/10/2026). DAT đọc lại trước khi đánh dấu W1-DAT-02 xong; second reader: LDN. Mọi số liệu dưới đây lấy từ văn bản và bảng; không có số nào đọc từ hình.

**Tiêu đề / tác giả / năm / nơi công bố hoặc trạng thái preprint:** *Multi-UAV Path Planning for Wireless Data Harvesting with Deep Reinforcement Learning*, 2021.
- **Tác giả:** Harald Bayerlein, Mirco Theile, Marco Caccamo, David Gesbert (EURECOM; TU München).
- **Trạng thái:** preprint arXiv:2010.12461v3 [cs.MA], 03/06/2021. Chú thích trang 1 ghi một phần đã trình bày tại IEEE GLOBECOM 2020 (tham khảo [1] của bài). PDF không ghi nơi đăng bản mở rộng ✱.

**URL nguồn gốc và phiên bản/ngày truy cập:** https://arxiv.org/abs/2010.12461 (v3), bản PDF DAT tải ngày 26/10/2026.

**Người đọc (NICK):** DAT (nháp Claude)

**Bài báo trả lời câu hỏi gì:** Làm sao điều khiển một đội UAV thu **tối đa lượng dữ liệu** từ các cảm biến IoT trong đô thị, chịu ràng buộc thời gian bay và tránh va chạm (PT (13)), bằng **một** chính sách DRL dùng lại được khi tham số kịch bản thay đổi mà không phải huấn luyện lại (§I, §I-B).

**Giả định hệ thống:**
- **Số UAV:** I ∈ {1, 2, 3} khi huấn luyện, đồng nhất, không trao đổi với nhau (§V-C, §VI-C, §VI-D).
- **Không gian:** lưới M × M, ô c = 10 m; độ cao cố định h = 10 m; chỉ quỹ đạo 2D (§II, §II-A, §VI-A). Có toà nhà cao (không bay qua được), vùng cấm bay (NFZ) và vùng cất/hạ cánh.
- **Hành động:** 6 hành động rời rạc: hover, đông, bắc, tây, nam, hạ cánh (PT (1)); hạ cánh chỉ được phép trong vùng hạ cánh (PT (2)).
- **Tốc độ:** v ∈ {0, V} với V = c/δt, tức **chỉ một tốc độ bay** (§II-A). Tốc độ không phải biến quyết định.
- **Năng lượng:** pin giảm **1 đơn vị mỗi bước** khi UAV đang hoạt động (PT (5)), tức hằng số theo thời gian, như nhau khi bay và khi hover.
  - Lý do tác giả đưa ra: theo mô hình của Liu et al. 2017 (tham khảo [27], **không** phải Zeng 2019), công suất thêm để bay ngang 10 m/s so với hover ≈ 30 W/310 W ≈ 10%, được coi là "negligible" (§II-A).
  - Pin được gọi thẳng là "thời gian bay còn lại".
- **Kênh:** LoS/NLoS điểm–điểm, suy hao log-khoảng cách cộng shadow fading (PT (7)–(9)); bản đồ che khuất tính bằng ray tracing (biến thể thuật toán Bresenham); tham số theo 3GPP urban micro: α_LoS = 2,27, α_NLoS = 3,64, σ²_LoS = 2, σ²_NLoS = 5 (§VI-A). Tác nhân không biết trước bản đồ che khuất.
- **Truy nhập:** TDMA, mỗi khe truyền chọn cảm biến có SNR cao nhất còn dữ liệu (max-rate); mỗi khe nhiệm vụ có λ = 4 khe truyền (PT (10)–(11), §VI-A).
- **Mục tiêu:** **lượng dữ liệu thu**, không phải AoI. Mỗi cảm biến có lượng dữ liệu ban đầu D_k,init hữu hạn, thu xong là hết (§II-B), nên đây là bài thu **một lần**, không có dữ liệu sinh định kỳ.

**Cơ chế, diễn đạt bằng lời của mình:**
- **Mô hình hoá:** Dec-POMDP (§III). Thưởng của mỗi tác nhân (PT (17)–(19)) gồm bốn thành phần:
  - α × dữ liệu thu được (thành phần duy nhất dùng chung giữa các tác nhân);
  - phạt β khi bộ điều khiển an toàn từ chối hành động;
  - phạt γ khi hết pin mà chưa hạ cánh;
  - phạt hằng số ε mỗi bước di chuyển.
- **Bộ điều khiển an toàn** (PT (16), §III-B): hành động không hợp lệ (đâm vật cản, vào NFZ, va UAV khác, hạ cánh sai chỗ) bị thay bằng hover, kèm phạt β. Đây là cơ chế khác với action masking: tác nhân vẫn chọn được hành động sai và học tránh nó qua phạt.
- **Quan sát** (§IV, PT (20)–(36)):
  - Bản đồ **căn tâm** theo vị trí UAV, kích thước (2M−1) × (2M−1).
  - Bản đồ được tách làm hai: bản đồ cục bộ cắt l × l giữ nguyên chi tiết, và bản đồ toàn cục nén bằng average pooling hệ số g.
  - Các lớp bản đồ gồm: môi trường (vùng hạ cánh, NFZ/vật cản), dữ liệu còn lại của cảm biến, thời gian bay còn lại và trạng thái hoạt động của các UAV. Thêm một số vô hướng là thời gian bay còn lại của chính UAV.
  - Bảng II: tách toàn cục–cục bộ giảm số phép tính suy luận, ví dụ Manhattan32 cần 80 MFLOPs khi chỉ căn tâm, còn 7,7 MFLOPs khi căn tâm kèm tách toàn cục–cục bộ.
- **Học:** DDQN với combined experience replay, cập nhật mạng mục tiêu mềm τ; khi huấn luyện chọn hành động bằng softmax với nhiệt độ β (§V-B, PT (45)).
  - Huấn luyện tập trung, triển khai phi tập trung. Kinh nghiệm của mọi UAV được gom chung để huấn luyện một mạng dùng cho tất cả (§V-C).
  - Mạng gồm CNN cho các bản đồ rồi các lớp fully connected (Fig. 3).
- **Domain randomization** (tác giả không dùng thuật ngữ này): đầu mỗi episode, các tham số kịch bản được lấy ngẫu nhiên (§VI-A):
  - số UAV;
  - số và vị trí cảm biến;
  - lượng dữ liệu mỗi cảm biến;
  - thời gian bay ban đầu;
  - điểm xuất phát.

  Khoảng giá trị theo từng bản đồ:
  - Manhattan32: I ∈ {1, 2, 3}, K ∈ [3, 10], D_k,init ∈ [5, 20], b₀ ∈ [50, 150] bước, 18 điểm xuất phát (§VI-C).
  - Urban50: I ∈ {1, 2, 3}, K ∈ [5, 10], D_k,init ∈ [5, 20], b₀ ∈ [100, 200] bước, 40 điểm xuất phát (§VI-D).
  - Vị trí cảm biến lấy ngẫu nhiên trên toàn bộ ô trống. **Bản đồ (toà nhà, NFZ) cố định cho mỗi tác nhân.**
- **Siêu tham số** (Bảng III):
  - N_max = 3 M bước (32 × 32), 4 M bước (50 × 50);
  - |D| = 50 000, minibatch m = 128;
  - τ = 0,005, γ = 0,95, nhiệt độ β = 0,1;
  - l = 17; g = 3 (32 × 32), g = 5 (50 × 50);
  - số tham số |θ| = 1 175 302 (32 × 32) và 978 694 (50 × 50).

**Bằng chứng mạnh nhất (mục/bảng/hình):**
- **Bảng IV** (trung bình 1000 kịch bản Monte Carlo ngẫu nhiên trên toàn khoảng tham số):

  | Chỉ số | Manhattan32 | Urban50 |
  | --- | --- | --- |
  | Hạ cánh thành công | 99,4% | 98,8% |
  | Tỉ lệ thu dữ liệu | 88,0% | 82,1% |
  | Tỉ lệ thu và đã hạ cánh | 87,5% | 81,1% |

- **Fig. 4 + §VI-B:** tác nhân dùng bản đồ học được, còn bốn biến thể đầu vào vô hướng (toạ độ tuyệt đối/tương đối × mạng nhỏ/lớn) "không thích nghi hiệu quả" với kịch bản thay đổi.
  - Tác nhân dùng bản đồ đạt mức cuối sau khoảng 20% số bước huấn luyện.
  - 3 M bước mất khoảng 40 giờ trên GPU Titan Xp (2017).
  - Tác giả tự nói so sánh này "không hoàn toàn công bằng", vì vị trí NFZ, toà nhà và vùng hạ cánh khó biểu diễn bằng vô hướng.
- **§VI-E, Fig. 7:** ảnh hưởng của từng tham số; mỗi điểm là trung bình 500 kịch bản Monte Carlo.
  - Có ví dụ đánh đổi cấp hệ thống: 1 UAV cần b₀ = 150, còn 2 UAV chỉ cần b₀ = 75 để cùng đạt khoảng 88% tỉ lệ thu kèm hạ cánh (Manhattan32).
- **Fig. 5, Fig. 6:** quỹ đạo minh hoạ với I = 1, 2, 3 trên cùng một bộ cảm biến, cho thấy các UAV tự chia vùng thu.

**Đánh giá trên kịch bản khác tập huấn luyện? Loại dịch chuyển nào?** **Có, nhưng chỉ ngoại suy tham số** (§VI-E, Fig. 7, đường nét đứt):
- **Các tham số được ngoại suy:**
  - số UAV lên 4 (huấn luyện {1, 2, 3});
  - số cảm biến lên tới 14 (Fig. 7b, K ∈ [3, 14]);
  - dữ liệu mỗi cảm biến lên tới 25 (Fig. 7c);
  - thời gian bay ngoài khoảng huấn luyện (Fig. 7d, b₀ ∈ [50, 200]): tăng cho Manhattan32, giảm cho Urban50.
- **Kết luận của tác giả:**
  - Hiệu năng "theo cùng xu hướng" như trong khoảng huấn luyện.
  - Với 4 UAV, hiệu năng giảm nhẹ do tỉ lệ hạ cánh giảm.
  - Tác giả viết chính sách "có thể ngoại suy thành công" sang tham số ngoài phân phối.
- **Những dịch chuyển bài không thử** (suy ra từ §VI-A, §VI-C, §VI-D):
  - Không đổi bản đồ: mỗi tác nhân chỉ huấn luyện và đánh giá trên một bản đồ.
  - Không đổi kích thước vùng.
  - Không đổi **phân phối không gian** của cảm biến: luôn ngẫu nhiên đều trên ô trống, không có kịch bản phân cụm.
  - Không đổi mô hình năng lượng.

**Số seed / cách báo cáo độ bất định:**
- **Một tác nhân huấn luyện cho mỗi bản đồ.** Tác giả viết "all results discussed in the following are a result of only two trained agents" (§VI-A), tức thực chất 1 seed huấn luyện cho mỗi bản đồ.
- Bảng IV và Fig. 7 chỉ báo trung bình Monte Carlo trên kịch bản (1000 và 500 lần), không có CI, không có độ biến thiên giữa các lần huấn luyện.
- Fig. 4 có trung bình và quantile 99%, nhưng tính trên các episode trong một lần huấn luyện, gom theo bin 2e5 bước.
- Không có kiểm định thống kê.

**Đối chứng gần nhất và độ công bằng của so sánh:**
- Đối chứng duy nhất là các tác nhân DRL dùng đầu vào vô hướng (Fig. 4).
- **Không có heuristic** (TSP, greedy) và không có lời giải tối ưu hay cận trên để biết 88% tỉ lệ thu tốt đến đâu.
- **Không có đối chứng huấn luyện trên một kịch bản cố định.** §VI-B lập luận rằng so sánh đó "would not yield meaningful results". Vì vậy lợi ích của việc huấn luyện ngẫu nhiên so với huấn luyện cố định, khi đánh giá trên kịch bản mới, **chưa được đo** trong bài.

**Giới hạn đã biết:**
1. **Năng lượng hằng số theo bước, một tốc độ duy nhất** (PT (5), §II-A): bài không thể nói gì về đánh đổi tốc độ–năng lượng. Lập luận "≈10%, negligible" dựa trên mô hình [27] ở 10 m/s, không xét dải tốc độ.
2. **Mục tiêu dữ liệu thu một lần:** không áp dụng trực tiếp cho thu định kỳ hay AoI. Chính bài xếp nhóm AoI ([10]–[13]) vào loại công trình phải huấn luyện lại (§I-A, §I-B).
3. **1 lần huấn luyện mỗi bản đồ, không CI** (§VI-A).
4. **OOD chỉ là ngoại suy tham số** và chỉ đọc được qua đồ thị (Fig. 7); không có bảng số.
5. **Tác giả tuyên bố "the first"** về tổng quát hoá theo không gian tham số cho thu dữ liệu đa UAV (§I, §I-B). Đề tài **không** được viết "đầu tiên tổng quát hoá" (quy tắc 7, CLAUDE.md).
6. Môi trường đô thị cố định với kênh ray tracing phức tạp hơn đề tài, nên khó so số trực tiếp.

**Khác biệt với đề tài (điền thẳng vào ma trận docs/04 §5):**
- **Bayerlein 2021:** đa UAV (1–3), mục tiêu dữ liệu thu một lần, năng lượng hằng số theo bước với một tốc độ, randomization trên tham số kịch bản trong một bản đồ cố định, OOD chỉ là ngoại suy tham số, 1 lần huấn luyện mỗi bản đồ, đối chứng chỉ là DRL đầu vào vô hướng.
- **Đề tài:**
  - một UAV;
  - AoI trung bình nhiều chu kỳ;
  - năng lượng đẩy phụ thuộc tốc độ, chính sách chọn trong 2 tốc độ;
  - DR trên bố trí, mật độ và năng lượng;
  - 4 bộ OOD có cấu trúc, trong đó có dịch chuyển phân phối không gian (phân cụm) và diện tích;
  - ≥ 10 seed với CI;
  - đối chứng PPO-fixed, DQN và heuristic.
- **Đề tài dùng lại ý tưởng của bài:** quan sát bản đồ căn tâm (`docs/02` §6, [B21] §IV). Nên trích §IV-A và [1] của bài cho lý do căn tâm giúp học tốt hơn.
- **Đối chứng PPO-fixed của đề tài trả lời đúng câu §VI-B bỏ ngỏ.** Nên viết là "Bayerlein et al. did not compare against a policy trained on a fixed scenario", không viết là họ sai.

Hàng ma trận đề xuất (thay hàng hiện có):

| Công trình | Mục tiêu AoI | Năng lượng phụ thuộc tốc độ | Huấn luyện trên nhiều bố trí | Đánh giá OOD có cấu trúc | Nhiều seed + CI |
| --- | --- | --- | --- | --- | --- |
| Bayerlein 2021 | Không (dữ liệu thu một lần, PT (13)) | Không (pin −1/bước, một tốc độ V; PT (5), §II-A) | Có (số UAV, số/vị trí/dữ liệu cảm biến, thời gian bay, điểm xuất phát; bản đồ cố định; §VI-A) | Một phần (ngoại suy tham số I, K, D, b₀; không đổi phân phối không gian hay bản đồ; §VI-E, Fig. 7) | Không (1 lần huấn luyện mỗi bản đồ; trung bình Monte Carlo, không CI; §VI-A, Bảng IV) |

**Có mã nguồn/dữ liệu không:** Có: https://github.com/hbayerlein/uav_data_harvesting (chú thích trang 1 và §VI-A). Chưa kiểm tra mã có chạy được hay không.

**Một câu hỏi cho nhóm:** Câu định vị nháp ở `docs/01` §3 viết *"While parameter generalization has been shown for single-shot data harvesting [B21] …"*. Câu này khớp với §I-B và §VI-E của bài. Có nên thêm ý "without a fixed-scenario control or multiple training seeds" (§VI-A, §VI-B) không? Ý này là dữ kiện kiểm chứng được, và làm rõ đóng góp về giao thức đánh giá. Nhưng phải viết trung tính, không biến thành phê phán.
