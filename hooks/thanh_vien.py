"""Hook MkDocs: xếp bài theo người và theo thời gian đăng.

Lấy ngày giờ từ lịch sử git (giờ Việt Nam):
  - ngày đăng  = commit đầu tiên của file
  - sửa cuối   = commit gần nhất của file

Hook làm ba việc lúc build:
  1. Trang thanh-vien/index.md: thay dấu <!-- DS_THANH_VIEN --> bằng một khung
     xổ xuống cho mỗi người, bài mới nhất trên cùng.
  2. Trang tien-do.md: thay dấu <!-- MOI_CAP_NHAT --> bằng 15 bài mới nhất của cả nhóm.
  3. Menu bên trái: bài trong mục của từng người xếp mới nhất trên cùng.

Muốn thêm người: tạo thư mục docs/thanh-vien/<ten>/ là tự có, không cần sửa file này.
"""
from __future__ import annotations

import datetime as dt
import fnmatch
import os
import re
import subprocess
from pathlib import Path

from mkdocs.structure.nav import Section
from mkdocs.structure.pages import Page

GIO_VN = dt.timezone(dt.timedelta(hours=7))
SO_NGAY_MOI = 3
SO_BAI_MOI_CAP_NHAT = 15

# Người có bài nằm ngoài thư mục thanh-vien/ (giữ đường link cũ).
# Mẫu là đường dẫn trong docs/, dùng ký tự * như glob.
THANH_VIEN_CO_DINH = [
    ("Kiên", ["index.md", "khao-sat-lien-quan.md", "benchmark-ban-23-11.md",
              "tai-lieu-chinh/*.md", "cau-hoi/*.md"]),
    ("Huy", ["nghien-cuu/*.md"]),
]
# Trang giới thiệu của một mục, không tính là bài.
BO_QUA = ["tai-lieu-chinh/index.md", "nghien-cuu/index.md", "thanh-vien/index.md",
          "thanh-vien/*/index.md"]

_cache: dict[str, tuple[dt.datetime, dt.datetime]] = {}
_docs_dir = ""
_bai: list[dict] = []


def _ngay_git(duong_dan: str) -> tuple[dt.datetime, dt.datetime]:
    """(ngày đăng, sửa cuối) của một file, theo giờ Việt Nam."""
    if duong_dan in _cache:
        return _cache[duong_dan]
    bay_gio = dt.datetime.now(GIO_VN)
    try:
        ra = subprocess.run(
            ["git", "log", "--follow", "--format=%at", "--", duong_dan],
            cwd=_docs_dir, capture_output=True, text=True, check=True,
        ).stdout.split()
    except (OSError, subprocess.CalledProcessError):
        ra = []
    if ra:
        dang = dt.datetime.fromtimestamp(int(ra[-1]), GIO_VN)
        sua = dt.datetime.fromtimestamp(int(ra[0]), GIO_VN)
    else:  # file chưa commit (xem thử trên máy)
        dang = sua = bay_gio
    _cache[duong_dan] = (dang, sua)
    return dang, sua


def _khop(duong_dan: str, mau: list[str]) -> bool:
    return any(fnmatch.fnmatch(duong_dan, m) for m in mau)


def _tieu_de(file_path: str, mac_dinh: str) -> str:
    try:
        for dong in Path(file_path).read_text(encoding="utf-8").splitlines():
            if dong.startswith("# "):
                return dong[2:].strip()
    except OSError:
        pass
    return mac_dinh


def _chu_nhan(src: str) -> str | None:
    if _khop(src, BO_QUA):
        return None
    for ten, mau in THANH_VIEN_CO_DINH:
        if _khop(src, mau):
            return ten
    m = re.match(r"thanh-vien/([^/]+)/", src)
    if m:
        return m.group(1).replace("-", " ").title()
    return None


