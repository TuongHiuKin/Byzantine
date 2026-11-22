# Dự án Byzantine FL

Trang này tổng hợp tiến độ nghiên cứu **Federated Learning chống tấn công Byzantine trên dữ liệu giao thông** của nhóm.

## Đọc ở đâu

| Bạn cần | Vào đây |
|---|---|
| Tài liệu chính gửi thầy (đề xuất GAP-1) | [Tài liệu chính](tai-lieu-chinh/index.md) |
| Bài của từng thành viên | [Thành viên](thanh-vien/index.md) |
| Câu hỏi đang xin ý kiến thầy | [Câu hỏi cho thầy](cau-hoi/index.md) |
| Cách đăng bài của mình lên trang | [Hướng dẫn đăng bài](huong-dan-dang-bai.md) |

## Những phần đang làm

*Cập nhật 17/11/2026.*

Câu hỏi chung của đề tài: các bộ gộp chống Byzantine coi client nào "khác đám đông" là đáng ngờ, nhưng trên dữ liệu giao thông thật thì client trung thực cũng khác nhau rất nhiều. Vậy bộ gộp có còn phân biệt được kẻ gian với người trung thực "khác biệt" không? Các phần dưới đây đều phục vụ câu hỏi đó.

| # | Phần đang làm | Tình trạng |
|---|---|---|
| 1 | **Đánh giá dữ liệu**: đặt tiêu chí và đo ra con số cho từng bộ dữ liệu (chia client có nghĩa ngoài đời không, client khác nhau thật đến mức nào, có lỗi tự nhiên không, có biết chắc ai là kẻ gian không) | Đã đo sơ bộ trên LargeST San Diego: 26 tuyến, lưu lượng chênh 18 lần, khác biệt giữa client gấp 3,81 lần so với chia ngẫu nhiên, 2,25 % giá trị bằng 0 |
| 2 | **Chuyển thí nghiệm FL sang dữ liệu thật**: code ByzCity hiện chạy trên dữ liệu sin + nhiễu, không dùng để kết luận được | Code đọc LargeST và VeReMi (`gia_lap_loi/`) đã có, chưa chạy đầy đủ trên dữ liệu thật |
| 3 | **Hoàn thiện đề xuất GAP-1 bản v2** | Đã có bản sửa sau góp ý, còn các chỗ đánh dấu [THIẾU] và [CHỐT] |
| 4 | **Thiết kế thí nghiệm có mốc so sánh**: FedAvg cùng điều kiện, chia client ngẫu nhiên, Local-only, Centralized; chạy đủ seed để kiểm định thống kê | Đang làm, để sửa hai mục thầy chấm thấp (baseline 5/10, thống kê 2/10) |
| 5 | **Dữ liệu HuddsTrafficFL** (Zenodo) | Đã có dữ liệu, chưa dùng |

!!! question "Đang chờ thầy quyết định"
    1. Đề tài đi theo hướng **dự báo lưu lượng** (dữ liệu LargeST, đề xuất v2 dùng được gần như nguyên) hay **phát hiện misbehavior V2X** (dữ liệu VeReMi, phải viết lại câu hỏi và chỉ số)?
    2. Đánh giá dữ liệu là **bước chuẩn bị** cho GAP-1 hay là **một sản phẩm riêng** có câu hỏi nghiên cứu riêng?

## Mới cập nhật

<!-- MOI_CAP_NHAT -->
- **10/11/2026**: [Báo cáo tổng hợp — LargeST-ByzBench](nghien-cuu/bao-cao-tong-hop.md)
- **10/11/2026**: [Đối chiếu bản GAP-1 với dữ liệu đã đo](nghien-cuu/doi-chieu-gap1.md)
- **10/11/2026**: [MLflow cho bản GAP-1 — đo ở ba quy mô](nghien-cuu/mlflow-cho-gap1.md)
- **10/11/2026**: [Đề cương nghiên cứu v3](nghien-cuu/de-xuat-v3.md)
- **10/11/2026**: [Đề xuất GAP-1, bản sửa sau góp ý của thầy (v2)](tai-lieu-chinh/de-xuat-gap1-v2.md)
- **05/11/2026**: [Đề xuất nghiên cứu GAP-1 (bản gửi thầy)](tai-lieu-chinh/de-xuat-gap1.md)
