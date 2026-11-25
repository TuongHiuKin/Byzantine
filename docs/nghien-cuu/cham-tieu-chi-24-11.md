# Chấm chính bộ tiêu chí 24/11 lên LargeST — kết quả và bốn lỗi thiết kế

*Phân tích phản biện bộ tiêu chí đánh giá dữ liệu (bản 24/11/2026) · 24/11/2026*

!!! info "Vì sao có trang này"
    Trang chủ đặt ra 8 tiêu chí T2/T3/F2/F3/B1/B3/K2/K3 và chọn **LargeST San Diego** làm bộ dữ liệu chính. Nguyên tắc đầu tiên của một rubric là nó phải **đứng được khi chấm lên chính dữ liệu mà tác giả đã chọn**. Trang này chạy đúng 7 tiêu chí đo được (B1 cần huấn luyện nên để riêng) lên dữ liệu HDF5 gốc, bằng mã chạy được, và báo cáo kết quả — kể cả phần bất lợi.

---

## 0. Kết luận trước

**Chấm xong: 1 đạt, 4 trượt ngưỡng, 2 không dùng được vì lỗi thiết kế.**

| Mã | Đo được | Ngưỡng 3 điểm (theo trang) | Kết quả |
|---|---|---|---|
| **T2** Độ đầy đủ | NaN **2,161 %** | ≤ 1 % | **TRƯỢT** (0 điểm) |
| **T3** Tính hợp lệ | lỗi **2,79 %** | ≤ 1 % | **TRƯỢT** (0 điểm) |
| **F2** Dị biệt | **2,85×** khi RNG sạch · 3,81 chỉ khi dùng chung RNG | ≥ 3 | **TRƯỢT** ở cách viết đúng |
| **F3** Tỉ trọng | Gini **0,401**, lớn nhất **13,27 %** | Gini 0,2–0,5, không client > 50 % | **ĐẠT** (3 điểm) |
| **B3** Lỗi giống tấn công | **59,09 %** client | 10–40 % | **TRƯỢT** (quá bẩn) |
| **K2** Độ tầm thường | R² **0,8667** | ≤ 0,70 | **TRƯỢT** (0 điểm) |
| **K3** Trôi phân phối | **0,19** (2019) · **0,272** (2020) · **0,527** (2021) | ≥ 2 | **KHÔNG THỂ ĐẠT** |

Ba kết luận:

1. **Rubric tự loại bộ dữ liệu mà nó chọn.** K2 = 0,8667 trong khi ngưỡng là ≤ 0,70. Đây không phải lỗi nhỏ — cùng một ngưỡng, chấm lên chính LargeST SD, cho **0 điểm ở hạng mục "độ tầm thường"**.
2. **K3 không thể đạt trên bất kỳ dữ liệu giao thông thật nào** — kể cả năm COVID. Đây là **lỗi cấu trúc của công thức**, sẽ giải thích ở §3.
3. **F2 là biến ngẫu nhiên, và con số công bố phụ thuộc thứ tự gọi hàm.** Tử số cố định; mẫu số là một lần rút ngẫu nhiên. Qua 200 seed F2 chạy **2,317–4,845** và **16,5 % seed cho 0 điểm**. Nặng hơn: mẫu số còn phụ thuộc **trạng thái RNG tích luỹ** — dùng chung một generator cho cả bước lấy mẫu lẫn bước shuffle cho ra **3,81**; reset generator (cách viết đúng) cho ra **2,85**, tức **trượt ngưỡng 3** (§6).
3. **B1 vẫn chưa đo được** vì cần huấn luyện — đúng như trang đã ghi, nhưng nó là tiêu chí được kỳ vọng dự báo FPR mạnh nhất (§4.2 của trang), nên thiếu nó là thiếu trụ chính.

Điểm tổng: **3/21 (14 %)**, chưa tính B1.

---

## 1. Cách đo và một điều phải nói trước

