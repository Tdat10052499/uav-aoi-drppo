# Form B — `zeng2019energy`

> Trạng thái: **DAT duyệt 26/10/2026**; soạn từ toàn văn PDF (arXiv:1804.02238v1, 31 trang, SHA256 `f071ace9…0e06160`, DAT tải và gửi ngày 26/10/2026). Second reader: LDN. Mọi số liệu lấy từ văn bản, phương trình và Bảng I; không có số nào đọc từ hình. Các số V_me, V_mr, P_h ghi dưới đây là **do nhóm tính** từ PT (6), (61) và Bảng I, bài không in các số này trong văn bản (chỉ vẽ ở Fig. 1).

**Tiêu đề / tác giả / năm / nơi công bố hoặc trạng thái preprint:** *Energy Minimization for Wireless Communication with Rotary-Wing UAV*.
- **Tác giả:** Yong Zeng, Jie Xu, Rui Zhang.
- **Trạng thái:** preprint arXiv:1804.02238v1 [cs.IT], 06/04/2018. Bản đăng IEEE Transactions on Wireless Communications 2019 ✱ (PDF v1 không ghi nơi đăng; thông tin số tập, trang chưa kiểm).

**URL nguồn gốc và phiên bản/ngày truy cập:** https://arxiv.org/abs/1804.02238 (v1), bản PDF DAT tải ngày 26/10/2026. Chưa đọc bản IEEE TWC chính thức.

**Người đọc (NICK):** DAT (nháp Claude)

**Bài báo trả lời câu hỏi gì:** Một UAV cánh quay phải thu/phát một lượng dữ liệu tối thiểu với mỗi nút mặt đất (GN). Làm sao chọn quỹ đạo, phân bổ thời gian truyền và tổng thời gian nhiệm vụ để **tổng năng lượng UAV** (đẩy + truyền thông) nhỏ nhất (Tóm tắt, bài toán (P1), PT (11)–(15)). Để làm được, bài **dẫn xuất mô hình công suất đẩy P(V) cho UAV cánh quay** (§II-B, Phụ lục A). Đây là phần đề tài dùng lại.

**Giả định hệ thống:**
- **Số UAV:** 1. **Số GN:** K tổng quát; mô phỏng dùng K = 3 (§V).
- **Không gian:** độ cao cố định H; quỹ đạo 2D liên tục q(t); điểm đầu q_I, điểm cuối q_F cho trước (PT (13)).
- **Kênh:** LoS thuần, suy hao không gian tự do: h_k(t) = β₀ / (H² + ‖q(t) − w_k‖²) (PT (1)). Tốc độ R_k = B log₂(1 + γ₀/(H² + ‖q − w_k‖²)) (PT (2)). Không có NLoS hay fading.
- **Truy nhập:** TDMA, mỗi thời điểm phục vụ tối đa một GN, λ_k(t) ∈ {0, 1} (PT (3), (14)).
- **Năng lượng:**
  - Tổng năng lượng = năng lượng đẩy ∫P(‖v(t)‖)dt (PT (9)) + P_c × thời gian **đang truyền** (PT (10)). P_c là hằng số (§II-B).
  - **Bỏ qua năng lượng do gia tốc.** Tác giả lý giải điều này hợp lệ khi thời gian cơ động chỉ chiếm phần nhỏ thời gian hoạt động (§II-B).
  - Bay ngang, không leo/hạ độ cao; giả định lực đẩy T ≈ W, tức κ ≈ 1 (Phụ lục A, sau PT (66)).
- **Mục tiêu:** **năng lượng**, với ràng buộc throughput Q̃_k cho mỗi GN (PT (11)). Đây là bài thu **một lần**: không có dữ liệu sinh định kỳ, không có AoI. Bài chỉ nhắc "data collection for periodic sensing" như một ứng dụng (§I).

**Cơ chế, diễn đạt bằng lời của mình:**
- **Mô hình công suất đẩy** (PT (6)):
  P(V) = P₀(1 + 3V²/U_tip²) + P_i(√(1 + V⁴/(4v₀⁴)) − V²/(2v₀²))^{1/2} + ½ d₀ρsAV³,
  với P₀ = (δ/8)ρsAΩ³R³ và P_i = (1 + k)W^{3/2}/√(2ρA) (PT (61)), v₀ = √(W/(2ρA)).
  - Ba thành phần: profile cánh quạt (tăng theo V²), cảm ứng (giảm theo V), ký sinh thân máy (tăng theo V³).
  - P(V) **không lồi, không lõm** theo V (§II-B). Khi V ≫ v₀ có xấp xỉ lồi PT (7).
  - P(V) **giảm rồi tăng** theo V: "hovering is in general not the most power-conserving status" (§II-B).
- **Hai tốc độ đặc trưng** (§II-B, PT (8)):
  - V_me = argmin P(V): bay được lâu nhất với năng lượng cho trước.
  - V_mr = argmin P(V)/V: bay được xa nhất với năng lượng cho trước (J/m nhỏ nhất).
  - "In practice, we usually have V_me ≤ V_mr ≤ V_max". Cả hai chỉ tìm được bằng số.
