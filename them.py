"""Thêm nhanh một file Markdown vào trang.

Cách dùng:
    python them.py <duong_dan_file.md> <tab> [--tieu-de "Tên hiện trên trang chủ"] [--push]

<tab> là một trong: tai-lieu-chinh, cap-nhat, nghien-cuu, gia-lap, nhap-nhom

Script sẽ:
  1. Copy file vào docs/<tab>/ với tên không dấu, gạch ngang.
  2. Ghi một dòng vào mục "Mới cập nhật" ở trang chủ (trừ tab nhap-nhom).
  3. Nếu có --push: git add, commit và push. Khoảng 1 phút sau trang cập nhật.
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
    ap.add_argument("tab", choices=TABS)
    ap.add_argument("--tieu-de")
    ap.add_argument("--push", action="store_true")
    a = ap.parse_args()

    nguon = Path(a.file)
    if not nguon.is_file():
        sys.exit(f"Không thấy file: {nguon}")
    ten_moi = bo_dau(nguon.stem) + nguon.suffix.lower()
    dich = DOCS / a.tab / ten_moi
    dich.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(nguon, dich)
    print(f"Đã copy -> {dich.relative_to(GOC)}")

    if a.tab != "nhap-nhom" and dich.suffix == ".md":
        tieu_de = a.tieu_de or tieu_de_tu_file(dich)
        ngay = datetime.date.today().strftime("%d/%m/%Y")
        dong = f"- **{ngay}**: [{tieu_de}]({a.tab}/{ten_moi})"
        index = DOCS / "index.md"
        nd = index.read_text(encoding="utf-8")
        if MOC in nd and dong not in nd:
            index.write_text(nd.replace(MOC, f"{MOC}\n{dong}", 1), encoding="utf-8")
            print("Đã thêm vào mục Mới cập nhật ở trang chủ.")

    if a.push:
        subprocess.run(["git", "add", "-A"], cwd=GOC, check=True)
        subprocess.run(["git", "commit", "-m", f"Thêm {ten_moi}"], cwd=GOC, check=True)
        subprocess.run(["git", "push"], cwd=GOC, check=True)
        print("Đã push. Trang sẽ cập nhật sau khoảng 1 phút.")
    else:
        print("Chưa push. Chạy lại với --push, hoặc tự git add/commit/push.")


if __name__ == "__main__":
    main()
