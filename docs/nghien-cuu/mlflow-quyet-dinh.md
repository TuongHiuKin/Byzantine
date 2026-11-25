# MLflow cho LargeST-ByzBench — đo ở đúng quy mô, và khuyến nghị

*Quyết định công cụ theo dõi thí nghiệm · đo 25/11/2026 · MLflow 3.18.0, Ryzen 7 6800H*

!!! info "Câu hỏi"
    "Có nên dùng MLflow cho 2.220–22.240 lần chạy của đề tài này không?" Không trả lời bằng tài liệu nhà sản xuất. Trang này cài MLflow, ghi **2.220 lần chạy thật × 34 chỉ số**, đo tốc độ, dung lượng, độ trễ truy vấn — rồi đo ba lựa chọn nhẹ hơn ở **cùng quy mô, cùng chỉ số**, để so sánh có cơ sở.

---

## 0. Khuyến nghị trước

**Dùng MLflow — nhưng không phải để ghi mỗi lần chạy.**

| Vai trò | Công cụ | Lý do đo được |
|---|---|---|
| **Ghi kết quả từng lần chạy** | **CSV/SQLite tự ghi** | MLflow chậm **3.435 lần** ở việc này |
| **Xem, so sánh, dựng UI** | **MLflow** | Ghi 2.220 lần vẫn chỉ **2,5 phút**, và UI là thứ CSV không có |

Nói cách khác: **ghi bằng CSV, xem bằng MLflow.** Ghi chậm không phải vấn đề lớn (2,5 phút cho cả Tầng 1), nhưng 3.435 lần là con số đáng biết trước khi ai đó đặt `mlflow.log_metrics` vào trong vòng lặp huấn luyện.

**Và MLflow không nên là nơi lưu kết quả chính.** Kết quả chính phải là **tệp trên đĩa, có hash, đọc lại được không cần MLflow** — đúng cách Malkani làm với 84.344 bản ghi. MLflow là lớp xem, không phải nguồn sự thật.

---

## 1. Quy mô đo — lấy từ đề cương, không phải giả định

| Hạng mục | Giá trị | Nguồn |
|---|---|---|
| Tầng 1 (bắt buộc) | **2.220** lần chạy | v3 §3.10 |
| Tầng 2 | 7.820 | `scale_test_cases.json` |
| Tầng 3 | 11.730 | `scale_test_cases.json` |
| Ma trận đầy | **22.240** | v3 Phụ lục B |
| Chỉ số mỗi lần chạy | **34** | v3 §3.8 / F.3 |
| Tham số mỗi lần chạy | **12** | v3 §3.6 |
| **Tổng điểm dữ liệu (Tầng 1)** | **75.480** | 2.220 × 34 |

34 chỉ số gồm: 4 độ chính xác · **22 MAE từng client** · worst-client · p90 · 5 phòng thủ (điểm gãy, ASR, utility retention, FPR, FNR) · wall-clock.

Con số 34 quan trọng: **22 trong 34 chỉ số là mức client**. Đó là lý do phải có nơi lưu dạng bảng, không chỉ một con số tổng.

---

## 2. MLflow đo được gì

### 2.1 Ghi

| Chỉ số | Giá trị |
|---|---|
| Ghi 2.220 lần chạy × 34 chỉ số | **152,5 s** |
| Mỗi lần chạy | **68,7 ms** |
| Tốc độ | **14,6 lần/giây** |
| Dung lượng DB | **37,4 MB** (**17.666 byte/lần chạy**) |

### 2.2 Đọc

| Truy vấn | Thời gian |
|---|---|
| `search_runs` lấy **toàn bộ** 2.220 dòng | **3.260 ms** |
| Lọc `aggregator=krum` và `ratio=0.2` (555 dòng) | **922 ms** |
| Lọc theo `attack` (1.000 dòng) | **1.621 ms** |
| Lọc theo `metrics.fpr > 20` (1.000 dòng) | **1.509 ms** |
| Sắp xếp top-100 theo FPR | **701 ms** |
| Chuyển sang pandas DataFrame | **13 ms** |

