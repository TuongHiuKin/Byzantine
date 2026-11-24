---
hide:
  - navigation
---

# Tiêu chí đánh giá dữ liệu và kế hoạch giả lập đầu tiên

*Benchmark đánh giá dữ liệu cho Federated Learning chống tấn công Byzantine trên dữ liệu giao thông · cập nhật 24/11/2026*

!!! info "Tình trạng"
    **Đang làm, chưa gửi thầy.** Trang này thay cho trang chính bản 23/11 (bản cũ giữ ở [Lưu trữ](benchmark-ban-23-11.md)). Các ngưỡng trong trang là ngưỡng ban đầu, sẽ được hiệu chỉnh bằng giả lập ở mục 5. Tiến độ các phần khác ở trang [Tiến độ chung](tien-do.md).

**Đọc nhanh:**

- **Khoảng trống:** chưa có thước đo nào, tính **trước khi huấn luyện**, cho biết một bộ dữ liệu có làm lộ hành vi của bộ gộp chống Byzantine hay không, và đã được kiểm chứng là dự báo đúng hành vi đó (mục 1).
- **Vì sao quan trọng:** bộ gộp không phân biệt được *client xấu* với *client lành có dữ liệu khác thường*, nên hoặc loại oan client lành, hoặc bỏ lọt kẻ tấn công (mục 2).
- **Câu hỏi nghiên cứu:** RQ1 điểm chấm có phát hiện đúng loại lỗi và mức lỗi không; RQ2 điểm chấm có dự báo được ảnh hưởng lên bộ gộp không; RQ3 dữ liệu giao thông thật tương đương mức Dirichlet α nào (mục 3).
- **8 tiêu chí** trong 4 nhóm, mỗi tiêu chí ghi rõ trả lời RQ nào và bằng cách nào (mục 4).
- **Giả lập đầu tiên** trên LargeST San Diego: tiêm lỗi có kiểm soát, chốt điểm trước, rồi mới chạy FL (mục 5).

---

## 1. Khoảng trống nghiên cứu

### 1.1. Đã có những gì

Có ba mảng nghiên cứu đã tồn tại riêng lẻ nhưng chưa ai ghép lại:

| Mảng | Đã có ở | Còn thiếu |
|---|---|---|
| **Chấm dữ liệu theo mục đích sử dụng** | Petkani và cs. 2026 (khung chất lượng dữ liệu giao thông, sáu chiều, chấm theo ngưỡng "theo nhiệm vụ"); Miller và cs. 2024 (ISO/IEC 25012 cộng 4 chiều mới); Mohammed và cs. 2024; METRIC 2024 (y tế) | Mục đích trong các bài này là điều khiển giao thông hoặc ML thông thường. **Chưa có khung nào lấy "nghiên cứu Byzantine-FL" làm mục đích** |
| **Đo đặc tính dữ liệu bằng con số** | TFB 2024 (6 chỉ số cho chuỗi thời gian: xu hướng, mùa vụ, trôi…); Fan và cs. 2025 (đo dị biệt bằng energy distance) | Đo trên **dữ liệu**, không đo trên **cập nhật mô hình**, tức thứ bộ gộp thật sự nhìn thấy. Không có tấn công |
| **Nối tính chất dữ liệu với hành vi bộ gộp** | **Malkani 2026** (arXiv 2611.22904); Karimireddy và cs. 2022 (Bucketing); Allouah và cs. 2023 (Fixing by Mixing) | Chỉ đo **sau khi đã huấn luyện** (Malkani chạy 54.214 lần), hoặc chỉ là lý thuyết. Dị biệt là nhân tạo (Dirichlet) hoặc chỉ xét tỉ lệ dữ liệu. Không có dữ liệu giao thông hay V2X |

Các benchmark Byzantine-FL hiện có (Blades, FedSecurity, ByzFL) coi dữ liệu là cho sẵn và chỉ chấm thuật toán, trên dữ liệu ảnh hoặc văn bản chia Dirichlet.

### 1.2. Phát biểu khoảng trống

