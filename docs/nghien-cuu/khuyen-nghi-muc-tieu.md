# Khuyến nghị chọn mục tiêu đánh giá

> **Tổng hợp bốn nguồn bằng chứng: chọn cái giá của phòng thủ làm mục tiêu chính, tấn công cảm biến làm phụ, loại tấn công mô hình thuần.**
>
> Tác giả: Nguyễn Quang Huy — SE194177 · GVHD: ThS. Lâm Hữu Khánh Phương · Đại học FPT · 10/11/2026

**Mục đích:** từ kết quả khảo sát web, ba báo cáo phân tích (AIMS, bài báo liên quan LargeST, đo lường chỉ số), và dữ liệu đã đo — chọn **mục tiêu đánh giá nào** cho benchmark.

**Sinh viên:** Nguyễn Quang Huy — SE194177 · **GVHD:** ThS. Lâm Hữu Khánh Phương · Đại học FPT
**Ngày:** 10 tháng 11 năm 2026
**Số liệu:** log phân tích cục bộ

---

## Tóm tắt

Bốn nguồn bằng chứng độc lập dẫn đến **cùng một khuyến nghị**. Báo cáo đề xuất chọn **cái giá của phòng thủ dưới dị biệt tự nhiên** làm mục tiêu chính, **tấn công mức dữ liệu cảm biến** làm mục tiêu phụ, và **loại** tấn công mức cập nhật mô hình thuần ra khỏi trọng tâm.

| Bằng chứng | Con số | Hàm ý |
|---|---|---|
| Trong 114 bài trích dẫn LargeST | **1** có FL, **0** có Byzantine | Miền chưa ai làm — nhưng cũng chưa ai đặt chuẩn |
| Trong 270 benchmark của AIMS | **0** về giao thông | Không có benchmark đối sánh sẵn |
| AIMS tự loại trừ khỏi phạm vi | *"adversarial robustness testing"* | Không mượn được phương pháp luận |
| Grid ByzCity | **0** cột kết quả | Chưa đo được gì; phải sinh response trước |
| Tấn công cảm biến ×3 | MAE ×3,00 nhưng **Δ chất lượng = +0,0** | Kiểm tra thường không phát hiện — đây là phát hiện |
| 22 % của 445 benchmark | không định nghĩa construct | Phải tự định nghĩa, không được mặc định |

Ba câu trả lời ngắn nằm ở §6.

---

## 1. Bối cảnh: hai nhánh, một câu hỏi

Dự án có hai nhánh với dữ liệu và mục tiêu khác nhau:

| | ByzCity | LargeST-ByzBench (GAP-1) |
|---|---|---|
| Dữ liệu | SUMO mô phỏng + TraCI | **PeMS San Diego thật**, 716 cảm biến |
| Tầng | 2 tầng, có điều khiển đèn | 1 tầng, chỉ dự báo |
| Số run | 1.950 | 22.240 (v3) / 5.145 (GAP-1) |
| Chỉ số | delay, queue, spillback | MAE, FPR, FNR, ASR |
| Câu hỏi | đèn tín hiệu có an toàn | **cái giá phòng thủ trên dữ liệu thật** |

Báo cáo này tập trung nhánh **LargeST-ByzBench**, vì đó là nơi có dữ liệu thật và có khoảng trống đã kiểm chứng. Nhánh ByzCity được nêu ở §5 vì grid của nó là ví dụ cụ thể cho vấn đề "chưa có cột kết quả".

---

## 2. Dữ liệu: nền tảng đã kiểm chứng

### 2.1 Bộ dữ liệu

LargeST San Diego (PeMS District 11), 716 cảm biến vòng, 2017–2021, tái lấy mẫu 15 phút.

| Chỉ số | Giá trị |
|---|---|
| Cảm biến | 716 |
| Số ô dữ liệu (5 phút, 5 năm) | 376.535.808 |
| Ô khuyết thiếu | 12.326.778 |
| **Tỷ lệ khuyết thiếu (gộp)** | **3,27 %** |
| Cạnh đồ thị | 18.035 |
| Ngưỡng bão hoà PeMS | 999 xe/5ph |

