# Báo cáo tổng hợp — LargeST-ByzBench

> **Tổng hợp bốn nhánh công việc: kiểm chứng 93 công trình, đề cương v3, đối chiếu bản GAP-1, và đánh giá MLflow.**
>
> Tác giả: Nguyễn Quang Huy — SE194177 · GVHD: ThS. Lâm Hữu Khánh Phương · Đại học FPT · 10/11/2026

**Đề tài:** Benchmark học liên kết chống Byzantine cho dự báo lưu lượng giao thông trên dữ liệu PeMS thật
**Sinh viên:** Nguyễn Quang Huy — SE194177
**Giảng viên hướng dẫn:** ThS. Lâm Hữu Khánh Phương
**Đơn vị:** Đại học FPT
**Ngày:** 10 tháng 11 năm 2026

---

## Tóm tắt

Báo cáo này tổng hợp bốn nhánh công việc: (i) kiểm chứng 93 công trình để xác lập khoảng trống nghiên cứu, (ii) đề cương v3 với ma trận thí nghiệm đầy đủ, (iii) đối chiếu bản đề xuất GAP-1 của nhóm với dữ liệu đã đo, và (iv) đánh giá MLflow cho hai quy mô ma trận khác nhau. Mọi con số trong báo cáo đọc từ tệp log phân tích cục bộ, không tính lại.

Ba kết luận chính. **Thứ nhất**, khoảng trống không phải "chưa ai làm Byzantine-FL cho giao thông" — phát biểu đó bị bác bỏ bởi Vehicular AttestedFL (VTC 2024) — mà là "chưa có benchmark tái lập được". **Thứ hai**, ma trận thí nghiệm của đề cương v3 cần **22.240 lần chạy**, không phải 1.178 như bản trước ghi; ở 0,35 h/lần là **46,3 tuần**, nên phải chạy theo ba tầng. **Thứ ba**, với 375 lần chạy và 5 ngày còn lại, MLflow là sai công cụ; với 10.290 lần chạy trong 12 tuần thì đáng dùng, nhưng phần quan trọng nhất của một benchmark thì nó không cung cấp.

---

## 1. Dữ liệu và kiểm chứng đường cơ sở

### 1.1 Bộ dữ liệu

LargeST San Diego (PeMS District 11), 716 cảm biến vòng, 2017–2021, tái lấy mẫu 15 phút.

| Chỉ số | Giá trị | Nguồn |
|---|---|---|
| Cảm biến | 716 | `01_cleaning_log.json` |
| Số ô dữ liệu (5 phút, 5 năm) | 376.535.808 | cùng tệp |
| Ô khuyết thiếu | 12.326.778 | cùng tệp |
| **Tỷ lệ khuyết thiếu (gộp)** | **3,27 %** | tính từ hai dòng trên |
| Cạnh đồ thị | 18.035 | `02_eda_results.json` |
| Ngưỡng bão hoà PeMS | 999 xe/5ph | `01_cleaning_log.json` |

Khuyết thiếu **không đều giữa các năm**: 2017 = 2,70 %, 2018 = 1,37 %, 2019 = 2,16 %, 2020 = 4,10 %, 2021 = 6,03 %. Báo cáo một con số 3,27 % mà không kèm phân bố sẽ khiến người đọc hiểu sai về độ đồng nhất của dữ liệu.

### 1.2 Cổng kiểm chứng tái lập

Tái lập LargeST phải khớp bảng gốc của bài NeurIPS 2023. Với mô hình HA (Historical Average), 12 chặng:

| | Giá trị |
|---|---|
| HL MAE 2019 đo được | **60,80** |
| HL MAE bài báo công bố | 60,79 |
| Sai lệch | 0,01 |

Sai lệch 0,01 chứng minh pipeline tái lập đúng. Đây là điều kiện cần trước khi mọi kết luận khác có nghĩa.

### 1.3 Sự kiện COVID-19 như phép kiểm tra nội tại

| | Giá trị |
|---|---|
| Lưu lượng trung bình 4/2020 | 128,49 xe/15ph |
| Nền 4/2017–2019 | 250,32 xe/15ph |
| Mức giảm | **−48,67 %** |