- **Giao thức fly–hover–communicate (FHC)** (§III):
  - UAV bay tới các điểm hover, chỉ truyền khi hover, mỗi điểm phục vụ một GN.
  - **Lemma 1:** trong FHC, đoạn bay tối ưu là bay với tốc độ không đổi V_mr. Chứng minh bị lược ("details are omitted for brevity").
  - Bài toán thứ tự thăm quy về TSP/TSPN, là NP-hard (P3). Vị trí hover tối ưu hoá bằng tối ưu lồi (Algorithm 1).
- **Thiết kế tổng quát** (§IV): cho phép truyền cả khi bay; rời rạc hoá đường bay theo đoạn (path discretization), giải bằng SCA (Algorithm 2), cho nghiệm tối ưu cục bộ.

**Bằng chứng mạnh nhất (mục/bảng/hình):**
- **Mô hình P(V) được dẫn xuất có căn cứ** (Phụ lục A, PT (61)–(66)), dựa trên giáo trình khí động học trực thăng (tham khảo [33], [34] của bài). Đây là bằng chứng lý thuyết, **không** phải đo thực nghiệm trên UAV thật.
- **§V, Fig. 3–4:** với FHC, tốc độ UAV chỉ có hai trạng thái: bay với V_mr hoặc hover. Với SCA tối thiểu năng lượng và Q̃ = 200 Mbit, UAV **bay vòng quanh GN với tốc độ nào đó thay vì hover ngay trên GN**; tác giả giải thích bằng việc hover không phải trạng thái tiết kiệm công suất nhất.
- **§V, Fig. 6:** FHC tối ưu luôn tốt hơn hai đối chứng (hover tại tâm hình học; hover trên từng GN). SCA cho "significant performance gains". Tối thiểu năng lượng trực tiếp cho tiết kiệm năng lượng hơn tối thiểu thời gian. **Văn bản không nêu con số phần trăm**; mọi so sánh định lượng chỉ có trên đồ thị.
- **Fig. 2:** Algorithm 2 hội tụ trong vài vòng lặp; cận trên lồi (P4.2) gần như trùng năng lượng thực (PT (43)).

**Đối chiếu với mã của đề tài** (`src/uavaoi/energy.py`, `channel.py`, `env.py`; tính lại ngày 26/10/2026 tại commit `1547bc4`):

| Đại lượng | Bài (Bảng I / PT) | Mã | Ghi chú |
| --- | --- | --- | --- |
| Công thức P(V) | PT (6) | `propulsion_power` | Khớp từng thành phần |
| P₀, P_i | PT (61) | `RotorParams.P0`, `.Pi` | Khớp |
| W, ρ, R, Ω, s, d₀, k, δ | 100; 1,225; 0,5; 400; 0,05; 0,3; 0,1; 0,012 | giống hệt | Khớp |
| A | 0,79 (A ≜ πR²) | 0,79 | πR² = 0,785; bài làm tròn, mã theo bài |
| U_tip = ΩR | 200 | 200,0 | Khớp |
| v₀ | 7,2 | 7,188 | Bài làm tròn |
| S_FP = d₀sA | 0,0118 | 0,01185 | Bài làm tròn |
| P₀ / P_i / P_h | không in số | 580,65 / 790,67 / 1371,3 W | Do nhóm tính |
| V_me / V_mr | không in số | 21,494 m/s (935,6 W) / 38,266 m/s (1199,5 W) | Do nhóm tính, lưới 0–60 m/s bước 0,001; thoả V_me ≤ V_mr ≤ V_max = 60 |
| Kênh, H, B, γ₀ | PT (1)–(2); 100 m; 1 MHz; 60 dB (§V) | `channel.rate_bps` | Khớp |
| P_c | 50 W, chỉ tính khi truyền (PT (10), §V) | `Pc = 50`; `env.step` cộng P_c chỉ khi hover **và** có cảm biến được phục vụ | Khớp với PT (10) |

- **Preset `light`** (W = 20, R = 0,4, A = 0,503, Ω = 300, d₀ = 0,6) **không có trong Bảng I của bản v1**. Không kiểm chứng được từ tài liệu đang có. `docs/02` đã đánh dấu bộ này [cần kiểm tra]; nhận định "trùng giá trị nhiều công trình sau trích dẫn" ở đó cũng chưa có nguồn.

**Đánh giá trên kịch bản khác tập huấn luyện? Loại dịch chuyển nào?** **Không áp dụng.** Bài là tối ưu tất định offline, không học. Lời giải được tính riêng cho một bố trí K = 3 cố định, với hai mức Q̃ (50 và 200 Mbit; Fig. 3–4) và một dải Q̃ (Fig. 6). Bố trí GN mới thì phải giải lại.

**Số seed / cách báo cáo độ bất định:** Không áp dụng: không có thành phần ngẫu nhiên; mỗi cấu hình cho một nghiệm. SCA chỉ đảm bảo tối ưu cục bộ (§IV), và kết quả phụ thuộc điểm khởi tạo (lấy từ nghiệm FHC, §V). Bài không báo độ nhạy theo khởi tạo.

