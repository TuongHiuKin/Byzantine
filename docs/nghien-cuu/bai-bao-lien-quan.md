# Bài báo liên quan — LargeST và GAP-1

> **114 bài trích dẫn LargeST: 1 bài có học liên kết, 0 bài có Byzantine. Khảo sát mới nhất 10/11/2026.**
>
> Tác giả: Nguyễn Quang Huy — SE194177 · GVHD: ThS. Lâm Hữu Khánh Phương · Đại học FPT · 10/11/2026

**Câu hỏi:** dựa trên dữ liệu LargeST và nhánh GAP-1 đang benchmark, có những bài nào đang dùng và đã đánh giá vấn đề này, gần đây nhất?

**Ngày tra:** 10/11/2026 · **Nguồn:** OpenAlex API + Crossref metadata · **Số liệu:** log phân tích cục bộ

---

## 0. Kết quả trước

**114 bài trích dẫn LargeST. Trong đó 1 bài có học liên kết, 0 bài có Byzantine.**

Đây không phải "chưa tìm thấy" — đây là đếm trên toàn bộ tập trích dẫn, có abstract để kiểm. Con số này xác nhận GAP-1 mạnh hơn mọi lập luận trước đó trong đề cương, và theo cách khó phản bác hơn: không phải tôi tìm không ra, mà là **tập trích dẫn của chính LargeST không có**.

Ba nhóm bài dưới đây, xếp theo mức liên quan đến hai trục FL × Byzantine.

---

## 1. Tập trích dẫn LargeST — số đo

LargeST (Liu và cộng sự, NeurIPS 2023) — OpenAlex `W7133245391`, **116 trích dẫn**, lấy được **114 bản ghi**.

| Năm | Số bài trích dẫn |
|---|---:|
| 2024 | 29 |
| 2025 | 21 |
| **2026** | **64** |

64/114 = **56 %** trích dẫn đến trong năm 2026. Đây là benchmark đang được dùng nhiều lên, không phải cũ.

### 1.1 Lọc theo hai trục

Đếm trên title + abstract của cả 114 bài (90 bài có abstract):

| Trục | Số bài | Tỉ lệ |
|---|---:|---:|
| Có chữ "federated" | **1** | 0,9 % |
| Có "byzantine" / "poison" / "malicious" | **0** | 0 % |
| Có cả hai | **0** | 0 % |

**Bài duy nhất có FL:** CRAFT — Cross-Region Adaptive Federated Transfer Learning for Urban Spatiotemporal Prediction (CIKM 2026, Dai và cộng sự, `10.1145/3799682.3840571`).

Đọc toàn văn abstract của CRAFT: nó dùng **federated transfer learning** giữa các thành phố, có LLM + mixture-of-experts, và **không** có Byzantine, không có poison, không có attack, không có non-IID theo nghĩa đối kháng. Chữ "robustness" trong abstract nói về *negative transfer*, không phải đối thủ.

**Hệ quả cho GAP-1:** ngay cả bài FL duy nhất trích dẫn LargeST cũng không chạm trục Byzantine. Tập trích dẫn của LargeST **hoàn toàn trống** ở trục này.

### 1.2 Điều này nói gì về khoảng trống

Phát biểu cũ của đề cương: *"chưa ai làm Byzantine-FL cho giao thông trên dữ liệu thật"* — **sai**, Vehicular AttestedFL (VTC 2024) đã làm.

Phát biểu mới, đo được: *"trong 114 công trình dùng chính bộ dữ liệu này, không công trình nào đánh giá Byzantine"*. Đây là phát biểu **hẹp hơn nhưng không phản bác được bằng một phản ví dụ** — vì phạm vi đã nêu rõ là tập trích dẫn của LargeST.

Đây là dạng khoảng trống mạnh nhất: không cần chứng minh "không ai trên đời", chỉ cần chứng minh "không ai trong tập này" — và tập này là tập mà bất kỳ ai làm LargeST cũng phải đọc.

