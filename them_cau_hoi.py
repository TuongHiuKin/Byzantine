"""Thêm một câu hỏi vào tab "Câu hỏi cho thầy".

Cách dùng:
    python them_cau_hoi.py "Nội dung câu hỏi" --chu-de "Tên ngắn" [--muc 5.2] [--push]

Câu hỏi mới được đánh số tiếp theo, ghi ngày hôm nay, trạng thái "📝 Chưa gửi".
Khi đã gửi hoặc thầy đã trả lời, sửa trực tiếp dòng Trạng thái và dòng "Thầy trả lời"
trong docs/cau-hoi/index.md (sửa được ngay trên github.com).
"""
import argparse
import datetime
import re
import subprocess
from pathlib import Path

GOC = Path(__file__).resolve().parent
FILE = GOC / "docs" / "cau-hoi" / "index.md"
MOC = "<!-- CAU_HOI_MOI"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cau_hoi")
    ap.add_argument("--chu-de", required=True, help="tên ngắn, hiện làm tiêu đề")
    ap.add_argument("--muc", help="mục liên quan trong đề xuất, ví dụ 5.2")
    ap.add_argument("--push", action="store_true")
    a = ap.parse_args()

    nd = FILE.read_text(encoding="utf-8")
    so = max([int(x) for x in re.findall(r"^## Q(\d+)\.", nd, flags=re.M)] or [0]) + 1
    ngay = datetime.date.today().strftime("%d/%m/%Y")
    muc = f" · Mục {a.muc}" if a.muc else ""
    khoi = (f"## Q{so}. {a.chu_de}\n\n*{ngay}{muc} · Trạng thái: 📝 Chưa gửi*\n\n"
            f"{a.cau_hoi.strip()}\n\n**Thầy trả lời:** *(chưa có)*\n\n")
    vi_tri = nd.index(MOC)
    FILE.write_text(nd[:vi_tri] + khoi + nd[vi_tri:], encoding="utf-8")
    print(f"Đã thêm Q{so}.")

    if a.push:
        subprocess.run(["git", "add", str(FILE)], cwd=GOC, check=True)
        subprocess.run(["git", "commit", "-m", f"Thêm câu hỏi Q{so}: {a.chu_de}"], cwd=GOC, check=True)
        subprocess.run(["git", "push"], cwd=GOC, check=True)
        print("Đã push. Trang sẽ cập nhật sau khoảng 1 phút.")
    else:
        print("Chưa push. Chạy lại với --push, hoặc tự git add/commit/push.")


if __name__ == "__main__":
    main()