### 2.3 Ngoại suy sang ma trận đầy

| | Ở 22.240 lần chạy |
|---|---|
| Thời gian ghi | **0,42 h** (~25 phút) |
| Dung lượng DB | **375 MB** |

**Cả hai đều chấp nhận được.** MLflow không sụp ở quy mô này.

---

## 3. Nhưng — so với lựa chọn nhẹ hơn, ở cùng quy mô

Cùng 2.220 lần chạy, cùng 34 chỉ số, cùng 12 tham số:

| Cách ghi | ms/lần chạy | Dung lượng | Phụ thuộc |
|---|---|---|---|
| **CSV append** | **0,02** | 0,84 MB | 0 |
| **SQLite trực tiếp** (stdlib) | **0,02** | 0,84 MB | 0 |
| MLflow (gộp 50 lần/1 run) | 29,2 | — | 70 MB |
| **MLflow (1 run/lần)** | **68,7** | **37,4 MB** | 70 MB |

**MLflow chậm 3.435 lần** so với ghi CSV; DB của nó **lớn 44 lần** cho cùng dữ liệu.

Con số 0,02 ms/run đã được kiểm chứng không phải lỗi đo: CSV có **2.220 dòng dữ liệu thật**, SQLite có **2.220 dòng × 47 cột** đọc lại được. Ghi tuần tự được đệm ở tầng OS — không `fsync` mỗi dòng, nên nhanh.

**Vì sao MLflow chậm:** mỗi `log_metrics` mở transaction SQL, ghi từng chỉ số thành một dòng trong bảng `metrics`, cập nhật index. 34 chỉ số = 34 lần ghi DB **cho mỗi lần chạy**. Gộp 50 lần vào một run giảm còn 29,2 ms nhưng **mất danh tính từng lần chạy** — vô dụng cho phân tích.

---

## 4. Những gì MLflow làm được mà CSV không

Không phải mọi thứ đều là tốc độ. Đây là phần **không đo bằng ms**:

| Khả năng | CSV | MLflow |
|---|---|---|
| UI so sánh run song song | không | **có** |
| Lọc + sắp xếp bằng SQL | tự viết | **có sẵn** |
| Lưu artifact (hình, mô hình) theo run | tự quản | **có sẵn** |
| Trực quan hoá metric theo bước | không | **có** |
| Chạy lại một run từ tham số đã ghi | tự viết | **có sẵn** |
| Đọc được **không cần** thư viện | **có** | không |
| KiB-level, không phụ thuộc | **có** | 70 MB |
| Ổn định 5 năm (không đổi schema) | **có** | phụ thuộc phiên bản |

Dòng cuối là quan trọng cho một luận văn: **CSV không bao giờ làm hỏng dữ liệu của bạn khi ai đó nâng cấp thư viện.** MLflow thì có thể — SQLite schema của nó đã đổi qua các phiên bản.

---

## 5. Một giới hạn cứng cần biết trước

`search_runs(max_results=...)` **không nhận quá 50.000**. Ma trận đầy là 22.240 nên vẫn vừa, nhưng bất kỳ ai viết "lấy hết để phân tích" phải biết mức trần này:

```
mlflow.exceptions.MlflowException: Invalid value 1000000 for parameter
'max_results'. It must be at most 50000
```

Tôi gặp lỗi này khi đo. Nó ghi trong mã nguồn MLflow chứ không nổi bật trong tài liệu — nên đáng ghi lại.

Ngoài ra: `search_runs` trả **list** nếu pandas không import được, **DataFrame** nếu có. Code phân tích phải xử lý cả hai, hoặc ghim pandas. Tôi gặp lỗi này luôn khi đo (`TypeError: list indices must be integers`).

---

## 6. Cách dùng đề nghị

### 6.1 Nguồn sự thật: CSV có hash

