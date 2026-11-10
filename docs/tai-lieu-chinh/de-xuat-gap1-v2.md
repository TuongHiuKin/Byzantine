# Đề xuất nghiên cứu: Benchmark học liên kết chống Byzantine trên dữ liệu giao thông đường bộ thật

*GAP-1 · Bản sửa đổi sau góp ý của thầy (v2) · 10/11/2026*

[Tải bản Word](de-xuat-gap1-v2.docx){ .md-button } [Xem bản trước (05/11)](de-xuat-gap1.md)

**Người đề xuất:** Tưởng Hiếu Kiên (nhóm Byzantine Research Group)
**Giảng viên hướng dẫn:** ThS. Lâm Hữu Khánh Phương
**Căn cứ sửa:** 18 mục góp ý của thầy, tài liệu *Thiết kế kỹ thuật GAP-1* (06/11) và bản rà soát thiết kế (07/11). Đối chiếu từng mục góp ý ở **Phụ lục C**.
**Tình trạng:** chưa có kết quả thí nghiệm. Các số liệu ở mục 5.1–5.2 là số đo sơ bộ trên dữ liệu, có script đi kèm (Phụ lục B).

!!! question "Các điểm em xin ý kiến thầy"
    Một số lựa chọn thiết kế em đang tạm dùng phương án đề nghị và đánh dấu *(xin ý kiến thầy)* ngay tại mục tương ứng. Danh sách đầy đủ ở **Phụ lục A**. Những thông tin còn đang đo hoặc kiểm tra được ghi là *(đang chờ xác nhận)* và sẽ cập nhật sau tuần 1.

# 1. Đặt vấn đề

Học liên kết (Federated Learning, FL) cho phép nhiều đơn vị quản lý đường cùng huấn luyện một mô hình dự báo lưu lượng mà không phải gom dữ liệu về một chỗ. Trong đề tài này, **một client là một đơn vị quản lý một hành lang hoặc một khu vực cảm biến**. Client giữ dữ liệu lưu lượng của các cảm biến thuộc hành lang hoặc khu vực đó.

Máy chủ không kiểm soát được các client. Một client bị chiếm quyền, hoặc có cảm biến bị can thiệp, có thể gửi cập nhật sai lệch (client *Byzantine*). Hậu quả mà đề tài đo được trực tiếp là **sai số dự báo tăng**, tính trên toàn mạng, trên từng client và riêng trong giờ cao điểm (mục 5.7).

Các bộ gộp chống Byzantine (Krum, Median, Trimmed Mean…) dựa trên một giả định chung: cập nhật của các client trung thực nằm gần nhau. Dữ liệu cảm biến thật vi phạm giả định này theo những cách mà dữ liệu mô phỏng và dữ liệu ảnh chia Dirichlet không có: cảm biến hỏng hoặc mất tín hiệu, hành lang ít xe và nhiều xe chênh nhau hàng chục lần, phân phối trôi theo năm và có sự kiện bất thường như COVID-19. Khi giả định bị vi phạm, bộ gộp có thể **loại nhầm client trung thực** (mất độ chính xác dù không có tấn công) hoặc **bỏ lọt client độc hại**.

# 2. Tổng quan và khoảng trống

## 2.1. Các hướng liên quan

| Hướng | Công trình tiêu biểu | Còn thiếu so với đề tài |
|---|---|---|
| Benchmark FL giao thông có Byzantine | HuddsTrafficFL (KBS 2026) [1]: 292 client, dữ liệu mô phỏng SUMO, bài toán phát hiện bất thường | Dữ liệu mô phỏng; bài toán phân loại, không phải dự báo; chỉ có FedAvg, Krum, Median |
| Dữ liệu giao thông thật quy mô lớn | LargeST (NeurIPS 2023) [2]: PeMS California 2017–2021, các bộ SD, GBA, GLA, CA | Không có FL, không có tấn công |
| FL dự báo giao thông | CNFGNN [3], FedGRU [4], FedGTP [5], gộp dựa trên đồ thị [6], FedASTAM [7] | Không xét client Byzantine. Đã kiểm [7]: không xuất hiện từ khóa *byzantine, poison, malicious, attack, krum* |
| FL không–thời gian có trao đổi liên client | FedeRICo [18] (truyền thông điệp tại biên giữa các client kề nhau) | Mở ra bề mặt tấn công mới (kênh liên client); thuộc giai đoạn 2 (mục 9) |
| Bộ gộp và dữ liệu dị biệt | Bucketing (ICLR 2022) [19]: Krum, Median, RFA thất bại khi dữ liệu non-IID ngay cả khi không có kẻ tấn công | Chứng minh trên dữ liệu tổng hợp và ảnh, với dị biệt Dirichlet nhân tạo |
| Tấn công đầu độc FL dự báo lưu lượng | [8] | Lưu lượng **mạng di động**, không phải giao thông đường bộ |
| Bộ gộp chống Byzantine trong xe | Uddin và cs. [9], SoK [10] | Dữ liệu CAN bus và IDS, đa số chia IID nhân tạo |

## 2.2. Rà soát có hệ thống

- **Chuỗi truy vấn** (Scopus, IEEE Xplore, ACM DL): `(Byzantine OR poisoning OR "robust aggregation") AND (federated) AND (traffic OR "spatio-temporal" OR PeMS OR LargeST)`.
- **Tiêu chí giữ lại:** có FL; có client độc hại hoặc bộ gộp chống Byzantine; dữ liệu giao thông đường bộ (thật hoặc mô phỏng).
- **Kết quả theo từng bước lọc:** số bài theo từng bước (tìm được → sau lọc tiêu đề và tóm tắt → sau đọc toàn văn) sẽ được báo cáo khi hoàn tất rà soát ở tuần 2. Nguồn bổ sung: ma trận 19 bài được giao, 74 bài trích dẫn LargeST, Connected Papers.
- Tình trạng đọc: [7] FedASTAM đã kiểm từ khóa, chưa đọc toàn văn; [18] FedeRICo đang đọc *(đang chờ xác nhận)*.

## 2.3. Khoảng trống

Các bộ gộp chống Byzantine giả định cập nhật của client trung thực nằm gần nhau. Bucketing [19] đã chỉ ra rằng dị biệt dữ liệu có thể phá vỡ giả định này, nhưng mới với dị biệt nhân tạo. **Chưa có đo lường nào cho thấy dị biệt tự nhiên của dữ liệu giao thông thật** (khuyết thiếu, chênh lệch lưu lượng giữa hành lang, trôi phân phối) **vi phạm giả định đó đến mức nào, yếu tố nào gây ra phần lớn vi phạm, và ảnh hưởng ra sao tới tỉ lệ loại nhầm client trung thực và bỏ lọt client độc hại.**

