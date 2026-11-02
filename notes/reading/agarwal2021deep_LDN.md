# Form B — `agarwal2021deep`

> Trạng thái: Claude soạn ngày 31/10/2026 theo yêu cầu của LDN, từ toàn văn bản HTML ar5iv của arXiv:2108.13264 (phần chính §1–§6; phụ lục chỉ dùng khi được phần chính dẫn tới). Người đọc: LDN (W1-LDN-02). Second reader: DAT.
> Bài này là **bài phương pháp thống kê**, không phải bài UAV. Các trường "giả định hệ thống" và "khác biệt với đề tài" được hiểu là: bài khuyến nghị gì, và nhóm áp dụng khuyến nghị nào trong `docs/03` §6 và `src/uavaoi/stats.py`. Bài không có hàng trong ma trận `docs/04` §5.

**Tiêu đề / tác giả / năm / nơi công bố hoặc trạng thái preprint:** *Deep Reinforcement Learning at the Edge of the Statistical Precipice*. Rishabh Agarwal, Max Schwarzer, Pablo Samuel Castro, Aaron Courville, Marc G. Bellemare (Google Research Brain Team, Mila). NeurIPS 2021, giải Outstanding Paper (ghi trên trang đầu). arXiv:2108.13264. Thư viện đi kèm: `rliable` (github.com/google-research/rliable).

**URL nguồn gốc và phiên bản/ngày truy cập:** https://arxiv.org/abs/2108.13264; toàn văn https://ar5iv.labs.arxiv.org/html/2108.13264 (ar5iv dựng từ bản arXiv mới nhất; số phiên bản không hiển thị ✱), truy cập 31/10/2026. Bản NeurIPS: liên kết PDF trong `docs/04` §1.

**Người đọc (NICK):** LDN

**Bài báo trả lời câu hỏi gì:** Khi mỗi thuật toán RL chỉ chạy được vài lần (3–10 lần huấn luyện), báo cáo một con số trung bình hay trung vị có đáng tin không, và nên báo cáo thế nào để kết luận không bị nhiễu ngẫu nhiên chi phối (§1, Bảng 1).

**Giả định / khung hình thức (thay cho "giả định hệ thống"):**
- Thuật toán được đánh giá trên M nhiệm vụ, mỗi nhiệm vụ N lần chạy độc lập; mỗi lần chạy cho một điểm chuẩn hoá x_{m,n} (§2).
- **Đơn vị lặp là lần chạy huấn luyện**, không phải episode đánh giá. Trong nghiên cứu tình huống, điểm của một lần chạy là trung bình lợi nhuận trên 100 episode đánh giá sau huấn luyện (§3).
- Một "lần chạy" không đồng nghĩa với cố định seed: cố định seed không kiểm soát được mọi nguồn ngẫu nhiên, ví dụ tính không tất định của GPU (§2, chú thích 2; §6).

**Cơ chế, diễn đạt bằng lời của mình:** Bài đưa ra ba công cụ cho chế độ ít lần chạy (§4, Bảng 1):
1. **Khoảng tin cậy bootstrap phân tầng (§4.1).** Lấy mẫu lại các lần chạy *có hoàn lại, độc lập trong từng nhiệm vụ*, tính chỉ số tổng hợp, lặp nhiều lần để có phân phối mẫu. Khoảng phân vị (percentile) cho độ phủ tốt từ N = 10 lần chạy với trung vị và IQM. Bootstrap trên **một** nhiệm vụ với N nhỏ thì kém tác dụng hơn, vì giả định "lấy mẫu lại xấp xỉ lấy mẫu từ phân phối thật" yếu khi chỉ có N điểm.
2. **Hồ sơ hiệu năng / phân phối điểm (§4.2).** Vẽ tỷ lệ lần chạy có điểm lớn hơn ngưỡng τ, kèm dải tin cậy bootstrap phân tầng. Cho thấy toàn bộ phân phối thay vì một con số; diện tích dưới đường tương ứng với trung bình.
3. **Chỉ số tổng hợp bền (§4.3).**
   - **IQM:** trung bình cắt 25% hai đầu của **toàn bộ** các lần chạy gộp qua nhiệm vụ (giữ ⌊NM/2⌋ giá trị). Bền với ngoại lai hơn trung bình, hiệu quả thống kê hơn trung vị.
   - **Optimality gap:** lượng điểm còn thiếu so với ngưỡng mục tiêu γ (mặc định 1,0).
   - **Xác suất cải thiện trung bình P(X > Y):** xác suất thuật toán X tốt hơn Y trên một nhiệm vụ chọn ngẫu nhiên; không đo độ lớn cải thiện.

