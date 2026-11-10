# Đề cương nghiên cứu v3 — LargeST-ByzBench

> **Bản đề cương sửa theo 18 hạng mục góp ý của giảng viên hướng dẫn. Ma trận 22.240 lần chạy, thiết kế thống kê chốt trước.**
>
> Tác giả: Nguyễn Quang Huy — SE194177 · GVHD: ThS. Lâm Hữu Khánh Phương · Đại học FPT · 10/11/2026

**Đề cương nghiên cứu (Research Proposal) — bản v3**

| | |
|---|---|
| **Sinh viên thực hiện** | Nguyễn Quang Huy — SE194177 |
| **Giảng viên hướng dẫn** | ThS. Lâm Hữu Khánh Phương |
| **Đơn vị** | Đại học FPT |
| **Chương trình** | Đồ án tốt nghiệp |
| **Ngày** | 06 tháng 11 năm 2026 |
| **Lĩnh vực** | Học máy phân tán · An toàn học máy · Giao thông thông minh |
| **Bản này sửa từ** | v2 (05/11/2026) theo góp ý 18 hạng mục của giảng viên hướng dẫn |



---

## Mục lục

1. Đặt vấn đề — bối cảnh, bài toán, câu hỏi nghiên cứu, mục tiêu, phạm vi
2. Tổng quan tài liệu và khoảng trống nghiên cứu — bốn nhóm tiếp cận, ma trận đối chiếu, khoảng trống đã kiểm chứng
3. Phương pháp nghiên cứu — dữ liệu, phân vùng client, mô hình, tấn công, phòng thủ, chỉ số, thống kê
4. Kết quả kỳ vọng và đóng góp
5. Kế hoạch triển khai và quản trị rủi ro
6. Tài liệu tham khảo
7. Phụ lục A–F — kết quả sơ bộ, giả định, kiểm chứng nguồn, phản chứng, ngân sách, đặc tả chi tiết

> **Ghi chú về độ dài.** Bản v3 dài khoảng 6.700 từ thân bài, vượt ngân sách 2.500–5.000 từ của một đề cương chuẩn. Nguyên nhân là xung đột thật giữa hai yêu cầu: rubric 18 hạng mục đòi 9 bộ gộp, 14 cấu hình tấn công, 10 seed, ablation R0–R4, TOST và Holm — không thể trình bày đủ trong 5.000 từ. Tôi ưu tiên đáp ứng rubric và **ghi rõ phần vượt ở đây** thay vì cắt bớt nội dung thầy yêu cầu. Nếu cần bản 5.000 từ để nộp, phần cắt được là các mục §3.6–3.7 và Phụ lục F, và tôi sẽ làm theo chỉ định.

---

## Tóm tắt

Dự báo lưu lượng giao thông đòi hỏi dữ liệu tập trung, nhưng dữ liệu cảm biến thuộc nhiều cơ quan quản lý và không thể chia sẻ thô — học liên kết (FL) giải quyết rào cản pháp lý đó nhưng mở ra bề mặt tấn công mới, nơi một client bị chiếm quyền làm hỏng mô hình chung. Trên chính tập dữ liệu của đề tài, một tấn công nhân ×3 làm sai số dự báo tăng gấp ba lần nhưng không thay đổi bất kỳ tín hiệu chất lượng dữ liệu nào (Δ = +0,0 trên thang 100), nên kiểm tra chất lượng thông thường không phát hiện được.

Khảo sát 93 công trình cho thấy trong 56 bài giao thông đường bộ chỉ 1 bài kết hợp Byzantine, và bài đó không phát hành phân vùng client. Bộ benchmark đầy đủ nhất (HuddsTrafficFL, 2026) tự nêu bốn tiêu chí mà một benchmark Byzantine-FL cho giao thông phải có, nhưng chính nó dùng mô phỏng SUMO — tức tự định nghĩa thước đo rồi tự trượt ở tiêu chí dữ liệu thật. Ngoài ra Karimireddy và cộng sự (ICLR 2022) đã chứng minh các bộ gộp Byzantine **gãy dưới dữ liệu dị biệt ngay cả khi không có kẻ tấn công**, nhưng mới đo trên dữ liệu tổng hợp và ảnh.

Đề tài xây dựng **LargeST-ByzBench** — benchmark Byzantine-FL trên 716 cảm biến PeMS San Diego thật, với ba phương án phân vùng client có dị biệt đo được (EMD gấp 3,81 lần phân vùng IID), chín bộ gộp chia ba vai, mười bốn cấu hình tấn công trên một trục cường độ chung, và kế hoạch phân tích thống kê chốt trước khi chạy. Kết quả kỳ vọng là artefact tái lập được cùng định lượng **cái giá của phòng thủ** — mức loại nhầm client trung thực do dị biệt tự nhiên, phân bố theo client, trên dữ liệu giao thông thật.

**Từ khóa:** học liên kết; tấn công Byzantine; dị biệt dữ liệu; dự báo giao thông; LargeST; benchmark tái lập

---

## 1. Đặt vấn đề

### 1.1 Bối cảnh

Dự báo lưu lượng là hạ tầng của điều khiển tín hiệu và quản lý ùn tắc, và các mô hình tốt nhất — DCRNN, Graph WaveNet, STGCN — đều huấn luyện tập trung. Rào cản không phải kỹ thuật mà là quyền sở hữu dữ liệu: cảm biến đường cao tốc thường do các cơ quan vùng khác nhau quản lý, và dữ liệu thô không thể gom về một chỗ. Học liên kết cho phép các cơ quan huấn luyện chung mà không trao đổi dữ liệu gốc.

### 1.2 Phát biểu bài toán

FL giải quyết rào cản pháp lý nhưng tạo lỗ hổng kỹ thuật: server chỉ thấy cập nhật tham số, không thấy dữ liệu, nên một client bị xâm nhập có thể gửi cập nhật tuỳ ý. Mức độ nghiêm trọng đã được đo trên chính tập dữ liệu của đề tài — tiêm lỗi vào cảm biến 1116061 (sạch nhất 2019, điểm chất lượng 92,7/100, MAE nền 19,87):

| Kiểu tấn công | Δ điểm chất lượng | MAE | Bội số phá hoại |
|---|---|---|---|
| Nhân ×3 | **+0,0** | 59,60 | **3,00×** |
| Nhiễu trắng đều | **+7,3** | 224,20 | **11,29×** |
| Đóng băng giá trị | −42,7 | 46,31 | 2,33× |
| Spike 5 % | −13,6 | 64,10 | 3,23× |

Hai quan sát quyết định. Tấn công ×3 phá sai số gấp ba nhưng **không đổi bất kỳ tín hiệu chất lượng nào** (Δ = +0,0) — kiểm tra chất lượng dữ liệu không phát hiện được. Nhiễu trắng đạt điểm chất lượng **100/100, cao hơn cả dữ liệu thật**, trong khi phá MAE gấp 11,29 lần.

Hậu quả đo được trong phạm vi đề tài: một cơ quan tham gia liên kết có thể làm sai số dự báo của toàn bộ mạng lên gấp ba lần, và các bên còn lại **không có cách nào biết**. Đề tài không đo hậu quả lên quyết định điều khiển tín hiệu — LargeST là dữ liệu cao tốc, không có vòng điều khiển.

### 1.3 Câu hỏi nghiên cứu và giả thuyết

| Mã | Câu hỏi / giả thuyết | Kiểm chứng bằng |
|---|---|---|
| **RQ1** | Trên dữ liệu thật với client chia theo địa lý, mỗi bộ gộp Bybantine gãy ở tỉ lệ client độc hại nào, cho từng kiểu tấn công? | Điểm gãy = tỉ lệ nhỏ nhất mà MAE vượt 110 % MAE của FedAvg sạch |
| **RQ2** | Khi tỉ lệ độc hại bằng 0 %, dị biệt tự nhiên làm mỗi bộ gộp mất bao nhiêu phần trăm độ chính xác, và mất **không đều** giữa các client như thế nào? | MAE mức client, client tệ nhất, phân vị 90, FPR ở 0 % độc hại |
| **RQ3** | Tấn công ở mức dữ liệu cảm biến có vượt qua bộ kiểm tra chất lượng và bộ gộp không, so với tấn công mức cập nhật mô hình trên cùng trục cường độ? | Tỉ lệ vượt 4 luật chất lượng; MAE theo 3 mức cường độ |
| **RQ4** | Yếu tố nào của dữ liệu thật — khuyết thiếu, phân vùng địa lý, hay trôi phân phối — làm thay đổi kết luận về bộ gộp? | Ablation R0–R4, mỗi cấu hình bật/tắt một yếu tố |
| **H1** | Krum gãy sớm hơn Median vì dị biệt hành lang làm phân tán tập con nó chọn | So điểm gãy ở tỉ lệ độc hại bằng 0 % |
| **H2** | Tồn tại tỉ lệ độc hại ngưỡng mà từ đó mọi bộ gộp đều gãy | Tìm tỉ lệ nhỏ nhất mà cả 6 bộ gộp vượt 110 % |
| **H3** | Suy giảm ở 0 % độc hại chủ yếu do **dương tính giả**, không phải do bỏ sót | So FPR với FNR ở tỉ lệ 0 % |
| **H4** | Bucketing thu hẹp được khoảng cách giữa bộ gộp và FedAvg sạch trên dữ liệu thật | So MAE có/không Bucketing, TOST biên ±10 % |

