# Malkani (2026) "Who Pays for Byzantine Robustness?" — phân tích và đối chiếu

*Phân tích tổng hợp phục vụ nghiên cứu benchmark đánh giá dữ liệu · 23/11/2026*

!!! info "Vì sao có trang này"
    Trang [Khảo sát công trình liên quan](../khao-sat-lien-quan.md) xếp bài Malkani vào nhóm **"cần đọc kỹ"** nhưng mới dừng ở mức một dòng mô tả. Đây là bản đọc toàn văn: ba câu hỏi nghiên cứu, bộ tiêu chí, kết quả định lượng, và những chỗ nó đụng trực tiếp vào hai nhánh công việc của nhóm.

---

## 0. Kết luận trong một khối

**Đây là bài gần nhất với hướng của nhóm, và nó là bài tốt nhất trong nhóm đó.** Nhưng nó làm một việc *khác* việc nhóm định làm, và sự khác nhau đó là chỗ đứng của nhóm.

Bài làm **audit bộ gộp sau khi chạy** (54.214 lần huấn luyện). Nhóm định làm **thước đo dữ liệu trước khi chạy**. Hai loại đóng góp khác nhau.

Ba điều bài này đóng góp mà nhóm nên kế thừa ngay:

| # | Đóng góp | Vì sao quan trọng với nhóm |
|---|---|---|
| 1 | **Kiểm tra hợp lệ theo tỉ lệ dữ liệu** — client giữ > 50 % trọng số làm weighted median/GeoMed thành "độc tài" | Bổ sung tầng kiểm tra mà `n ≥ 2f + 3` bỏ lọt |
| 2 | **Đối chứng exact-twin leave-out** tách "mất dữ liệu" khỏi "thiệt hại tấn công" | Phần lớn cái gọi là "phòng thủ gãy" thật ra là **97 % mất dữ liệu** |
| 3 | **Báo cáo metric theo từng client** chứ không chỉ trung bình gộp | Trung bình che giấu tấn công tàng hình hoàn toàn |

Và một điều bài này **không** làm, là chỗ nhóm còn đứng được:

> Bài đo cái giá **sau** 54.214 lần chạy. Nó không kiểm tra liệu cái giá đó có **dự báo được từ dữ liệu trước khi huấn luyện** hay không. Đó là câu hỏi của nhóm.

---

## 1. Mục tiêu nghiên cứu — ba câu hỏi của bài

Bài đặt vấn đề bằng một nghịch lý đo lường: tài liệu Byzantine-FL được xây trên quy mô **không tồn tại trong thực tế**.

> *"Clinical federated learning (FL) collaborations typically connect only three to six hospitals, yet Byzantine-robust aggregation rules are designed and benchmarked on synthetic partitions across dozens of equal-sized clients."*

Dẫn chứng từ chính FLamby: trong 7 bộ dữ liệu y tế thật, **mỗi liên đoàn chỉ có 2–6 cơ sở**. Hai hệ quả trở thành tiền đề:

**(a) Quy tắc chọn theo khoảng cách cần đủ hàng xóm trung thực.** Krum cần `n ≥ 2f + 3`, Bulyan cần `n ≥ 4f + 3`. Với n = 4 và f = 1, Krum không hợp lệ; Bulyan không xác định về toán học ở mọi mạng 4 và 6 bệnh viện khi f ≥ 1.

**(b) Cỡ dữ liệu chênh nhau hàng bậc.** Trong Fed-ISIC2019, một trung tâm giữ **53,4 %** ảnh huấn luyện, trung tâm nhỏ nhất giữ **1,9 %**. Khi quy tắc gộp có trọng số theo cỡ mẫu, điểm gãy dịch từ số client sang tỉ lệ dữ liệu.

Ba câu hỏi nghiên cứu, nguyên văn:

| Mã | Câu hỏi | Đo bằng |
|---|---|---|
| **RQ-A** | *With four to six collaborating hospitals, which rules remain mathematically valid, which degenerate into simpler operators, and when does sample-size weighting hand unilateral control to a single institution?* | Bảng hợp lệ theo số client + bảng hợp lệ theo trọng số |
| **RQ-B** | *When the central server defends against f assumed attackers in clean and attacked regimes, what is the accuracy cost of robustness, and which specific hospitals bear that cost?* | Accuracy trung bình, worst-honest, **ảnh hưởng tương đối từng client** |
| **RQ-C** | *When a major clinical centre turns Byzantine and global performance drops sharply, how much of that degradation is true adversarial damage versus the unavoidable loss of that institution's honest training data?* | **Đối chứng exact-twin leave-out** |

Ba câu này xếp theo đúng thứ tự người đọc cần: *có hợp lệ không* → *giá bao nhiêu* → *giá đó là thật hay là ảo giác đo lường*. RQ-C là câu mạnh nhất.

---

## 2. Bộ tiêu chí nghiên cứu

### 2.1 Dữ liệu — phân vùng thật, không tổng hợp

| Bộ | n | Cơ sở (lớn → nhỏ) | Mô hình | Metric chính | Vòng | Seed |
|---|---|---|---|---|---|---|
| Fed-Heart-Disease | **4** | Cleveland 40,9 % · Hungary 35,4 % · VA 17,5 % · Switzerland **6,2 %** | logistic regression | accuracy (weighted theo test size) | **106** | 20 |
| Fed-TCGA-BRCA | **6** | Northeast 28,6 % · West 18,9 % · South 18,0 % · Midwest 14,9 % · Europe 14,9 % · Canada **4,6 %** | linear Cox | C-index phân tầng | **243** | 20 (f=2: 5) |
| Fed-ISIC2019 | **6** | Centre 0 **53,4 %** · C1 17,0 % · C2 14,5 % · C3 9,7 % · C4 3,5 % · C5 **1,9 %** | linear head trên EfficientNet-B0 đóng băng | balanced accuracy gộp | **101** | 20 |

Trước khi làm gì khác, họ **tái lập baseline FLamby**: Heart khớp chính xác từng seed (0,748 ± 0,027), TCGA lệch −0,025 (trong 0,14 SD), ISIC trong khoảng chấp nhận định trước. Đây là cổng vào, không phải phần phụ.

### 2.2 Tám quy tắc × hai chế độ trọng số

FedAvg · coordinate-wise Median · Trimmed Mean · Krum · Multi-Krum · Bulyan · Geometric Median (RFA) · Centered Clipping. Mỗi quy tắc chạy **không trọng số** và **trọng số theo cỡ mẫu**.

Chi tiết quyết định: **trọng số chỉ vào toán tử gộp cuối**, còn **chọn ứng viên và đếm cắt vẫn không trọng số**. Đây chính là biến làm nên phát hiện §3.4 — và là lý do `trimmed_mean (w)` và `multi_krum (w)` sống sót còn `median (w)` thì không.

### 2.3 Bảy tấn công, có một cái thiết kế riêng

`none` · label flipping · sign flipping · Gaussian · ALIE (Baruch) · **ALIE z=1** · IPM. Kẻ tấn công mức mô hình là **omniscient** — thấy toàn bộ update trung thực mỗi vòng.

**ALIE z=1 là đóng góp nhỏ nhưng sắc.** Công thức Baruch đặt *z* từ *n* và *f*; ở n = 4 hoặc 6 với f = 1, nó cho **z = 0** — nghĩa là ALIE chỉ gửi **trung bình của các update trung thực**, tức không tấn công gì. Vậy ALIE chuẩn **chưa bao giờ kiểm tra được** câu hỏi trung tâm: *liệu phòng thủ có phân biệt được kẻ tấn công với một bệnh viện trung thực chỉ đơn giản là có dữ liệu khác không?*

### 2.4 Quy mô chạy

| Hạng mục | Số |
|---|---|
| Bản ghi kết quả | **84.344** |
| Lần chạy có huấn luyện | **54.214** |
| Cấu hình bất khả thi (không chạy) | **30.130** |
| Điểm grid (heart + tcga + isic) | 20.160 + 15.120 + 39.840 = **75.120** |
| Đối chứng leave-out | **7.160** |

Kiểm phép trừ: 84.344 − 54.214 = 30.130, **khớp** con số PROTOCOL ghi.

