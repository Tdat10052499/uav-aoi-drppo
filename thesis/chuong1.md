# Chương 1. Cơ sở lý thuyết

> **BẢN NHÁP W11-FAO-01, viết sớm ngày 22/10/2026 (FAO).** Second reader: DAT.
>
> - Chương này chỉ trình bày kiến thức nền. Mô hình cụ thể của đề tài (tham số, MDP, hàm thưởng) thuộc Chương 3 (`docs/02`).
> - Không có số liệu thực nghiệm nào trong chương.
> - Trích dẫn dùng khoá trong `paper/references.bib`. Khoá có đánh dấu ✱ chưa kiểm thông tin xuất bản (`note = {VERIFY}`).
> - Tài liệu kinh điển cho chương này (sutton2018reinforcement, mnih2015human, schulman2016high, holm1979simple, cliff1993dominance) được thêm vào `references.bib` ngày 23/10/2026. mnih2015human và cliff1993dominance đã đối chiếu Crossref; ba khoá còn lại có `note = {VERIFY}` (✱).

## 1.1. UAV trong thu thập dữ liệu IoT

### 1.1.1. Bài toán
- Trong nhiều ứng dụng giám sát (môi trường, nông nghiệp, cảnh báo sớm), cảm biến IoT được đặt ở vùng không có hạ tầng viễn thông mặt đất.
- Một UAV có thể bay tới gần từng cảm biến để nhận dữ liệu. Nhờ khoảng cách ngắn và đường truyền thường là tầm nhìn thẳng (LoS), cảm biến chỉ cần công suất phát thấp.
- Bài toán đặt ra gồm hai quyết định gắn chặt với nhau:
  - **quỹ đạo:** bay đi đâu, với tốc độ nào;
  - **lập lịch:** khi nào phục vụ cảm biến nào.
- Cả hai bị giới hạn bởi năng lượng pin của UAV.
- Ở dạng tổng quát, bài toán là tối ưu tổ hợp phi lồi. Nhiều biến thể chứa bài toán người du lịch (TSP) làm trường hợp riêng~[sun2025aoi, §III-F].

### 1.1.2. Giao thức bay – dừng – truyền
Giao thức *fly–hover–communicate* [zeng2019energy ✱, §III]:
- UAV bay giữa các điểm dừng và chỉ truyền nhận khi đang hover.
- Ưu điểm: tách chuyển động khỏi truyền thông, nên lập lịch và tính năng lượng đơn giản hơn.
- Nhược điểm: bỏ qua khả năng thu dữ liệu trong lúc bay.

### 1.1.3. Mô hình năng lượng đẩy của UAV cánh quay
Theo Zeng, Xu và Zhang [zeng2019energy ✱, PT (6)], công suất đẩy của UAV cánh quay bay ngang với tốc độ V là:

$$
P(V)=P_0\left(1+\frac{3V^2}{U_{tip}^2}\right)+P_i\left(\sqrt{1+\frac{V^4}{4v_0^4}}-\frac{V^2}{2v_0^2}\right)^{1/2}+\frac{1}{2}d_0\rho s A V^3
$$

Ba số hạng lần lượt là:
1. **công suất profile của cánh**, tăng theo V²;
2. **công suất cảm ứng**, giảm khi V tăng;
3. **công suất cản thân**, tăng theo V³.

Các hằng số:
- $P_0$ và $P_i$ là công suất profile và công suất cảm ứng khi hover;
- $U_{tip}$ là tốc độ đầu cánh;
- $v_0$ là vận tốc cảm ứng trung bình khi hover;
- $d_0, \rho, s, A$ lần lượt là tỷ số cản thân, mật độ không khí, độ đặc rotor và diện tích đĩa rotor.

Khi V = 0, công suất hover là $P_h = P_0 + P_i$.

Hai hệ quả quan trọng cho đề tài [zeng2019energy ✱, §II-B]:
- **P(V) không đơn điệu.** Tồn tại tốc độ **V_me** = argmin P(V), cho thời gian bay dài nhất với cùng năng lượng. Hover vì vậy **không** phải trạng thái tiết kiệm công suất nhất.
- **Năng lượng trên mỗi mét có cực tiểu riêng.** Tốc độ **V_mr** = argmin P(V)/V cho quãng đường dài nhất với cùng năng lượng, và V_me ≤ V_mr.

