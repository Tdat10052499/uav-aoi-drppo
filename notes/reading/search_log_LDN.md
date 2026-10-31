# Nhật ký tìm kiếm hệ thống Q1–Q3 (W1-LDN-04, W1-LDN-05)

> Owner: LDN · Second reader: DAT · Giao thức: `docs/04` §6.
> Trạng thái: **NHÁP chờ LDN duyệt.** Claude chạy truy vấn trên Chrome của LDN và soạn sàng lọc ngày 31/10/2026. Mọi quyết định giữ/loại dưới đây là đề xuất; LDN đọc lại trước khi đánh dấu W1-LDN-04/05 xong. Các thay đổi so với giao thức (mục 1, 2) cần DAT đồng ý: xem `notes/yeu-cau/2026-10-31_ldn_can-DAT_tim-kiem-q1-q3.md`.

## 1. Cơ sở dữ liệu và khả năng truy cập (31/10/2026)

| CSDL theo giao thức | Truy cập | Xử lý |
| --- | --- | --- |
| IEEE Xplore | **Không.** Trang chủ và trang tìm kiếm đều hiện trang lỗi trên Chrome của LDN, kể cả khi không đăng nhập | Thay bằng OpenAlex (bên dưới). Bài IEEE vẫn có trong OpenAlex và Google Scholar |
| Scopus | **Không.** Trường không đăng ký; tài khoản cá nhân của LDN chỉ mở Scopus Preview (tra tác giả, nguồn), không có tìm kiếm tài liệu | Thay bằng OpenAlex |
| arXiv | Có (API công khai) | Chạy đủ Q1–Q3 |
| Google Scholar | Có (không đăng nhập) | Chạy đủ Q1–Q3; chỉ sàng lọc 100 kết quả đầu mỗi truy vấn |
| *OpenAlex (thay thế, ngoài giao thức)* | Có (API công khai, không khoá API) | Chạy đủ Q1–Q3, tìm trong tiêu đề + tóm tắt |

**Khoảng thời gian:** 2018–2026. **Ngày tìm:** 31/10/2026 (giờ Việt Nam).

## 2. Chuỗi truy vấn đã chạy

Chuỗi gốc ở `docs/04` §6. Điều chỉnh chung: không CSDL nào ở đây xử lý đúng ký tự đại diện `generaliz*`, nên thay bằng `generalization OR generalize OR generalizable OR generalizing OR generalized OR generalizes OR generalisation OR generalise` (Scholar: bốn dạng đầu cùng `generalizable`).

**arXiv** (`export.arxiv.org/api/query`, trường `abs:`, `submittedDate:[201801010000 TO 202612312359]`):
```
Q1: (abs:UAV OR abs:UAVs OR abs:drone OR abs:drones) AND (abs:"age of information" OR abs:AoI)
    AND abs:"reinforcement learning" AND (abs:generalization OR … OR abs:"domain randomization"
    OR abs:unseen OR abs:"out-of-distribution" OR abs:meta)
Q2: (abs:UAV OR … ) AND (abs:"data collection" OR abs:"data harvesting") AND abs:"reinforcement learning"
    AND (abs:"variable number of sensors" OR abs:"scenario parameters" OR abs:"map-based")
Q3: (abs:UAV OR abs:UAVs) AND abs:"age of information" AND (abs:"propulsion energy" OR abs:"rotary-wing")
    AND (abs:PPO OR abs:"proximal policy")
```
Kiểm tra: viết `generaliz*` nguyên văn thì Q1 chỉ ra 5 bài (so với 13), xác nhận API không mở rộng ký tự đại diện. Thêm `UAVs`, `drones` không đổi số kết quả (API đưa về từ gốc).

**OpenAlex** (`api.openalex.org/works`, `filter=publication_year:2018-2026,title_and_abstract.search:<chuỗi>`): cùng chuỗi Boolean như trên, bỏ tiền tố trường. OpenAlex tự đưa về từ gốc (`stemmed`).