> Đã có khung đánh giá chất lượng dữ liệu theo mục đích sử dụng, kể cả cho dữ liệu giao thông. Đã có cách đo đặc tính dữ liệu chuỗi thời gian bằng con số. Gần đây đã có bằng chứng rằng tính chất dữ liệu làm đổi kết luận về bộ gộp chống Byzantine. Nhưng **chưa có thước đo nào, tính trước khi huấn luyện, cho biết một bộ dữ liệu có làm lộ được hành vi của bộ gộp chống Byzantine hay không, và đã được kiểm chứng là dự báo đúng hành vi đó.** Vì vậy, người nghiên cứu Byzantine-FL trên dữ liệu giao thông và V2X hiện chọn dữ liệu theo thói quen (Dirichlet, mô phỏng, sin + nhiễu), và không biết kết quả của mình có chuyển được sang dữ liệu thật hay không.

### 1.3. Khác bài gần nhất (Malkani, 17/11/2026) ở đâu

| | Malkani 2026 | Benchmark của nhóm |
|---|---|---|
| Đối tượng được chấm | Bộ gộp | **Bộ dữ liệu** và cách chia client |
| Lúc đo | Sau khi chạy 54.214 lần huấn luyện | **Trước khi huấn luyện**, rồi kiểm chứng bằng một số lần chạy |
| Tính chất dữ liệu được xét | Tỉ lệ dữ liệu mỗi bệnh viện | Thiếu và lỗi, dị biệt, tỉ trọng, độ phân tán cập nhật, lỗi giống tấn công, độ tầm thường, trôi |
| Dữ liệu | Y tế (FLamby), 4–6 client | Giao thông, hàng chục client |

Hai bên cùng kết luận rằng tính chất dữ liệu quyết định việc bộ gộp có loại nhầm client trung thực hay không. Vì vậy bài Malkani là **bằng chứng ủng hộ** sự cần thiết của benchmark, không phải bài trùng. Phân tích chi tiết ở trang [Phân tích Malkani (2026)](nghien-cuu/phan-tich-malkani.md).

### 1.4. Khoảng trống này dựa vào đâu

- **Tra cứu ngày 23/11/2026** bằng tìm kiếm web theo 9 nhóm từ khóa: chất lượng dữ liệu trong FL; benchmark Byzantine-FL với dị biệt tự nhiên; chỉ số đo dị biệt FL; đặc tính dữ liệu chuỗi thời gian; chất lượng dữ liệu cảm biến giao thông; FL cho dự báo giao thông; đánh giá dữ liệu V2X; nghiên cứu thực nghiệm bộ gộp Byzantine dưới dị biệt; khung "fitness for use".
- Đọc toàn văn hoặc tóm tắt các bài gần nhất. Danh sách đầy đủ, mỗi bài trả lời ba câu "có chấm dữ liệu không, có nối với bộ gộp không, có dữ liệu giao thông không", xem trang [Khảo sát công trình liên quan](khao-sat-lien-quan.md).
- **Giới hạn:** đây là kết quả tra nhanh, chưa phải rà soát có hệ thống. Chưa tra Scopus, IEEE Xplore, ACM DL. Một số bài mới đọc tóm tắt. Hướng này đang có người tiếp cận nhanh (bài Malkani ra 6 ngày trước ngày tra), nên cần theo dõi tiếp.

---

## 2. Vì sao khoảng trống này quan trọng

### 2.1. Bộ gộp không phân biệt được client xấu với client có dữ liệu xấu

Các bộ gộp chống Byzantine (Krum, Median, Trimmed Mean, FLTrust…) không nhìn thấy dữ liệu, chỉ nhìn thấy **cập nhật** mà client gửi lên. Chúng đều dựa trên một giả định: **client trung thực gửi cập nhật giống nhau, ai khác hẳn thì đáng ngờ**. Trên dữ liệu giao thông thật, giả định này dễ vỡ, dẫn tới hai lỗi ngược nhau:

- **Loại oan.** Client lành nhưng khác thường bị coi là kẻ tấn công. Ở LargeST San Diego, tuyến I15 hướng Bắc trung bình 414 xe mỗi 15 phút, còn SR11 hướng Đông chỉ 23 xe, chênh 18 lần. Cả hai đều trung thực, nhưng bộ gộp có thể loại SR11. Client có cảm biến kẹt hoặc mất dữ liệu cũng gửi cập nhật lệch, và cũng dễ bị loại. Hậu quả là mô hình chung mất đúng phần dữ liệu khó và hiếm.
- **Bỏ lọt.** Khi các client lành vốn đã tản ra, kẻ tấn công khéo léo (kiểu ALIE, IPM) chỉ cần nằm trong độ tản đó là không bị phát hiện.

Hiện ta không biết trước một bộ dữ liệu sẽ gây ra lỗi nào và ở mức nào.

### 2.2. Bằng chứng là dữ liệu làm đổi kết luận

- **Cùng một bộ gộp, kết quả trái ngược nhau giữa các bài.** Median gần như không bị ảnh hưởng trên HuddsTrafficFL (KBS 2026), nhưng thất bại trên dữ liệu viễn thông Milan (Zhang 2024) và dữ liệu Open-RAN chia theo trạm. Giả thuyết của nhóm là khác biệt này đến từ **dữ liệu**, cụ thể là cách dữ liệu chia cho các client, chứ không chỉ do thuật toán.
- **Malkani 2026:** bộ gộp không trọng số luôn giảm trọng số của client có cập nhật khác thường nhất. Một client giữ quá nửa dữ liệu thì thành "độc tài" của mô hình chung.
- **Karimireddy và cs. 2022:** Krum, Median thất bại khi dữ liệu non-IID ngay cả khi **không có tấn công**.

### 2.3. Hệ quả cho người nghiên cứu và người dùng thực tế

- **Kết luận không chuyển được sang dữ liệu thật.** Dữ liệu sin + nhiễu đang dùng trong code ByzCity không có lỗi nào, nhưng chỉ cần biết giờ trong ngày đã đoán đúng 98 % phương sai. Trên dữ liệu đó, bộ gộp nào cũng trông tốt, nên kết luận "Median chống được mọi tấn công" không có ý nghĩa.
- **Đo sau khi huấn luyện thì quá đắt.** Malkani cần 54.214 lần chạy để thấy hiện tượng. Một thước đo tính trước huấn luyện, chỉ bằng numpy/pandas, cho biết sớm và rẻ dữ liệu có làm lộ hành vi bộ gộp không.
- **Dùng được trong thực tế.** Benchmark được định vị là **một sản phẩm độc lập**, đồng thời là **công cụ dùng được khi triển khai**: trước khi đưa một hệ thống FL chống Byzantine vào một mạng cảm biến giao thông, đơn vị triển khai chấm dữ liệu của mình để biết bộ gộp có nguy cơ loại oan hay bỏ lọt ở đâu.

---

## 3. Câu hỏi nghiên cứu

Câu hỏi chung: **các chỉ số đo trên dữ liệu, trước khi huấn luyện, có cho biết đúng tình trạng của dữ liệu và dự báo được hành vi của bộ gộp chống Byzantine không?** Câu hỏi này tách thành:

| RQ | Câu hỏi | Trả lời "có" khi |
|---|---|---|
| **RQ1** | Điểm chấm của từng tiêu chí có **phát hiện đúng loại lỗi và mức lỗi** trong dữ liệu không? | Tiêm một loại lỗi đã biết ở nhiều mức: tiêu chí tương ứng đổi điểm đúng chiều, tăng giảm theo mức lỗi, còn các tiêu chí không liên quan gần như không đổi |
| **RQ2** | Điểm chấm trước huấn luyện có **dự báo được ảnh hưởng lên bộ gộp** không, gồm tỉ lệ loại oan client lành (FPR), chi phí độ bền và điểm gãy? | Tương quan Spearman giữa tiêu chí và hành vi bộ gộp đạt \|ρ\| ≥ 0,6 |
| **RQ3** | Dữ liệu giao thông thật (LargeST chia theo tuyến) **tương đương với mức Dirichlet α nào** mà các bài Byzantine-FL hay dùng? | Tìm được khoảng α cho điểm F2, B1 và FPR gần với chia theo tuyến |

