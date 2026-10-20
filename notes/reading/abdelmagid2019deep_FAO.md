# Form B — `abdelmagid2019deep`

> Trạng thái: soạn từ toàn văn PDF (arXiv v2). FAO rà lại trước khi đánh dấu W2-FAO-01 xong; second reader: LDN.

**Tiêu đề / tác giả / năm / nơi công bố hoặc trạng thái preprint:** *Deep Reinforcement Learning for Minimizing Age-of-Information in UAV-assisted Networks*. M. A. Abd-Elmagid, A. Ferdowsi, H. S. Dhillon, W. Saad (Wireless@VT, Virginia Tech), 2019. Bản đã đọc là arXiv:1905.02993v2 [cs.IT], 18/08/2019. Nơi công bố là IEEE GLOBECOM 2019 ✱; thông tin này lấy từ `paper/references.bib`, vì PDF arXiv không ghi hội nghị.

**URL nguồn gốc và phiên bản/ngày truy cập:** https://arxiv.org/abs/1905.02993 (v2), truy cập ngày 20/10/2026.

**Người đọc (NICK):** FAO

**Bài báo trả lời câu hỏi gì:** Bài tìm cách chọn đồng thời quỹ đạo của một UAV và lịch truyền gói cập nhật từ các nút mặt đất có pin hữu hạn, sao cho tổng AoI có trọng số nhỏ nhất trong khoảng thời gian bay τ (§I "Contributions", §III-A, PT (7)–(8)).

**Giả định hệ thống:**
- **UAV và không gian:** một UAV bay ở độ cao cố định h = 100 m. Vùng 1100 × 1100 m được chia thành lưới 11 × 11 ô, mỗi ô 100 m (§II-A, §IV).
- **Hành động:** mỗi slot UAV đi một ô theo {N, S, E, W} hoặc đứng yên I (PT (2)). Đồng thời UAV chọn tối đa một nút được truyền, w(n) ∈ {0, …, M} (§II-B).
- **Kênh:** LoS thuần, g = β₀/d² (PT (1)).
- **Năng lượng:** chỉ mô hình hoá năng lượng của **nút mặt đất**. Pin được chia thành lượng tử, và chi phí truyền tính theo công thức Shannon (PT (3)–(5)). UAV **không có mô hình năng lượng đẩy**. Giới hạn pin của UAV chỉ thể hiện qua ràng buộc thời gian τ, với ô xuất phát và ô kết thúc cố định (§II-A).
- **Mục tiêu:** tổng AoI có trọng số trên chân trời τ (PT (7)). Gói được sinh khi cần (generate-at-will). AoI về 1 khi nút được phục vụ, nếu không thì tăng và bão hoà ở A_max (PT (6)).
- **Quy mô mô phỏng:** M ≤ 3 nút (§IV).

**Cơ chế, diễn đạt bằng lời của mình:**
- **Mô hình hoá:** bài toán là MDP chân trời hữu hạn. Trạng thái gồm (mức pin, AoI) của từng nút cùng (vị trí UAV, thời gian còn dư so với thời gian cần để về đích) (§II-B).
- **Thuật toán:** không gian trạng thái quá lớn để giải bằng DP, nên tác giả dùng DQN.
  - Mạng có một lớp fully connected 200 nút, dùng replay memory, ε-greedy và γ = 1 vì bài toán theo episode.
  - Hành động là tổ hợp di chuyển × lập lịch (§III-B, Alg. 1, Fig. 2).
  - Trọng số được cập nhật một lần sau mỗi episode, trên một batch b mẫu (Alg. 1, dòng 13–17).
- **Lý thuyết:** Định lý 1 cho cận trên và cận dưới của tổng chi phí khi các nút đồng nhất (PT (9)–(10)).

**Bằng chứng mạnh nhất (mục/bảng/hình):**
- **Fig. 5b** (kịch bản 4, τ từ 10 đến 100): theo tác giả, sum-AoI trung bình của DRL nhỏ hơn khoảng 50% so với chính sách theo khoảng cách và khoảng 75% so với random walk (§IV-C).
- **Fig. 3b** (kịch bản 2, τ = 16): UAV vòng lên phía bắc để phục vụ hai nút rồi quay về đường thẳng. Đây chỉ là minh hoạ định tính (§IV-B).
- **Fig. 4:** sum-AoI hội tụ sau 50 000 episode huấn luyện ở kịch bản 1 (§IV-A).