**Google Scholar** (lọc năm 2018–2026, 20 kết quả/trang, 5 trang mỗi truy vấn):
```
Q1: ("UAV" OR "drone") ("age of information" OR "AoI") "reinforcement learning"
    (generalization OR generalize OR generalizable OR "domain randomization" OR unseen OR "out-of-distribution" OR meta)
Q2: ("UAV" OR "drone") ("data collection" OR "data harvesting") "reinforcement learning"
    ("variable number of sensors" OR "scenario parameters" OR "map-based")
Q3: "UAV" "age of information" ("propulsion energy" OR "rotary-wing") ("PPO" OR "proximal policy")
```

## 3. Số kết quả

| Truy vấn | arXiv (mọi chuyên mục) | arXiv (chỉ cs.NI, cs.LG, eess.SP) | OpenAlex | Google Scholar (ước lượng) | Scholar đã sàng lọc | IEEE Xplore | Scopus |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Q1 | 13 | 6 | 14 | khoảng 2 830 | 100 | — | — |
| Q2 | 4 | 4 | 8 | khoảng 1 580 | 100 | — | — |
| Q3 | 0 | 0 | 1 | khoảng 274 | 100 | — | — |

- arXiv: số dùng cho PRISMA là cột "mọi chuyên mục". Lọc chuyên mục đúng như giao thức sẽ loại 2 bài liên quan trực tiếp (2311.06742, cs.IT; 2502.01268, cs.RO).
- OpenAlex có bản trùng nội bộ (bản preprint và bản tạp chí của cùng bài): Q1 14 bản ghi ứng với 10 bài, Q2 8 bản ghi ứng với 5 bài.
- Scholar tìm trên toàn văn và sắp theo mức liên quan, nên chỉ 100 kết quả đầu mỗi truy vấn được sàng lọc. Đây là giới hạn của tìm kiếm, ghi trong chương 2.

## 4. PRISMA rút gọn

| Bước | Số bản ghi |
| --- | --- |
| Bản ghi nhận vào sàng lọc: arXiv 17 + OpenAlex 23 + Scholar 300 | 340 |
| Loại trùng (so tiêu đề đã chuẩn hoá; AAV coi như UAV) | 61 |
| Bản ghi duy nhất được sàng lọc | ≈ 279 |
| Loại ở bước tiêu đề (rõ ràng ngoài phạm vi: MEC/offloading, xe/vệ tinh/AUV, điều hướng, tổng quan, sách, luận văn) | ≈ 187 |
| Loại ở bước tóm tắt/đoạn trích (mã E1–E3, mục 6) | 30 |
| Đã có trong ma trận `docs/04` §5 trước tìm kiếm (Bayerlein 2021, Abd-Elmagid 2019, Sun 2025, OH-DRL 2025, Lamenza 2026) | 5 |
| **Giữ để đọc toàn văn** | **57** (nhóm A 9, B 12, C 36; trong đó A9 Sarathchandra 2025 đã có hàng ma trận nhưng còn ô "Chưa rõ") |

Yi 2020 (`yi2020deep`, đã có trong ma trận) không xuất hiện trong kết quả Q1–Q3 vì tóm tắt không có từ khoá tổng quát hoá; vẫn phải đọc theo W1-LDN-02.

Dấu ≈: loại trùng bằng so tiêu đề có thể sót bản ghi trùng có tiêu đề khác hẳn (ví dụ một bản ghi Scholar bị cắt tiêu đề). LDN kiểm lại khi duyệt.

## 5. Tiêu chí chọn/loại (`docs/04` §6) và mã dùng ở đây

**Chọn:** UAV thu dữ liệu từ cảm biến/thiết bị mặt đất; có DRL; và có **(I1)** đánh giá trên kịch bản khác tập huấn luyện, **hoặc (I2)** AoI + năng lượng đẩy của UAV.
**Loại:** chỉ tối ưu lồi/heuristic; chỉ điều khiển bay mức thấp.