Khoảng trống này trả lời được bằng thí nghiệm của đề tài, và không phụ thuộc vào nhận định "chưa có công trình nào kết hợp đủ ba yếu tố".

# 3. Câu hỏi nghiên cứu

Cả bốn câu hỏi dùng chung dữ liệu, cách chia client, mô hình và quy ước thống kê.

**RQ1. Điểm gãy trên dữ liệu thật.** Với client chia theo hành lang, mỗi bộ gộp chịu được đến tỉ lệ client độc hại bao nhiêu trước từng kiểu tấn công cập nhật mô hình?
- *Điểm gãy* là tỉ lệ độc hại nhỏ nhất r ∈ {10, 20, 30, 40 %} mà tại đó MAE trung bình theo seed **vượt 110 % MAE của FedAvg sạch** (cùng cách chia), hoặc quá trình huấn luyện phân kỳ (loss không hữu hạn, hoặc lớn hơn 10 lần loss vòng đầu). Không gãy ở 40 % thì ghi "> 40 %". Biên 10 % trùng với biên TOST ở mục 5.8.
- Nếu MAE của bộ gộp **khi không có tấn công** đã vượt 110 % FedAvg sạch, ghi điểm gãy là "0 %". Khi đó cái giá phòng thủ (RQ2) đã vượt biên, trước cả khi có tấn công.
- Krum và Multi-Krum chạy với hai cấu hình f: f đúng (oracle) và f ước lượng sai, cố định f = round(0,2 n).
- Quy tắc gán nhãn này được viết trước khi chạy và nằm trong kế hoạch phân tích (mục 5.8).

**RQ2. Cái giá của dị biệt tự nhiên.** Khi dị biệt giữa client là tự nhiên, không phải Dirichlet nhân tạo, các bộ gộp mất bao nhiêu độ chính xác ở 0 % độc hại? Cái giá đó dồn lên những client nào, và có giải thích được bằng đặc trưng chất lượng của client không? Bucketing có thu hẹp được khoảng cách trên dữ liệu giao thông thật không?
- Đây là câu hỏi đo lường ("bao nhiêu, ở đâu, khi nào"), không phải câu hỏi tồn tại. Bucketing [19] đã trả lời câu hỏi tồn tại.

**RQ3. Tấn công ở mức cảm biến.** Các tấn công thao túng dữ liệu cảm biến (nhân hệ số, kẹt giá trị, trôi dần, báo 0 xe, phát lại), khi đặt trên cùng một trục cường độ, có vượt qua bộ kiểm tra chất lượng dữ liệu chỉ dùng lưu lượng và vượt qua các bộ gộp không? Biến thể chỉ tấn công trong giờ cao điểm thì sao?

**RQ4. Yếu tố nào của dữ liệu thật làm đổi kết luận?** Giữ cố định mạng đường, mô hình và tấn công, rồi bật hoặc tắt từng yếu tố (khuyết thiếu, cách chia client, trôi phân phối) theo thiết kế ablation R0–R4 (mục 5.9). Mỗi khác biệt về điểm gãy và cái giá phòng thủ quy được về yếu tố nào?

# 4. Đóng góp dự kiến

Mỗi đóng góp là một phát hiện, gắn với một câu hỏi và một bảng kết quả dự kiến.

| # | Đóng góp | RQ | Kết quả dự kiến |
|---|---|---|---|
| C1 | Định lượng cái giá của dị biệt tự nhiên: mức mất MAE và tỉ lệ loại nhầm client trung thực của từng bộ gộp, phân rã theo từng yếu tố của dữ liệu thật | RQ2, RQ4 | Bảng MAE sạch theo bộ gộp × client; biểu đồ tỉ lệ loại nhầm theo đặc trưng chất lượng; bảng R0–R4 |
| C2 | Bản đồ điểm gãy bộ gộp × tấn công trên dữ liệu thật, gồm cả Krum với f ước lượng sai | RQ1 | Bảng điểm gãy, có cờ ô vi phạm lý thuyết |
| C3 | Bộ tấn công cảm biến đặt trên một trục cường độ chung, cùng tỉ lệ vượt bộ luật chất lượng và vượt bộ gộp | RQ3 | Bảng tỉ lệ vượt theo tấn công × cường độ × bộ gộp |

Code, cấu hình, seed và file phân vùng client được phát hành như một yêu cầu tái lập (mục 5.10), không tính là đóng góp khoa học. Nhóm không phân phối lại dữ liệu.

# 5. Phương pháp

## 5.1. Dữ liệu

**Nguồn:** LargeST San Diego (SD), 716 cảm biến vòng PeMS, chỉ có lưu lượng (không có occupancy hay tốc độ).

**Kịch bản chính** *(xin ý kiến thầy, Phụ lục A, mục 1)*:

| Hạng mục | Giá trị |
|---|---|
| Năm | 2019 |
| Bước thời gian | 15 phút (theo cấu hình benchmark LargeST); 35.040 bước |
| Chia theo thời gian 6:2:2 | Train 01/01–07/08 (21.024 bước) · Val 08/08–19/10 (7.008) · Test 20/10–31/12 (7.008) |
| Cửa sổ | 12 bước vào, dự báo các chặng 15, 30 và 60 phút |
| Kịch bản trôi | Mô hình huấn luyện trên tập train 2019, test trên năm 2020 |

Kịch bản này cũng là cấu hình R0 của ablation, nên kết quả RQ1–RQ2 nối thẳng sang RQ4.

**Những gì đo được trên metadata và dữ liệu (script ở Phụ lục B):**
- District và County là hằng số trên toàn bộ SD. Không chia theo quận được; trục chia có nghĩa là hành lang (`Fwy`, 26 giá trị) và tọa độ.
- File parquet đã điền NaN bằng 0: **0 ô NaN**, 2,25 % ô bằng 0 (năm 2019). Vì vậy tỉ lệ khuyết thiếu và masked MAE **bắt buộc phải tính từ file HDF5 gốc** (đang kiểm tra lại file gốc). Nếu không có HDF5, dùng mặt nạ thay thế: chuỗi số 0 kéo dài ≥ 3 giờ trong khung 06–22 được coi là khuyết thiếu, và ghi rõ đây là giới hạn.
- Cảm biến gần như chết (> 95 % số 0 trong 2019): đo được 2 cảm biến trên parquet 2019; một phân tích trước ghi 33, con số này sẽ được đối chiếu lại trên HDF5 *(đang chờ xác nhận)*. **Cách xử lý mặc định:** giữ trong dữ liệu huấn luyện của client (đúng với thực tế vận hành), loại khỏi phép tính chỉ số, và đưa vào đặc trưng chất lượng của client.
- Giá trị 999 là ngưỡng cắt của PeMS (37 ô trong năm 2019), được đánh dấu là bị cắt, không phải lưu lượng thật.
- Tỉ lệ số 0 tăng từ 2,25 % (2019) lên 6,19 % (2021). Đây là dấu hiệu cảm biến xuống cấp theo thời gian.
- Các số sơ bộ trong bản trước (3,27 % khuyết thiếu, 18.035 cạnh, lưu lượng tháng 4/2020 giảm 48,7 %) sẽ được chạy lại từ HDF5. Mức giảm do COVID được tính trên **giao các cảm biến còn hoạt động cả năm 2019 và 2020**, để mẫu số không đổi.

