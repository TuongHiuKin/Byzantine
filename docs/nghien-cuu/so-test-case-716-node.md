# Số test case cho GAP-1 ở 716 node

> **Bao nhiêu lần chạy cho một thành phố ít node nhất: 2.060 bắt buộc, 7.820 đầy đủ, 11.730 nếu mở cả ba mức client.**
>
> Tác giả: Nguyễn Quang Huy — SE194177 · GVHD: ThS. Lâm Hữu Khánh Phương · Đại học FPT · 10/11/2026

**Câu hỏi:** nếu nghiên cứu GAP-1 trên thành phố ít node nhất (khoảng 700 cảm biến), cần bao nhiêu test case?

**Trả lời ngắn:** **2.060 test case cho tầng bắt buộc**, 7.820 cho tầng đầy đủ, 11.730 nếu mở cả ba mức client. Nhưng câu hỏi thật không phải "bao nhiêu" — mà là **"716 node chặn trục nào"**, và nó chặn đúng trục mà bản thiết kế đang hỏi.

**Ngày:** 10/11/2026 · **Nguồn số:** log phân tích cục bộ, `01_data/interim/sd_sensors_716.csv`

---

## 1. Trước hết: "test case" ở đây nghĩa là gì

Có hai đại lượng khác nhau, và lẫn chúng là nguồn gốc của mọi ước lượng sai:

| | Đại lượng | Đơn vị | Ai quyết định |
|---|---|---|---|
| **A** | Số **lần chạy** cần thực hiện | run = một cấu hình × một seed | Thiết kế thí nghiệm |
| **B** | Số **client** chia được từ dữ liệu | client | Metadata của bộ dữ liệu |

Ở thành phố lớn, A là ràng buộc. Ở thành phố ít node, **B chặn A** — và đó chính là trường hợp 716 node.

---

## 2. 716 node chặn cái gì

### 2.1 Không chia được 32 client

Metadata `sd_sensors_716.csv` chỉ có **26 giá trị `Fwy`** (hành lang). `District`, `County`, `Type` đều là hằng số trên toàn bộ 716 cảm biến.

**Bản GAP-1 §5.2 yêu cầu thử với 8, 16 và 32 client.** Con số 32 **bất khả thi** — không có trục nào tạo được 32 nhóm. Đây là lỗi phải sửa trước khi chạy.

### 2.2 Ngay cả 26 cũng không dùng được

Chia 26 hành lang thành 26 client cho phân bố cực lệch:

| n client | min | median | max | max/min | Dùng được? |
|---:|---:|---:|---:|---:|---|
| 4 | 178 | 179 | 180 | 1,0× | có |
| 8 | 86 | 89 | 95 | 1,1× | có |
| 10 | 64 | 68 | 95 | 1,5× | có |
| 12 | 49 | 51 | 95 | 1,9× | có |
| 16 | 26 | 34 | 95 | 3,7× | có |
| 20 | 15 | 22 | 95 | 6,3× | biên |
| 24 | 4 | 18 | 95 | 23,8× | **không** |
| 26 | 1 | 17 | 95 | 95,0× | **không** |

Hai hành lang nhỏ nhất: **SR11-E có 1 cảm biến**, SR54-E/W và SR11-W mỗi cái 3. Client một cảm biến không huấn luyện được gì, và median sẽ coi nó là outlier — tức **chính phòng thủ gây ra loại nhầm** mà đề tài muốn đo.

**Ngưỡng dùng được: n ≤ 16.** Với n = 16, client nhỏ nhất có 26 cảm biến — đủ để train và đủ lớn để không bị coi là nhiễu.

### 2.3 Hệ quả lên ma trận

| Trục | Bản GAP-1 viết | 716 node cho phép |
|---|---|---|
| Số client | 8, 16, **32** | 8, 12, **16** |
| Số mức client | 3 | **tối đa 3** (8/12/16), thực tế nên 2 |
| Tỉ lệ độc hại | 10/20/30/40 % | giữ nguyên |
| Bộ gộp | 7 ô | giữ nguyên |
| Tấn công | 12 | giữ nguyên |
| Seed | 5 | **phải là 10** |

---

## 3. Ràng buộc thứ hai: Krum tự loại mình ở n nhỏ

Krum cần *n ≥ 2f + 3* với *f* = số client độc hại. Ở n nhỏ, tỉ lệ 30–40 % đẩy *f* vượt ngưỡng:

| n | 10 % | 20 % | 30 % | 40 % |
|---:|---|---|---|---|
| 8 | ✓ f=1 | ✓ f=2 | ✓ f=2 | **✗ f=3** |
| 12 | ✓ | ✓ | ✓ f=4 | **✗ f=5** |
| 16 | ✓ | ✓ | ✓ f=5 | ✓ f=6 |
| 20 | ✓ | ✓ | ✓ | ✓ |
| 26 | ✓ | ✓ | ✓ | ✓ |

**n = 8 và 12 mất ô 40 %.** Bulyan còn tệ hơn: cần *n ≥ 4f + 3*, nên **mất cả 30 % và 40 % ở mọi n ≤ 26**.

Nếu chỉ chạy n = 8, ma trận có **ô trống ở 40 %** — và ô trống đó phải được khai là "ngoài giới hạn lý thuyết", không phải "chưa chạy". Đây là chỗ MLflow không giúp được: nó không có trạng thái "bị loại".

---

## 4. Số test case, tính từ thiết kế

