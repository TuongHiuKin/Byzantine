# Phân tích báo cáo Stanford AIMS

> **Kiểm chứng báo cáo crawl 270 benchmark AIMS: số liệu đúng, nhưng viết cho dự án khác và áp IRT sai giả định.**
>
> Tác giả: Nguyễn Quang Huy — SE194177 · GVHD: ThS. Lâm Hữu Khánh Phương · Đại học FPT · 10/11/2026

**Đối tượng:** `Bao_Cao_Crawl_Stanford_AIMS_Measurement_DB.pdf` (10/11/2026)
**Kiểm chứng với:** `aims_benchmarks_catalog.json` (270 benchmarks), `byzcity_experiment_grid.csv` (1.950 run), PyPI, arXiv API
**Ngày:** 10/11/2026

---

## 0. Kết luận

Báo cáo này **crawl đúng và số liệu đúng**. Tôi kiểm lại từng con số với catalog gốc — khớp hết. Bảy arXiv ID đều trỏ đúng bài. Package `torch-measure` có thật trên PyPI.

Nhưng nó mắc **một lỗi định vị nghiêm trọng** và **ba lỗi phương pháp** khiến phần khuyến nghị không dùng được nguyên trạng.

**Lỗi định vị:** báo cáo viết cho **ByzCity** — một đồ án khác (SUMO + đèn tín hiệu, 1.950 run). Công việc hiện tại của anh là **LargeST-ByzBench** (PeMS thật, 22.240 run, GAP-1). Hai dự án khác nhau về dữ liệu, về câu hỏi, và về tầng đo lường.

**Lỗi phương pháp:** phần §4 (dùng Rasch/IRT để "đo DB") áp một mô hình tâm trắc học vào dữ liệu mà **các giả định của nó bị vi phạm**, và trình bày như thể đó là chuẩn của Stanford AIMS — trong khi Stanford AIMS không nói vậy.

---

## 1. Những gì báo cáo làm đúng

### 1.1 Số liệu crawl khớp chính xác

Kiểm từng con số với `aims_benchmarks_catalog.json` (270 bản ghi):

| Báo cáo nói | Catalog thực tế | |
|---|---|---|
| 270 benchmarks | 270 | **đúng** |
| 8.400.000+ items | 8.403.704 | **đúng** |
| 92.100.000+ responses | 92.060.497 | **đúng** (làm tròn lên) |
| 19 categories | 19 | **đúng** |
| Reasoning 76 | 76 | **đúng** |
| General 49 | 49 | **đúng** |
| Safety 42 | 42 | **đúng** |
| Agents & Tool Use 29 | 29 | **đúng** |
| Software Engineering 24 | 24 | **đúng** |
| ML Engineering 7 | 7 | **đúng** |
| Cybersecurity 4 | 4 | **đúng** |

Con số **781 subjects** là con số duy nhất tôi **không tái tạo được** từ catalog: trường `models` là số đếm theo từng benchmark, tổng 22.746 — không phải số mô hình phân biệt. 781 có thể đúng nhưng không suy ra được từ dữ liệu đã crawl. Nên ghi nguồn.

### 1.2 Mười hai benchmark đều có thật

Tôi tra cả 12 trong catalog — không cái nào bịa:

| Benchmark | items | responses | models |
|---|---:|---:|---:|
| `auditing_sabotage_bench` | 68 | 1.869 | 18 |
| `agentdojo` | 1.081 | 69.798 | 29 |
| `dtap_bench` | 13.392 | 106.570 | 10 |
| `llmail_inject` | 207.291 | 461.593 | 23 |
| `svrpbench` | 40 | 160 | 4 |
| `frontieror` | 180 | 2.230 | 15 |
| `enginemt_qa` | 676 | 676 | 1 |
| `tabarena` | 346.195 | 2.457.106 | 384 |
| `perfcodebench` | 1.854 | 23.854 | 20 |
| `harmbench` | 62.160 | 107.274 | 33 |
| `advprompter` | 50 | 100 | 2 |
| `kernelbench` | 250 | 73.998 | 19 |

Số liệu trong báo cáo khớp từng dòng.

### 1.3 Bảy arXiv ID đều đúng bài

Kiểm qua arXiv API:

| ID | Bài thật | Khớp báo cáo? |
|---|---|---|
| 2604.16286 | Auditing Sabotage Bench | **đúng** |
| 2406.13352 | AgentDojo | **đúng** |
| 2605.04808 | DecodingTrust-Agent Platform (DTap) | **đúng** |
| 2506.09956 | LLMail-Inject | **đúng** |
| 2506.20093 | ITFormer (EngineMT-QA) | **đúng** |
| 2605.25246 | FrontierOR | **đúng** |
| 2605.15222 | PerfCodeBench | **đúng** |

Đây là điểm đáng khen: bịa arXiv ID là lỗi phổ biến nhất của báo cáo do LLM sinh, và báo cáo này không mắc.

### 1.4 `torch-measure` là package thật

| | |
|---|---|
| Tên | `torch-measure` 0.1.0 |
| Tác giả | AIMS Foundations |
| Mô tả | "PyTorch-native measurement science toolkit: IRT, CAT, psychometric metrics, and factor models for AI evaluation" |
| Phụ thuộc | torch≥2.0, numpy, scipy, scikit-learn, pandas, pyro-ppl, huggingface_hub |
| Wheel | 90 KB · sdist 4 MB |
| License | MIT |

Đúng là thư viện của Stanford AIMS. Không phải bịa.

---

## 2. Lỗi định vị: báo cáo viết cho dự án khác

### 2.1 Báo cáo nói gì

> "Đối tượng áp dụng: Đồ án Tốt nghiệp Capstone **ByzCity**"
> "ByzCity là đồ án: Federated learning chống tấn công Byzantine cho dự báo lưu lượng **và điều khiển đèn tín hiệu**"
> "Tầng 2 — Điều khiển Vòng kín Vật lý (Closed-loop **SUMO + TraCI**)"

### 2.2 Thực tế trong dự án

Cả hai đều tồn tại, nhưng là **hai nhánh khác nhau**:

| | ByzCity | LargeST-ByzBench (GAP-1) |
|---|---|---|
| Dữ liệu | **SUMO mô phỏng** + TraCI | **PeMS San Diego thật**, 716 cảm biến |
| Tầng 2 | Đèn tín hiệu vòng kín | **không có** |
| Số run | 1.950 | 22.240 (v3) hoặc 5.145 (GAP-1) |
| Số client | 10 | 8–16 |
| Chỉ số | delay, queue, spillback, teleport | MAE, FPR, FNR, ASR |
| Câu hỏi trung tâm | đèn tín hiệu có an toàn không | **cái giá phòng thủ trên dữ liệu thật** |

`byzcity_experiment_grid.csv` **có thật** (1.950 dòng, 17 cột, 6 aggregator, 10 seed) — nhưng grid đó **không có một cột chỉ số SUMO nào**:

```
SUMO metric cols in grid: NONE
```

Không có `delay`, `queue`, `spillback`, `teleport`, `throughput`. Nghĩa là **tầng 2 mà báo cáo mô tả chưa được ghi vào grid**. Báo cáo mô tả một hệ thống 2 tầng, nhưng dữ liệu hiện có chỉ là tầng 1 (FL).

Một chi tiết nữa cho thấy báo cáo đọc grid chưa kỹ: nó viết *"lớp an toàn `{clamp, clamp+fallback}`"* — hai giá trị. Grid thực tế có **ba**: `clamp`, `clamp+fallback`, và **`off`**. Thiếu `off` nghĩa là bỏ mất nhóm đối chứng không bảo vệ — đúng nhóm cần để đo "cái giá của phòng thủ".

### 2.3 Vì sao điều này quan trọng

Toàn bộ phần khuyến nghị của báo cáo — chọn SVRPBench, FrontierOR, ánh xạ delay/queue sang Response — **đứng trên tầng 2 không tồn tại trong dữ liệu**.

Nếu áp nguyên trạng vào LargeST-ByzBench:
- Không có delay/queue để đo → cột Response rỗng
- SVRPBench và FrontierOR không liên quan (chúng là vận tải/OR, không phải dự báo lưu lượng)
- Ánh xạ Item → "Peak/Off-peak, ngã tư trung tâm hay rìa" sai: LargeST chia theo **hành lang**, không theo ngã tư

