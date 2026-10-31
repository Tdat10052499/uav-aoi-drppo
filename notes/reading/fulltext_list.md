# Danh sách đọc toàn văn sau tìm kiếm Q1–Q3 (W1-LDN-05)

> Nguồn: `notes/reading/search_log_LDN.md` §6 (mã A1–A9, B1–B12, C1–C36). Soạn 31/10/2026 (Claude cho LDN), **chờ LDN duyệt và DAT đồng ý cách chia**.
> Đầu vào của W2-DAT-01 (phần DAT) và W2-LDN-01 (phần LDN). Mỗi bài đọc xong: Form B ở `notes/reading/<khoá-bib>_<NICK>.md` và một hàng ma trận `docs/04` §5.

## Mức đọc đề xuất

| Nhóm | Mức đọc | Hạn đề xuất | Vì sao |
| --- | --- | --- | --- |
| A (9 + Yi 2020) | Toàn văn, Form B đầy đủ, hàng ma trận đủ 5 cột có mục/bảng | **T3 03/11** (trước G0 04/11) | Có AoI hoặc năng lượng UAV **và** có tổng quát hoá. Đây là các bài có thể đủ 5 cột, quyết định tiêu chí G0 số 2 |
| B (12) | Đọc mục mô hình + mục thực nghiệm; hàng ma trận rút gọn | T6 13/11 (trước G1) | Tổng quát hoá theo tham số kịch bản, phần lớn không AoI |
| C (36) | Đọc mục mô hình + mục thực nghiệm; chỉ điền 3 cột: tốc độ có là biến quyết định không, có huấn luyện nhiều bố trí/OOD không, số seed + CI | T6 13/11 (trước G1) | Có AoI + năng lượng đẩy; cần cho cột "năng lượng phụ thuộc tốc độ" và cho Related Work |

Nếu một bài nhóm B/C hoá ra có đánh giá ngoài phân phối thật, chuyển lên nhóm A và báo DAT ngay.

## Nhóm A — đọc trước G0

| Mã | Bài | Người đọc | Truy cập toàn văn |
| --- | --- | --- | --- |
| A1 | Gong et al. 2024, UAV-aided lifelong learning for AoI and energy (IEEE IoT-J) | DAT | arXiv 2312.00334 |
| A3 | Lu et al. 2025, attention-enhanced prompt Decision Transformers (IEEE WCL) | DAT | arXiv 2505.22170 |
| A4 | Chen, Liu, Zhang, Hanzo 2024, learning-aided UAV cooperation reduces AoI (IEEE Commun. Lett., DOI 10.1109/LCOMM.2024.3369761) | DAT | Cần IEEE Xplore hoặc bản tác giả |
| A5 | Toure et al. 2026, attention-based MORL for energy and data collection (IEEE IoT-J) | DAT | arXiv 2601.14092 |
| A7 | Zhou et al. 2024, population-invariant MADRL (HyperQMIX) (IEEE IoT-J, DOI 10.1109/JIOT.2024.3474926) | DAT | Cần IEEE Xplore hoặc bản tác giả |
| A2 | Yi et al. 2023/2025, meta-RL for solar-powered UAV data collection | LDN | arXiv 2311.06742 |
| A6 | Xiao, Yi, Wang et al. 2024, meta-learning DRL for fresh data collection in UAV-assisted WSNs | LDN | Cần IEEE Xplore hoặc bản tác giả (cùng nhóm tác giả với A2) |
| A8 | Eldeeb, Alves 2026, few-shot meta-offline RL (IEEE TMLCN) | LDN | arXiv 2502.01268 |
| A9 | Sarathchandra et al. 2025, meta-deep RL for age and power (IEEE TVT) — đã có hàng ma trận | LDN | arXiv 2501.14603 |
| — | Yi et al. 2020, DRL for fresh data collection (`yi2020deep`) — đã có hàng ma trận, không ra trong Q1–Q3 | LDN | ar5iv 2003.00391 |

Chia theo cụm tác giả để đọc nhanh: phần LDN gồm hai cụm Eldeeb–Alves (A8, A9) và Yi–Wang (A2, A6, Yi 2020); phần DAT gồm các bài còn lại. Mỗi người 5 bài.

## Nhóm B

| Mã | Bài | Người đọc |
| --- | --- | --- |
| B1 | Bayerlein et al. 2020 (GLOBECOM), tiền thân Bayerlein 2021 | DAT |
| B2 | Theile et al. 2021 (ICAR), bản đồ toàn cục–cục bộ | DAT |
| B3 | Seong, Jo, Shin 2023 (EAAI) | DAT |
| B4 | Abualhayja'a et al. 2025 (IEEE TVT), RIS-UAV data harvesting | DAT |
| B10 | Talukdar et al. 2025 (Physical Communication), dual map DDQN | DAT |
| B11 | Kumar, Misra 2024 (arXiv), ARDDQN | DAT |
| B12 | Kumar et al. 2026 (IEEE Access), Transformer DDQN | DAT |
| B5 | Pan et al. 2024 (IEEE IoT-J), GNN + QMIX cho AoI | LDN |
| B6 | Shukla, Shukla 2026 (IEEE TSC), ACDQN | LDN |
| B7 | Topology-aware two-stage generative learning (SSRN, preprint) | LDN |
| B8 | Lin et al. (SSRN, preprint), structural priors and generalization | LDN |
| B9 | Yuan et al. 2026 (IEEE IoT-J), grey time window | LDN |

B1–B4, B10–B12 cùng dòng bài "bản đồ + tham số kịch bản" của Bayerlein mà DAT đã đọc, nên giao DAT.

## Nhóm C

Chia xen kẽ: mã lẻ cho DAT, mã chẵn cho LDN (mỗi người 18 bài).

| Người đọc | Mã |
| --- | --- |
| DAT | C1, C3, C5, C7, C9, C11, C13, C15, C17, C19, C21, C23, C25, C27, C29, C31, C33, C35 |
| LDN | C2, C4, C6, C8, C10, C12, C14, C16, C18, C20, C22, C24, C26, C28, C30, C32, C34, C36 |

Bảng đầy đủ tên bài ở `search_log_LDN.md` §6.3.

## Lưu ý truy cập

Nhóm không truy cập được IEEE Xplore (31/10/2026). Với bài chỉ có trên IEEE, thử theo thứ tự: bản arXiv/TechRxiv, trang tác giả, xin GVHD hoặc thư viện, email xin bản tác giả (người đọc tự soạn và tự gửi). Không truy cập được thì ghi "chỉ tóm tắt" như `ohdrl2025_FAO.md`.