**Chuẩn hóa** *(xin ý kiến thầy, Phụ lục A, mục 5)*: mặc định chuẩn hóa z-score toàn cục, dùng trung bình và độ lệch chuẩn tổng hợp từ tập train của các client. Chạy thêm một kiểm tra độ nhạy với chuẩn hóa theo từng client (mục 5.11). Lý do: cách chuẩn hóa quyết định chênh lệch lưu lượng giữa hành lang (18 lần) có hiện ra trong cập nhật mô hình hay không, tức quyết định RQ2 có quan sát được hiện tượng hay không.

**Mở rộng:** LargeST GBA, hoặc CA chia theo Caltrans district, chỉ cho các cấu hình chính, sau tuần 12 (mục 9).

## 5.2. Chia client

**Phân bố hành lang đo được:** 26 hành lang, từ 1 đến 95 cảm biến mỗi hành lang (chênh 95 lần). Lưu lượng trung bình chênh 18 lần giữa hành lang thấp nhất (SR11-E, 23,1 xe/15 phút) và cao nhất (I15-N, 414,6).

**Ba cách chia dùng trong thí nghiệm** *(xin ý kiến thầy, Phụ lục A, mục 2)*:

| Cách chia | Thuật toán | Số client | Vai trò |
|---|---|---|---|
| **P-A** (chính) | Nhóm theo `Fwy` (tuyến × hướng). Gộp mọi nhóm dưới 10 cảm biến vào nhóm kề gần nhất theo tọa độ trung bình. Nếu còn dưới 20 client, gộp tiếp các cặp nhỏ nhất | n_A ≈ 20–24 (chốt sau khi chạy script phân vùng ở tuần 1) | Kịch bản chính của mọi RQ |
| **P-B** | KMeans trên (Lat, Lng), k = 8, 16, 32. Đo được: 89–90, 44–45 và 22–23 cảm biến mỗi client | 8 / 16 / 32 | Quét số client; đối chứng cân bằng kích thước |
| **IID** | Chia ngẫu nhiên cảm biến thành n_A nhóm | n_A | Đối chứng không dị biệt; R0, R1 của ablation |

Chia theo cụm hành vi (DTW) chuyển sang phần mở rộng, làm stress-test.

**Chỉ số non-IID:**
- Wasserstein-1 (EMD) giữa phân phối lưu lượng các client, năm 2019, khung 06–22 giờ. Đo trên 26 hành lang: **median 86,4 so với 22,6 khi chia IID, tức gấp 3,81 lần**. Sẽ đo lại trên P-A sau khi gộp và trên P-B.
- Độ phân tán cập nhật ở vòng đầu, khi chưa có tấn công: trung bình khoảng cách L2 từ cập nhật của mỗi client tới trung bình các cập nhật.
- **Cổng dị biệt:** nếu EMD median của P-A nhỏ hơn 2 lần IID, dữ liệu SD không đủ dị biệt; chuyển sang LargeST CA hoặc GBA.

**Trọng số của FedAvg:** chạy cả FedAvg có trọng số theo số mẫu và không trọng số, vì Median và Krum không có trọng số. So sánh bộ gộp với FedAvg không trọng số tách được tác dụng của phòng thủ ra khỏi tác dụng của trọng số.

**Tái lập:** một lệnh sinh phân vùng từ metadata. Phát hành kèm file JSON ánh xạ client → danh sách sensor ID, có mã băm SHA-256, để phân vùng không đổi khi metadata LargeST đổi phiên bản.

## 5.3. Mô hình dự báo

- **Chính: GRU chung cho từng nút.** Đầu vào là 12 bước lưu lượng đã chuẩn hóa của một cảm biến, đầu ra là 4 bước tiếp theo (chặng 15, 30, 60 phút lấy từ đây). Siêu tham số (số lớp, kích thước ẩn, số vòng FL, số epoch cục bộ, learning rate) được chốt ở tuần 1 và ghi vào kế hoạch phân tích viết trước.
- **Giới hạn phải nêu:** mô hình từng nút bỏ qua phụ thuộc không gian. Kết luận ở kịch bản chính chỉ áp dụng cho lớp mô hình không dùng đồ thị.
- **Kiểm tra kiến trúc (bắt buộc): STGCN** trên tập con gồm 3 bộ gộp (FedAvg, Median, Krum với f = 20 % n) × 2 tấn công (ALIE, báo 0 xe) × 2 tỉ lệ (10 %, 30 %), cộng 3 bộ gộp khi sạch. Mỗi client dùng đồ thị con gồm các cảm biến của mình.
- **Tiêu chí:** báo cáo thứ hạng bộ gộp có giữ nguyên khi đổi từ GRU sang STGCN không (Kendall τ trên tập con, kèm bảng thứ hạng đầy đủ).

## 5.4. Nhãn và đặc trưng chất lượng client

- **Nhãn client độc hại:** nhóm tự tiêm tấn công nên biết chắc client nào độc hại. Nhãn này dùng để tính FPR và FNR.
- **Đặc trưng chất lượng mức client**, tính tự động trên tập train, **trước khi điền khuyết thiếu**:
  1. Tỉ lệ khuyết thiếu (từ HDF5).
  2. Số giờ đứng yên (giá trị không đổi ≥ 6 giờ liên tục).
  3. Mức trôi 2019 → 2020: EMD giữa phân phối lưu lượng năm 2019 và năm 2020 của chính client đó.
- Bỏ phần nhãn bất thường theo thời điểm: đối chiếu sự cố PeMS, gán nhãn sự kiện và kiểm tra thủ công.

## 5.5. Mô hình đe dọa

| Thành phần | Mặc định *(xin ý kiến thầy, Phụ lục A, mục 4)* |
|---|---|
| Tỉ lệ client độc hại | 0, 10, 20, 30, 40 %. f = round(tỉ lệ × n) |
| Chọn client độc hại | Ngẫu nhiên theo seed. Cùng một tập client độc hại cho mọi bộ gộp trong cùng seed (để ghép cặp). Ghi lại danh tính và kích thước các client bị chọn |
| Thời điểm và tính liên tục | Bắt đầu từ vòng 1, tấn công ở mọi vòng |
| Phối hợp | Tấn công cập nhật mô hình: các client độc hại gửi cùng một cập nhật. Tấn công cảm biến: dùng cùng tham số trên dữ liệu của mỗi client |
| Mức hiểu biết (i): chỉ biết dữ liệu và cập nhật của mình | Sign-flip, Gaussian, các tấn công cảm biến |
| Mức hiểu biết (ii): biết cả cập nhật của client trung thực | ALIE, IPM, Min-Max |

