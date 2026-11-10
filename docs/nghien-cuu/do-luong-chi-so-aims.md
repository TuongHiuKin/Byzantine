# Đo chỉ số thí nghiệm theo chuẩn AIMS

> **AIMS loại trừ adversarial robustness khỏi phạm vi. Khung Subject-Item dùng được, torch_measure chưa nên dùng, và grid ByzCity chưa có cột kết quả.**
>
> Tác giả: Nguyễn Quang Huy — SE194177 · GVHD: ThS. Lâm Hữu Khánh Phương · Đại học FPT · 10/11/2026

**Câu hỏi:** báo cáo AIMS + `torch_measure` + các bài cũ nói gì về cách đo chỉ số khi chạy thí nghiệm và tiêu chí đánh giá; áp dụng vào đây ra sao?

**Nguồn sơ cấp:** roadmap AIMS (Truong và cộng sự, 25/04/2026), `aims.stanford.edu/measurement-db`, `torch_measure` docs + GitHub, `ByzCity` grid, `report_data.json`
**Ngày:** 10/11/2026

---

## 0. Ba kết luận

**Thứ nhất — AIMS tự loại trừ đúng bài toán của anh.** Roadmap viết nguyên văn: *"We do not address safety evaluation, red-teaming, or adversarial robustness testing"* — vì đó là *"normative judgments where the 'correct' response depends on context and values, posing construct validity questions that are qualitatively different"*. Byzantine-FL chính là adversarial robustness. AIMS cung cấp **khung đo lường**, không cung cấp **phương pháp cho miền này**.

**Thứ hai — khung Subject–Item–Response áp được, nhưng ma trận hiện tại chưa sẵn.** Grid `byzcity_experiment_grid.csv` là **kế hoạch chạy**, không phải **bảng kết quả**: không có một cột kết quả nào. Chưa đo được gì cho tới khi có cột response.

**Thứ ba — `torch_measure` chưa dùng được cho đồ án.** 20 sao, 32 fork, tutorial trống (*"Coming soon"*), một bản release. Đây là thư viện nghiên cứu sơ khai, không phải công cụ ổn định để đưa vào một benchmark phải nộp.

---

## 1. AIMS nói gì về đo lường — và nó không nói gì

### 1.1 Phạm vi tự khai

Roadmap (Truong, Goodman, Brunskill, Domingue, Haber, Koyejo; 25/04/2026) tuyên bố rõ ranh giới:

| Trong phạm vi | Ngoài phạm vi |
|---|---|
| Đo năng lực qua tương tác item–response | Safety evaluation |
| Hai chế độ: tĩnh ($\theta_i$) và động ($\theta_i(t)$) | Red-teaming |
| IRT, CAT, knowledge tracing | **Adversarial robustness** |
| Construct validity, reliability | Normative judgments |

**Hệ quả trực tiếp:** không thể trích AIMS làm "phương pháp luận nền" cho một benchmark Byzantine. AIMS nói rằng loại đo lường đó cần **xử lý riêng** vì câu hỏi "phản hồi nào đúng" phụ thuộc giá trị, không phụ thuộc năng lực.

Trong Byzantine-FL, "đúng" nghĩa là *client độc hại bị loại* và *client trung thực không bị loại*. Đó là **phán đoán chuẩn tắc**, không phải ước lượng năng lực tiềm ẩn. AIMS không có khung cho việc này.

### 1.2 Cái AIMS thật sự cho, và nó có giá trị

Ba thứ dùng được ngay:

**(a) Khung dữ liệu 4 thành phần.** $(Subject, Item, Interactor, Trial) \to Response$. Đây là cách đặt tên tốt cho ma trận thí nghiệm, và nó **buộc phải tách** "cái được đo" khỏi "cái làm nhiễu".

**(b) Hai chế độ đo.** Tĩnh (một $\theta$ cho mỗi subject) và động (đường $\theta(t)$). Với đồ án: một lần chạy = tĩnh; đường cong theo tỉ lệ độc hại = động.

**(c) Chẩn đoán chất lượng item.** AIMS đưa ra bằng chứng định lượng rất mạnh:

| Phát hiện | Nguồn |
|---|---|
| **22 %** của **445** benchmark công bố mà **không định nghĩa construct** | Bean và cộng sự (2025), trích trong roadmap |
| **8,8 %** item GSM8K có lỗi (câu hỏi mơ hồ, đáp án sai, chấm điểm sai) | Truong và cộng sự (2025) |
| Sau khi loại item lỗi, hạng của DeepSeek-R1 đổi từ **thứ ba từ dưới lên thứ hai** | cùng nguồn |
| Một nhân tố năng lực chung giải thích **66 %** phương sai trên 591 mô hình | Ilic & Gignac (2024) |