**Nguồn dữ liệu:** HDF5 gốc `ca_his_raw_2019.h5` (105.120 dòng × 716 cảm biến SD), **không dùng parquet** — parquet đã qua `.fillna(0)`, tức chính bước xóa mất tín hiệu khuyết thiếu mà T2 đo. Dùng parquet thì T2 sẽ luôn bằng 0 % và tiêu chí mất nghĩa.

**Mã:** `61_score_criteria_24-11.py` (T2, T3, F2, F3, B3, K2, K3) và `62_b3_k3_check.py` (sửa B3, kiểm K3 trên ba năm). Kết quả thô ở `03_outputs/logs/criteria_measured_24-11.json`.

**Nói trước về ba chỗ tôi phải tự sửa trong quá trình đo** — vì chúng cho thấy rubric còn chỗ mơ hồ:

- **B3 lần đầu ra 77,27 %.** Lỗi của tôi: tôi tính dòng lưu lượng bằng 0 kéo dài là "mất dữ liệu dài". Nhưng cảm biến đọc 0 xe lúc 3 giờ sáng là **đúng**, không phải thiếu. Bỏ zero-run khỏi luật, còn **59,09 %**.
- **K2 đo bằng hai cách khác nhau** (vector hóa và theo từng cảm biến) cho 0,8667 — khớp. Đây là con số vững.
- **F2 dùng EMD 1 chiều (Wasserstein-1)** tính từ CDF thực nghiệm trên lưới 401 điểm, vì EMD đa chiều cần bài toán vận tải. Với phân phối lưu lượng 1-D, W1 **chính là** EMD, nên đây không phải xấp xỉ.

---

## 2. K2 — tiêu chí tự loại bộ dữ liệu nó chọn

### 2.1 Số đo

Dự báo lưu lượng bằng **hồ sơ trung bình theo giờ trong ngày** (24 giá trị cho mỗi cảm biến), rồi tính R² trên toàn bộ 73.639.430 ô hữu hạn của năm 2019:

$$R^2 = 1 - \frac{\sum (y - \hat{y})^2}{\sum (y - \bar{y})^2} = \mathbf{0{,}8667}$$

Ngưỡng của trang: **R² ≤ 0,70 để được 3 điểm**, với lý do *"nếu chỉ lịch theo giờ đã dự báo đúng, mọi bộ gộp đều trông tốt, kết luận không có ý nghĩa"*.

**LargeST SD được 0,8667 → 0 điểm.**

### 2.2 Vì sao ngưỡng này sai, không phải dữ liệu

Tiêu chí này đo **độ dễ dự báo mức lưu lượng**, nhưng tuyên bố đo **độ tầm thường của bài toán**. Hai thứ này ngược nhau trên dữ liệu tuần hoàn:

- Giao thông có chu kỳ ngày **rất mạnh** — đó là tính chất vật lý, không phải lỗi dữ liệu.
- Chính vì chu kỳ mạnh, hồ sơ giờ giải thích được phần lớn phương sai **của mức trung bình**.
- Nhưng **sai số tuyệt đối** của hồ sơ giờ vẫn lớn: đo được MAE **45,19** so với SOTA **17,74** — tệ **2,5 lần**, và tệ hơn cả **last-value (17,71)**.

Nói cách khác: dữ liệu này **dễ đoán mức** nhưng **khó dự báo chính xác**. R² cao không phải bằng chứng bài toán tầm thường; nó là bằng chứng dữ liệu có mùa vụ. Dùng R² để loại dữ liệu là dùng sai đại lượng.

### 2.3 Sửa thế nào

Không hạ ngưỡng. **Đổi đại lượng đo** sang tỉ số sai số:

$$\text{K2} = \frac{\text{MAE của luật đơn giản}}{\text{MAE của SOTA}}$$

Với LargeST SD: `45,19 / 17,74 = 2,55`. Một bài toán mà luật đơn giản tệ gấp 2,5 lần SOTA **không hề tầm thường**. Ngưỡng hợp lý: **tỉ số ≥ 1,5 thì không tầm thường**.

