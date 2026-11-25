# PROTOCOL — LargeST-ByzBench

**Khoá ngày: 25/11/2026.** Mọi luật dưới đây được chốt **trước** khi chạy bất kỳ vòng FL nào.
Thay đổi sau ngày này phải ghi thành **amendment có ngày riêng**, không sửa lặng lẽ.

Lý do file này tồn tại: v3 có câu "kế hoạch phân tích chốt trước khi chạy, ghi ngày", nhưng các luật nằm rải trong 22 trang văn xuôi và **chưa có ngày nào được ghi**. Không có file mang ngày thì "chốt trước" không kiểm chứng được, và mọi lần cắt phạm vi về sau đều đọc như quyết định hậu nghiệm — kể cả khi nó được quyết trung thực.

Trang này là bản công khai của tệp giao thức đã khoá ngày **25/11/2026**. Để hiểu các con số nền, xem [Hạ tầng triển khai](ha-tang-trien-khai.md) và [Chấm bộ tiêu chí 24/11](cham-tieu-chi-24-11.md).

---

## 1. Đơn vị công việc — định nghĩa "một vòng"

> **Một vòng = 22 client (tham gia đầy đủ, không lấy mẫu) × 3 epoch cục bộ × 32 bước mini-batch × batch 256.**

Đây là **luật bắt buộc**, không phải gợi ý. Không client nào duyệt toàn bộ dữ liệu trong một vòng.

**Vì sao phải chốt:** đo trên máy thật, hai định nghĩa "một vòng" chênh nhau **46 lần**:

| Định nghĩa | Cửa sổ/vòng | Thời gian/vòng |
|---|---|---|
| Duyệt toàn bộ dữ liệu (1 epoch) | 25.072.172 (100 %) | **961 s = 0,267 h** |
| **Lấy mẫu (luật này)** | 540.672 (2,16 %) | **20,7 s = 0,0058 h** |

Không ghi câu này thì hai người triển khai ra hai ngân sách chênh 46 lần. Nguồn: log đo cấu hình trên máy thật (giữ trong bản lưu nội bộ).

---

## 2. Luật hội tụ `R_conv`

`R_conv` = **vòng sớm nhất** mà từ đó trở đi, trung bình validation **không bao giờ thấp hơn quá 0,5 điểm** so với mức bình ổn cuối (trung bình các vòng 151–200).

| Tham số | Giá trị chốt |
|---|---|
| Số vòng tối đa | **200** |
| Mức bình ổn | trung bình MAE validation các vòng 151–200 |
| Dung sai | **0,5 điểm MAE** |
| Tập dùng để chốt | validation = 6 tháng cuối 2019 |
| Số seed để chốt | **10** |
| Áp dụng cho | GRU và MLP; STGCN chốt riêng |

**Luật chốt giá trị:** `R_conv` = **trung vị** của 10 lần đo, làm tròn lên bội số của 5.

**Vì sao phải chốt:** điểm gãy được định nghĩa là "tỉ lệ độc hại nhỏ nhất mà MAE vượt **110 % MAE FedAvg sạch**". Nếu mô hình chưa hội tụ, MAE còn đang giảm và con số 110 % đo trên một điểm bất kỳ của đường cong — đổi số vòng là đổi kết luận.

**Trạng thái hiện tại:** **CHƯA ĐO.** `R_conv` chưa có giá trị. Luật đã chốt, phép đo chưa chạy. Khi có giá trị, ghi vào bảng dưới và **không sửa luật**:

| Mô hình | `R_conv` | Ngày đo | Nguồn |
|---|---|---|---|
| GRU | *(chưa đo)* | | |
| MLP | *(chưa đo)* | | |
| STGCN | *(chưa đo)* | | |

---

## 3. FedAvg nào là mẫu số của điểm gãy

> **Điểm gãy so với FedAvg CÓ TRỌNG SỐ theo số mẫu.** Biến thể không trọng số báo cáo ở bảng phụ, không dùng làm mẫu số.

**Vì sao:** hai biến thể FedAvg chênh nhau **+3,4 / +0,6 / +5,2 điểm** trên ba bộ dữ liệu ở Malkani (2026). Với biên 110 %, sai 5 điểm là **dịch điểm gãy đi một mức tỉ lệ**.

---

## 4. Thiết kế thống kê

| Hạng mục | Luật |
|---|---|
| Số seed ô chính | **10** |
| Số seed ô phụ | 3–5, **chỉ báo cáo mô tả, không kiểm định** |
| Họ so sánh chính | **m = 10** (9 bộ gộp so FedAvg, 1 so Local-only) |
| Kiểm định | Wilcoxon signed-rank ghép cặp theo seed |
| Hiệu chỉnh | **Holm** trên cả họ m = 10 |
| Tương đương | **TOST, biên ±10 % MAE** |
| Khoảng tin cậy mức client | bootstrap theo cụm (seed × client) |
| Ngưỡng ý nghĩa | p < 0,05 sau Holm |