Con số 8,8 % là lập luận mạnh nhất cho thiết kế của anh: **nếu item lỗi làm đổi thứ hạng trên một benchmark đơn giản như GSM8K, thì một benchmark Byzantine không kiểm tra item của chính nó sẽ không đáng tin.**

### 1.3 Điều AIMS nói mà báo cáo trước bỏ qua

Roadmap cảnh báo về chính phương pháp mà báo cáo kia đề xuất:

> *"Zhou và cộng sự (2025) áp mô hình IRT 4 tham số cho 11 benchmark, phát hiện biến thiên lớn về chất lượng item — **nhưng công trình này giả định tính một chiều mà không kiểm tra** liệu mỗi benchmark có đo một construct nhất quán hay không."*

Đây đúng là lỗi tôi đã chỉ ra ở báo cáo trước: áp Rasch một chiều lên 6 aggregator mà không kiểm tra tính một chiều. AIMS tự nêu nó như một **hạn chế của công trình đương thời**, không phải cách làm chuẩn.

---

## 2. `torch_measure` — thực trạng

Kiểm trực tiếp PyPI + docs + GitHub:

| | |
|---|---|
| Phiên bản | 0.1.0 (một bản duy nhất) |
| Tác giả | AIMS Foundations |
| GitHub | **20 sao · 32 fork · 1 release** · tạo 21/02/2026 |
| License | MIT |
| Tutorial | **"Coming soon."** |
| Phụ thuộc | torch≥2.0, numpy, scipy, scikit-learn, pandas≥2.3, pyro-ppl, huggingface_hub |

### 2.1 API thật, đọc từ docs

Những gì **có** trong `torch_measure.metrics`:

| Hàm | Chức năng |
|---|---|
| `tetrachoric_correlation(data, min_pairs=5)` | Ma trận tương quan tứ phân cho dữ liệu nhị phân |
| `point_biserial_correlation(continuous, binary)` | Tương quan điểm–nhị phân |
| `infit_statistics(predicted, observed, mask)` | Infit MNSQ theo item; **>1,3 = underfit, <0,7 = overfit** |
| `outfit_statistics(predicted, observed, mask)` | Outfit MNSQ theo item |
| `item_total_correlation(data, mask)` | Tương quan item–tổng đã hiệu chỉnh |

Đây là bộ chẩn đoán **chất lượng item** — đúng thứ cần cho một benchmark. Cụ thể: `infit`/`outfit` cho biết item nào hành xử không nhất quán với mô hình, tức **ô nào trong ma trận là nhiễu chứ không phải tín hiệu**.

**Giới hạn:** mọi hàm nhận `data` là **ma trận nhị phân** (0/1/NaN). Không có hàm nào cho response liên tục. Đây là ràng buộc thiết kế, không phải chi tiết cài đặt.

### 2.2 Vì sao chưa nên dùng

Ba lý do cụ thể:

1. **Tutorial trống.** Trang tutorials ghi đúng hai từ: *"Coming soon."* Không có ví dụ chạy được.
2. **Một release, 0.1.0.** API chưa ổn định. Đưa vào artefact nộp bài nghĩa là người chấm cài `torch-measure==0.1.0` và hy vọng nó chạy.
3. **Kéo theo `pyro-ppl`** — một thư viện xác suất lớn — cho một phép tính mà 40 tham số Rasch làm được bằng 30 dòng PyTorch thuần.

**Khuyến nghị:** không phụ thuộc `torch_measure`. Viết Rasch/2PL bằng PyTorch thuần (đã có trong báo cáo trước, chạy được), nhưng **sao chép ý tưởng chẩn đoán** từ `infit`/`outfit` — đó mới là phần có giá trị.

---

## 3. Áp vào ma trận của anh — số đo thật

### 3.1 Grid hiện tại là kế hoạch, không phải kết quả

Kiểm `byzcity_experiment_grid.csv`:

| Cột kết quả có trong grid | |
|---|---|
| bất kỳ cột nào chứa `mae`/`delay`/`acc`/`score`/`result`/`metric` | **KHÔNG CÓ** |
| `needs_training` | `yes`: 1.770 · `no (reuse model)`: 180 |

