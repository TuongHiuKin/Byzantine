# Nghiên cứu benchmark đánh giá dữ liệu (bản 23/11)

!!! note "Bản lưu trữ"
    Đây là trang chính bản 23/11/2026, **chưa gửi thầy**, giữ nguyên để dùng lại sau. Bản hiện hành ở [trang chính](index.md).

*Dự án Federated Learning chống tấn công Byzantine trên dữ liệu giao thông · cập nhật 23/11/2026*

!!! info "Tình trạng"
    **Đang làm, chưa gửi thầy.** Thầy yêu cầu nhóm nghiên cứu benchmark đánh giá dữ liệu và đưa thầy xem **trước khi** làm tiếp đề xuất GAP-1. Vì vậy trang chính chỉ trình bày phần này. Tiến độ các phần khác ở trang [Tiến độ chung](tien-do.md).

## 1. Vì sao phải đánh giá dữ liệu trước

Các bộ gộp chống Byzantine (Krum, Median, Trimmed Mean…) đều dựa trên một giả định: **client trung thực gửi cập nhật giống nhau, ai khác hẳn thì đáng ngờ**. Trên dữ liệu giao thông thật, giả định này dễ bị vỡ. Ở LargeST San Diego, tuyến I15 hướng Bắc trung bình 414 xe mỗi 15 phút, còn SR11 hướng Đông chỉ 23 xe, chênh 18 lần. Cả hai đều trung thực, nhưng bộ gộp có thể coi SR11 là kẻ gian (loại nhầm), hoặc kẻ gian khéo léo trốn được trong đám client vốn đã khác nhau (bỏ lọt).

Muốn đo hiện tượng này, **dữ liệu phải thật sự chứa những khác biệt đó**. Dữ liệu "sạch" chưa chắc đã "phù hợp": dữ liệu sin + nhiễu đang dùng trong code ByzCity không có lỗi nào, nhưng chỉ cần biết giờ trong ngày là đã đoán đúng 98 % phương sai, nên không trả lời được câu hỏi của đề tài.

Đánh giá dữ liệu ở đây không hỏi "dữ liệu này tốt không", mà hỏi:

> **Dữ liệu này có chứa những điều kiện mà câu hỏi nghiên cứu cần quan sát không, và chứa nhiều cỡ nào?**

## 2. Một benchmark gồm những gì

Một benchmark là một **gói quy tắc thi** để so sánh công bằng, không chỉ là một bộ dữ liệu. Các benchmark nghiêm túc (LargeST, LEAF, FLamby, Blades, ByzFL…) thường có 8 phần:

| # | Thành phần | Trả lời câu hỏi |
|---|---|---|
| 1 | Mục tiêu và phạm vi | Đo năng lực gì, trong bối cảnh nào, cái gì **không** đo |
| 2 | Nhiệm vụ | Đầu vào là gì, đầu ra là gì |
| 3 | Dữ liệu | Lấy từ đâu, xử lý thế nào, giấy phép gì |
| 4 | Cách chia dữ liệu | Train/val/test và cách chia client |
| 5 | Giao thức đánh giá | Bao nhiêu lần chạy, seed nào, tinh chỉnh tham số đến đâu |
| 6 | Chỉ số | Đo bằng con số nào, con số nào là chính |
| 7 | Baseline | So với cái gì để biết một con số là tốt hay xấu |
| 8 | Bộ công cụ tái lập | Người khác chạy lại có ra đúng số không |

Benchmark FL và Byzantine có thêm: mô hình FL (số client, số vòng), kiểu dị biệt (tự nhiên hay Dirichlet), mô hình đe dọa, ma trận tấn công × phòng thủ, và đánh dấu các ô vi phạm giả định lý thuyết (Krum cần n ≥ 2f + 3).

**Một benchmark tốt** phải đạt bốn nhóm tiêu chí (tổng hợp từ BetterBench, NeurIPS 2024):