**Vì sao 10 seed:** Wilcoxon chính xác hai phía có p nhỏ nhất = 2/2^n. Với n = 5, p_min = **0,0625** — không đạt 0,05 dù hiệu ứng lớn đến đâu.

---

## 5. Điều kiện hợp lệ — hai tầng, ghi `invalid` không chạy ngầm

**Tầng 1 — theo số client:**

| Cơ chế | Điều kiện | Ghi chú với n = 22 |
|---|---|---|
| Krum | `n ≥ 2f + 3` | hợp lệ đến **40 %** (cần 21) |
| Bulyan | `n ≥ 4f + 3` | hợp lệ đến **20 %** (cần 19); 30 % cần 31 → **bất khả** |
| Trimmed mean | `n − 2f > 2` | không thoái hoá đến **40 %** |

**Tầng 2 — theo tỉ lệ dữ liệu:** client giữ `> 50 %` tổng trọng số làm weighted median / weighted GeoMed thành *update của chính client đó*. P-A **tự động đạt** (lớn nhất 13,27 %, hai lớn nhất 25,28 %).

**Luật ghi:** ô vi phạm được gắn nhãn `invalid` và **không chạy**. Ô vi phạm theo thiết kế (trimmed mean khi tỉ lệ > β) gắn nhãn `gãy_theo_thiết_kế` và **không trình bày như phát hiện**.

---

## 6. Ngưỡng và chỉ số

| Hạng mục | Luật |
|---|---|
| Điểm gãy | tỉ lệ độc hại nhỏ nhất làm MAE **> 110 %** MAE FedAvg (có trọng số) sạch |
| MAPE | chỉ tính ô có lưu lượng **≥ 20 xe/15ph** |
| Bắt buộc kèm MAE | **mean magnitude** |
| Bắt buộc kèm hiệu quả phòng thủ | **FPR và FNR** |
| Bắt buộc kèm mọi so sánh | FedAvg cùng điều kiện |
| Mức client | MAE từng client, **client tệ nhất**, p90 |

---

## 7. Cổng dừng trước ma trận tấn công

Chạy **Local-only, Centralized, FedAvg sạch** (10 seed mỗi cái).

> **Cổng:** MAE của FedAvg phải tốt hơn Local-only với Wilcoxon ghép cặp, **p < 0,05 sau Holm**.
>
> **Không đạt → dừng.** Đổi cách chia client hoặc chuyển sang FL cá nhân hoá. Không chạy ma trận tấn công.

Cổng này chạy **đầu tiên**, trước mọi tấn công.

---

## 8. Ngân sách và luật cắt trước

**Máy thi hành:** Ryzen 7 6800H (16 luồng), 31,2 GiB RAM, RTX 3050 4 GB. `torch 2.15.0+cpu`.

| Tầng | Số lần chạy | Thời gian ở 0,0058 h/vòng × 50 vòng |
|---|---|---|
| **Tầng 1 (bắt buộc)** | **2.220** | **~3,8 tuần** |
| Tầng 2 | 7.820 | ~13,4 tuần |
| Tầng 3 | 11.730 | ~20,1 tuần |
| Ma trận đầy | **22.240** | ~38 tuần |

> **Luật cắt đã chốt trước:** nếu thời gian mỗi lần chạy đo được **> 0,5 h**, cắt tấn công cảm biến xuống 3 kiểu → Tầng 1 còn **1.960 lần**.

Chỉ có **một** luật cắt. Nếu thời gian thực tế vượt xa hơn mức đó, quyết định cắt tiếp phải ghi thành amendment **trước** khi xem kết quả tấn công.

**Trạng thái:** `t` thật **chưa đo** (chưa có vòng FL nào chạy). Luật cắt sẽ được áp khi có `t`.

---

## 9. Dữ liệu và phân vùng

| Hạng mục | Giá trị |
|---|---|
| Bộ dữ liệu | LargeST San Diego, **716 cảm biến**, 26 tuyến `Fwy` |
| Độ phân giải | 5 phút gốc → **15 phút** |
| Train / Val / Test | 2017-01-01 → 2019-12-31 / 6 tháng cuối 2019 / **2021** |
| Kịch bản trôi | train 2019 → test 2020 |
| Phân vùng chính | **P-A: 22 client theo hành lang**, sàn 10 cảm biến |
| Cổng dị biệt | EMD median so IID phải **≥ 2×** |

**Đo dị biệt — hai con số, cả hai đúng, khác nhau ở cách dùng generator:**

| Cách đo | Tử số | Mẫu số | Tỉ số |
|---|---|---|---|
| Chung một `rng` (như `56_compute_emd.py`) | 86,37 | 22,64 | 3,81 |
| **Generator riêng cho mỗi phép ngẫu nhiên** | 86,37 | 30,27 | **2,85** |
| Phân vùng P-A 22 client, 24 giờ | 81,92 | 24,20 | 3,39 |

> **Luật:** dùng tỉ số **2,85** (cách viết sạch) làm con số chính thức trong mọi văn bản. Ngưỡng cổng **2×** vẫn đạt. Không dùng 3,81 vì nó phụ thuộc thứ tự tiêu hao RNG, không phải tính chất dữ liệu.