Đây là **danh sách việc cần chạy**, không phải kết quả. Không thể tính bất kỳ chỉ số đo lường nào cho tới khi chạy xong và ghi kết quả về.

**Đây là điều quan trọng nhất của cả báo cáo:** mọi đề xuất "dùng IRT đo DB" đều vô nghĩa ở thời điểm hiện tại, vì chưa có cột response nào để đo.

### 3.2 Cấu trúc ma trận nếu có kết quả

Đếm thật trên grid:

**Một điểm phải đếm lại kỹ:** ô không chỉ là `aggregator × item`. Hai cột nữa cũng là **trục**, không phải thuộc tính của ô:

- `agg_params` — **10 mức** (`f=1/2/3`, `beta=0.1..0.4`, `tau=median_norm`, `root=100 samples`, `-`)
- `safety_guard` — **3 mức** (`off`, `clamp`, `clamp+fallback`)

Đếm đúng:

| | |
|---|---|
| Subjects (aggregator) | **6** |
| Items (attack × ratio × scenario × heterogeneity) | **37** (36 tấn công + 1 ô sạch `nan`) |
| Mức `agg_params` | **10** |
| Mức `safety_guard` | **3** |
| **Ô có dữ liệu** | **284** |
| Tổng run | 1.950 |
| **Run/ô** | **6,87 trung bình · min 5 · max 35** |

Nếu bỏ hai trục phụ và chỉ đếm `aggregator × item` thì được 236 ô với **1 run mỗi ô** — nhưng đó là đếm sai, vì mỗi ô đó thực chất chứa nhiều cấu hình khác nhau về `agg_params` và `safety_guard`. Con số **284 ô / 6,87 run** mới là cấu trúc thật, và **không ô nào dưới 5 run**.

### 3.3 Kiểm tra bậc tự do

| | |
|---|---|
| Tham số cần ước lượng | 5 $\theta$ + 36 $\beta$ = **41** |
| Số ô quan sát | **284** |
| Số quan sát | 1.950 |
| Tham số / quan sát | **0,021** |

Ngưỡng kinh điển là < 0,1 — nên **về bậc tự do, Rasch khả thi**. 41 tham số trên 284 ô là tỉ lệ lành mạnh.

### 3.4 Nhưng vẫn có ba vấn đề thật

**(a) 81 % ô có dưới 10 run.** 230/284 ô. Với 5–9 run, ước lượng $\theta$ có sai số chuẩn lớn; `infit`/`outfit` trên 5 quan sát gần như vô nghĩa.

**(b) Item phụ thuộc cục bộ theo thiết kế.** Item = `attack × ratio × scenario × heterogeneity`. Hai item `ALIE_f20_S1_low` và `ALIE_f30_S1_low` chia sẻ 3/4 thành phần. Chúng tương quan vì **cùng cấu trúc**, không vì năng lực tiềm ẩn. Rasch không có cách tách hai nguồn này nếu không khai báo cấu trúc lồng.

**(c) Một chiều chưa được kiểm.** Krum giỏi chống Sign-Flip, gãy dưới Min-Max ở tỉ lệ cao; Median ngược lại. Không có lý do để tin một $\theta$ duy nhất mô tả cả hai. `torch_measure` có `tetrachoric_correlation` để **kiểm** tính một chiều (ma trận tương quan tứ phân gần khối một) — nhưng phải chạy kiểm định, không được giả định.

---

## 4. Nên đo gì — danh mục chỉ số

Kết hợp ba nguồn: AIMS (chẩn đoán item), literature FL (chỉ số miền), và yêu cầu của rubric.

### 4.1 Tầng 1 — chỉ số kết quả (mỗi run ghi)

| Nhóm | Chỉ số | Bắt buộc | Ghi chú |
|---|---|---|---|
| Độ chính xác | masked MAE | **có** | bỏ ô NaN gốc |
| | RMSE | có | |
| | MAPE ngưỡng 20 xe/15ph | có | tránh nổ ở đêm |
| | **mean magnitude** | **có** | đi kèm mọi MAE, chống bẫy đơn vị |
| Mức client | MAE từng client, tệ nhất, p90 | **có** | cái giá dồn lên vài client |
| Phòng thủ | FPR **và** FNR | **có** | phải cả hai |
| | ASR | có | tỉ lệ vòng tấn công đạt mục tiêu |
| | utility retention | có | MAE có phòng thủ / MAE sạch |
| Hệ thống | wall-clock | có | `needs_training` đã có, cần thời gian thật |