**Cách sửa:** giữ nguyên phần §1 (khảo sát AIMS — đúng và có giá trị), viết lại §2–§5 cho đúng đối tượng.

---

## 3. Lỗi phương pháp 1: IRT/Rasch không áp được cho dữ liệu này

Đây là phần nghiêm trọng nhất, vì nó là "giá trị cốt lõi" mà báo cáo tự nhận.

### 3.1 Báo cáo đề xuất gì

Ánh xạ 1.950 run thành ma trận Subject × Item, rồi fit **mô hình Rasch**:

$$P(Y_{si}=1 \mid \theta_s, b_i) = \sigma(\theta_s - b_i)$$

với $\theta_s$ = "năng lực phòng thủ nội tại" của aggregator $s$, $b_i$ = "độ khốc liệt" của kịch bản $i$.

### 3.2 Ba giả định bị vi phạm

Mô hình Rasch yêu cầu ba điều. Dữ liệu ByzCity vi phạm cả ba:

**(a) Yêu cầu: mỗi ô (s, i) có nhiều quan sát Bernoulli độc lập.**

Mỗi ô trong ma trận chỉ có **một** giá trị, vì mỗi (subject, item) tương ứng đúng một cấu hình và seed đã bị gộp vào item. Ma trận 6 × N với **mỗi ô một số** — không có gì để ước lượng phương sai. Rasch cần lặp để tách $\theta$ khỏi $b$; với một quan sát mỗi ô, mô hình chỉ là một phép biến đổi đơn điệu của tỉ lệ thành công, không thêm thông tin.

**(b) Yêu cầu: các item độc lập có điều kiện (local independence).**

Các item ở đây là **tổ hợp của cùng những trục**: attack × ratio × scenario × non-IID. Item "ALIE_f40_S1_high" và "ALIE_f30_S1_high" chia sẻ 3/4 thành phần. Chúng tương quan mạnh theo thiết kế, không phải do năng lực tiềm ẩn. Rasch sẽ **gán tương quan đó cho $\theta$**, làm $\theta$ phóng đại.

**(c) Yêu cầu: một chiều (unidimensionality).**

Báo cáo gộp 6 aggregator × nhiều tấn công vào **một** trục $\theta$. Nhưng Krum giỏi chống Sign-Flip và **gãy** dưới Min-Max ở tỉ lệ cao; Median ngược lại. Không có một "năng lực phòng thủ" đơn nhất — có **nhiều năng lực theo loại tấn công**. Ép thành một chiều sẽ tạo ra thứ hạng vô nghĩa.

### 3.3 Vấn đề nhị phân hoá

Báo cáo định nghĩa:

```python
FIXED_TIME_DELAY_BASE = 45.0  # Giả định mốc fixed-time chuẩn
df['success'] = (df['delay'] <= FIXED_TIME_DELAY_BASE * 1.05).astype(int)
```

Hai lỗi trong ba dòng:

1. **`45.0` là "giả định"** — chính comment nói vậy. Không có mốc này trong dữ liệu. Ngưỡng tuỳ ý sẽ quyết định toàn bộ thứ hạng: đổi 45 → 40 và thứ hạng đổi.
2. **`df['delay']` không tồn tại** trong `byzcity_experiment_grid.csv`. Đoạn code sẽ ném `KeyError` ngay dòng đầu.

Nhị phân hoá một chỉ số liên tục (delay) thành 0/1 **vứt bỏ phần lớn thông tin**: một aggregator có delay 46 s và một có 120 s đều thành `0`, dù khác nhau 2,6 lần. Với dữ liệu liên tục, dùng mô hình hồi quy (hoặc IRT liên tục) đúng hơn, và không cần ngưỡng tuỳ ý.

### 3.4 Stanford AIMS không nói làm vậy

Báo cáo trình bày IRT như "chuẩn của Stanford AIMS". Đọc mô tả package thật:

> "`torch_measure` treats evaluation itself as a **predictive modeling problem**: latent-variable models infer a system's capability directly from sparse benchmark observations and **predict its performance on unseen tasks**."

