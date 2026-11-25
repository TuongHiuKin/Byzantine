"""Thêm nhanh một file Markdown vào trang.

Cách dùng:
    python them.py <duong_dan_file.md> <tab> [--tieu-de "Tên hiện trên trang chủ"] [--push]

<tab> là một trong: tai-lieu-chinh, cap-nhat, nghien-cuu, gia-lap, nhap-nhom,
      hoặc thanh-vien/<ten-khong-dau> để đăng vào mục của một thành viên

Script sẽ:
  1. Copy file vào docs/<tab>/ với tên không dấu, gạch ngang.
  2. Nếu có --push: git add, commit và push. Khoảng 1 phút sau trang cập nhật.
"""
import argparse
import datetime
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

GOC = Path(__file__).resolve().parent
DOCS = GOC / "docs"
TABS = ["tai-lieu-chinh", "cap-nhat", "nghien-cuu", "gia-lap", "nhap-nhom"]
MOC = "<!-- MOI_CAP_NHAT -->"


def bo_dau(chuoi: str) -> str:
    chuoi = chuoi.replace("đ", "d").replace("Đ", "D")
    chuoi = unicodedata.normalize("NFKD", chuoi).encode("ascii", "ignore").decode()
    chuoi = re.sub(r"[^A-Za-z0-9.]+", "-", chuoi).strip("-").lower()
    return chuoi


def tieu_de_tu_file(p: Path) -> str:
    for dong in p.read_text(encoding="utf-8").splitlines():
        if dong.startswith("# "):
            return dong[2:].strip()
    return p.stem


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("tab", help=f"Một trong {', '.join(TABS)}, hoặc thanh-vien/<ten>")
    ap.add_argument("--tieu-de")
    ap.add_argument("--push", action="store_true")
    a = ap.parse_args()

    hop_le = a.tab in TABS or re.fullmatch(r"thanh-vien/[a-z0-9-]+", a.tab)
    if not hop_le:
        sys.exit(f"Tab không hợp lệ: {a.tab}. Dùng {', '.join(TABS)} hoặc thanh-vien/<ten-khong-dau>.")

    nguon = Path(a.file)
    if not nguon.is_file():
        sys.exit(f"Không thấy file: {nguon}")
    ten_moi = bo_dau(nguon.stem) + nguon.suffix.lower()
    dich = DOCS / a.tab / ten_moi
    dich.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(nguon, dich)
    print(f"Đã copy -> {dich.relative_to(GOC)}")

    # "Mới cập nhật" và trang Thành viên tự lấy ngày từ git (hooks/thanh_vien.py),
    # nên không cần ghi tay nữa.

    if a.push:
        subprocess.run(["git", "add", "-A"], cwd=GOC, check=True)
        subprocess.run(["git", "commit", "-m", f"Thêm {ten_moi}"], cwd=GOC, check=True)
        subprocess.run(["git", "push"], cwd=GOC, check=True)
        print("Đã push. Trang sẽ cập nhật sau khoảng 1 phút.")
    else:
        print("Chưa push. Chạy lại với --push, hoặc tự git add/commit/push.")


if __name__ == "__main__":
    main()
