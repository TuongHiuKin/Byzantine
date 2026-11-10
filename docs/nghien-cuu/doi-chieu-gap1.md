# Đối chiếu bản GAP-1 với dữ liệu đã đo

> **Kiểm bốn con số dữ liệu trong bản đề xuất GAP-1: ba đúng, một không có trong bài gốc. Kèm phân tích thiết kế thống kê.**
>
> Tác giả: Nguyễn Quang Huy — SE194177 · GVHD: ThS. Lâm Hữu Khánh Phương · Đại học FPT · 10/11/2026

**Đối tượng:** `tuonghiukin.github.io/Byzantine/tai-lieu-chinh/de-xuat-gap1/` — bản 05/11/2026
**Đối chiếu với:** artefact của `LargeST_Analysis` + abstract chính thức của bài HuddsTrafficFL (KBS 2026)
**Ngày:** 10/11/2026

---

## 1. Bốn con số về dữ liệu: ba đúng, một không tồn tại

Đây là phần dễ kiểm nhất và cũng là phần hội đồng sẽ kiểm đầu tiên.

| Bản GAP-1 viết | Đo từ artefact | Kết luận |
|---|---|---|
| "tỷ lệ khuyết thiếu **3,27 %**" | Pooled 2017–2021: **3,27 %** (12.326.778 / 376.535.808 ô) | **Đúng chính xác** |
| "**18.035** cạnh" | `01_cleaning_log.json` → `nonzero_edges: 18035` | **Đúng chính xác** |
| "lưu lượng tháng 4/2020 giảm **48,7 %**" | `03_model_results.json` → `pct_change: -48.67` | **Đúng** (làm tròn 48,7 từ 48,67) |
| "Huddersfield (**382 nút giao**)" | Abstract KBS 2026 + Zenodo: **0 lần** chuỗi "382" | **Không có trong bài — không xác minh được** |

### Về con số 382

Tôi đọc cả hai bản abstract chính thức:

- **KBS 2026** — `10.1016/j.knosys.2026.117003`: 2.608 ký tự, **không có "382"**
- **Zenodo record** — `10.5281/zenodo.22707916`: 615 ký tự, **không có "382"**

Bài báo nói **"junction-level traffic behaviour"** (nhãn bất thường ở mức nút giao) và **"292 clients"** — nhưng **không nêu số nút giao**. Con số 382 là nhóm tự thêm vào.

Đây là lỗi nhỏ về mặt nội dung nhưng **lỗi lớn về mặt phương pháp**: đó là con số duy nhất trong đoạn mở đầu không truy được về nguồn. Một phản biện viên bắt được chỗ này sẽ hỏi tiếp *"còn con số nào khác cũng tự thêm?"*.

**Cách sửa:** bỏ "382 nút giao", thay bằng **"292 client"** — con số này có trong cả abstract KBS và Zenodo, và mạnh hơn vì nó là đơn vị FL thật.

### Điều đáng khen

Ba con số còn lại khớp **chính xác đến hai chữ số thập phân**, và 3,27 % là con số **gộp toàn bộ 2017–2021** — không phải lấy một năm rồi gọi là tổng. Điều này cho thấy nhóm thật sự chạy pipeline, không chép.

Một lưu ý để tránh bị hỏi khó: khuyết thiếu **không đều giữa các năm** — 2018 chỉ 1,37 %, 2021 lên 6,03 %. Nếu báo cáo một con số 3,27 % mà không nói phân bố, người đọc sẽ tưởng dữ liệu đồng nhất. Nên ghi kèm khoảng.

---

## 2. Vấn đề nghiêm trọng: 5 seed không thể đạt p < 0,05

Bản GAP-1 §5.7 ghi: *"Tối thiểu **5 seed**, báo cáo trung bình ± độ lệch chuẩn, kiểm định Wilcoxon có hiệu chỉnh cho nhiều phép so sánh."*

Đây không phải lựa chọn thận trọng — nó **bất khả thi về mặt toán học**:

```
Wilcoxon signed-rank chính xác hai phía, n = 5:
  p_min = 2/2⁵ = 0,0625
```