Mục tiêu là **dự đoán hiệu năng trên bài chưa thấy** — không phải "xếp hạng aggregator". Và nó dành cho **benchmark có hàng trăm nghìn phản hồi** (TabArena: 2,4 triệu; LLMail: 461 nghìn), nơi mỗi subject × item có nhiều quan sát.

Áp nó vào 1.950 run với một quan sát mỗi ô là **dùng sai công cụ**, không phải "áp dụng chuẩn".

---

## 4. Lỗi phương pháp 2: đếm trùng và so sánh sai

### 4.1 "781 subjects" không suy ra được

Catalog lưu `models` là **số đếm theo benchmark**. Tổng: **22.746**. Nếu cộng dồn sẽ được 22.746 "subjects", không phải 781. Con số 781 có thể là số mô hình **phân biệt** trên toàn Data Bank — nhưng catalog đã crawl **không chứa tên mô hình**, chỉ chứa số lượng. Vậy 781 đến từ nguồn khác, và báo cáo không ghi nguồn.

### 4.2 So sánh "12 benchmark tiêu biểu" không có tiêu chí

Báo cáo nói "sàng lọc ra 12 benchmarks tiêu biểu nhất" nhưng không nêu tiêu chí lọc. Kiểm lại: trong 270 benchmark, **4 cái** thuộc `cybersecurity`, **7 cái** thuộc `ml_engineering`, **0 cái** thuộc giao thông. Vậy 12 cái được chọn bằng gì?

Đối chiếu với nhu cầu thật của GAP-1, chỉ **2 trong 12** là liên quan:
- `agentdojo` — cặp chỉ số Utility vs ASR (đúng dạng RQ1/RQ2)
- `auditing_sabotage_bench` — phát hiện phá hoại ngầm (gần với phát hiện client độc hại)

Còn lại: SVRPBench (định tuyến xe), FrontierOR (quy hoạch tuyến tính), TabArena (dữ liệu bảng), KernelBench (CUDA kernel), PerfCodeBench (tối ưu mã), LLMail (prompt injection qua email), HarmBench/AdvPrompter (jailbreak), DTap (red-teaming agent) — **không liên quan đến dự báo lưu lượng giao thông**.

### 4.3 Điều báo cáo bỏ sót: AIMS **không có** benchmark giao thông

Đây là phát hiện đáng giá nhất mà báo cáo không nêu. Trong 270 benchmark:

| Danh mục | Số lượng |
|---|---:|
| reasoning | 76 |
| general | 49 |
| safety | 42 |
| medicine | 35 |
| mathematics | 30 |
| agents_and_tool_use | 29 |
| science | 25 |
| software_engineering | 24 |
| knowledge | 21 |
| … | … |
| **giao thông / transportation** | **0** |

**Không một benchmark nào về giao thông.** Gần nhất là SVRPBench — định tuyến xe, không phải dự báo lưu lượng.

Nghĩa là: Stanford AIMS **không thể** cung cấp benchmark đối sánh cho GAP-1. Nó chỉ cung cấp **khung khái niệm** (Subject–Item–Response) và **thư viện đo lường**. Đó là kết luận đúng, và nó ngược với giọng của báo cáo ("tìm kiếm các benchmark trên Stanford AIMS để so chuẩn").

---

## 5. Lỗi phương pháp 3: kế hoạch Parquet không khớp schema AIMS

Báo cáo đề xuất đóng gói thành 4 tệp: `benchmarks.parquet`, `subjects.parquet`, `items.parquet`, `responses.parquet`.

Kiểm catalog: schema thật của AIMS dùng các trường `code, name, categories, items, models, responses, paper, institutions, license, scaleType, saturation, fit, observed, attacks`. Không có tệp `subjects.parquet`/`items.parquet` riêng trong bản crawl — đó là **suy diễn** của báo cáo, không phải schema gốc.

Đóng gói theo 4 tệp tự đặt tên là hợp lý về kỹ thuật, nhưng **không phải "schema chuẩn của Stanford AIMS"** như báo cáo khẳng định. Nên gọi đúng: "một schema quan hệ lấy cảm hứng từ AIMS".

---

## 6. Nếu áp vào công việc hiện tại (LargeST-ByzBench), dùng được gì