Khuyết thiếu **không đều**: 2017 = 2,70 %, 2018 = 1,37 %, 2019 = 2,16 %, 2020 = 4,10 %, 2021 = 6,03 %.

### 2.2 Cổng tái lập

| | Giá trị |
|---|---|
| HL MAE 2019 đo được | **60,80** |
| HL MAE bài báo công bố | 60,79 |
| Sai lệch | 0,01 |

Đây là điều kiện cần: nếu pipeline không tái lập được số của bài gốc, mọi kết luận sau đó vô nghĩa.

### 2.3 Trôi phân phối có thật

| | |
|---|---|
| Lưu lượng trung bình 4/2020 | 128,49 xe/15ph |
| Nền 4/2017–2019 | 250,32 xe/15ph |
| Mức giảm | **−48,67 %** |

Đây là hiệu ứng trôi lớn nhất trong dữ liệu, và là lý do trục "trôi phân phối" có cơ sở thực nghiệm.

### 2.4 Dị biệt tự nhiên — trục trung tâm của khuyến nghị

Earth Mover's Distance giữa phân phối lưu lượng từng hành lang, 716 cảm biến, 2019, giờ 06–22:

| Cách chia | min | median | p90 | max |
|---|---:|---:|---:|---:|
| Theo hành lang (26 nhóm) | 4,1 | **86,4** | 193,3 | 307,4 |
| IID ngẫu nhiên (26 nhóm) | 5,2 | 22,6 | 43,9 | 74,1 |

**Tỉ lệ median = 3,81×.** Chia theo hành lang tạo dị biệt gần bốn lần IID, **đo được trước khi chạy thí nghiệm nào**.

Cơ chế cụ thể: I15-N trung bình **414,6** xe/15ph, SR11-E chỉ **23,1** — chênh **18×**. Client I15-N có update magnitude lớn gấp 18 lần, nên median sẽ coi nó là outlier.

---

## 3. Khoảng trống: bốn nguồn bằng chứng

### 3.1 Tập trích dẫn LargeST trống ở trục Byzantine

LargeST (NeurIPS 2023) có **116 trích dẫn**, lấy được **114 bản ghi**, **90** có abstract.

| Lọc trên title + abstract | Số bài |
|---|---:|
| Có "federated" | **1** |
| Có "byzantine" / "poison" / "malicious" | **0** |
| Có cả hai | **0** |

Phân bố theo năm: 2024 = 29 · 2025 = 21 · **2026 = 64**. Tốc độ dùng tăng gần gấp ba, nhưng trục an toàn vẫn trống.

Bài FL duy nhất là **CRAFT** (CIKM 2026) — federated *transfer* learning giữa các thành phố, có LLM + mixture-of-experts, **không Byzantine, không tấn công**.

### 3.2 AIMS không có benchmark giao thông

Trong **270** benchmark của Stanford AIMS:

| Danh mục | Số |
|---|---:|
| reasoning | 76 |
| safety | 42 |
| ml_engineering | 7 |
| cybersecurity | 4 |
| **giao thông / vận tải** | **0** |

Tổng: **8.403.704** items, **92.060.497** responses, **19** danh mục. Không một benchmark nào về giao thông. Gần nhất là SVRPBench — định tuyến xe, không phải dự báo lưu lượng.

### 3.3 AIMS tự loại trừ đúng bài toán này

Roadmap AIMS (Truong, Goodman, Brunskill, Domingue, Haber, Koyejo; 25/04/2026) tuyên bố phạm vi:

> *"We do not address safety evaluation, red-teaming, or **adversarial robustness testing**: these involve normative judgments where the 'correct' response depends on context and values, posing construct validity questions that are qualitatively different from ability estimation."*