### 4.2 Tầng 2 — chẩn đoán chất lượng (một lần, trên cả ma trận)

Đây là phần lấy từ AIMS:

| Chỉ số | Câu hỏi nó trả lời | Lấy từ |
|---|---|---|
| **Infit MNSQ** theo item | Ô nào hành xử không nhất quán gần độ khó? | `torch_measure.metrics.infit_statistics` |
| **Outfit MNSQ** theo item | Ô nào có outlier xa độ khó? | cùng |
| Tương quan tứ phân | Ma trận có gần một chiều không? | `tetrachoric_correlation` |
| Item–total correlation | Item nào không đo cùng construct? | `item_total_correlation` |
| Đường cong $\theta$ theo tỉ lệ | Chế độ động: năng lực có sụp không, ở đâu? | roadmap §5 |

Ngưỡng đọc: infit/outfit **> 1,3 = underfit** (nhiễu), **< 0,7 = overfit** (mẫu Guttman). Đây là ngưỡng trong docs, không phải tôi tự đặt.

### 4.3 Tầng 3 — tiêu chí đánh giá (cổng)

Kế thừa từ rubric đã phân tích, cộng thêm hai cổng từ AIMS:

| Cổng | Ngưỡng | Nguồn |
|---|---|---|
| FedAvg tốt hơn Local-only | Wilcoxon ghép cặp, p < .05 | thiết kế v3 |
| EMD dị biệt | median ≥ 2× IID | thiết kế v3 |
| **Ô vi phạm $n \ge 2f+3$** | gắn `invalid`, không tính là phát hiện | literature |
| **Item chất lượng** | loại item có infit/outfit ngoài [0,7; 1,3] **trước khi** xếp hạng | **AIMS** |
| **Độ phủ ô** | báo cáo % ô có ≥ 5 run | **AIMS** (sparsity disclosure) |

Cổng thứ tư là bài học trực tiếp từ GSM8K: **loại item lỗi trước, rồi mới xếp hạng** — vì nếu không, thứ hạng có thể là artefact của item lỗi.

---

## 5. Ba việc phải làm, theo thứ tự

### 5.1 Sinh cột kết quả (chặn mọi thứ khác)

Grid chưa có kết quả. Việc đầu tiên không phải là IRT, mà là **chạy và ghi kết quả**. Định dạng tối thiểu:

```
run_id, aggregator, attack, ratio, scenario, heterogeneity, seed,
final_mae, mean_magnitude, rmse, fpr, fnr, asr, utility_retention, wall_clock_s
```

Một dòng mỗi `run_id`, khớp 1-1 với grid. Không gộp seed.

### 5.2 Chạy bốn chẩn đoán trước khi báo cáo bất kỳ thứ hạng nào

```python
# sau khi có kết quả: kiểm tra tính một chiều TRƯỚC
R = tetrachoric_correlation(binary_matrix, min_pairs=5)
# gần ma trận khối một -> một chiều hợp lý; nhiều khối -> đa chiều, phải dùng MIRT
```

Nếu ma trận tương quan tứ phân **không** gần khối một: **không dùng Rasch một chiều**. Chuyển sang báo cáo từng chiều (theo loại tấn công), hoặc dùng mô hình đa chiều. Đây chính là lỗi AIMS phê bình ở Zhou và cộng sự.

### 5.3 Đặt lại cách phát biểu kết quả

Với 6 aggregator và 5 run/ô, đừng nói "Krum có năng lực phòng thủ $\theta = 1,2$". Nói:

> "Krum có MAE trung vị 61,3 (IQR 58,9–64,1) trên 5 seed ở tỉ lệ 20 %; khác biệt so FedAvg có ý nghĩa sau Holm (p = .003)."

Đây là ngôn ngữ **đo được**, không phải ngôn ngữ **năng lực tiềm ẩn**. $\theta$ chỉ nên xuất hiện nếu (a) tính một chiều đã kiểm, (b) mỗi ô có ≥ 10 run, (c) infit/outfit trong ngưỡng.

---

## 6. Điều chỉnh so với báo cáo AIMS trước

Tôi đã sai một điểm ở báo cáo `19_PHAN_TICH_BAO_CAO_AIMS.md`, cần sửa:

| Tôi đã nói | Thực tế đo lại | |
|---|---|---|
| "mỗi ô trong ma trận chỉ có **một** giá trị" | **6,87 run/ô** trên 284 ô, min 5 | **sai** |
| "Rasch không khả thi vì thiếu bậc tự do" | 40 tham số / 1.950 quan sát = **0,021**, dưới ngưỡng 0,1 | **khả thi về bậc tự do** |

