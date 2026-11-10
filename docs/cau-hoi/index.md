# Câu hỏi cho thầy

Các câu hỏi em cần xin ý kiến thầy về đề tài, mới nhất ở dưới cùng. Mỗi câu ghi ngày, mục liên quan trong [đề xuất GAP-1 (v2)](../tai-lieu-chinh/de-xuat-gap1-v2.md), trạng thái và câu trả lời của thầy khi có.

**Trạng thái:** 📝 Chưa gửi · ⏳ Đã gửi, chờ trả lời · ✅ Thầy đã trả lời

---

## Q1. Kịch bản dữ liệu chính

*10/11/2026 · Mục 5.1 · Trạng thái: 📝 Chưa gửi*

Em dùng năm 2019 chia 6:2:2 theo thời gian như thầy gợi ý, còn trôi phân phối thì kiểm tra riêng bằng cách test trên năm 2020. Thầy thấy cách này đủ chưa, hay em vẫn nên giữ kịch bản train 2017–2019 / test 2021 ạ?

**Thầy trả lời:** *(chưa có)*

## Q2. Cách chia client chính

*10/11/2026 · Mục 5.2 · Trạng thái: 📝 Chưa gửi*

Em lấy cách chia theo hành lang (khoảng 20–24 client) làm kịch bản chính, còn 8/16/32 client chia theo KMeans tọa độ chỉ để quét số client. Thầy có đồng ý lấy hành lang làm kịch bản chính không ạ?

**Thầy trả lời:** *(chưa có)*

## Q3. FL bất đồng bộ

*10/11/2026 · Mục 8, 9 · Trạng thái: 📝 Chưa gửi*

Em đề xuất bỏ FL bất đồng bộ khỏi GAP-1 và đưa sang hướng mở rộng để giữ khối lượng trong 12 tuần. Thầy có đồng ý không ạ?

**Thầy trả lời:** *(chưa có)*

## Q4. Mô hình đe dọa

*10/11/2026 · Mục 5.5 · Trạng thái: 📝 Chưa gửi*

Mặc định client độc hại tấn công từ vòng đầu, liên tục và phối hợp với nhau. Thầy có muốn em thêm kịch bản tấn công muộn hoặc ngắt quãng không ạ?

**Thầy trả lời:** *(chưa có)*

## Q5. Chuẩn hóa dữ liệu

*10/11/2026 · Mục 5.1 · Trạng thái: 📝 Chưa gửi*

Em dùng z-score toàn cục và chạy thêm một kiểm tra độ nhạy với chuẩn hóa theo từng client. Thầy thấy chọn toàn cục làm mặc định có hợp lý không ạ?

**Thầy trả lời:** *(chưa có)*

## Q6. Danh sách tấn công

*10/11/2026 · Mục 5.5 · Trạng thái: 📝 Chưa gửi*

Em giữ 5 tấn công cập nhật mô hình là Sign-flip, Gaussian, ALIE, IPM và Min-Max, bỏ Scaling và Min-Sum. Danh sách này đã đủ chưa ạ?

**Thầy trả lời:** *(chưa có)*

## Q7. Bước R1′ trong ablation

*10/11/2026 · Mục 5.9 · Trạng thái: 📝 Chưa gửi*

Em có thêm bước R1′ (huấn luyện với masked loss) để tách tác dụng của khuyết thiếu khỏi cách xử lý khuyết thiếu. Thầy thấy bước này có cần thiết không ạ?

**Thầy trả lời:** *(chưa có)*

## Q8. Tài nguyên tính toán

*10/11/2026 · Mục 5.11 · Trạng thái: 📝 Chưa gửi*

Toàn bộ khoảng 1.220 lần chạy, nếu chạy tuần tự thì vượt thời gian. Nhóm mình có thể dùng GPU hoặc máy của lab để chạy song song khoảng 4 tiến trình không ạ?

**Thầy trả lời:** *(chưa có)*

<!-- CAU_HOI_MOI: câu hỏi mới được thêm phía trên dòng này -->