Thi hành: mỗi lần chạy ghi **một lần, nguyên tử** (file tạm rồi rename) → run bị kill không để lại `.json` hỏng. Grid **resume được**, chia được `<i>/<N>`. Toàn bộ trên **MacBook M4 16 GB**, CPU.

### 2.5 Kiểm tra hợp lệ — hai tầng, và tầng thứ hai là đóng góp mới

Tầng 1 là kiểm tra tổ hợp quen thuộc. Tầng 2 là thứ họ thêm (`validity_table.py --weights`): kiểm tra theo **tỉ lệ dữ liệu**.

> weighted median và weighted GeoMed trở thành **update của client lớn nhất** khi client đó giữ **> 50 %** tổng trọng số.

Kiểm số học: `1/0,534 = 1,8727` — khớp con số 1,87 của bài. Ảnh hưởng tương đối của centre 0 dưới `median (w)` = **1,87** (tức 100 % tổng thể), của centre 1–5 = **0,00–0,01**.

Phát hiện này **không thể thấy bằng kiểm tra n ≥ 2f+3**: ở n = 6, f = 1, mọi quy tắc trừ Bulyan đều qua cửa kiểm tra đếm — kể cả `median (w)` đang là độc tài.

### 2.6 Pre-registration — chỗ đáng học nhất về kỷ luật

`docs/PROTOCOL.md` ghi **từng luật và ngày cố định**, để người đọc biết luật nào được đặt **trước** khi thấy kết quả:

| Ngày | Việc được cố định |
|---|---|
| 2026-10-03 | Luật chọn τ cho Centered Clipping (v2), sửa lên v2.1 cùng ngày |
| 2026-10-04 | Sửa lỗi seed: FLamby gọi `torch.manual_seed(42)` lúc import → ảnh hưởng 4 lần chạy, ghi rõ và chạy lại |
| 2026-10-11 | Grid LR và số vòng cho TCGA, **metric** (C-index phân tầng, 608 cặp) |
| 2026-10-12 | **Amendment 1**: xử lý seed "không bao giờ học được" ở mọi LR |
| 2026-10-13 | Chốt trước ALIE z=1 · grid TCGA · chế độ chính ISIC |
| 2026-10-16 | Luật ISIC (SGD thay Adam, worst-centre với k=5) |
| 2026-10-17 | **Amendment 2**: khi mọi LR ổn định, dùng LR công bố của FLamby |
| 2026-10-18 | **Hợp lệ theo tỉ lệ dữ liệu** · đối chứng leave-out |
| 2026-10-19 | Cột `no_alie` là con số thiệt hại tấn công chính |

Ba điểm đáng chú ý về **tính trung thực**:

- **Amendment 1 và 2 khai rõ là "làm SAU khi thấy kết quả màn hình, TRƯỚC mọi lần chạy tiếp."** Không giấu, không giả vờ tiên nghiệm.
- **Ngưỡng 0,50 / 0,60 cho "collapse"** ở TCGA được khai: *"fixed after seeing the two test-set collapses in the reproduction, but before any validation run."*
- **Họ tự đính chính đúng một tuần sau:** luật chọn τ v1 dùng "lower bound > 0", sửa thành "> +0,5 điểm" vì nhận ra v1 *"would systematically favour larger tau, i.e. less clipping and less robustness, whenever seed noise is small."*

Ngoài ra họ **miễn trừ metric không đủ bằng chứng**: worst-region của TCGA chỉ tính vùng có **≥ 3 ca tử vong trong test** (Northeast 14, West 8, South 4, Midwest 3; loại Europe 2 và Canada 1), vì *"the number of deaths, not pairs, is the real amount of evidence."* South chỉ có 4 ca → báo như **remark, không phải finding**.

---

## 3. Bốn kết quả

### 3.1 [RQ-A] Hợp lệ phải xét theo tỉ lệ dữ liệu, không phải số client