Lỗi của tôi hai lần, cùng một gốc: **đếm ô mà không kiểm khoá ô**.

Lần đầu tôi đọc đoạn code mẫu của báo cáo, thấy `item = attack + ratio + scenario + non_iid` rồi giả định mỗi item xuất hiện một lần — sai, vì mỗi item có nhiều seed.

Lần thứ hai, khi kiểm lại bằng `csv.DictReader`, tôi dựng khoá thiếu `agg_params` và `safety_guard`, nên mỗi ô chỉ còn một run và kết luận vẫn sai theo hướng ngược lại.

Đếm đúng phải gồm **cả bốn trục phụ**: `agg_params` (10 mức) và `safety_guard` (3 mức). Kết quả **284 ô, 6,87 run/ô, không ô nào dưới 5**.

Lần thứ ba tôi vẫn sai, vì dựng khoá bằng `csv.DictReader` còn `attack` rỗng đọc thành chuỗi `"None"`, trong khi pandas đọc thành `NaN` — hai khoá khác nhau cho cùng một ô. Chỉ khi dùng **một** đường đọc (pandas) cho cả tài liệu và test thì con số mới ổn định. Đây là bài học: khi đếm ô, phải kiểm rằng mọi giá trị rỗng được chuẩn hoá **giống nhau** ở mọi nơi.

**Kết luận không đổi** nhưng lý do đổi: IRT **không** bị loại vì thiếu dữ liệu; nó bị **hoãn** vì (a) chưa có cột kết quả, (b) tính một chiều chưa kiểm, (c) 60 % ô dưới 10 run. Ba lý do này yếu hơn "bất khả thi" nhưng vẫn đủ để không dùng ngay.

---

## 7. Trả lời trực tiếp

> Đo chỉ số thí nghiệm khi chạy và mục tiêu đo đạc tiêu chí đánh giá — theo AIMS và các bài cũ?

**Khi chạy, ghi bốn nhóm:** độ chính xác (MAE + **mean magnitude** + RMSE + MAPE ngưỡng), mức client (từng client, tệ nhất, p90), phòng thủ (**FPR và FNR bắt buộc**, ASR, utility retention), hệ thống (wall-clock).

**Tiêu chí đánh giá, năm cổng:** FedAvg > Local-only (Wilcoxon, p<.05); EMD ≥ 2× IID; ô vi phạm $n \ge 2f+3$ gắn `invalid`; **loại item có infit/outfit ngoài [0,7;1,3] trước khi xếp hạng**; **báo cáo % ô có ≥5 run**.

**Từ AIMS, dùng ba thứ:** khung 4 thành phần để đặt tên; chẩn đoán item (infit/outfit/tetrachoric) làm bộ lọc chất lượng; cảnh báo GSM8K 8,8 % làm lập luận cho việc tự kiểm item.

**Từ AIMS, không dùng:** IRT/Rasch như phương pháp chính (chưa đủ điều kiện); `torch_measure` như phụ thuộc (0.1.0, tutorial trống).

**Việc chặn đầu tiên:** grid chưa có cột kết quả. Không có kết quả thì không có gì để đo.

---

## Phụ lục — nguồn

| Nội dung | Nguồn |
|---|---|
| Phạm vi loại trừ adversarial robustness | Truong và cộng sự (2026), *A Measurement Science Roadmap*, §Scope |
| 22 % / 445 benchmark không định nghĩa construct | Bean và cộng sự (2025), trích trong roadmap §2 |
| GSM8K 8,8 % item lỗi, đổi thứ hạng | Truong và cộng sự (2025), roadmap Hình 2 |
| 66 % phương sai một nhân tố | Ilic & Gignac (2024), trích trong roadmap §3 |
| Phê bình Zhou và cộng sự giả định một chiều | roadmap §3, *Positioning* |
| API `infit`/`outfit`/`tetrachoric` | `torch-measure.readthedocs.io/en/latest/api/metrics.html` |
| 20 sao, 32 fork, tutorial "Coming soon" | GitHub `aims-foundations/torch_measure` |
| 270 benchmark, 8,4M items, 92,1M responses, 781 subjects | `aims.stanford.edu/measurement-db` |
| 6 aggregator, 36 item, 212 ô, 9,03 run/ô | `byzcity_experiment_grid.csv` |
| Grid không có cột kết quả | cùng tệp, 17 cột đã liệt kê |