Hệ quả: nếu mô hình năng lượng là hằng số mỗi bước, chính sách không có lý do gì để chọn tốc độ. Khi P(V) phụ thuộc tốc độ, lựa chọn tốc độ trở thành một phần của bài toán. Đây là lý do đề tài đưa tốc độ vào không gian hành động (Chương 3).

### 1.1.4. Kênh truyền tầm nhìn thẳng
Với UAV ở độ cao H, vị trí ngang **q**, và cảm biến tại **w**, kênh LoS suy hao không gian tự do cho tốc độ truyền [zeng2019energy ✱, PT (1)–(2)]:

$$
R=B\log_2\left(1+\frac{\gamma_0}{H^2+\lVert\mathbf q-\mathbf w\rVert^2}\right)
$$

trong đó B là băng thông và $\gamma_0$ là SNR tham chiếu ở khoảng cách 1 m.

Mô hình này bỏ qua che khuất. Mô hình xác suất LoS theo góc ngẩng [alhourani2014optimal] là mở rộng thường gặp, nhưng đề tài không dùng (xem mục giới hạn, Chương 5).

## 1.2. Tuổi thông tin (Age of Information)

### 1.2.1. Định nghĩa
Tuổi thông tin (AoI) [kaul2012realtime ✱] đo độ "tươi" của thông tin mà bên nhận có về một nguồn. Nếu bản cập nhật mới nhất mà bên nhận có được sinh ở thời điểm u(t), thì AoI tại thời điểm t là:

$$
\Delta(t)=t-u(t).
$$

AoI tăng tuyến tính theo thời gian giữa hai lần cập nhật, và giảm xuống khi một bản cập nhật mới tới, tạo dạng răng cưa.

### 1.2.2. Dạng rời rạc
Trong mô hình thời gian rời rạc theo khe, gói được sinh ngay khi được yêu cầu (*generate-at-will*), nên AoI về 1 khi nguồn được phục vụ. Nếu không được phục vụ, AoI tăng thêm 1 mỗi khe và bão hoà ở mức trần $\Delta_{\max}$:

$$
\Delta_n(t+1)=\begin{cases}1,&\text{nguồn } n \text{ được phục vụ ở khe } t\\ \min\big(\Delta_n(t)+1,\Delta_{\max}\big),&\text{ngược lại.}\end{cases}
$$

Abd-Elmagid và cộng sự dùng dạng này với UAV [abdelmagid2019deep, PT (6)].

### 1.2.3. Chỉ số
- **AoI trung bình theo thời gian và nguồn:** $\bar\Delta = \frac{1}{TN}\sum_t\sum_n \Delta_n(t)$. Phản ánh độ tươi chung của toàn mạng.
- **Peak AoI:** giá trị AoI lớn nhất trước mỗi lần cập nhật, hoặc lớn nhất trên chân trời. Phản ánh trường hợp xấu nhất; Sun và cộng sự dùng chỉ số này làm mục tiêu [sun2025aoi].
- **Điểm khác với thông lượng và độ trễ:** để giảm AoI, phải cập nhật **đều** các nguồn. Phục vụ dồn một nguồn gần UAV không đủ.
- **Liên hệ với quỹ đạo:** mục tiêu AoI vì vậy tự nhiên dẫn tới quỹ đạo tuần hoàn qua các cảm biến.

## 1.3. Quá trình quyết định Markov