Mỗi lần chạy ghi **một dòng** vào CSV, theo mô hình Malkani ghi 84.344 bản ghi:

```
03_outputs/runs/
  tier1.csv                  # một dòng / lần chạy, 47 cột
  tier1.sha256               # hash để chứng minh không sửa
  artifacts/<run_id>/        # hình, mô hình của run đó
```

`run_id` dạng `t1_krum_alie_z1_r20_i50_s03` — đọc được bằng mắt, không cần tra cứu.

### 6.2 Lớp xem: đẩy CSV sang MLflow **sau khi chạy xong**

```python
# sau khi tier1.csv đã đóng và hash đã ghi
import mlflow, pandas as pd
mlflow.set_tracking_uri("sqlite:///03_outputs/mlflow.db")
df = pd.read_csv("03_outputs/runs/tier1.csv")
with mlflow.start_run(run_name="tier1-import"):     # MỘT run cho cả lô
    for _, r in df.iterrows():
        mlflow.log_metrics({f"fpr__{r.run_id}": r.fpr})
```

Cách này có cả hai: **CSV là nguồn sự thật**, MLflow chỉ để xem. Nếu MLflow hỏng hay nâng cấp làm đổi schema, dữ liệu vẫn nguyên.

### 6.3 Nếu vẫn muốn ghi trực tiếp bằng MLflow

Thì ít nhất:
- **Gộp metric vào một lần gọi** (`log_metrics(dict)`, không gọi 34 lần) — tôi đã làm vậy, và 68,7 ms là **sau khi** đã gộp.
- **Không ghi trong vòng huấn luyện**, chỉ ghi cuối mỗi lần chạy.
- Chấp nhận 25 phút để ghi cả ma trận đầy — chấp nhận được nếu chạy qua đêm.

---

## 7. Trả lời trực tiếp

**"Có nên dùng MLflow không?"**

**Có, nhưng là lớp xem chứ không phải nơi lưu.** Ở quy mô 2.220–22.240 lần chạy, MLflow **không sụp** (0,42 h ghi, 375 MB cho ma trận đầy) và UI của nó là thứ CSV không thay được khi bạn cần so 9 bộ gộp × 14 tấn công × 4 tỉ lệ bằng mắt.

Nhưng **đừng để nó thành nguồn sự thật**. Nó chậm 3.435 lần, DB lớn 44 lần, phụ thuộc 70 MB, và schema có thể đổi giữa các phiên bản. Một luận văn cần dữ liệu đọc được sau 5 năm — CSV đảm bảo điều đó, MLflow không.

**Chi phí của khuyến nghị này:** 0 đồng, 0 dòng phụ thuộc thêm, và khoảng 30 dòng code để đẩy CSV sang MLflow khi cần xem.

---

## Phụ lục — Nguồn số

| Số | Tệp | Script |
|---|---|---|
| 2.220 × 34, 68,7 ms/run, 37,4 MB, 3.260 ms search | `mlflow_bench.json` | `74_mlflow_bench.py` |
| CSV 0,02 ms, SQLite 0,02 ms, 2.220 dòng × 47 cột | `tracking_alts.json` | `75_tracking_alts.py` |
| Trần `max_results` = 50.000 | mã nguồn MLflow 3.18.0 | gặp khi chạy `74` |
| 2.220 / 7.820 / 11.730 / 22.240 lần chạy | `14_RESEARCH_PROPOSAL_V3.md` §3.10, Phụ lục B | — |
| Mặc định SQLite từ 3.7.0 | [MLflow self-hosting docs](https://mlflow.org/docs/latest/self-hosting) | — |

**Kiểm chứng chéo:** 2.220 × 68,7 ms = 152,5 s — khớp lần đo thật. Số dòng CSV (2.220) và SQLite (2.220 × 47 cột) đọc lại từ đĩa, không phải đếm trong bộ nhớ. Cả hai lần chạy `74` (152,5 s và 166,2 s) đều nằm trong ±9 %, cho thấy phép đo ổn định.