Công thức: `7 ô bộ gộp × 12 tấn công × số mức client × 4 tỉ lệ × số seed`, cộng lưới sạch, cộng lượt Krum *f* ước lượng sai.

| Kịch bản | Số lần chạy | Tuần @0,35 h |
|---|---:|---:|
| **Như bản viết** (n=8,16 @5 seed) | 3.910 | 8,1 |
| n=8,16 @10 seed | 7.820 | 16,3 |
| n=8,12,16 @10 seed | 11.730 | 24,4 |
| n=16 duy nhất @10 seed | 3.910 | 8,1 |
| **Tầng 1** (2 mức client, 1 tỉ lệ 20 %, 10 seed) | **2.060** | **4,3** |
| Tầng 2 (2 mức client, 4 tỉ lệ, 10 seed) | 7.820 | 16,3 |
| Tầng 3 (thêm n=12) | 11.730 | 24,4 |

### Năng lực của 12 tuần

| Tốc độ mỗi lần chạy | Số lần chạy tối đa trong 12 tuần |
|---|---:|
| 0,15 h | 13.440 |
| 0,35 h | **5.760** |
| 0,70 h | 2.880 |

**Kết luận trực tiếp:** ở 0,35 h/lần, 12 tuần chứa được **5.760 lần chạy**. Ma trận đầy đủ (11.730) **không vừa** — cần 24,4 tuần. Ngay cả bản nhẹ hơn (7.820) cũng vượt 12 tuần.

Chỉ **Tầng 1 (2.060 lần, 4,3 tuần)** vừa, và còn 7,7 tuần cho phân tích và viết.

---

## 5. Khuyến nghị: ma trận ba tầng cho 716 node

### Tầng 1 — bắt buộc, 2.060 lần, 4,3 tuần

| Thành phần | Giá trị |
|---|---|
| Số client | **8 và 16** (bỏ 32) |
| Tỉ lệ độc hại | **20 %** duy nhất |
| Bộ gộp | đủ 7 ô |
| Tấn công | đủ 12 |
| Seed | **10** |
| Lưới sạch | có |
| Krum *f* ước lượng sai | có |

Trả lời được RQ1 (hiệu năng), RQ2 (cái giá phòng thủ), RQ3 (tấn công cảm biến) ở một tỉ lệ. **Không** trả lời được RQ2 đầy đủ vì thiếu đường cong theo tỉ lệ.

### Tầng 2 — mở tỉ lệ, +5.760 lần, +12 tuần

Thêm 10/30/40 %. Đây là tầng trả lời **"điểm gãy ở đâu"** — câu hỏi chính của RQ1. Không có nó, bài chỉ nói được "ở 20 % thì thế này", không nói được ngưỡng.

### Tầng 3 — mở trục client, +3.910 lần

Thêm n = 12. Đây là tầng kiểm chứng *n ≥ 2f + 3* có đúng trên dữ liệu thật không. Nếu bỏ, mất phần lý thuyết.

**Ưu tiên nếu buộc cắt:** giữ **Tầng 1 + một phần Tầng 2** (thêm tỉ lệ 40 %) — vì 40 % là nơi Krum gãy, tức nơi có phát hiện. Bỏ Tầng 3.

---

## 6. Ba điều phải sửa trong bản GAP-1

1. **Bỏ "32 client"** — bất khả thi với 26 hành lang. Thay bằng **8, 12, 16**.
2. **Khai rõ n ≤ 16 mới khả thi**, kèm lý do phân bố (95 cảm biến vs 1 cảm biến).
3. **Khai ô bị loại theo lý thuyết**: Krum ở n=8, 40 % và toàn bộ Bulyan ở 30–40 %.

Nếu không sửa, người phản biện sẽ tự tính và thấy ma trận có ô không thể chạy — mà bài lại không nói.

---

## 7. Trả lời trực tiếp câu hỏi

> Nếu nghiên cứu GAP-1 trên thành phố ít node nhất cỡ 700, cần bao nhiêu test case?

| Mức | Số test case | Thời gian @0,35 h |
|---|---:|---:|
| **Tối thiểu để bảo vệ được** | **2.060** | 4,3 tuần |
| Đủ để có đường cong tỉ lệ | 7.820 | 16,3 tuần |
| Đầy đủ ba mức client | 11.730 | 24,4 tuần |

**Con số nên dùng: 2.060.** Đó là ma trận nhỏ nhất mà vẫn trả lời được ba câu hỏi nghiên cứu, và vừa 12 tuần cùng thời gian viết.

Nhưng có một điều quan trọng hơn con số: **716 node không phải "tha hồ chạy ít test case hơn".** Nó là mức **tối thiểu** của LargeST mà vẫn còn chia được client. Nếu chọn thành phố nhỏ hơn nữa — dưới 100 node — thì không chia được quá 4–6 client, và toàn bộ trục client sụp. 716 là **biên dưới khả dụng**, không phải lựa chọn tiết kiệm.

---

## Phụ lục — nguồn số

| Nội dung | Nguồn |
|---|---|
| 716 cảm biến, 26 hành lang, phân bố kích thước | `01_data/interim/sd_sensors_716.csv` |
| Số lần chạy, tuần, năng lực 12 tuần | log phân tích cục bộ |
| Sinh số | script phân tích cục bộ |
| Điều kiện Krum, Bulyan | Blanchard và cộng sự (2017); El Mhamdi và cộng sự (2018) |
| 0,35 h/lần | giả định của kế hoạch, **chưa đo thật** |