| Mã | Ý nghĩa |
| --- | --- |
| E1 | Không phải UAV thu dữ liệu từ cảm biến mặt đất (UAV tự cảm biến, chuyển tiếp, MEC, học liên kết, …) |
| E2 | Không dùng DRL (tối ưu, heuristic, giải tích, LLM, mạng nơ-ron có giám sát) |
| E3 | Có UAV + DRL nhưng tóm tắt/đoạn trích không cho thấy I1 hay I2 |

**Nhóm giữ lại** (mức ưu tiên đọc):
- **A:** có AoI hoặc năng lượng UAV **và** có dấu hiệu đánh giá ngoài phân phối / tổng quát hoá. Đây là các bài có thể làm tiêu chí G0 số 2 không đạt; đọc toàn văn và viết Form B **trước G0 (04/11)**.
- **B:** có dấu hiệu tổng quát hoá theo tham số kịch bản nhưng không có AoI (hoặc chưa rõ).
- **C:** có AoI + năng lượng đẩy (I2) nhưng chưa thấy đánh giá ngoài phân phối. Cần cho cột "năng lượng phụ thuộc tốc độ" và "nhiều seed + CI".

## 6. Sàng lọc tóm tắt/đoạn trích

Nguồn: AX = arXiv, OA = OpenAlex, GS = Scholar (`GS-Q1-10` = Q1, kết quả thứ 10). Nhận định dựa trên tóm tắt (AX, OA) hoặc đoạn trích Scholar (GS); chưa đọc toàn văn.

### 6.1 Giữ — nhóm A (đọc trước G0)

| # | Bài | Nguồn | Lý do |
| --- | --- | --- | --- |
| A1 | Gong et al., *UAV-Aided Lifelong Learning for AoI and Energy Optimization in Nonstationary IoT Networks*, IEEE IoT-J 2024 (arXiv 2312.00334) | AX Q1, OA Q1, GS-Q1-2 | AoI + năng lượng; tối ưu cả quỹ đạo **và vận tốc bay** của UAV; đánh giá trên môi trường chưa thấy (zero-shot). Rủi ro trùng định vị cao nhất |
| A2 | Yi et al., *Meta-RL for Timely and Energy-efficient Data Collection in Solar-powered UAV/AAV-assisted IoT Networks*, arXiv 2311.06742 (2023); bản tạp chí IEEE Trans. 2025 ✱ | AX, OA, GS-Q1-59 | AoI + năng lượng UAV; meta-RL để tăng khả năng tổng quát hoá |
| A3 | Lu et al., *Attention-Enhanced Prompt Decision Transformers for UAV/AAV-Assisted Communications with AoI*, IEEE WCL 2025 (arXiv 2505.22170) | AX, OA | AoI dưới ràng buộc năng lượng dài hạn; số người dùng thay đổi; thích nghi kịch bản mới (Decision Transformer, học ngoại tuyến) |
| A4 | Chen, Liu, Zhang, Hanzo, *Learning-Aided UAV-Cooperation Reduces the Age-of-Information in Wireless Networks*, IEEE Commun. Lett. 2024 | GS-Q1-10, OA (tra tiêu đề) | Năng lượng UAV + AoI; MARL; đoạn trích nói có thử khả năng tổng quát hoá bằng vị trí sinh ngẫu nhiên |
| A5 | Toure et al., *Optimizing Energy and Data Collection in UAV-aided IoT Networks using Attention-based MORL*, IEEE IoT-J 2026 (arXiv 2601.14092) | AX Q2, OA Q2, GS-Q2-7 | Năng lượng + thu dữ liệu (không AoI); nêu rõ mục tiêu tổng quát hoá ngoài phân phối huấn luyện, thử trên kịch bản chưa thấy |
| A6 | Xiao, Yi, Wang et al., *Meta-learning DRL for Fresh Data Collection in UAV-assisted WSNs*, hội nghị 2024 ✱ | GS-Q1-11 | AoI; meta-learning; cảm biến dịch chuyển sau thảm hoạ (thay đổi bố trí). Năng lượng: chưa rõ |
| A7 | Zhou et al., *Population-Invariant MADRL for AoI-Aware UAV Trajectory Design and Communication Scheduling in WSNs*, IEEE IoT-J 2024 | GS-Q1-26, OA (tra tiêu đề) | AoI; chuyển chính sách giữa các bài toán có số UAV và số cảm biến khác nhau (HyperQMIX). Năng lượng: chưa rõ |
| A8 | Eldeeb, Alves, *Resilient UAV/AAV Trajectory Planning via Few-Shot Meta-Offline RL*, IEEE TMLCN 2026 (arXiv 2502.01268) | AX, OA, GS-Q1-21 | AoI + công suất phát; thích nghi môi trường chưa thấy bằng MAML |
| A9 | Sarathchandra et al., *Age and Power Minimization via Meta-Deep RL in UAV/AAV Networks*, IEEE TVT 2025 (arXiv 2501.14603) | AX, OA, GS-Q1-1 | Đã có trong ma trận, còn ô "Chưa rõ" (W2-LDN-01). AoI + công suất phát; meta theo hàm mục tiêu |

