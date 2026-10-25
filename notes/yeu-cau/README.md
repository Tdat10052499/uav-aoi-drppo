# Yêu cầu giữa các thành viên

> Từ 25/10/2026 nhóm không ghi biên bản họp (`docs/DECISIONS.md`). Câu hỏi, yêu cầu số liệu và việc cần người khác làm được trao đổi qua các file trong thư mục này. Claude của người nhận đọc chúng khi người đó hỏi "hôm nay tôi cần làm gì?".

## Gửi yêu cầu
1. Tạo file `notes/yeu-cau/<YYYY-MM-DD>_<nick người gửi>_can-<NICK người nhận>_<chủ-đề>.md`, ví dụ `2026-10-27_ldn_can-DAT_steps-per-s.md`.
2. Mỗi việc là một mục, có tiêu đề dạng `## A1. <câu hỏi hoặc việc cần làm>`. Mỗi mục ghi:
   - cần gì, cụ thể (số liệu nào, file nào, quyết định nào);
   - để làm gì, và task hoặc gate nào đang chờ;
   - hạn mong muốn.
3. Commit thẳng `main` với message `[NICK] YYYY-MM-DD: yêu cầu <NICK> ...`, rồi push.

## Trả lời
- Viết một dòng bắt đầu bằng `<NICK>:` ngay dưới mục, ví dụ `DAT: giữ 200k, chỉ chạy DQN trên máy LDN.` Có thể thêm link commit, PR, run ID.
- Mục có dòng trả lời được coi là đã xử lý. Mục chưa có dòng trả lời hiện trong `python scripts/today.py` của người nhận, ở mục **YÊU CẦU GỬI BẠN**. Người gửi thấy nó ở mục **BẠN ĐANG CHỜ NGƯỜI KHÁC TRẢ LỜI**.
- Không xoá file hay mục đã trả lời: đây là nhật ký quyết định của nhóm. Quyết định về thiết kế hoặc lịch thì ghi thêm vào `docs/DECISIONS.md`.

Các file cũ `notes/<ngày>_<nick>_can-<NICK>.md` (ví dụ của FAO ngày 21–22/10) vẫn được `today.py` đọc theo cùng quy ước.