| Nhóm | Nội dung | Ví dụ không đạt |
|---|---|---|
| **A. Đo đúng thứ cần đo** | Con số phản ánh đúng năng lực; điều kiện giống thực tế; nói rõ phạm vi áp dụng | Chỉ báo MAE trung bình rồi kết luận "chống tấn công tốt" |
| **B. Phân biệt được phương pháp** | Bài toán không quá dễ, không quá khó; khác biệt lớn hơn dao động giữa các seed; thứ hạng bền | Một luật ngưỡng đơn giản đã đạt F1 0,99 |
| **C. So sánh công bằng, đáng tin** | Cùng điều kiện cho mọi phương pháp; đủ baseline; đủ seed và hiệu chỉnh thống kê; không rò rỉ tập test | 3 seed, so bằng mắt |
| **D. Người khác dùng lại được** | Code, cấu hình, seed công khai; có datasheet và giấy phép; chi phí chạy hợp lý | Số liệu trong báo cáo không do code sinh ra |

## 3. Khoảng trống của nhóm

Các khung đánh giá hiện có chia làm hai phía không nối với nhau:

- **Chất lượng dữ liệu** (Datasheets, ISO/IEC 25012): chấm dữ liệu tự thân, như thiếu, sai, có ghi nguồn không.
- **Benchmark FL/Byzantine** (LEAF, FLamby, Blades, ByzFL): coi dữ liệu là cho sẵn, chỉ chấm thuật toán.

Theo khảo sát nhanh, **chưa thấy ai chấm một bộ dữ liệu theo câu hỏi "bộ này có làm lộ ra hành vi của bộ gộp chống Byzantine không"**. Nhận định này còn cần một đợt rà soát có hệ thống để kiểm lại.

Danh sách các bài báo và repo đã tìm được, phần nào đã có người làm và phần nào chưa, xem trang **[Khảo sát công trình liên quan](khao-sat-lien-quan.md)** (cập nhật 23/11/2026).

## 4. Bộ tiêu chí đề xuất

Bốn tầng, mỗi tiêu chí chấm 0–3 điểm (0 = không dùng được cho câu hỏi đó, 3 = rất tốt). Tầng 1–2 lấy lại của người khác, **tầng 3–4 là phần mới**. Các ngưỡng là đề xuất ban đầu, sẽ hiệu chỉnh ở bước E1.

| Tầng | Mã | Tiêu chí | 3 điểm khi |
|---|---|---|---|
| **1. Dữ liệu có đáng tin không** | T1 | Mức thật (đo thật / mô phỏng hiệu chỉnh / mô phỏng thuần / hàm tổng hợp) | Đo thật |
| | T2 | Đầy đủ: tỉ lệ ô thiếu, tính trên file gốc trước khi điền | ≤ 1 % |
| | T3 | Hợp lệ: ô đứng yên lâu, chạm trần, giá trị âm | ≤ 0,5 % |
| | T4 | Quy mô và độ phủ | ≥ 500 nút và ≥ 2 năm |
| | T5 | Tái lập và giấy phép | Có nguồn cố định, script, giấy phép, mã băm |
| **2. Chia client có ý nghĩa không** | F1 | Phân vùng client tự nhiên (tuyến đường, khu vực, RSU…) | Có khóa thật, ≥ 15 nhóm |
| | F2 | Dị biệt tự nhiên: EMD khi chia tự nhiên ÷ EMD khi chia ngẫu nhiên | ≥ 3 |
| | F3 | Lệch kích thước client (hệ số Gini) | Trong khoảng 0,2–0,4 |
| | F4 | Lợi ích FL: Centralized tốt hơn Local-only bao nhiêu | ≥ 10 % và ≥ 80 % client có lợi |
| **3. Có làm lộ hành vi bộ gộp không** (mới) | B1 | **HDR**: độ phân tán cập nhật trung thực khi chia tự nhiên ÷ khi chia ngẫu nhiên | ≥ 2 |
| | B2 | Độ tập trung của độ lệch: 20 % client lệch nhất chiếm bao nhiêu | Báo cáo, không chấm |
| | B3 | Lỗi tự nhiên trông giống tấn công: tỉ lệ client trung thực bị luật chất lượng gắn cờ | 10–40 % |
| | B4 | Tiêm được tấn công mà vẫn biết chắc nhãn | Tiêm được cả hai loại, ≥ 2 kênh |
| | B5 | Nhãn misbehavior có sẵn (chỉ hướng V2X) | ≥ 10 kiểu |
| | B6 | Đủ client cho lý thuyết (n ≥ 2f + 3) | n ≥ 15 |
| **4. Khớp nhiệm vụ và chuyển giao** | K1 | Khớp bài toán (hồi quy hay phân loại) | Khớp trực tiếp |
| | K2 | **Không tầm thường**: một luật đơn giản đã giải được chưa | Dự báo: giờ trong ngày giải thích ≤ 70 % phương sai |
| | K3 | Trôi phân phối theo thời gian | ≥ 3 lần, có sự kiện đã biết |
| | K4 | **Dấu vân tay mô phỏng – thực**: so 5 thống kê với dữ liệu thật | Mọi thống kê nằm trong khoảng của dữ liệu thật |