**Tấn công cập nhật mô hình trong ma trận lõi** *(xin ý kiến thầy, Phụ lục A, mục 6)*: Sign-flip, Gaussian, ALIE [13], IPM [17], Min-Max [16]. Scaling và Min-Sum bỏ khỏi ma trận lõi, vì Scaling bị Norm Clipping chặn một cách hiển nhiên và Min-Sum gần với Min-Max.

**Tấn công cảm biến (RQ3):** nhân hệ số k, kẹt giá trị, trôi dần, báo 0 xe, phát lại. Biến thể có mục tiêu: báo 0 xe và nhân k **chỉ trong 07–09 giờ và 16–19 giờ**.

**Trục cường độ chung:** với mỗi tấn công cảm biến, hiệu chỉnh tham số sao cho MAE cục bộ (mô hình FedAvg sạch, đánh giá trên dữ liệu đã bị tấn công của chính client độc hại) tăng **+25 %, +50 % và +100 %** so với khi sạch. Tham số được dò trên tập val và cố định trước khi chạy ma trận. Nếu một tấn công không đạt được mức nào đó (ví dụ phát lại không tới +100 %), ghi "không đạt" và dùng mức tối đa đạt được.

**Bộ kiểm tra chất lượng dữ liệu (chỉ dùng lưu lượng):**
- L1: giá trị đứng yên ≥ 6 giờ liên tục.
- L2: vượt phân vị 99,9 % của chính cảm biến đó (tính trên tập train).
- L3: lệch quá 3σ so với trung bình các cảm biến kề cùng tuyến (theo thứ tự `ID2`).
- L4: bằng 0 kéo dài ≥ 3 giờ trong khung 06–22 giờ.

Mỗi tấn công báo cáo tỉ lệ vượt qua từng luật và tỉ lệ vượt cả bốn luật.

**Ràng buộc lý thuyết và cờ ô:**
- Krum và Multi-Krum cần n ≥ 2f + 3. Ô vi phạm được gắn cờ "ngoài giới hạn lý thuyết" và tách khỏi bảng chính. Trên P-B, ô k = 8 với 40 % (f = 3) bị loại. Trên P-A, mọi ô đều hợp lệ nếu n_A ≥ 20.
- Trimmed Mean cắt ⌊βn⌋ client mỗi phía. Ô có **f > ⌊βn⌋** được gắn nhãn `gãy_theo_thiết_kế`, không trình bày như một phát hiện. Phải tính theo số client chứ không theo phần trăm: ví dụ với n = 8 và β = 0,1, ⌊0,8⌋ = 0, tức Trimmed Mean không cắt gì; ô này bị loại. Bảng nhãn đầy đủ được lập sau khi biết n_A.

## 5.6. Phòng thủ và baseline

| Nhóm | Cơ chế | Tham số mặc định | Ghi chú |
|---|---|---|---|
| Cận dưới | **Local-only** | — | Mỗi client tự huấn luyện, không chia sẻ |
| Cận trên | **Centralized** | — | Huấn luyện tập trung trên toàn bộ dữ liệu |
| Đối chứng | **FedAvg** có trọng số và không trọng số | — | Không phòng thủ |
| Phòng thủ bắt buộc | **Krum** [11] | f oracle; f = round(0,2 n) | Ở 0 % độc hại, dùng f = round(0,2 n), vì phía phòng thủ không biết là không có tấn công |
| | **Multi-Krum** [11] | chọn m = n − f cập nhật | |
| | **Median** theo tọa độ [12] | — | |
| | **Trimmed Mean** [12] | β = 0,1 / 0,2 / 0,3 | Cờ f > ⌊βn⌋ |
| | **Norm Clipping** | ngưỡng = trung vị chuẩn L2 của các cập nhật trong vòng | |
| Đối chứng dị biệt (bắt buộc) | **Bucketing** [19] + Krum; Bucketing + Median | kích thước nhóm s = 2 | Không phải phòng thủ Byzantine: dùng để trả lời RQ2, chứng minh cái giá đo được là do dị biệt chứ không do lỗi cài đặt |
| Nên có (nếu còn ngân sách) | Centered Clipping, RFA (trung vị hình học), Bulyan | Bulyan chỉ ở ô n ≥ 4f + 3 | Ví dụ với n = 8, Bulyan chỉ hợp lệ ở 10 % |

FLTrust chuyển sang phần mở rộng, vì cần máy chủ có tập dữ liệu sạch mà đề tài chưa có.

**Tập so sánh chính cho RQ2 gồm 9 cấu hình phòng thủ:** Krum, Multi-Krum, Median, Trimmed Mean (3 giá trị β), Norm Clipping, Bucketing + Krum, Bucketing + Median. Local-only, Centralized và FedAvg là mốc so sánh, không tính vào 9 cấu hình này.

**Cổng lợi ích FL (trước mọi thí nghiệm tấn công):** FedAvg có trọng số trên P-A phải tốt hơn Local-only, kiểm định Wilcoxon ghép cặp trên 10 seed, p < 0,05 sau hiệu chỉnh Holm. Cổng chỉ xét trên P-A; P-B và IID chỉ báo cáo mô tả. Nếu không đạt: dừng ma trận tấn công, đổi cách chia (ít client hơn, client lớn hơn) hoặc chuyển trọng tâm sang FL cá nhân hóa.

## 5.7. Chỉ số đánh giá

| Nhóm | Chỉ số | Định nghĩa | Chỉ số chính của |
|---|---|---|---|
| Độ chính xác | **Masked MAE** | Bỏ các ô khuyết thiếu gốc (từ HDF5) và các ô 999 | Mọi RQ |
| | RMSE | Có mặt nạ như trên | |
| | MAPE có ngưỡng | Chỉ tính các điểm có lưu lượng thật ≥ 20 xe/15 phút | |
| | Độ lớn trung bình của dự báo | Báo cáo kèm MAE, để phát hiện mô hình dự báo gần 0 | |
| Mức client | MAE từng client; MAE của client tệ nhất; MAE phân vị 90 % theo client | | **RQ2** |
| Giờ cao điểm | MAE trong khung 07–09 giờ và 16–19 giờ | | **RQ3** (biến thể có mục tiêu) |
| Phòng thủ | Điểm gãy | Mục 3, RQ1 | **RQ1** |
| | Tỉ lệ giữ độ chính xác | MAE FedAvg sạch / MAE có phòng thủ | RQ2 |
| | FPR (loại nhầm) | Krum, Multi-Krum: tỉ lệ client trung thực không được chọn, trung bình theo vòng. Median, Trimmed Mean: tỉ lệ tọa độ của client trung thực bị cắt hoặc không được chọn làm trung vị. Norm Clipping: tỉ lệ vòng mà cập nhật của client trung thực bị cắt chuẩn | **RQ2** |
| | FNR (bỏ lọt) | Định nghĩa tương tự, cho client độc hại | RQ1 |
| Tấn công cảm biến | Tỉ lệ vượt luật | Tỉ lệ cửa sổ bị tấn công không bị L1–L4 bắt | **RQ3** |
| Hệ thống | Thời gian một lần chạy | Giờ trên một cấu hình × seed | Ước lượng khối lượng |

