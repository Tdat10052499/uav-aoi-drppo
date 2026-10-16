# 03 — Giao thức thực nghiệm

Thiết kế: thực nghiệm mô phỏng có kiểm soát. **Biến độc lập:** phương pháp huấn luyện (DR vs fixed), thuật toán (PPO vs DQN), λ. **Biến điều kiện:** bộ đánh giá (ID, 4 OOD). **Biến phụ thuộc:** AoI, năng lượng, độ suy giảm OOD. Đơn vị phân tích = **seed huấn luyện** (trung bình qua các episode đánh giá), theo khuyến nghị của Agarwal et al. (NeurIPS 2021) [A21].

---

## 1. Phân phối huấn luyện
| Tên | Mô tả | Mã |
| --- | --- | --- |
| **DR** (đề xuất) | Mỗi episode: N ~ U{10..30}, bố trí đều ngẫu nhiên, E_max ~ U[0,8; 1,2] MJ, điểm xuất phát ngẫu nhiên, L = 1000 m | `scenarios.TRAIN_DR` |
| **Fixed** (đối chứng) | Một bố trí duy nhất: N = 20, đều, E_max = 1,0 MJ, xuất phát tâm vùng, seed bố trí 0 | `scenarios.TRAIN_FIXED` |

## 2. Phương pháp so sánh
| Phương pháp | Vai trò | Ghi chú |
| --- | --- | --- |
| DR-PPO (MaskablePPO) | Đề xuất | `train_ppo.py --train dr --masked` |
| Fixed-PPO | Đối chứng then chốt cho RQ1/H1 | Cùng kiến trúc, cùng ngân sách bước và ngân sách tinh chỉnh |
| DR-DQN | Đối chứng thuật toán (RQ3) | `--algo dqn` |
| TSP (NN + 2-opt) | Heuristic mạnh, có thông tin đầy đủ | Chu trình cố định, hover tại mỗi điểm dừng |
| Greedy-AoI | Heuristic | Tới cảm biến có AoI/(khoảng cách + 100 m) lớn nhất |
| Random (có mask) | Cận dưới, kiểm tra môi trường | |

Heuristic đọc trạng thái thật (vị trí, AoI), tức thông tin tương đương quan sát nhưng ở độ phân giải đầy đủ. Đây là đối chứng **có lợi** cho heuristic — cần nêu rõ trong bài.

## 3. Ngân sách & seed
- **Seed huấn luyện:** 0–9 (10 seed) cho mỗi phương pháp học trong kết quả chính. MVP: tối thiểu 5 seed, ghi rõ là sơ bộ.
- **Seed đánh giá:** 100 episode cố định, seed 100000–100099 (`scenarios.eval_seeds`), tách biệt hoàn toàn với seed huấn luyện. Cùng bộ seed cho mọi phương pháp ⇒ so sánh theo cặp kịch bản.
- **Ngân sách bước:** bằng nhau cho mọi phương pháp học (điểm xuất phát 2 triệu bước; chốt sau đo đạc tuần 3).
- **Tinh chỉnh siêu tham số:** cùng số lượt Optuna (gợi ý 20 lượt × 200k bước) cho DR-PPO và Fixed-PPO, đánh giá tinh chỉnh trên **tập ID**, không bao giờ trên OOD.

## 4. Bộ đánh giá (ID + 4 OOD có cấu trúc)
| Bộ | Dịch chuyển so với huấn luyện | Tham số | Kiểm tra điều gì |
| --- | --- | --- | --- |
| `id` | Không | Như DR | Hiệu năng trong phân phối |
| `ood_cluster` | Cấu trúc không gian | 2–4 cụm Gauss, σ = 80 m | Bố trí phân cụm chưa thấy |
| `ood_density` | Số lượng (ngoại suy) | N ∈ {40, 50} | Nhiều cảm biến hơn khoảng huấn luyện |
| `ood_area` | Tỷ lệ không gian | L = 1500 m (ô lưới 93,75 m) | Vùng rộng hơn, cùng độ phân giải lưới |
| `ood_energy` | Tài nguyên | E_max ~ U[0,5; 0,7] MJ | Ngân sách năng lượng thấp hơn |

Lưu ý với Fixed-PPO: **mọi** bộ, kể cả `id`, đều là ngoài phân phối huấn luyện của nó. Độ suy giảm OOD vì vậy được tính so với `id` của chính phương pháp đó (§5).

## 5. Chỉ số
- **Chính:** AoI trung bình theo thời gian và cảm biến Ā (đơn vị: khe), tính trên toàn chân trời T kể cả khi hết pin sớm (`docs/02` §6).
- **Phụ:** peak AoI; năng lượng đã dùng (J, và tỷ lệ so với E_max); số lần thu; độ phủ (tỷ lệ cảm biến được thu ít nhất một lần); tỷ lệ hành động hover/chậm/nhanh; số lần chạm biên; tỷ lệ hết pin sớm; thời gian suy luận mỗi bước.
- **Độ suy giảm OOD** cho seed i, bộ s: deg_i(s) = (Ā_i(s) − Ā_i(id)) / Ā_i(id). Dương = tệ hơn.