Mỗi giả thuyết đều **có thể sai**, và mỗi cái sai đều cho thông tin. H1 sai → dị biệt không phải nguyên nhân, phải tìm cơ chế khác. H3 sai → phòng thủ yếu vì bỏ sót tấn công, đổi hướng thiết kế. H4 sai → Bucketing không chuyển được sang dữ liệu giao thông, đóng góp C4 mất nhưng C2 vẫn còn.

### 1.4 Mục tiêu

**Tổng quát:** xây dựng và phát hành bộ benchmark tái lập được cho Byzantine-FL trên dữ liệu giao thông thật, kèm định lượng cái giá của phòng thủ dưới dị biệt tự nhiên.

**Cụ thể (SMART), theo thứ tự thực hiện:**

1. **Xây dựng** ba phương án phân vùng client kèm script sinh lại, chỉ số dị biệt đo được, và tệp ánh xạ client → cảm biến có hash.
2. **Đo** điểm gãy của 9 bộ gộp dưới 14 cấu hình tấn công, ở 4 tỉ lệ độc hại.
3. **Định lượng** cái giá của phòng thủ ở tỉ lệ 0 %, tách riêng FPR theo từng client và hồi quy FPR theo đặc trưng chất lượng.
4. **Xác định** yếu tố nào của dữ liệu thật gây ra suy giảm, bằng ablation R0–R4.
5. **Phát hành** mã nguồn, phân vùng, cấu hình, log và kế hoạch phân tích đã chốt trước.

### 1.5 Phạm vi và giới hạn

**Trong phạm vi:** LargeST San Diego (District 11), 716 cảm biến, 2017–2021, tái lấy mẫu 15 phút; tác vụ hồi quy 12 bước vào / 12 bước ra; 9 bộ gộp; 14 cấu hình tấn công; FL đồng bộ.

**Ngoài phạm vi, kèm lý do:**

- **Không đề xuất thuật toán phòng thủ mới** — đây là nghiên cứu benchmark; đóng góp là artefact và đo lường.
- **Không giải quyết backdoor và label-flip** — cần nhãn rời rạc, LargeST là hồi quy không có nhãn để lật.
- **Không đưa FL bất đồng bộ vào ma trận lõi** — thêm một trục làm khối lượng chạy tăng gấp ba (xem Phụ lục B). Để ở "Hướng mở rộng" như một thí nghiệm riêng.
- **Không đo chi phí trên mạng thật** — không có quyền truy cập hạ tầng Caltrans.
- **Không mở rộng sang LargeST CA (8.600 cảm biến)** — kế hoạch giai đoạn sau, sau tuần 12.

---

## 2. Tổng quan tài liệu và khoảng trống nghiên cứu

### 2.1 Nền tảng lý thuyết và cái giá của dị biệt

FedAvg dùng trung bình có trọng số, nên một cập nhật có magnitude lớn kéo lệch kết quả. Các cơ chế Byzantine thay trung bình bằng hàm bền vững: **Krum** (Blanchard và cộng sự, 2017) chọn cập nhật có tổng khoảng cách tới *n − f − 2* cập nhật gần nhất nhỏ nhất; **median và trimmed mean** (Yin và cộng sự, 2018) thay trung bình bằng trung vị hoặc cắt biên; **FLTrust** (Cao và cộng sự, 2021) dùng tập sạch nhỏ ở server làm mốc chuẩn hoá magnitude.

**Điểm chung quyết định:** cả bốn giả định cập nhật của client trung thực nằm **gần nhau**. Giả định đó không đúng khi dữ liệu giữa các client dị biệt.

Đây không phải suy đoán — Karimireddy, He và Jaggi (ICLR 2022) chứng minh kết quả ngược với trực giác thông thường:

> "Existing Byzantine-robust aggregators (Krum, coordinate-wise median, RFA) **fail under non-iid data even without adversaries** — heterogeneity alone breaks them."

Nghĩa là câu hỏi "dị biệt có làm phòng thủ mất tác dụng không" đã có câu trả lời lý thuyết: **có**. Nhưng câu trả lời đó được xây trên dữ liệu tổng hợp và benchmark ảnh, nơi dị biệt được tạo bằng phân phối Dirichlet nhân tạo với tham số do người thí nghiệm chọn. Trên dữ liệu giao thông thật, dị biệt **không do ai chọn** — nó đến từ hành lang ít xe, cảm biến hỏng, và trôi phân phối theo năm.

Khoảng trống vì thế không phải "dị biệt có phá phòng thủ không", mà **"nó phá bao nhiêu, trên client nào, và dưới dạng dị biệt nào"**.

Ba cơ chế cụ thể khiến dị biệt giao thông khác dị biệt Dirichlet nhân tạo. Thứ nhất, dị biệt ở đây **có cấu trúc địa lý**, không phải nhiễu ngẫu nhiên: hành lang ít xe và hành lang cao điểm tạo hai cụm tách biệt, nên median có thể loại cả một cụm thay vì loại một outlier. Thứ hai, dị biệt **tương quan với chất lượng dữ liệu**: client có tỉ lệ khuyết thiếu cao thường cũng là client ít xe, nên "khác biệt tự nhiên" và "dữ liệu kém" không tách rời — đây là lý do RQ2 phải hồi quy FPR theo đặc trưng chất lượng chứ không chỉ báo cáo FPR trung bình. Thứ ba, dị biệt **thay đổi theo thời gian** do trôi phân phối, nên cùng một bộ gộp có thể đứng vững ở 2019 và gãy ở 2020 — điều mà một phép đo cắt ngang không phát hiện được.

### 2.2 Bốn nhóm tiếp cận

**Nhóm A — Byzantine-FL cho lưu lượng viễn thông** (trưởng thành nhất). Ma, Yang và Jiao (2025) ghép bất đồng bộ với differential privacy; Zheng và cộng sự (2024) thử Multi-Krum, trimmed mean, median trên lưu lượng không dây. *Tiên tiến, nhưng đối tượng là lưu lượng gói/cell, không phải xe.*

**Nhóm B — FL cho giao thông đường bộ, không có an ninh** (đa số). FedGRU (Liu và cộng sự, 2020) đặt nền với PeMS thật 39.000 detector; CNFGNN (Meng và cộng sự, 2021) và FedGTP (2024) thêm phụ thuộc không gian giữa client. *FL chạy được trên dữ liệu thật, nhưng không mô hình hoá client độc hại.*

**Nhóm C — Giao thông đường bộ + Byzantine** (một công trình). Vehicular AttestedFL (Badu-Marfo và cộng sự, VTC 2024) dùng tốc độ thật của Toronto Downtown — 76 nút giao, 223 link, chu kỳ 5 phút — với ba tuyến phòng thủ behavior attestation. *Gần nhất, nhưng chỉ 5 RSU, một kiểu tấn công, không phát hành phân vùng.*

**Nhóm D — Benchmark.** HuddsTrafficFL (Babar, Khan và Parkinson, 2026) đầy đủ nhất: 292 client, 91.482 quan sát, nhãn bất thường từ cảm biến, baseline Krum và Coordinate Median. *Nhưng dùng **SUMO/TraCI mô phỏng**.*

### 2.3 Ma trận đối chiếu