Byzantine-FL là adversarial robustness. **Không thể trích AIMS làm phương pháp luận nền** cho một benchmark Byzantine. AIMS cho khung, không cho phương pháp miền.

### 3.4 Nhưng AIMS cho ba thứ dùng được

| Thứ | Nội dung |
|---|---|
| Khung 4 thành phần | $(Subject, Item, Interactor, Trial) \to Response$ — buộc tách "đo" khỏi "nhiễu" |
| Chẩn đoán chất lượng item | infit/outfit MNSQ, tương quan tứ phân, item–total |
| Bằng chứng item lỗi | **8,8 %** item GSM8K lỗi; loại ra thì DeepSeek-R1 đổi từ thứ ba từ dưới lên **thứ hai** |

Thêm hai con số cho thấy benchmark hiện có cấu trúc nhưng chưa được kiểm đủ:

- **22 %** của **445** benchmark được công bố mà **không định nghĩa construct** (Bean và cộng sự, 2025).
- Một nhân tố năng lực chung giải thích **66 %** phương sai trên **591** mô hình (Ilic & Gignac, 2024) — nghĩa là có cấu trúc một chiều mạnh, nhưng phải **kiểm** chứ không được **giả định**.

**Hàm ý cho khuyến nghị:** nếu chuẩn ngành còn 22 % không định nghĩa construct, thì một benchmark mới **phải tự định nghĩa rõ** — đó là điều kiện để đứng vững, không phải phần phụ.

---

## 4. Đo được gì — bằng chứng định lượng

### 4.1 Tấn công cảm biến vượt kiểm tra chất lượng

Đo trên cảm biến thật (ID 1116061), bộ kiểm tra 4 luật:

| Tấn công | Δ điểm chất lượng | Hệ số MAE |
|---|---|---:|
| Nhân ×3 | **+0,0** | **3,00×** |
| Nhiễu ngẫu nhiên | 100,0 | 11,29× |
| Báo 0 xe | — | 0,00× |

Tấn công nhân ×3 làm sai số tăng gấp ba nhưng **không thay đổi một tín hiệu chất lượng nào** (Δ = +0,0 trên thang 100). Trong khi nhiễu ngẫu nhiên — dễ phát hiện hơn nhiều — bị chấm **100,0**.

Tỉ lệ neighbour-ratio z-score: ×2 → z = 3,6 · ×3 → z = 7,3 · ×1,5 → z = 1,8. Ngưỡng thông thường (z = 3) **bỏ lọt mức ×1,5 hoàn toàn**.

### 4.2 Khối lượng chạy

| Quy mô | Số lần chạy | Tuần @0,35 h |
|---|---:|---:|
| Phương án A (subset) | 375 | — |
| **Tầng 1 (bắt buộc)** | **2.060** | **4,3** |
| Tầng 2 (mở tỉ lệ) | 7.820 | 16,3 |
| Tầng 3 (mở client) | 11.730 | 24,4 |
| v3 đầy đủ | 22.240 | 46,3 |

**Năng lực 12 tuần ở 0,35 h/lần: 5.760 lần chạy.** Chỉ Tầng 1 vừa.

### 4.3 Ràng buộc client

716 cảm biến, **26 hành lang**. Phân bố cực lệch: I5-N có **95** cảm biến, SR11-E có **1**.

| n client | min | max/min | Dùng được? |
|---:|---:|---:|---|
| 8 | 86 | 1,1× | có |
| 16 | 26 | 3,7× | có |
| 20 | 15 | 6,3× | biên |
| 26 | 1 | 95,0× | **không** |

**n ≤ 16** mới khả thi. Bản GAP-1 yêu cầu thử **32 client** — bất khả thi.

### 4.4 Ma trận ByzCity: chưa có kết quả

Kiểm `byzcity_experiment_grid.csv`:

| | |
|---|---|
| Tổng run | 1.950 |
| Subjects (aggregator) | 6 |
| Items (attack × ratio × scenario × heterogeneity) | 36 |
| Trục `agg_params` | 10 mức |
| Trục `safety_guard` | 3 mức |
| **Ô có dữ liệu** | **284** |
| Runs/ô | **6,87** (min 5, max 35) |
| Ô dưới 10 run | **230 (81 %)** |
| **Cột kết quả** | **không có** |

Đây là **kế hoạch chạy**, không phải bảng kết quả. Không có cột `mae`, `delay`, `score`, `metric` nào. 1.770 run cần huấn luyện, 180 dùng lại mô hình.

**Hệ quả:** mọi đề xuất "dùng IRT đo ma trận" đều **vô nghĩa ở thời điểm hiện tại** — chưa có response để đo.

---

## 5. Bài học phương pháp từ ba báo cáo

### 5.1 Không dùng IRT làm phương pháp chính (chưa đủ điều kiện)

Ba lý do, theo thứ tự:

1. **Chưa có cột kết quả.** Không có gì để fit.
2. **Tính một chiều chưa kiểm.** Krum giỏi chống Sign-Flip, gãy dưới Min-Max ở tỉ lệ cao; Median ngược lại. Không có lý do tin một $\theta$ duy nhất mô tả cả hai. AIMS tự phê bình đúng lỗi này ở Zhou và cộng sự (2025): *"giả định tính một chiều mà không kiểm tra"*.
3. **81 % ô dưới 10 run.** Với 5–9 run, `infit`/`outfit` gần như vô nghĩa.

Về bậc tự do thì **khả thi**: 41 tham số / 1.950 quan sát = 0,021, dưới ngưỡng 0,1. Nhưng bậc tự do không phải điều kiện duy nhất.

### 5.2 Không phụ thuộc `torch_measure`

| | |
|---|---|
| Phiên bản | 0.1.0 (duy nhất) |
| GitHub | **20 sao · 32 fork · 1 release** |
| Tutorial | *"Coming soon."* |
| Phụ thuộc | torch, numpy, scipy, scikit-learn, pandas, **pyro-ppl**, huggingface_hub |

Nhưng **sao chép ý tưởng** từ API của nó: `infit_statistics`, `outfit_statistics` (ngưỡng **>1,3 = underfit, <0,7 = overfit**), `tetrachoric_correlation`, `item_total_correlation`. Đó là phần có giá trị, viết được bằng PyTorch thuần.

### 5.3 Grid phải có cột kết quả trước

Định dạng tối thiểu, một dòng mỗi `run_id`, khớp 1-1 với grid, **không gộp seed**:

```
run_id, aggregator, attack, ratio, scenario, heterogeneity, seed,
final_mae, mean_magnitude, rmse, fpr, fnr, asr, utility_retention, wall_clock_s
```

`mean_magnitude` bắt buộc đi kèm mọi MAE — chống bẫy đơn vị (288 bin 5-phút cộng lại bằng 30.393 trong khi file 15-phút ghi 10.156, lệch −66,7 %).

---

## 6. KHUYẾN NGHỊ

### 6.1 Mục tiêu chính: **cái giá của phòng thủ dưới dị biệt tự nhiên**

**Phát biểu:** khi không có kẻ tấn công, các bộ gộp Byzantine giảm độ chính xác bao nhiêu trên dữ liệu giao thông thật, và client trung thực nào bị loại nhầm?

**Vì sao chọn:**

| Lý do | Bằng chứng |
|---|---|
| Có cơ sở lý thuyết đã công bố | Karimireddy và cộng sự (ICLR 2022): aggregator Byzantine gãy dưới non-IID **ngay cả khi không có đối thủ** |
| Chưa ai đo trên giao thông thật | 0/114 bài trích dẫn LargeST có Byzantine |
| Đo được **trước** khi chạy thí nghiệm | EMD median 86,4 vs 22,6 = **3,81×**, đo trên 716 cảm biến |
| Có cơ chế cụ thể | I15-N 414,6 vs SR11-E 23,1 xe/15ph = **18×** → median coi client lớn là outlier |
| Không cần giả định gì thêm | Không cần nhãn bất thường, không cần mô phỏng |
| Cả hai kết cục đều công bố được | Nếu gãy: phát hiện. Nếu đứng vững: phòng thủ tốt hơn ta tưởng |

