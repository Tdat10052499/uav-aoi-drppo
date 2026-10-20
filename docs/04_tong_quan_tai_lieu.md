# 04 — Tổng quan tài liệu cốt lõi

Trạng thái: mẫu tài liệu có chọn lọc, chưa phải tổng quan hệ thống. Ký hiệu: ✔ = đã mở và đọc nội dung (toàn văn hoặc tóm tắt); ◐ = chỉ thấy tóm tắt/đoạn trích qua tìm kiếm; ✱ = trích từ hiểu biết chung, **phải kiểm tra** thông tin xuất bản trước khi đưa vào bài. Khoá BibTeX tương ứng nằm trong `paper/references.bib`.

---

## 1. Tài liệu bắt buộc đọc (theo thứ tự ưu tiên)

| Khoá | Công trình | Trạng thái | Vì sao quan trọng với đề tài |
| --- | --- | --- | --- |
| `bayerlein2021multi` | Bayerlein, Theile, Caccamo, Gesbert — *Multi-UAV Path Planning for Wireless Data Harvesting with Deep Reinforcement Learning*, [arXiv:2010.12461v3](https://arxiv.org/pdf/2010.12461) (mở rộng từ GLOBECOM 2020). Mã nguồn: [github.com/hbayerlein/uav_data_harvesting](https://github.com/hbayerlein/uav_data_harvesting) | ✔ toàn văn | **Công trình gần nhất.** DDQN đa tác tử, bản đồ toàn cục–cục bộ căn tâm; tổng quát hoá theo số UAV, số/vị trí/lượng dữ liệu cảm biến, thời gian bay, điểm xuất phát; có thử ngoại suy tham số. Mục tiêu: tối đa dữ liệu thu; năng lượng hằng số mỗi bước (lập luận rằng chi phí bay ngang chỉ hơn hover khoảng 10%). |
| `zeng2019energy` | Zeng, Xu, Zhang — *Energy Minimization for Wireless Communication with Rotary-Wing UAV*, [arXiv:1804.02238](https://arxiv.org/pdf/1804.02238) (IEEE TWC 2019 ✱) | ✔ toàn văn | Nguồn của mô hình công suất đẩy (phương trình 6, 61), kênh LoS (1)–(2), giao thức fly–hover–communicate, tham số Bảng I. |
| `agarwal2021deep` | Agarwal, Schwarzer, Castro, Courville, Bellemare — *Deep RL at the Edge of the Statistical Precipice*, NeurIPS 2021 ([PDF](https://proceedings.neurips.cc/paper_files/paper/2021/file/f514cec81cb148559cf475e7426eed5e-Paper.pdf)); thư viện [rliable](https://pypi.org/project/rliable) | ◐ | Cơ sở phương pháp luận cho CI bootstrap, IQM khi số lần chạy ít. |
| `yi2020deep` | Yi et al. — *Deep Reinforcement Learning for Fresh Data Collection in UAV-assisted IoT Networks* ([ar5iv 2003.00391](https://ar5iv.arxiv.org/html/2003.00391)); IEEE INFOCOM Workshops 2020 theo trích dẫn của [B21] | ◐ | MDP cho quỹ đạo + lập lịch giảm AoI có trọng số, có ràng buộc năng lượng — tiền thân trực tiếp của bài toán AoI. |
| `abdelmagid2019deep` | Abd-Elmagid, Ferdowsi, Dhillon, Saad — *DRL for Minimizing AoI in UAV-Assisted Networks*, GLOBECOM 2019 ✱ ([arXiv:1905.02993v2](https://arxiv.org/abs/1905.02993)) | ✔ toàn văn (`notes/reading/abdelmagid2019deep_FAO.md`) | Công trình AoI–DRL kinh điển, đối chứng khái niệm. |
| `alhourani2014optimal` | Al-Hourani, Kandeepan, Lardner — *Optimal LAP Altitude for Maximum Coverage*, IEEE WCL 3(6):569–572, 2014, DOI 10.1109/LWC.2014.2342736 ([RMIT](https://research-repository.rmit.edu.au/articles/journal_contribution/Optimal_LAP_altitude_for_maximum_coverage/27465243)) | ◐ | Mô hình xác suất LoS cho mở rộng kênh (bản đầy đủ). Hệ số a, b cần lấy từ bài gốc. |

## 2. AoI + năng lượng + DRL (bối cảnh, so sánh trong Related Work)

| Khoá | Công trình | Trạng thái | Điểm chính (theo tác giả) |
| --- | --- | --- | --- |
| `ohdrl2025` | *OH-DRL: An AoI-Guaranteed Energy-Efficient Approach for UAV-Assisted IoT Data Collection*, IEEE TWC 24(6):5009–5022, 2025 ([trang](https://research.usc.edu.au/esploro/outputs/journalArticle/OH-DRL-An-AoI-Guaranteed-Energy-Efficient-Approach-for/991127505202621)) | ◐ chỉ tóm tắt, không truy cập được toàn văn (`notes/reading/ohdrl2025_FAO.md`) | DRL phân cấp + STAR-RIS; giảm 14,4% năng lượng bay, giảm 66% số episode hội tụ so với DRL đối chứng |
| `sarathchandra2025age` | Sarathchandra et al. — *Age and Power Minimization via Meta-Deep RL in UAV Networks*, [arXiv:2501.14603](https://arxiv.org/pdf/2501.14603.pdf) | ◐ | DQN + MAML; thích nghi khi **hàm mục tiêu** thay đổi (không phải bố trí) |
| `sun2025aoi` | Sun et al. — *AoI Optimization in Laser-charged UAV-assisted IoT Networks: A MADRL Method*, [arXiv:2507.08429](https://arxiv.org/pdf/2507.08429) | ✔ toàn văn (`notes/reading/sun2025aoi_FAO.md`) | MAPPO có bộ nhớ thời gian; giảm tới 15,1% peak AoI so với MADRL đối chứng |
| `huang_lbi` | Huang et al. — *A Learning-Based Iterative Algorithm for AoI-Optimal Trajectory Planning in UAV-Assisted IoT Networks* ([trang](https://scholar.xjtu.edu.cn/en/publications/a-learning-based-iterative-algorithm-for-aoi-optimal-trajectory-p/)) | ◐ | SCA cho lập lịch + A3C phân cấp cho đường bay |
| `kumari2024aoi` | Kumari et al. — *AoI-Aware DRL Based UAV Path Planning for Defence Applications*, IEEE SPACE 2024, DOI 10.1109/SPACE63117.2024.10668088 | ◐ | Phân cụm + PPO; mẫu tham khảo cấu trúc bài hội nghị ngắn |
| `coop2023` | *Cooperative Data Collection with Multiple UAVs for Information Freshness in the IoT*, [arXiv:2303.01381](https://arxiv.org/pdf/2303.01381) | ◐ | Dec-POMDP, CTDE (QMIX) — tham khảo cho hướng mở rộng đa UAV |
| `lamenza2025` | de Souza Lamenza et al. — *DRL Approaches for Sensor Data Collection by a Swarm of UAVs*, Advanced Intelligent Systems, DOI 10.1002/aisy.202501146 | ◐ (không mở được toàn văn) | "Flexible sensor count": một mô hình cho số cảm biến/tác tử bất kỳ; bài toán thăm một lần. **Cần đọc toàn văn** để định vị. |

## 3. Tổng quan & tổng quát hoá
| Khoá | Công trình | Trạng thái |
| --- | --- | --- |
| `zhao2025survey` | Zhao et al. — *A Survey on DRL based UAV Communications and Networking*, [arXiv:2502.12875](https://arxiv.org/abs/2502.12875v1) | ◐ |
| `amodu2025survey` | Amodu et al. (có Nguyễn Công Lương) — *A comprehensive survey of DRL in UAV-assisted IoT data collection*, Vehicular Communications, 2025, DOI 10.1016/j.vehcom.2025.100949 | ◐ |
| `luong2019applications` | Luong et al. — *Applications of DRL in Communications and Networking: A Survey*, IEEE COMST 21(4), 2019 ([arXiv:1810.07862](https://arxiv.org/pdf/1810.07862)) | ◐ |
| `liu2024generalizable` | Liu — *Learning Generalizable Policy for Obstacle-Aware Autonomous Drone Racing*, [arXiv:2411.04246](https://arxiv.org/abs/2411.04246v1) | ✔ toàn văn (`notes/reading/liu2024generalizable_FAO.md`) — domain randomization mỗi rollout |
| `robustquad2021` | *Robust Deep RL for Quadcopter Control*, [arXiv:2111.03915](https://arxiv.org/pdf/2111.03915) | ◐ — chỉ ra giới hạn "trong phân phối" của domain randomization |

## 4. Tài liệu nền phải trích (✱ — kiểm tra thông tin xuất bản)
- Schulman et al., *Proximal Policy Optimization Algorithms*, arXiv:1707.06347, 2017.
- Tobin et al., *Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World*, IROS 2017.
- Kaul, Yates, Gruteser, *Real-time status: How often should one update?*, IEEE INFOCOM 2012 (định nghĩa AoI).
- Raffin et al., *Stable-Baselines3: Reliable Reinforcement Learning Implementations*, JMLR 2021.
- Huang, Ontañón, *A Closer Look at Invalid Action Masking in Policy Gradient Algorithms*, FLAIRS 2022 (cơ sở cho MaskablePPO).

## 5. Ma trận định vị (điền tiếp trong tuần 1–2)
| Công trình | Mục tiêu AoI | Năng lượng phụ thuộc tốc độ | Huấn luyện trên nhiều bố trí | Đánh giá OOD có cấu trúc | Nhiều seed + CI |
| --- | --- | --- | --- | --- | --- |
| Bayerlein 2021 | Không (dữ liệu thu) | Không (hằng số/bước) | Có | Một phần (ngoại suy tham số) | Monte Carlo trên kịch bản |
| Yi 2020 | Có | Có ràng buộc năng lượng | Chưa rõ | Chưa rõ | Chưa rõ |
| Sarathchandra 2025 | Có | Công suất phát | Không (thay mục tiêu) | Không | Chưa rõ |
| Lamenza 2025 | Không (thăm một lần) | Chưa rõ | Có (số cảm biến linh hoạt) | Chưa rõ | Chưa rõ |
| Abd-Elmagid 2019 | Có (tổng AoI có trọng số) | Không (UAV chỉ bị ràng buộc thời gian τ; năng lượng là pin của nút) | Không (vị trí nút cố định mỗi kịch bản) | Không (chỉ quét e_max, τ, mật độ) | Không (TB 1000 episode, không seed/CI) |
| Sun 2025 | Có (peak AoI, đa UAV) | Có mô hình P(v) nhưng v cố định 5 m/s, nên không là biến quyết định | Không (IoT cố định) | Không (chỉ quét η_le) | Không (không báo seed; vùng "variance" không rõ n) |
| OH-DRL 2025 (chỉ tóm tắt) | Có (ràng buộc AoI trung bình tối đa; mục tiêu là năng lượng bay) | Chưa rõ (có tối thiểu năng lượng bay; mô hình chưa kiểm) | Chưa rõ | Chưa rõ | Chưa rõ |
| Liu 2024 (tham khảo DR, ngoài phạm vi) | Không (đua drone) | Không | Có (môi trường mới mỗi rollout) | Có (4 mức khó + 4 đường đua thiết kế tay) | Không (1 chính sách, không seed/CI) |
| **Đề tài này** | Có | Có (Zeng 2019) | Có | Có (4 bộ) | Có (10 seed, CI, Holm) |

Các ô "Chưa rõ" phải được điền bằng việc đọc toàn văn; nếu một công trình có đủ cả năm cột "Có", đóng góp C2 phải được viết lại (gate G0, `05`).

## 6. Chiến lược tìm kiếm cho tổng quan hệ thống (tuần 1)
**Cơ sở dữ liệu:** IEEE Xplore, Scopus, Google Scholar (tra thủ công), arXiv (cs.NI, cs.LG, eess.SP). **Khoảng thời gian:** 2018–2026.

Chuỗi tìm kiếm:
```
Q1: ("UAV" OR "drone") AND ("age of information" OR "AoI") AND ("reinforcement learning")
    AND ("generaliz*" OR "domain randomization" OR "unseen" OR "out-of-distribution" OR "meta")
Q2: ("UAV" OR "drone") AND ("data collection" OR "data harvesting") AND ("reinforcement learning")
    AND ("variable number of sensors" OR "scenario parameters" OR "map-based")
Q3: ("UAV") AND ("age of information") AND ("propulsion energy" OR "rotary-wing") AND ("PPO" OR "proximal policy")
```
**Tiêu chí chọn:** bài toán UAV thu dữ liệu từ cảm biến mặt đất; có DRL; có đánh giá trên kịch bản khác tập huấn luyện **hoặc** có AoI + năng lượng đẩy. **Loại:** chỉ tối ưu lồi/heuristic, chỉ điều khiển bay mức thấp.
**Ghi nhận:** mỗi bài điền một hàng vào ma trận §5 + 1 dòng "khác biệt với đề tài". Ghi số kết quả mỗi truy vấn, số bài sau lọc tiêu đề/tóm tắt, số bài đọc toàn văn (sơ đồ PRISMA rút gọn cho chương 2 của đồ án).

## 7. Hội nghị (kiểm tra ngày 16/10/2026)
| Hội nghị | Hạn nộp | Ghi chú |
| --- | --- | --- |
| [INISCOM 2027](https://iniscom.eai-conferences.org/2027/call-for-papers/) (Late Track 2) | 31/10/2026 | Springer LNICST; 6–11 trang (short) hoặc 12–20 trang (full) |
| [ICISN 2027](https://www.icisn.com/) | Chưa công bố trên trang | 20–21/03/2027, ĐH Hải Dương; Springer LNNS (Scopus) |
| FJCAI 2027 (HT quốc gia về AI, VKU đăng cai) | Chưa công bố | Bản 2026: hạn 01/12/2025, thông báo 15/01/2026; 6–8 trang IEEE; kỷ yếu ISBN |
| [AIEI 2027](https://www.aiei2027.org/) | 15/02/2027 | ĐH Văn Lang |
| IEEE SMC 2027 (TP.HCM) | 15/04/2027 theo trang tổng hợp, chưa có trang chính thức | |