| Quy tắc | n=4 f=1 | n=4 f=2 | n=6 f=1 | n=6 f=2 | Heart 40,9 % | TCGA 28,6 % | ISIC 53,4 % |
|---|---|---|---|---|---|---|---|
| FedAvg | – | – | – | – | – | – | – |
| Median | hợp lệ | vi phạm | hợp lệ | hợp lệ | hợp lệ | hợp lệ | **Độc tài / gãy f=1 / gãy f=2** |
| Trimmed mean | = median | vi phạm | hợp lệ | = median | hợp lệ | hợp lệ | hợp lệ |
| Krum | vi phạm | vi phạm | hợp lệ | vi phạm | bỏ qua w | bỏ qua w | bỏ qua w |
| Multi-Krum | vi phạm | vi phạm | hợp lệ | vi phạm | n/a | hợp lệ | hợp lệ |
| Bulyan | vi phạm | vi phạm | vi phạm | vi phạm | n/a | n/a | n/a |
| GeoMed | hợp lệ | vi phạm | hợp lệ | hợp lệ | hợp lệ | gãy f=2* | **Độc tài / gãy f=1 / gãy f=2** |
| Centered Clipping | hợp lệ | vi phạm | hợp lệ | hợp lệ | hợp lệ | hợp lệ | **gãy f=1 / gãy f=2** |

Hai thoái hoá được ghi nhận bằng kiểm tra số (500/500 lần chạy khớp): ở `n=4, f=1` và `n=6, f=2`, **trimmed mean không trọng số chính là coordinate-wise median** vì `n − 2f ≤ 2`.

### 3.2 [RQ-B] Cái giá khi sạch, và ai trả

Trọng số theo cỡ mẫu **cải thiện** accuracy trung bình khi mọi bệnh viện trung thực: FedAvg **+3,4** (Heart), **+0,6** (TCGA), **+5,2** (ISIC). Nhưng nó **đánh vào bệnh viện nhỏ**:

| Hiện tượng | Số |
|---|---|
| Heart: FedAvg không trọng số → có trọng số | trung bình 70,9 % → **74,3 %**, worst hospital 66,6 % → **63,0 %** |
| Heart: `median (w)`, Switzerland (6,2 %) | ảnh hưởng **0,00** → worst hospital xuống **58,8 %** |
| ISIC: `median (w)` độc tài | accuracy centre 1: 74,3 % → **43,1 %**; centre 4: 48,8 % → **33,5 %** |

Phát hiện đối nghịch trực giác: **quy tắc không trọng số chiết khấu client có update lạ nhất, không phải client nhỏ nhất.** Tương quan `ρ(cỡ, ảnh hưởng)`:

| Bộ | ρ | Diễn giải |
|---|---|---|
| Fed-Heart-Disease | **+0,20** | phạt bệnh viện **nhỏ nhất** (Switzerland, 30 bệnh nhân) |
| Fed-TCGA-BRCA | **−0,35 … −0,55** | phạt cơ sở **lớn** |
| Fed-ISIC2019 | **−0,60 … −0,77** | phạt cơ sở **lớn** mạnh hơn |

Trên TCGA, **Krum chọn vùng nhỏ nhất (Canada, 40 bệnh nhân) với tần suất gấp 4,4× tỉ lệ danh nghĩa**, làm Krum sạch **thấp hơn FedAvg 13 điểm** (69,0 so với 82,0). Trên ISIC, `median` và `GeoMed` không trọng số giảm ảnh hưởng centre 0 xuống 0,48 / 0,43 tỉ lệ, đồng thời **nâng centre nhỏ nhất lên 1,56–1,67×**, đưa accuracy nội bộ C5 từ 76,6 % lên **91,3 %**.

Một quy tắc gần như không có giá khi sạch: **Centered Clipping không trọng số** — trong 0,1–0,2 điểm của FedAvg trên TCGA và ISIC, và **tốt hơn FedAvg +2,5 điểm** trên Heart.

### 3.3 [RQ-B] Tấn công tàng hình — phát hiện sắc nhất

ALIE z=1, trên Fed-Heart-Disease:

| Quy tắc | Mức sụt của **worst honest hospital** |
|---|---|
| FedAvg không trọng số | **−0,3 ± 0,4** (gần như không hề hấn) |
| Median | **−9,5 ± 0,8** |
| Median (w) | **−10,0 ± 0,6** |
| GeoMed | **−8,6 ± 0,9** |

