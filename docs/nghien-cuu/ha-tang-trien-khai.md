# Hạ tầng triển khai nghiên cứu — đo trên máy thật, và chỗ ngân sách sai

*Đánh giá hạ tầng cho LargeST-ByzBench · đo 25/11/2026 · máy Huy-Laptop*

!!! info "Câu hỏi của trang này"
    "Hạ tầng hiện tại có triển khai được nghiên cứu này không?" Không trả lời bằng cảm nhận. Trang này đo CPU, RAM, GPU, ổ đĩa, tốc độ huấn luyện thật, rồi đặt các số đo đó cạnh ngân sách **0,35 h/lần chạy** trong đề cương v3. Kết luận: **hạ tầng đủ, nhưng con số 0,35 sai 76 lần** — và cái sai nằm ở chỗ khác chứ không phải ở chỗ người ta tưởng.

---

## 0. Kết luận trước

| Câu hỏi | Trả lời |
|---|---|
| Máy có đủ để chạy không? | **Đủ**, nhưng phải chọn đúng định nghĩa "một vòng". |
| Có cần GPU không? | **Không bắt buộc.** CPU đủ nếu chạy đúng thiết kế lấy mẫu. |
| `torch` đã cài chưa? | **Chưa.** Tôi vừa cài bản CPU-only để đo; bản CUDA là **2,47 GB** và ghim torch ở 2.6.0. |
| Ngân sách 0,35 h/lần đúng không? | **Sai 76 lần** nếu hiểu "một vòng" là duyệt toàn bộ dữ liệu; **đúng** nếu hiểu là lấy mẫu mini-batch. |
| Tier 1 (2.220 lần) có chạy được không? | **Có** — 3,8 tuần ở 50 vòng/lần. Nhưng **không** ở 100+ vòng. |
| Ràng buộc lớn nhất là gì? | **VRAM 4 GB và việc phải chốt định nghĩa `R_conv`** — không phải tốc độ CPU. |

---

## 1. Hạ tầng đo được

| Thành phần | Thông số | Đánh giá |
|---|---|---|
| CPU | **AMD Ryzen 7 6800H**, 8 nhân / **16 luồng** | Đủ. Matmul FP32 ~120 GFLOPS thực tế. |
| RAM | **31,2 GiB** (18,7 GiB trống lúc đo) | **Dư nhiều.** Toàn bộ 1,12 GiB cửa sổ float32 nằm gọn trong RAM. |
| GPU | **RTX 3050 Laptop, 4.096 MiB VRAM**, compute 8.6, driver 610.91 | **Là ràng buộc thật** — xem §4. |
| Ổ đĩa | 476 GB, còn **238 GB** | Dư. Dữ liệu thô 6,8 GB/tệp HDF5, parquet 151 MB. |
| `torch` | **chưa cài**; tôi cài `2.15.0+cpu` để đo | Phải quyết: CPU (126 MB) hay CUDA (2,47 GB). |

**Đo I/O:** đọc 20.000 dòng HDF5 (105.120 × 8.600) mất **0,62 s** → quét toàn tệp ~**3,3 s**. Đọc parquet cả năm 15 phút (35.040 × 716) mất **0,10 s**.

Nghĩa là **I/O không phải nút cổ chai**. Mọi chi phí đều nằm ở tính toán.

---

## 2. Quy mô bài toán, đo từ phân vùng thật

| Hạng mục | Giá trị |
|---|---|
| Dữ liệu | 35.040 dòng × 716 cảm biến (1 năm, 15 phút) |
| Cửa sổ 12-vào / 12-ra | **35.017** mỗi cảm biến |
| **Tổng cửa sổ** | **25.072.172** |
| Tất cả input float32 | **1,12 GiB** |
| Cửa sổ mỗi client | min **350.170** · median **665.323** · max **3.326.615** |

Đây là con số quyết định mọi thứ phía sau: một "vòng" có duyệt hết 25,1 triệu cửa sổ hay không.

---

## 3. Tốc độ huấn luyện đo thật

### 3.1 Một bước mini-batch

GRU(64), batch 256, CPU, 16 luồng:

| Cấu hình | Tham số | s/bước | cửa sổ/giây |
|---|---|---|---|
| hid 64, batch 256 | 12.929 | 0,0100 | 25.611 |
| **hid 64, batch 1024** | 12.929 | 0,0232 | **44.199** ← nhanh nhất |
| hid 128, batch 1024 | 50.433 | 0,0384 | 26.703 |