---

## 2. Nhóm A — Dùng LargeST, không có FL (đa số)

Nhóm này là **baseline so sánh trực tiếp** cho phần dự báo của GAP-1. Không bài nào có Byzantine, nhưng chúng định nghĩa "kết quả tốt trên LargeST là bao nhiêu".

Các hướng chính trong 114 bài:

| Hướng | Số bài | Ví dụ tiêu biểu |
|---|---:|---|
| Kiến trúc không gian–thời gian | nhiều nhất | Transformer không gian, GNN hiệu quả cao |
| Khả mở rộng (scalability) | 7 | Xử lý 8.600 cảm biến |
| Benchmark / đánh giá | 9 | So sánh mô hình trên cùng split |
| Dự báo giao thông ứng dụng | 4 | Ùn tắc, luồng xe |

**Bài đáng chú ý:** "Efficient Large-Scale Traffic Forecasting with Transformers: A Spatial..." (2025, **72 trích dẫn**) — bài có ảnh hưởng nhất trong tập, và nó cũng **không** có Byzantine. Đây là đối thủ trực tiếp về mặt "dùng LargeST hiệu quả", không phải đối thủ về mặt an toàn.

---

## 3. Nhóm B — Tấn công vào dự báo giao thông, KHÔNG dùng FL

Nhóm này quan trọng vì nó là **nền lý thuyết cho tấn công mức dữ liệu cảm biến** — đóng góp mới của GAP-1.

| Bài | Năm | Trích dẫn | Vì sao liên quan |
|---|---|---:|---|
| Practical Adversarial Attacks on Spatiotemporal Traffic Forecasting Models | 2022 | 22 | Tấn công trực tiếp vào mô hình dự báo giao thông — nền cho trục RQ3 |
| Robust Spatiotemporal Traffic Forecasting with Reinforced Dynamic Adversarial Training | 2023 | 20 | Phòng thủ đối kháng **không dùng FL** — chứng minh hướng này đã có người làm, nhưng tập trung |
| Spatially Focused Attack against Spatiotemporal Graph Neural Networks | 2021 | 6 | Tấn công có mục tiêu theo không gian — tương ứng tấn công "giờ cao điểm" của GAP-1 |
| One Vertex Attack on GNN-based Spatiotemporal Forecasting | 2021 | 2 | Tấn công một nút — tương ứng tấn công mức cảm biến |
| Reinforcement Learning-Based Node-Wise Adversarial Attacks Against Spatiotemporal Traffic Forecasting | 2026 | 0 | **Mới nhất**, tấn công từng nút — gần nhất với RQ3 của GAP-1 |

**Điểm cốt lõi:** tất cả năm bài này tấn công mô hình **tập trung**. Không bài nào đặt tấn công trong bối cảnh client phân tán. Đây chính là khe giữa nhóm B và nhóm C.

---

## 4. Nhóm C — FL + Byzantine, KHÔNG dùng giao thông

Nhóm này là **nền phương pháp** — nơi lấy Krum, Median, Trimmed Mean, và nơi lấy thang đo.

| Bài | Năm | Trích dẫn | Vai trò |
|---|---|---:|---|
| FLDetector: Defending FL Against Model Poisoning via Detecting Malicious Clients | 2022 | 389 | Phát hiện client độc hại — tương ứng FPR/FNR của GAP-1 |
| ShieldFL: Mitigating Model Poisoning in Privacy-Preserving FL | 2022 | 387 | Phòng thủ + riêng tư cùng lúc |
| zPROBE: Zero Peek Robustness Checks for FL | 2023 | 26 | **Kiểm tra độ bền** — gần với tinh thần benchmark |
| ROBY: A Byzantine-Robust and Privacy-Preserving Serverless FL Framework | 2025 | 24 | Mới nhất, không server |
| AgrEvader: Poisoning Membership Inference against Byzantine-robust FL | 2023 | 29 | Tấn công **vào chính bộ gộp Byzantine** — bằng chứng phòng thủ có lỗ |
| A comprehensive analysis of model poisoning attacks in FL for autonomous vehicles | 2024 | 21 | Gần giao thông nhất trong nhóm này, nhưng là **xe tự lái**, không phải lưu lượng đường |