## 6. Giả thuyết & kiểm định (đăng ký trước)
| Mã | Phát biểu | Kiểm định | Đơn vị |
| --- | --- | --- | --- |
| H1 | deg(DR-PPO) < deg(Fixed-PPO) trên từng bộ OOD | Hoán vị một phía, 20 000 hoán vị; hiệu chỉnh Holm trên 4 bộ; α = 0,05. Kết luận "ủng hộ H1" nếu ≥ 3/4 bộ có ý nghĩa sau hiệu chỉnh | 10 seed/nhóm |
| H2 | Ā(DR-PPO) < Ā(TSP) trên `ood_cluster` | Hoán vị một phía; báo cáo Cliff's δ | 10 seed vs 100 episode |
| H3 | Quan sát bản đồ căn tâm cần cho H1 | Chỉ mô tả (ablation) | — |

- Luôn báo cáo: trung bình kèm 95% CI bootstrap, IQM và cỡ hiệu ứng (Cliff's δ). Không chỉ báo cáo p-value.
- Welch t-test (SciPy) chỉ dùng làm kiểm tra phụ; kết luận dựa trên kiểm định hoán vị (không giả định phân phối, phù hợp n = 10).
- **Ngưỡng ý nghĩa thực tiễn:** nhóm phải chốt trước khi chạy (ví dụ: giảm ≥ 10% độ suy giảm OOD). Hiện **chưa xác định**.
- Mã: `scripts/analyze.py` thực hiện bảng tóm tắt, H1 và H2.

## 7. Ablation & RQ2
| Thí nghiệm | Thay đổi | Phục vụ |
| --- | --- | --- |
| A1 | Bỏ DR (= Fixed-PPO) | RQ1 |
| A2 | Quan sát không căn tâm (lưới tuyệt đối + kênh vị trí UAV) | H3 |
| A3 | Quan sát vector có padding tới N_max = 50 | H3 |
| A4 | Bỏ action mask (PPO thường, kẹp biên + phạt μ) | Độ nhạy thiết kế |
| A5 | Chỉ một mức tốc độ (V_me) | Vai trò của lựa chọn tốc độ |
| RQ2 | λ ∈ {0; 0,05; 0,1; 0,2; 0,5}, 5 seed mỗi λ | Đường đánh đổi AoI–năng lượng |

Ablation A2, A3 cần viết thêm mã (biến thể quan sát) — chưa có trong bộ khởi đầu.

## 8. Kế hoạch tính toán (cần đo, không ước đoán)
1. Tuần 3: đo thời gian 100k bước PPO trên máy nhóm (CPU và GPU nếu có).
2. Từ đó tính tổng: (số phương pháp học) × (số seed) × (số bước). Phương án B: DR-PPO, Fixed-PPO, DR-DQN × 10 seed, cộng ablation × 5 seed, cộng RQ2 5 λ × 5 seed.
3. Nếu vượt ngân sách: giảm bước trước, giảm seed sau cùng (không dưới 5 seed và phải ghi rõ).

Tham chiếu tốc độ môi trường (đo khi dựng bộ mã, 1 tiến trình, CPU 2 nhân, NumPy, chưa tối ưu): khoảng 4 300 bước/giây, gồm sinh quan sát và mask, hành động ngẫu nhiên. Đây **không** phải tốc độ huấn luyện PPO, vốn bị giới hạn bởi cập nhật mạng nơ-ron.

## 9. Mẫu đăng ký trước (điền trước khi chạy thực nghiệm chính, lưu `docs/PREREG.md`)
```markdown
Ngày khoá: ____  Commit: ____
Cấu hình môi trường (EnvConfig): đính kèm JSON
Siêu tham số cuối (sau tinh chỉnh trên ID): ____
Số seed: __  Số bước: __  Bộ seed đánh giá: 100000–100099
Ngưỡng ý nghĩa thực tiễn cho H1: ____
Tiêu chí loại một lần chạy (nếu có, ví dụ phân kỳ NaN): ____
Bất kỳ thay đổi nào sau ngày khoá: ghi vào DECISIONS.md kèm lý do
```

## 10. Đe doạ tính hợp lệ
- **Nội tại:** lỗi mô phỏng (đã có kiểm thử đơn vị cho AoI, năng lượng, mask, chống dừng sớm); reward hacking (trực quan hoá quỹ đạo hằng tuần, theo dõi tỷ lệ hover, độ phủ).
- **Cấu trúc:** AoI trung bình có thể che peak AoI ⇒ luôn báo cáo cả hai; thời gian bay không cố định ⇒ chỉ số tính trên toàn T.
- **Ngoại tại:** kênh LoS không che khuất, 2D, một UAV, không gió ⇒ ghi rõ trong phần giới hạn; không suy ra hiệu năng thực tế.
- **Kết luận thống kê:** nhiều so sánh ⇒ Holm; n = 10 seed nhỏ ⇒ dùng kiểm định hoán vị + CI, tránh tuyên bố mạnh khi CI chồng lấn.
- **Tinh chỉnh không cân bằng:** ngân sách Optuna bằng nhau, tinh chỉnh chỉ trên ID.
- **Đối chứng có lợi cho heuristic:** heuristic biết trạng thái đầy đủ — điều này làm kết quả "DR-PPO thắng TSP" (nếu có) trở nên thận trọng hơn, không ngược lại.