def on_files(files, config):
    global _docs_dir, _bai
    _docs_dir = config["docs_dir"]
    _bai = []
    for f in files.documentation_pages():
        src = f.src_uri
        ten = _chu_nhan(src)
        if ten is None:
            continue
        dang, sua = _ngay_git(os.path.join(_docs_dir, src))
        _bai.append({
            "src": src, "nguoi": ten, "dang": dang, "sua": sua,
            "tieu_de": _tieu_de(f.abs_src_path, Path(src).stem),
        })
    _bai.sort(key=lambda b: b["dang"], reverse=True)
    return files


def _gio(t: dt.datetime) -> str:
    return t.strftime("%d/%m/%Y %H:%M")


def _nhan(b: dict) -> str:
    bay_gio = dt.datetime.now(GIO_VN)
    if bay_gio - b["dang"] <= dt.timedelta(days=SO_NGAY_MOI):
        return '<span class="nhan-moi">MỚI</span> '
    if b["sua"] - b["dang"] > dt.timedelta(hours=1) and bay_gio - b["sua"] <= dt.timedelta(days=SO_NGAY_MOI):
        return '<span class="nhan-moi-sua">MỚI SỬA</span> '
    return ""


def _link(tu_trang: str, toi: str) -> str:
    goc = os.path.dirname(tu_trang)
    return os.path.relpath(toi, goc or ".").replace(os.sep, "/")


def _sua_cuoi(b: dict) -> str:
    return _gio(b["sua"]) if b["sua"] - b["dang"] > dt.timedelta(hours=1) else "—"


def _ds_thanh_vien(trang: str) -> str:
    nguoi: dict[str, list[dict]] = {}
    for b in _bai:
        nguoi.setdefault(b["nguoi"], []).append(b)
    # người có bài mới nhất lên trước
    thu_tu = sorted(nguoi, key=lambda n: nguoi[n][0]["dang"], reverse=True)
    khoi = []
    for ten in thu_tu:
        ds = nguoi[ten]
        dong = [f'??? note "{ten} · {len(ds)} bài · mới nhất {_gio(ds[0]["dang"])}"',
                "",
                "    | Bài | Đăng lúc | Sửa lần cuối |",
                "    |---|---|---|"]
        for b in ds:
            dong.append(f'    | {_nhan(b)}[{b["tieu_de"]}]({_link(trang, b["src"])}) '
                        f'| {_gio(b["dang"])} | {_sua_cuoi(b)} |')
        khoi.append("\n".join(dong))
    return "\n\n".join(khoi)


def _moi_cap_nhat(trang: str) -> str:
    dong = ["| Bài | Người đăng | Đăng lúc |", "|---|---|---|"]
    for b in _bai[:SO_BAI_MOI_CAP_NHAT]:
        dong.append(f'| {_nhan(b)}[{b["tieu_de"]}]({_link(trang, b["src"])}) '
                    f'| {b["nguoi"]} | {_gio(b["dang"])} |')
    return "\n".join(dong)


def on_page_markdown(markdown, page, config, files):
    src = page.file.src_uri
    if "<!-- DS_THANH_VIEN -->" in markdown:
        markdown = markdown.replace("<!-- DS_THANH_VIEN -->", _ds_thanh_vien(src))
    if "<!-- MOI_CAP_NHAT -->" in markdown:
        markdown = markdown.replace("<!-- MOI_CAP_NHAT -->", _moi_cap_nhat(src))
    return markdown


def on_nav(nav, config, files):
    """Trong mục của từng người, xếp bài mới nhất lên trên (trang giới thiệu giữ đầu)."""
    ngay = {b["src"]: b["dang"] for b in _bai}

    def duyet(items):
        for it in items:
            if isinstance(it, Section):
                trang = [c for c in it.children if isinstance(c, Page)]
                cua_nguoi = [p for p in trang if p.file.src_uri in ngay]
                if cua_nguoi and len(cua_nguoi) == len([p for p in trang if not _khop(p.file.src_uri, BO_QUA)]):
                    dau = [c for c in it.children if not (isinstance(c, Page) and c.file.src_uri in ngay)]
                    cua_nguoi.sort(key=lambda p: ngay[p.file.src_uri], reverse=True)
                    it.children = dau + cua_nguoi
                duyet(it.children)

    duyet(nav.items)
    return nav
