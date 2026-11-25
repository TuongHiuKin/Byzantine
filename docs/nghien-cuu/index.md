# Nghiên cứu của Nguyễn Quang Huy

Phần này tập hợp công việc của **Nguyễn Quang Huy (SE194177)** trong dự án — gồm kiểm chứng khoảng trống nghiên cứu, đề cương v3, đối chiếu bản đề xuất của nhóm với dữ liệu đã đo, và đánh giá công cụ theo dõi thí nghiệm.

Mọi con số trong các tài liệu dưới đây đọc từ tệp kết quả đã sinh, không tính lại bằng tay. Các bộ kiểm chứng chạy lại được và trả mã lỗi khi có sai lệch.

## Danh sách tài liệu

- **[Giao thức chốt trước khi chạy — PROTOCOL (25/11/2026)](protocol.md)** — Khoá 12 luật trước khi có vòng FL đầu tiên: đơn vị 'một vòng', `R_conv`, mẫu số FedAvg, 10 seed + Holm + TOST, điều kiện hợp lệ, cổng dừng, luật cắt, phân vùng P-A và nguồn sự thật là CSV. Kèm nhật ký pre-registration.
- **[Khuyến nghị chọn mục tiêu đánh giá](khuyen-nghi-muc-tieu.md)** — Tổng hợp bốn nguồn bằng chứng: chọn cái giá của phòng thủ làm mục tiêu chính, tấn công cảm biến làm phụ, loại tấn công mô hình thuần.
- **[Báo cáo tổng hợp — LargeST-ByzBench](bao-cao-tong-hop.md)** — Tổng hợp bốn nhánh công việc: kiểm chứng 93 công trình, đề cương v3, đối chiếu bản GAP-1, và đánh giá MLflow.
- **[Đề cương nghiên cứu v3 — LargeST-ByzBench](de-xuat-v3.md)** — Bản đề cương sửa theo 18 hạng mục góp ý của giảng viên hướng dẫn. Ma trận 22.240 lần chạy, thiết kế thống kê chốt trước.
- **[Đối chiếu bản GAP-1 với dữ liệu đã đo](doi-chieu-gap1.md)** — Kiểm bốn con số dữ liệu trong bản đề xuất GAP-1: ba đúng, một không có trong bài gốc. Kèm phân tích thiết kế thống kê.
- **[Số test case cho GAP-1 ở 716 node](so-test-case-716-node.md)** — Bao nhiêu lần chạy cho một thành phố ít node nhất: 2.060 bắt buộc, 7.820 đầy đủ, 11.730 nếu mở cả ba mức client.
- **[Bài báo liên quan — LargeST và GAP-1](bai-bao-lien-quan.md)** — 114 bài trích dẫn LargeST: 1 bài có học liên kết, 0 bài có Byzantine. Khảo sát mới nhất 10/11/2026.
- **[Phân tích báo cáo Stanford AIMS](phan-tich-bao-cao-aims.md)** — Kiểm chứng báo cáo crawl 270 benchmark AIMS: số liệu đúng, nhưng viết cho dự án khác và áp IRT sai giả định.
- **[Đo chỉ số thí nghiệm theo chuẩn AIMS](do-luong-chi-so-aims.md)** — AIMS loại trừ adversarial robustness khỏi phạm vi. Khung Subject-Item dùng được, torch_measure chưa nên dùng, và grid ByzCity chưa có cột kết quả.
- **[MLflow cho LargeST-ByzBench — đo ở đúng quy mô](mlflow-quyet-dinh.md)** — Cài MLflow 3.18.0, ghi **2.220 lần chạy × 34 chỉ số** thật: **68,7 ms/lần**, 37,4 MB, truy vấn toàn bộ 3.260 ms. So cùng quy mô với CSV (0,02 ms) và SQLite (0,02 ms) → **MLflow chậm 3.435 lần**. Khuyến nghị: **ghi bằng CSV, xem bằng MLflow**.
- **[Hạ tầng triển khai — đo trên máy thật](ha-tang-trien-khai.md)** — Ryzen 7 6800H (16 luồng), 31,2 GiB RAM, RTX 3050 4 GB. Đo thật: **44.199 cửa sổ/giây** trên CPU; một vòng **0,267 h** nếu duyệt toàn bộ, **0,0058 h** nếu lấy mẫu — chênh **46 lần**. Ngân sách 0,35 h/lần của đề cương chỉ đúng ở định nghĩa thứ hai, và đề cương không ghi nó giả định cái nào.
- **[Chấm bộ tiêu chí 24/11 lên LargeST — kết quả và ba lỗi thiết kế](cham-tieu-chi-24-11.md)** — Chạy đúng 7 tiêu chí đo được của trang chủ lên HDF5 gốc: T2 2,161 %, T3 2,79 %, F2 3,386×, F3 Gini 0,401, B3 59,09 %, K2 R² 0,8667, K3 0,19–0,53. **6/21 điểm** — rubric tự loại bộ dữ liệu nó chọn. Kèm ba lỗi công thức (K2 dùng sai đại lượng, K3 không thể đạt kể cả năm COVID, B3 ngoài băng).
- **[Phân tích Malkani (2026) — "Who Pays for Byzantine Robustness?"](phan-tich-malkani.md)** — Đọc toàn văn arXiv:2611.22904: ba câu hỏi nghiên cứu, tám bộ gộp trên phân vùng bệnh viện thật, 54.214 lần chạy. Phát hiện trung tâm: 97 % mức sụt mà người ta quy cho tấn công thực ra là mất dữ liệu. Kèm đối chiếu với phân vùng P-A 22 client.
- **[MLflow cho bản GAP-1 — đo ở ba quy mô](mlflow-cho-gap1.md)** — Đánh giá MLflow cho ma trận thí nghiệm 375 / 5.145 / 10.290 lần chạy. Kết luận đảo chiều theo quy mô.

## Ghi chú về trạng thái

| Tài liệu | Trạng thái |
|---|---|
| Báo cáo tổng hợp | Hoàn chỉnh, đã kiểm chứng 92 phép |
| Đề cương v3 | Hoàn chỉnh, chờ phản hồi của giảng viên |
| Đối chiếu GAP-1 | Hoàn chỉnh, đã gửi nhóm |
| Số test case ở 716 node | Hoàn chỉnh, 54 phép kiểm |
| Bài báo liên quan | Hoàn chỉnh, khảo sát 114 bài trích dẫn |
| Phân tích báo cáo AIMS | Hoàn chỉnh, 45 phép kiểm |
| Đo chỉ số theo AIMS | Hoàn chỉnh, 47 phép kiểm |
| Khuyến nghị mục tiêu | Hoàn chỉnh, 95 phép kiểm — bản tổng hợp |
| MLflow cho GAP-1 | Hoàn chỉnh, kèm số đo thực nghiệm |