Đây là hiệu ứng trôi phân phối lớn nhất trong bộ dữ liệu, và là lý do trục ablate "trôi phân phối" trong đề cương có cơ sở thực nghiệm chứ không phải giả định.

---

## 2. Khoảng trống nghiên cứu

### 2.1 Corpus và thống kê

| Chỉ số | Giá trị |
|---|---|
| Tổng công trình | 93 |
| Giao thông đường bộ | 56 |
| Đường bộ **+** học liên kết | 2 |
| Đường bộ **+** FL **+** Byzantine | **1** |
| Đường bộ + FL + Byzantine + **bất đồng bộ** | **0** |
| Bài báo cáo đồng thời MAE **và** attack-success | **0/93** |

Liên hệ giữa "thuộc nhánh FL" và "quan tâm Byzantine":

| | Giá trị |
|---|---|
| FL đề cập Byzantine | 10/17 = 59 % |
| Ngoài FL đề cập Byzantine | 1/76 |
| χ²(1, N = 93) | 38,71 |
| p | **< .001** |
| φ | 0,688 |
| Odds ratio | 107,1 |

Byzantine là mối quan tâm **nội bộ cộng đồng FL**, chưa thấm vào cộng đồng ứng dụng giao thông. φ = 0,688 là khoảng cách đo được giữa hai cộng đồng.

### 2.1b Kiểm định bộ lọc trước khi dùng con số

Mọi ô trong bảng trên phụ thuộc vào một bộ phân loại, và bộ phân loại phải được đo trước khi tin:

| | Ban đầu | Sau khi sửa |
|---|---|---|
| Precision (lọc "giao thông đường bộ") | — | **0,918** |
| Recall | **0,534** | **1,000** |
| Số bài | — | 56 |

Recall ban đầu 0,534 nghĩa là bộ lọc **bỏ sót gần một nửa** bài giao thông. Nếu báo cáo con số 56 mà không kiểm recall, mọi ô phía sau đều kế thừa lỗi này — và hướng sai là **đánh giá thấp** mức độ đã có công trình, tức làm khoảng trống trông rộng hơn thực tế. Sau khi mã hoá lại theo title + concepts (không theo abstract, vì abstract chứa câu phủ định nêu đúng từ cần loại), precision 0,918 và recall 1,000.

Con số 56 vì thế là **cận dưới** của số bài giao thông thật, không phải con số chính xác.

### 2.2 Phát biểu khoảng trống đã kiểm chứng

Phát biểu tuyệt đối "chưa ai làm Byzantine-FL cho giao thông trên dữ liệu thật" **sai** — Vehicular AttestedFL (VTC 2024) đã làm trên Toronto Downtown, 76 nút giao, 223 route link, chu kỳ 5 phút. Phát biểu "chưa có benchmark Byzantine" cũng **sai** — FLPoison và byzantine-fl-bench đã có, chỉ khác miền.

Khoảng trống đúng:

> **Chưa có đo lường nào cho thấy dị biệt tự nhiên của dữ liệu giao thông thật vi phạm giả định "cập nhật trung thực nằm gần nhau" đến mức nào, và hệ quả lên tỉ lệ loại nhầm và bỏ lọt là bao nhiêu.**

HuddsTrafficFL có cấu trúc benchmark nhưng dùng SUMO; Vehicular AttestedFL có dữ liệu thật nhưng không phải benchmark. **Giao của hai tập này rỗng.**

### 2.3 Bằng chứng mạnh nhất đến từ đối thủ gần nhất

HuddsTrafficFL (Knowledge-Based Systems, 2026) tự nêu bốn tiêu chí mà một benchmark Byzantine-FL cho giao thông phải có, khi phê bình các benchmark trước. Đây là dạng khoảng trống dễ bảo vệ nhất: **đối thủ tự đặt ra tiêu chí, và đề tài đáp ứng đúng tiêu chí còn thiếu** — không phải tôi suy ra tiêu chí từ ngoài.