**Giải thích RQ3.** Các bài Byzantine-FL thường chia dữ liệu theo phân phối Dirichlet với tham số α: α nhỏ thì các client rất khác nhau, α lớn thì gần giống nhau. Chưa ai biết dữ liệu giao thông thật ứng với α bằng bao nhiêu. Nếu đo ra, ví dụ "LargeST chia theo tuyến tương đương α khoảng 0,3", người khác đọc lại được kết quả trên Dirichlet của họ và biết kết quả đó có còn đúng với giao thông thật không. RQ3 dùng chung lần chạy với RQ2, không cần chạy thêm.

**Hướng làm tiếp (chưa làm ở giả lập đầu tiên):** dữ liệu có hồ sơ điểm thế nào thì nên dùng bộ gộp nào. Câu này cần nhiều bộ dữ liệu hơn mới kết luận được.

---

## 4. Các tiêu chí và cách mỗi tiêu chí trả lời câu hỏi nghiên cứu

Mỗi tiêu chí chấm 0–3 điểm. Tất cả tính được chỉ bằng numpy/pandas qua script `cham_du_lieu.py`, **không cần huấn luyện FL**. Các ngưỡng 3 điểm là ngưỡng ban đầu.

### 4.1. Bảng tiêu chí

| Nhóm | Mã | Tiêu chí | Đo gì | Cách tính | Ngưỡng 3 điểm |
|---|---|---|---|---|---|
| **T. Nền tảng dữ liệu** | T2 | Độ đầy đủ | Dữ liệu bị thiếu | % ô NaN, cảm biến "chết", chuỗi giá trị 0 kéo dài ≥ 3 giờ | Thiếu ≤ 1 % |
| | T3 | Tính hợp lệ | Giá trị bất thường | % ô bị kẹt ≥ 6 giờ, % ô chạm trần (ví dụ 999) | Lỗi ≤ 1 % |
| **F. Mức phù hợp với FL** | F2 | Mức dị biệt tự nhiên | Các client khác nhau về phân phối đến mức nào khi chia theo thực tế (ví dụ theo tuyến) | Trung vị EMD giữa từng cặp client, chia cho cùng đại lượng khi chia ngẫu nhiên (giữ số mẫu mỗi client). Chia ngẫu nhiên ứng với 1 | ≥ 3 |
| | F3 | Tỉ trọng client | Có client nào áp đảo về số mẫu không | Hệ số Gini của số mẫu; tỉ trọng client lớn nhất | Gini 0,2–0,5 và không client nào > 50 % |
| **B. Đặc thù Byzantine** | B1 | HDR (độ phân tán cập nhật trung thực) | Gradient của các client lành tản ra đến mức nào | Mô hình tham chiếu ridge AR-12 huấn luyện tập trung; tính gradient MSE của từng client tại mô hình đó; lấy độ phân tán; chia cho cùng đại lượng khi chia ngẫu nhiên | ≥ 2 |
| | B3 | Lỗi tự nhiên giống tấn công | Có sẵn client "lành nhưng trông như độc" không | % client có cảm biến kẹt, chạm trần hoặc mất dữ liệu dài | 10–40 % |
| **K. Bài toán** | K2 | Độ tầm thường | Bài toán có quá dễ không | Dự báo: R² khi chỉ dùng hồ sơ trung bình theo giờ trong ngày | R² ≤ 0,70 |
| | K3 | Trôi phân phối | Dữ liệu thay đổi theo thời gian | EMD giữa nửa đầu và nửa sau chuỗi, chia cho EMD giữa quý 1 và quý 2 | ≥ 2 |