Batch lớn hơn nhanh hơn rõ rệt trên CPU (44.199 vs 25.611 cửa sổ/s, **+73 %**). Đây là tối ưu miễn phí.

### 3.2 Hai định nghĩa "một vòng", chênh nhau **46 lần**

Đây là chỗ toàn bộ ngân sách nằm:

| Định nghĩa | Mô tả | Cửa sổ/vòng | Thời gian/vòng |
|---|---|---|---|
| **A. Duyệt toàn bộ** | Mỗi client quét **hết** dữ liệu, 1 epoch | 25.072.172 (100 %) | **961 s = 0,267 h** |
| **B. Lấy mẫu** | 22 client × 3 epoch cục bộ × 32 bước × batch 256 | 540.672 (**2,16 %**) | **20,7 s = 0,0058 h** |

Chênh **46 lần**. FedAvg chuẩn chạy theo **B**; phép tính FLOPs ở lượt đầu của tôi giả định **A**, nên nó cho ra con số bi quan sai.

---

## 4. Ràng buộc VRAM — và nó có thật

Ước lượng bộ nhớ GRU(64) gồm trọng số + Adam + activation + gradient:

| Batch | VRAM cần | 4 GiB? |
|---|---|---|
| 32 | 0,5 MiB | vừa |
| 256 | 2,4 MiB | vừa |
| 1.024 | 9,2 MiB | vừa |

GRU(64) **rất nhỏ** — 12.929 tham số. Với 4 GB VRAM, mô hình này không phải vấn đề. **Vấn đề chỉ xuất hiện nếu chuyển sang STGCN** (đề cương bắt buộc ở tập con, §3.3).

Ước lượng STGCN trên 716 nút: ma trận kề 716² float32 = **2,0 MB**; nhưng activation cho batch 32 với hidden 64 và 2 lớp đồ thị có thể lên **hàng trăm MB**. Vẫn vừa 4 GB, nhưng **biên hẹp hơn nhiều** — và đây là lý do phải **đo STGCN riêng trước khi hứa** 120 lần chạy STGCN.

---

## 5. Ngân sách: con số 0,35 sai ở đâu

Đề cương v3 §3.10 ghi: Tầng 1 = 2.220 lần × **0,35 h/lần** = **4,6 tuần**.

Đặt cạnh số đo:

| Định nghĩa vòng | 50 vòng/lần | 100 vòng/lần | 200 vòng/lần |
|---|---|---|---|
| **A. Duyệt toàn bộ** | 176 tuần (**38×** vượt) | 353 tuần (**77×** vượt) | 706 tuần (**153×** vượt) |
| **B. Lấy mẫu** | **3,8 tuần — VỪA** | 7,7 tuần (1,7× vượt) | 15,3 tuần (3,3× vượt) |

**Chẩn đoán:** con số 0,35 h/lần không sai ngẫu nhiên — nó **đúng cỡ** cho một lần chạy 50–60 vòng theo định nghĩa B. Nghĩa là người viết đề cương đã ngầm giả định thiết kế lấy mẫu, **nhưng không ghi giả định đó ra**. Vì thế nó không kiểm chứng được, và khi triển khai sẽ có người đọc "một vòng" là duyệt toàn bộ rồi kết luận hạ tầng không đủ.

**Số vòng tối đa còn vừa ngân sách 4,6 tuần:**

| Định nghĩa | Số vòng tối đa/lần |
|---|---|
| A. Duyệt toàn bộ | **7 vòng** — không dùng được cho FL |
| B. Lấy mẫu | **359 vòng** — dư cho mọi thiết kế hợp lý |

---

## 6. Ba quyết định phải chốt trước khi code

### 6.1 Chốt định nghĩa "một vòng" trong protocol

Đây là **cùng một lỗ hổng** tôi đã nêu ở tài liệu 27 (§2.2 — chưa chốt `R_conv`), nhưng lần này có số đo đi kèm. Phải ghi vào `PROTOCOL.md`:

> Một vòng = 22 client (tham gia đầy đủ) × **3 epoch cục bộ** × **32 bước mini-batch** × batch **256**. Không client nào duyệt toàn bộ dữ liệu trong một vòng.

