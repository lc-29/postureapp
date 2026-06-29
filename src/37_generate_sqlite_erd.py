"""Generate a polished ERD for the posture app SQLite database."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle


BASE_DIR = Path(__file__).resolve().parents[1]
FIGURES_DIR = BASE_DIR / "reports" / "figures"
OUTPUT_PNG = FIGURES_DIR / "hinh_3_9_erd_sqlite_pretty.png"
OUTPUT_SVG = FIGURES_DIR / "hinh_3_9_erd_sqlite_pretty.svg"


TABLES = {
    "NguoiDung": {
        "title": "NguoiDung",
        "subtitle": "Tài khoản người dùng",
        "xy": (0.55, 6.45),
        "wh": (4.35, 3.25),
        "color": "#0f766e",
        "fields": [
            "PK  maNguoiDung : INTEGER",
            "    tenDangNhap : TEXT UNIQUE",
            "    email : TEXT UNIQUE",
            "    matKhauHash : TEXT",
            "    matKhauSalt : TEXT",
            "    emailDaXacThuc : INTEGER",
            "    lanDangNhapCuoi : TEXT",
            "    ngayTao : TEXT",
        ],
    },
    "EmailOtp": {
        "title": "EmailOtp",
        "subtitle": "Xác thực email/OTP",
        "xy": (5.85, 7.05),
        "wh": (4.2, 2.65),
        "color": "#16a34a",
        "fields": [
            "PK  maOtp : INTEGER",
            "FK  maNguoiDung : INTEGER",
            "    email : TEXT",
            "    otpHash, otpSalt : TEXT",
            "    mucDich : TEXT",
            "    hetHanLuc : TEXT",
            "    daSuDung, soLanThu : INTEGER",
        ],
    },
    "CaiDat": {
        "title": "CaiDat",
        "subtitle": "Cấu hình riêng theo người dùng",
        "xy": (11.05, 6.55),
        "wh": (4.65, 3.15),
        "color": "#2563eb",
        "fields": [
            "PK  maCaiDat : INTEGER",
            "FK  maNguoiDung : INTEGER",
            "    thoiGianCanhBao : INTEGER",
            "    thoiGianChoCanhBao : INTEGER",
            "    batAmThanh, nguonCamera",
            "    duongDanModel, duongDanScaler",
            "    cheDoGiaoDien : TEXT",
            "    smoothingWindowFrames/Threshold",
        ],
    },
    "ThongTinModel": {
        "title": "ThongTinModel",
        "subtitle": "Metadata mô hình",
        "xy": (16.75, 6.8),
        "wh": (4.2, 2.65),
        "color": "#64748b",
        "fields": [
            "PK  maModel : INTEGER",
            "    tenModel : TEXT",
            "    duongDanModel : TEXT",
            "    duongDanScaler : TEXT",
            "    soDacTrungDauVao : INTEGER",
            "    kieuDauRa : TEXT",
            "    accuracy/precision/recall/f1",
        ],
    },
    "PhienLamViec": {
        "title": "PhienLamViec",
        "subtitle": "Phiên chạy webcam/video",
        "xy": (5.65, 2.55),
        "wh": (4.7, 3.55),
        "color": "#7c3aed",
        "fields": [
            "PK  maPhien : INTEGER",
            "FK  maNguoiDung : INTEGER",
            "    thoiGianBatDau/KetThuc : TEXT",
            "    loaiNguon, giaTriNguon : TEXT",
            "    tongSoFrame : INTEGER",
            "    soFrameDung/Sai/KhongCoNguoi",
            "    tongThoiGianDung/Sai : REAL",
            "    soLanCanhBao, doTinCayTrungBinh",
        ],
    },
    "NhatKyTuThe": {
        "title": "NhatKyTuThe",
        "subtitle": "Nhật ký trạng thái theo frame",
        "xy": (11.35, 2.55),
        "wh": (4.65, 3.55),
        "color": "#ea580c",
        "fields": [
            "PK  maNhatKy : INTEGER",
            "FK  maPhien : INTEGER",
            "    thoiDiem : TEXT",
            "    trangThai : TEXT",
            "    nhanDuDoan : INTEGER",
            "    xacSuatSai, doTinCay : REAL",
            "    daCanhBao, loaiCanhBao",
            "    chiSoFrame, fps, ghiChu",
        ],
    },
    "ThongKeNgay": {
        "title": "ThongKeNgay",
        "subtitle": "Tổng hợp thống kê ngày",
        "xy": (0.55, 2.3),
        "wh": (4.35, 3.0),
        "color": "#0891b2",
        "fields": [
            "PK  maThongKe : INTEGER",
            "FK  maNguoiDung : INTEGER",
            "UQ  (maNguoiDung, ngay)",
            "    ngay : TEXT",
            "    tongSoPhien : INTEGER",
            "    tongThoiGianLamViec : REAL",
            "    tongThoiGianDung/Sai : REAL",
            "    tongSoCanhBao, tiLeDung/Sai",
        ],
    },
}


def box_anchor(name: str, side: str) -> tuple[float, float]:
    x, y = TABLES[name]["xy"]
    w, h = TABLES[name]["wh"]
    if side == "left":
        return x, y + h / 2
    if side == "right":
        return x + w, y + h / 2
    if side == "top":
        return x + w / 2, y + h
    if side == "bottom":
        return x + w / 2, y
    raise ValueError(side)


def draw_table(ax: plt.Axes, spec: dict[str, object]) -> None:
    x, y = spec["xy"]
    w, h = spec["wh"]
    color = spec["color"]
    header_h = 0.62
    body_color = "#ffffff"
    border_color = "#334155"

    outer = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.025,rounding_size=0.08",
        linewidth=1.25,
        edgecolor=border_color,
        facecolor=body_color,
        zorder=2,
    )
    ax.add_patch(outer)
    header = Rectangle(
        (x, y + h - header_h),
        w,
        header_h,
        linewidth=0,
        facecolor=color,
        zorder=3,
    )
    ax.add_patch(header)

    ax.text(
        x + w / 2,
        y + h - 0.23,
        spec["title"],
        ha="center",
        va="center",
        fontsize=12.2,
        color="white",
        fontweight="bold",
        zorder=4,
    )
    ax.text(
        x + w / 2,
        y + h - 0.50,
        spec["subtitle"],
        ha="center",
        va="center",
        fontsize=7.7,
        color="#e0f2fe",
        zorder=4,
    )

    fields = spec["fields"]
    line_step = (h - header_h - 0.30) / max(len(fields), 1)
    start_y = y + h - header_h - 0.22
    for idx, field in enumerate(fields):
        field_color = "#0f172a"
        weight = "normal"
        if field.startswith("PK"):
            field_color = "#b91c1c"
            weight = "bold"
        elif field.startswith("FK"):
            field_color = "#1d4ed8"
            weight = "bold"
        elif field.startswith("UQ"):
            field_color = "#a16207"
            weight = "bold"
        ax.text(
            x + 0.18,
            start_y - idx * line_step,
            field,
            ha="left",
            va="top",
            fontsize=7.55,
            color=field_color,
            family="DejaVu Sans Mono",
            fontweight=weight,
            zorder=4,
        )


def draw_relation(
    ax: plt.Axes,
    start: tuple[float, float],
    end: tuple[float, float],
    label: str,
    start_card: str = "1",
    end_card: str = "N",
    dashed: bool = False,
    label_offset: tuple[float, float] = (0.0, 0.0),
) -> None:
    style = (0, (4, 3)) if dashed else "solid"
    color = "#334155" if not dashed else "#64748b"
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops=dict(
            arrowstyle="-",
            color=color,
            linewidth=1.35,
            linestyle=style,
            shrinkA=4,
            shrinkB=4,
            connectionstyle="angle3,angleA=0,angleB=90",
        ),
        zorder=1,
    )

    sx, sy = start
    ex, ey = end
    ax.text(sx + 0.09, sy + 0.09, start_card, fontsize=9.2, color=color, fontweight="bold")
    ax.text(ex - 0.22, ey + 0.09, end_card, fontsize=9.2, color=color, fontweight="bold")
    ax.text(
        (sx + ex) / 2 + label_offset[0],
        (sy + ey) / 2 + label_offset[1],
        label,
        ha="center",
        va="center",
        fontsize=8.6,
        color=color,
        bbox=dict(boxstyle="round,pad=0.18", facecolor="#f8fafc", edgecolor="none", alpha=0.92),
        zorder=5,
    )


def main() -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["axes.unicode_minus"] = False

    fig, ax = plt.subplots(figsize=(17.8, 9.8))
    ax.set_xlim(0, 21.5)
    ax.set_ylim(1.5, 10.1)
    ax.axis("off")
    fig.patch.set_facecolor("#f8fafc")
    ax.set_facecolor("#f8fafc")

    ax.text(
        10.75,
        9.98,
        "Hình 3.9. ERD cơ sở dữ liệu SQLite của ứng dụng phát hiện tư thế",
        ha="center",
        va="top",
        fontsize=18,
        fontweight="bold",
        color="#0f172a",
    )
    ax.text(
        10.75,
        9.63,
        "Dữ liệu được ràng buộc theo người dùng; nhật ký phiên làm việc được tổng hợp thành thống kê ngày",
        ha="center",
        va="top",
        fontsize=10.5,
        color="#475569",
    )

    for table in TABLES.values():
        draw_table(ax, table)

    draw_relation(
        ax,
        box_anchor("NguoiDung", "right"),
        box_anchor("EmailOtp", "left"),
        "xác thực email",
        label_offset=(0.0, 0.42),
    )
    draw_relation(
        ax,
        box_anchor("NguoiDung", "right"),
        box_anchor("CaiDat", "left"),
        "cấu hình riêng",
        label_offset=(0.0, 0.10),
    )
    draw_relation(
        ax,
        box_anchor("NguoiDung", "bottom"),
        box_anchor("PhienLamViec", "left"),
        "thực hiện phiên",
        label_offset=(-0.50, -0.08),
    )
    draw_relation(
        ax,
        box_anchor("NguoiDung", "bottom"),
        box_anchor("ThongKeNgay", "top"),
        "thống kê theo ngày",
        label_offset=(-0.18, -0.08),
    )
    draw_relation(
        ax,
        box_anchor("PhienLamViec", "right"),
        box_anchor("NhatKyTuThe", "left"),
        "ghi log tư thế",
        label_offset=(0.0, 0.28),
    )
    draw_relation(
        ax,
        box_anchor("CaiDat", "right"),
        box_anchor("ThongTinModel", "left"),
        "đường dẫn model/scaler",
        dashed=True,
        start_card="",
        end_card="",
        label_offset=(0.0, 0.28),
    )
    draw_relation(
        ax,
        box_anchor("PhienLamViec", "left"),
        box_anchor("ThongKeNgay", "right"),
        "tổng hợp ngày",
        dashed=True,
        start_card="",
        end_card="",
        label_offset=(0.05, -0.34),
    )

    legend_x, legend_y = 16.8, 2.1
    legend = FancyBboxPatch(
        (legend_x, legend_y),
        4.0,
        1.0,
        boxstyle="round,pad=0.08,rounding_size=0.08",
        linewidth=1.0,
        edgecolor="#cbd5e1",
        facecolor="#ffffff",
        zorder=2,
    )
    ax.add_patch(legend)
    ax.text(legend_x + 0.18, legend_y + 0.74, "Chú thích", fontsize=9.5, fontweight="bold", color="#0f172a")
    ax.text(legend_x + 0.18, legend_y + 0.47, "PK: khóa chính    FK: khóa ngoại", fontsize=8.4, color="#334155")
    ax.plot([legend_x + 0.18, legend_x + 0.70], [legend_y + 0.22, legend_y + 0.22], color="#334155", linewidth=1.35)
    ax.text(legend_x + 0.78, legend_y + 0.22, "Quan hệ khóa ngoại", va="center", fontsize=8.4, color="#334155")
    ax.plot(
        [legend_x + 2.15, legend_x + 2.67],
        [legend_y + 0.22, legend_y + 0.22],
        color="#64748b",
        linewidth=1.35,
        linestyle=(0, (4, 3)),
    )
    ax.text(legend_x + 2.75, legend_y + 0.22, "Quan hệ logic", va="center", fontsize=8.4, color="#334155")

    fig.subplots_adjust(left=0.015, right=0.985, top=0.985, bottom=0.025)
    fig.savefig(OUTPUT_PNG, dpi=320)
    fig.savefig(OUTPUT_SVG)
    plt.close(fig)
    print(f"Saved: {OUTPUT_PNG}")
    print(f"Saved: {OUTPUT_SVG}")


if __name__ == "__main__":
    main()