| Tiêu chí | VTC 2024 | Hudds 2026 | FLPoison 2025 | byz-fl 2026 | FedBuff 2022 | **Đề tài** |
|---|---|---|---|---|---|---|
| Dữ liệu giao thông đường bộ thật | ✅ Toronto | ❌ SUMO | ❌ ảnh | ❌ y tế | ❌ tổng hợp | ✅ **PeMS SD** |
| Tấn công gradient Byzantine | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| Nhiều kiểu tấn công | ❌ 1 | ✅ | ✅ 15 | ✅ 7 | ❌ | ✅ **14** |
| Baseline + phân vùng phát hành | ❌ | ✅ 292 | ✅ | ✅ | ❌ | ✅ **9 / 3 phương án** |
| Đo cái giá phòng thủ ở 0 % độc hại | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ **RQ2** |
| Chỉ số mức client (p90, tệ nhất) | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Báo cáo cả MAE và attack-success | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ **bắt buộc** |
| Protocol chốt trước khi chạy | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ **kế thừa** |

Ba hàng bị lược (cơ chế FL, mã nguồn mở, cơ chế phòng thủ đơn lẻ) đều đạt ở mọi cột nên không phân biệt được. **Không hàng nào đủ cả 8 tiêu chí.** FedBuff được thêm vào vì nó là nguồn gốc lý thuyết của bộ đệm, và cột Byzantine của nó trống — xem Phụ lục D.

### 2.4 Khoảng trống — phát biểu đã kiểm chứng

Khoảng trống **không phải** "chưa ai làm Byzantine-FL cho giao thông trên dữ liệu thật" — Vehicular AttestedFL bác bỏ phát biểu đó. Cũng **không phải** "chưa có benchmark Byzantine" — FLPoison và byzantine-fl-bench đã có, chỉ khác miền.

HuddsTrafficFL có cấu trúc benchmark nhưng dùng SUMO; Vehicular AttestedFL có dữ liệu thật nhưng không phải benchmark. **Giao của hai tập này rỗng.**

Khoảng trống đúng là:

> **Chưa có đo lường nào cho thấy dị biệt tự nhiên của dữ liệu giao thông thật vi phạm giả định "cập nhật trung thực nằm gần nhau" đến mức nào, và hệ quả lên tỉ lệ loại nhầm và bỏ lọt là bao nhiêu.**

Ba bằng chứng định lượng: trong **56** bài giao thông đường bộ chỉ **1** bài kết hợp Byzantine; trong 93 bài, **0** bài báo cáo đồng thời MAE và attack-success; liên hệ "thuộc nhánh FL" × "quan tâm Byzantine" đạt **φ = 0,688** (χ²(1) = 38,71, p < 0,001) — 10/17 bài FL so với 1/76 bài ngoài FL. Byzantine là mối quan tâm **nội bộ cộng đồng FL**, chưa thấm vào cộng đồng ứng dụng.

**Bằng chứng mạnh nhất đến từ chính HuddsTrafficFL.** Bài báo tự nêu bốn tiêu chí mà một benchmark Byzantine-FL cho giao thông phải có, khi phê bình các benchmark trước:

> "Existing benchmark datasets are mainly based on image classification or generic network intrusion tasks and often fail to capture **geographically distributed clients, naturally occurring non-IID data, sensor-derived anomaly labels, and integrated Byzantine attack evaluation** within a unified framework."

HuddsTrafficFL đáp ứng cả bốn — nhưng trên mô phỏng SUMO/TraCI (nguyên văn abstract: *"developed from a city-scale traffic sensing environment using SUMO/TraCI simulations and OpenStreetMap road networks"*). Nó **tự định nghĩa thước đo rồi tự trượt ở tiêu chí "dữ liệu thật"** — tiêu chí chính nó không đưa vào danh sách vì đã mặc định là có.

Đây là dạng khoảng trống mạnh nhất để bảo vệ: không phải tôi suy ra tiêu chí từ ngoài, mà **đối thủ gần nhất tự đặt ra tiêu chí, và đề tài đáp ứng đúng tiêu chí còn thiếu**.

### 2.5 Nhánh bất đồng bộ và bộ đệm — vì sao nó không nằm trong ma trận lõi

Một nhánh riêng của FL đáng nêu vì nó chạm trực tiếp vào cơ chế gây suy giảm. FedBuff (Nguyen và cộng sự, 2022) chứng minh rằng với bộ đệm kích thước *K*, cận trên staleness giảm theo *K*: τ_max,K ≤ ⌈τ_max,1/K⌉. Nghĩa là bất đồng bộ không phải một trục độc lập cần thêm vào ma trận — nó là **biến điều khiển mà giao thức tổng hợp đã tác động lên**.

Nhưng quan hệ đó **không đơn điệu**. Trên ba benchmark của FedBuff, K = 10 tốt nhất và K = 100 tệ hơn cả K = 1 (CelebA: 32,4 → 31,9 → 71,6 nghìn client trips). Với đề tài này, hệ quả là câu hỏi đúng về bộ đệm **không phải** "K tối thiểu là bao nhiêu" mà "K tối ưu dịch đi đâu khi có tấn công Byzantine" — vì K lớn vừa giảm staleness (tốt cho phòng thủ) vừa gộp nhiều cập nhật độc hại hơn vào một lần tổng hợp (xấu).

Đây là một câu hỏi hấp dẫn nhưng **không phải câu hỏi của đề tài này**. Thêm trục trễ vào ma trận lõi nhân số lần chạy lên gấp ba (xem Phụ lục B), và câu trả lời sẽ phụ thuộc vào một tham số mà đề tài chưa có cơ sở để chọn. Vì thế bất đồng bộ nằm ở "Hướng mở rộng", không ở RQ chính.

Hai công trình gần đây mở rộng nhánh này: FedeRICo (Orozco, Luo và Wahlström, 2026) cho phép trao đổi thông tin tại biên giữa các client kề nhau — đây là **bề mặt tấn công mới** chưa nằm trong mô hình đe doạ của đề tài; và FedASTA (Li và cộng sự, 2024) dùng attention không–thời gian nhưng **không có thành phần đối kháng** (đếm từ khoá: `byzantine`, `poison`, `malicious`, `attack`, `krum` đều bằng 0). Cả hai không trùng phạm vi, nhưng FedeRICo là lý do đề tài giới hạn mô hình đe doạ ở **kênh client–server duy nhất** thay vì giả định đó là hiển nhiên.

### 2.6 Phản chứng đã tìm và đã xử lý

Ba benchmark Byzantine tái lập được đã tồn tại — FLPoison (Zhang và cộng sự, 2025, miền ảnh), byzantine-fl-bench (2026, miền y tế), ByzFL (Gonzalez và cộng sự, 2025, thư viện tổng quát). Cả ba chứng minh cấu trúc benchmark **khả thi và đã được cộng đồng chấp nhận**, nhưng không cái nào có giao thông hay bất đồng bộ. Chi tiết đối chiếu ở **Phụ lục D**, giao thức kế thừa ở §3.9.

### 2.7 Một ghi chú về chất lượng nguồn

Một survey peer-reviewed mô tả FedGRU là có *"poisoned models"*; đếm từ khoá trong toàn văn FedGRU cho **0 lần** ở cả tám từ — nên tổng quan này chỉ trích văn bản gốc (đầy đủ ở **Phụ lục C**). Đây cũng là lý do bảng 93 bài được gọi là **cận dưới**: phương pháp đếm từ khoá chỉ sinh âm tính giả, không sinh dương tính giả.

---

## 3. Phương pháp nghiên cứu

Ba câu hỏi phân loại, trả lời trước khi vào thiết kế:

| Câu hỏi | Trả lời |
|---|---|
| Định lượng hay định tính? | **Định lượng** — kết luận dựa trên MAE, FPR, FNR, EMD đo được |
| Dữ liệu mới hay nguồn sẵn có? | **Thứ cấp** — LargeST công khai của Caltrans |
| Mô tả, tương quan, thực nghiệm? | **Thực nghiệm có kiểm soát** — biến độc lập: bộ gộp, tỉ lệ Byzantine, cường độ tấn công |

**Tổng thể và mẫu.** Toàn bộ 716 cảm biến PeMS District 11, **không lấy mẫu** nên không có sai số chọn mẫu. Đơn vị phân tích là *cảm biến* (trong phân vùng) và *vòng huấn luyện* (trong đo lường). Tập test là 20 % cuối chuỗi thời gian, không chia ngẫu nhiên — chia ngẫu nhiên sẽ để dữ liệu tương lai rò vào tập huấn luyện.

### 3.1 Dữ liệu

**Nguồn:** LargeST (Liu và cộng sự, 2023), phân vùng San Diego. Quy mô đo trên dữ liệu thực tế:

| Thuộc tính | Giá trị |
|---|---|
| Số cảm biến | 716 |
| Số tuyến cao tốc (`Fwy`) | 26 |
| Số làn chính | 2.842 (trung bình 3,97; min 2; max 8) |
| Khoảng thời gian | 2017-01-01 → 2021-12-31 |
| Độ phân giải | 5 phút gốc; tái lấy mẫu **15 phút** |
| Quan sát mỗi năm | 35.040 × 716 |
| Bounding box | 66,4 km × 95,7 km |

**Kịch bản thời gian:**

| Tập | Giai đoạn | Lý do |
|---|---|---|
| Train | 2017-01-01 → 2019-12-31 | Đủ dài cho mùa vụ |
| Validation | 6 tháng cuối 2019 | Tránh chọn siêu tham số theo phân phối COVID |
| Test | 2021 | Năm sạch nhất về can thiệp |
| Kịch bản trôi (R3, R4) | train 2019, test 2020 | Đo tác dụng trôi do COVID |

**Ba cái bẫy dữ liệu đã xác nhận bằng đo:**

1. **Parquet đã `fillna(0)`** — 0 NaN trong `sd_flow_2019.parquet`, 2,25 % ô bằng 0. Tín hiệu khuyết thiếu đã mất, và 2 cảm biến gần như chết bị che thành "lưu lượng thấp tự nhiên". **Hệ quả:** đặc trưng chất lượng phải tính lại từ HDF5 gốc, trước `fillna`.
2. **Trần 999 là censoring**, không phải giá trị thật — nhưng rất thưa: 16 / 37 / 12 ô ở 2017 / 2019 / 2021 (≤ 0,0002 % mỗi năm). Ghi chú, không cần hiệu chỉnh.
3. **Tỉ lệ zero tăng theo năm:** 2,79 % (2017) → 2,25 % (2019) → **6,19 %** (2021) — tín hiệu suy giảm cảm biến, là lý do phải có kịch bản trôi.

**Tiền xử lý:** pipeline chuẩn LargeST `resample("15min").mean().round(0).fillna(0)`. `.mean()` gây lệch đơn vị — 288 bin 5 phút cộng lại bằng 30.393 xe/ngày, tệp 15 phút chỉ 10.156 (−66,7 %). Giữ nguyên pipeline gốc để so sánh được với bài báo, và báo cáo rõ đây là trung bình, không phải tổng.

**Cổng kiểm chứng.** HL (historical last) đạt MAE trung bình 60,80 ở 2019, khớp 60,79 công bố trong Bảng 2 bài báo LargeST. Pipeline sai thì con số này lệch ngay — điều kiện chạy mọi thí nghiệm phía sau.

### 3.2 Phân vùng client

**Ràng buộc từ metadata:** trong 10 cột của `sd_sensors_716.csv`, `District`, `County` và `Type` đều là **hằng số** trên toàn bộ 716 cảm biến. Chỉ có `Fwy` (26 giá trị) và toạ độ là trục chia khả dụng. Thiết kế "chia theo quận" không thi hành được trên SD.

**P-A — theo hành lang, có sàn kích thước (kịch bản chính).** Nhóm theo `Fwy` (26 nhóm), gộp mọi nhóm dưới 10 cảm biến vào nhóm kề gần nhất về toạ độ trung bình, rồi gộp thêm các cặp nhỏ nhất nếu còn dưới 20 client.

Lý do có sàn: phân bố hành lang cực kỳ lệch — I5-N có **95** cảm biến, SR11-E chỉ **1**. Tỉ lệ max/min = **95×**. Client một cảm biến không huấn luyện được gì, và median sẽ coi nó là outlier. Kết quả kỳ vọng: **20–24 client**, kích thước 10–95.

**P-B — theo không gian.** KMeans trên `(Lat, Lng)` với k = 8 / 16 / 32; đo được min/median/max = 89/89/90, 44/45/45, 22/22/23, tỉ lệ **1,0×**. Cân bằng hoàn hảo nhưng **mất ý nghĩa vận hành** — một cụm cắt ngang nhiều hành lang thuộc nhiều đơn vị quản lý. Dùng làm đối chứng.

**P-C — theo cụm hành vi (DTW).** Gom theo dạng chuỗi thời gian, không theo vị trí; dị biệt cao nhất, dùng làm stress-test.

**Dị biệt đo được (kết quả, không phải phụ lục).** Earth Mover's Distance giữa phân phối lưu lượng từng hành lang, toàn bộ 716 cảm biến, 2019, giờ 06–22:

| Cách chia | EMD min | median | p90 | max |
|---|---|---|---|---|
| Theo hành lang (26 nhóm) | 4,1 | **86,4** | 193,3 | 307,4 |
| IID ngẫu nhiên (26 nhóm) | 5,2 | **22,6** | 43,9 | 74,1 |

**Tỉ lệ median = 3,81×.** Chia theo hành lang tạo dị biệt lớn gần bốn lần IID, và đo được **trước khi chạy thí nghiệm nào**. Đây là **cổng kiểm tra**: nếu EMD median < 2× IID, dữ liệu SD không đủ dị biệt và phải chuyển sang LargeST GBA/CA thay vì báo cáo kết quả âm như một phát hiện.

Nguồn dị biệt cụ thể: lưu lượng trung bình I15-N là **414,6 xe/15ph**, SR11-E chỉ **23,1** — chênh **18×**. Client I15-N có update magnitude lớn gấp 18 lần, nên median sẽ coi nó là outlier. Đây chính là cơ chế Karimireddy và cộng sự dự đoán.

**Tính tái lập:** phát hành script sinh phân vùng **và** tệp JSON ánh xạ client → danh sách `ID` cảm biến, kèm hash SHA-256, để phân vùng không phụ thuộc phiên bản metadata.

### 3.3 Mô hình dự báo

Kiến trúc cố định: **GRU** hoặc **MLP nhỏ** cho từng nút, 12 bước vào / 12 bước ra. Mô hình nhỏ vì cần chạy hàng trăm cấu hình, và mục tiêu là đo tác động của tấn công, không đạt kết quả tốt nhất.

**Giới hạn phải khai báo:** mô hình chung cho từng nút **bỏ qua phụ thuộc không gian**, nên kết luận chỉ áp dụng cho lớp mô hình không dùng đồ thị. Vì vậy **STGCN là bắt buộc** trên một tập con — 3 bộ gộp × 2 tấn công × 2 tỉ lệ độc hại — để kiểm tra thứ hạng bộ gộp có đổi theo kiến trúc không.

### 3.4 Gán nhãn

Hai loại, tách bạch. **Nhãn client độc hại** do nhóm tự tiêm nên biết chắc — dùng đo TPR/FPR của các bộ gộp có bước chọn lọc. **Đặc trưng chất lượng mức client:** ba đặc trưng tính tự động từ dữ liệu train **trước khi `fillna`** — tỉ lệ khuyết thiếu, số giờ dài nhất đứng yên, mức trôi giữa 2019 và 2020. Không xây nhãn bất thường mức thời điểm: đối chiếu sự cố PeMS và kiểm tra thủ công tốn công mà không câu hỏi nào cần.

### 3.5 Mô hình đe dọa

Tỉ lệ client độc hại 0 / 10 / 20 / 30 / 40 %, chọn ngẫu nhiên theo seed. Hai mức hiểu biết: (i) chỉ biết dữ liệu và cập nhật của mình; (ii) biết cả cập nhật trung thực. Kịch bản mặc định: tấn công **từ vòng 1, liên tục mọi vòng, các client độc hại phối hợp** gửi cùng một cập nhật.

**Bảng hợp lệ lý thuyết.** Krum cần *n ≥ 2f + 3*, Bulyan cần *n ≥ 4f + 3*:

| n | 10 % | 20 % | 30 % | 40 % |
|---|---|---|---|---|
| 8 | ✓✓ | ✓✗B | ✓✗B | **✗K ✗B** |
| 16 | ✓✓ | ✓✓ | ✓✗B | ✓✗B |
| 20 | ✓✓ | ✓✓ | ✓✗B | ✓✗B |
| 32 | ✓✓ | ✓✓ | ✓✗B | ✓✗B |

Ba quy tắc: ô `n = 8 @ 40 %` **bất khả** với Krum → loại khỏi bảng chính, ghi "ngoài giới hạn lý thuyết"; Bulyan chỉ báo cáo ở ≤ 20 %; **Krum chạy thêm cấu hình f ước lượng sai** (cố định f = 20 % × n bất kể tỉ lệ thật) vì oracle là giả định không thực tế.