**Chỉ số phải báo cáo:**

| Nhóm | Chỉ số | Bắt buộc |
|---|---|---|
| Phòng thủ | **FPR** (client trung thực bị loại) | **có** |
| | **FNR** (client độc hại được nhận) | **có** |
| | Điểm gãy (110 % MAE FedAvg sạch) | có |
| | Utility retention | có |
| Độ chính xác | masked MAE + **mean magnitude** | **có** |
| | RMSE, MAPE ngưỡng 20 xe/15ph | có |
| Mức client | MAE từng client, tệ nhất, p90 | **có** |
| Hồi quy | FPR ~ đặc trưng chất lượng client (khuyết thiếu, giờ đứng yên, mức trôi) | **có** |

Dòng cuối là phần làm nên đóng góp: **không chỉ báo FPR trung bình, mà chỉ ra FPR dồn lên client nào**.

### 6.2 Mục tiêu phụ: **tấn công mức dữ liệu cảm biến**

**Phát biểu:** tấn công ở mức cảm biến (nhân k, kẹt giá trị, trôi, báo 0, phát lại) có vượt qua kiểm tra chất lượng thông thường và các bộ gộp không?

**Vì sao chọn:**

- **Chưa ai làm trong FL giao thông.** 12 loại tấn công trong GAP-1 gồm 5 loại cảm biến — không bài nào trong 114 bài trích dẫn LargeST có.
- **Đã có bằng chứng định lượng:** ×3 → MAE ×3,00 nhưng Δ chất lượng **+0,0**; nhiễu ngẫu nhiên bị chấm 100,0.
- **Có nền lý thuyết từ miền khác:** Physics-Attested FL (Information, 04/11/2026) nói nguyên văn *"existing defences operate strictly in update space, leaving aggregators blind to data poisoning"* — đúng luận điểm này, nhưng trên hạ tầng nước.

**Rủi ro thời gian:** Physics-Attested FL mới hơn GAP-1 sáu ngày. Nếu ai ghép ý này với giao thông + FL trước, mục tiêu phụ mất tính mới. **Đây là lý do nộp sớm thay vì mở rộng.**

### 6.3 Loại bỏ: tấn công mức cập nhật mô hình thuần

| Lý do loại | |
|---|---|
| Đã bão hoà | FLDetector 389 trích dẫn, ShieldFL 387, AgrEvader 29 |
| Không có gì mới trên giao thông | Sign-Flip/ALIE/Min-Max đã chuẩn hoá từ 2017–2021 |
| Không tạo được phát hiện | Kết quả dự đoán được: Krum chịu được, FedAvg gãy |
| Vẫn phải chạy | Giữ làm **đối chứng**, không làm trọng tâm |

### 6.4 Năm cổng đánh giá

| Cổng | Ngưỡng | Nguồn |
|---|---|---|
| FedAvg > Local-only | Wilcoxon ghép cặp, p < .05 | thiết kế v3 |
| Dị biệt đủ lớn | EMD median ≥ 2× IID | thiết kế v3 |
| Ô vi phạm $n \ge 2f+3$ | gắn `invalid`, không là phát hiện | literature |
| **Chất lượng item** | loại ô có infit/outfit ngoài [0,7; 1,3] **trước khi** xếp hạng | **AIMS** |
| **Độ phủ ô** | báo cáo % ô có ≥ 5 run | **AIMS** |

Cổng thứ tư là bài học trực tiếp từ GSM8K: loại item lỗi trước, rồi mới xếp hạng. Không làm vậy, thứ hạng có thể là artefact của ô lỗi.

### 6.5 Những gì **không được tuyên bố**

