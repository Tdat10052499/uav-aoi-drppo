# 02 — Mô hình hệ thống & MDP

Quy ước nguồn: **[Z19]** = Zeng, Xu, Zhang, *Energy Minimization for Wireless Communication with Rotary-Wing UAV* (arXiv:1804.02238v1, 2018; bản IEEE TWC 2019). **[B21]** = Bayerlein et al., arXiv:2010.12461v3 (2021). Giá trị ghi **"thiết kế"** là lựa chọn của đề tài, không đến từ tài liệu; phải được nêu rõ như vậy trong bài báo.

---

## 1. Kịch bản
- Vùng vuông L × L (m), N cảm biến mặt đất tại vị trí w_n, sinh dữ liệu cập nhật liên tục.
- Một UAV cánh quay bay ở độ cao cố định H, thời gian rời rạc theo khe quyết định δt (s), chân trời T khe.
- Giao thức **fly–hover–communicate** [Z19, §III]: UAV chỉ truyền nhận khi dừng (hover); khi bay không thu dữ liệu. Lựa chọn này đơn giản hoá lập lịch và khớp với mô hình năng lượng.

## 2. Mô hình năng lượng đẩy (đã đối chiếu [Z19], phương trình (6))

```latex
P(V)=P_0\left(1+\frac{3V^2}{U_{tip}^2}\right)+P_i\left(\sqrt{1+\frac{V^4}{4v_0^4}}-\frac{V^2}{2v_0^2}\right)^{1/2}+\frac{1}{2}d_0\rho s A V^3
```

với P_0 = (δ/8)·ρ·s·A·Ω³·R³ và P_i = (1+k)·W^{3/2}/√(2ρA) [Z19, phương trình (61)], v_0 = √(W/(2ρA)). Công suất hover P_h = P_0 + P_i. Công suất truyền thông P_c là hằng số khi truyền.

Hai tốc độ đặc trưng [Z19, §II-B]: **V_me** = argmin P(V) (bền nhất theo thời gian), **V_mr** = argmin P(V)/V (xa nhất theo quãng đường). [Z19] chỉ ra hover **không** phải trạng thái tiết kiệm công suất nhất.

### Bảng tham số (bộ mặc định = [Z19] Bảng I, arXiv v1 — đã đối chiếu)
| Ký hiệu | Ý nghĩa | Giá trị |
| --- | --- | --- |
| W | Trọng lượng (N) | 100 |
| ρ | Mật độ không khí (kg/m³) | 1,225 |
| R | Bán kính rotor (m) | 0,5 |
| A | Diện tích đĩa rotor (m²) | 0,79 |
| Ω | Vận tốc góc cánh (rad/s) | 400 |
| U_tip | Tốc độ đầu cánh (m/s) | 200 |
| s | Độ đặc rotor | 0,05 |
| d_0 | Tỷ số cản thân | 0,3 |
| k | Hệ số hiệu chỉnh công suất cảm ứng | 0,1 |
| δ | Hệ số cản profile | 0,012 |
| P_c | Công suất truyền thông (W) | 50 (mục V của [Z19]) |

**Giá trị suy ra** (tính lại bằng `code/uavaoi/energy.py`, kiểm thử trong `tests/`): P_0 ≈ 580,6 W; P_i ≈ 790,7 W; v_0 ≈ 7,19 m/s (khớp 7,2 của [Z19]); P_h ≈ 1371,3 W; V_me ≈ 21,5 m/s (P ≈ 935,6 W); V_mr ≈ 38,3 m/s (P ≈ 1199,5 W).

**Bộ tham số "nhẹ" (tuỳ chọn, `preset="light"`):** W = 20 N, R = 0,4 m, A = 0,503 m², Ω = 300 rad/s, d_0 = 0,6, cùng ρ, s, k, δ. Cho P_0 ≈ 79,86 W, P_i ≈ 88,63 W — trùng các giá trị nhiều công trình sau trích dẫn. **[cần kiểm tra]** bộ này với bản IEEE TWC chính thức của [Z19] trước khi dùng làm mặc định.

## 3. Mô hình kênh & tốc độ truyền (đã đối chiếu [Z19], phương trình (1)–(2))

```latex
R_n(t)=B\log_2\left(1+\frac{\gamma_0}{H^2+\lVert \mathbf{q}(t)-\mathbf{w}_n\rVert^2}\right)
```

Kênh LoS, suy hao không gian tự do; γ_0 là SNR tham chiếu tại 1 m. Tham số mặc định lấy từ mục V của [Z19]: H = 100 m, B = 1 MHz, γ_0 = 60 dB (SNR cực đại khi UAV ngay trên cảm biến = 20 dB).

**Mở rộng tuỳ chọn (bản đầy đủ):** mô hình xác suất LoS của Al-Hourani và cộng sự (IEEE WCL 2014). Hệ số môi trường (a, b, η_LoS, η_NLoS) **[cần kiểm tra]** từ bài gốc trước khi cài đặt.

## 4. Thu dữ liệu & lập lịch (thiết kế)
- Mỗi lần thu, cảm biến gửi một gói trạng thái kích thước S (bit). Thu thành công khi UAV hover và R_n·δt ≥ S.
- TDMA: mỗi khe phục vụ **tối đa một** cảm biến (như ràng buộc (3) của [Z19]). Quy tắc chọn: cảm biến khả thi có AoI lớn nhất.
- Mặc định (thiết kế): S = 15 Mbit, δt = 3 s ⇒ cần R ≥ 5 Mbps ⇒ SNR ≥ 31 ⇒ bán kính thu hiệu dụng ≈ 149 m (tính từ phương trình trên).