Đây là **đảo ngược hoàn toàn** kết luận thông thường: tấn công **nhẹ nhất theo trung bình** lại **gây hại nhất cho bệnh viện yếu nhất**. Lý do: *"because median-type operators track coordinate order statistics"* — ALIE z=1 ẩn mình một độ lệch chuẩn **bên trong** dải trung thực, nên nó **dịch chuyển thứ tự** mà median dựa vào.

**Bài học phương pháp:** trung bình gộp **che giấu** loại thiệt hại này. Nếu chỉ báo accuracy trung bình, bạn sẽ kết luận FedAvg tốt hơn median dưới ALIE z=1 — và sai hoàn toàn.

### 3.4 [RQ-C] Kết quả trung tâm: phần lớn "gãy" là mất dữ liệu

Bảng V của bài, tách bằng đối chứng exact-twin. Tỉ lệ "mất dữ liệu / tổng sụt":

**Fed-Heart-Disease, khi Cleveland (40,9 %) tấn công:**

| Quy tắc | Mất dữ liệu | Thiệt hại tấn công | % sụt do mất dữ liệu |
|---|---|---|---|
| Median | **−19,1** | **+0,3** | **98 %** |
| Trimmed mean | **−19,1** | **+0,3** | **98 %** |
| GeoMed | −15,0 | −1,4 | **91 %** |
| Centered Clipping | −19,0 | −1,2 | **94 %** |
| FedAvg | −8,2 | −7,2 | 53 % |

**Fed-ISIC2019, khi centre 0 (53,4 %) tấn công:**

| Quy tắc | Mất dữ liệu | Thiệt hại tấn công | % do mất dữ liệu |
|---|---|---|---|
| Median | −7,5 | −3,8 | 66 % |
| Trimmed mean | −9,1 | −2,3 | 80 % |
| GeoMed | −7,7 | −3,3 | 70 % |
| Centered Clipping | −10,4 | −2,9 | 78 % |
| FedAvg | −10,6 | −8,5 | 55 % |

**Con số gọn nhất:** trung bình 4 quy tắc robust không trọng số, **97 %** mức sụt trên Heart và **74 %** trên ISIC là **do mất dữ liệu**, không phải do tấn công.

Câu của bài: *"Without leave-out controls, an attack by the largest institution makes every defence appear broken."*

### 3.5 Kết quả ngược lại: quy tắc có trọng số **thật sự** bị tấn công

| Quy tắc | Heart: mất dữ liệu | Heart: thiệt hại tấn công |
|---|---|---|
| `median (w)` | −4,5 | **−4,3** |
| `geomed (w)` | −5,3 | **−9,0** |
| `cc (w)` | −3,1 | **−11,1** |
| `trimmed_mean (w)` | −20,6 | **+6,0** (tốt hơn!) |
| `multi_krum (w)` | −17,5 | −1,7 |

Trên ISIC, khi centre 0 vượt 50 % trọng số, thiệt hại tấn công thật: `cc (w)` **−16,1**, `geomed (w)` **−19,5**, `median (w)` **−25,1** — và accuracy gộp dưới `median (w)` rơi xuống **gần mức đoán ngẫu nhiên (11,7–12,6 %)**.

Ngược lại `trimmed_mean (w)` và `multi_krum (w)` — **cắt/chọn theo số đếm trước, rồi mới áp trọng số** — chỉ chịu **−3,0** và **−1,7** điểm. Đây là cơ sở cho khuyến nghị #2 của bài.

### 3.6 Bốn khuyến nghị triển khai