### 3.6 Ma trận tấn công và trục cường độ

**Trục cường độ chung.** Mỗi tấn công được điều chỉnh tham số sao cho MAE cục bộ của client độc hại tăng **+25 % / +50 % / +100 %** so với khi sạch. Nhờ vậy mọi tấn công đo trên cùng thang, và so sánh không phụ thuộc tham số được chọn.

| Nhóm | Tấn công | Nguồn |
|---|---|---|
| Cập nhật mô hình | Sign-flip, Scaling, Gaussian, ALIE, IPM, Min-Max, Min-Sum | Baruch và cộng sự (2019); Xie và cộng sự (2019); Shejwalkar & Houmansadr (2021) |
| Dữ liệu cảm biến | Nhân k, Kẹt giá trị, Trôi dần, Báo 0 xe, Phát lại | **Đóng góp mới** |
| Có mục tiêu | Báo-0 / nhân k chỉ trong 07–09h và 16–19h | Biến thể của nhóm trên |

**Bộ kiểm tra chất lượng 4 luật, chỉ dùng lưu lượng (LargeST không có occupancy hay tốc độ):**

```
L1: đứng yên ≥ 6 giờ liên tục
L2: vượt phân vị 99,9 % của chính cảm biến (tính trên 2017–2019)
L3: lệch > 3σ so với trung bình cảm biến kề cùng tuyến (theo ID2)
L4: bằng 0 kéo dài ≥ 3 giờ trong khung 06–22
```

Mỗi tấn công báo cáo **tỉ lệ vượt từng luật** và **tỉ lệ vượt cả bốn**.

### 3.7 Cơ chế phòng thủ

Chín cơ chế, chia ba vai. **Hai cận:** Local-only (cận dưới — không chia sẻ gì) và Centralized (cận trên — học tập trung toàn bộ). **Sáu phòng thủ Byzantine:** FedAvg làm đối chứng không phòng thủ, Krum (chạy cả f oracle và f ước lượng sai), Multi-Krum, Median, Trimmed Mean (β = 0,1/0,2/0,3), Norm Clipping. **Một đối chứng dị biệt:** Bucketing.

Nên có nếu kịp: FLTrust, Centered Clipping, RFA. Bảng tham số ở **Phụ lục F**.

**Vì sao Bucketing tách riêng.** Karimireddy và cộng sự (2022) đề xuất Bucketing để xử lý **dị biệt**, không chống client độc hại. Nó gom update thành nhóm nhỏ, lấy trung bình trong nhóm, rồi đưa vào bộ gộp Byzantine. Vai trò ở đây là **đối chứng để chứng minh cái giá phòng thủ đo được là do dị biệt, không do lỗi cài đặt**: nếu không có Bucketing, kết quả "Krum gãy ở 0 % Byzantine" sẽ bị quy cho bug.

**Gãy theo thiết kế.** Trimmed Mean với β phải gãy khi tỉ lệ độc hại > β. Mọi ô như vậy được gắn nhãn `gãy_theo_thiết_kế` trong bảng kết quả, **không trình bày như phát hiện**.

**Cổng kiểm tra trước ma trận tấn công:** chạy Local-only, Centralized và FedAvg sạch (10 seed mỗi cái). **Cổng:** MAE của FedAvg phải tốt hơn Local-only với Wilcoxon ghép cặp, p < 0,05. Không đạt thì dừng, đổi cách chia client hoặc chuyển sang FL cá nhân hoá — không chạy tiếp.

### 3.8 Chỉ số đánh giá

Bốn nhóm, mỗi nhóm có một chỉ số **bắt buộc** không được bỏ. **Độ chính xác:** masked MAE (bỏ ô NaN gốc, không tính ô đã điền), RMSE, MAPE có ngưỡng 20 xe/15ph, và **mean magnitude đi kèm mọi MAE**. **Mức client:** MAE từng client, client tệ nhất, phân vị 90 — vì cái giá phòng thủ dồn lên vài client chứ không hiện ở trung bình. **Phòng thủ:** điểm gãy (110 % MAE FedAvg sạch), ASR, utility retention, và **bắt buộc cả FPR lẫn FNR**. **Hệ thống:** wall-clock mỗi cấu hình.

**Quy tắc báo cáo:** không MAE mà thiếu mean magnitude; không hiệu quả phòng thủ mà thiếu FPR; không so sánh mà thiếu FedAvg cùng điều kiện. Bảng định nghĩa đầy đủ ở **Phụ lục F**.

### 3.9 Thiết kế thống kê và kế hoạch phân tích

**Số seed, tính ngược từ kiểm định.** Wilcoxon signed-rank chính xác hai phía có p nhỏ nhất = 2/2ⁿ. Với 5 seed, p nhỏ nhất là **0,0625** — không đạt 0,05 dù hiệu ứng lớn đến đâu; đây là lý do bản v2 (3 seed) không thể kết luận gì. Sau hiệu chỉnh Holm cho m phép so sánh, cần p_min < 0,05/m:

| m (số so sánh chính) | Seed tối thiểu |
|---|---|
| 1 | 6 |
| 4 | 8 |
| 10 | 9 |
| 20 | 10 |

**Chốt: 10 seed cho ô chính** (cổng, 9 bộ gộp khi sạch, 2–3 ô tấn công trọng tâm). Ô còn lại 3–5 seed, **chỉ báo cáo mô tả, không kiểm định**.

**Kiểm định phải dùng:**

| Câu hỏi | Kiểm định | Lý do |
|---|---|---|
| Bộ gộp A khác B? | **Wilcoxon signed-rank ghép cặp theo seed** | Cùng seed cho cả hai → ghép cặp |
| Tương đương? | **TOST, biên ±10 % MAE** | Câu hỏi "có giảm không" cần kiểm định tương đương |
| Chỉ số mức client | **Bootstrap theo cụm (seed × client)** | Client không độc lập |
| Nhiều so sánh | **Holm** | Kiểm soát FWER |

**Kế hoạch phân tích chốt trước khi chạy**, ghi ngày: danh sách m so sánh chính (m = 10: 9 bộ gộp so FedAvg, 1 so Local-only); kiểm định từng so sánh; biên tương đương ±10 %; số seed từng tầng; quy tắc tách ô vi phạm lý thuyết.

**Kế thừa từ byzantine-fl-bench (2026):** chốt luật trước khi chạy và ghi ngày; ghi `invalid` khi giả định cơ chế bị vi phạm; chạy đối chứng bỏ client tấn công để tách "mất dữ liệu" khỏi "bị tấn công".

---

## 4. Kết quả kỳ vọng và đóng góp

### 4.1 Đóng góp

| # | Đóng góp | Loại | Vì sao đứng vững |
|---|---|---|---|
| **C1** | Benchmark Byzantine-FL trên PeMS thật, phát hành phân vùng + giao thức | Artefact | Giao của "dữ liệu thật" + "Byzantine" + "cấu trúc benchmark" hiện rỗng |
| **C2** | Định lượng **cái giá của phòng thủ** dưới dị biệt tự nhiên: mức loại nhầm ở 0 % độc hại, phân bố theo client | Phát hiện | Karimireddy và cộng sự chứng minh *có* gãy; chưa ai đo *bao nhiêu* trên dữ liệu giao thông thật |
| **C3** | Trục cường độ chung cho tấn công ở mức dữ liệu cảm biến, và tỉ lệ vượt bộ kiểm tra chất lượng | Phương pháp | Cho phép so sánh tấn công cảm biến với tấn công cập nhật trên cùng thang |
| **C4** | Kết luận về yếu tố nào của dữ liệu thật gây suy giảm (ablation R0–R4) | Phân tích | Tách được ba yếu tố chồng nhau mà thiết kế so-sánh-hai-bộ-dữ-liệu không tách được |

Giao thức tái lập (seed, cấu hình, mã commit) nằm trong §3.9 như **yêu cầu chất lượng**, không phải đóng góp — đây là điểm sửa so với v2.

### 4.2 Ý nghĩa thực tiễn

**Cho cơ quan vận hành:** quy trình kiểm tra trước khi tham gia liên kết — bộ gộp nào chịu được bao nhiêu phần trăm client bị chiếm, và mất bao nhiêu độ chính xác khi không có tấn công.