### 6.2 Giữ — nhóm B

| # | Bài | Nguồn | Lý do |
| --- | --- | --- | --- |
| B1 | Bayerlein et al., *UAV Path Planning for Wireless Data Harvesting: A DRL Approach*, GLOBECOM 2020 (arXiv 2007.00544) | AX, OA, GS-Q2-1 | Tiền thân của Bayerlein 2021; tổng quát hoá theo tham số kịch bản |
| B2 | Theile et al., *UAV Path Planning using Global and Local Map Information with DRL*, ICAR 2021 (arXiv 2010.06917) | AX, OA, GS-Q2-5 | Mở rộng tổng quát hoá theo tham số kịch bản (cùng nhóm Bayerlein) |
| B3 | Seong, Jo, Shin, *Multi-UAV Trajectory Optimizer: A Sustainable System for Wireless Data Harvesting with DRL*, EAAI 2023 | OA Q2, GS-Q2-3 | Đoạn trích: chính sách tổng quát hoá theo nhiều tham số kịch bản; có sạc |
| B4 | Abualhayja'a et al., *Efficient Data Harvesting in Urban IoT Networks: DRL for RIS-UAV Communications*, IEEE TVT 2025 | GS-Q2-8 | Đoạn trích: thích nghi khi tham số kịch bản thay đổi. Không AoI |
| B5 | Pan et al., *GNN-Empowered Effective Partial Observation MARL for AoI Management in Multi-UAV Network*, IEEE IoT-J 2024 | GS-Q1-14 | AoI; GNN + QMIX cho kịch bản chưa biết trước. Cần kiểm "unknown scenario" có phải OOD |
| B6 | Shukla, Shukla, *QoS-Aware UAV Service Scheduling for Timely IoT Data Aggregation in Dynamic Environments*, IEEE TSC 2026 | GS-Q1-30 | AoI + năng lượng; thử trên nhiều mẫu di chuyển của thiết bị |
| B7 | *A Topology-Aware Two-Stage Generative Learning Framework for AoI-Optimal UAV Trajectory Planning*, preprint SSRN ✱ | GS-Q1-51 | AoI; GAT + A3C theo cấu trúc topo; chưa bình duyệt |
| B8 | Lin et al., *When Do Structural Priors Improve Generalization in Decentralized UAV Scheduling?*, preprint SSRN ✱ | GS-Q1-68 | Đánh giá tổng quát hoá có kiểm soát nhiều điều kiện; chưa rõ có thu dữ liệu |
| B9 | Yuan et al., *Freshness and Service-Aware UAV-Assisted IoT Data Collection via Joint AoI and Grey Time Window Modeling*, IEEE IoT-J 2026 | GS-Q1-91 | AoI; đoạn trích nêu thử trên bố trí chưa thấy và 3 seed. Chưa rõ phương pháp có phải DRL |
| B10 | Talukdar et al., *A Dual Map-Based Cooperative DDQN Approach for Trajectory Planning in a UAV-enabled IoT Network*, Physical Communication 2025 | GS-Q2-10 | Thu dữ liệu đa UAV; thích nghi điều kiện thay đổi (cần kiểm) |
| B11 | Kumar, Misra, *ARDDQN: Attention Recurrent DDQN for UAV Coverage Path Planning and Data Harvesting*, arXiv 2405.11013 | GS-Q2-21 | Dòng bài bản đồ của Bayerlein; cần kiểm có thử tham số kịch bản mới |
| B12 | Kumar et al., *Transformer based DDQN for UAV Coverage Path Planning and Data Harvesting*, IEEE Access 2026 | GS-Q2-34 | Như B11 |