1. **Kiểm tra hợp lệ tổ hợp trước khi chọn aggregator.** Không bao giờ dùng Bulyan ở n ≤ 6; không dùng Krum/Multi-Krum ở n=4 (f≥1) hoặc n=6 (f≥2).
2. **Giữ trọng số mẫu RA NGOÀI bước lọc robust.** Khi một cơ sở giữ > 50 % bản ghi, không dùng weighted median / GeoMed / CC. Ngay cả ở 29 % (TCGA), đưa trọng số vào trong toán tử robust làm **tăng thiệt hại tấn công 1,6–2,2×**. Nếu muốn trọng số, áp **sau** bước chọn theo đếm, hoặc dùng **CC không trọng số**.
3. **Dùng đối chứng leave-out khi đọc stress test.** Không có nó, người thực hành *"risk discarding working count-based defences by mistaking honest data loss for adversarial failure."*
4. **Theo dõi metric validation theo từng cơ sở.** Trung bình gộp **không phát hiện** được độc tài khi sạch (ISIC) và tấn công tàng hình (ALIE z=1 trên Heart).

---

## 4. Đụng chạm với hai nhánh công việc của nhóm

### 4.1 Với nhánh "benchmark đánh giá dữ liệu"

| Nội dung Malkani | Đụng gì | Cần làm |
|---|---|---|
| Data-share validity (> 50 % = độc tài) | Tiêu chí **F2/F3** hiện chỉ có EMD và Gini kích thước | Thêm một chỉ số: **client lớn nhất chiếm bao nhiêu %** — đo được trước huấn luyện, đúng loại chỉ số nhánh này muốn |
| ρ(cỡ, ảnh hưởng) **đổi dấu theo miền** | Đây chính là hiện tượng nhánh này muốn **giải thích** | Bài đo ρ **sau** khi chạy. Nhóm có thể hỏi: chỉ số dữ liệu nào **dự báo** dấu của ρ? |
| Trung bình gộp che giấu hại cho worst-client | Ủng hộ yêu cầu báo cáo metric theo client | Trích làm động lực |
| Worst-metric phải loại đơn vị thiếu bằng chứng | Bài loại vùng có < 3 ca tử vong | Nguyên tắc áp được: worst-client chỉ tính client đủ mẫu test |

### 4.2 Với nhánh "LargeST-ByzBench"

Kiểm trên phân vùng P-A (22 client, 716 cảm biến):

| Kiểm tra | P-A | Ngưỡng | Kết luận |
|---|---|---|---|
| Client lớn nhất | **13,27 %** dữ liệu | độc tài nếu > 50 % | an toàn **3,8×** |
| Hai client lớn nhất cộng lại | **25,28 %** | cặp độc tài nếu > 50 % | an toàn **2,0×** |
| max / min | **9,5×** | — | (Fed-ISIC2019 là 28,1×) |
| Gini kích thước client | **0,401** | — | lệch vừa |
| HHI → số client hiệu dụng | **0,0724 → 13,8** | — | 13,8 trên 22 danh nghĩa |
| Krum hợp lệ đến | **40 %** (cần 21, có 22) | `n ≥ 2f+3` | biên **1 client** |
| Bulyan hợp lệ đến | **20 %** (cần 19, có 22) | `n ≥ 4f+3` | 30 % cần **31** → bất khả |
| Trimmed mean không thoái hoá đến | **40 %** (còn 4 client) | `n − 2f > 2` | thoái hoá nếu còn ≤ 2 |

**Kết luận: P-A tự động đạt kiểm tra data-share** — không client nào gần ngưỡng 50 %. Đây là lý do định lượng để trả lời "22 client có đủ không", thay vì nói "đủ cho Krum".

### 4.3 Chỗ bài này **không** chạm — khoảng trống còn lại

| Malkani làm | Malkani **không** làm |
|---|---|
| Đo cái giá **sau** 54.214 lần chạy | **Dự báo** cái giá **trước** khi chạy, từ chỉ số dữ liệu |
| Y tế, n ∈ {4, 6} | Giao thông, **n = 22**, dữ liệu cảm biến chuỗi thời gian |
| Tấn công **mức cập nhật mô hình** | Tấn công **mức dữ liệu cảm biến** (nhân k, báo 0 xe, kẹt giá trị) |
| Accuracy / C-index / balanced accuracy | **MAE / RMSE** của bài toán **hồi quy** |
| f ∈ {1, 2} | **f đến 9** (40 % của 22) |
| Tương quan `ρ(cỡ, ảnh hưởng)` **sau** khi chạy | Tương quan **dữ liệu ↔ FPR** **trước** khi chạy |