### 1.3.1. Định nghĩa
Một quá trình quyết định Markov (MDP) là bộ $(\mathcal S,\mathcal A,P,r,\gamma)$, gồm:
- tập trạng thái $\mathcal S$ và tập hành động $\mathcal A$;
- xác suất chuyển $P(s'\mid s,a)$;
- hàm thưởng $r(s,a)$;
- hệ số chiết khấu $\gamma\in[0,1]$.

Tính Markov: trạng thái kế tiếp chỉ phụ thuộc trạng thái và hành động hiện tại.

Chính sách $\pi(a\mid s)$ là phân phối xác suất trên hành động tại mỗi trạng thái. Mục tiêu là tìm chính sách làm cực đại lợi ích kỳ vọng:

$$
J(\pi)=\mathbb E_\pi\Big[\sum_{t=0}^{T-1}\gamma^t r_t\Big].
$$

### 1.3.2. Hàm giá trị và phương trình Bellman
Các hàm giá trị:
- hàm giá trị trạng thái $V^\pi(s)$;
- hàm giá trị hành động $Q^\pi(s,a)$;
- hàm lợi thế $A^\pi(s,a)=Q^\pi(s,a)-V^\pi(s)$.

$Q^\pi$ thoả phương trình Bellman:

$$
Q^\pi(s,a)=r(s,a)+\gamma\,\mathbb E_{s'\sim P,\,a'\sim\pi}\big[Q^\pi(s',a')\big].
$$

Chính sách tối ưu thoả phương trình Bellman tối ưu, thay kỳ vọng theo $a'$ bằng $\max_{a'}$.
[sutton2018reinforcement ✱]

### 1.3.3. Quan sát không đầy đủ
- Khi tác tử không thấy toàn bộ trạng thái, bài toán là MDP quan sát một phần (POMDP).
- Trong thực hành DRL, thường xấp xỉ bằng cách đưa vào mạng một quan sát giàu thông tin, ví dụ bản đồ lưới căn tâm theo tác tử [bayerlein2021multi], hoặc thêm bộ nhớ hồi quy (LSTM) [sun2025aoi].

### 1.3.4. Hành động không hợp lệ
Ở một số trạng thái, có những hành động không hợp lệ, ví dụ bay ra ngoài vùng. Có hai cách xử lý:
1. **Cho phép rồi sửa lại:** hành động vẫn được thực hiện, nhưng vị trí bị kẹp tại biên và tác tử bị phạt. Tác tử phải tự học tránh những hành động này.
2. **Che hành động (action masking):** đặt xác suất của hành động không hợp lệ bằng 0 trước khi lấy mẫu. Huang và Ontañón [huang2022closer ✱] phân tích cách che này trong policy gradient và cho thấy gradient vẫn hợp lệ với phân phối đã che.

Thư viện sb3-contrib cài đặt cách 2 dưới tên MaskablePPO.

## 1.4. Từ học tăng cường tới học tăng cường sâu

### 1.4.1. Học tăng cường
- Học tăng cường (RL) tìm chính sách tốt bằng tương tác với môi trường, không cần biết trước P và r.
- Hai họ chính:
  - **Dựa trên giá trị:** học $Q$, rồi chọn hành động tham lam theo $Q$.
  - **Dựa trên chính sách:** tối ưu trực tiếp tham số θ của $\pi_\theta$ theo gradient của $J$.
- **Actor-critic** kết hợp hai họ: actor là chính sách, critic ước lượng giá trị để giảm phương sai của gradient.

### 1.4.2. Học tăng cường sâu
Học tăng cường sâu (DRL) dùng mạng nơ-ron làm hàm xấp xỉ cho $Q$, $V$ hoặc $\pi$. Nhờ vậy RL áp dụng được cho không gian trạng thái lớn, như ảnh hay bản đồ lưới. Với quan sát dạng lưới, mạng tích chập (CNN) là lựa chọn tự nhiên vì khai thác cấu trúc không gian.

### 1.4.3. Deep Q-Network (DQN)
DQN học $Q_\phi$ bằng cách tối thiểu sai số Bellman trên các mẫu lấy từ bộ nhớ phát lại (replay buffer):