**Điểm cốt lõi:** nhóm này rất mạnh về phương pháp (hàng trăm trích dẫn) nhưng **không bài nào dùng dữ liệu giao thông đường bộ**. Đây là nửa còn lại của khe.

---

## 5. Nhóm D — Giao nhau: gần nhất với GAP-1

Đây là danh sách ngắn thật sự. Chỉ những bài chạm **cả hai** trục:

| Bài | Năm | Venue | Trục | Thiếu gì |
|---|---|---|---:|---|
| **HuddsTrafficFL** | 2026 | Knowledge-Based Systems | FL + Byzantine + giao thông | **Dữ liệu SUMO mô phỏng**, không phải PeMS thật |
| **Vehicular AttestedFL** | 2024 | IEEE VTC | FL + Byzantine + dữ liệu thật | Toronto Downtown, **không phải benchmark**, không phát hành phân vùng client |
| **Poisoning Attacks on FL-based Wireless Traffic Prediction** | 2024 | IFIP Networking | FL + poison + "traffic" | Là lưu lượng **mạng di động**, không phải giao thông đường bộ |
| **CRAFT** | 2026 | CIKM | FL + LargeST | **Không có Byzantine, không có tấn công** |
| **F2C-Net** | 2026 | Computer Networks | FL + traffic + privacy | Transformer-RL cho điều khiển, không có đối thủ |
| **Physics-Attested FL** | 2026 | Information (MDPI) | FL + poison + dữ liệu cảm biến thật | **Nước**, không phải giao thông — nhưng phương pháp chuyển được |

**Đọc bảng này theo chiều dọc:** mỗi bài đáp ứng 2–3 ô, không bài nào đáp ứng cả 4 (dữ liệu giao thông thật + FL + Byzantine + cấu trúc benchmark). Đó chính là GAP-1.

### 5.1 Bài mới nhất đáng chú ý: Physics-Attested FL

`10.3390/info17111101`, 04/11/2026 — **mới hơn GAP-1 sáu ngày**.

Abstract nói nguyên văn: *"existing defences operate strictly in update space, leaving aggregators blind to data poisoning; model updates derived from fabricated telemetry remain indistinguishable from honest contributions."*

Đây **chính xác là luận điểm của RQ3** trong GAP-1 — rằng phòng thủ hiện tại chỉ nhìn cập nhật mô hình, không nhìn dữ liệu, nên tấn công ở mức cảm biến đi qua. Bài này làm trên **hạ tầng nước**, dùng "process invariants" (bất biến vật lý) làm attestation.

**Vì sao quan trọng:** đây vừa là **xác nhận** vừa là **cảnh báo**.
- Xác nhận: luận điểm RQ3 là đúng và đang được cộng đồng nhận ra.
- Cảnh báo: nếu ai đó áp dụng cùng ý tưởng cho giao thông trước, GAP-1 mất phần RQ3. Cần đọc bài này và trích dẫn nó như **bằng chứng khoảng trống đang bị lấp từ phía khác miền** — đó là lập luận mạnh, không phải điểm yếu.

---

## 6. Đánh giá chung: vấn đề này đang ở đâu

### 6.1 Ba cộng đồng, ba ngôn ngữ, gần như không nói chuyện với nhau

| Cộng đồng | Quan tâm | Dùng LargeST? | Có Byzantine? |
|---|---|---|---|
| Dự báo giao thông | độ chính xác, khả mở rộng | **có** (114 bài) | **không** |
| FL an toàn | tấn công, phòng thủ, phát hiện | **không** | **có** (mạnh) |
| Giao thông + an toàn | cả hai | rất ít | rất ít |