Điểm mạnh của cách sửa này: nó vẫn tính được trước khi chạy FL (chỉ cần một baseline và một con số SOTA công bố), nên không phá vỡ định vị "đo trước huấn luyện" của benchmark.

---

## 3. K3 — công thức không thể đạt, kể cả trên dữ liệu có COVID

### 3.1 Số đo

$$K3 = \frac{\text{EMD}(\text{nửa đầu},\ \text{nửa sau})}{\text{EMD}(Q1, Q2)}$$

| Năm | Tử số (H1 vs H2) | Mẫu số (Q1 vs Q2) | **K3** | Ghi chú |
|---|---|---|---|---|
| 2019 | 2,301 | 12,081 | **0,190** | Năm "sạch" |
| 2020 | 15,283 | 56,168 | **0,272** | **Có COVID** — trôi mạnh nhất |
| 2021 | 14,822 | 28,102 | **0,527** | Hồi phục |

**Ngưỡng của trang: K3 ≥ 2.** Không năm nào đạt, kể cả năm có đại dịch.

### 3.2 Lỗi cấu trúc

Mẫu số `EMD(Q1, Q2)` là **chênh lệch mùa vụ trong cùng một năm** — đông so với xuân. Tử số là **chênh lệch nửa năm**.

Trên dữ liệu giao thông, **biên độ mùa vụ luôn lớn hơn biên độ trôi**. Nên tỉ số **luôn nhỏ hơn 1** — và ngưỡng 2 đòi hỏi trôi phải **gấp đôi** mùa vụ. Đó là điều không xảy ra trong thực tế, kể cả khi có một cú sốc như COVID: đo được 0,272, tức mùa vụ vẫn lớn gấp **3,7 lần** trôi.

Đây là dạng lỗi phổ biến khi thiết kế chỉ số: **chuẩn hóa bằng một đại lượng lớn hơn đại lượng cần đo**. Chỉ số không phân biệt được "không có trôi" với "có trôi nhưng mùa vụ mạnh hơn".

### 3.3 Sửa thế nào

Ba cách, tùy câu hỏi thật sự muốn trả lời:

1. **So cùng kỳ giữa hai năm:** `EMD(2019 H1, 2020 H1)` — triệt tiêu mùa vụ bằng cách so tháng 1–6 với tháng 1–6.
2. **Chuẩn hóa bằng nhiễu, không bằng mùa vụ:** chia cho EMD giữa hai nửa của **cùng một tháng** — mẫu số nhỏ, phản ánh biến động nền.
3. **Bỏ dạng tỉ số, dùng độ dốc:** hồi quy EMD theo thời gian, báo hệ số góc. Không có ngưỡng cứng, nhưng đọc được chiều và độ lớn.

---

## 4. B3 — dữ liệu quá bẩn so với băng kỳ vọng

**Đo được 59,09 % client** bị gắn cờ theo luật của chính trang ("có cảm biến kẹt, chạm trần hoặc mất dữ liệu dài"), trong khi băng 3 điểm là **10–40 %**.

Phân bố thực tế (13 client bị gắn cờ):

| Client | Kẹt dài nhất | NaN % | Ghi chú |
|---|---|---|---|
| SR94-W | **29,75 h** | 0,015 | kẹt gần 30 giờ |
| SR78-E | 25,00 h | 0,017 | |
| I5-N | 22,58 h | 0,966 | hành lang lớn nhất, 95 cảm biến |
| I905-W | 15,67 h | **14,845** | mất dữ liệu nặng nhất |
| I15-S | 14,83 h | 0,825 | |
| I805-N | 14,75 h | 0,806 | |
| I8-E | 14,42 h | 4,272 | |
| I5-S | 13,42 h | 4,342 | |
| I905-E | 10,08 h | 0,017 | |
| I8-W | 8,33 h | 4,950 | |
| SR78-W | 6,58 h | 0,017 | |
| I805-S | 6,42 h | 2,059 | |
| I15-N | 5,50 h | 2,425 | (kẹt dưới ngưỡng 6 h, nhưng NaN cao + có ô chạm trần) |

