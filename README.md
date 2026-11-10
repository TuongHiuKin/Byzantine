# Dự án Byzantine FL

Trang cập nhật tiến độ: https://tuonghiukin.github.io/Byzantine/

## Thêm tài liệu mới

```bash
python them.py duong/dan/file.md tai-lieu-chinh --push
```

Các tab: `tai-lieu-chinh`, `cap-nhat`, `nghien-cuu`, `gia-lap`, `nhap-nhom`.
Hoặc kéo thả file vào thư mục `docs/<tab>/` ngay trên github.com.

## Thêm câu hỏi cho thầy

```bash
python them_cau_hoi.py "Nội dung câu hỏi" --chu-de "Tên ngắn" --muc 5.2 --push
```

Hoặc sửa thẳng `docs/cau-hoi/index.md` trên github.com: chép một khối `## Q…` có sẵn, đổi số và nội dung. Khi đã gửi hoặc thầy trả lời, sửa dòng Trạng thái (📝 Chưa gửi → ⏳ Đã gửi → ✅ Đã trả lời) và dòng "Thầy trả lời".

## Xem thử trên máy

```bash
pip install -r requirements.txt
mkdocs serve
```

Mở http://127.0.0.1:8000

## Lưu ý

Trang này công khai. Không đưa số điện thoại, email, mật khẩu hay PDF bài báo có bản quyền lên đây (file `.pdf` đã bị chặn trong `.gitignore`).