**Quy tắc báo cáo:** không báo MAE mà thiếu độ lớn dự báo; không báo hiệu quả phòng thủ mà thiếu FPR; không so sánh bộ gộp mà thiếu FedAvg cùng điều kiện.

**Phân tích RQ2 theo client:** hồi quy FPR của từng client theo ba đặc trưng chất lượng (mục 5.4) và lưu lượng trung bình của client, dùng mô hình hỗn hợp với hiệu ứng ngẫu nhiên theo seed.

## 5.8. Thiết kế thống kê

**Kế hoạch phân tích viết trước:** chốt và ghi ngày ở cuối tuần 2, trước khi chạy cổng FL. Kế hoạch gồm danh sách so sánh chính, phép kiểm định, biên tương đương, số seed theo từng tầng và quy tắc xử lý các ô bị gắn cờ.

**Họ so sánh chính (m = 13), hiệu chỉnh Holm trên cả họ:**

| Nhóm | Số phép so sánh | Kiểm định |
|---|---|---|
| Cổng: FedAvg so với Local-only trên P-A | 1 | Wilcoxon signed-rank ghép cặp theo seed |
| RQ2: 9 cấu hình phòng thủ so với FedAvg, sạch, trên P-A | 9 | TOST, biên ±10 % MAE, mỗi phía là Wilcoxon một phía ghép cặp |
| RQ1: 3 ô tấn công trọng tâm (ALIE ở 20 %, với Median, Trimmed Mean β = 0,2 và Krum f = 20 % n), so với FedAvg cùng tấn công. Nếu n_A làm ô Trimmed Mean có f > ⌊0,2 n_A⌋ (ví dụ n_A = 24: f = 5, cắt 4), dùng β = 0,3 | 3 | Wilcoxon ghép cặp |

**Số seed:** 10 seed cho mọi ô thuộc họ so sánh chính. Với 10 cặp, p hai phía nhỏ nhất là 2/2¹⁰ ≈ 0,00195, nhỏ hơn ngưỡng Holm chặt nhất 0,05/13 ≈ 0,00385, nên mọi so sánh chính về nguyên tắc có thể đạt ý nghĩa. Các ô còn lại chạy 3–5 seed và chỉ báo cáo mô tả (trung bình ± độ lệch chuẩn, khoảng tin cậy bootstrap).

**Kết luận của RQ2:** mỗi cấu hình được xếp vào "tương đương", "kém hơn" hoặc "không kết luận được" theo TOST. Không dùng p > 0,05 để kết luận "không khác".

**Chỉ số mức client:** khoảng tin cậy bằng bootstrap theo cụm (seed × client), vì các client trong cùng seed không độc lập.

**Không dùng** Mann-Whitney cho các so sánh ghép cặp: với 3 so với 3 seed, p nhỏ nhất là 2/C(6,3) = 0,10, không bao giờ đạt 0,05.

## 5.9. Ablation R0–R4 (RQ4)

| Cấu hình | Khuyết thiếu | Chia client | Train / test |
|---|---|---|---|
| R0 | Đã điền (nội suy tuyến tính) | IID | 2019 / 2019 |
| R1′ | Giữ nguyên, huấn luyện với masked loss | IID | 2019 / 2019 |
| R1 | Thật: giá trị 0 do fillna, đúng như pipeline LargeST | IID | 2019 / 2019 |
| R2 | Đã điền | P-A | 2019 / 2019 |
| R3 | Đã điền | IID | 2019 / 2020 |
| R4 | Thật | P-A | 2019 / 2020 |

- R0 → R1′ đo tác dụng của việc dữ liệu có khuyết thiếu. R1′ → R1 đo tác dụng của cách xử lý khuyết thiếu. R0 → R2 đo tác dụng của dị biệt hành lang. R0 → R3 đo tác dụng của trôi phân phối. R4 là cả ba yếu tố cùng lúc. *(Xin ý kiến thầy về việc giữ R1′, Phụ lục A, mục 7.)*
- **Giữ cố định:** mô hình GRU; 4 bộ gộp (FedAvg, Median, Trimmed Mean β = 0,2, Krum f = 20 % n); hai điều kiện: sạch và ALIE ở 20 %.
- **Số seed:** 5 seed cho điều kiện sạch, 3 seed cho điều kiện có tấn công; báo cáo mô tả.
- **Tiêu chí hoàn thành:** mỗi khác biệt giữa R0 và R4 quy được về một yếu tố cụ thể.

## 5.10. Cài đặt, kiểm thử và tái lập

- Code FL hiện có bằng NumPy, đã có các tấn công, bộ gộp và loader LargeST. Mỗi lần chạy tự ghi cấu hình, seed, mã commit.
- **Kiểm thử đơn vị** cho từng bộ gộp trên ví dụ 4 client có đáp án tính tay.
- **Đối chiếu với ByzFL** [20] trên 3–5 cấu hình; sai lệch phải nhỏ hơn 1e-6.
- **Đo thời gian** một lần chạy GRU và STGCN trên SD ở tuần 1.
- Phát hành code, script dữ liệu, file phân vùng client (JSON + SHA-256), kế hoạch phân tích viết trước.

## 5.11. Khối lượng thí nghiệm

Một "lần chạy" là một cấu hình × một seed, huấn luyện đầy đủ.