| Phần của báo cáo | Dùng được? | Cách dùng |
|---|---|---|
| §1 khảo sát AIMS (270, 8,4M items, 19 categories) | **có** | Trích làm bối cảnh "measurement science cho AI" ở phần related work |
| Khung Subject–Item–Interactor–Response | **có, có sửa** | Đây là cách đặt tên tốt cho ma trận 22.240 run: Subject=aggregator, Item=(attack, ratio, intensity, client count), Response=(MAE, FPR, FNR) |
| §4 IRT/Rasch | **không** | Giả định bị vi phạm; dùng kiểm định ghép cặp đã có trong v3 (Wilcoxon + TOST + Holm) |
| §5 Parquet 4 tệp | **có, có sửa** | Đóng gói 22.240 run theo 4 tệp là hợp lý — nhưng đó là schema tự đặt, không phải "chuẩn AIMS" |
| SVRPBench, FrontierOR, TabArena, KernelBench | **không** | Không liên quan dự báo lưu lượng |
| `agentdojo` (Utility vs ASR) | **có** | Đúng cặp chỉ số RQ1/RQ2 — nên trích |
| `auditing_sabotage_bench` | **có, thận trọng** | Ý tưởng "kiểm toán phá hoại" gần với FPR/FNR, nhưng miền là mã nghiên cứu, không phải gradient |

### 6.1 Ánh xạ đúng cho LargeST-ByzBench

| AIMS | LargeST-ByzBench |
|---|---|
| Subject | 13 ô bộ gộp (không phải 6) |
| Interactor | 14 cấu hình tấn công × 4 tỉ lệ × 3 cường độ |
| Item | phân vùng client (P-A/P-B/P-C) × điều kiện dữ liệu (R0–R4) |
| Trial | 10 seed |
| Response | MAE, FPR, FNR, ASR, wall-clock — **liên tục, không nhị phân hoá** |

Khác biệt then chốt với báo cáo: **không nhị phân hoá**. Dữ liệu liên tục, và câu hỏi là "cái giá bao nhiêu", không phải "đạt/không đạt".

---

## 7. Ba việc nên làm

1. **Đổi đối tượng báo cáo.** Nếu muốn dùng cho GAP-1, viết lại §2–§5 quanh LargeST: bỏ tầng SUMO, bỏ delay/queue, đổi sang MAE/FPR/FNR. Giữ §1.

2. **Bỏ phần IRT, hoặc làm đúng.** Nếu vẫn muốn dùng `torch_measure`, cần: (a) gộp seed vào Trial để mỗi ô có 10 quan sát, (b) dùng mô hình nhiều chiều thay vì Rasch một chiều, (c) giữ Response liên tục. Đây là một bài toán riêng, không phải "một đoạn code mẫu".

3. **Trích `agentdojo` và nêu rõ AIMS không có benchmark giao thông.** Đây là hai sự thật dùng được ngay trong related work: AIMS có khung đo lường trưởng thành nhưng **trống ở miền giao thông** — cùng dạng lập luận với "114 bài trích dẫn LargeST, 0 bài Byzantine".

---

## 8. Bảng kiểm chứng

| Nội dung báo cáo | Kết quả | Nguồn |
|---|---|---|
| 270 benchmarks | **đúng** | `aims_benchmarks_catalog.json` |
| 8.403.704 items | **đúng** | cùng tệp |
| 92.060.497 responses | **đúng** (báo cáo làm tròn 92,1M) | cùng tệp |
| 19 categories, phân bố | **đúng** từng số | cùng tệp |
| 781 subjects | **không tái tạo được** | catalog chỉ có tổng 22.746 |
| 12 benchmark được nêu | **có thật, số khớp** | cùng tệp |
| 7 arXiv ID | **đúng bài** | arXiv API |
| `torch-measure` 0.1.0 | **có thật**, tác giả AIMS Foundations | PyPI |
| 1.950 runs ByzCity | **đúng** | `byzcity_experiment_grid.csv` |
| 10 clients, 6 aggregator, 10 seed | **đúng** | cùng tệp |
| Tầng 2 SUMO trong grid | **sai — không có cột nào** | cùng tệp |
| `df['delay']` trong code mẫu | **sai — KeyError** | cùng tệp |
| AIMS có benchmark giao thông | **sai — 0 cái** | catalog |