## 5. Tuổi thông tin (AoI)

```latex
\Delta_n(t+1)=\begin{cases}1, & \text{if sensor } n \text{ is served in slot } t\\ \min\big(\Delta_n(t)+1,\ \Delta_{\max}\big), & \text{otherwise}\end{cases}
```

AoI đo bằng số khe, Δ_max = T. Chỉ số chính: AoI trung bình theo thời gian và theo cảm biến, Ā = (1/(T·N)) Σ_t Σ_n Δ_n(t); chỉ số phụ: peak AoI. Định nghĩa AoI gốc: Kaul, Yates, Gruteser (INFOCOM 2012) **[cần kiểm tra trích dẫn]**.

## 6. Công thức MDP

### Trạng thái/quan sát (thiết kế, theo ý tưởng bản đồ căn tâm của [B21] §IV)
Lưới G × G phủ vùng (mặc định G = 16, ô 62,5 m khi L = 1000 m), **căn tâm** theo vị trí UAV thành ảnh (2G−1) × (2G−1), 5 kênh:
1. Tổng AoI chuẩn hoá (Δ/Δ_max) của cảm biến trong ô
2. Số cảm biến trong ô (chuẩn hoá)
3. Mặt nạ ngoài vùng (1 = ngoài vùng)
4. Mặt phẳng hằng: năng lượng còn lại / E_max
5. Mặt phẳng hằng: thời gian còn lại / T

Kích thước quan sát không phụ thuộc N; diện tích khác nhau được chuẩn hoá theo L (giới hạn: kích thước ô vật lý thay đổi ở bộ OOD-area).

### Hành động: 17 hành động rời rạc (thiết kế)
- a = 0: hover + thu dữ liệu.
- a = 1…8: bay theo 8 hướng ở **V_me**; a = 9…16: 8 hướng ở **V_mr**. Quãng bay mỗi khe = V·δt (≈ 64 m và ≈ 115 m với mặc định).
- Hành động đưa UAV ra ngoài vùng bị chặn bởi action mask (MaskablePPO) hoặc bị kẹp tại biên kèm phạt μ (PPO thường).

### Năng lượng mỗi khe
Bay: E_t = P(V)·δt. Hover-thu: E_t = (P_h + P_c·1[có truyền])·δt.

### Hàm thưởng (thiết kế)

```latex
r_t=-\frac{1}{N}\sum_{n=1}^{N}\frac{\Delta_n(t+1)}{\Delta_{\max}}-\lambda\,\frac{E_t}{P_h\,\delta t}-\mu\,\mathbb{1}[\text{boundary}]
```

### Kết thúc episode & chống reward hacking
- Hết T khe (truncated) hoặc năng lượng không đủ cho bước tiếp theo (terminated).
- **Rủi ro:** nếu chỉ dừng sớm, tác tử có thể "học" cách cạn pin sớm để tránh các phần thưởng âm còn lại. **Biện pháp:** khi dừng sớm, cộng phạt (số khe còn lại)·(1 + λ·ρ_max + μ), với ρ_max = max(P_h + P_c, P(V_me), P(V_mr))/P_h. Mức phạt này không nhỏ hơn chi phí lớn nhất mà bất kỳ khe nào có thể gây ra, nên dừng sớm không bao giờ có lợi. Kiểm thử: `code/tests/test_core.py::test_early_battery_death_never_pays`.
- **Chỉ số AoI khi dừng sớm:** AoI tiếp tục tăng (không thu thêm) đến hết chân trời T, để so sánh công bằng giữa phương pháp hết pin sớm và phương pháp chạy đủ T.
- **Quan sát từ mô phỏng (heuristic, 100 episode/bộ, `code/results/`):** với cấu hình mặc định, TSP và tham lam AoI hết pin trước T ở 92–100% episode tuỳ bộ (100% ở OOD-energy). Ràng buộc năng lượng vì vậy có hiệu lực, và còn dư địa cho chính sách biết điều tiết tốc độ và hover.

## 7. Bảng tham số môi trường mặc định (thiết kế)
| Tham số | Mặc định | Ghi chú |
| --- | --- | --- |
| L | 1000 m | OOD-area: 1500 m |
| N | U{10,…,30} khi huấn luyện | OOD-density: {40, 50} |
| T, δt | 300 khe, 3 s | 15 phút nhiệm vụ |
| E_max | U[0,8; 1,2] MJ | OOD-energy: U[0,5; 0,7] MJ; 1 MJ đủ hover ≈ 243 khe (không truyền) hoặc ≈ 234 khe (có truyền) < T |
| S | 15 Mbit | bán kính thu ≈ 149 m |
| G | 16 | quan sát 5 × 31 × 31 |
| λ | 0,1 (quét {0; 0,05; 0,1; 0,2; 0,5} cho RQ2) | |
| μ | 0,1 | |
| Vị trí xuất phát | ngẫu nhiên trong vùng | |

Mọi giá trị "thiết kế" phải được giữ cố định trước khi chạy thực nghiệm chính; thay đổi sau đó phải ghi vào `DECISIONS.md`.
