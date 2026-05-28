from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MAIN_APP = PROJECT_ROOT / "src" / "4_main_desktop_app.py"


def test_main_app_contains_accented_vietnamese_ui_text():
    text = MAIN_APP.read_text(encoding="utf-8")

    required_text = [
        "Ứng dụng phát hiện tư thế làm việc",
        "Chưa bật camera",
        "Ngưỡng sai sau làm mượt",
        "Độ tin cậy",
        "Dashboard thống kê tư thế",
        "Tỷ lệ thời gian",
        "Cảnh báo theo phiên",
        "Bảng phiên trong ngày",
        "TƯ THẾ ĐÚNG",
        "KHÔNG PHÁT HIỆN NGƯỜI",
    ]

    for value in required_text:
        assert value in text


def test_main_app_uses_windows_font_for_vietnamese_text():
    text = MAIN_APP.read_text(encoding="utf-8")

    assert 'APP_FONT_FAMILY = "Segoe UI"' in text
    assert 'plt.rcParams["font.family"] = APP_FONT_FAMILY' in text
    assert "ImageDraw.Draw" in text