| Tầng | Nội dung | Seed | Số lần chạy |
|---|---|---|---|
| Cổng FL | Centralized (10) + Local-only, FedAvg có trọng số, FedAvg không trọng số × 3 cách chia (P-A, P-B k = 16, IID) | 10 | 100 |
| RQ2: cái giá phòng thủ | 9 cấu hình × P-A (10 seed) + 9 × P-B k = 8/16/32 (3 seed) + 9 × IID (3 seed) | 10 / 3 | 198 |
| Kiểm tra độ nhạy chuẩn hóa | FedAvg + 9 cấu hình, P-A, chuẩn hóa theo client | 3 | 30 |
| RQ1: ma trận lõi | 5 tấn công × 4 tỉ lệ × 7 bộ gộp (FedAvg, Krum oracle, Krum f = 20 %, Multi-Krum, Median, Trimmed Mean β = 0,2, Norm Clipping), P-A | 3 | 420 |
| RQ1: ô trọng tâm | Thêm 7 seed cho 4 cấu hình (3 ô trọng tâm + FedAvg) để đủ 10 seed | +7 | 28 |
| RQ3: tấn công cảm biến | 5 kiểu × 3 cường độ × 4 bộ gộp, ở 20 % độc hại | 3 | 180 |
| RQ3: có mục tiêu | 2 biến thể × 3 cường độ × 4 bộ gộp | 3 | 72 |
| RQ4: ablation | 6 cấu hình × 4 bộ gộp × (5 seed sạch + 3 seed có tấn công) | 5 / 3 | 192 |
| **Tổng GRU** | | | **1.220** |
| Kiểm tra STGCN | 3 bộ gộp × 2 tấn công × 2 tỉ lệ + 3 bộ gộp sạch | 3 | 45 |

Hiệu chỉnh cường độ tấn công cảm biến chỉ cần huấn luyện cục bộ trên một client, nên chi phí nhỏ và không tính vào bảng.

**Tính khả thi:** thời gian máy cần = 1.220 × t / p, với t là số giờ một lần chạy và p là số lần chạy song song được. t sẽ đo thật ở tuần 1; cấu hình máy và p *(xin ý kiến thầy, Phụ lục A, mục 8)*. Ví dụ với giả định: t = 0,35 giờ và p = 4 thì cần khoảng 107 giờ máy, tức 5–6 tuần máy chạy liên tục 20 giờ/tuần, nằm trong cửa sổ tuần 3–10. Ngược lại, chạy tuần tự (p = 1) cần 427 giờ, vượt ngân sách.

**Thứ tự cắt nếu đo xong tuần 1 thấy vượt ngân sách** (đã chốt từ trước):
1. Bỏ điều kiện có tấn công của RQ4 (−72).
2. RQ3 có mục tiêu giữ 1 biến thể là báo 0 xe (−36).
3. RQ2 bỏ P-B k = 8 và k = 32 (−54).
4. RQ1 bỏ Gaussian khỏi ma trận lõi (−84).

Cắt cả bốn bước còn 974 lần chạy. Không bao giờ cắt cổng FL, các ô thuộc họ so sánh chính và kiểm tra STGCN.

# 6. Tiến độ (12 tuần, có cổng)

| Tuần | Việc | Cổng định lượng | Nếu không đạt |
|---|---|---|---|
| 1 | Đọc lại HDF5; sinh phân vùng P-A và đo n_A, EMD; đo thời gian một lần chạy GRU và STGCN; bắt đầu rà soát có hệ thống | EMD median của P-A ≥ 2 lần IID; t và p đã đo | EMD thấp: chuyển sang CA hoặc GBA. Vượt giờ: áp thứ tự cắt ở mục 5.11 |
| 2 | Kiểm thử đơn vị, đối chiếu ByzFL; hoàn tất rà soát; hiệu chỉnh cường độ tấn công cảm biến; **chốt kế hoạch phân tích, ghi ngày** | Sai lệch so với ByzFL < 1e-6; không có công trình trùng RQ2 và RQ3 | Sửa code trước tuần 3. Nếu trùng hướng: dời trọng tâm sang RQ3 |
| 3 | Cổng FL: Local-only, Centralized, FedAvg (10 seed) | FedAvg tốt hơn Local-only trên P-A, p < 0,05 sau Holm | Dừng; đổi cách chia hoặc chuyển sang FL cá nhân hóa |
| 4–5 | RQ2: 9 cấu hình khi sạch; kiểm tra độ nhạy chuẩn hóa | FPR đo được cho mọi bộ gộp có chọn lọc | Thiếu log chọn client: bổ sung log, chạy lại P-A |
| 6–8 | RQ1: ma trận lõi và ô trọng tâm | Điểm gãy xác định được cho ≥ 80 % ô hợp lệ | Thêm seed cho các ô sát ngưỡng 110 % |
| 9 | RQ3: tấn công cảm biến và biến thể giờ cao điểm | Mọi tấn công nằm trên cùng trục cường độ | Ghi "không đạt mức" theo quy tắc ở mục 5.5 |
| 10 | RQ4: ablation R0–R4; kiểm tra STGCN | Mỗi khác biệt quy được về một yếu tố | Báo cáo các yếu tố không tách được như một giới hạn |
| 11–12 | Phân tích theo kế hoạch viết trước; đóng gói code | Mọi so sánh chính được kết luận theo đúng quy tắc đã viết trước | — |

# 7. Rủi ro

| Rủi ro | Xác suất | Dấu hiệu sớm | Xử lý | Giai đoạn chịu trách nhiệm |
|---|---|---|---|---|
| FL không tốt hơn Local-only | Trung bình | Cổng tuần 3 không đạt | Đổi cách chia (ít client hơn, client lớn hơn) hoặc chuyển sang FL cá nhân hóa | Tuần 3 |
| Thống kê không đủ lực | Trung bình | Độ lệch chuẩn giữa các seed lớn hơn hiệu ứng kỳ vọng | Tăng seed cho ô chính; bootstrap theo cụm | Tuần 4–8 |
| Lỗi cài đặt bộ gộp | Cao | Kiểm thử đơn vị thất bại; lệch so với ByzFL | Sửa trước khi chạy ma trận | Tuần 2 |
| Ô ma trận vi phạm điều kiện lý thuyết | Cao | Thấy ngay khi lập ma trận | Gắn cờ, tách khỏi bảng chính | Tuần 2 (lập ma trận) |
| Dữ liệu SD không đủ dị biệt để phòng thủ gãy | Thấp (EMD đã gấp 3,81 lần IID) | EMD median của P-A dưới 2 lần IID | Chuyển sang LargeST CA hoặc GBA | Tuần 1 |
| Không có HDF5 gốc, mất tín hiệu khuyết thiếu | Đã xảy ra ở parquet | Parquet có 0 NaN | Đọc lại HDF5; nếu không có, dùng mặt nạ thay thế và ghi giới hạn | Tuần 1 |
| Vượt thời gian chạy | Cao | t × 1.220 / p vượt ngân sách | Áp thứ tự cắt ở mục 5.11 | Tuần 1 |
| Có công trình trùng hướng | Trung bình | Rà soát có hệ thống tìm thấy bài mới | Dời trọng tâm sang RQ3 (tấn công cảm biến) | Tuần 1–2 |
| Giấy phép dữ liệu không cho phân phối lại | Thấp | — | Chỉ phát hành script tải và xử lý | Tuần 11–12 |