**Đối chứng gần nhất và độ công bằng của so sánh:**
- Đối chứng: hover tại tâm hình học, hover trên từng GN (cả hai là trường hợp riêng của FHC với điểm hover cố định), và SCA tối thiểu thời gian (§V).
- So sánh công bằng về mô hình (cùng P(V), cùng kênh). Tuy nhiên chỉ có **một** bố trí GN, nên chưa rõ mức chênh lệch có giữ trên bố trí khác hay không.

**Giới hạn đã biết:**
1. **Bỏ qua gia tốc** (§II-B). Môi trường của đề tài đổi tốc độ tức thời giữa các khe, nên **nhất quán** với giả định này, nhưng cũng thừa hưởng giới hạn của nó: với khe 3 s và thay đổi tốc độ thường xuyên (V_me ↔ V_mr ↔ hover), năng lượng gia tốc bị bỏ qua có thể không còn nhỏ. Bài báo nên nêu điều này như một giới hạn.
2. **Mô hình lý thuyết, chưa kiểm chứng bằng đo bay thật** trong bài này; tham số Bảng I là giá trị mô phỏng, không phải của một UAV thương mại cụ thể.
3. **Kênh LoS thuần** (PT (1)), không NLoS hay shadowing; hợp với độ cao 100 m vùng thoáng, không hợp với đô thị dày.
4. **Một bố trí K = 3, không có tổng quát hoá.** Bài toán NP-hard (TSP) nên khó mở rộng ra K lớn và cập nhật online. Đây là lập luận hợp lý cho việc dùng chính sách học, nhưng bài không tự nêu hướng này.
5. **Lemma 1 không có chứng minh đầy đủ** (§III).

**Khác biệt với đề tài (điền thẳng vào ma trận docs/04 §5):**
- **Zeng 2019:** tối ưu tất định offline, mục tiêu năng lượng với ràng buộc throughput một lần, tốc độ là biến liên tục, một bố trí cố định.
- **Đề tài:** dùng **mô hình** P(V), kênh và tham số của bài, nhưng bài toán khác: AoI trung bình nhiều chu kỳ, chính sách học được, tốc độ rời rạc {hover, V_me, V_mr}, DR trên bố trí và đánh giá OOD.
- **Hệ quả thiết kế đáng nêu trong bài báo (dữ kiện từ mô hình, do nhóm tính):**
  - Hover không truyền tốn 1371,3 W, **cao hơn** bay ở V_me (935,6 W) và ở V_mr (1199,5 W).
  - Theo năng lượng/quãng đường, V_mr (31,3 J/m) rẻ hơn V_me (43,5 J/m).
  - Vậy trong môi trường, khi chưa có gì để thu, "bay chậm" rẻ hơn "đứng chờ". Đây đúng là hiện tượng Zeng quan sát ở Fig. 3(b)/4(b).
  - **Giả thuyết** (chưa kiểm): chính sách PPO sẽ học tránh hover không truyền và lượn quanh cụm cảm biến. Có thể kiểm bằng chỉ số `hover_frac` đã có trong `env.py`; cần ghi vào experiment card nếu muốn đưa thành nhận định.
- **Việc chọn V_me và V_mr làm hai mức tốc độ** của không gian hành động dựa trên định nghĩa ở §II-B, không phải trên một kết quả tối ưu của bài cho bài toán AoI. Lemma 1 chỉ nói V_mr tối ưu cho đoạn bay trong FHC với mục tiêu năng lượng. Bài báo nên viết là "two characteristic speeds defined in [Z19]", không viết là "optimal speeds".

Hàng ma trận đề xuất (thêm mới, đánh dấu là nguồn mô hình):

| Công trình | Mục tiêu AoI | Năng lượng phụ thuộc tốc độ | Huấn luyện trên nhiều bố trí | Đánh giá OOD có cấu trúc | Nhiều seed + CI |
| --- | --- | --- | --- | --- | --- |
| Zeng 2019 (nguồn mô hình, tối ưu tất định) | Không (năng lượng tối thiểu với throughput Q̃ một lần; PT (11)) | Có (P(V) PT (6), (61); FHC bay ở V_mr, Lemma 1) | Không (giải offline cho một bố trí K = 3; §V) | Không áp dụng (không học) | Không áp dụng (tất định; SCA tối ưu cục bộ) |

**Có mã nguồn/dữ liệu không:** PDF v1 không dẫn mã nguồn hay dữ liệu.

**Một câu hỏi cho nhóm:** Preset `light` không kiểm chứng được từ bản v1. Nhóm chọn cách nào?
- (a) Xoá `light` khỏi `PRESETS` và `docs/02` cho tới khi có nguồn. **Khuyến nghị**, vì mặc định `zeng2019_arxiv_v1` đã kiểm khớp và chưa thực nghiệm nào dùng `light`.
- (b) Giữ nhưng chỉ dùng sau khi ai đó đọc bản IEEE TWC chính thức và ghi số trang/bảng.
