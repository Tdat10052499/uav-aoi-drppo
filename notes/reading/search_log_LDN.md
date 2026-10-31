# Nhật ký tìm kiếm hệ thống Q1–Q3 (W1-LDN-04, W1-LDN-05)

> Owner: LDN · Second reader: DAT · Giao thức: `docs/04` §6.
> Trạng thái: **NHÁP, chưa chạy truy vấn.** Claude soạn khung ngày 31/10/2026 cho LDN. LDN duyệt mọi quyết định giữ/loại trước khi đánh dấu task xong.

## 1. Cơ sở dữ liệu và khả năng truy cập (31/10/2026)

| CSDL | Truy cập | Ghi chú |
| --- | --- | --- |
| Scopus | Có (tài khoản trường của LDN) | Tìm trong TITLE-ABS-KEY |
| IEEE Xplore | LDN không truy cập được bằng tài khoản trường | Trang tìm kiếm và tóm tắt của IEEE Xplore mở công khai; chỉ toàn văn cần quyền. Đã báo DAT (`notes/yeu-cau/`) |
| arXiv | Công khai | Lọc chuyên mục cs.NI, cs.LG, eess.SP |
| Google Scholar | Công khai, tra thủ công | Không hỗ trợ ký tự đại diện; tìm cả toàn văn nên số kết quả lớn |

**Khoảng thời gian:** 2018–2026 (theo `docs/04` §6).

## 2. Chuỗi truy vấn theo cú pháp từng CSDL

Chuỗi gốc ở `docs/04` §6. Mọi điều chỉnh so với chuỗi gốc được ghi ở cột "Điều chỉnh".

### Scopus (Advanced search)
```
Q1: TITLE-ABS-KEY ( ( "UAV" OR "drone" ) AND ( "age of information" OR "AoI" ) AND ( "reinforcement learning" )
      AND ( generaliz* OR "domain randomization" OR "unseen" OR "out-of-distribution" OR "meta" ) )
      AND PUBYEAR > 2017 AND PUBYEAR < 2027
Q2: TITLE-ABS-KEY ( ( "UAV" OR "drone" ) AND ( "data collection" OR "data harvesting" ) AND ( "reinforcement learning" )
      AND ( "variable number of sensors" OR "scenario parameters" OR "map-based" ) )
      AND PUBYEAR > 2017 AND PUBYEAR < 2027
Q3: TITLE-ABS-KEY ( "UAV" AND "age of information" AND ( "propulsion energy" OR "rotary-wing" )
      AND ( "PPO" OR "proximal policy" ) )
      AND PUBYEAR > 2017 AND PUBYEAR < 2027
```

### IEEE Xplore (Command Search, All Metadata, lọc năm 2018–2026)
```
Q1: ("UAV" OR "drone") AND ("age of information" OR "AoI") AND ("reinforcement learning")
    AND (generaliz* OR "domain randomization" OR "unseen" OR "out-of-distribution" OR "meta")
Q2: ("UAV" OR "drone") AND ("data collection" OR "data harvesting") AND ("reinforcement learning")
    AND ("variable number of sensors" OR "scenario parameters" OR "map-based")
Q3: ("UAV") AND ("age of information") AND ("propulsion energy" OR "rotary-wing") AND ("PPO" OR "proximal policy")
```

### arXiv (Advanced search, trường Abstract, 2018–2026)
Cùng chuỗi như IEEE Xplore. Điều chỉnh: arXiv chỉ lọc được theo nhóm lớn (Computer Science, EESS), nên lọc chuyên mục cs.NI, cs.LG, eess.SP làm thủ công khi sàng lọc.

### Google Scholar (2018–2026)
Điều chỉnh: thay `generaliz*` bằng `generalization OR generalize OR generalizable OR generalizing`. Scholar tìm trong toàn văn nên chỉ sàng lọc tối đa 100 kết quả đầu (sắp theo mức liên quan) mỗi truy vấn; ghi rõ số này.

## 3. Số kết quả (PRISMA rút gọn)

| Truy vấn | Scopus | IEEE Xplore | arXiv | Google Scholar | Ngày tìm |
| --- | --- | --- | --- | --- | --- |
| Q1 | | | | | |
| Q2 | | | | | |
| Q3 | | | | | |

| Bước | Số bài |
| --- | --- |
| Tổng kết quả (mọi CSDL, mọi truy vấn) | |
| Sau loại trùng | |
| Loại ở bước tiêu đề/tóm tắt | |
| Giữ lại để đọc toàn văn | |
| Đã có trong ma trận `docs/04` §5 trước tìm kiếm | |

## 4. Tiêu chí chọn/loại (`docs/04` §6)
- **Chọn:** UAV thu dữ liệu từ cảm biến mặt đất; có DRL; có đánh giá trên kịch bản khác tập huấn luyện **hoặc** có AoI + năng lượng đẩy.
- **Loại:** chỉ tối ưu lồi/heuristic; chỉ điều khiển bay mức thấp.

## 5. Sàng lọc tiêu đề/tóm tắt

| # | Tiêu đề (năm) | Nguồn (CSDL, Q) | Giữ/Loại | Lý do (theo tiêu chí §4) |
| --- | --- | --- | --- | --- |