---

## 5. Đánh giá phê bình

### 5.1 Điểm mạnh

- **Câu hỏi đúng chỗ.** RQ-C (tách mất-dữ-liệu khỏi bị-tấn-công) là câu hỏi mà tài liệu Byzantine-FL bỏ qua, và nó **đảo ngược** kết luận của nhiều bài trước.
- **Kỷ luật protocol.** Chốt ngày từng luật, khai amendment, khai ngưỡng hậu nghiệm, tự đính chính τ-rule sau một tuần.
- **Chọn "phân vùng thật" thay vì Dirichlet** — đúng lý do: dị biệt tự nhiên mới phá giả định "client trung thực giống nhau".
- **Phát hành đủ.** 84.344 bản ghi, protocol, script tái lập mọi bảng/hình, release đóng băng.
- **Miễn trừ metric thiếu bằng chứng** thay vì báo một con số ồn ào.
- **Tự khai hạn chế**: không client sampling, không adaptive attack, ISIC dùng backbone đóng băng.

### 5.2 Điểm yếu

- **n quá nhỏ để nói gì về quy mô lớn.** n ∈ {4, 6} là chỗ Krum/Bulyan **bất khả**. Kết quả không ngoại suy được sang n = 22, 100, hay 1000.
- **Tất cả mô hình đều tuyến tính** (logistic regression, Cox, linear head trên đặc trưng đóng băng). Không có một mạng nơ-ron nào được huấn luyện thật — cái giá của phòng thủ **có thể khác hẳn** ở mô hình phi tuyến, nơi hình học của update khác.
- **1 tác giả, chưa qua review.** Code do Claude Code hỗ trợ (khai ở Acknowledgments).
- **Chỉ f ∈ {1, 2}.** Không thử f = 3 trở lên.
- **Độc tài "sạch" chỉ phát hiện được ở nơi có client > 50 %.** Trong 3 bộ dữ liệu thì chỉ ISIC có → mẫu phát hiện = **1 ca**. Đây là điểm yếu thống kê của phát hiện mạnh nhất bài.
- **Không có tương quan định lượng giữa chỉ số dữ liệu và cái giá.** `ρ(cỡ, ảnh hưởng)` là tương quan **sau** khi chạy, không phải chỉ số tiên nghiệm.

### 5.3 Vì sao điểm yếu lại là cơ hội của nhóm

| Malkani yếu ở | Nhánh của nhóm mạnh ở |
|---|---|
| n = 4/6, Krum bất khả | **n = 22**, Krum hợp lệ đến 40 %, Bulyan đến 20 % |
| Mô hình tuyến tính | **GRU/LSTM/STGCN** trên 716 cảm biến |
| Phát hiện độc tài trên 1 ca | **P-A không có client > 50 %** → kiểm tra này *đạt*, không phải *phát hiện* |
| Không dự báo | **dữ liệu → FPR** là đóng góp nhóm có thể làm |

---

## 6. Điều chỉnh cho trang Khảo sát công trình liên quan

Trang [Khảo sát công trình liên quan](../khao-sat-lien-quan.md) đã xếp bài Malkani đúng chỗ ở mục 2, nhưng ba chi tiết cần sửa sau khi đọc toàn văn:

| Chỗ trên trang | Hiện tại | Đúng hơn |
|---|---|---|
| Mục 2, cột "Đã làm được gì" | *"Bộ gộp không trọng số luôn bỏ qua client có cập nhật khác thường nhất"* | Chính xác hơn: chiều của việc chiết khấu **đổi theo miền** — phạt client **nhỏ** trên Heart (ρ = +0,20) nhưng phạt client **lớn** trên ISIC (ρ = −0,77). Đây còn mạnh hơn phát biểu hiện tại |
| Mục 2, cột "Khác nhóm mình ở đâu" | *"Đo sau khi huấn luyện; chấm bộ gộp, không chấm dữ liệu"* | Đúng, nhưng nên thêm: bài **có** đo một chỉ số dữ liệu — tỉ lệ dữ liệu của client lớn nhất — nên nó **gần hơn** nhánh nhóm một bước so với mô tả hiện tại |
| Mục 3.4, dòng `byzantine-fl-bench` | *"Repo nhỏ, 3 bộ gộp trên CIFAR-10, đang phát triển"* | **Sai so với README hiện tại:** repo có **8 bộ gộp** và **3 bộ FLamby** (Heart-Disease, TCGA-BRCA, ISIC2019), không phải CIFAR-10. Đã có release `v1.0-manuscript` với 84.344 bản ghi |
| Mục 5, việc tiếp theo | *"Đọc toàn văn bài Malkani"* | Việc này **đã xong** — xem trang này |

