# Đề xuất nghiên cứu: Benchmark học liên kết chống Byzantine trên dữ liệu giao thông đường bộ thật

*Bản trình thầy góp ý — GAP-1 · 05/11/2026*

[Tải bản Word](de-xuat-gap1.docx)

**Người đề xuất:** Tưởng Hiếu Kiên (nhóm Byzantine Research Group)
**Giảng viên hướng dẫn:** ThS. Lâm Hữu Khánh Phương
**Tình trạng:** bản nháp để xin ý kiến, chưa phải phạm vi đã chốt. Chưa có kết quả thực nghiệm nào trong tài liệu này.

# 1. Đặt vấn đề

Học liên kết (Federated Learning, FL) cho phép nhiều đơn vị quản lý đường, trạm bên đường (RSU) hoặc thành phố cùng huấn luyện một mô hình dự báo lưu lượng mà không cần gom dữ liệu về một chỗ. Đổi lại, máy chủ không kiểm soát được các client: một client bị chiếm quyền hoặc có cảm biến bị can thiệp có thể gửi cập nhật sai lệch (client *Byzantine*). Hậu quả là mô hình chung dự báo sai và các hệ thống điều khiển giao thông phía sau ra quyết định sai.

Các bộ gộp chống Byzantine (Krum, Median, Trimmed Mean…) đã được đề xuất nhiều. Tuy vậy, chúng chủ yếu được đánh giá trên dữ liệu ảnh hoặc dữ liệu xâm nhập mạng. Chính bài HuddsTrafficFL (Knowledge-Based Systems, 2026), benchmark gần nhất với đề tài, đã nêu hạn chế này:

> *"Existing benchmark datasets are mainly based on image classification or generic network intrusion tasks and often fail to capture geographically distributed clients, naturally occurring non-IID data, sensor-derived anomaly labels, and integrated Byzantine attack evaluation."*

HuddsTrafficFL lấp được phần lớn các thiếu sót đó, nhưng **dữ liệu của nó sinh bằng mô phỏng SUMO** trên bản đồ Huddersfield (382 nút giao). Vì vậy, tính non-IID "tự nhiên" và các nhãn bất thường của nó vẫn do mô hình hành vi xe của bộ mô phỏng tạo ra. Dữ liệu đo ngoài đường thật có những đặc điểm mà mô phỏng thường không có: cảm biến hỏng, mất dữ liệu, trôi phân phối theo năm, và các sự kiện bất thường như đại dịch COVID-19. Đây đúng là những yếu tố có thể khiến bộ gộp chống Byzantine **loại nhầm client trung thực** hoặc **bỏ lọt client độc hại**.

# 2. Tổng quan và khoảng trống

| Hướng | Công trình tiêu biểu | Còn thiếu |
|---|---|---|
| Benchmark FL giao thông có Byzantine | HuddsTrafficFL (KBS 2026) [1] | Dữ liệu mô phỏng SUMO |
| Dữ liệu giao thông thật quy mô lớn | LargeST (NeurIPS 2023) [2]: cảm biến PeMS California 2017–2021; các bộ SD (716 cảm biến), GBA (2.352), GLA (3.834), CA (8.600) | Không có FL, không có tấn công |
| FL cho dự báo giao thông | CNFGNN (KDD 2021) [3], FedGRU [4], FedGTP (KDD 2024) [5], FL với gộp dựa trên đồ thị [6] | Mặc định mọi client đều trung thực (cần đọc kỹ để xác nhận) |
| Tấn công đầu độc FL dự báo lưu lượng | Poisoning FL-based wireless traffic prediction [8] | Là lưu lượng **mạng di động**, không phải giao thông đường bộ |
| So sánh bộ gộp chống Byzantine trong xe | Uddin và cs. (MDPI Automation 2026) [9]: FedAvg, Median, Trimmed Mean, Krum, Multi-Krum, GeoMed với 10–40% client độc hại | Dữ liệu CAN bus trong xe |
| Tổng quan FL phát hiện xâm nhập cho xe | SoK (arXiv 2026) [10] | Chỉ ra rằng đa số bài không có client Byzantine, chia dữ liệu IID nhân tạo và chỉ dùng một bộ dữ liệu |