### 6.3 Giữ — nhóm C (AoI + năng lượng đẩy, chưa thấy OOD)

| # | Bài | Nguồn |
| --- | --- | --- |
| C1 | Liu et al., *Resource Allocation for UAV-Enabled Spatio-Temporal Crowdsourcing in Smart Cities*, IEEE TVT 2025 (TD3/PPO/SAC; có kịch bản tổng hợp và thành phố thật) | OA Q1, GS-Q1-73 |
| C2 | Ferdowsi, Abd-Elmagid, Saad et al., *Neural Combinatorial DRL for Age-Optimal Joint Trajectory and Scheduling Design*, IEEE JSAC 2021 | GS-Q1-38 |
| C3 | Alam et al., *Integrated Trajectory, Association, and Fair Resource Allocation for AoI and Energy-Aware Data Collection*, IEEE OJCOMS 2026 | GS-Q1-45 |
| C4 | Li, Wu, Wang, *Multi-Agent DRL-Driven Age-Energy Efficiency Optimization in STAR-RIS Assisted Consumer-Grade Unmanned Vehicle Applications*, IEEE TCE 2025 | GS-Q1-50, GS-Q3-37 |
| C5 | Eldeeb, Alves, *Diffusion Offline RL for Fair and Energy-Efficient UAV-Assisted Wireless Networks*, arXiv 2606.16331 | GS-Q1-69 |
| C6 | Qadri et al., *AoS-Aware Trajectory Learning for UAV-Assisted IoT Sensing under Energy and Communication Constraints*, IEEE Sensors J. 2026 | GS-Q1-93 |
| C7 | Nobrega et al., *AoI-Aware Trajectory Planning for Smart Agriculture Using PPO*, ICMLCN 2024 (đoạn trích: không đánh giá tổng quát hoá) | OA Q3, GS-Q1-94, GS-Q3-3 |
| C8 | Li et al., *Attention-Based DRL for Logistics and Data Collection in AoI-Aware UAV Networks*, IEEE TCCN 2026 (không có tóm tắt) | GS-Q1-24, GS-Q2-31 |
| C9 | Kamali et al., *AoI-Aware Data Collection for Multi IRS-Assisted UAV Networks: A DRL Approach*, IEEE Access 2026 | GS-Q3-5 |
| C10 | Hu et al., *Minimizing Energy Consumption in UAV-Assisted Maritime Wireless Powered Networks with Constrained AoI*, IEEE Trans. 2025 ✱ | GS-Q3-7 |
| C11 | Gao et al., *Energy-Fairness-Aware Multi-UAV Trajectory Planning Algorithm for AoI-Constrained Data Collection*, IEEE Trans. 2026 ✱ | GS-Q3-8 |
| C12 | Fu et al., *AoI Minimization for UAV-Assisted IoT Networks: A Safe Actor-Critic with Policy Distillation Approach*, IEEE TNSE 2023 ✱ | GS-Q3-9 |
| C13 | Zhang, Chen, *PPO-Based Real-Time Optimization of AoI and Energy Consumption in UAV-Assisted IoT Networks*, hội nghị 2026 ✱ | GS-Q3-10 |
| C14 | Feng et al., *AoI Minimization for Data Collection with Multiple UAVs Cooperation*, 2025 ✱ | GS-Q3-11 |
| C15 | Wei et al., *Trajectory Design and Resource Allocation for RIS-Assisted UAV-Enabled WPCNs using DRL*, China Communications 2025 | GS-Q3-14 |
| C16 | Zhao et al., *A PPO-based Algorithm towards AoI-Aware Energy-Efficient UAV-assisted Data Collection*, ACM 2025 ✱ | GS-Q3-15 |
| C17 | Zhu et al., *MADDPG Based Path Planning for Multi-UAV Information Collection in IoT Networks*, IEEE Trans. 2026 ✱ | GS-Q3-16 |
| C18 | Bai et al., *An MA-HPPO Approach for Multi-UAV Data Collection*, IEEE TWC 2024 | GS-Q3-26 |
| C19 | Li et al., *Intelligent Scheduling of UAVs and Sensors for Information Age Minimization at Wireless Powered IoT*, 2024 ✱ | GS-Q3-27 |
| C20 | Wang et al., *Flight Trajectory Control with Network-Oriented Hierarchical RL for UAVs-Assisted Data Time-Sensitive IoT*, IEEE Trans. 2025 ✱ | GS-Q3-34 |
| C21 | Mei et al., *Energy-Aware Multi-UAV Collaboration for Data Collection and Trajectory Planning with MADDPG*, IEEE TNSM 2026 ✱ | GS-Q3-35 |
| C22 | Chen et al., *Multi-UAV Aided Data Collection in Complex 3D Urban Environments: A MADRL Approach Enhanced with Pheromone-Reward Shaping*, IEEE Trans. 2026 ✱ | GS-Q3-43 |
| C23 | Tang et al., *DRL for AoI-Aware Trajectory and Phase-Shift Design in IRS-Assisted UAV Data Collection*, IEEE Trans. 2025 ✱ | GS-Q3-44 |
| C24 | Zhang et al., *A Multi-UAV Trajectory Planning Algorithm for Time-Sensitive Data Collection*, hội nghị 2024 ✱ | GS-Q3-49 |
| C25 | Jia et al., *AoI- and Energy-Efficient Multi-UAV Coordination via Hierarchical DRL*, IEEE Trans. SMC 2026 ✱ | GS-Q3-53 |
| C26 | Gao et al., *Energy-efficient UAV Trajectory Planning Algorithm for AoI-constrained Data Collection*, J. Electronics & Information Technology 2024 ✱ | GS-Q3-61 |
| C27 | Huang et al., *AoI-Aware Data Collection in Heterogeneous UAV-Assisted WSNs*, Sensors 2026 (cần kiểm có DRL) | GS-Q3-62 |
| C28 | Shen et al., *Communication-Enhanced DRL for AoI- and Energy-Aware UAV Trajectory Optimization in MCS Data Collection*, GLOBECOM 2025 | GS-Q3-66 |
| C29 | Al-Qurabat, *IF-UAV: An Intelligent Federated Framework for Energy-Efficient Data Collection in UAV-Assisted IoT Systems*, Int. J. Commun. Syst. 2026 ✱ | GS-Q3-70 |
| C30 | Gong et al., *Joint Trajectory Design and Resource Allocation for QoS-Aware Emergency Data Collection in UAV-Assisted WPCNs*, Electronics 2026 | GS-Q3-73 |
| C31 | Yuan et al., *Hierarchical RL Based Joint Trajectory Planning and Resource Allocation in UAV-Assisted IoT-Sensor Networks*, IEEE Trans. 2025 ✱ | GS-Q3-77 |
| C32 | Ning et al., *Joint Optimization of Data Acquisition and Trajectory Planning for UAV-Assisted Wireless Powered IoT*, IEEE Trans. 2024 ✱ | GS-Q3-78 |
| C33 | Lu et al., *Joint Trajectory Planning and Channel Selection for AoI Minimization in Multi-UAV-Assisted IoT Networks*, IEEE Trans. 2026 ✱ | GS-Q3-79 |
| C34 | Peng et al., *Time-Effective UAV-IRS-Collaborative Data Harvesting: A Robust DRL Approach*, IEEE Trans. 2024 ✱ | GS-Q3-80 |
| C35 | Zhou et al., *Constrained Soft Actor-Critic for Energy-Aware Trajectory Design in UAV-Aided IoT Networks*, IEEE WCL 2022 ✱ | GS-Q3-84 |
| C36 | Huang et al., *A Learning-Based Iterative Algorithm for AoI-Optimal Trajectory Planning in UAV-Assisted IoT Networks*, IEEE Trans. 2025 ✱ (khoá `huang_lbi`, `docs/04` §2) | GS-Q3-81 |