Nguồn: các log đo EMD và rubric 24/11 (giữ trong bản lưu nội bộ).

---

## 10. Ghi kết quả

**Nguồn sự thật:** CSV trên đĩa, một dòng mỗi lần chạy, kèm `sha256`.

```
runs/
  tier1.csv          # 34 chỉ số + 12 tham số mỗi dòng
  tier1.sha256
  artifacts/<run_id>/
```

`run_id` dạng `t1_krum_alie_z1_r20_i50_s03` — đọc được bằng mắt.

**MLflow là lớp xem, không phải nơi lưu.** Đẩy từ CSV sang sau khi chạy xong. MLflow chậm **3.435 lần** khi ghi (68,7 ms/lần so 0,02 ms) và DB lớn 44 lần; schema có thể đổi giữa các phiên bản. Nguồn: log benchmark MLflow (giữ trong bản lưu nội bộ).

### 10.1 Quyết định lưu trữ — CHỐT 25/11/2026

Người quyết định: chủ dự án. Ghi lại nguyên văn ý kiến rồi diễn giải thành luật.

| Hạng mục | Quyết định | Lý do |
|---|---|---|
| **MLflow tracking** | **Bật, ghi vào ổ đĩa local** | Có UI để xem; đã cài 3.18.0 |
| Đường dẫn MLflow | thư mục MLflow cục bộ | Không đặt trên thư mục đồng bộ |
| Backend | **`sqlite:///`** (không dùng file-store) | MLflow 3.18 từ chối file-store — "maintenance mode". Chỉ chạy được nếu đặt `MLFLOW_ALLOW_FILE_STORE=true`, tức dùng backend đã bị khai tử |
| **Checkpoint từng run** | **CÓ — lưu, nếu kích thước cho phép** | Đây là lần chạy **lấy dữ liệu mẫu**, cần giữ để tái lập và kiểm tra |
| Giới hạn checkpoint | Lưu trọng số (không lưu optimizer state) | 12.929 tham số × 4 B = **51 KB/run**; 2.220 run = **109,5 MB** |
| **DOI Zenodo** | **KHÔNG — chưa cần** | Chỉ cần bản benchmark; công bố để sau |
| Bản sao ngoài ổ C | **ổ lưu ngoài (USB 30 GB)** hoặc **1 tệp CSV nén** | Không đưa cây MLflow lên Drive: **9,2 tệp/run × 2.220 = 20.424 tệp**, vượt ngưỡng sync client |

**Đo được, dùng để chốt:** MLflow tạo **9,2 tệp mỗi lần chạy** kể cả một checkpoint 51 KB. Ở 2.220 run là **20.424 tệp** — dung lượng 109,5 MB không phải vấn đề, nhưng số tệp thì có. Nguồn: log đo chi phí artifact MLflow (giữ trong bản lưu nội bộ).

**Hệ quả cho G6:** ghi **cả** CSV (nguồn sự thật) **và** MLflow (lớp xem) **và** checkpoint từng run vào `mlflow/artifacts/<run_id>/weights.npy`. Sau khi một tầng xong, nén `runs/*.csv` thành một tệp zip — đó là thứ đem sao lưu.

**Chưa chốt:** chưa có yêu cầu công bố kèm DOI, nên không thêm bước upload. Nếu sau này cần, Zenodo là miễn phí và nhận zip.

---

## 11. Pre-registration — nhật ký khoá luật

| Ngày | Việc được chốt |
|---|---|
| **2026-11-25** | File này tạo. Chốt §1 (đơn vị vòng), §2 (luật `R_conv`), §3 (FedAvg có trọng số), §4 (thống kê), §5 (hợp lệ hai tầng), §6 (chỉ số), §7 (cổng dừng), §8 (luật cắt), §9 (dữ liệu + **2,85** thay 3,81), §10 (ghi kết quả). |
| **2026-11-25** | Chốt **§10.1** — lưu trữ: MLflow local + checkpoint từng run + **không** DOI Zenodo. Trả lời câu hỏi treo của task D0. |

**Amendment** (thêm dòng khi sửa, không sửa bảng trên):

| Ngày | Amendment | Lý do |
|---|---|---|
| | *(chưa có)* | |

---

## 12. Ba việc còn treo, ghi rõ để không ai tưởng đã xong

| # | Việc | Trạng thái |
|---|---|---|
| 1 | Đo `R_conv` cho GRU / MLP / STGCN | **chưa làm** — §2 chỉ có luật, chưa có số |
| 2 | Đo `t` (giờ/lần chạy) thật | **chưa làm** — §8 dùng số từ benchmark, chưa từ run thật |
| 3 | Đo STGCN — chi phí có thể khác GRU nhiều | **chưa làm** — là ô ngân sách duy nhất chưa đo |

Cả ba đều cần **code FL chạy được**, mà hiện tại project **chưa có dòng code huấn luyện liên kết nào**.

**Đã đóng:** câu hỏi lưu trữ (task D0) — xem §10.1.