### 2.4 Câu hỏi RQ2 đã được trả lời một phần từ 2022

Karimireddy và cộng sự (ICLR 2022) đã chứng minh các bộ gộp Byzantine **gãy dưới dữ liệu dị biệt ngay cả khi không có kẻ tấn công**. Vì thế RQ2 không còn là "có gãy không" mà phải là **"gãy bao nhiêu, trên client nào"** — và mới đo trên dữ liệu tổng hợp, chưa ai đo trên giao thông thật.

---

## 3. Thiết kế thí nghiệm của đề cương v3

### 3.1 Phân vùng client

Trong 10 cột metadata của `sd_sensors_716.csv`, `District`, `County` và `Type` đều là hằng số. Chỉ `Fwy` (26 giá trị) và toạ độ là trục chia khả dụng.

| Cách chia | EMD min | median | p90 | max |
|---|---|---|---|---|
| Theo hành lang (26 nhóm) | 4,1 | **86,4** | 193,3 | 307,4 |
| IID ngẫu nhiên (26 nhóm) | 5,2 | 22,6 | 43,9 | 74,1 |

**Tỉ lệ median = 3,81×.** Chia theo hành lang tạo dị biệt lớn gần bốn lần IID, và đo được **trước khi chạy thí nghiệm nào**. Đây là cổng kiểm tra: nếu EMD median < 2× IID, dữ liệu không đủ dị biệt và phải chuyển sang GBA/CA.

Cơ chế cụ thể: lưu lượng trung bình I15-N là 414,6 xe/15ph, SR11-E chỉ 23,1 — chênh **18×**. Client I15-N có update magnitude lớn gấp 18 lần, nên median sẽ coi nó là outlier.

### 3.2 Ma trận và khối lượng chạy

| Thành phần | Phép tính | Số lần |
|---|---|---|
| Ma trận tấn công | 13 ô × 14 tấn công × 4 tỉ lệ × 3 cường độ × 10 seed | 21.840 |
| Lưới sạch | 13 × 10 seed | 130 |
| Ablation R0–R4 | 5 × 10 × 3 bộ gộp | 150 |
| Tập con STGCN | 3 × 2 × 2 × 10 | 120 |
| **Tổng** | | **22.240** |

**13 ô tham số, không phải 9**: FedAvg chạy hai biến thể có/không trọng số, Krum chạy hai biến thể *f* oracle và *f* ước lượng sai, Trimmed Mean chạy ba mức β.

Hệ quả thời gian — rủi ro lớn nhất của đề tài:

| Tốc độ | 22.240 lần cần |
|---|---|
| 0,35 h/lần | **46,3 tuần** |
| 0,7 h/lần | **92,7 tuần** |

Không vừa 12 tuần. Vì thế kế hoạch chia ba tầng, trong đó **Tầng 1 = 2.220 lần, 4,6 tuần**, đủ trả lời RQ1, RQ2 và RQ4.

### 3.3 Thiết kế thống kê

Số seed phải tính ngược từ kiểm định. Wilcoxon signed-rank chính xác hai phía có p nhỏ nhất = 2/2ⁿ:

| n seed | p nhỏ nhất |
|---|---|
| 5 | **0,0625** — không đạt 0,05 |
| 10 | 0,00195 |

Với Holm cho m = 10 phép so sánh, ngưỡng là 0,005 — nên 10 seed cho ô chính là mức tối thiểu, không phải lựa chọn thận trọng.

Kendall τ để so thứ hạng giữa dữ liệu thật và mô phỏng có độ phân giải thấp: với 5 bộ gộp chỉ nhận **11 giá trị phân biệt**; với 9 bộ gộp là **37**. Đây là lý do thiết kế dùng 9 bộ gộp chứ không phải 5.

---

## 4. Đối chiếu bản GAP-1 của nhóm

### 4.1 Bốn con số dữ liệu

| Bản GAP-1 viết | Đo từ artefact | Kết luận |
|---|---|---|
| khuyết thiếu 3,27 % | 3,27 % (gộp 5 năm) | **đúng chính xác** |
| 18.035 cạnh | 18.035 | **đúng chính xác** |
| 4/2020 giảm 48,7 % | −48,67 % | **đúng** |
| Huddersfield 382 nút giao | 0 lần trong abstract KBS và Zenodo | **không có trong bài** |