Ngoài ra, một đóng góp của bài nên được đưa vào **bảng bản đồ mục 1**: dòng *"Đo tỉ lệ loại nhầm client trung thực"* hiện xếp **"Rất ít"** với Malkani — nhưng bài còn đo được **phân tách mất-dữ-liệu/thiệt-hại-tấn-công**, thứ chưa có ở bất kỳ công trình nào khác trong bảng. Đề nghị thêm một dòng riêng cho việc này.

---

## 7. Định vị lại sau khi đọc bài này

Trang khảo sát kết luận: *"Đừng gọi là 'benchmark Byzantine-FL trên dữ liệu thật' (phần này đã có người làm), mà là 'thước đo dữ liệu cho Byzantine-FL'."* **Đọc toàn văn xác nhận kết luận đó, và làm nó mạnh hơn.**

Lý do: Malkani đã chiếm trọn vế "benchmark Byzantine-FL trên dữ liệu thật, chia client tự nhiên" — với 54.214 lần chạy, 3 bộ dữ liệu, protocol chốt ngày. Nhóm mà nộp một bài cùng loại sẽ bị so trực tiếp và thua ở mọi trục (số lần chạy, số bộ dữ liệu, độ chín của protocol).

Nhưng khoảng trống mà trang khảo sát nêu — *dự báo hành vi bộ gộp từ dữ liệu trước khi huấn luyện* — **vẫn còn nguyên sau bài này**, và giờ có thêm hai chỗ bám:

1. **Bài đo ρ(cỡ, ảnh hưởng) và thấy nó đổi dấu theo miền.** Nếu chỉ số dữ liệu dự báo được dấu đó, đó là một kết quả cụ thể, kiểm chứng được.
2. **Bài đo phần tách mất-dữ-liệu/thiệt-hại.** Nếu dữ liệu dự báo được **phần nào** của mức sụt là mất dữ liệu, nhóm có một thước đo có mục đích rõ ràng.

Cả hai đều là câu hỏi **nhân quả - dự báo**, không phải bảng điểm mô tả. Đó là hình dạng đóng góp mà trang khảo sát đã gọi là *"điều kiện để benchmark được chấp nhận"*.

---

## Phụ lục — Nguồn đã đọc

| Nguồn | Định danh | Đọc gì |
|---|---|---|
| Malkani (2026) | arXiv:2611.22904 [cs.LG], nộp 17/11/2026 | Toàn văn HTML: §I–§V, Table I–VI, Appendix A |
| Protocol | `docs/PROTOCOL.md` trong repo | Toàn văn |
| Repo | `github.com/adnanmalkani/byzantine-fl-bench` | README, MIT, `v1.0-manuscript`, 8 aggregator, 3 bộ FLamby |
| Nền lý thuyết | Allouah et al., NeurIPS 2023, arXiv:2309.13591 (đã xác minh qua arXiv API) | Abstract + proceedings |
| Baseline y tế | FLamby, Ogier du Terrail et al., NeurIPS 2022 | Qua trích dẫn [3] |

**Kiểm chứng số học** (tính lại từ dữ liệu bài công bố): 84.344 − 54.214 = 30.130 khớp PROTOCOL · `1/0,534 = 1,8727` khớp 1,87 · ISIC share 53,4 % / 1,9 % khớp · Krum/Bulyan ở n=4,6 khớp mọi phát biểu · trimmed mean thoái hoá khi `n − 2f ≤ 2` khớp · P-A 13,27 % / 25,28 % / HHI 0,0724.
