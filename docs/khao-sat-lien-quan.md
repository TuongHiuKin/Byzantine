# Khảo sát công trình liên quan: phần nào đã có, phần nào chưa ai làm

*Phục vụ nghiên cứu benchmark đánh giá dữ liệu · tra cứu ngày 23/11/2026*

!!! info "Đọc nhanh"
    - **Chưa tìm thấy công trình nào làm đúng hướng của nhóm:** dùng thước đo tính trên dữ liệu **trước khi huấn luyện** để biết một bộ dữ liệu có làm lộ hành vi của bộ gộp chống Byzantine không (gãy ở đâu, loại nhầm client trung thực nào).
    - **Hai phía đã có "viên gạch" nhưng chưa ai nối lại:** phía *đo dữ liệu* (đo dị biệt, đo đặc tính chuỗi thời gian, khung chất lượng dữ liệu giao thông) và phía *hành vi bộ gộp trên dữ liệu thật* (ai bị loại nhầm, bộ gộp nào gãy).
    - **Có nhóm đi rất gần** và mới công bố trong tháng 11/2026. Cần theo dõi hằng tuần (mục 5).
    - **Định vị đề nghị:** đừng gọi là "benchmark Byzantine-FL trên dữ liệu thật" (phần này đã có người làm), mà là **"thước đo dữ liệu cho Byzantine-FL"**, tức cây cầu nối hai phía.

---

## 1. Bản đồ: đã có, có liên quan, chưa có

| Phần việc | Tình trạng | Ai đã làm (xem mục 2–3) |
|---|---|---|
| Đề xuất bộ gộp chống Byzantine mới | ✅ **Đã có rất nhiều** (bão hòa) | ICLR 2026, NeurIPS 2025, hàng chục bài khác |
| Benchmark ma trận tấn công × bộ gộp trên dữ liệu ảnh | ✅ **Đã có nhiều** | Blades, ByzFL, FedSecurity, FLPoison, edgefed-bench |
| Byzantine-FL trên dữ liệu thật, chia client tự nhiên | 🟡 **Mới xuất hiện (2024–2026)** | Malkani (y tế), `oran-fed-robust` (mạng di động), Zhang 2024 (lưu lượng di động Milan) |
| Benchmark Byzantine-FL cho giao thông đường bộ | 🟡 **Ít, chưa có trên dữ liệu thật** | HuddsTrafficFL (mô phỏng SUMO), AttestedFL (5 client, chia nhân tạo) |
| Đo tỉ lệ loại nhầm client trung thực | 🟡 **Rất ít** | edgefed-bench (chỉ Multi-Krum), Malkani |
| Đo dị biệt dữ liệu bằng con số | 🟡 **Có, nhưng không cho Byzantine** | Li và cs. (6 thước đo dị biệt), Fan 2025 (energy distance) |
| Đo đặc tính chuỗi thời gian bằng con số | 🟡 **Có, nhưng không cho FL** | TFB 2024 (trend, seasonality, shifting…) |
| Khung chất lượng dữ liệu giao thông theo mục đích | 🟡 **Có, nhưng không có FL hay tấn công** | Petkani và cs. 2026 |
| Nêu lỗi "chia IID nhân tạo", "benchmark quá dễ" | 🟡 **Đã nêu, chưa đo** | SoK 2026 (FL cho phát hiện xâm nhập trên xe), Wu & Keogh 2021 |
| **Thước đo dữ liệu trước huấn luyện, dự báo được hành vi bộ gộp** | ❌ **Chưa tìm thấy** | — |
| **So sánh có hệ thống các bộ dữ liệu giao thông và V2X cho Byzantine-FL** | ❌ **Chưa tìm thấy** | — |
| **Byzantine-FL trên LargeST** | ❌ **Chưa tìm thấy** | Xem thêm trang [Bài báo liên quan](nghien-cuu/bai-bao-lien-quan.md): 114 bài trích dẫn LargeST, 0 bài có Byzantine |

---

## 2. Các công trình gần nhất (cần đọc kỹ)