Không ghi câu này thì hai người triển khai sẽ ra hai ngân sách chênh 46 lần.

### 6.2 Quyết định CPU hay CUDA

| Lựa chọn | Dung lượng | Đánh giá |
|---|---|---|
| `torch 2.15.0+cpu` | **126,7 MB** | Đã cài. Đủ cho toàn bộ Tầng 1 nếu chạy định nghĩa B. |
| `torch 2.6.0+cu124` | **2.532 MB** | Ghim torch ở 2.6.0. Nhanh hơn cho STGCN, nhưng phải đổi phiên bản. |

**Khuyến nghị: giữ bản CPU.** Đo được 26.000–44.000 cửa sổ/s là đủ cho kế hoạch. Cài CUDA chỉ để tăng tốc một mô hình 12.929 tham số là đổi 2,4 GB và một lần hạ cấp torch để lấy tốc độ không cần thiết. Chỉ chuyển sang CUDA **sau khi** đo STGCN và thấy nó thật sự là nút cổ chai.

### 6.3 Đo STGCN trước khi hứa 120 lần chạy

Đề cương §3.10 có 120 lần chạy STGCN trong Tầng 1. Với STGCN, chi phí **không** như GRU: nó phụ thuộc kích thước đồ thị (716 nút × 716) và số lớp lan truyền. Đây là **ô chưa được đo** duy nhất trong ngân sách, và nó có thể phá kế hoạch nếu chậm gấp 20 lần GRU.

---

## 7. Việc cần làm, theo thứ tự

| # | Việc | Thời gian | Vì sao trước |
|---|---|---|---|
| 1 | **Chốt định nghĩa vòng** vào `PROTOCOL.md` | 15 phút | Không có nó, mọi ước lượng vô nghĩa |
| 2 | Xác nhận `torch` CPU trong `requirements.txt` | 5 phút | Tránh người sau cài CUDA 2,4 GB |
| 3 | **Đo STGCN thật** trên 716 nút | 1 giờ | Là ô ngân sách duy nhất chưa đo |
| 4 | Chốt `R_conv` bằng số đo (không bằng cảm nhận) | 3 giờ | Xem tài liệu 27 §2.2 |
| 5 | Sinh `his.npz` từ HDF5 | 1 giờ chạy | Điều kiện để code đọc dữ liệu |

Việc 1 và 2 làm được ngay trong buổi. Việc 3 là thứ duy nhất còn có thể **đảo ngược kết luận "hạ tầng đủ"**.

---

## 8. Kết luận

**Hạ tầng đủ, và dư ở RAM/ổ đĩa/I-O.** Ràng buộc thật là **VRAM 4 GB** (chỉ ảnh hưởng nếu mở rộng sang STGCN lớn) và **sự mơ hồ về định nghĩa một vòng** — chứ không phải tốc độ.

Con số đáng nhớ: **0,267 h/vòng** nếu duyệt toàn bộ, **0,0058 h/vòng** nếu lấy mẫu — chênh 46 lần. Ngân sách 4,6 tuần của đề cương chỉ đúng ở định nghĩa thứ hai, và đề cương **không nói** nó giả định định nghĩa nào. Đó là một câu phải thêm vào protocol, không phải một cái máy phải mua.

---

## Phụ lục — Nguồn số

| Số | Tệp | Script |
|---|---|---|
| CPU/RAM/GPU/VRAM | đo trực tiếp | `69_infra_bench.py` |
| 25.072.172 cửa sổ, 1,12 GiB | `infra_bench2.json` | `70_infra_bench2.py` |
| 44.199 cửa sổ/s, phân bố theo batch | `infra_gru_real.json` | `71_gru_real_throughput.py` |
| 0,267 h/vòng (A), 0,0058 h/vòng (B), 46× | `infra_round_defs.json` | `72_round_definition.py` |
| HDF5 0,62 s/20k dòng | đo trực tiếp | `69_infra_bench.py` |
| Dung lượng wheel: 126,7 MB / 2.532 MB | `pip download --dry-run` | — |

**Mọi số trong trang này do máy này sinh ra.** Không có số nào chép từ tài liệu nhà sản xuất. Các ước lượng FLOPs ở `69/70` được **thay thế** bằng số đo ở `71/72` — chúng chỉ còn giá trị như một phép kiểm tra bậc độ lớn.