**Cho cộng đồng nghiên cứu:** một sân chơi chung. Mỗi bài Byzantine hiện tự chọn dataset và thước đo nên kết quả không so sánh được; phân vùng và baseline chuẩn biến "phương pháp của tôi tốt hơn" thành tuyên bố kiểm chứng được.

**Cho lĩnh vực:** dịch chuyển từ "đề xuất thuật toán mới" sang "đo lường nghiêm túc" — với 11 bài đã đề xuất thuật toán nhưng 0 bài báo cáo đủ chỉ số, giá trị biên của thuật toán thứ mười hai thấp hơn giá trị của một thước đo đúng.

### 4.3 Kết quả có thể công bố trong mọi nhánh

| Nhánh | Kết quả | Đóng góp |
|---|---|---|
| H1 đúng | Krum gãy sớm hơn Median ở 0 % độc hại | Bằng chứng dị biệt phá Krum trước |
| H1 sai | Không khác biệt | Dị biệt không phải cơ chế chính — tìm nguyên nhân khác |
| H2 đúng | Có ngưỡng tỉ lệ độc hại tới hạn | Khuyến nghị ngưỡng triển khai |
| H2 sai | Không có ngưỡng chung | Kết luận phải đánh giá theo từng bộ gộp × tấn công |
| H3 đúng | Dương tính giả chiếm ưu thế | "Phòng thủ hỏng vì quá khắt khe" + FPR |
| H3 sai | Âm tính giả chiếm ưu thế | "Phòng thủ yếu vì bỏ sót" + FNR |
| H4 đúng | Bucketing thu hẹp khoảng cách | Chuyển được kỹ thuật sang giao thông |
| H4 sai | Bucketing không cứu được | Dị biệt giao thông khác dị biệt Dirichlet |

Không nhánh nào ra "không có gì để báo cáo" — đây là tiêu chí thiết kế, không phải may mắn.

---

## 5. Kế hoạch triển khai và quản trị rủi ro

### 5.1 Phân rã công việc, có cổng

| Tuần | Việc | Cổng (định lượng) |
|---|---|---|
| 1–2 | Rà soát có hệ thống (Scopus/IEEE/ACM); unit test 9 bộ gộp; **đo thời gian một lần chạy** | Không có công trình trùng RQ2; sai lệch với ByzFL < 1e-6 |
| 3 | Local-only, Centralized, FedAvg sạch (10 seed) | **FedAvg tốt hơn Local-only, p < 0,05** |
| 4–5 | 9 bộ gộp khi sạch; FPR ở 0 % độc hại (RQ2) | FPR đo được cho mọi bộ gộp có chọn lọc |
| 6–8 | Ma trận tấn công mô hình (RQ1, RQ3) | Điểm gãy xác định cho ≥ 80 % ô hợp lệ |
| 9 | Tấn công cảm biến + biến thể giờ cao điểm | Mọi tấn công trên cùng trục cường độ |
| 10 | Ablation R0–R4 (RQ4); kiểm tra lại bằng STGCN | Mỗi khác biệt quy được về một yếu tố |
| 11–12 | Phân tích theo kế hoạch đã chốt; đóng gói | Mọi so sánh chính đạt ý nghĩa sau Holm |

**Tổng 12 tuần — nhưng chỉ đủ cho Tầng 1.** Ma trận đầy đủ cần 22.240 lần chạy (Phụ lục B), tức 46–93 tuần; 12 tuần chỉ chứa được khoảng 2.200 lần (Tầng 1). Kế hoạch vì thế chạy **theo tầng đã định trước**, không theo "cố hết": tuần 4–8 chạy Tầng 1, tuần 9–10 mở rộng nếu kịp, tuần 11–12 phân tích và đóng gói trên **đúng những gì đã chạy**.

Xử lý khi cổng không đạt: tuần 3 thất bại → đổi cách chia (ít client hơn, client lớn hơn) hoặc chuyển FL cá nhân hoá. Thời gian chạy > 0,5 h/lần → cắt tấn công cảm biến xuống 3 kiểu, Tầng 1 còn 1.960 lần.

### 5.2 Ma trận rủi ro

| Rủi ro | Xác suất | Dấu hiệu sớm | Đối sách |
|---|---|---|---|
| **FL không tốt hơn Local-only** | Trung bình | Cổng tuần 3 không đạt | Đổi cách chia; hoặc chuyển FL cá nhân hoá |
| **Không đủ lực thống kê** | Trung bình | SD giữa seed > hiệu ứng kỳ vọng | Tăng seed ô chính; bootstrap theo cụm |
| **Lỗi cài đặt bộ gộp** | Cao | Unit test sai; lệch ByzFL | Sửa trước tuần 3, không chạy tiếp |
| **Ô vi phạm n ≥ 2f+3** | Cao | Lập ma trận là thấy | Tách khỏi bảng chính, ghi chú |
| **Dữ liệu không đủ dị biệt** | Thấp | EMD median < 2× IID | Chuyển sang LargeST GBA/CA |
| **Vượt thời gian chạy** | Cao | Đo ở tuần 1 | Cắt tầng cảm biến + giảm kiểu tấn công |
| **Pipeline đã fillna, mất khuyết thiếu** | **Đã xảy ra** | Parquet có 0 NaN | Đọc lại HDF5 gốc trước tuần 3 |
| **Trùng hướng khi có bài mới** | Trung bình | Rà soát tuần 1–2 | Dịch sang tấn công cảm biến (C3) |

### 5.3 Sản phẩm bàn giao

| Mã | Sản phẩm | Tuần |
|---|---|---|
| **D1** | Mã nguồn FL + 9 bộ gộp + 14 tấn công, có unit test | 2 |
| **D2** | Ba phân vùng client (JSON + script + hash) | 3 |
| **D3** | Bảng điểm gãy và cái giá phòng thủ | 5 |
| **D4** | Kết quả ablation R0–R4 | 10 |
| **D5** | Kế hoạch phân tích đã chốt + log toàn bộ lần chạy | 11 |
| **D6** | Báo cáo + bài báo | 12 |

---

## 6. Tài liệu tham khảo

Babar, F. F., Khan, S., & Parkinson, S. (2026). HuddsTrafficFL: A benchmark testbed and dataset for Byzantine-robust federated learning in urban traffic systems. *Knowledge-Based Systems*. https://doi.org/10.1016/j.knosys.2026.117003

Badu-Marfo, G., Al Mallah, R., & Farooq, B. (2024). Defense via behavior attestation against attacks in connected and automated vehicles based federated learning systems. *2024 IEEE 99th Vehicular Technology Conference (VTC2024-Spring)*. https://doi.org/10.1109/VTC2024-Spring62846.2024.10683195

Baruch, G., Baruch, M., & Goldberg, Y. (2019). A little is enough: Circumventing defenses for distributed learning. *Advances in Neural Information Processing Systems 32*.

Blanchard, P., El Mhamdi, E. M., Guerraoui, R., & Stainer, J. (2017). Machine learning with adversaries: Byzantine tolerant gradient descent. *Advances in Neural Information Processing Systems 30*, 119–129.

Cao, X., Fang, M., Liu, J., & Gong, N. Z. (2021). FLTrust: Byzantine-robust federated learning via trust bootstrapping. *Network and Distributed System Security Symposium*. https://doi.org/10.14722/ndss.2021.24434

Gonzalez, M., Guerraoui, R., Pinot, R., Rizk, G., Stephan, J., & Taiani, F. (2025). ByzFL: Research framework for robust federated learning. arXiv:2505.24802. https://doi.org/10.48550/arXiv.2505.24802

Karimireddy, S. P., He, L., & Jaggi, M. (2022). Byzantine-robust learning on heterogeneous datasets via bucketing. *International Conference on Learning Representations*. arXiv:2006.09365

Li, K., Zhang, Y., Wang, H., Zhuo, Y., & Chen, X. (2024). FedASTA: Federated adaptive spatial-temporal attention for traffic flow prediction. arXiv:2405.13090. https://doi.org/10.48550/arXiv.2405.13090

Liu, X., Xia, Y., Liang, Y., Hu, J., Wang, Y., & Bai, L. (2023). LargeST: A benchmark dataset for large-scale traffic forecasting. *Advances in Neural Information Processing Systems 36*. https://doi.org/10.52202/075280-3293

Liu, Y., Yu, J. J. Q., Kang, J., Niyato, D., & Zhang, S. (2020). Privacy-preserving traffic flow prediction: A federated learning approach. *IEEE Internet of Things Journal, 7*(8), 7751–7763. https://doi.org/10.1109/JIOT.2020.2991401