Tiêu chí HDR có thể hiểu thế này: mỗi client "kéo" mô hình về phía dữ liệu của mình. Nếu các client trung thực kéo gần cùng hướng, bộ gộp dễ thấy kẻ kéo ngược. HDR = 2 nghĩa là các lực kéo trung thực phân tán gấp đôi so với khi chia ngẫu nhiên.

## 5. Chấm thử các bộ dữ liệu

**Số in đậm** là đã đo; số thường là suy từ mô tả công khai; `?` là chưa đo.

| Tiêu chí | Sin + nhiễu (ByzCity) | LargeST SD | HuddsTrafficFL | VeReMi Extension |
|---|---|---|---|---|
| Bài toán | Dự báo | Dự báo | Phát hiện bất thường | Phát hiện misbehavior |
| T1 Mức thật | 0 | **3** (PeMS) | 1 (SUMO) | 1 (mô phỏng) |
| T4 Quy mô | 1 | **3** (716 nút, 2017–2021) | 2 | 2 |
| T5 Giấy phép | 0 | 2 | 1 (CC BY-NC-ND) | 3 |
| F1 Phân vùng tự nhiên | 0 | **3** (26 hành lang) | 2 | 2 |
| F2 Dị biệt tự nhiên | **0** (0,92) | **3** (3,81) | ? | ? |
| B1 HDR | **0** (1,05) | ? | ? | ? |
| B5 Nhãn sẵn | 0 | 0 (tự tiêm) | 2 | 3 (khoảng 19 kiểu) |
| K2 Không tầm thường | **0** (0,98) | ? | cần đo | cần đo |
| K3 Trôi | **0** | **3** (COVID 2020) | 1 | 0 |

## 6. Chọn dữ liệu

| Bộ dữ liệu | Vai trò | Lý do |
|---|---|---|
| **LargeST San Diego** | **Bộ chính** | Mạnh nhất ở mức thật, phân vùng client tự nhiên, dị biệt và trôi phân phối. Thầy đã ghi trong góp ý là bộ này đủ cho giai đoạn đầu. Điểm yếu (một kênh lưu lượng, không có nhãn sẵn) không chặn đề tài vì nhóm tự tiêm tấn công |
| HuddsTrafficFL | Mốc mô phỏng | Dùng để so "mô phỏng khác thật ở đâu" (K4). Không làm bộ chính vì giấy phép không cho sửa rồi phát hành lại, và số client chưa khớp |
| VeReMi Extension | Phép thử hướng V2X | Chỉ chạy phép thử "có quá dễ không" (K2). Nếu một luật ngưỡng đã đạt F1 > 0,9 thì hướng V2X yếu ngay từ dữ liệu |
| Sin + nhiễu | Chỉ kiểm tra code | Trượt gần mọi tiêu chí quan trọng, không dùng để kết luận |
| SUMO tự sinh | Bù chỗ thiếu | Chỉ sinh khi cần "núm vặn", ví dụ HDR = 1, 2, 3, 4 để vẽ đường liều – đáp ứng |

Việc cần làm ngay: đọc LargeST SD từ **file HDF5 gốc** (bản parquet đã điền số 0, che mất chỗ thiếu dữ liệu), rồi đo ba số còn thiếu là T2, B1 và K2.

## 7. Các bước thực hiện

Đi từ rẻ đến đắt. E0 và E1 không cần huấn luyện FL, chạy được trên laptop.