$$
\mathcal L(\phi)=\mathbb E\Big[\big(r+\gamma\max_{a'}Q_{\bar\phi}(s',a')-Q_\phi(s,a)\big)^2\Big],
$$

trong đó $Q_{\bar\phi}$ là mạng đích, được cập nhật chậm. Khám phá theo ε-greedy.
[mnih2015human]

Đặc điểm:
- DQN là thuật toán **off-policy** nên dùng lại mẫu cũ, nhưng cần bộ nhớ phát lại lớn.
- Abd-Elmagid và cộng sự dùng DQN cho bài toán AoI–UAV [abdelmagid2019deep]. Bayerlein và cộng sự dùng biến thể double DQN [bayerlein2021multi].

### 1.4.4. Gradient chính sách và ước lượng lợi thế
Định lý gradient chính sách cho:

$$
\nabla_\theta J=\mathbb E\big[\nabla_\theta\log\pi_\theta(a_t\mid s_t)\,\hat A_t\big].
$$

Ước lượng lợi thế tổng quát (GAE) cân bằng giữa độ chệch và phương sai qua tham số λ_GAE:

$$
\hat A_t=\sum_{l\ge0}(\gamma\lambda_{GAE})^l\,\delta_{t+l},\qquad \delta_t=r_t+\gamma V(s_{t+1})-V(s_t).
$$

[schulman2016high ✱]

> **Lưu ý ký hiệu:** λ_GAE khác với trọng số năng lượng λ trong hàm thưởng của đề tài (Chương 3).

## 1.5. Proximal Policy Optimization (PPO)

### 1.5.1. Hàm mục tiêu cắt
PPO [schulman2017proximal ✱] là thuật toán actor-critic **on-policy**. Gọi $\rho_t(\theta)=\pi_\theta(a_t\mid s_t)/\pi_{\theta_{old}}(a_t\mid s_t)$ là tỷ số xác suất giữa chính sách mới và chính sách thu mẫu. PPO tối ưu hàm mục tiêu cắt:

$$
L^{CLIP}(\theta)=\mathbb E_t\Big[\min\big(\rho_t(\theta)\hat A_t,\ \mathrm{clip}(\rho_t(\theta),1-\epsilon,1+\epsilon)\hat A_t\big)\Big].
$$

Phép cắt bỏ động lực đẩy $\rho_t$ ra khỏi khoảng $[1-\epsilon,1+\epsilon]$. Nhờ vậy có thể cập nhật nhiều epoch trên cùng một lô dữ liệu mà chính sách không thay đổi quá xa.

### 1.5.2. Hàm mất mát đầy đủ
Hàm mất mát đầy đủ cộng thêm hai thành phần:
- sai số của critic, $c_1(V_\theta(s_t)-\hat V_t)^2$;
- thưởng entropy, $c_2\,\mathcal H[\pi_\theta(\cdot\mid s_t)]$, để duy trì khám phá.

### 1.5.3. Vì sao chọn PPO cho đề tài
- Ổn định với siêu tham số mặc định, và phổ biến trong các bài thu dữ liệu UAV gần đây [sun2025aoi].
- Kết hợp được trực tiếp với action masking (MaskablePPO).
- Chạy song song nhiều môi trường dễ dàng.

Đánh đổi: PPO on-policy nên cần nhiều mẫu hơn các thuật toán off-policy. Vì vậy đề tài giữ DQN làm đối chứng thuật toán (RQ3).

## 1.6. Tổng quát hoá và domain randomization

### 1.6.1. Trong phân phối và ngoài phân phối
- Gọi $\mathcal D_{train}$ là phân phối các kịch bản (bố trí cảm biến, số cảm biến, ngân sách năng lượng…) dùng khi huấn luyện.
- Chính sách **tổng quát hoá trong phân phối** (ID) nếu hoạt động tốt trên kịch bản mới rút từ chính $\mathcal D_{train}$.
- Chính sách **tổng quát hoá ngoài phân phối** (OOD) nếu vẫn hoạt động tốt khi kịch bản đến từ phân phối khác.
- Cách đo đề tài dùng (Chương 4, `docs/03` §5): độ suy giảm tương đối giữa hiệu năng trên bộ OOD và trên bộ ID của **cùng** một chính sách,

$$
\mathrm{deg}(s)=\frac{\bar\Delta(s)-\bar\Delta(\mathrm{id})}{\bar\Delta(\mathrm{id})}.
$$

### 1.6.2. Huấn luyện trên một kịch bản cố định
Nhiều công trình DRL cho UAV huấn luyện và đánh giá trên cùng một bố trí cố định [abdelmagid2019deep, sun2025aoi]. Khi bố trí thay đổi, chính sách thường phải huấn luyện lại. Bayerlein và cộng sự chỉ ra hạn chế này và huấn luyện trên dải tham số kịch bản [bayerlein2021multi].

### 1.6.3. Domain randomization
Domain randomization (DR) [tobin2017domain ✱]:
- mỗi episode, tham số môi trường được rút ngẫu nhiên từ một phân phối rộng;
- tác tử buộc phải học chiến lược không phụ thuộc một cấu hình cụ thể.

DR ban đầu dùng để chuyển chính sách từ mô phỏng sang thực tế. Liu [liu2024generalizable] dùng DR cho đua drone: sinh lại đường đua mới mỗi rollout. Kết quả là tỷ lệ thành công giảm dần khi đường đua thử lệch xa phân phối huấn luyện.

Giới hạn đã biết: DR chủ yếu đảm bảo hiệu năng **trong vùng được ngẫu nhiên hoá**. Ngoại suy ra ngoài vùng đó không được bảo đảm. Đây chính là câu hỏi mà các bộ OOD có cấu trúc của đề tài được thiết kế để kiểm tra.

### 1.6.4. Biểu diễn quan sát bất biến theo số cảm biến
Để một mạng xử lý được số cảm biến thay đổi, quan sát phải có kích thước cố định. Hai lựa chọn phổ biến:
1. **Vector có đệm** tới số cảm biến tối đa: phụ thuộc thứ tự cảm biến, và không mở rộng quá mức tối đa.
2. **Bản đồ lưới:** mỗi ô chứa thông tin tổng hợp của các cảm biến trong ô.

Bản đồ lưới **căn tâm** theo vị trí tác tử [bayerlein2021multi] có thêm tính bất biến tịnh tiến, nên CNN học được quy tắc cục bộ dùng chung cho mọi vị trí. Đề tài dùng lựa chọn 2, và kiểm vai trò của nó bằng ablation A2/A3 (H3).

## 1.7. Đánh giá thống kê trong DRL

### 1.7.1. Đơn vị lặp
Kết quả DRL dao động mạnh giữa các lần huấn luyện với seed khác nhau. Vì vậy:
- **đơn vị lặp độc lập là seed huấn luyện**;
- các episode đánh giá của cùng một model **không** phải mẫu độc lập.

### 1.7.2. Khuyến nghị khi số lần chạy ít
Khi chỉ có ít lần chạy, Agarwal và cộng sự [agarwal2021deep] khuyến nghị:
- báo cáo khoảng tin cậy bootstrap;
- dùng **IQM** (trung bình liên tứ phân vị, bỏ 25% thấp nhất và 25% cao nhất), vì IQM bền hơn trung bình và hiệu quả hơn trung vị;
- không chỉ báo một con số điểm.

### 1.7.3. Công cụ kiểm định đề tài dùng (`src/uavaoi/stats.py`)
- **Kiểm định hoán vị:** hoán vị nhãn nhóm nhiều lần để có phân phối của thống kê dưới H0. Không giả định phân phối chuẩn, nên phù hợp cỡ mẫu nhỏ (n = 10).
- **Hiệu chỉnh Holm:** kiểm soát sai số loại I theo họ khi kiểm nhiều giả thuyết (4 bộ OOD). Holm mạnh hơn Bonferroni mà vẫn giữ cùng mức kiểm soát.
  [holm1979simple ✱]
- **Cliff's δ:** cỡ hiệu ứng phi tham số, bằng P(X > Y) − P(X < Y), nằm trong [−1, 1].
  [cliff1993dominance]
- **Phân biệt kiểm định và thăm dò:** giả thuyết khẳng định phải đăng ký trước (PREREG); mọi phân tích ngoài đăng ký chỉ là thăm dò và được báo cáo như vậy.

## 1.8. Tóm tắt chương

Chương 1 trình bày:
- mô hình năng lượng đẩy phụ thuộc tốc độ, cho thấy tốc độ là một biến quyết định có ý nghĩa;
- AoI, là thước đo độ tươi đòi hỏi cập nhật đều;
- MDP, DRL, cùng hai thuật toán đề tài dùng là PPO (có action masking) và DQN;
- domain randomization, cách đo tổng quát hoá ID/OOD và các công cụ thống kê cho số lần chạy ít.

Chương 2 rà soát các công trình đã kết hợp những thành phần này, và chỉ ra phần còn để ngỏ mà đề tài nhắm tới.