> **Đã bỏ F4** (lợi ích của FL so với huấn luyện cục bộ), vì F4 cần chạy FL thật, không còn là "đo trước khi huấn luyện". F4 được dùng làm **biến kết quả**, không làm tiêu chí.

**Số đã đo được đến nay:** LargeST SD chia theo tuyến có F2 = 3,81, dữ liệu sin + nhiễu có F2 = 0,92. Trên tập kiểm tra tổng hợp, chia theo tuyến cho HDR = 2,64, chia ngẫu nhiên cho 0,83. Dữ liệu sin + nhiễu có K2 = 0,98. Các số còn lại sẽ đo ở bước 0 của mục 5.

### 4.2. Mỗi tiêu chí trả lời câu hỏi nghiên cứu như thế nào

**RQ1** được trả lời bằng cách **tiêm lỗi có kiểm soát**: mỗi tiêu chí có một "núm vặn" làm thay đổi đúng thứ nó đo, ở nhiều mức biết trước. **RQ2** được trả lời bằng cách so điểm của tiêu chí với hành vi bộ gộp đo được khi chạy FL.

| Mã | Vì sao liên quan tới bộ gộp | Trả lời RQ1: núm vặn và kết quả phải thấy | Trả lời RQ2: kỳ vọng với bộ gộp |
|---|---|---|---|
| **T2** | Client có nhiều ô thiếu gửi cập nhật lệch khỏi số đông, dễ bị coi là kẻ tấn công | Xóa ngẫu nhiên 0, 1, 5, 10, 20 % ô (cả xóa rải rác và xóa thành đoạn dài). T2 phải giảm theo mức xóa; T3, F2 gần như không đổi | Thiếu nhiều ở một số client thì FPR tăng. Đo T2 để tách FPR do lỗi dữ liệu khỏi FPR do khác biệt thật giữa client |
| **T3** | Như T2: cảm biến kẹt hoặc chạm trần làm cập nhật lệch | Cho một số cảm biến đứng yên ≥ 6 giờ, hoặc chạm trần 999, ở nhiều mức. T3 phải bắt được; T2 không đổi | Như T2 |
| **F2** | Bộ gộp dựa trên khoảng cách hay trung vị ngầm giả định client lành giống nhau. F2 càng cao thì client lành càng khác nhau, càng dễ bị loại nhầm | Trộn dần từ chia theo tuyến sang chia ngẫu nhiên (hệ số trộn 0; 0,25; 0,5; 0,75; 1). F2 phải giảm từ khoảng 3,8 về khoảng 1 | **Ứng viên chính dự báo FPR** của Krum và Median: kỳ vọng tương quan dương. Cũng là trục chính của RQ3 |
| **F3** | Client có hơn 50 % dữ liệu gần như quyết định mô hình chung ("độc tài", Malkani 2026). Krum cần n ≥ 2f + 3 client | Gộp dần các client nhỏ vào một client để tỉ trọng client lớn nhất lên 30, 50, 70 %. Gini và tỉ trọng lớn nhất phải tăng tương ứng | Tỉ trọng > 50 % thì bộ gộp không trọng số sai lệch rõ hơn so với FedAvg có trọng số |
| **B1** | Bộ gộp chỉ thấy cập nhật. B1 đo đúng thứ bộ gộp thấy nhưng vẫn tính được trước khi chạy FL | Cùng phép trộn như F2. HDR phải đi từ mức chia theo tuyến về khoảng 1 | HDR cao thì FPR cao và tấn công ALIE/IPM dễ lọt hơn. Cũng là trục của RQ3 |
| **B3** | "Bài thi khó": bộ gộp phải phân biệt được lỗi thật với tấn công. B3 = 0 thì benchmark quá dễ, B3 quá cao thì dữ liệu quá bẩn | Đặt lỗi T2/T3 vào 0, 10, 20, 40 % số client. B3 phải đọc ra đúng tỉ lệ đó | B3 tăng thì FPR tăng, và đo được bộ gộp nào phân biệt lỗi tự nhiên với tấn công tốt hơn |
| **K2** | Nếu chỉ lịch theo giờ đã dự báo đúng, mọi bộ gộp đều trông tốt, kết luận không có ý nghĩa | Thay dần dữ liệu bằng hồ sơ trung bình theo giờ cộng nhiễu. K2 phải tăng lên gần 1 | K2 cao thì khoảng cách giữa các bộ gộp co lại, ma trận tấn công × phòng thủ mất khả năng phân biệt |
| **K3** | Khi dữ liệu trôi, cập nhật lành đổi theo từng vòng. Bộ gộp dùng lịch sử (FLTrust, tham chiếu từ vòng trước) dễ bị đánh lừa | Chọn cửa sổ thời gian có và không có đợt trôi đã biết (COVID 2020). K3 phải khác rõ giữa hai cửa sổ | K3 cao thì FLTrust sai nhiều hơn các bộ gộp không dùng lịch sử |