Về con số 382: cả bản KBS (`10.1016/j.knosys.2026.117003`, 2.608 ký tự) và bản Zenodo (`10.5281/zenodo.22707916`) đều **không chứa chuỗi "382"**. Bài nói **"292 clients"** và **"junction-level traffic behaviour"** nhưng không nêu số nút giao. Cách sửa: bỏ "382 nút giao", thay bằng "292 client" — con số này có trong cả hai nguồn và mạnh hơn vì là đơn vị FL thật.

### 4.2 Ma trận GAP-1 lớn hơn bản nháp

| Trục | Giá trị theo văn bản | Số mức |
|---|---|---|
| Bộ gộp | 5 cơ chế, Trimmed Mean × 3 β | **7 ô** |
| Tấn công | 7 mức mô hình + 5 mức cảm biến | **12** |
| Số client | 8 / 16 / 32 | **3** |
| Tỉ lệ độc hại | 10 / 20 / 30 / 40 % | 4 |

Ma trận thiết kế: 7 × 12 × 3 × 4 × 5 = 5.040, cộng lưới sạch 105 = **5.145** (5 seed) hoặc **10.290** (10 seed).

**Phương án A chạy 375 = 7,3 %.** Nó bỏ 2 ô bộ gộp, 7 kiểu tấn công, 1 tỉ lệ, và **toàn bộ trục client**. Riêng trục client là mất mát lớn nhất: đó là trục duy nhất kiểm chứng được Krum có còn đứng khi *n* thay đổi, mà Krum cần *n ≥ 2f + 3*.

### 4.3 Thời hạn

Bản viết ngày 05/11 nói "còn khoảng 10 ngày" — đúng lúc đó. Hôm nay 10/11, còn **5 ngày**. Phương án A dành 08–11/11 cho ma trận lõi, tức **hôm nay là ngày cuối**.

Khối lượng Phương án A là 375 lần chạy:

| Tốc độ | Tổng | Vừa 4 ngày? |
|---|---|---|
| 0,35 h/lần | 5,5 ngày | không |
| 0,7 h/lần | 10,9 ngày | không |

Cộng thời gian viết 12–15 trang LNCS, Phương án A không khả thi trừ khi cắt xuống khoảng 36 lần chạy hoặc chạy trên tập con cảm biến.

---

## 5. Đánh giá MLflow

### 5.1 MLflow thực chất là gì

Đọc từ source 3.18.1.dev0 (6.721 file trong package, 1.278 file `.py`):

| Subpackage | Số file |
|---|---|
| `server` (UI React + REST) | 5.122 |
| `genai` | 234 |
| `store` | 204 |
| `tracking` | 47 |

`genai` gấp **5,0 lần** `tracking` — trọng tâm đã chuyển sang tracing LLM. Và grep toàn package: **0 file** chứa `federated`, `num_clients`, `federated_round`, hoặc `byzantine`. MLflow **không có khái niệm** học liên kết; vòng FL là code của người dùng.

### 5.2 Ba mặc định của bản 3.x phá vỡ hướng dẫn cũ

1. **File backend từ chối chạy.** Cần `MLFLOW_ALLOW_FILE_STORE=true`, nếu không `mlruns/` không mở được trên MLflow ≥ 3.0. Đây là rủi ro trực tiếp cho artefact nộp kèm.
2. **Model cây bị skops chặn.** RandomForest/XGBoost/LightGBM bị từ chối đến khi khai `skops_trusted_types=["sklearn.tree._tree.Tree"]`.
3. **Trace ghi bất đồng bộ.** Đọc ngay sau khi span đóng trả `None` kèm thông báo "span data is corrupted" — thực chất là race condition, phải `flush_trace_async_logging()`.

### 5.3 Chi phí đo được

Một ô đầy đủ (7 tag/param, 30 vòng × 3 metric):

