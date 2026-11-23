# Tiến độ chung

Trang này tổng hợp tiến độ nghiên cứu **Federated Learning chống tấn công Byzantine trên dữ liệu giao thông** của nhóm. Việc ưu tiên hiện tại là [nghiên cứu benchmark đánh giá dữ liệu](index.md), theo yêu cầu của thầy: hoàn thành và đưa thầy xem trước khi làm tiếp các phần khác.

## Những phần đang làm

*Cập nhật 23/11/2026.*

| # | Phần đang làm | Tình trạng |
|---|---|---|
| 1 | **Nghiên cứu benchmark đánh giá dữ liệu** (ưu tiên số 1): đặt tiêu chí và đo ra con số cho từng bộ dữ liệu | Đang làm. Đã có khung tiêu chí và số đo sơ bộ trên LargeST San Diego: 26 tuyến, lưu lượng chênh 18 lần, khác biệt giữa client gấp 3,81 lần so với chia ngẫu nhiên, 2,25 % giá trị bằng 0. Xem [trang chính](index.md) |
| 2 | **Chuyển thí nghiệm FL sang dữ liệu thật**: code ByzCity hiện chạy trên dữ liệu sin + nhiễu, không dùng để kết luận được | Code đọc LargeST và VeReMi (`gia_lap_loi/`) đã có, chưa chạy đầy đủ trên dữ liệu thật |
| 3 | **Hoàn thiện đề xuất GAP-1 bản v2** | Đã có bản sửa sau góp ý, còn các chỗ [THIẾU] và [CHỐT]. Tạm dừng đến khi thầy xem xong benchmark |
| 4 | **Thiết kế thí nghiệm có mốc so sánh**: FedAvg cùng điều kiện, chia client ngẫu nhiên, Local-only, Centralized; chạy đủ seed để kiểm định thống kê | Đã có trong v2, theo góp ý của thầy (baseline 5/10, thống kê 2/10) |
| 5 | **Dữ liệu HuddsTrafficFL** (Zenodo) | Dùng làm mốc mô phỏng trong benchmark, không làm dữ liệu chính |

!!! question "Đang chờ thầy quyết định"
    1. Đề tài đi theo hướng **dự báo lưu lượng** (dữ liệu LargeST) hay **phát hiện misbehavior V2X** (dữ liệu VeReMi)?
    2. Benchmark đánh giá dữ liệu là **bước chuẩn bị** cho GAP-1 hay là **một sản phẩm riêng** có câu hỏi nghiên cứu riêng?

## Mới cập nhật

<!-- MOI_CAP_NHAT -->
- **23/11/2026**: [Malkani (2026) — phân tích và đối chiếu](nghien-cuu/phan-tich-malkani.md)
- **10/11/2026**: [Báo cáo tổng hợp — LargeST-ByzBench](nghien-cuu/bao-cao-tong-hop.md)
- **10/11/2026**: [Đối chiếu bản GAP-1 với dữ liệu đã đo](nghien-cuu/doi-chieu-gap1.md)
- **10/11/2026**: [MLflow cho bản GAP-1 — đo ở ba quy mô](nghien-cuu/mlflow-cho-gap1.md)
- **10/11/2026**: [Đề cương nghiên cứu v3](nghien-cuu/de-xuat-v3.md)
- **10/11/2026**: [Đề xuất GAP-1, bản sửa sau góp ý của thầy (v2)](tai-lieu-chinh/de-xuat-gap1-v2.md)
- **05/11/2026**: [Đề xuất nghiên cứu GAP-1 (bản gửi thầy)](tai-lieu-chinh/de-xuat-gap1.md)