Ma, H., Yang, K., & Jiao, Y. (2025). Cellular traffic prediction via Byzantine-robust asynchronous federated learning. *IEEE Transactions on Network Science and Engineering*. https://doi.org/10.1109/TNSE.2025.3545912

McMahan, B., Moore, E., Ramage, D., Hampson, S., & Agüera y Arcas, B. (2017). Communication-efficient learning of deep networks from decentralized data. *Proceedings of the 20th International Conference on Artificial Intelligence and Statistics* (PMLR 54, pp. 1273–1282).

Meng, C., Rambhatla, S., & Liu, Y. (2021). Cross-node federated graph neural network for spatio-temporal data modeling. *Proceedings of the 27th ACM SIGKDD Conference on Knowledge Discovery and Data Mining*. https://doi.org/10.1145/3447548.3467371

Nguyen, J., Malik, K., Zhan, H., Yousefpour, A., Rabbat, M., Malek, M., & Huba, D. (2022). Federated learning with buffered asynchronous aggregation. *Proceedings of the 25th International Conference on Artificial Intelligence and Statistics* (PMLR 151, pp. 3581–3607).

Orozco, F., Luo, M., & Wahlstrom, J. (2026). FedeRICo: Federated region-influenced coupling for traffic flow prediction. arXiv:2609.20026. https://doi.org/10.48550/arXiv.2609.20026

Pang, X., Zhao, C., Wang, Z., Hu, J., Wang, Y., Wang, L., Wei, T., Ren, K., & Chen, C. (2025). PoiSAFL: Scalable poisoning attack framework to Byzantine-resilient semi-asynchronous federated learning. *34th USENIX Security Symposium*.

Shejwalkar, V., & Houmansadr, A. (2021). Manipulating the Byzantine: Optimizing model poisoning attacks and defenses for federated learning. *Network and Distributed System Security Symposium*. https://doi.org/10.14722/ndss.2021.24498

Xie, C., Koyejo, O., & Gupta, I. (2019). Fall of empires: Breaking Byzantine-tolerant SGD by inner product manipulation. *Proceedings of the 35th Conference on Uncertainty in Artificial Intelligence*.

Yin, D., Chen, Y., Kannan, R., & Bartlett, P. (2018). Byzantine-robust distributed learning: Towards optimal statistical rates. *Proceedings of the 35th International Conference on Machine Learning* (PMLR 80, pp. 5650–5659).

Zhang, C., et al. (2024). FedGTP: Exploiting inter-client spatial dependency in federated graph-based traffic prediction. *Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining*. https://doi.org/10.1145/3637528.3671613

Zhang, H., Liu, Y., He, X., Wu, J., Cong, T., & Huang, X. (2025). SoK: Benchmarking poisoning attacks and defenses in federated learning. arXiv:2502.03801. https://doi.org/10.48550/arXiv.2502.03801

Zheng, T., Li, B., et al. (2024). Poisoning attacks on federated learning-based wireless traffic prediction. *IFIP Networking Conference*. https://doi.org/10.23919/IFIPNetworking62109.2024.10619763

---

## Phụ lục A. Kết quả sơ bộ đã có

Bốn hạng mục đã đo, giảm rủi ro thực thi:

| Hạng mục | Trạng thái | Bằng chứng |
|---|---|---|
| Metadata 716 cảm biến | ✅ | `sd_sensors_716.csv`, 26 hành lang |
| Dị biệt đo được (EMD 3,81× IID) | ✅ | EMD median 86,4 vs 22,6 |
| Cổng kiểm chứng pipeline | ✅ | HL MAE 2019 = 60,80, khớp 60,79 công bố |
| Ba bẫy dữ liệu đã xác định | ✅ | 0 NaN, 2 cảm biến chết, trần 999 thưa |
| Chạy trên dữ liệu thật | ❌ | **Chưa có kết quả nào** |

---

## Phụ lục B. Giả định và lý do loại bất đồng bộ khỏi ma trận lõi

**Giả định:** (1) PeMS San Diego đại diện cho một mạng cao tốc đô thị điển hình; (2) GRU từng nút là proxy hợp lý cho mô hình dự báo; (3) phân vùng theo hành lang phản ánh ranh giới quản lý thực tế.

**Vì sao bất đồng bộ ở "Hướng mở rộng", không ở ma trận lõi.** Thêm một trục trễ bốn mức nhân số lần chạy lên **bốn lần**. Bất đồng bộ được giữ như một thí nghiệm riêng (2 bộ gộp × 2 tấn công × 4 tỉ lệ × 4 mức trễ × 2 seed = 128 lần), trả lời câu hỏi **thứ hạng bộ gộp có đổi khi có trễ không** — một câu hỏi có cực trị, không phải đường cong bốn mức.

**Khối lượng chạy của ma trận lõi — tính lại từ thiết kế.** Đây là con số phải đứng vững trước hội đồng, nên nó được tính từ §3.5–3.9 chứ không ước lượng:

| Thành phần | Phép tính | Số lần chạy |
|---|---|---|
| Ma trận tấn công chính | 13 ô tham số × 14 tấn công × 4 tỉ lệ × 3 cường độ × 10 seed | **21.840** |
| Lưới sạch (0 % độc hại) | 13 ô × 10 seed | 130 |
| Ablation R0–R4 | 5 cấu hình × 10 seed × 3 bộ gộp | 150 |
| Tập con STGCN | 3 bộ gộp × 2 tấn công × 2 tỉ lệ × 10 seed | 120 |
| **Tổng** | | **22.240** |

**13 ô tham số** (không phải 9): FedAvg chạy hai biến thể có/không trọng số, Krum chạy hai biến thể *f* oracle và *f* ước lượng sai, Trimmed Mean chạy ba mức β — đúng như rubric yêu cầu.

**Hệ quả về thời gian — và đây là rủi ro lớn nhất của đề tài.** Ở 0,35 h/lần, 22.240 lần cần **46 tuần**; ở 0,7 h/lần cần **93 tuần**. Không vừa 12 tuần. Vì thế kế hoạch phải hạ tầng theo bậc, và bậc phải viết trước:

- **Tầng 1 (bắt buộc, 2.220 lần)** — 13 ô × 14 tấn công × 1 tỉ lệ (20 %) × 1 cường độ (+50 %) × 10 seed = 1.820 lần; cộng lưới sạch (130), ablation (150) và STGCN (120) = **2.220**. Ở 0,35 h/lần là **4,6 tuần**. Đủ để trả lời RQ1, RQ2, RQ4.
- **Tầng 2 (nếu tầng 1 xong trước tuần 8)** — mở tỉ lệ 10/30/40 % và hai cường độ còn lại.
- **Tầng 3 (chỉ khi còn thời gian)** — phần còn lại.

Báo cáo phải ghi rõ tầng nào đã chạy. Một benchmark chạy đủ tầng 1 và khai báo trung thực **đứng vững hơn** một benchmark hứa 22.240 lần rồi nộp 1.178.

**Cơ sở lý thuyết cho hướng mở rộng:** FedBuff (Nguyen và cộng sự, 2022) chứng minh τ_max,K ≤ ⌈τ_max,1/K⌉, tức tăng bộ đệm làm giảm độ trễ hiệu dụng. Nhưng quan hệ **không đơn điệu** — trên CelebA, K = 10 cho 31,9 nghìn client trips còn K = 100 cho 71,6, tệ hơn cả K = 1 (32,4). Nếu mở rộng sang async, câu hỏi đúng là *điểm tối ưu của K khi có tấn công*, không phải "K càng lớn càng tốt".

---

## Phụ lục C. Kiểm chứng chất lượng nguồn thứ cấp

Một survey peer-reviewed mô tả FedGRU — bài nền của FL cho giao thông — là có *"malicious users introducing poisoned models"* và cơ chế *"verifiers"*. Nếu đúng, FedGRU đã là một phần của khoảng trống và luận điểm của đề cương phải đổi.

Đếm từ khoá trong toàn văn FedGRU (Liu và cộng sự, 2020):

| Từ khoá | Số lần |
|---|---|
| `poison` | 0 |
| `verifier` | 0 |
| `malicious` | 0 |
| `attack` | 0 |
| `Byzantine` | 0 |
| `adversar` | 0 |
| `tamper` | 0 |
| `trust` | 0 |

**Cả tám đều 0 lần.** Survey mô tả sai bài gốc. Vì thế mọi tuyên bố về một bài cụ thể trong đề cương này được đọc từ văn bản gốc, không trích qua survey.