| Công trình | Năm, nơi | Họ làm phần nào | Đã làm được gì | Khác nhóm mình ở đâu |
|---|---|---|---|---|
| **Malkani**, [*Who Pays for Byzantine Robustness?*](https://arxiv.org/abs/2611.22904) | arXiv, 17/11/2026 | Ai chịu thiệt khi dùng bộ gộp chống Byzantine, với ít bệnh viện tham gia | 8 bộ gộp, dữ liệu y tế FLamby (4–6 client), 54.214 lần chạy. Bộ gộp không trọng số luôn bỏ qua client có cập nhật khác thường nhất, kể cả khi client đó trung thực | Đo **sau** khi huấn luyện; chấm **bộ gộp**, không chấm dữ liệu; lĩnh vực y tế |
| [`oran-fed-robust`](https://github.com/adeliusa486/oran-fed-robust) | GitHub, 2026 | Benchmark bộ gộp trên dữ liệu mạng di động **thật**, chia client **tự nhiên** theo trạm gốc | Dưới tấn công IPM, Krum và Median **tệ hơn cả FedAvg không phòng thủ**; Trimmed Mean và FLTrust ổn định | Nói dị biệt là thật nhưng **không đo**; không báo tỉ lệ loại nhầm |
| **Babar, Khan, Parkinson**, [HuddsTrafficFL](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7206471) ([repo](https://github.com/FarahBabar/HuddsTrafficFL)) | KBS 2026 | Testbed Byzantine-FL cho giao thông đô thị, phát hiện bất thường | 292 client theo nút giao; FedAvg về AUC 0,50 khi bị đầu độc; Median đạt AUC ≥ 0,9874 **ở mọi tổ hợp** | Dữ liệu mô phỏng SUMO; kết quả gần trần nên khó phân biệt bộ gộp; không chấm dữ liệu |
| **Li và cs.**, *Benchmarking Data Heterogeneity Evaluation Approaches for Personalized Federated Learning* | Workshop FL 2024, Springer 2025 | So sánh 6 cách đo dị biệt dữ liệu | Hướng dẫn chọn thước đo dị biệt | Gần nhất về phía **đo dữ liệu**, nhưng cho FL cá nhân hóa, không có Byzantine. Có thể dùng lại làm baseline |
| **Shahsavari và cs.**, [*SoK: FL for Intrusion Detection in Vehicular Networks*](https://arxiv.org/abs/2607.10914) | arXiv, 07/2026 | Rà soát hơn 60 bài FL cho xe | Chỉ ra lỗi phổ biến: chia IID nhân tạo, dựa vào benchmark tầm thường, đánh giá đối kháng yếu | **Nêu đúng vấn đề nhóm muốn đo**, nhưng không đưa ra cách đo. Nên trích làm động lực |

---

## 3. Các công trình liên quan khác

### 3.1. Byzantine-FL hoặc đầu độc trên giao thông, mạng và xe

| Công trình | Năm, nơi | Bài toán, dữ liệu | Đã làm được gì | Thiếu so với hướng của nhóm |
|---|---|---|---|---|
| Zhang, Fang, Huang, Liu. [*Poisoning Attacks on FL-based Wireless Traffic Prediction*](https://arxiv.org/abs/2404.14389) | 2024–2025 | Dự báo lưu lượng di động, Telecom Italia Milan (thật) | Tấn công "tiêm lưu lượng giả" làm **mọi** bộ gộp (Median, Krum, FLTrust…) thất bại; đề xuất GLID | Không đo dị biệt hay loại nhầm |
| Ma, Yang, Jiao. [*Cellular Traffic Prediction via Byzantine-robust Async FL*](https://arxiv.org/abs/2505.19263) | IEEE TNSE 2025 | Milano, Trento, LTE (thật) | Khung bất đồng bộ + quyền riêng tư vi phân | Dị biệt chỉ nói định tính |
| Badu-Marfo, Al Mallah, Farooq. [*AttestedFL*](https://arxiv.org/abs/2403.09531) | IEEE VTC 2024 | Tốc độ đường Toronto (thật), 5 RSU chia nhân tạo | 3 cách phòng thủ dựa trên hành vi; kết quả định tính | Quá ít client, không có số liệu |
| Demir và cs. [*Targeted Attacks and Defenses for Distributed FL in Vehicular Networks*](https://arxiv.org/abs/2510.15109) | arXiv 2025 | Phát hiện BSM độc hại, VeReMi Extension | Tấn công có mục tiêu và backdoor rất hiệu quả | Không có bộ gộp chống Byzantine chuẩn |
| *Clean-label Poisoning Attack and Defense Game for FL in Vehicular Networks* | arXiv 2610.32765, cuối 2026 | FL cho xe | Mô hình trò chơi tấn công – phòng thủ | **Bài mới, cần đọc**; chưa rõ dữ liệu |
| *A Privacy-Preserving and Byzantine-Resilient FL Scheme in VANETs* | Springer, 07/2026 | VANET | Nhận diện xe Byzantine qua độ lệch gradient | Chưa rõ dữ liệu và tỉ lệ độc hại |
| Khan và cs. *MoFed-Guard* | Frontiers in AI 2026 | Misbehavior VANET, VeReMi Extension | FL tại RSU; có thử sign-flip với Krum, Trimmed Mean | Tác giả nói **không** khẳng định chống Byzantine |
| Wu và cs. [*Byzantine-Robust Multimodal FL for Intelligent Connected Vehicle*](https://doi.org/10.3390/electronics13183635) | Electronics 2024 | Nhận dạng đối tượng (KITTI, nuScenes), 100 xe chia nhân tạo | Trimmed Mean kèm nén top-k | Dị biệt chỉ nêu tên |
| FedTP; [*FL with Graph-Based Aggregation for Traffic Forecasting*](https://arxiv.org/abs/2507.09805) | 2025 | Dự báo giao thông METR-LA, PEMS-BAY | FL dự báo giao thông | **Không có tấn công** |

### 3.2. Đo dữ liệu và chất lượng dữ liệu

| Công trình | Năm, nơi | Đo gì | Thiếu gì |
|---|---|---|---|
| Fan và cs. [*Measuring Heterogeneity in ML with Distributed Energy Distance*](https://arxiv.org/abs/2501.16174) | arXiv 2025 | Độ khác nhau giữa phân phối đặc trưng các nguồn dữ liệu | Nối với hội tụ, không nối với tấn công |
| Qiu và cs. [*TFB*](https://arxiv.org/abs/2403.20150) | PVLDB 2024 | 6 đặc tính chuỗi thời gian tính được: trend, seasonality, stationarity, shifting, transition, correlation. Có cả METR-LA, PEMS-BAY | Không có FL, không gắn mục đích |
| Petkani và cs. [*Data Quality in Traffic Management*](https://doi.org/10.3390/futuretransp6030124) | Future Transportation 2026 | Sáu chiều chất lượng dữ liệu giao thông, ngưỡng theo mục đích sử dụng | Mục đích là điều khiển đèn, không có FL hay tấn công |
| Miller và cs. [*Current and New Data Quality Dimensions*](https://www.mdpi.com/2306-5729/9/12/151) | Data 2024 | ISO/IEC 25012 cộng 4 chiều mới, trong đó có "usefulness" (phù hợp mục đích) | Chưa chấm bằng số |
| Mohammed và cs. [*Data Quality Assessment*](https://arxiv.org/abs/2403.00526) | arXiv 2024 | Năm khía cạnh: dữ liệu, nguồn, hệ thống, nhiệm vụ, con người | Bài định hướng |
| Jiang và cs. [*FNBench*](https://arxiv.org/abs/2505.06684) | arXiv 2025 | Benchmark FL bền vững trước nhãn nhiễu | Nhiễu là điều kiện thí nghiệm, không phải thứ được chấm |
| Panda, Patil. [*Evaluating FL under data heterogeneity*](https://link.springer.com/article/10.1007/s44163-026-02339-0) | Discover AI 2026 | Khi dị biệt tăng, accuracy trung bình gần như không đổi nhưng client tệ nhất giảm mạnh | Không có Byzantine; ủng hộ chỉ số theo client |

### 3.3. Lý thuyết nối dị biệt với hành vi bộ gộp

| Công trình | Nội dung |
|---|---|
| Karimireddy, He, Jaggi. *Bucketing* (ICLR 2022) | Krum, Median thất bại khi non-IID ngay cả khi không có tấn công (dị biệt nhân tạo) |
| Allouah và cs. [*Fixing by Mixing*](https://arxiv.org/abs/2302.01772) (2023) | "Một client Byzantine khó phân biệt với một client trung thực khác thường" |
| *Robust Federated Inference* (ICLR 2026) | Sai số bộ gộp phụ thuộc tỉ lệ độc hại và độ khác nhau giữa đầu ra các client |
| *Cross-Attack Robust Aggregation for FL* (2026) | Krum, Multi-Krum thất bại khi non-IID mạnh; Median chịu phạt độ chính xác |

### 3.4. Bộ dữ liệu và repo hạ tầng

| Tên | Dùng để |
|---|---|
| [VeReMi NextGen](https://veremi-dataset.github.io/veremi-nextgen) (IEEE VNC 2026) | Dữ liệu misbehavior V2X mới, 15 kiểu tấn công; tác giả nói khó hơn VeReMi Extension, nhưng chưa có thước đo chung để kiểm |
| SPADE (2025/2026), VehiGAN (ACM 2025) | Thêm dữ liệu V2X, dữ liệu tổng hợp |
| ByzFL, FLPoison, BRA-FL, Blades, FedSecurity | Thư viện tấn công và bộ gộp dùng lại được |
| [`edgefed-bench`](https://github.com/Rajchhapariya/edgefed-bench) | Có cách đo tỉ lệ loại nhầm của Multi-Krum (2,3 % ở 20 % độc hại, Fashion-MNIST) |
| [`byzantine-fl-bench`](https://github.com/adnanmalkani/byzantine-fl-bench) | Repo nhỏ, 3 bộ gộp trên CIFAR-10, đang phát triển (cùng tác giả với bài Malkani) |
| `Federated-Time-Series-Forecasting` (GitHub) | Hạ tầng FL chuỗi thời gian, có lệch theo thời gian |

---

## 4. Khoảng trống của nhóm

> Các nghiên cứu Byzantine-FL gần đây đã chuyển sang dữ liệu thật và chia client tự nhiên, và đã có tổng quan chỉ ra lỗi "chia nhân tạo" và "benchmark quá dễ". Nhưng **chưa có công cụ nào đo các tính chất đó trên dữ liệu trước khi huấn luyện**. Vì vậy không biết kết quả bài này có so được với bài kia không, và không giải thích được vì sao cùng một bộ gộp lại thắng ở bộ dữ liệu này nhưng thua ở bộ khác.

**Ví dụ mâu thuẫn cụ thể nên dùng làm động lực:** Median gần như hoàn hảo ở HuddsTrafficFL (AUC ≥ 0,9874), nhưng thất bại ở bài lưu lượng Milan (Zhang 2024) và dưới tấn công IPM ở `oran-fed-robust`. Một thước đo dữ liệu chung có thể giải thích vì sao, ví dụ do độ khó hay mức dị biệt khác nhau.

**Câu hỏi nghiên cứu rút ra:** các chỉ số tính trên dữ liệu trước khi huấn luyện có dự báo được tỉ lệ loại nhầm client trung thực và điểm gãy của bộ gộp chống Byzantine không? Trả lời "có" thì benchmark là công cụ hữu ích. Trả lời "không" thì cũng là phát hiện: chứng minh phải đo trực tiếp trên cập nhật mô hình.

**Điều kiện để benchmark được chấp nhận:** phải chứng minh được điểm của nó dự báo đúng hành vi bộ gộp. Nếu không, nó chỉ là một bảng thống kê mô tả.

---

## 5. Việc tiếp theo

- [ ] Đọc toàn văn bài Malkani (arXiv 2611.22904) và bài Li và cs. về đo dị biệt.
- [ ] Đọc bài *Clean-label Poisoning… Vehicular Networks* (arXiv 2610.32765).
- [ ] Theo dõi hằng tuần: arXiv và repo `byzantine-fl-bench`, `oran-fed-robust`.
- [ ] Rà soát có hệ thống trên Scopus, IEEE Xplore, ACM DL; ghi số bài qua từng bước lọc.
- [ ] Kiểm lại thông tin xuất bản của các bài mới đọc tóm tắt trước khi trích dẫn.

??? note "Cách tra cứu và độ tin cậy"
    - Tra ngày 23/11/2026 bằng tìm kiếm web, tìm kiếm repo GitHub, và ba câu hỏi trên Perplexity. Đã đọc trực tiếp trang tóm tắt hoặc README của các công trình ở mục 2 và phần lớn mục 3.
    - Một số công trình (đánh dấu "chưa rõ" hoặc không có link) mới thấy qua kết quả tìm kiếm, **chưa đọc trực tiếp**. Cần kiểm lại trước khi trích dẫn.
    - Perplexity từng trộn lẫn bài báo của Malkani với repo `byzantine-fl-bench`. Thông tin ở trang này đã được đối chiếu với README gốc.
    - Đây là tra nhanh, **chưa phải rà soát có hệ thống**.