Nhóm đã rà soát 19 bài trong ma trận tài liệu được giao và 74 bài trích dẫn LargeST. Không bài nào kết hợp đủ ba yếu tố: **dữ liệu đường bộ thật, FL và tấn công/phòng thủ Byzantine**.

**Khoảng trống (GAP-1).** Hiện chưa có benchmark công khai nào đánh giá có hệ thống các bộ gộp FL chống Byzantine cho dự báo giao thông đường bộ trên **dữ liệu cảm biến đo thật**, với client phân bố theo địa lý, non-IID tự nhiên và giao thức tái lập được. Do đó cũng chưa biết các kết luận rút ra trên dữ liệu mô phỏng có còn đúng với dữ liệu thật hay không.

*Giới hạn của lượt rà soát:* nhóm mới tìm qua web, Connected Papers và bảng 93 bài, chưa tra có hệ thống trên Scopus và IEEE Xplore. Bài [7] (so sánh các cách gộp cho FL dự báo lưu lượng) mới tìm thấy và chưa đọc toàn văn. Nhóm sẽ đọc bài này trước tiên vì đây là bài có khả năng trùng hướng nhất.

# 3. Mục tiêu và câu hỏi nghiên cứu

**Mục tiêu:** xây dựng và công bố một benchmark FL chống Byzantine cho dự báo lưu lượng trên dữ liệu đường bộ thật, rồi dùng nó để đánh giá các bộ gộp phổ biến.

- **RQ1. Hiệu năng trên dữ liệu thật.** Trên dữ liệu thật, client chia theo địa lý, các bộ gộp (Krum, Multi-Krum, Median, Trimmed Mean) chống được những kiểu tấn công nào, và đến tỷ lệ client độc hại bao nhiêu?
- **RQ2. Cái giá của phòng thủ.** Khi không có tấn công, các bộ gộp làm giảm độ chính xác bao nhiêu? Chúng có loại nhầm các client trung thực nhưng khác biệt tự nhiên (hành lang ít xe, cảm biến hay mất dữ liệu) không?
- **RQ3. Tấn công sát thực tế.** Các tấn công ở mức dữ liệu cảm biến (nhân hệ số, kẹt giá trị, trôi dần, báo 0 xe) có vượt qua được kiểm tra chất lượng dữ liệu thông thường và các bộ gộp không? So với tấn công kinh điển ở mức cập nhật mô hình thì sao?
- **RQ4 (mở rộng). Mô phỏng và thật.** Dưới cùng một giao thức, thứ hạng các bộ gộp trên dữ liệu thật có giống thứ hạng trên dữ liệu mô phỏng HuddsTrafficFL không?

# 4. Đóng góp dự kiến

1. **Benchmark dữ liệu thật:** cách chia client theo hành lang đường trên LargeST, script chuẩn bị dữ liệu và chia tập theo thời gian. Nhóm phát hành code, không phân phối lại dữ liệu.
2. **Bộ tấn công sát thực tế cho cảm biến giao thông**, dùng chung giao diện với các tấn công kinh điển.
3. **Đánh giá có hệ thống** các bộ gộp, có đo cả cái giá của phòng thủ khi không bị tấn công.
4. **Giao thức tái lập:** mỗi kết quả kèm cấu hình, seed và mã commit, báo cáo trung bình ± độ lệch chuẩn và kiểm định thống kê.

# 5. Phương pháp

## 5.1. Dữ liệu

- **Chính:** LargeST San Diego (SD): 716 cảm biến vòng từ PeMS, 2017–2021, bước 5 phút. Nhóm đã phân tích sơ bộ bộ dữ liệu này: tỷ lệ khuyết thiếu 3,27%, đồ thị 716 nút và 18.035 cạnh, lưu lượng tháng 4/2020 giảm 48,7% so với nền 2017–2019.
- **Mở rộng (nếu kịp):** LargeST GBA hoặc GLA, để kiểm tra kết luận trên một mạng đường khác.
- **Đối chứng mô phỏng (RQ4):** bộ dữ liệu HuddsTrafficFL trên Zenodo (giấy phép CC BY-NC-ND 4.0).