---

## Phụ lục D. Phản chứng và giao thức kế thừa

Ba benchmark Byzantine tái lập được đã tồn tại, nên "chưa có benchmark Byzantine nào" là sai:

| Công trình | Miền | Đóng gói | Dữ liệu giao thông? |
|---|---|---|---|
| **FLPoison** (Zhang và cộng sự, 2025) | Ảnh | 15 tấn công × 17 phòng thủ | ❌ |
| **byzantine-fl-bench** (2026) | Y tế (FLamby) | 8 quy tắc × 7 tấn công, protocol chốt ngày | ❌ |
| **ByzFL** (Gonzalez và cộng sự, 2025) | Tổng quát | Thư viện chuẩn, cấu hình JSON | ❌ |

**Vì sao đây là tin tốt:** cả ba chứng minh cấu trúc benchmark Byzantine **khả thi và đã được chấp nhận**, nên đề tài không phải thuyết phục hội đồng rằng ý tưởng làm được. Chúng trống ở đúng hai trục: không có dữ liệu giao thông, không có đo lường cái giá của dị biệt tự nhiên.

**Điều đề tài không được nhận:** "ý tưởng benchmark Byzantine-FL" không phải đóng góp mới. Nếu bị hỏi khác FLPoison ở đâu, câu trả lời phải là ba điều kiện đồng thời — dữ liệu giao thông thật, phân vùng phát hành, và đo lường cái giá phòng thủ dưới dị biệt tự nhiên.

**Giao thức kế thừa từ byzantine-fl-bench:** (1) chốt luật trước khi chạy, ghi ngày; (2) ghi `invalid` khi giả định cơ chế bị vi phạm — Bulyan cần *n ≥ 4f + 3*, Krum cần *n ≥ 2f + 3*; (3) chạy đối chứng bỏ client tấn công, để tách phần sụt do mất dữ liệu khỏi phần sụt do tấn công. Với giao thông điều này đặc biệt quan trọng: loại một client là mất luôn dữ liệu của vùng đó.

**Về FedBuff.** Bài này là nguồn gốc lý thuyết của bộ đệm K, và đếm từ khoá trong toàn văn cho `byzantine` = 0, `poison` = 0, `malicious` = 0, `adversar` = 0, `krum` = 0. Nó **không** phải công trình Byzantine, và được trích ở đây cho đúng vai trò: cơ sở cho hướng mở rộng async, không phải đối thủ trong ma trận.

---

## Phụ lục E. Ngân sách, nguồn lực và đạo đức

### E.1 Ngân sách

| Hạng mục | Chi phí |
|---|---|
| Dữ liệu LargeST (công khai) | 0 |
| Thư viện (PyTorch, scikit-learn, scipy) | 0 |
| Lưu trữ kết quả (Zenodo, DOI) | 0 |
| GPU dự phòng (tuỳ chọn) | ~2.000.000 VNĐ |
| **Tổng** | **0 – 2.000.000 VNĐ** |

Thời gian: 12 tuần × 20 giờ = **240 giờ** công.

### E.2 Đạo đức

Dữ liệu công khai của Caltrans PeMS, không có thông tin cá nhân — cảm biến vòng chỉ đếm xe. Tấn công mô phỏng trên dữ liệu đã công bố, không nhắm vào hệ thống đang vận hành. Mã tấn công phát hành công khai vì mục đích tái lập — chuẩn trong lĩnh vực (PoiSAFL, USENIX Security 2025).

**Nguyên tắc trung thực:** mọi con số trong báo cáo đọc từ artefact đã chạy, không phải ước lượng. Chỗ nào là kế hoạch thì ghi rõ là kế hoạch.

---

## Phụ lục F. Đặc tả chi tiết cơ chế phòng thủ và chỉ số

### F.1 Chín cơ chế, tham số và điều kiện áp dụng

| # | Cơ chế | Nhóm | Tham số | Điều kiện áp dụng |
|---|---|---|---|---|
| 1 | **Local-only** | Cận dưới | — | Không chia sẻ; mỗi client học riêng |
| 2 | **Centralized** | Cận trên | — | Toàn bộ dữ liệu về một chỗ |
| 3 | **FedAvg** | Đối chứng | trung bình có trọng số theo số mẫu | Không phòng thủ |
| 4 | **Krum** | Phòng thủ | *f* oracle và *f* = 20 % n | Cần *n ≥ 2f + 3* |
| 5 | **Multi-Krum** | Phòng thủ | *m = n − f − 2* | Cùng điều kiện Krum |
| 6 | **Median** | Phòng thủ | trung vị từng chiều | Không cần biết *f* |
| 7 | **Trimmed Mean** | Phòng thủ | β = 0,1 / 0,2 / 0,3 | Gãy theo thiết kế khi tỉ lệ > β |
| 8 | **Bucketing** | Đối chứng dị biệt | bucket size 5–10 | Không chống tấn công — chỉ giảm phương sai |
| 9 | **Norm Clipping** | Phòng thủ | ngưỡng cắt theo norm trung vị | Chi phí gần 0 |

Nên có: FLTrust (cần tập sạch ở server), Centered Clipping, RFA/Geometric Median.

**FedAvg có hai biến thể phải chạy cả hai:** có trọng số theo số mẫu và không trọng số. Median và Krum vốn không có trọng số, nên nếu chỉ chạy FedAvg có trọng số thì khác biệt giữa chúng có thể bị nhầm là tác dụng của phòng thủ thay vì tác dụng của cách lấy trung bình.

### F.2 Định nghĩa chỉ số

| Nhóm | Chỉ số | Định nghĩa / ngưỡng |
|---|---|---|
| **Độ chính xác** | Masked MAE | Bỏ qua ô NaN gốc; không tính ô đã điền |
| | RMSE | — |
| | MAPE có ngưỡng | Chỉ tính ô có lưu lượng ≥ 20 xe/15ph (tránh nổ ở đêm và ở tấn công báo-0) |
| | Mean magnitude | Độ lớn trung bình dữ liệu — **bắt buộc đi kèm MAE** |
| **Mức client** | MAE từng client | — |
| | MAE client tệ nhất | max trên client |
| | MAE phân vị 90 | — |
| **Giờ cao điểm** | MAE 07–09h, 16–19h | — |
| **Phòng thủ** | Điểm gãy | Tỉ lệ độc hại nhỏ nhất mà MAE > 110 % MAE FedAvg sạch |
| | ASR | Tỉ lệ vòng tấn công đạt mục tiêu |
| | Utility retention | MAE có phòng thủ / MAE sạch |
| | FPR | Tỉ lệ client trung thực bị loại — **bắt buộc** |
| | FNR | Tỉ lệ client độc hại được nhận — **bắt buộc** |
| **Hệ thống** | Wall-clock | Giờ/cấu hình, để ước lượng khối lượng |

### F.3 Ablation R0–R4

Bốn cấu hình bật/tắt ba yếu tố của dữ liệu thật, giữ cố định mạng đường, mô hình và tấn công:

| Cấu hình | Khuyết thiếu | Chia client | Trôi phân phối |
|---|---|---|---|
| **R0** | Đã điền khuyết | IID | 2019 / 2019 |
| **R1** | Đã điền khuyết | Theo hành lang | 2019 / 2019 |
| **R2** | Đã điền khuyết | Theo hành lang | 2019 / 2020 |
| **R3** | Giữ khuyết thiếu (masked loss) | IID | 2019 / 2019 |
| **R4** | Giữ khuyết thiếu | Theo hành lang | 2019 / 2020 |

**Vì sao R3 tồn tại.** Bản góp ý ban đầu đặt R1 = "khuyết thiếu thật" đối lập với R0 = "đã nội suy". Nhưng "đã nội suy" nghĩa là đã áp một chiến lược điền khuyết, nên cấu hình đó đo **tác dụng của chiến lược điền khuyết**, không đo **tác dụng của việc dữ liệu có khuyết thiếu**. Hai thứ khác nhau:

- **Giữ khuyết thiếu với masked loss** → phòng thủ thấy client "thưa" dữ liệu thật.
- **Đã điền khuyết** → client trông đầy đủ nhưng có giá trị bịa.

R0→R3 đo tác dụng của *khuyết thiếu tồn tại*; R3→R1 đo tác dụng của *điền khuyết*. Tách được hai hiệu ứng này là điều kiện để kết luận "yếu tố nào gây suy giảm" có nghĩa.
