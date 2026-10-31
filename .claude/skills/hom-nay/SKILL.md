---
name: hom-nay
description: Dùng khi một thành viên (DAT, LDN, FAO) hỏi "hôm nay tôi cần làm gì", "việc hôm nay", "bắt đầu ngày", "today" trong repo uav-aoi-drppo. Lập kế hoạch ngày từ schedule/tasks.json rồi thực hiện theo quy trình RIVF.
---

# Hôm nay tôi cần làm gì?

Mục tiêu: trong vài phút, thành viên biết chính xác việc của ngày, rồi Claude làm cùng họ đến khi có bằng chứng.

## 1. Đồng bộ và xác định người, ngày
1. Chạy `git status --short`.
   - Nếu working tree sạch: `git pull --rebase`.
   - Nếu có thay đổi chưa commit: KHÔNG pull. Liệt kê các file, rồi hỏi thành viên muốn commit, stash hay bỏ qua.
2. Chạy `python scripts/today.py --json`. Ngày tính theo giờ Việt Nam; **không tự đoán ngày**.
   - Nếu kết quả có `"error": "unknown_nick"`: hỏi một lần "Bạn là DAT, LDN hay FAO?", rồi chạy `python scripts/today.py --set-nick <NICK>` và chạy lại bước 2.
3. Kiểm tra nhanh để biết thực tế đang đứng ở đâu (bước này chỉ đọc):
   - `python tests/test_core.py` khi task hôm nay động tới mã;
   - `gh issue view <số>` cho các issue liên quan, nếu `gh` dùng được;
   - các file trong `outputs` của task đã tồn tại chưa.
   Nếu một task chưa đánh dấu xong nhưng file kết quả đã có và đạt `done_when`, nói ra và đề nghị đánh dấu xong.

## 2. Trình bày kế hoạch (ngắn, tiếng Việt)
Thứ tự ưu tiên:
0. **YÊU CẦU GỬI BẠN** (`inbox`): câu hỏi, số liệu, quyết định mà thành viên khác đang chờ, từ `notes/yeu-cau/` và `notes/*_can-<NICK>.md`. Gom theo người gửi; với mỗi mục, đọc file và nói cần thành viên trả lời gì. Trả lời bằng dòng `<NICK>:` dưới mục, theo lời của thành viên.
2. **CẦN REVIEW** (`reviews`). Second reader chậm sẽ chặn cả nhóm.
3. **HÔM NAY** (`today`).
4. Task bị chặn (`blocked`): nêu đang chờ ai và việc gì.

Với mỗi task cần làm, ghi:
- id, tiêu đề, hạn;
- 2–4 bước cụ thể;
- **phần Claude làm** (viết mã, chạy lệnh, soạn Form B từ PDF thành viên cung cấp, soạn nháp email);
- **phần thành viên phải tự làm** (gửi email, chấp nhận lời mời, bấm nộp, quyết định khoa học, đọc và ký second reader);
- tiêu chí `done_when`.

Thêm 1 dòng về gate gần nhất (`next_gate`, còn bao nhiêu ngày). Nếu task trễ hơn 2 ngày nằm trên đường tới gate, ghi rõ "báo DAT".

Kết thúc bằng **một** câu hỏi: "Bắt đầu với [id] nhé?" (hoặc đề xuất thứ tự khác nếu thành viên có giới hạn thời gian). Không hỏi thêm.

## 3. Thực hiện
Ngay khi bắt đầu một task: `python scripts/today.py --start <ID>`.

Quy tắc bắt buộc (từ RIVF-Paper, `docs/00_HUONG_DAN_PROJECT.md`):
- **Thực nghiệm:**
  - card (Form D) phải có **trước** khi chạy;
  - chỉ chạy qua `scripts/*.py`, để run record tự sinh;
  - **không bao giờ** sửa, xoá hay ghi đè `results/raw/`.
- **Lần chạy dài (> 30 phút) hoặc lần đầu của cấu hình mới:**
  - hỏi thành viên trước khi chạy;
  - chạy nền và theo dõi vài phút đầu;
  - ghi run ID vào card.
- **Số đo thời gian (steps/s, giờ máy):** chỉ hợp lệ khi nick là DAT và chạy trên máy cố định. Máy khác thì ghi là "không dùng cho bài".
- **Thay đổi `src/` hoặc `scripts/`:**
  - làm trên nhánh `<nick viết thường>/<chủ-đề>`;
  - kiểm thử phải pass;
  - mở PR, gán second reader của task làm reviewer.
  `notes/` và `schedule/status/` được commit thẳng `main`.
- **Ghi chú đọc (Form B):**
  - chỉ viết từ văn bản thật của bài báo (PDF hoặc URL mở được);
  - mỗi nhận định ghi mục, bảng hoặc hình;
  - không mở được toàn văn thì nói rõ và hỏi thành viên đính kèm PDF;
  - **không điền từ trí nhớ**.
- **Thống kê:**
  - đơn vị lặp là seed huấn luyện;
  - pilot (EXP-02) chỉ mô tả, không p-value;
  - không đổi giả thuyết hay ngưỡng sau khi thấy kết quả. PREREG khoá tại G1.
- **Hành động thay mặt người:** không tự gửi email, mời collaborator, nộp bài hay bấm submit. Chỉ soạn nháp, để thành viên tự làm.
- **Lịch:** không sửa `schedule/tasks.json`. Nếu lịch cần đổi, ghi đề xuất vào ghi chú ngày và báo DAT.
- **Cần người khác** (số liệu, quyết định, review, file): không chờ buổi gặp và không ghi biên bản. Soạn file yêu cầu theo `notes/yeu-cau/README.md`, cho thành viên đọc lại, rồi commit thẳng `main` và push.
- **Khi bị chặn quá 30 phút:**
  - `python scripts/today.py --block <ID> --note "<lý do, chờ ai>"`;
  - viết ví dụ tái hiện nhỏ nhất;
  - comment vào issue liên quan.

## 4. Đóng task
Chỉ đánh dấu xong khi `done_when` đã thật sự đạt:
```bash
python scripts/today.py --done <ID> --evidence "<run ID | commit | đường dẫn file | link PR>"
```
Nếu là second reader:
```bash
python scripts/today.py --approve <ID> --evidence "<dòng review_log | review PR | run ID chạy lại>"
python scripts/today.py --request-changes <ID> --evidence "..." --note "<cần sửa gì>"
```
Nếu task có `issue` và task đó là phần cuối của issue, đề nghị đóng issue (`gh issue close <số> --comment "..."`). Hỏi thành viên trước khi đóng.

Cuối ngày, hoặc khi thành viên nói "xong rồi" hay "kết thúc ngày": dùng skill `ket-thuc-ngay`.