**Đây là kết quả có ích, không phải thất bại.** Nó nói rằng LargeST SD có **sẵn hơn một nửa số client là "lành nhưng trông như độc"** — đúng điều kiện B3 muốn tạo ra để thử bộ gộp. Nhưng nó **ra ngoài băng 3 điểm**, nên theo rubric thì bộ dữ liệu này **quá bẩn để dùng làm bộ chính**.

Xử lý đúng không phải nới băng. Hai lựa chọn trung thực:

- **Chấp nhận và khai báo:** dùng LargeST SD, ghi rõ B3 = 59 % và coi đây là **điều kiện thí nghiệm mạnh** (bộ gộp có nhiều cơ hội loại oan). B3 cao chính là biến độc lập tốt cho RQ2.
- **Lọc trước khi chia client:** loại 13 client bị gắn cờ hoặc các cảm biến kẹt dài, rồi chấm lại. Nhưng khi đó phải báo cáo **cả hai** điểm số, vì lọc đi chính là thay đổi dữ liệu.

---

## 5. T2 và T3 — trượt ngưỡng, nhưng ngưỡng có hợp lý?

| Tiêu chí | Đo được | Ngưỡng 3 điểm | Điểm |
|---|---|---|---|
| T2 | NaN **2,161 %** | ≤ 1 % | 0 |
| T3 | lỗi **2,79 %** (2,793 % cảm biến kẹt ≥ 6 h + 0,0003 % ô chạm trần) | ≤ 1 % | 0 |

Đây là chỗ tôi **không** kết luận rubric sai. Ngưỡng 1 % cho dữ liệu PeMS là **quá chặt so với thực tế vận hành** — nhưng đó là một quan điểm hợp lý về chất lượng dữ liệu, và người đặt ngưỡng có quyền đặt kỳ vọng cao.

Điều đáng nêu: nếu **hai trong tám tiêu chí** đều cho 0 điểm trên bộ dữ liệu chính, thì điểm tổng của bộ dữ liệu đó sẽ thấp **bất kể** hành vi bộ gộp — và RQ2 (tương quan giữa điểm và FPR) mất phương sai để tương quan. Một rubric mà bộ dữ liệu chính chỉ đạt ~1/8 hạng mục là rubric **không còn phân biệt được** gì trên dữ liệu đó.

**Đề nghị:** tách hai loại ngưỡng.

- **Ngưỡng "đủ điều kiện chạy"** (gate): dữ liệu phải qua để được đưa vào benchmark. Ở đây nên nới — T2 ≤ 5 %, T3 ≤ 5 % — vì PeMS thật không bao giờ đạt 1 %.
- **Ngưỡng "chất lượng cao"** (score): giữ 1 % để chấm điểm. Một bộ dữ liệu qua gate nhưng không đạt score vẫn dùng được, chỉ là bị trừ điểm.

Như vậy điểm vẫn phân biệt được, và gate vẫn chặn được dữ liệu hỏng thật.

---

## 6. F2 trượt ngưỡng, F3 đạt

### F2: 2,85 ở cách viết đúng, 3,81 nhờ trạng thái RNG — ngưỡng ≥ 3

Đo trên **26 tuyến gốc** của LargeST (đúng như `56_compute_emd.py`), bằng `scipy.stats.wasserstein_distance`, mẫu 20.000/nhóm, seed 0:

| Cách quản lý RNG | EMD thật | EMD đối chứng | **F2** |
|---|---|---|---|
| **Chung một generator** (như script hiện tại) | 86,37 | 22,64 | **3,81** — đạt |
| **Generator mới cho đối chứng** (cách viết đúng) | 86,37 | **30,27** | **2,85** — **trượt** |

Tử số khớp hoàn hảo với con số công bố (86,37 vs 86,4). Toàn bộ khác biệt nằm ở **mẫu số**, và mẫu số phụ thuộc **thứ tự gọi hàm**, không phụ thuộc dữ liệu. Chi tiết ở mục dưới.

