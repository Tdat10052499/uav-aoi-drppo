# Thiết kế phương pháp: PG-TG-PPO (Physics-Grounded, Tour-Guided PPO)

> **Nháp.** Claude soạn ngày 06/11/2026 theo lựa chọn của DAT: "Gộp A + B (tour-guided)".
> **Chưa ai duyệt.** Trước khi viết mã, FAO (môi trường) và LDN (thống kê) cần đọc.
> **Cơ sở:**
> - báo cáo rà soát tài liệu 2023–2026 (Claude Doc của DAT, chưa đưa vào repo; DAT gửi link khi cần) (phương án A, B);
> - mã tại `main` (`src/uavaoi/env.py`, `baselines.py`, `scenarios.py`).
>
> Chỗ nào ghi "giả thuyết" là chưa kiểm. Chỗ nào ghi ✱ là cần xác minh trong mã hoặc thư viện.

## 1. Vì sao cần phương pháp này (dữ kiện → giả thuyết)

### Dữ kiện từ EXP-03 (10 seed, đã khoá)

| Đại lượng | id | ood_energy |
|---|---|---|
| Ā của DR-PPO | 52,2 | 147,6 |
| Ā của TSP | 28,6 | 60,5 |
| Ā của Random | 126,2 | 133,9 |

- Trên `ood_area`, PPO chỉ thu hẹp được 14% khoảng cách từ Random tới TSP.
- Trên `ood_energy`, PPO kém hơn cả Random.

### Dữ kiện từ mã nguồn

- **Kênh năng lượng chuẩn hoá theo ngân sách.** Quan sát dùng kênh 3 = E/E_max (`env.py` dòng 204), nên mọi episode đều bắt đầu ở giá trị 1,0.
- **Kích thước ô thay đổi theo vùng.** Ô lưới = L/16 (`env.py` dòng 191).
- **TRAIN_DR giữ L cố định.** L luôn bằng 1000 m (`docs/PREREG.md` §3).
- **TSP bay nhanh khi còn xa mục tiêu.** `TSPPolicy` dùng `_move_towards`, hàm này chọn V_mr khi khoảng cách > V_mr·δt (`baselines.py` dòng 18). TSP vì vậy không tiết kiệm năng lượng.

### Giả thuyết G1: quan sát che ngữ cảnh

Policy không biết ngân sách pin tuyệt đối và tỉ lệ không gian, nên không thể điều chỉnh hành vi theo chúng (conflict state, Benjamins et al.).

### Giả thuyết G2: học di chuyển từng ô là bài toán khó không cần thiết

PPO phẳng phải tự học định tuyến từng ô, trong khi TSP giải phần này gần tối ưu. Học cả hai cùng lúc có thể là lý do PPO thua TSP ngay trên `id`.

### Giả thuyết G3: chỗ một policy học được có thể thắng TSP

Vì TSP không biết tiết kiệm pin, một policy biết chọn tốc độ, bỏ qua điểm, chờ hoặc rẽ khỏi tour có thể thắng TSP khi ngân sách pin thấp.

Phương pháp gộp hai thành phần: **A** đánh vào G1, **B** đánh vào G2 và G3.

## 2. Thành phần A: quan sát neo vật lý

Mục tiêu: hai ngữ cảnh khác nhau về E_max hoặc L phải cho **quan sát khác nhau** khi hành động tối ưu khác nhau. Đồng thời, ngữ cảnh OOD phải rơi vào vùng giá trị đã gặp khi huấn luyện, càng nhiều càng tốt.

| Đặc trưng | Hiện tại | Neo vật lý (đề xuất) |
|---|---|---|
| Kích thước ô | L/16 (đổi theo vùng) | **cố định 62,5 m** (= 1000/16, nên ở L = 1000 m bản đồ giống hệt hiện tại) |
| Cửa sổ | 31×31 căn tâm UAV | giữ 31×31; cảm biến ngoài cửa sổ dồn lên ô biên theo hướng |
| Kênh năng lượng | E / E_max | **ρ_E = (E / e_Vme) / (T − t)**, cắt [0, 2]. e_Vme là năng lượng một khe bay ở V_me (công suất thấp nhất). ρ_E = 1 nghĩa là "vừa đủ bay tới hết chu kỳ". |
| Kênh thời gian | **đã có** (kênh 4, `env.py`; sửa 06/11, bản trước ghi nhầm "không có") | giữ nguyên (T − t)/T |

