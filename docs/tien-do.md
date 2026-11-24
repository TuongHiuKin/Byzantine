# Tiến độ chung

Trang này tổng hợp tiến độ nghiên cứu **Federated Learning chống tấn công Byzantine trên dữ liệu giao thông** của nhóm. Việc ưu tiên hiện tại là [nghiên cứu benchmark đánh giá dữ liệu](index.md), theo yêu cầu của thầy: hoàn thành và đưa thầy xem trước khi làm tiếp các phần khác.

## Những phần đang làm

*Cập nhật 24/11/2026.*

| # | Phần đang làm | Tình trạng |
|---|---|---|
| 1 | **Nghiên cứu benchmark đánh giá dữ liệu** (ưu tiên số 1): đặt tiêu chí và đo ra con số cho từng bộ dữ liệu | Đang làm. Đã có khung tiêu chí và số đo sơ bộ trên LargeST San Diego: 26 tuyến, lưu lượng chênh 18 lần, khác biệt giữa client gấp 3,81 lần so với chia ngẫu nhiên, 2,25 % giá trị bằng 0. Ngày 24/11: chốt 8 tiêu chí, câu hỏi nghiên cứu RQ1–RQ3 và kế hoạch giả lập đầu tiên. Xem [trang chính](index.md) |
| 2 | **Chuyển thí nghiệm FL sang dữ liệu thật**: code ByzCity hiện chạy trên dữ liệu sin + nhiễu, không dùng để kết luận được | Code đọc LargeST và VeReMi (`gia_lap_loi/`) đã có, chưa chạy đầy đủ trên dữ liệu thật |
| 3 | **Hoàn thiện đề xuất GAP-1 bản v2** | Đã có bản sửa sau góp ý, còn các chỗ [THIẾU] và [CHỐT]. Tạm dừng đến khi thầy xem xong benchmark |
| 4 | **Thiết kế thí nghiệm có mốc so sánh**: FedAvg cùng điều kiện, chia client ngẫu nhiên, Local-only, Centralized; chạy đủ seed để kiểm định thống kê | Đã có trong v2, theo góp ý của thầy (baseline 5/10, thống kê 2/10) |
| 5 | **Dữ liệu HuddsTrafficFL** (Zenodo) | Dùng làm mốc mô phỏng trong benchmark, không làm dữ liệu chính |

!!! success "Đã chốt (24/11/2026)"
    1. Làm **dự báo lưu lượng trên LargeST trước**, hướng V2X (VeReMi) để giai đoạn sau.
    2. Benchmark đánh giá dữ liệu là **một sản phẩm độc lập**, đồng thời là công cụ dùng được khi triển khai thực tế.

    Câu hỏi còn chờ thầy: xem mục 6 của [trang chính](index.md).

## Mới cập nhật

<!-- MOI_CAP_NHAT -->
- **25/11/2026**: [Hạ tầng triển khai — đo trên máy thật](nghien-cuu/ha-tang-trien-khai.md)
- **24/11/2026**: [Chấm bộ tiêu chí 24/11 lên LargeST — kết quả và ba lỗi thiết kế](nghien-cuu/cham-tieu-chi-24-11.md)
- **24/11/2026**: [Tiêu chí đánh giá dữ liệu và kế hoạch giả lập đầu tiên](index.md) (thay trang chính; bản 23/11 chuyển vào [Lưu trữ](benchmark-ban-23-11.md))
- **23/11/2026**: [Malkani (2026) — phân tích và đối chiếu](nghien-cuu/phan-tich-malkani.md)
- **10/11/2026**: [Báo cáo tổng hợp — LargeST-ByzBench](nghien-cuu/bao-cao-tong-hop.md)
- **10/11/2026**: [Đối chiếu bản GAP-1 với dữ liệu đã đo](nghien-cuu/doi-chieu-gap1.md)
- **10/11/2026**: [MLflow cho bản GAP-1 — đo ở ba quy mô](nghien-cuu/mlflow-cho-gap1.md)
- **10/11/2026**: [Đề cương nghiên cứu v3](nghien-cuu/de-xuat-v3.md)
- **10/11/2026**: [Đề xuất GAP-1, bản sửa sau góp ý của thầy (v2)](tai-lieu-chinh/de-xuat-gap1-v2.md)
- **05/11/2026**: [Đề xuất nghiên cứu GAP-1 (bản gửi thầy)](tai-lieu-chinh/de-xuat-gap1.md)
