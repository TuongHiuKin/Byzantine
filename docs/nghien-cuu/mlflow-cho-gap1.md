# MLflow cho bản GAP-1 — đo ở ba quy mô

> **Đánh giá MLflow cho ma trận thí nghiệm 375 / 5.145 / 10.290 lần chạy. Kết luận đảo chiều theo quy mô.**
>
> Tác giả: Nguyễn Quang Huy — SE194177 · GVHD: ThS. Lâm Hữu Khánh Phương · Đại học FPT · 10/11/2026

**Bản được phân tích:** proposal GAP-1 của nhóm (05/11/2026), không phải v3 của tôi
**Số đo:** MLflow 3.18.0, file backend, 10/11/2026

---

## 0. Kết luận đảo ngược so với lần trước

Lần trước tôi khuyên dùng MLflow, với ma trận **22.240 lần chạy**. Bản GAP-1 có ma trận **khác hẳn**, và kết luận phải đổi:

| | v3 (của tôi) | GAP-1 (của nhóm) |
|---|---|---|
| Ma trận thiết kế đầy đủ | 22.240 | **5.145** (5 seed) / **10.290** (10 seed) |
| Phương án đang chạy | — | **375** (Phương án A, nộp ICCIES) |
| Số trục | 4 (bộ gộp, tấn công, tỉ lệ, cường độ) | **5** (thêm số client 8/16/32) |
| Số bộ gộp | 13 ô | 7 ô |
| Số tấn công | 14 | 12 |

**Kết luận mới:**

- Ở **375 lần chạy** (Phương án A): **không nên dùng MLflow.** Chi phí tích hợp 3,5 ngày đổi lấy **14 giây** tiết kiệm máy — tỷ lệ 1:7.000. Còn 5 ngày đến hạn nộp.
- Ở **10.290 lần chạy** (làm đầy đủ): **nên dùng**, nhưng phần đáng giá nhất — kiểm tra ma trận đủ — **MLflow không cho**, phải viết dù chọn công cụ nào.

---

## 1. Ma trận GAP-1 lớn hơn bản nháp 375 rất nhiều

Đọc §5.2–5.7 của bản GAP-1:

| Trục | Giá trị trong văn bản | Số mức |
|---|---|---|
| Bộ gộp (§5.6) | FedAvg, Krum, Multi-Krum, Median, Trimmed Mean **× 3 mức β** | **7 ô** |
| Tấn công (§5.5) | 7 mức cập nhật mô hình + 5 mức dữ liệu cảm biến | **12** |
| Số client (§5.2) | 8 / 16 / 32 | **3** |
| Tỉ lệ độc hại (§5.5) | 10 / 20 / 30 / 40 % | 4 |
| Seed (§5.7) | 5 (bất khả thi — xem `45_verify`) | 5 |

**Ma trận thiết kế:** 7 × 12 × 3 × 4 × 5 = **5.040** lần, cộng lưới sạch 105 = **5.145**.

**Phương án A chỉ chạy 375 = 7,3 %.** Cụ thể nó bỏ:
- 2 ô bộ gộp (Trimmed Mean chỉ chạy 1 mức β thay vì 3)
- 7 kiểu tấn công (bỏ toàn bộ 5 kiểu cảm biến + 2 kiểu mô hình)
- **toàn bộ trục số client** (chỉ chạy 16)
- 1 tỉ lệ (bỏ 40 %)

Điều này **không sai** — Phương án A là cắt phạm vi có ý thức để kịp hạn. Nhưng bài nộp phải ghi rõ *"375/5.145 ô, đã bỏ trục client và tầng tấn công cảm biến"*, nếu không người phản biện sẽ tưởng đây là ma trận đầy đủ.

**Riêng trục số client là mất mát lớn.** Đó là trục **duy nhất** kiểm tra được Krum có còn đứng vững khi `n` thay đổi — và Krum cần `n ≥ 2f+3`, nên bỏ trục này là bỏ luôn phần kiểm chứng điều kiện lý thuyết.

---

## 2. Đo ở cả ba quy mô

### 2.1 Chi phí ghi

Đo trên 200 lần chạy đúng hình dạng một ô (7 tag/param, 30 vòng × 3 metric):

| | |
|---|---|
| Trung vị | **120 ms/lần** (p95 = 151 ms) |
| Dung lượng | **2,5 KB** / 17 file |

Ngoại suy:

| Quy mô | Số lần | Chi phí ghi |
|---|---|---|
| Phương án A | 375 | **45 giây** |
| Thiết kế 5 seed | 5.145 | **10,3 phút** |
| Thiết kế 10 seed | 10.290 | **20,6 phút** |