**Bằng chứng mạnh nhất (mục/bảng/hình):**
- **Fig. 2 (trái), §3:** với 5–20 lần chạy như các bài đã công bố, trung vị báo cáo nằm rải trên một khoảng rộng khi lấy lại tập lần chạy khác; có cặp thuật toán bị đảo thứ tự so với kết luận gốc (DER so với OTR).
- **Fig. 2 (phải), §3:** CI của trung vị vẫn rộng ở 50 lần chạy; CI của IQM hẹp hơn nhiều.
- **Fig. 3, §3:** trung vị mẫu là ước lượng chệch; độ chệch giữa 5 và 100 lần chạy của SPR bằng khoảng 36% mức cải thiện nó tuyên bố.
- **Fig. 4, §3:** để phát hiện cải thiện cho trước, IQM cần ít lần chạy hơn trung vị.
- **Fig. 5, §3:** đổi giao thức đánh giá (lấy điểm tối đa trong huấn luyện thay vì điểm cuối) giải thích phần lớn cải thiện được tuyên bố của CURL và SUNRISE.
- **Fig. 6, §4.1:** khoảng phân vị đạt độ phủ gần danh nghĩa 95% từ 10 lần chạy (bootstrap phân tầng trên 26 trò chơi); với 3 lần chạy, CI bootstrap hẹp hơn thật.
- **§5, Fig. 9–12:** áp dụng lại cho ALE, DM Control, Procgen; nhiều tuyên bố cải thiện có CI chồng lấn lớn; một số cải thiện chỉ có xác suất 50–70%.

**Đánh giá trên kịch bản khác tập huấn luyện? Loại dịch chuyển nào?** Không áp dụng (bài phương pháp). Procgen (một bộ đánh giá tổng quát hoá) chỉ được dùng làm ví dụ phân tích lại (§5, Fig. 12).

**Số seed / cách báo cáo độ bất định:** Đây là chủ đề của bài. Khuyến nghị: luôn báo khoảng tin cậy; ưu tiên CI và cỡ hiệu ứng, **tránh kết luận nhị phân "có ý nghĩa / không ý nghĩa" theo p < 0,05** (§2, Remark). Khi hai CI chồng lấn, tính CI của **hiệu** giữa hai thuật toán (chú thích Fig. 2).

**Đối chứng gần nhất và độ công bằng của so sánh:** Bài nhấn mạnh giữ **cùng giao thức đánh giá** cho mọi thuật toán: điểm cuối huấn luyện, không lấy điểm tốt nhất trong quá trình huấn luyện (§3, Fig. 5).

**Giới hạn đã biết:**
1. Kiểm chứng độ phủ CI (Fig. 6) làm trên bootstrap **phân tầng qua 26 nhiệm vụ**. Bài không chứng minh độ phủ tốt cho CI bootstrap trên **một** nhiệm vụ với N = 10; chính bài nói trường hợp này kém tác dụng hơn (§4.1).
2. Các ngưỡng số lần chạy (50–100 cho trung vị) là của Atari 100k, nơi độ biến thiên rất lớn; không suy trực tiếp ra bài toán khác.
3. Bài khuyên tránh kiểm định ý nghĩa nhị phân nhưng không đề xuất quy tắc ra quyết định thay thế cho nghiên cứu cần đăng ký trước.

**Khác biệt với đề tài → khuyến nghị nào nhóm áp dụng** (đối chiếu `docs/03` §3, §6 và `src/uavaoi/stats.py`):