| Bước | Làm gì | Đầu ra |
|---|---|---|
| **E0** | Chấm điểm mọi bộ dữ liệu bằng script `cham_du_lieu.py` | Bảng ở mục 5 không còn ô `?`. Nếu HDR của LargeST SD < 1,5 thì chuyển sang LargeST CA/GBA |
| **E1** | Kiểm tra thước đo có ổn định không: lặp với 10 seed, 5 tập con cảm biến, 3 năm | Chỉ số nào dao động > 15 % hoặc làm đổi thứ hạng thì không dùng |
| **E2** | Chỉ số dữ liệu có dự báo được hành vi bộ gộp không: khoảng 15 cặp (dữ liệu, cách chia), 5 bộ gộp khi sạch, 5 seed | Tương quan giữa HDR và tỉ lệ loại nhầm (FPR). Giả thuyết: Spearman ≥ 0,6 với Krum |
| **E3** | Núm vặn dị biệt: trộn cảm biến theo tỉ lệ α từ 0 (ngẫu nhiên) đến 1 (theo hành lang), so với chia Dirichlet | Đồ thị HDR – FPR, đọc được "giao thông thật tương đương Dirichlet α bao nhiêu" |
| **E4** | Phép thử tầm thường trên dữ liệu có nhãn (VeReMi, HuddsTrafficFL) | Kiểu tấn công nào bị một luật đơn giản bắt với F1 ≥ 0,9 thì loại |
| **E5** | Dấu vân tay mô phỏng – thực: thống kê nào khác thì làm thử bản LargeST "kéo về phía mô phỏng" ở đúng thống kê đó | Biết thống kê nào làm đổi kết luận về bộ gộp. Thay cho ablation R0–R4 |

**Lịch đề nghị:** tuần 1 làm E0 trên LargeST SD và HuddsTrafficFL, E4 trên VeReMi. Tuần 2 làm E1 và chốt ngưỡng các tiêu chí **trước khi** nhìn kết quả bộ gộp. E2 và E3 dùng chung lần chạy với phần "cái giá của phòng thủ" của GAP-1 ở tuần 4–6.

Từ bộ tiêu chí này có thể rút ra một câu hỏi nghiên cứu kiểm chứng được: **các chỉ số đo trên dữ liệu, trước khi huấn luyện, có dự báo được bộ gộp sẽ loại nhầm client trung thực bao nhiêu và gãy ở đâu không?**

## 8. Câu hỏi xin ý kiến thầy

1. Thầy muốn benchmark dữ liệu là **một sản phẩm riêng** (bảng điểm dữ liệu, công bố được) hay là **bước chuẩn bị** cho GAP-1? Nếu là sản phẩm riêng, câu hỏi ở cuối mục 7 sẽ thành câu hỏi nghiên cứu chính.
2. Về hướng dự báo hay V2X: em đề nghị chạy phép thử E4 trước (dưới 1 giờ máy) rồi mới chốt.
3. Ngưỡng 0–3 điểm của các tiêu chí: thầy muốn dựa theo chuẩn nào (ví dụ ISO/IEC 25012), hay để nhóm hiệu chỉnh bằng bước E1?

??? note "Tài liệu tham khảo"
    - Reuel A. và cs. *BetterBench: Assessing AI Benchmarks, Uncovering Issues, and Establishing Best Practices*. NeurIPS 2024 Datasets and Benchmarks. arXiv:2411.12990.
    - Gebru T. và cs. *Datasheets for Datasets*. Communications of the ACM, 2021.
    - Wu R., Keogh E. *Current Time Series Anomaly Detection Benchmarks are Flawed and are Creating the Illusion of Progress*. IEEE TKDE, 2021. arXiv:2009.13807.
    - Dehghani M. và cs. *The Benchmark Lottery*. arXiv:2107.07002, 2021.
    - Raji I. D. và cs. *AI and the Everything in the Whole Wide World Benchmark*. NeurIPS 2021 Datasets and Benchmarks.
    - Caldas S. và cs. *LEAF: A Benchmark for Federated Settings*. arXiv:1812.01097.
    - Ogier du Terrail J. và cs. *FLamby*. NeurIPS 2022.
    - Li S. và cs. *Blades: A Unified Benchmark Suite for Byzantine Attacks and Defenses in Federated Learning*. arXiv:2206.05359.
    - Liu X. và cs. *LargeST: A Benchmark Dataset for Large-Scale Traffic Forecasting*. NeurIPS 2023. arXiv:2306.08259.