# 8. Quyết định phạm vi

| Câu hỏi | Quyết định |
|---|---|
| Quan hệ với ByzCity | Nhánh bổ sung, độc lập. ByzCity đo hậu quả vật lý trong mô phỏng có vòng điều khiển; GAP-1 đo hành vi bộ gộp trên dữ liệu thật. Hai nhánh dùng chung bộ tấn công, bộ gộp và quy ước thống kê (ghép cặp theo seed, TOST ±10 %) |
| LargeST SD có đủ không | Đủ cho giai đoạn đầu. Mở rộng sang GBA hoặc CA (chia theo district) sau tuần 12, chỉ cho các cấu hình chính |
| Vòng kín điều khiển đèn tín hiệu | Bỏ khỏi GAP-1, vì LargeST là dữ liệu cao tốc |
| Khung FL | Giữ code NumPy hiện có, kèm kiểm thử và đối chiếu ByzFL |
| FL bất đồng bộ | **Bỏ khỏi GAP-1**, ghi vào hướng mở rộng (mục 9) *(xin ý kiến thầy, Phụ lục A, mục 3)* |
| HuddsTrafficFL | Không còn là điều kiện của thiết kế; chỉ dùng trong phần đặt vấn đề và tổng quan |

# 9. Hướng mở rộng (sau GAP-1)

- **FL bất đồng bộ:** câu hỏi đặt ra là thứ hạng bộ gộp có đổi khi có độ trễ không. FedBuff [21] cho thấy kích thước bộ đệm K tác động trực tiếp lên độ trễ hiệu dụng, nên K là biến điều khiển tự nhiên của thí nghiệm. Chỉ chạy trên 2 bộ gộp tốt nhất từ RQ1.
- **Kênh liên client** (CNFGNN [3], FedGTP [5], FedeRICo [18]): tấn công qua embedding hoặc thông điệp tại biên, và phòng thủ dựa trên láng giềng hoặc tính nhất quán tại biên. Dùng kết quả RQ2 làm động lực thiết kế.
- **Mạng đường khác:** LargeST GBA, hoặc CA với client là Caltrans district.
- **Chia theo cụm hành vi (DTW)** làm stress-test; **FLTrust** khi có tập dữ liệu sạch phía máy chủ.

# Tài liệu tham khảo

[1] HuddsTrafficFL. *Knowledge-Based Systems*, 2026 (S0950705126017296).
[2] X. Liu et al. LargeST: A Benchmark Dataset for Large-Scale Traffic Forecasting. NeurIPS 2023 Datasets and Benchmarks. arXiv:2306.08259.
[3] C. Meng, S. Rambhatla, Y. Liu. Cross-Node Federated Graph Neural Network for Spatio-Temporal Data Modeling. KDD 2021. arXiv:2106.05223.
[4] Y. Liu et al. Privacy-preserving Traffic Flow Prediction: A Federated Learning Approach. arXiv:2003.08725.
[5] FedGTP: Exploiting Inter-Client Spatial Dependency in Federated Graph-based Traffic Prediction. KDD 2024.
[6] Federated Learning with Graph-Based Aggregation for Traffic Forecasting. arXiv:2507.09805.
[7] FedASTAM: Adaptive Spatio-Temporal Federated Learning for Traffic Flow Prediction. *Applied Sciences* 16(5):2402, 2026; arXiv:2405.13090.
[8] Poisoning Attacks on Federated Learning-based Wireless Traffic Prediction. arXiv:2404.14389.
[9] Uddin et al. Robust Federated Learning for Anomaly Detection in Connected Autonomous Vehicle Networks Under Adversarial Attacks. *Automation* 7(3):80, 2026.
[10] Shahsavari et al. SoK: Federated Learning for Intrusion Detection in Vehicular Networks. arXiv:2607.10914, 2026.
[11] P. Blanchard et al. Machine Learning with Adversaries: Byzantine Tolerant Gradient Descent. NeurIPS 2017.
[12] D. Yin et al. Byzantine-Robust Distributed Learning: Towards Optimal Statistical Rates. ICML 2018.
[13] G. Baruch et al. A Little Is Enough: Circumventing Defenses for Distributed Learning. NeurIPS 2019.
[14] X. Cao et al. FLTrust: Byzantine-robust Federated Learning via Trust Bootstrapping. NDSS 2021.
[15] B. McMahan et al. Communication-Efficient Learning of Deep Networks from Decentralized Data. AISTATS 2017.
[16] V. Shejwalkar, A. Houmansadr. Manipulating the Byzantine: Optimizing Model Poisoning Attacks and Defenses for Federated Learning. NDSS 2021.
[17] C. Xie, O. Koyejo, I. Gupta. Fall of Empires: Breaking Byzantine-tolerant SGD by Inner Product Manipulation. UAI 2019.
[18] Orozco et al. FedeRICo. arXiv:2609.20026.
[19] S. P. Karimireddy, L. He, M. Jaggi. Byzantine-Robust Learning on Heterogeneous Datasets via Bucketing. ICLR 2022.
[20] ByzFL: Research Framework for Robust Federated Learning. arXiv:2505.24802.
[21] J. Nguyen et al. Federated Learning with Buffered Asynchronous Aggregation (FedBuff). AISTATS 2022.

*Danh mục đang được kiểm tra lại năm, nơi công bố và tên tác giả trước khi trích dẫn chính thức.*

---

# Phụ lục A. Các điểm xin ý kiến thầy

Các lựa chọn dưới đây đang dùng phương án em đề nghị. Em mong thầy cho ý kiến trước khi chốt kế hoạch phân tích ở cuối tuần 2.