Trên **phân vùng P-A 22 client** (định nghĩa khác, dùng trong đề cương §3.2): EMD thật 81,92 / đối chứng 24,20 → **3,386**. Cả ba con số 2,85 · 3,39 · 3,81 đều là tỉ số của **cùng một công thức** trên **cùng một dữ liệu**; chúng khác nhau vì cách chia nhóm và cách quản lý RNG.

**Đính chính một khẳng định tôi đã đăng ở bản trước của trang này.** Tôi từng viết *"`fillna(0)` thổi phồng F2 từ 3,39 lên 3,81"*. Đó là suy luận từ cơ chế, **không phải số đo** — và khi đo thì nó **sai cả hai chiều**. Đo bằng cùng một công cụ trên bốn đầu vào (`64_f2_fillna_test.py`):

| Đầu vào | EMD thật | EMD ngẫu nhiên | **F2** | NaN % | 0 % |
|---|---|---|---|---|---|
| HDF5 5 phút, giữ NaN | 81,924 | 24,196 | **3,386** | 2,161 | 0,165 |
| HDF5 15 phút, **không** điền | 81,928 | 24,208 | **3,384** | 2,146 | 0,101 |
| HDF5 15 phút, **`fillna(0)`** | 81,695 | 25,745 | **3,173** | 0 | 2,247 |
| parquet như đang có | 81,695 | 28,633 | **2,853** | 0 | 2,247 |

Hai điều rút ra, cả hai **ngược** với điều tôi đã viết:

1. **`fillna(0)` làm F2 GIẢM, không tăng** — 3,384 → 3,173 (−0,211). Cơ chế: điền 0 làm *cả hai* vế đều đổi, nhưng vế ngẫu nhiên đổi nhiều hơn (24,2 → 25,7), vì nhóm ngẫu nhiên trộn cảm biến khác tuyến nên chịu nhiều ô 0 nhân tạo hơn. Tăng mẫu số thì tỉ số giảm.
2. **Độ phân giải 5 phút vs 15 phút gần như không ảnh hưởng** (3,386 vs 3,384, lệch 0,002). Yếu tố quyết định là **có hay không điền 0**, và **bản parquet đang dùng**.

### F2 không ổn định theo seed — lỗi thiết kế thứ tư

F2 có dạng `EMD(chia thật) / EMD(chia ngẫu nhiên)`. Tử số **cố định** với một bộ dữ liệu và một cách chia. Nhưng **mẫu số phụ thuộc vào một lần rút ngẫu nhiên** — và bất kỳ ai chấm F2 đều phải chọn seed cho lần rút đó, mà trang **không nói seed nào**.

Đo **200 seed** (`67_f2_seed_200.py`; bộ ước lượng histogram đã được kiểm khớp với công cụ trực tiếp — lệch 0,003 trên phép chia thật):

| | Giá trị |
|---|---|
| Tử số (cố định, không ngẫu nhiên) | **81,925** |
| Mẫu số qua 200 seed | **16,908 – 35,361** (trung vị 23,874, sd 3,264) |
| **F2** | **2,317 – 4,845** |
| Trung vị F2 | **3,432** |
| Độ lệch chuẩn | **0,455** |
| **Đạt ≥ 3** | **167/200 = 83,5 %** |
| **Trượt < 3** | **33/200 = 16,5 %** |

Hai hệ quả:

1. **Con số 3,386 tôi báo cáo ở bản trước là seed 0 trên phân vùng P-A — không phải "F2 của LargeST".** F2 là một *phân bố* (qua 200 seed: 2,317–4,845, trung vị 3,432, sd 0,455) **và** phụ thuộc cách quản lý RNG (2,85 hoặc 3,81). Báo một điểm mà không báo seed **và** không báo cách quản lý generator là báo một mẫu như thể nó là hằng số.
2. **Điểm số lật theo seed.** Ngưỡng 3 điểm là F2 ≥ 3. Qua 200 seed, **167 lần đạt và 33 lần trượt (16,5 %)**. Cùng một bộ dữ liệu, cùng một công thức, cùng một ngưỡng — gần **1/6 khả năng nhận 0 điểm** thay vì 3. Một tiêu chí mà điểm của nó phụ thuộc một biến không được khai báo thì chưa phải tiêu chí, mà là một phép thử may rủi.