**0,0625 > 0,05.** Dù hiệu ứng lớn đến đâu, dù mọi cặp đều cùng chiều, p không thể xuống dưới 0,0625.

Và "hiệu chỉnh cho nhiều phép so sánh" làm nó **tệ hơn**, không tốt hơn:

| Số so sánh m | Ngưỡng Holm | Với 5 seed |
|---|---|---|
| 1 | p < 0,050 | **bất khả** (p_min = 0,0625) |
| 3 | p < 0,0167 | **bất khả** |
| 10 | p < 0,005 | **bất khả** |

Nghĩa là toàn bộ §5.7 về kiểm định thống kê **không thể thực thi như đã viết**. Mọi bảng kết quả sẽ chỉ báo cáo được mô tả, không kết luận được gì.

Đây chính là điểm thầy đã cho **2/10** ở hạng mục "Thống kê" trong bản góp ý trước. Bản mới **vẫn chưa sửa**.

**Cách sửa — chọn một:**

1. **10 seed cho ô chính** (p_min = 2/2¹⁰ ≈ 0,002), ô còn lại 3–5 seed chỉ báo cáo mô tả. Đây là cách bản v3 của tôi đang dùng.
2. **Giữ 5 seed nhưng đổi kiểm định**: dùng **bootstrap khoảng tin cậy** thay cho kiểm định giả thuyết, và **không tuyên bố "p < 0,05"** ở bất kỳ đâu.

Cách 1 trung thực hơn. Cách 2 nhanh hơn nhưng phải bỏ hẳn ngôn ngữ "có ý nghĩa thống kê".

---

## 3. Kendall τ với 5 bộ gộp: đúng như thầy đã cảnh báo

RQ4 so thứ hạng giữa dữ liệu thật và mô phỏng bằng Kendall τ. Với 5 bộ gộp, τ chỉ có thể nhận **11 giá trị phân biệt** trên toàn miền [−1, 1].

Hệ quả: nếu thứ hạng sai **một cặp**, τ gần như không đổi. Với k = 5, τ không đủ độ phân giải để nói "thứ hạng giống nhau" theo nghĩa có ý nghĩa — nó chỉ nói "không đảo lộn hoàn toàn".

Thầy đã viết đúng: *"Kendall τ trên 3–5 bộ gộp có độ phân giải rất thấp."* Bản mới vẫn giữ 5 bộ gộp ở kế hoạch chính.

**Cách sửa:**
- Nếu giữ Kendall τ: tăng lên **9 bộ gộp** (37 giá trị phân biệt), hoặc
- Bỏ Kendall τ, thay bằng **so sánh trực tiếp từng cặp** với khoảng tin cậy bootstrap — trả lời đúng câu hỏi "bộ gộp nào đổi thứ hạng" thay vì nén tất cả vào một số.

---

## 4. Thời hạn: 10 ngày đã thành 5 ngày

Bản viết ngày 05/11 nói *"còn khoảng 10 ngày"* — đúng vào lúc đó (05/11 → 15/11 = 10 ngày).

Hôm nay **10/11/2026**, còn **5 ngày**. Bản kế hoạch Phương án A dành:

| Ngày | Việc |
|---|---|
| 06–08/11 | Chuẩn bị dữ liệu, chạy FedAvg sạch | ← **đã qua** |
| 08–11/11 | Ma trận lõi | ← **hôm nay là ngày cuối** |
| 11–14/11 | Viết bài, thầy đọc |
| 15/11 | Nộp |

Nghĩa là **giai đoạn chạy ma trận đã hết hạn hôm nay**. Nếu chưa chạy xong, Phương án A không còn khả thi như đã viết.

### Khối lượng Phương án A có vừa không?

5 bộ gộp × 5 tấn công × 3 tỉ lệ × 5 seed = **375 lần chạy**.

| Thời gian/lần | Tổng | So với 4 ngày còn lại |
|---|---|---|
| 0,35 h | 131 h = **5,5 ngày** | **Không vừa** |
| 0,7 h | 262 h = **10,9 ngày** | Không vừa |
| 1,0 h | 375 h = **15,6 ngày** | Không vừa |