| # | Vấn đề | Phương án đang dùng | Lý do | Mục |
|---|---|---|---|---|
| 1 | Kịch bản dữ liệu chính | Năm 2019, chia 6:2:2 theo thời gian (theo gợi ý của thầy), thay cho train 2017–2019 / test 2021 trong bản thiết kế kỹ thuật; trôi phân phối kiểm tra riêng bằng test trên 2020 | Rẻ hơn khoảng 3 lần, hết mâu thuẫn về tập validation, trùng với cấu hình R0 | 5.1 |
| 2 | Cách chia client chính | P-A (theo hành lang, n_A ≈ 20–24) là kịch bản chính, chạy 10 seed và dùng cho cổng lợi ích FL; 8/16/32 client lấy từ P-B (KMeans) để quét số client | Hành lang là đơn vị quản lý có thật, giữ được dị biệt tự nhiên | 5.2, 5.6, 5.8 |
| 3 | FL bất đồng bộ | Bỏ khỏi GAP-1, đưa vào hướng mở rộng | Giữ khối lượng trong 12 tuần; câu hỏi chính không cần độ trễ | 8, 9 |
| 4 | Mô hình đe dọa mặc định | Tấn công từ vòng 1, liên tục, các client độc hại phối hợp | Trường hợp xấu nhất, dễ so sánh với tài liệu | 5.5 |
| 5 | Chuẩn hóa dữ liệu | z-score toàn cục; thêm kiểm tra độ nhạy với chuẩn hóa theo client | Cách chuẩn hóa quyết định dị biệt có hiện ra trong cập nhật hay không | 5.1, 5.11 |
| 6 | 5 tấn công trong ma trận lõi | Sign-flip, Gaussian, ALIE, IPM, Min-Max (bỏ Scaling, Min-Sum) | Scaling bị Norm Clipping chặn hiển nhiên; Min-Sum gần Min-Max | 5.5 |
| 7 | Bước R1′ trong ablation | Giữ R1′ (huấn luyện với masked loss) | Tách tác dụng của khuyết thiếu khỏi cách xử lý khuyết thiếu | 5.9 |
| 8 | Tài nguyên tính toán | Ước tính 1.220 lần chạy GRU; cần chạy song song khoảng 4 tiến trình | Chạy tuần tự vượt ngân sách thời gian | 5.11 |

Các lựa chọn nhỏ hơn đã nêu trong bài và em giữ nguyên trừ khi thầy góp ý: Bucketing đi với Krum và Median, kích thước nhóm s = 2 (mục 5.6); cảm biến chết giữ khi huấn luyện, loại khi tính chỉ số (mục 5.1).

**Thông tin đang chờ xác nhận** (em sẽ cập nhật sau tuần 1): thời gian một lần chạy đo thật; số client n_A của P-A; tỉ lệ khuyết thiếu và số cảm biến chết đo lại trên HDF5 gốc; siêu tham số GRU; kết quả rà soát có hệ thống và kết luận sau khi đọc FedASTAM, FedeRICo.

# Phụ lục B. Truy vết số liệu

| Số liệu | Nguồn |
|---|---|
| 716 cảm biến, 26 hành lang, 1–95 cảm biến mỗi hành lang | `01_data/interim/sd_sensors_716.csv` |
| EMD hành lang: median 86,4; IID 22,6; tỉ lệ 3,81 lần | `scratch/measure_non_iid.py` |
| Lưu lượng trung bình theo hành lang, từ 23,1 đến 414,6 | `scratch/measure_non_iid.py` |
| KMeans k = 8/16/32, tỉ lệ kích thước lớn nhất/nhỏ nhất 1,0 | `scratch/design_partition.py` |
| Parquet 2019 có 0 NaN, 2,25 % số 0; 2 cảm biến > 95 % số 0 | `scratch/check_nan.py` |
| Giá trị 999: 16 / 37 / 12 ô trong 2017 / 2019 / 2021 | `scratch/check_nan.py` |
| Điều kiện hợp lệ của Krum và Bulyan theo n và tỉ lệ độc hại | `scratch/feasibility_v3.py` |
| Số seed tối thiểu theo m; p nhỏ nhất của Wilcoxon và Mann-Whitney | Tính tay, mục 5.8 |

# Phụ lục C. Đối chiếu với 18 mục góp ý

| # | Mục góp ý (điểm, khuyến nghị) | Đã sửa ở |
|---|---|---|
| 1 | Đặt vấn đề (7, NÂNG CẤP) | Mục 1: bỏ câu về hệ thống điều khiển; thống nhất định nghĩa client; hậu quả gắn với chỉ số ở 5.7 |
| 2 | Tổng quan và khoảng trống (5, THAY ĐỔI) | Mục 2.2–2.3: khoảng trống viết thành câu hỏi; chuỗi truy vấn; FedASTAM, FedeRICo, Bucketing |
| 3 | RQ1 (7, NÂNG CẤP) | Mục 3: điểm gãy 110 %, quy tắc gán nhãn, Krum với f ước lượng sai |
| 4 | RQ2 (8, CHẤP NHẬN + chỉ số) | Mục 3, 5.7, 5.8: phát biểu lại; chỉ số mức client; TOST; hồi quy FPR theo đặc trưng chất lượng |
| 5 | RQ3 (7, NÂNG CẤP) | Mục 5.5: bộ luật L1–L4; trục cường độ +25/50/100 %; biến thể giờ cao điểm |
| 6 | RQ4 (3, THAY ĐỔI) | Mục 3, 5.9: thay bằng ablation R0–R4, thêm R1′ |
| 7 | Đóng góp (6, THAY ĐỔI) | Mục 4: 3 đóng góp dạng phát hiện, mỗi cái gắn một RQ; giao thức tái lập chuyển xuống 5.10 |
| 8 | Dữ liệu (7, NÂNG CẤP) | Mục 5.1: năm, bước 15 phút, kích thước từng tập; script ở Phụ lục B |
| 9 | Chia client (6, NÂNG CẤP) | Mục 5.2: thuật toán, phân bố kích thước, EMD, FedAvg có và không trọng số, JSON + mã băm |
| 10 | Mô hình (6, NÂNG CẤP) | Mục 5.3: giới hạn mô hình từng nút; STGCN bắt buộc trên tập con |
| 11 | Gán nhãn (4, LOẠI BỎ một phần) | Mục 5.4: bỏ nhãn thủ công; 3 đặc trưng chất lượng mức client |
| 12 | Mô hình đe dọa (7, NÂNG CẤP) | Mục 5.5: thời điểm, tính liên tục, phối hợp, mức hiểu biết; cờ n ≥ 2f + 3 và f > ⌊βn⌋ |
| 13 | Baseline (5, NÂNG CẤP) | Mục 5.6: Local-only, Centralized, Bucketing, Norm Clipping bắt buộc; CC, RFA nên có; cổng lợi ích FL |
| 14 | Chỉ số (7, NÂNG CẤP) | Mục 5.7: masked MAE, MAPE có ngưỡng, client tệ nhất và p90, MAE giờ cao điểm |
| 15 | Thống kê (2, THAY ĐỔI) | Mục 5.8: 10 seed cho ô chính; m = 13 với Holm; TOST ±10 %; bootstrap theo cụm; kế hoạch viết trước |
| 16 | Hiện trạng (6, NÂNG CẤP) | Mục 5.10: kiểm thử đơn vị, đối chiếu ByzFL, đo thời gian |
| 17 | Tiến độ (6, THAY ĐỔI) | Mục 6: baseline ở tuần 3; mỗi cổng có tiêu chí định lượng và phương án khi không đạt; đo thời gian trước khi chốt ma trận |
| 18 | Rủi ro (6, NÂNG CẤP) | Mục 7: 4 rủi ro thầy yêu cầu và các rủi ro mới; ByzCity chuyển sang mục 8 |