### Lời giải đúng cho 3,81 — và nó là một lỗi nặng hơn tôi tưởng

Ở bản trước tôi viết 3,81 là "một seed khác". **Đó cũng là đoán, và sai.** Tôi đã lần lượt loại bốn giả thuyết bằng cách đo từng cái:

| Giả thuyết | Kiểm bằng | Kết quả |
|---|---|---|
| Cửa sổ giờ 06–22 | `65_f2_window_test.py` | Lọc 06–22 làm F2 **giảm** còn 3,104. Không phải. |
| `fillna(0)` | `64_f2_fillna_test.py` | `fillna` làm F2 **giảm** 3,384 → 3,173. Không phải. |
| Cỡ mẫu 20.000/nhóm | `77_f2_attribution.py` | Đổi tử số rất ít, tỉ số 2,803–2,889. Không phải. |
| Nhóm IID đều nhau vs lệch cỡ | `78_f2_equal_vs_matched.py` | Tử số khớp đúng **86,37**, mẫu số vẫn 30,27. Không đủ. |
| **Trạng thái RNG tích luỹ** | `79_f2_rng_order.py` | **Khớp chính xác: 86,37 / 22,64 / 3,81** |

Nguyên nhân thật: `56_compute_emd.py` tạo **một** `rng = default_rng(0)` rồi dùng nó cho **cả** bước lấy mẫu theo hành lang (26 lần `rng.choice`) **và** bước `rng.shuffle` dựng nhóm IID. Nên phép shuffle **không phải** `default_rng(0).shuffle()` — nó là shuffle của một generator đã bị tiêu hao 26 lần.

Đo cả hai cách xử lý, cùng công thức, cùng dữ liệu:

| Cách xử lý RNG | Tử số | Mẫu số | **F2** |
|---|---|---|---|
| **Chung một `rng`** (như `56` đang làm) | 86,37 | **22,64** | **3,81** |
| `rng` mới cho nhóm đối chứng | 86,37 | 30,27 | **2,85** |
| Đề cương công bố | 86,40 | 22,60 | 3,81 |

**Cùng một công thức, cùng dữ liệu, hai cách quản lý RNG → 3,81 hoặc 2,85.** Chênh **0,96**.

Đây là lỗi **nặng hơn** lỗi seed tôi báo trước đó, vì hai lý do:

1. **Nó không lộ ra khi chạy lại script.** `56_compute_emd.py` tái lập đúng 3,81 mỗi lần — nên bất kỳ ai kiểm tra cũng thấy "đúng". Chỉ khi viết lại độc lập từ công thức mới lộ ra tỉ số thật là 2,85.
2. **Mẫu số 22,6 phụ thuộc thứ tự tiêu hao RNG, không phụ thuộc dữ liệu.** Đó không phải một tính chất của bộ dữ liệu; đó là một tính chất của thứ tự gọi hàm.

**Hệ quả cho ngưỡng ≥ 3:** với cách quản lý RNG sạch (mỗi phép ngẫu nhiên một generator riêng, tức cách viết đúng), F2 của bộ dữ liệu này là **2,85 — trượt ngưỡng 3**. Con số 3,81 chỉ đạt được nhờ trạng thái RNG tích luỹ.

**Sửa thế nào:** bỏ mẫu số ngẫu nhiên. Dùng mốc **tất định**: EMD giữa các cảm biến **trong cùng một tuyến** (dị biệt nội tại), hoặc EMD giữa các tuyến so với EMD giữa **các nửa thời gian của cùng một tuyến**. Tỉ số khi đó không phụ thuộc lần rút nào và không phụ thuộc thứ tự gọi hàm.

### F3: Gini 0,401, client lớn nhất 13,27 %