## 5.2. Chia client

- Mỗi client là một **nhóm cảm biến cùng hành lang hoặc cùng khu vực**, mô phỏng một đơn vị quản lý đường giữ dữ liệu riêng. Thử với 8, 16 và 32 client.
- Đo và báo cáo mức non-IID thực tế giữa các client.
- Chia ngẫu nhiên (IID) chỉ dùng làm đối chứng.
- Tập train, val và test chia theo thời gian. Thêm một kịch bản trôi phân phối: train trên năm 2019, test trên năm 2020.

## 5.3. Mô hình dự báo

Mô hình chính là GRU hoặc MLP nhỏ, vì mục tiêu là đo tác động của tấn công chứ không phải đạt kết quả tốt nhất. Nếu kịp, nhóm thử thêm một mô hình đồ thị nhẹ (STGCN) để xem kết luận có phụ thuộc kiến trúc không. Dự báo ở các chặng 15, 30 và 60 phút, theo quy ước của LargeST.

## 5.4. Gán nhãn

Đề tài dùng hai loại nhãn và tách bạch chúng:

1. **Nhãn client độc hại:** do nhóm tự tiêm tấn công nên biết chắc client nào độc hại. Nhãn này dùng để đo khả năng phát hiện của các bộ gộp có bước chọn lọc.
2. **Nhãn bất thường từ cảm biến:** dữ liệu thật không có sẵn loại nhãn này, nên nhóm sẽ tự xây từ ba nguồn:
   (a) khuyết thiếu, giá trị đứng yên nhiều giờ, giá trị bão hòa;
   (b) cờ chất lượng và dữ liệu sự cố của PeMS, nếu đối chiếu được thời gian và vị trí;
   (c) các sự kiện lớn đã biết như giai đoạn COVID-19 và ngày lễ.
   Mỗi nhãn ghi rõ nguồn gốc. Một tập con sẽ được hai thành viên kiểm tra thủ công để ước lượng sai số nhãn.

## 5.5. Mô hình đe dọa

- **Tỷ lệ client độc hại:** 0, 10, 20, 30 và 40%, chọn ngẫu nhiên theo seed.
- **Mức hiểu biết của kẻ tấn công:** (i) chỉ biết dữ liệu và cập nhật của chính mình; (ii) biết cả cập nhật của các client trung thực.
- **Tấn công cập nhật mô hình:** Sign-flip, Scaling, nhiễu Gaussian, ALIE [13], IPM [17], Min-Max và Min-Sum [16].
- **Tấn công dữ liệu cảm biến (đóng góp mới):** nhân lưu lượng với hệ số k, kẹt giá trị (stuck-at), trôi dần, báo 0 xe khi đang ùn tắc, phát lại dữ liệu cũ (replay).

## 5.6. Phòng thủ và baseline

- **Bắt buộc:** FedAvg [15] (mốc không phòng thủ), Krum và Multi-Krum [11], Median và Trimmed Mean [12].
- **Nếu kịp:** Norm Clipping và FLTrust [14].
- **Cấu hình:** Krum nhận đúng số client độc hại f. Trimmed Mean thử với β = 0,1, 0,2 và 0,3, có nêu breakdown point của từng mức.

## 5.7. Chỉ số đánh giá

| Khía cạnh | Chỉ số |
|---|---|
| Độ chính xác | MAE, RMSE, MAPE ở các chặng 15, 30 và 60 phút |
| Tác động tấn công | Mức tăng MAE so với FedAvg khi không bị tấn công; số lượt huấn luyện phân kỳ |
| Cái giá phòng thủ | Mức tăng MAE khi không bị tấn công; tỷ lệ client trung thực bị loại nhầm |
| Phát hiện | TPR, FPR, F1 cho các bộ gộp có bước chọn lọc |
| Mô phỏng và thật (RQ4) | Hệ số tương quan thứ hạng Kendall τ giữa hai bảng xếp hạng bộ gộp |
| Thống kê | Tối thiểu 5 seed, báo cáo trung bình ± độ lệch chuẩn, kiểm định Wilcoxon có hiệu chỉnh cho nhiều phép so sánh |