Trên thời gian huấn luyện, đây là **0,01 %** — không bao giờ là lý do để không dùng.

### 2.2 Đối chiếu với CSV — con số quyết định

| Quy mô | Số lần | MLflow ghi | CSV ghi | MLflow quét | CSV đọc |
|---|---:|---:|---:|---:|---:|
| Phương án A | 375 | 45,0 s | **0,0008 s** | 1,57 s | **0,005 s** |
| Thiết kế 5 seed | 5.145 | 617,5 s | 0,004 s | 21,6 s | 0,002 s |
| Thiết kế 10 seed | 10.290 | 1.235 s | **0,008 s** | 43,2 s | **0,004 s** |

MLflow ghi chậm hơn CSV **~50.000 lần**. Nghe khủng khiếp, nhưng phải đọc đúng: 43 giây cho 10.290 lần vẫn **không đáng kể** so với 0,7 h × 10.290 = 300 ngày huấn luyện. Chi phí ghi không phải vấn đề ở bất kỳ quy mô nào.

**Vấn đề nằm ở chỗ khác.**

### 2.3 Việc phân tích tốn bao nhiêu — và nó giống hệt nhau

Tôi chạy đúng phép phân tích mà bài báo cần (bảng mean ± SD ± CI95 theo ô, xếp hạng bộ gộp, so sánh ghép cặp theo seed) trên **cả hai** đường:

| | MLflow | CSV |
|---|---|---|
| Viết | 12,7 s | 14,3 ms |
| Đọc + phân tích | 1,50 s + 22 ms | 2,1 ms + 22,5 ms |
| **Kết quả** | 75 ô, xếp hạng `fedavg → multi_krum → krum → tm0.1 → median` | **giống hệt** |

**Kết quả phân tích giống hệt nhau, đến từng thứ hạng.** Vì sau khi `search_runs` trả về, cả hai đều là một DataFrame pandas. MLflow không giúp gì ở bước này.

### 2.4 Bài toán Phương án A, tính thẳng

```
MLflow: 14,27 giây máy
CSV   :  0,039 giây máy
Chênh : 14,23 giây
Tích hợp MLflow: 3,5 ngày = 100.800 giây
Tỷ lệ: gấp 7.082 lần chi phí so với tiết kiệm
```

Còn **5 ngày** đến hạn ICCIES. Dùng 3,5 ngày trong số đó để tích hợp một công cụ giúp tiết kiệm 14 giây là quyết định sai.

---

## 3. Vậy MLflow cho GAP-1 cái gì mà CSV không có

Không phải hiệu năng. Ba thứ này:

| Thứ | Có giá trị với GAP-1? |
|---|---|
| **Resume sau crash** | **Có** — một lần chạy 0,7 h chết ở vòng 25 thì không phải làm lại |
| **Chụp môi trường mỗi lần chạy** (`python_env.yaml`, `requirements.txt`) | **Có** — đây là yêu cầu tái lập ở §4 mục 4 của bản GAP-1 |
| **Truy vấn nhiều trục không phải viết filter** | Có, nhưng 375 dòng CSV thì `pandas` cũng xong trong 2 ms |
| UI so sánh | **Không** — máy này không dựng được server (Application Control chặn SQLAlchemy) |
| **Kiểm tra ma trận đủ** | **Không có trong MLflow** — xem §4 |

Hai dòng đầu là lý do thật để dùng. Và cả hai đều **không cần 3,5 ngày** — resume là một tham số `run_id`, chụp môi trường là một lời gọi `log_artifact`.

---

## 4. Khoảng trống vẫn nguyên: MLflow không biết ma trận còn thiếu gì

Đo lại trên chính ma trận 10.080 ô:

```
Liệt kê từ thiết kế : 10.080 ô kỳ vọng, hash 8bcaf0fff4b39e4f  (8 ms)
Một lần search_runs : báo 5 run đã có
                      không nói gì về 10.075 ô chưa chạy
Độ đầy đủ           : 0,05%   ← MLflow không tính con số này
```

Với một benchmark, **độ đầy đủ là con số quan trọng nhất** — và nó phải được tính bên ngoài công cụ. Đây là lý do `.csv` không hề thua kém: bạn phải viết phép đối chiếu dù chọn gì.

Hai điều MLflow **không** có, đã kiểm lại:

1. **Không có trạng thái "bị loại".** Krum ở `n = 8, 40 %` vi phạm `n ≥ 2f+3` → phải loại. MLflow chỉ có `FINISHED` / `FAILED` / `KILLED`. Ô bị loại trông **giống hệt** ô chưa chạy. Phải tự đặt `validity=invalid` + `reason`.
2. **Không có API đầy đủ.** Đã nói ở trên.