✱ = tên tạp chí/hội nghị bị Scholar cắt ngắn, chưa kiểm thông tin xuất bản.

### 6.4 Loại ở bước tóm tắt/đoạn trích (30)

| Mã | Bài (nguồn) |
| --- | --- |
| E1 | Hu et al. 2020, U2D underlay (AX 2003.05830); Hu et al. 2020, Cooperative Internet of UAVs (AX 2007.14297, GS-Q1-76); DSC-UAV semantic communication (AX 2601.01430); GDM-MADDPG DNN task assignment (AX 2411.08299, GS-Q1-22); Peake et al. 2021 adaptive exploration, "AoI" = vùng quan tâm (AX 2105.01606, GS-Q1-5); AERO federated (OA Q1); UAV-RIS covert ISCC (OA Q1); Wu et al. 2026 UAV swarms sampling–buffering–routing (GS-Q1-3); Wu et al. 2026 age-driven UAV swarms (GS-Q1-12); MetaComm crowd sensing (GS-Q1-41) |
| E2 | FRSICL, LLM in-context learning, DRL chỉ là đối chứng (AX 2507.10134, OA Q1) — **đáng nhắc trong Related Work vì tối ưu vận tốc UAV cho AoI**; Luo et al. network AoI, tìm kiếm cây/Hamilton (GS-Q1-82; OA khớp bản WCNC 2022 ✱); Ndiaye et al. 2023 ensemble DNN (GS-Q1-97); Pan et al. 2018 dynamic speed control, giải tích (GS-Q2-97) |
| E3 | Ndiaye et al. 2024 decentralized MARL, "generalized AoI" là dạng công thức (AX 2312.15778, OA, GS-Q1-9); Long et al. 2025 semantic-aware AoI (GS-Q1-16); Fan et al. 2022 RIS-UAV 3D urban, tổng quát hoá chỉ là hướng tương lai (GS-Q1-18, GS-Q3-100); MA-HEAD-Net (GS-Q1-23); TL-RATS (GS-Q1-28, GS-Q3-28); Li et al. 2024 MAPPO data collection (GS-Q2-9); Bulusu et al. NOMA (GS-Q2-11); Qi et al. 2026 game-theoretic (GS-Q2-15, GS-Q3-19); Jin et al. 2024 urban accessibility (GS-Q2-16); Nguyen et al. 2022 3D trajectory (GS-Q2-17); Esrafilian et al. 2021 model-aided DRL (GS-Q2-23); Baba et al. SAC agriculture (GS-Q2-24); Li et al. 2022 DDRL-RA WPSN (GS-Q2-27); Wang et al. 2026 survival-aware DRL-NMPC (GS-Q2-36, GS-Q3-20); Chen et al. 2023 model-aided FedQMIX (GS-Q2-50); Bao et al. 2026 MAPPO energy-aware (GS-Q2-61) |

Ghi nhận ngoài tiêu chí, có ích cho chương 2: các tổng quan Amodu et al. 2023 (Drones), 2024 (IEEE Access), sách Amodu et al. 2025; Lee et al. 2026 (Drones); Zhao et al. 2025 (COMST); Chen et al. 2025 (ACM CSUR); luận văn Emami 2023 (điều khiển hành trình + thu dữ liệu, liên quan biến tốc độ). Dùng để tra ngược tài liệu, không đưa vào số PRISMA.
