# LDN → FAO: góp ý second reader 4 Form B (W2-FAO-01) — 02/11/2026

> Trả lời bằng dòng `FAO:` dưới mục. Quy ước: `notes/yeu-cau/README.md`.
> LDN đã **duyệt** W2-FAO-01 (đối chiếu 01/11: Abd-Elmagid qua ar5iv, Liu và Sun qua bản HTML arXiv, OH-DRL qua tóm tắt trên OpenAlex). Các hàng ma trận khớp với bài. Góp ý dưới đây đều nhỏ, không đổi hàng ma trận; sửa khi tiện, không chặn G0.

## A1. Abd-Elmagid 2019 (`abdelmagid2019deep_FAO.md`)
- §IV-C (bàn Fig. 5a) viết chính sách distance-based "has to satisfy the time constraint", nên câu "distance-based không tính đến ràng buộc thời gian τ hay ô đích" mâu thuẫn với bài; nên sửa.
- Có thể thêm: trạng thái (§II-B) chỉ gồm (pin, AoI) của nút và (vị trí UAV, thời gian dư), không chứa vị trí nút. Điều này củng cố ô "Không" ở cột nhiều bố trí.
- Nhỏ: phần cập nhật trọng số trong Algorithm 1 là dòng 14–19 theo bản HTML, không phải 13–17.

FAO: (02/11) Đồng ý cả 3 ý; đã sửa `abdelmagid2019deep_FAO.md`. Đối chiếu ar5iv: câu Fig. 5a là "the distance-based policy stays constant after e_max=2^5 because the agent has to satisfy the time constraint"; định nghĩa ở đoạn đầu §IV-C không nhắc τ hay ô đích. Form B nay ghi cả hai, và ghi rằng bài không mô tả cơ chế thoả ràng buộc. Thêm câu trạng thái không chứa vị trí nút (§II-B, vị trí chỉ vào PT (1), (3)–(4)). Algorithm 1 sửa thành dòng 14–19.

## A2. Liu 2024 (`liu2024generalizable_FAO.md`)
- Các tỉ lệ 98/55/37/26% của Fig. 6 không có trong văn bản §IV-A, chỉ đọc được từ hình. Nên ghi "đọc từ hình" như cách Form B Sun đã làm.

FAO: (02/11) Đồng ý; đã ghi "đọc từ hình" trong `liu2024generalizable_FAO.md`. Văn bản §IV-A và chú thích Fig. 6 không có số nào.

## A3. Sun 2025 (`sun2025aoi_FAO.md`)
- Đã kiểm khớp: tốc độ hằng số (§III-A), v = 5 m/s, N_D = 10, P_α = 14,7517 W, P_β = 41,5409 W, v_tip = 80 m/s, v₀ = 5,0463 m/s (Bảng IV), DR là hướng tương lai (§VII), vùng tô "variance" (§V-B1).
- LDN chưa tìm thấy trong văn bản câu "MAPPO-TM có peak AoI thấp hơn 5–10% ở mọi η_le" (§V-B2). FAO kiểm lại nguồn câu này; nếu là số đọc từ hình thì ghi rõ.

FAO: (02/11) Câu này có trong §V-B2 (bản HTML arXiv v1, đoạn bàn Fig. 4(b)): "MAPPO-TM consistently outperforms other algorithms across different η_le values, achieving a 5-10% lower peak AoI." Đây là số tác giả viết, không phải đọc từ hình. Câu không nêu so với thuật toán nào và không tách theo η_le. Đã chép nguyên văn vào `sun2025aoi_FAO.md`; nhận xét "tại η_le = 0,25 hai đường gần trùng" vẫn giữ, vì đó là số FAO đọc từ hình.

## A4. OH-DRL 2025 (`ohdrl2025_FAO.md`)
- Tóm tắt trên OpenAlex khớp Form B; danh sách 7 tác giả khớp.
- Tóm tắt có câu "achieves better convergence performance and energy-saving efficiency across different network scales". Nên sửa "Tóm tắt không nhắc tới tổng quát hoá hay kịch bản chưa thấy" thành "tóm tắt chỉ nhắc đánh giá ở nhiều quy mô mạng; không rõ có huấn luyện lại cho mỗi quy mô".
- OpenAlex (01/11): đóng truy cập, `any_repository_has_fulltext = false`; có một mục figshare nhưng không có PDF. DAT sẽ nhờ GVHD/thư viện (DAT 01/11).
- Cột 6 mới "Đối chứng huấn luyện trên bố trí cố định" (DECISIONS 2026-11-01): FAO điền cho 4 hàng của mình trước T3 03/11.

FAO: (02/11) A4: đã sửa câu tổng quát hoá theo đề xuất; tóm tắt đối chiếu trên UniSC và OpenAlex W4408145075 (cùng nội dung; OpenAlex `is_oa = false`, `any_repository_has_fulltext = false`). Cột 6: đã thêm cột vào header bảng `docs/04` §5 (các hàng khác để "(người đọc hàng này điền)") và điền 4 hàng của FAO: Abd-Elmagid, Sun, Liu = Không; OH-DRL = Chưa rõ; mỗi ô có mục. Mỗi Form B cũng có dòng cột 6.
