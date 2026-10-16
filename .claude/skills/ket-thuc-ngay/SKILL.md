---
name: ket-thuc-ngay
description: Dùng khi thành viên nói "kết thúc ngày", "xong rồi", "tổng kết hôm nay", "end of day" trong repo uav-aoi-drppo. Ghi chú ngày Form H, cập nhật trạng thái, commit và push.
---

# Kết thúc ngày

1. `python scripts/today.py --json` để biết task nào đang `doing` và task nào hạn hôm nay chưa xong.
2. Với mỗi task đã làm trong ngày:
   - Nếu đạt `done_when`: `python scripts/today.py --done <ID> --evidence "..."`.
   - Nếu chưa xong: giữ trạng thái `doing`, ghi phần còn lại vào ghi chú.
   - Nếu bị chặn: `--block <ID> --note "..."`.
3. Tạo khung ghi chú ngày bằng `python scripts/today.py --note-file`, rồi điền Form H **từ việc thật đã làm hôm nay**:
   - **Hôm nay biết thêm điều gì:** một câu. Không viết kiểu "đã làm mô hình".
   - **Bằng chứng:** run ID, commit hash, đường dẫn hình hoặc file. Bắt buộc có.
   - **Điều còn chưa chắc.**
   - **Thực nghiệm nhỏ nhất có tính quyết định cho ngày mai.**
   - **Owner và second reader.**
   - **Cần giúp gì:** kèm ví dụ tái hiện nhỏ nhất. Ghi "không" nếu không cần.

   Đưa bản điền cho thành viên đọc và sửa trước khi commit.
4. Commit chỉ những file của mình, gồm ghi chú ngày, `schedule/status/<NICK>.json`, và các file kết quả hoặc ghi chú của task:
   ```bash
   git add notes/<ngày>_<nick>.md schedule/status/<NICK>.json <các file khác của task>
   git commit -m "[<NICK>] <YYYY-MM-DD>: <tóm tắt 1 dòng>"
   git pull --rebase && git push
   ```
   Mã trong `src/` và `scripts/` không push thẳng: chúng nằm trên nhánh riêng với PR.
5. Nếu task có issue, comment tiến độ 1–2 dòng vào issue kèm bằng chứng, nếu `gh` dùng được. Hỏi thành viên trước khi gửi.
6. Kết thúc bằng 2 dòng:
   - việc đầu tiên ngày mai, lấy từ `python scripts/today.py --date <ngày mai>`;
   - ai đang chờ thành viên (`waiting_on_me`).