**Đánh giá trên kịch bản khác tập huấn luyện? Loại dịch chuyển nào?** Không.
- Mỗi kịch bản 1–5 có vị trí nút cố định (Fig. 3).
- Các biến thiên e_max, τ và mật độ nút (Fig. 5a–c) là quét tham số; mỗi điểm trên hình là một cấu hình riêng.
- Bài không nói rõ có huấn luyện lại cho từng cấu hình hay không. Cách trình bày gợi ý mỗi cấu hình được huấn luyện riêng, nhưng đây là suy luận, không phải dữ kiện.

**Số seed / cách báo cáo độ bất định:**
- Số liệu là sum-AoI trung bình trên 1000 episode (§IV, đoạn đầu).
- Bài không báo số seed huấn luyện, và Fig. 4–5 không có thanh lỗi hay khoảng tin cậy.

**Đối chứng gần nhất và độ công bằng của so sánh:**
- **Hai heuristic được dùng (§IV-C):**
  - *distance-based:* cập nhật nút gần nhất nếu nút đó cách dưới 2 ô, đồng thời di chuyển về phía nút có AoI lớn nhất;
  - *random walk.*
- **Đối chứng yếu:**
  - Random walk chỉ là cận tầm thường.
  - Distance-based không tính đến ràng buộc thời gian τ hay ô đích.
- **Những gì bài không làm:**
  - Không so với lời giải DP tối ưu. Ở kịch bản 1–2 (1–2 nút) không gian có thể đủ nhỏ để giải đúng; đây là suy luận.
  - Không so với heuristic quy hoạch đường đi.
  - Không có thông tin tinh chỉnh tham số cho các đối chứng.

**Giới hạn đã biết:**
- Quy mô rất nhỏ (≤ 3 nút, lưới 11 × 11).
- Không có năng lượng đẩy của UAV, kênh chỉ là LoS, và tốc độ cố định ở một ô mỗi slot.
- Không có số seed hay CI, và không công bố mã.
- Câu "đầu tiên áp dụng deep RL để tìm chính sách age-optimal" (§I) là tuyên bố của chính tác giả vào năm 2019.

**Khác biệt với đề tài (điền thẳng vào ma trận docs/04 §5):**
- **Điểm chung:** AoI tổng (có trọng số), lưới rời rạc, AoI về 1 khi được phục vụ và bão hoà ở mức trần (giống PT (6) và `env.py`), hành động lập lịch thu.
- **Khác biệt:**
  - Đề tài có năng lượng đẩy phụ thuộc tốc độ (Zeng 2019), và chọn tốc độ nằm trong hành động.
  - Đề tài huấn luyện trên phân phối bố trí (DR) và đánh giá trên 4 bộ OOD với 10 seed + CI.
  - Abd-Elmagid chỉ có năng lượng phía nút cùng ràng buộc thời gian phía UAV, và một bố trí cố định cho mỗi kịch bản.
- **Cách dùng:** đối chứng khái niệm trong Related Work, tức DRL cho AoI–UAV trên một bố trí cố định.

Hàng ma trận đề xuất:

| Công trình | Mục tiêu AoI | Năng lượng phụ thuộc tốc độ | Huấn luyện trên nhiều bố trí | Đánh giá OOD có cấu trúc | Nhiều seed + CI |
| --- | --- | --- | --- | --- | --- |
| Abd-Elmagid 2019 | Có (tổng AoI có trọng số) | Không (UAV chỉ bị ràng buộc thời gian τ; năng lượng là pin của nút) | Không (vị trí nút cố định mỗi kịch bản) | Không (chỉ quét e_max, τ, mật độ) | Không (TB 1000 episode, không seed/CI) |

**Có mã nguồn/dữ liệu không:** Không thấy liên kết mã hay dữ liệu trong bài. Bài chỉ nêu dùng TF-Agents và GPU NVIDIA P100 (§IV).

**Một câu hỏi cho nhóm:** `GreedyAoIPolicy` của ta gần với chính sách distance-based của bài (phục vụ nút trong tầm, đi về nút có AoI lớn). Có nên nêu sự tương ứng này trong phần baseline, để reviewer thấy baseline có tiền lệ trong tài liệu không?