| Chỉ số | Giá trị | Ngưỡng |
|---|---|---|
| Gini | **0,401** | trong 0,2–0,5 — đạt |
| Client lớn nhất | **13,27 %** | ≤ 50 % — đạt |
| Hai lớn nhất | 25,28 % | — |
| max/min | 9,5× | — |

Đạt. Lưu ý ngưỡng dưới của Gini (0,2) **có vấn đề riêng**: Gini thấp nghĩa là các client **cân bằng**, mà cân bằng thì **ít dị biệt** — tức là F2 thấp. Hai tiêu chí F2 và F3 **kéo ngược nhau**, và rubric không nói xử lý xung đột đó thế nào.

---

## 7. Bảng tổng hợp — và một vấn đề về điểm tổng

| Mã | Đo được | Ngưỡng | Điểm | Loại lỗi nếu trượt |
|---|---|---|---|---|
| T2 | 2,161 % | ≤ 1 % | **0** | ngưỡng quá chặt cho PeMS |
| T3 | 2,79 % | ≤ 1 % | **0** | ngưỡng quá chặt cho PeMS |
| F2 | **2,85×** (RNG sạch) · 3,81 chỉ khi RNG dùng chung | ≥ 3 | **0** | mẫu số phụ thuộc một lần rút **và** thứ tự gọi hàm |
| F3 | 0,401 / 13,27 % | 0,2–0,5, ≤ 50 % | **3** | — |
| B1 | *chưa đo* | ≥ 2 | **?** | cần huấn luyện |
| B3 | 59,09 % | 10–40 % | **0** | dữ liệu thật quá bẩn |
| K2 | R² 0,8667 | ≤ 0,70 | **0** | **đại lượng đo sai** |
| K3 | 0,19–0,53 | ≥ 2 | **0** | **công thức không thể đạt** |
| | | | **3/21** | (chưa tính B1) |

**Nếu chấm đủ 8 hạng mục, LargeST SD được khoảng 3/21 điểm (14 %)** — một bộ dữ liệu bị rubric của chính nó xếp vào loại kém, dù đây là benchmark giao thông được trích dẫn nhiều nhất và đã tái lập đúng Bảng 2 của bài gốc (HL MAE 60,80 vs 60,79).

Đó là **dấu hiệu rubric đang đo sai thứ**, không phải dấu hiệu dữ liệu kém. Một rubric mà bộ dữ liệu chuẩn của lĩnh vực chỉ đạt 14 % thì rubric đó cần hiệu chỉnh lại ngưỡng và công thức trước khi dùng để loại bất cứ thứ gì.

---

## 8. Việc cần làm, theo thứ tự

| # | Việc | Vì sao trước |
|---|---|---|
| 1 | **Sửa K2** sang tỉ số MAE (luật đơn giản ÷ SOTA), ngưỡng ≥ 1,5 | Công thức hiện tại loại mọi dữ liệu tuần hoàn, tức mọi dữ liệu giao thông |
| 2 | **Sửa K3** sang so cùng kỳ giữa hai năm, hoặc bỏ dạng tỉ số | Công thức hiện tại không thể đạt, kể cả năm COVID |
| 2b | **Khai báo seed cho F2, hoặc bỏ mẫu số ngẫu nhiên** | 16,5 % seed cho 0 điểm; F2 hiện là biến ngẫu nhiên không khai báo |
| 3 | **Tách ngưỡng gate và ngưỡng score** cho T2/T3 | PeMS thật không đạt 1 %; giữ 1 % làm score, nới gate lên 5 % |
| 4 | **Quyết định B3**: chấp nhận 59 % làm điều kiện mạnh, hay lọc trước | Đây là quyết định về **thiết kế thí nghiệm**, phải chốt trước khi chạy |
| 5 | **Đo B1** — cần mô hình ridge AR-12 huấn luyện tập trung | B1 là tiêu chí dự báo FPR mạnh nhất theo §4.2 của trang |
| 6 | **Ghi rõ đọc HDF5 hay parquet** trong mọi báo cáo F2 | `fillna(0)` thổi phồng F2 3,39 → 3,81 |