## 5.8. Hiện trạng sẵn có

- Có code FL viết bằng NumPy với đầy đủ các tấn công và bộ gộp nêu trên, cùng loader cho LargeST. Mỗi lần chạy tự ghi lại cấu hình, mã commit, trung bình và độ lệch chuẩn.
- Có bản phân tích dữ liệu LargeST SD.
- Có bộ dữ liệu HuddsTrafficFL tải về từ Zenodo.
- Chưa có kết quả nào chạy trên dữ liệu thật.

# 6. Kế hoạch

Kế hoạch có hai phương án, tùy quyết định của thầy về việc nộp ICCIES 2027. Hội nghị nhận bài đến **15/11/2026**: bài tiếng Anh, 12–15 trang theo mẫu Springer LNCS, kỷ yếu Springer CCIS.

**Phương án A: nộp ICCIES 2027 (còn khoảng 10 ngày, phạm vi thu gọn)**

| Ngày | Việc |
|---|---|
| 06–08/11 | Chuẩn bị LargeST SD, chia client theo hành lang, chạy FedAvg khi không bị tấn công |
| 08–11/11 | Chạy ma trận lõi: 5 bộ gộp × 4–5 kiểu tấn công × tỷ lệ 10/20/30% × 5 seed |
| 11–14/11 | Nhóm tự viết bài; thầy đọc và góp ý |
| 15/11 | Nộp bài qua CMT |

Ở phương án này, RQ1 và RQ2 là phần chính, RQ3 chỉ làm một phần, còn RQ4 để dành cho bài sau.

**Phương án B: làm đầy đủ (khoảng 12 tuần), nhắm một hội nghị hoặc tạp chí sau**

| Giai đoạn | Thời lượng | Việc |
|---|---|---|
| 1 | 2 tuần | Rà soát tài liệu có hệ thống; chốt phạm vi |
| 2 | 2 tuần | Pipeline LargeST và HuddsTrafficFL theo cùng một giao thức |
| 3 | 2 tuần | Baseline khi không bị tấn công; xây nhãn bất thường |
| 4 | 3 tuần | Ma trận tấn công × phòng thủ |
| 5 | 1 tuần | Phân tích và kiểm định thống kê |
| 6 | 2 tuần | Viết bài, đóng gói code |

# 7. Rủi ro

| Rủi ro | Cách giảm |
|---|---|
| Đã có công trình trùng hướng mà nhóm chưa thấy | Đọc bài [7] trước tiên; tra có hệ thống trên Scopus và IEEE Xplore. Nếu trùng, chuyển trọng tâm sang RQ2 và RQ3 |
| Giấy phép dữ liệu không cho phân phối lại | Chỉ phát hành script tải và xử lý dữ liệu |
| Nhãn bất thường trên dữ liệu thật không chắc chắn | Tách nhãn client độc hại (chắc chắn) khỏi nhãn cảm biến (ước lượng); kiểm tra thủ công một phần |
| So sánh LargeST (đường cao tốc ở Mỹ) với HuddsTrafficFL (đô thị ở Anh) không cân xứng | Chỉ so thứ hạng các bộ gộp, không so MAE tuyệt đối |
| Khối lượng thí nghiệm lớn so với thời gian | Chạy thử nhỏ để đo thời gian trước, ưu tiên ma trận lõi |
| Lệch với đề cương ByzCity đã nộp (mô phỏng SUMO, vòng kín đèn tín hiệu) | Xin thầy quyết định ở mục 8 |
| ICCIES cấm văn bản do AI sinh ra | Nhóm tự viết toàn bộ nội dung bài nộp |

# 8. Kính xin thầy cho ý kiến