| Không nói | Vì sao |
|---|---|
| "năng lực phòng thủ tiềm ẩn $\theta$" | Tính một chiều chưa kiểm; 81 % ô dưới 10 run |
| "chưa ai trên đời làm" | Vehicular AttestedFL (VTC 2024) đã làm |
| "AIMS là chuẩn phương pháp luận" | AIMS tự loại trừ adversarial robustness |
| "5 seed đủ" | $p_{min} = 2/2^5 = 0,0625 > 0,05$ — bất khả thi |
| "32 client" | Chỉ có 26 hành lang, n ≥ 20 không dùng được |
| "1.178 lần chạy" | Ma trận thật là 22.240 |

Nói đúng: *"trong 114 bản ghi OpenAlex trích dẫn LargeST, đếm theo title và abstract, 1 bài có FL và 0 bài có Byzantine"*.

### 6.6 Kế hoạch chạy

| Tầng | Nội dung | Số lần | Tuần |
|---|---|---:|---:|
| **Tầng 1** | n = 8, 16 · tỉ lệ 20 % · 7 bộ gộp · 12 tấn công · 10 seed | **2.060** | **4,3** |
| Tầng 2 | thêm 10/30/40 % — trả lời "điểm gãy ở đâu" | 7.820 | 16,3 |
| Tầng 3 | thêm n = 12 — kiểm $n \ge 2f+3$ | 11.730 | 24,4 |

**Nếu buộc cắt:** giữ Tầng 1 + thêm tỉ lệ **40 %** (nơi Krum gãy, tức nơi có phát hiện). Bỏ Tầng 3.

**Ràng buộc phải khai:** n ≤ 16, không 32. Nếu buộc cắt trục client, giữ tối thiểu 3 mức × 2 bộ gộp × 1 tấn công × 1 tỉ lệ × 5 seed = **30 lần** — rẻ, và cứu được lập luận lý thuyết.

---

## 7. Việc phải làm trước, theo thứ tự

| # | Việc | Vì sao trước | Chặn gì |
|---|---|---|---|
| 1 | **Sinh cột kết quả** cho grid | Không có response thì không đo được gì | Mọi phân tích |
| 2 | **Đo thời gian một lần chạy thật** | Mọi ước lượng tuần dùng 0,35 h/lần, **chưa đo** | Quyết định tầng nào |
| 3 | **Kiểm tính một chiều** (tương quan tứ phân) trước khi dùng bất kỳ $\theta$ | AIMS phê bình đúng lỗi này | Ngôn ngữ báo cáo |
| 4 | **Sửa 6 tuyên bố sai** ở §6.5 trong mọi bản nộp | Người phản biện sẽ tự tính | Tính đúng đắn |
| 5 | Chạy Tầng 1 | 4,3 tuần | Kết quả |

---

## 8. Giới hạn

| Hạn chế | Ảnh hưởng |
|---|---|
| Chỉ dùng OpenAlex cho khảo sát trích dẫn | Chưa tra Scopus/IEEE; 1/114 và 0/114 là **cận dưới**, 24/114 bài không có abstract |
| 0,35 h/lần là **giả định** | Chưa đo thật; nếu 0,15 h thì 12 tuần chứa 13.440 lần và ma trận đầy đủ vừa |
| 3 bài ScienceDirect trả 403 | Chỉ xác minh DOI/metadata |
| Grid ByzCity chưa có kết quả | Mọi phân tích IRT là **khuyến nghị cho tương lai**, không phải kết quả |
| AIMS không có benchmark giao thông | Không có đối sánh sẵn, phải tự xây |

---

## 9. Tóm tắt một đoạn