Các việc trên sửa được trong một buổi và **phải sửa trước khi chấm thêm bộ dữ liệu nào**, vì nếu không, mọi bảng so sánh sau đó đều dựa trên công thức hỏng.

---

## 9. Những gì trang này làm đúng

Để cân bằng — bản 24/11 này tốt hơn hẳn bản trước ở nhiều điểm:

- **Bỏ F4 khỏi bộ tiêu chí** vì F4 cần chạy FL — quyết định đúng, giữ được định vị "đo trước huấn luyện".
- **RQ3 (tương đương Dirichlet α) là câu hỏi mới và có giá trị thật.** Chưa ai đo dữ liệu giao thông thật ứng với α nào, và nếu đo được thì người khác đọc lại được kết quả Dirichlet của họ. Đây là đóng góp riêng, không trùng Malkani.
- **Mỗi tiêu chí có "núm vặn" và kết quả phải thấy** (§4.2) — đây chính là thiết kế RQ1 đúng: tiêm lỗi đã biết, kiểm tiêu chí phản ứng đơn điệu (Spearman ≥ 0,9) và tiêu chí không liên quan đứng yên (< 15 %). Rất ít benchmark tự kiểm chứng công cụ đo của mình.
- **Khai báo trước rằng kết quả âm tính vẫn được báo cáo** — đúng chuẩn.
- **Chia bước 0 → 4 với "chốt trước" ở bước 2** — đây là kỷ luật pre-registration, cùng ý tưởng với Malkani.

Vấn đề của trang không phải thiếu suy nghĩ. Vấn đề là **ba công thức trong số tám chưa được chạy thử trên dữ liệu thật trước khi đặt ngưỡng** — và đó chính xác là việc trang này vừa làm.

---

## Phụ lục — Trạng thái mã nguồn

Trang chủ viện dẫn ba script. Kiểm trên repo `TuongHiuKin/Byzantine` HEAD `4353d0f` (23/11/2026):

| Tệp được viện dẫn | Có trong repo? |
|---|---|
| `cham_du_lieu.py` | **Không** |
| `du_lieu.py` | **Không** |
| `chay.py` | **Không** |

Toàn bộ `.py` trong repo: `them.py`, `them_cau_hoi.py` (hai script thêm trang MkDocs).

Điều này **không** nhất thiết là lỗi — mã có thể chưa được đẩy lên. Nhưng nó có nghĩa là **chưa ai ngoài tác giả chạy lại được** bất kỳ con số nào trong trang chấm điểm, kể cả F2 = 3,81, HDR = 2,64, K2 = 0,98 của dữ liệu sin. Các con số trong trang này được đo bằng mã ở `61_score_criteria_24-11.py` và `62_b3_k3_check.py`, chạy lại được.

**Kiểm chứng trích dẫn — 10/10.**

- **8/8 arXiv** resolve đúng, title khớp từng chữ (arXiv API, 24/11/2026). Không có định danh nào trỏ sang bài khác.
- **2/2 DOI** khớp **mọi trường** (Crossref, 25/11/2026):

| DOI | Kết quả Crossref | Khớp |
|---|---|---|
| `10.3390/futuretransp6030124` | Petkani et al., *Data Quality in Traffic Management: Framework and Real-World Impacts*, **Future Transportation 6(3):124, 2026** | title, journal, vol 6, issue 3, article 124, năm 2026 — **tất cả** |
| `10.3390/data9120151` | Miller et al., *A Framework for Current and New Data Quality Dimensions: An Overview*, **Data 9(12):151, 2024** | title, journal, vol 9, issue 12, article 151, năm 2024 — **tất cả** |

Danh sách tham chiếu của trang **không có lỗi trích dẫn nào** — kể cả số tập, số kỳ, số bài. Đây là mức chính xác cao hơn phần lớn bài báo đã công bố, và cần nói rõ vì nó **tách biệt** khỏi các vấn đề phương pháp ở trên: người viết tra tài liệu tốt, chỉ là ba trong tám công thức chưa được chạy thử.