Hệ quả kiểm được: ở L = 1000 m, mọi kênh trừ kênh năng lượng giống hệt quan sát cũ. Cần một kiểm thử đơn vị cho điều này.

**Mệnh đề cần viết** (cho phần phương pháp, LDN hoặc DAT chứng minh): nếu hai kịch bản chỉ khác nhau ở E_max, thì tại mọi trạng thái có cùng (vị trí, AoI, năng lượng tuyệt đối còn lại, t), quan sát neo cho hai kịch bản là như nhau. Khi đó policy không cần biết E_max ban đầu, vì động lực học từ trạng thái đó trở đi giống nhau. Quan sát cũ không có tính chất này, vì nó chia cho E_max. Mệnh đề tương tự cho L cần giả thiết vùng đủ rộng so với cửa sổ (✱ cần phát biểu cẩn thận).

## 3. Thành phần B: PPO tầng cao trên nền tour

Bài toán quyết định được chuyển thành semi-MDP: mỗi quyết định là một **macro-action** kéo dài nhiều khe.

### Điểm quyết định

Có ba loại điểm quyết định:
- lúc bắt đầu episode;
- sau mỗi lần thu xong dữ liệu;
- sau một hành động "chờ".

### Hành động: Discrete(2K + 2), có mask, với K = 5 ứng viên

**Ứng viên c₁…c₅:**
- c₁: điểm kế tiếp trên tour TSP (tính lúc reset, như `TSPPolicy`);
- c₂: điểm sau c₁ trên tour;
- c₃–c₅: ba cảm biến có tỉ số AoI / thời gian bay cao nhất, không trùng c₁ và c₂.

**Hành động:**
- (cᵢ, V_me) hoặc (cᵢ, V_mr): bay thẳng tới cᵢ ở tốc độ đã chọn, hover thu một lần khi vào tầm r_eff (env tự phục vụ cảm biến có AoI cao nhất trong tầm), rồi kết thúc macro-action;
- "chờ 1 khe": hover, không bay;
- "kết thúc sớm có chủ đích": tuỳ chọn, ✱ cân nhắc bỏ.

**Mask:** che ứng viên không còn đủ năng lượng để tới và thu.

### Tầng thấp

Bay tất định, dùng lại `_move_towards`, nhưng **ép tốc độ đã chọn** chứ không tự chuyển nhanh/chậm.

### Phần thưởng

Lấy tổng phần thưởng từng khe của env trong suốt macro-action, nên mục tiêu AoI + λ·năng lượng không đổi.

Chiết khấu: lý tưởng là γ^τ, với τ là số khe của macro-action. SB3/sb3-contrib không hỗ trợ chiết khấu thay đổi theo bước ✱. Có hai cách làm, nhóm phải chọn và ghi vào card trước khi chạy:
- (a) cộng dồn có chiết khấu bên trong wrapper và dùng γ cố định cho mỗi quyết định;
- (b) chỉ cộng dồn, không chiết khấu bên trong.

### Quan sát

Dict gồm hai phần:
- bản đồ neo vật lý (thành phần A), qua SmallCNN;
- vector đặc trưng ứng viên, kích thước K × 4: thời gian bay tới ứng viên tính theo khe ở V_me, AoI/Δmax, năng lượng cần / năng lượng còn, và cờ "đúng điểm tour".

Cần MaskablePPO với `MultiInputPolicy` ✱ (kiểm xem sb3-contrib bản đang dùng có hỗ trợ không).

### Điểm khác với các bài lai đã xem (OH-DRL, HDRL-TSRAM, TWA\*)

Tầng học không chỉ chọn thứ tự. Nó còn chọn **nhịp tiêu năng lượng**: tốc độ, chờ, bỏ qua điểm. Tất cả trong bối cảnh AoI nhiều chu kỳ, có năng lượng phụ thuộc tốc độ, và đánh giá zero-shot dưới dịch chuyển có cấu trúc. Theo rà soát, chưa thấy bài nào làm như vậy.