Đây không phải suy đoán — đó là hệ quả trực tiếp của hai con số 1/114 và 0/114.

### 6.2 Xu hướng 2026

64/114 trích dẫn đến trong 2026, tức tốc độ tăng gần gấp ba so với 2025. Nhưng trong 64 bài đó:
- **0 bài** có Byzantine
- **1 bài** (CRAFT) có FL, và không có đối thủ

Nghĩa là **làn sóng dùng LargeST đang tăng nhanh mà trục an toàn vẫn trống**. Khoảng trống không bị lấp bởi thời gian — nó đang rộng ra.

### 6.3 Áp lực thời gian thật

Hai bài 2026 cho thấy hướng đang dịch:
- **Physics-Attested FL** (11/2026): tấn công dữ liệu vượt phòng thủ mức cập nhật — đúng RQ3, khác miền
- **Reinforcement Learning-Based Node-Wise Adversarial Attacks** (2026): tấn công từng nút trên mô hình tập trung — đúng công cụ RQ3, khác bối cảnh

Nếu một nhóm ghép hai ý này lại cho giao thông + FL, GAP-1 mất phần lớn tính mới. **Đây là lý do nên nộp sớm thay vì mở rộng phạm vi.**

---

## 7. Danh sách nên đọc, theo thứ tự

| # | Bài | Vì sao đọc trước |
|---|---|---|
| 1 | **Physics-Attested FL** (Information, 11/2026) | Mới nhất, đúng luận điểm RQ3, phải biết để định vị |
| 2 | **CRAFT** (CIKM 2026) | Bài FL duy nhất dùng LargeST — đối thủ trực tiếp về "dùng LargeST + FL" |
| 3 | **Reinforcement Learning Node-Wise Attacks** (2026) | Công cụ tấn công nút mới nhất |
| 4 | **zPROBE** (ICCV 2023) | Cách kiểm tra độ bền có hệ thống — mẫu cho thiết kế benchmark |
| 5 | **AgrEvader** (WWW 2023) | Chứng minh bộ gộp Byzantine có lỗ — nền cho RQ1 |
| 6 | **Practical Adversarial Attacks on Spatiotemporal Traffic** (2022) | Nền cho tấn công mức dữ liệu trên mô hình giao thông |
| 7 | **Efficient Large-Scale Traffic Forecasting with Transformers** (2025) | Baseline mạnh nhất trên LargeST, 72 trích dẫn |

---

## 8. Giới hạn của khảo sát này

| Hạn chế | Ảnh hưởng |
|---|---|
| Chỉ dùng OpenAlex | Scopus và IEEE Xplore có thể có thêm; chưa tra |
| 24/114 bài không có abstract | Đếm theo abstract là **cận dưới**; nhưng 0 bài có "byzantine" trong **title** nên khó có bài bị bỏ sót |
| Lọc bằng từ khoá | Bài dùng khái niệm Byzantine mà không dùng chữ (ví dụ "robust aggregation" không nêu tên) có thể bị bỏ |
| Chưa đọc toàn văn | Trừ HuddsTrafficFL, CRAFT, Physics-Attested FL — ba bài đã đọc abstract kỹ |

**Con số 1/114 và 0/114 nên được phát biểu kèm giới hạn này**, không phải như một khẳng định tuyệt đối. Đúng dạng: *"trong 114 bản ghi OpenAlex trích dẫn LargeST, đếm theo title và abstract, 1 bài có FL và 0 bài có Byzantine"*.

---

## Phụ lục — dữ liệu thô

| Tệp | Nội dung |
|---|---|
| log phân tích cục bộ | 114 bài, đếm theo trục, danh sách bài FL |
| OpenAlex `W7133245391` | LargeST, 116 trích dẫn |
| `10.1145/3799682.3840571` | CRAFT, CIKM 2026 |
| `10.3390/info17111101` | Physics-Attested FL, 04/11/2026 |
| `10.1016/j.knosys.2026.117003` | HuddsTrafficFL, KBS 2026 |