---

## 5. Kế hoạch giả lập đầu tiên

Mục tiêu: kiểm tra tiêu chí **thật sự** phát hiện đúng lỗi (RQ1) và dự báo được hành vi bộ gộp (RQ2, RQ3), không chỉ "nghe hợp lý".

### 5.1. Dữ liệu

- **LargeST San Diego** làm bộ chính, đọc từ **file HDF5 gốc** (bản đã điền số 0 che mất chỗ thiếu dữ liệu). Client chia theo tuyến đường.
- **Làm LargeST trước.** VeReMi (hướng V2X) để giai đoạn sau, khi bộ tiêu chí đã được kiểm chứng trên dữ liệu dự báo.
- Dữ liệu sin + nhiễu chỉ dùng để kiểm tra code chạy đúng, không dùng để kết luận.

### 5.2. Các bước

| Bước | Làm gì | Trả lời | Đầu ra |
|---|---|---|---|
| **0. Chấm mốc** | Chấm LargeST SD chia theo tuyến và chia ngẫu nhiên bằng `cham_du_lieu.py`. Lặp với 5 seed để xem điểm có ổn định không | Chuẩn bị | Bảng điểm mốc 8 tiêu chí. Tiêu chí nào dao động > 15 % giữa các seed thì đánh dấu không ổn định |
| **1. Tiêm lỗi có kiểm soát** | Với mỗi tiêu chí, vặn núm như bảng mục 4.2, 4–5 mức, 5 seed. Chấm lại sau mỗi lần tiêm | RQ1 | Bảng "tiêu chí × mức tiêm". Đạt khi điểm đổi đơn điệu theo mức tiêm (Spearman ≥ 0,9) và tiêu chí không liên quan đổi < 15 % |
| **2. Chốt trước** | Ghi lại điểm và ngưỡng của mọi biến thể dữ liệu **trước khi** xem kết quả FL, để không chỉnh ngưỡng cho khớp kết quả | Giữ tính khách quan | File điểm đã chốt, có ngày và mã băm |
| **3. Chạy FL** | Trên các biến thể dữ liệu của bước 1 (khoảng 15 điểm dữ liệu), thêm các cách chia Dirichlet α ∈ {0,1; 0,3; 1; 10}. Bộ gộp: FedAvg, Krum, Median, Trimmed Mean, FLTrust. Hai điều kiện: sạch, và tấn công ALIE/IPM với 20 % client độc. Quét tỉ lệ client độc từ 10 % đến 40 % để tìm điểm gãy. 5 seed | RQ2, RQ3 | Mỗi lần chạy ghi: **FPR** (% lượt client lành bị loại), **chi phí độ bền** (MAE với bộ gộp trừ MAE với FedAvg, điều kiện sạch), **điểm gãy**, và F4 |
| **4. Kiểm định** | Tính Spearman giữa từng tiêu chí và FPR, chi phí độ bền, điểm gãy. So điểm F2, B1 và FPR của chia theo tuyến với các mức Dirichlet | RQ2, RQ3 | Bảng "tiêu chí × bộ gộp" với ρ. Tiêu chí có \|ρ\| ≥ 0,6 thì giữ, dưới 0,6 thì chỉ để mô tả. Đồ thị F2/B1 theo FPR. Khoảng α tương đương với chia theo tuyến |