| Khuyến nghị của Agarwal 2021 | Đề tài | Ghi chú |
| --- | --- | --- |
| Đơn vị lặp là lần chạy huấn luyện, không phải episode (§2, §3) | **Áp dụng.** `docs/03` (đoạn mở đầu), `stats.py` docstring | Mỗi seed là trung bình trên 100 episode đánh giá, đúng như §3 của bài |
| Báo khoảng tin cậy, không chỉ điểm (§4.1) | **Áp dụng.** `docs/03` §6: trung bình kèm 95% CI bootstrap | `bootstrap_ci` là percentile bootstrap, 10 000 lần, đúng loại khoảng bài khuyên |
| Bootstrap **phân tầng** qua nhiệm vụ (§4.1) | **Chưa.** CI hiện tính riêng cho từng bộ đánh giá (một "nhiệm vụ", N = 10 seed) | Với CI riêng từng bộ, bài không bảo đảm độ phủ (giới hạn 1). Nếu báo một chỉ số gộp qua 4 bộ OOD, phải dùng bootstrap phân tầng (lấy lại seed trong từng bộ) |
| IQM (§4.3) | **Áp dụng.** `docs/03` §6; `stats.iqm` | `stats.iqm` giữ x[⌊0,25n⌋ : ⌈0,75n⌉]; Đã kiểm 31/10: kết quả trùng `scipy.stats.trim_mean(x, 0.25)` với n = 5, 10, 20, 40. Với chỉ số gộp, bài tính IQM trên **mọi lần chạy gộp qua nhiệm vụ** |
| Cỡ hiệu ứng, xác suất cải thiện (§4.3) | **Áp dụng gián tiếp.** Cliff's δ (`docs/03` §6) | δ = P(X > Y) − P(X < Y), nên có thể đổi ra xác suất cải thiện: P(X > Y) = (1 + δ)/2 khi không có giá trị bằng nhau. Có thể báo thêm con số này cho dễ đọc |
| Tránh kết luận nhị phân theo p-value (§2) | **Áp dụng một phần.** H1 dùng kiểm định hoán vị + Holm, α = 0,05, quy tắc "≥ 3/4 bộ có ý nghĩa" | Lệch có chủ đích: nghiên cứu đăng ký trước cần quy tắc quyết định. Bù lại bằng việc luôn báo CI và Cliff's δ cạnh p (`docs/03` §6). Nên ghi lý do lệch này trong PREREG |
| CI của **hiệu** khi CI chồng lấn (chú thích Fig. 2) | **Chưa** | Đề xuất cho W2-LDN-02/W5-LDN-01: báo CI bootstrap của deg(DR) − deg(Fixed) trên từng bộ OOD |
| Hồ sơ hiệu năng / phân phối điểm (§4.2) | **Chưa** | Có thể làm hình phụ: phân phối deg theo seed cho DR và Fixed trên mỗi bộ; cân nhắc cho F4 |
| Cùng giao thức đánh giá, dùng điểm cuối huấn luyện (§3) | **Áp dụng.** `train_ppo.py` lưu `model.zip` khi kết thúc huấn luyện; `evaluate.py` đánh giá file đó | Không chọn checkpoint tốt nhất theo OOD (`docs/03` §3 cấm tinh chỉnh trên OOD) |
| Số lần chạy: 3–10 phổ biến; CI phân vị ổn từ khoảng 10 (§1, §4.1) | **Áp dụng.** 10 seed cho kết quả chính; MVP tối thiểu 5 seed ghi là sơ bộ (`docs/03` §3) | Với 5 seed, CI kém tin cậy hơn; pilot 2 seed chỉ mô tả, đúng tinh thần bài (Fig. 6: 3 lần chạy đã làm CI hẹp hơn thật) |
| Công bố mọi lần chạy riêng lẻ (§6) | **Áp dụng.** `results/raw/` chỉ ghi thêm, có run record | |
| Cố định seed không thay được nhiều lần chạy (§6) | **Áp dụng.** Seed huấn luyện 0–9 là 10 lần chạy độc lập, không phải để "tái lập một kết quả đẹp" | |

**Có mã nguồn/dữ liệu không:** Có. Thư viện `rliable` (PyPI) và toàn bộ lần chạy riêng lẻ của bài (§6).

**Một câu hỏi cho nhóm:** Theo §4.1, CI bootstrap trên **một** bộ đánh giá với 10 seed không được bài kiểm chứng độ phủ. Có nên (a) giữ CI từng bộ nhưng nêu giới hạn này trong Setup, và (b) thêm một chỉ số gộp qua 4 bộ OOD (IQM của deg trên 40 cặp seed–bộ, CI bootstrap phân tầng theo bộ) làm kết quả tóm tắt, dùng thẳng `rliable` hoặc tự cài trong `stats.py` (W2-LDN-02) không? Phải chốt trước khi khoá PREREG ở G1.