| | |
|---|---|
| Ghi mỗi lần | **120 ms** (p95 = 151 ms) |
| Dung lượng | **2,5 KB** / 17 file |
| Quét toàn bộ | ~4,2 ms/lần |

Ngoại suy chi phí ghi:

| Quy mô | Số lần | Chi phí ghi |
|---|---|---|
| Phương án A | 375 | 45 giây |
| Thiết kế 5 seed | 5.145 | 10,3 phút |
| Thiết kế 10 seed | 10.290 | 20,6 phút |

Trên thời gian huấn luyện, đây là 0,01 % — không bao giờ là lý do để không dùng.

### 5.4 Khoảng trống quyết định

**MLflow không có API kiểm tra tính đầy đủ của ma trận.** Đo trên 10.080 ô:

| | |
|---|---|
| Liệt kê từ thiết kế | 10.080 ô, hash `8bcaf0fff4b39e4f` (8 ms) |
| Một `search_runs` | báo 5 run đã có |
| Số ô chưa chạy mà nó báo | **0** — im lặng về 10.075 ô |
| Độ đầy đủ | 0,05 % (MLflow không tính) |

Với paper thường điều này không sao. Với benchmark thì chí mạng: tuyên bố trung tâm là "ma trận đã chạy đủ", và kết luận "Krum gãy ở 30 %" có thể chỉ vì ô đó **chưa bao giờ chạy**.

Cùng vấn đề với ô bị loại: MLflow chỉ có `FINISHED` / `FAILED` / `KILLED`, không có trạng thái "bị loại theo lý thuyết". Ô vi phạm *n ≥ 2f + 3* trông **giống hệt** ô chưa chạy.

### 5.5 Khuyến nghị theo quy mô

Hai phép đo khác cơ sở, phải tách rõ:

- **Ngoại suy chỉ riêng phần ghi**, hình dạng ô đầy đủ (30 vòng × 3 metric): 120 ms × 375 = **45,0 s**; 5.145 lần = 10,3 phút; 10.290 lần = 20,6 phút.
- **Đo đầu-cuối thật** trên một ô đơn giản hơn (một metric cuối, không ghi từng vòng): MLflow **14,27 s** (12,7 ghi + 1,5 quét + 22 ms phân tích) so với CSV **0,039 s**.

| | MLflow | CSV | Chênh |
|---|---|---|---|
| Ghi, ô đầy đủ (ngoại suy, 375 lần) | 45,0 s | — | — |
| Đầu-cuối, ô đơn giản (đo thật, 375 lần) | 14,27 s | 0,039 s | 14,23 s |
| Kết quả phân tích | 75 ô, thứ hạng `fedavg → multi_krum → krum → tm0.1 → median` | **giống hệt** | 0 |
| Thời gian tích hợp | 3,5 ngày = 100.800 s | ~0 | **7.082×** |

Con số quyết định là dòng cuối: bỏ 100.800 giây công để tiết kiệm 14,23 giây máy. Với Phương án A còn 5 ngày, đây là quyết định sai.

Với Phương án B (10.290 lần, 12 tuần), phép so đổi chiều: 20,6 phút ghi là không đáng kể, và hai thứ MLflow cho mà CSV không cho — **resume sau crash** và **chụp môi trường** — trở nên đáng giá. Khuyến nghị: **dùng MLflow**, tích hợp 1,5 ngày.

Với Phương án B: dùng MLflow vì hai lý do cụ thể — **resume sau crash** (đã đo: mở lại bằng `run_id`, 6 điểm liên tục) và **chụp môi trường mỗi lần chạy** (`python_env.yaml` chính là yêu cầu tái lập). Ghi song song cũng đã kiểm: 4 worker, cả 4 exit 0, không mất run nào.

Giới hạn phải khai báo: trên máy này **không dựng được `mlflow server`** vì Application Control chặn DLL của SQLAlchemy (server import SQLAlchemy vô điều kiện qua `_search_limits.py`). Client, tracking, registry và tracing đều chạy đủ — đây là giới hạn môi trường, không phải lỗi MLflow.

### 5.6 Ngưỡng vận hành cần biết