Bốn nguồn độc lập — tập trích dẫn LargeST (1/114 có FL, 0/114 có Byzantine), 270 benchmark của AIMS (0 về giao thông), roadmap AIMS (tự loại trừ adversarial robustness), và bằng chứng định lượng trên dữ liệu thật (tấn công ×3 giấu hoàn toàn khỏi kiểm tra chất lượng) — dẫn đến cùng một khuyến nghị: **chọn "cái giá của phòng thủ dưới dị biệt tự nhiên" làm mục tiêu chính, "tấn công mức dữ liệu cảm biến" làm mục tiêu phụ, loại tấn công mức cập nhật mô hình thuần khỏi trọng tâm.** Mục tiêu chính đứng vững vì nó có cơ sở lý thuyết đã công bố, đo được trước khi chạy thí nghiệm (EMD 3,81×), có cơ chế cụ thể (18× chênh lưu lượng), và cả hai kết cục đều công bố được — điều mà một benchmark chỉ-để-thắng không có.

---

## Tài liệu tham khảo

Blanchard, P., El Mhamdi, E. M., Guerraoui, R., & Stainer, J. (2017). Machine learning with adversaries: Byzantine tolerant gradient descent. In *Advances in Neural Information Processing Systems 30*.

Bean, A. M., và cộng sự (2025). Measuring what matters: Construct validity in large language model benchmarks. Dẫn theo Truong và cộng sự (2026).

Babar, F. F., Khan, S., & Parkinson, S. (2026). HuddsTrafficFL: A benchmark testbed and dataset for Byzantine-robust federated learning in urban traffic systems. *Knowledge-Based Systems*. https://doi.org/10.1016/j.knosys.2026.117003

Karimireddy, S. P., He, L., & Jaggi, M. (2022). Byzantine-robust learning on heterogeneous datasets via bucketing. In *International Conference on Learning Representations*.

Liu, X., Xia, Y., Chen, J., Yang, Q., & Liu, Y. (2023). LargeST: A benchmark dataset for large-scale traffic forecasting. In *Advances in Neural Information Processing Systems 36, Datasets and Benchmarks Track*.

McMahan, B., Moore, E., Ramage, D., Hampson, S., & Agüera y Arcas, B. (2017). Communication-efficient learning of deep networks from decentralized data. In *Proceedings of the 20th International Conference on Artificial Intelligence and Statistics* (PMLR 54, pp. 1273–1282).

Shejwalkar, V., & Houmansadr, A. (2021). Manipulating the Byzantine: Optimizing model poisoning attacks and defenses for federated learning. In *Proceedings of the Network and Distributed System Security Symposium*.

Truong, S., Goodman, N., Brunskill, E., Domingue, B., Haber, N., & Koyejo, S. (2026). *A measurement science roadmap: From human assessment to AI evaluation*. Stanford University.

Xie, C., Koyejo, O., & Gupta, I. (2019). Fall of empires: Breaking Byzantine-tolerant SGD by inner product manipulation. In *Proceedings of the 35th Conference on Uncertainty in Artificial Intelligence* (PMLR 115).

Yin, D., Chen, Y., Kannan, R., & Bartlett, P. (2018). Byzantine-robust distributed learning: Towards optimal statistical rates. In *Proceedings of the 35th International Conference on Machine Learning* (PMLR 80, pp. 5650–5659).

---

## Phụ lục A — Bản đồ nguồn

| Nội dung | Tệp |
|---|---|
| Mọi con số trong báo cáo này | log phân tích cục bộ |
| Sinh số liệu | script phân tích cục bộ |
| Khảo sát 114 bài trích dẫn | log phân tích cục bộ |
| Ma trận 270 benchmark AIMS | `aims_benchmarks_catalog.json` |
| Khối lượng chạy, ràng buộc client | log phân tích cục bộ |
| Dữ liệu, cổng tái lập, COVID | log phân tích cục bộ |
| Grid ByzCity | `byzcity_experiment_grid.csv` |

## Phụ lục B — Bộ kiểm chứng

| Script | Số phép |
|---|---|
| `44_verify_run_volume.py` | 18 |
| `47_verify_tong_hop.py` | 92 |
| `50_verify_test_cases.py` | 54 |
| `51_verify_related_work.py` | 53 |
| `52_verify_aims_analysis.py` | 45 |
| `53_verify_do_luong.py` | 47 |
