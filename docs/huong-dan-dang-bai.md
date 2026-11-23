# Hướng dẫn đăng bài

Mỗi thành viên đăng bài vào thư mục riêng của mình: `docs/thanh-vien/<ten-khong-dau>/`. Trang tự cập nhật khoảng 1 phút sau khi bài được đưa lên GitHub.

## Lần đầu: tạo mục của mình

1. Trên github.com, mở repo, vào thư mục `docs/thanh-vien/`.
2. Bấm **Add file → Create new file**, gõ tên `ten-khong-dau/index.md` (ví dụ `minh/index.md`).
3. Dán mẫu dưới đây, sửa lại, rồi bấm **Commit changes**.

```markdown
# Bài của Minh

Một hai câu giới thiệu phần việc mình làm trong dự án.

## Danh sách bài

- **[Tên bài 1](ten-bai-1.md)**: một câu tóm tắt.
```

4. Thêm một dòng cho mình vào bảng ở trang [Thành viên](thanh-vien/index.md) (file `docs/thanh-vien/index.md`).

## Đăng bài mới

**Cách 1, trên github.com (không cần cài gì):** vào `docs/thanh-vien/<ten>/`, bấm **Add file → Upload files**, kéo thả file `.md` vào rồi **Commit changes**. Sau đó thêm một dòng link tới bài vào `index.md` của mình.

**Cách 2, trên máy (có tự thêm vào "Mới cập nhật" ở trang [Tiến độ chung](tien-do.md)):**

```bash
python them.py duong/dan/bai.md thanh-vien/minh --push
```

## Quy ước

- Viết bằng Markdown, dòng đầu là tiêu đề `# ...`. Tên file không dấu, nối bằng gạch ngang.
- Ảnh để cạnh bài trong cùng thư mục, chèn bằng `![mô tả](ten-anh.png)`.
- Trang này **công khai**: không đưa số điện thoại, email, mật khẩu, mã số sinh viên hay PDF bài báo có bản quyền.
- Câu hỏi cần hỏi thầy thì thêm vào trang [Câu hỏi cho thầy](cau-hoi/index.md) thay vì để trong bài riêng.