| | |
|---|---|
| `max_results` tối đa | **50.000** |
| `search_runs` lọc theo | **giá trị cuối cùng** của metric, không theo lịch sử |
| Đếm bằng `search_runs` trong vòng lặp | O(N²) — trông như treo, không phải lỗi |

---

## 6. Bằng chứng về tấn công ở mức cảm biến

Đo trên một cảm biến thật của bộ dữ liệu (ID 1116061), dùng bộ kiểm tra chất lượng 4 luật:

| Tấn công | Δ điểm chất lượng | Hệ số MAE |
|---|---|---|
| Nhân ×3 | **+0,0** | **3,00×** |
| Nhiễu ngẫu nhiên | 100,0 | 11,29× |
| Báo 0 xe | — | 0,00× |

Tấn công nhân ×3 làm sai số dự báo tăng gấp ba lần nhưng **không thay đổi bất kỳ tín hiệu chất lượng dữ liệu nào** (Δ = +0,0 trên thang 100). Trong khi nhiễu ngẫu nhiên — dễ phát hiện hơn nhiều — lại bị chấm điểm 100,0. Đây là bằng chứng định lượng cho luận điểm: kiểm tra chất lượng thông thường không phát hiện được tấn công có chủ đích.

Tỉ lệ neighbour-ratio z-score: nhân ×2 cho z = 3,6; ×3 cho z = 7,3; ×1,5 cho z = 1,8. Ngưỡng phát hiện thông thường (z = 3) bỏ lọt mức ×1,5 hoàn toàn.

---

## 7. Kiểm chứng và giới hạn

### 7.1 Trạng thái kiểm chứng

| Bộ kiểm | Số phép | Kết quả |
|---|---|---|
| Thiết kế kỹ thuật | 44 | đạt |
| Đề cương v3 | 118 | đạt |
| Cổng hợp nhất v3 | 17 | đạt |
| Khối lượng chạy | 18 | đạt |
| Đối chiếu GAP-1 | 33 | đạt |
| MLflow — phân tích | 39 | đạt |
| MLflow — báo cáo cho đồ án | 32 | đạt |
| MLflow — báo cáo cho GAP-1 | 45 | đạt |

Mỗi bộ kiểm chạy lại được và trả mã lỗi khác 0 khi có sai lệch. Số liệu trong báo cáo này đọc từ `report_data.json`, sinh bởi `46_build_report_data.py`.

### 7.2 Điều không xác minh được

| Hạn chế | Ảnh hưởng |
|---|---|
| 3 bài ScienceDirect trả HTTP 403 (BRAFed, AsyncDefender, FedPSA) | Chỉ xác minh DOI/metadata qua OpenAlex, không đọc được toàn văn |
| FedASTAM không có bản ghi trong OpenAlex | Trích arXiv `2405.13090`; **không** khẳng định venue Applied Sciences |
| Rà soát chưa tra có hệ thống Scopus/IEEE Xplore | Corpus 93 bài là qua web, Connected Papers và trích dẫn LargeST |
| `mlflow server` không dựng được trên máy này | Chỉ đo được API lập trình, không đo UI |
| LargeST là đường cao tốc, không có đèn tín hiệu | Không kết luận được gì về điều khiển đèn |

### 7.3 Điều đã sửa so với các bản trước

| Sai | Đúng | Cách phát hiện |
|---|---|---|
| Ma trận cần 1.178 lần chạy | **22.240** | `44_verify_run_volume.py` |
| 12×4×6×4×3 = 3.474 | **3.456** | cùng script |
| 1.178 lần = 21 tuần | **2,5 tuần** | cùng script |
| Huddersfield 382 nút giao | không có trong bài | đọc abstract KBS + Zenodo |
| 5 seed đạt p < 0,05 | p nhỏ nhất = **0,0625** | `45_verify_doi_chieu.py` |

---

## 8. Việc cần làm

### 8.1 Trước hạn ICCIES 15/11 (còn 5 ngày)