1. GAP-1 sẽ **thay thế** đề cương ByzCity (SUMO, vòng kín đèn Webster), là một **nhánh bổ sung**, hay là **một bài báo riêng**?
2. Có nộp ICCIES 2027 theo **phương án A** không? Nếu bài ByzCity cũng nhắm ICCIES thì nhóm nộp một bài hay hai bài?
3. Dùng LargeST SD là đủ chưa, hay cần thêm một mạng đường khác?
4. LargeST là dữ liệu đường cao tốc, không có đèn tín hiệu. Thầy có đồng ý bỏ phần vòng kín điều khiển đèn khỏi GAP-1 không?
5. Danh sách tấn công và phòng thủ ở mục 5.5–5.6 đã phù hợp chưa?
6. Nhóm dùng khung FL nào: Flower, FLGo hay code tự viết hiện có?
7. Có đưa FL bất đồng bộ vào không? Phần này chồng lên hướng nghiên cứu AFL của thầy.

# Tài liệu tham khảo

[1] HuddsTrafficFL. *Knowledge-Based Systems*, 2026 (bản PDF mã S0950705126017296; bổ sung tên tác giả và DOI từ bản gốc).
[2] X. Liu et al. LargeST: A Benchmark Dataset for Large-Scale Traffic Forecasting. NeurIPS 2023 Datasets and Benchmarks. arXiv:2306.08259.
[3] C. Meng, S. Rambhatla, Y. Liu. Cross-Node Federated Graph Neural Network for Spatio-Temporal Data Modeling. KDD 2021. arXiv:2106.05223.
[4] Y. Liu et al. Privacy-preserving Traffic Flow Prediction: A Federated Learning Approach. arXiv:2003.08725.
[5] FedGTP: Exploiting Inter-Client Spatial Dependency in Federated Graph-based Traffic Prediction. KDD 2024.
[6] Federated Learning with Graph-Based Aggregation for Traffic Forecasting. arXiv:2507.09805.
[7] Adaptive Spatio-Temporal Federated Learning for Traffic Flow Prediction: Framework and Aggregation Approaches Evaluation (ResearchGate, chưa đọc toàn văn).
[8] Poisoning Attacks on Federated Learning-based Wireless Traffic Prediction. arXiv:2404.14389.
[9] Uddin et al. Robust Federated Learning for Anomaly Detection in Connected Autonomous Vehicle Networks Under Adversarial Attacks. *Automation* 7(3):80, 2026.
[10] Shahsavari et al. SoK: Federated Learning for Intrusion Detection in Vehicular Networks. arXiv:2607.10914, 2026.
[11] P. Blanchard et al. Machine Learning with Adversaries: Byzantine Tolerant Gradient Descent (Krum). NeurIPS 2017.
[12] D. Yin et al. Byzantine-Robust Distributed Learning: Towards Optimal Statistical Rates (Median, Trimmed Mean). ICML 2018.
[13] G. Baruch et al. A Little Is Enough: Circumventing Defenses for Distributed Learning (ALIE). NeurIPS 2019.
[14] X. Cao et al. FLTrust: Byzantine-robust Federated Learning via Trust Bootstrapping. NDSS 2021.
[15] B. McMahan et al. Communication-Efficient Learning of Deep Networks from Decentralized Data (FedAvg). AISTATS 2017.
[16] V. Shejwalkar, A. Houmansadr. Manipulating the Byzantine: Optimizing Model Poisoning Attacks and Defenses for Federated Learning (Min-Max, Min-Sum). NDSS 2021.
[17] C. Xie, O. Koyejo, I. Gupta. Fall of Empires: Breaking Byzantine-tolerant SGD by Inner Product Manipulation (IPM). UAI 2019.

*Ghi chú: các mục [5]–[8] mới được xác nhận qua tiêu đề và trang arXiv, chưa đọc toàn văn. Trước khi trích dẫn chính thức, nhóm cần kiểm tra lại năm, nơi công bố và tên tác giả của toàn bộ danh mục.*