Cộng thêm thời gian viết bài 12–15 trang LNCS, Phương án A **không khả thi** trừ khi:
- Cắt xuống còn **2 bộ gộp × 3 tấn công × 2 tỉ lệ × 3 seed = 36 lần** (≈ 0,5–1,3 ngày), hoặc
- Dùng kết quả trên **một tập con cảm biến** (ví dụ 100/716) để giảm thời gian mỗi lần chạy 5–7 lần.

Điều này cần thầy quyết, nhưng nhóm nên trình bày **phép tính** chứ không chỉ trình bày kế hoạch.

---

## 5. Điểm mạnh thật của bản này

Không phải mọi thứ đều cần sửa. Ba điểm đáng giữ:

1. **Trung thực về giới hạn rà soát.** Ghi rõ *"chưa tra có hệ thống trên Scopus và IEEE Xplore"* và *"bài [7] mới tìm thấy, chưa đọc toàn văn"*. Đây là cách khai báo đúng — người phản biện sẽ tin phần còn lại hơn.

2. **Tự nêu rủi ro trùng hướng và có phương án.** *"Nếu trùng, chuyển trọng tâm sang RQ2 và RQ3"* — đây là kế hoạch B cụ thể, không phải câu đối phó.

3. **Phân biệt nhãn chắc chắn và nhãn ước lượng.** §5.4 tách *nhãn client độc hại* (biết chắc vì tự tiêm) khỏi *nhãn bất thường từ cảm biến* (phải suy ra). Nhiều bài trộn hai loại này rồi báo F1 như thể cả hai đều chắc chắn.

4. **Câu hỏi §8 rất tốt.** Bảy câu hỏi đều là câu hỏi thật cần thầy quyết, đặc biệt câu 1 (thay thế / bổ sung / bài riêng) và câu 7 (bất đồng bộ — chồng lên hướng AFL của thầy). Đây là phần nên giữ nguyên.

---

## 6. Ba việc nên làm ngay, theo thứ tự

| # | Việc | Vì sao trước |
|---|---|---|
| 1 | **Bỏ "382 nút giao", thay bằng "292 client"** | Sửa 1 phút, chặn được câu hỏi về nguồn |
| 2 | **Đổi 5 seed → 10 seed cho ô chính, hoặc bỏ hết ngôn ngữ "p < 0,05"** | §5.7 hiện không thực thi được; đây là điểm thầy cho 2/10 |
| 3 | **Trình bày phép tính 375 lần chạy × thời gian/lần = ? ngày** và xin thầy quyết cắt phạm vi | Để thầy thấy Phương án A không còn vừa, thay vì hứa rồi trượt |

Ba việc này không cần chạy thêm thí nghiệm nào. Chúng sửa **tính đúng đắn của tài liệu**, không sửa nội dung nghiên cứu.

---

## 7. Một câu tổng kết

Bản GAP-1 có **nền đúng**: gap được phát biểu cẩn thận, giới hạn được khai báo, rủi ro được nêu, và ba trong bốn con số dữ liệu khớp chính xác với artefact. Vấn đề nằm ở **ba chi tiết thực thi**: một con số không có nguồn (382), một thiết kế thống kê bất khả thi (5 seed), và một thời hạn đã trôi mất một nửa. Cả ba đều sửa được trong một ngày, và cả ba đều là thứ hội đồng sẽ hỏi đầu tiên.

---

## Phụ lục — nguồn kiểm chứng

| Nội dung | Nguồn |
|---|---|
| 3,27 % pooled | `LargeST_Analysis/log phân tích cục bộ (`raw_nan_pct` 5 năm) |
| 18.035 cạnh | cùng file, `nonzero_edges`; `02_eda_results.json`, `n_edges_directed` |
| −48,67 % | log phân tích cục bộ, `H1_covid_shock.pct_change` |
| Abstract KBS 2026 | OpenAlex `doi:10.1016/j.knosys.2026.117003`, 2.608 ký tự |
| Abstract Zenodo | OpenAlex `doi:10.5281/zenodo.22707916`, 615 ký tự |
| p_min = 2/2ⁿ | tính trực tiếp |
| Kendall τ resolution | đếm hoán vị, k = 5 → 11 giá trị, k = 9 → 37 giá trị |
| 375 lần chạy | 5 × 5 × 3 × 5 |