**Đối chiếu arXiv 2611.03884** (Gao, Moltafet, Sadjadpour, "Timely Ground-Station Status Delivery via UAV-Assisted Data Collection and Hierarchical RL", Asilomar 2026, bản accepted manuscript; có bản tạp chí [15] chưa đọc ✱). Claude đọc toàn văn 5 trang do DAT gửi ngày 06/11.

**Bài này đã làm:**
- **Kiến trúc HAE-AC.** Tầng trên là actor PPO chọn hướng di chuyển trong 5 lựa chọn (B/N/Đ/T/hover), giữ hướng tối đa μ = 10 khe. Mỗi ứng viên được chấm điểm qua một vector đặc trưng gồm khe, năng lượng UAV, khoảng cách, AoI (§III-B). Tầng dưới là bộ lập lịch tất định cho thu/chuyển tiếp và công suất.
- **Mask theo năng lượng quay về.** Chỉ cho các hướng còn đủ năng lượng bay về depot ("return-feasible").
- **Năng lượng và tốc độ.** Có mô hình đẩy cánh quay, nhưng **tốc độ cố định** 15 m/s (Bảng I).
- **Huấn luyện theo curriculum.** (N, cạnh vùng, T) = (25, 1000 m, 300) → (50, 1400 m, 600) → (100, 2000 m, 1200), tức là có huấn luyện qua nhiều diện tích.
- **Seed.** 3 seed huấn luyện, báo mean ± std. Không có CI.
- **Baseline.** Distance-greedy, ASG (heuristic theo độ cũ), SL-AC. **Không có TSP.**
- **Thử không huấn luyện lại.** Theo N ∈ {25, …, 150} (§IV-A). Một phép thử kết hợp: cụm + T = 600 + pin 130 kJ (§IV-B). Chính tác giả ghi đây là "combined robustness test rather than a test of spatial generalization alone".
- **Kết quả.** −22,5% AoI so với ASG (151,2 so với 195,1 khe).

**Hệ quả cho tính mới của nhóm:**
- **Thu hẹp.** Mẫu "tầng trên học di chuyển + tầng dưới tất định" cho UAV–AoI đã có: bài này, và [13] trong bài. Ý đưa khoảng cách tuyệt đối và năng lượng UAV vào đặc trưng ứng viên, kèm mask năng lượng, cũng đã có. Bài của nhóm **phải trích** bài này và không được trình bày "lai/phân tầng" như điểm mới tự thân.
- **Còn đứng được** (trong các bài đã xem):
  - tầng học chọn **mục tiêu trên nền tour TSP và tốc độ** (nhịp tiêu năng lượng), thay vì chọn hướng ở tốc độ cố định;
  - so với **TSP, TSP-eco, TSP-adaptive** và ablation tầng cao greedy;
  - thử zero-shot **tách riêng từng trục** (pin, diện tích, cụm, mật độ), cùng bộ OOD mới khoá trước. Bài này chỉ có một phép thử gộp;
  - thiết kế 2×2 tách tác dụng của DR và của quan sát neo;
  - 10 seed kèm CI.
- **Câu định vị nên đổi.** Không viết "đề xuất kiến trúc phân tầng". Viết: "chúng tôi kiểm có kiểm soát *khi nào* một policy phân tầng có quan sát neo vật lý tổng quát hoá zero-shot theo từng trục dịch chuyển, và so với heuristic tour mạnh".

## 4. Baseline: phải công bằng, kể cả với TSP mạnh hơn

Nếu chỉ so với TSP hiện tại (luôn bay nhanh khi xa), reviewer sẽ nói chỉ cần cho TSP bay V_me là đủ. Vì vậy cần thêm baseline:

| Baseline | Mô tả | Cần huấn luyện? |
|---|---|---|
| Random, Greedy-AoI, TSP | như EXP-01 | không |
| **TSP-eco** | TSP nhưng luôn bay V_me | không (sửa nhỏ `baselines.py`, qua PR) |
| **TSP-adaptive** | TSP chọn V_mr khi ρ_E > 1 và V_me khi ρ_E ≤ 1 (quy tắc tay) | không |
| **Tầng cao greedy** | cùng ứng viên, cùng tầng thấp, nhưng chọn ứng viên có tỉ số AoI/thời gian bay lớn nhất | không. Đây là ablation tách phần đóng góp của tầng học. |
| Flat PPO, quan sát cũ (EXP-03) | DR và Fixed, 10 seed | không (tái dùng checkpoint) |

Nếu PG-TG-PPO không thắng được TSP-adaptive và tầng cao greedy, bài không có tuyên bố "DRL thắng heuristic". Khi đó bài vẫn còn phần cơ chế (A). Phải ghi rõ trước điều này.

## 5. Các nhánh huấn luyện và chi phí

| Nhánh | Phân phối | Quan sát | Tầng | Seed | Mục đích |
|---|---|---|---|---|---|
| **M1 (chính)** | DR | neo | tour-guided | 10 (10–19) | Phương pháp đề xuất |
| M2 | Fixed | neo | tour-guided | 10 | Tác dụng của DR |
| M3 | DR | cũ (tương đối) | tour-guided | 10 | Tác dụng của quan sát neo |
| M4 | DR | neo | phẳng (17 hành động) | 10 | Tác dụng của tầng tour |
| (tái dùng) | DR / Fixed | cũ | phẳng | 10 + 10 | EXP-03 |

Ước tính máy:
- Nhánh phẳng M4: khoảng 15 giờ cho 10 seed × 2M bước (đo ở EXP-03).
- Nhánh tour-guided: mỗi episode chỉ có khoảng 50–100 quyết định thay vì 300 bước, nhưng mỗi quyết định mô phỏng nhiều khe. Số bước cần và tốc độ thực tế chưa biết ✱, phải đo ở pilot. Ước tính tạm 8–12 giờ mỗi nhánh.
- **Tổng ≈ 40–55 giờ**, cộng pilot khoảng 4 giờ, cộng baseline (vài phút).

Số đo thời gian chính thức chỉ lấy từ máy DAT (quy tắc 4).

## 6. Bộ đánh giá

- **Bộ cũ (phụ, để so với EXP-03):** id, ood_cluster, ood_density, ood_area, ood_energy, giữ nguyên seed 100000–100099.
- **Bộ mới, khoá trước, chưa ai chạy (chính):**
  - `ood_energy_low`: E_max 0,35–0,45 MJ;
  - `ood_area_2000`: L = 2000 m ✱ (kiểm xem T = 300 có đủ không);
  - `ood_combo`: cụm + E_max 0,5–0,7 MJ.

  Seed đánh giá mới: 300000–300099.

Lý do có bộ mới: các ý tưởng ở đây sinh ra từ việc xem số EXP-03. Kiểm trên bộ chưa ai thấy là cách bảo vệ mạnh nhất chống HARKing.

## 7. Thứ tự làm (chưa phải lịch; DAT chốt qua `tasks.json`)

1. **Chẩn đoán miễn phí**, cần DAT push `results/raw/EXP-03` trước: `early_termination`, `hover_frac`, tỉ lệ chậm/nhanh theo bộ và nhánh. Nếu trên `ood_energy` PPO hết pin sớm nhiều hơn TSP, G1 được củng cố.
2. **Đọc 3 bài** có thể trùng: arXiv 2611.03884, Bayerlein 2021 (b₀ có nằm trong quan sát không), Theile ~2020 "Varying Power Constraints".
3. **Duyệt bản thiết kế** này, card EXP-08 và PREREG phụ lục B (FAO, LDN).
4. **PR mã**, đều qua nhánh và second reader:
   - `obs_mode` trong `env.py` (FAO);
   - wrapper `src/uavaoi/options.py`;
   - TSP-eco, TSP-adaptive và greedy-high-level trong `baselines.py`;
   - kiểm thử.
5. **Pilot:** 2 seed × M1, M4, chỉ mô tả; đo tốc độ; áp dụng tiêu chí dừng ghi trong card.
6. **Khoá PREREG phụ lục B** (tag mới), rồi chạy M1–M4 trên seed 10–19.
7. Phân tích, claim–evidence, second reader.