---

## 5. Khuyến nghị theo từng phương án

### Phương án A — 375 lần, còn 5 ngày

**Đừng dùng MLflow.** Dùng CSV + git.

```python
# mỗi lần chạy ghi một dòng, kèm hash cấu hình và commit
row = dict(aggregator=..., attack=..., clients=..., ratio=..., seed=...,
           final_mae=..., fpr=..., fnr=..., wall_s=...,
           config_hash=sha256(json.dumps(cfg, sort_keys=True).encode())[:16],
           commit=git_rev_parse_head())
pd.DataFrame([row]).to_csv("results.csv", mode="a", header=not exists, index=False)
```

Cộng thêm **một lần** chạy `log_artifact` kiểu gì cũng được nếu muốn chụp môi trường — nhưng ở 375 lần, một file `pip freeze > env.txt` là đủ.

**Việc bắt buộc phải làm, không phụ thuộc công cụ:** sinh manifest 375 ô kỳ vọng từ thiết kế, hash, rồi đối chiếu hai chiều sau khi chạy. Đây là thứ biến 375 dòng CSV thành một benchmark.

### Phương án B — 10.290 lần, 12 tuần

**Dùng MLflow**, vì ba lý do cụ thể:

1. Resume — 10.290 lần chạy, mỗi lần 0,7 h, trong 12 tuần chắc chắn có lần chết giữa chừng.
2. Chụp môi trường — yêu cầu tái lập ở §4.
3. Truy vấn — 12 trục × 7 ô × 3 client = 252 ô, lọc bằng tay trên CSV sẽ sinh code filter không ai test.

Nhưng vẫn phải viết manifest + đối chiếu hai chiều. Thời gian tích hợp thực tế: **1,5 ngày** cho Phương án B, không phải 3,5 — vì không cần phần giảm chiều phức tạp (252 ô, pandas xử lý tức thì).

### Cả hai phương án

**Bắt buộc ghi vào README của artefact:**

```
mlflow==3.18.0
MLFLOW_ALLOW_FILE_STORE=true     # nếu dùng, nếu không mlruns/ không mở được
```

Thiếu dòng thứ hai, người chấm chạy MLflow ≥ 3.0 sẽ **không mở được** thư mục `mlruns/`.

---

## 6. Ba điều chỉnh cho chính bản GAP-1

Ngoài MLflow, ma trận mới làm lộ ba điểm trong văn bản:

1. **Phải khai báo 375/5.145 = 7,3 %.** §6 Phương án A hiện chỉ liệt kê việc, không nói bỏ bao nhiêu phần trăm ma trận. Người phản biện sẽ tự tính và hỏi.

2. **Bỏ trục client là mất phần kiểm chứng lý thuyết.** Krum cần `n ≥ 2f+3`. Nếu chỉ chạy `n = 16`, không kiểm được điều kiện này. Nếu buộc phải cắt, hãy giữ **3 mức client × 2 bộ gộp (Krum, FedAvg) × 1 tấn công × 1 tỉ lệ × 5 seed = 30 lần** — rẻ, và cứu được lập luận.

3. **5 seed vẫn bất khả thi.** Ở 375 lần, đổi sang **10 seed cho ô chính** chỉ thêm 375 lần chạy (12,7 s ghi, nhưng 0,7 h × 375 huấn luyện). Nếu không đổi được seed, phải **bỏ hết ngôn ngữ "p < 0,05"** và chỉ báo cáo mô tả.

---

## 7. Một câu

Với 375 lần chạy và 5 ngày, MLflow là **sai công cụ** — không phải vì nó dở, mà vì ở quy mô đó `pandas` đã làm xong mọi việc nó làm, nhanh hơn 50.000 lần, không cần cài đặt. Với 10.290 lần trong 12 tuần, MLflow **đáng dùng** — nhưng vì resume và chụp môi trường, không vì tốc độ, và phần quan trọng nhất của một benchmark (chứng minh ma trận đủ) thì **vẫn phải tự viết**.

---

## Phụ lục — nguồn

| Nội dung | Tệp |
|---|---|
| Chi phí ghi 120 ms, 2,5 KB, 17 file | kết quả đo MLflow |
| Ngoại suy 375 / 5.145 / 10.290 | cùng tệp, `extrapolated_write` |
| MLflow vs CSV, phân tích giống hệt | kết quả đo MLflow |
| 10.080 ô, hash `8bcaf0ff…`, độ đầy đủ 0,05 % | kết quả đo MLflow, `manifest`/`demo` |
| 375 = 7,3 % của 5.145 | tính từ §5.2–5.7 của bản GAP-1 |
| 5 seed bất khả thi | script phân tích cục bộ |