### 5.3. Việc cần chuẩn bị trong code

- Script tiêm lỗi theo từng tiêu chí (xóa ô, làm kẹt, chạm trần, trộn cách chia, gộp client, thay bằng hồ sơ theo giờ, chọn cửa sổ thời gian).
- `chay.py` ghi lại client được chọn hoặc bị loại ở mỗi vòng (hiện chưa ghi), để tính FPR.
- Thêm cách chia Dirichlet α cho LargeST trong `du_lieu.py`.

### 5.4. Kết quả mong đợi

- **RQ1:** mỗi tiêu chí phản ứng đúng với lỗi của nó và ít phản ứng với lỗi khác.
- **RQ2:** F2 và B1 tương quan dương với FPR của Krum và Median. K2 cao thì mọi bộ gộp đều đạt kết quả tốt (benchmark quá dễ).
- **RQ3:** tìm được khoảng α mà Dirichlet cho F2, B1 và FPR gần với chia theo tuyến.
- **Nếu kết quả không ra như vậy, đó vẫn là phát hiện có giá trị:** nghĩa là các thước đo dữ liệu quen thuộc **không** đủ để dự báo hành vi bộ gộp, phải đo trực tiếp trên cập nhật mô hình. Kết quả âm tính cũng được báo cáo.

---

## 6. Câu hỏi xin ý kiến thầy

1. **Cơ sở chọn ngưỡng:** nên dùng ngưỡng theo chuẩn chất lượng dữ liệu (ví dụ ISO/IEC 25012, các nghiên cứu về chất lượng dữ liệu giao thông), hay để giả lập hiệu chỉnh hoàn toàn (mục 5)?
2. **Tiêu chí kiểm chứng:** ngưỡng \|ρ\| ≥ 0,6 trên khoảng 15 điểm dữ liệu có đủ thuyết phục không, hay cần thêm bộ dữ liệu?

??? note "Tài liệu tham khảo"
    - Malkani A. *Who Pays for Byzantine Robustness? Validity, Data-Share Dictatorships, and Fairness When Only a Few Hospitals Collaborate*. arXiv:2611.22904, 2026.
    - Karimireddy S. P., He L., Jaggi M. *Byzantine-Robust Learning on Heterogeneous Datasets via Bucketing*. ICLR 2022.
    - Allouah Y. và cs. *Fixing by Mixing: A Recipe for Optimal Byzantine ML under Heterogeneity*. arXiv:2302.01772, 2023.
    - Petkani và cs. *Data Quality in Traffic Management: Framework and Real-World Impacts*. Future Transportation 6(3):124, 2026.
    - Miller và cs. *A Framework for Current and New Data Quality Dimensions: An Overview*. Data 9(12):151, 2024.
    - Mohammed và cs. *Data Quality Assessment: Challenges and Opportunities*. arXiv:2403.00526, 2024.
    - Schwabe và cs. *The METRIC-framework for assessing data quality for trustworthy AI in medicine*. arXiv:2402.13635, 2024.
    - Qiu X. và cs. *TFB: Towards Comprehensive and Fair Benchmarking of Time Series Forecasting Methods*. PVLDB 2024. arXiv:2403.20150.
    - Fan và cs. *Measuring Heterogeneity in Machine Learning with Distributed Energy Distance*. arXiv:2501.16174, 2025.
    - Li S. và cs. *Blades: A Unified Benchmark Suite for Byzantine Attacks and Defenses in Federated Learning*. arXiv:2206.05359.
    - Liu X. và cs. *LargeST: A Benchmark Dataset for Large-Scale Traffic Forecasting*. NeurIPS 2023. arXiv:2306.08259.
    - Wu R., Keogh E. *Current Time Series Anomaly Detection Benchmarks are Flawed and are Creating the Illusion of Progress*. IEEE TKDE, 2021.