1. **Bỏ "382 nút giao", thay bằng "292 client"** — 1 phút, chặn câu hỏi về nguồn.
2. **Khai báo 375/5.145 = 7,3 %** trong §6 Phương án A — người phản biện sẽ tự tính nếu không khai.
3. **Đổi 5 seed → 10 seed cho ô chính**, hoặc bỏ hết ngôn ngữ "p < 0,05" và chỉ báo cáo mô tả.
4. **Trình bày phép tính 375 × giờ/lần** và xin thầy quyết cắt phạm vi.
5. **Không tích hợp MLflow** — dùng CSV + manifest hash.

### 8.2 Nếu theo Phương án B (12 tuần)

1. Sinh manifest kỳ vọng từ code thiết kế, hash, đối chiếu hai chiều sau khi chạy — đây là thứ biến 10.290 run thành một benchmark.
2. Dùng MLflow với `MLFLOW_ALLOW_FILE_STORE=true`, ghim `mlflow==3.18.0`.
3. Giữ tối thiểu 3 mức client × 2 bộ gộp × 1 tấn công × 1 tỉ lệ × 5 seed = 30 lần nếu buộc cắt trục client — rẻ, và cứu được lập luận *n ≥ 2f + 3*.

### 8.3 Chưa có số, cần đo

| Việc | Vì sao cần |
|---|---|
| Thời gian một lần chạy thật | Mọi ước lượng tuần trong báo cáo dùng 0,35–0,7 h/lần, **chưa đo thật** |
| Unit test 9 bộ gộp đối chiếu ByzFL | Cổng tuần 2 của đề cương |
| Đọc lại HDF5 gốc lấy NaN thật | Nếu muốn giữ trục khuyết thiếu ở R3 |

---

## Tài liệu tham khảo

Blanchard, P., El Mhamdi, E. M., Guerraoui, R., & Stainer, J. (2017). Machine learning with adversaries: Byzantine tolerant gradient descent. In *Advances in Neural Information Processing Systems 30*.

Karimireddy, S. P., He, L., & Jaggi, M. (2022). Byzantine-robust learning on heterogeneous datasets via bucketing. In *International Conference on Learning Representations*.

Liu, X., Xia, Y., Chen, J., Yang, Q., & Liu, Y. (2023). LargeST: A benchmark dataset for large-scale traffic forecasting. In *Advances in Neural Information Processing Systems 36, Datasets and Benchmarks Track*.

McMahan, B., Moore, E., Ramage, D., Hampson, S., & Agüera y Arcas, B. (2017). Communication-efficient learning of deep networks from decentralized data. In *Proceedings of the 20th International Conference on Artificial Intelligence and Statistics* (PMLR 54, pp. 1273–1282).

Nguyen, J., Malik, A., Zhan, H., Yousefpour, A., Rabbat, M., Malek, M., & Hosseini, R. (2022). Federated learning with buffered asynchronous aggregation. In *Proceedings of the 25th International Conference on Artificial Intelligence and Statistics* (PMLR 151).

Shejwalkar, V., & Houmansadr, A. (2021). Manipulating the Byzantine: Optimizing model poisoning attacks and defenses for federated learning. In *Proceedings of the Network and Distributed System Security Symposium*.

Xie, C., Koyejo, O., & Gupta, I. (2019). Fall of empires: Breaking Byzantine-tolerant SGD by inner product manipulation. In *Proceedings of the 35th Conference on Uncertainty in Artificial Intelligence* (PMLR 115).

Yin, D., Chen, Y., Kannan, R., & Bartlett, P. (2018). Byzantine-robust distributed learning: Towards optimal statistical rates. In *Proceedings of the 35th International Conference on Machine Learning* (PMLR 80, pp. 5650–5659).

Baruch, G., Baruch, M., & Goldberg, Y. (2019). A little is enough: Circumventing defenses for distributed learning. In *Advances in Neural Information Processing Systems 32*.

Babar, F. F., Khan, S., & Parkinson, S. (2026). HuddsTrafficFL: A benchmark testbed and dataset for Byzantine-robust federated learning in urban traffic systems. *Knowledge-Based Systems*. https://doi.org/10.1016/j.knosys.2026.117003

---
