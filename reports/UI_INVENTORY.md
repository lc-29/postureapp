# UI Inventory

Ngay cap nhat: 2026-05-27

## Pham vi

- `src/4_main_desktop_app.py`
- Main window realtime
- Sidebar dieu khien
- Baseline debug panel
- Statistics dashboard
- Chart/fallback chart
- Dialog loi database/model/export

## Trang thai truoc khi sua

| Khu vuc | Trang thai cu | Van de |
|---|---|---|
| App theme | `ctk.set_appearance_mode("dark")` | Khong dap ung yeu cau light mode. |
| Main layout | Video trai, sidebar phai | Dung cho demo, nhung sidebar la chuoi input/nut dai. |
| Video frame | CTkFrame mac dinh dark | Can surface sang va placeholder ro hon. |
| Status | Label lon + confidence/timer | Co thong tin can thiet, nhung chua nam trong status section. |
| Counters | Text block nhieu dong | Kho scan khi demo. |
| Baseline panel | Text block dai | Can surface light va can giam cam giac debug thuan text. |
| Statistics | Popup dark, 5 card, pie/bar chart, textbox phien | Co ban nhung chua truc quan du, chua co trend/risk/table cot. |
| QA | Checklist chuc nang co ban | Thieu light mode, dashboard, date filter, risk, export. |

## Mau hard-code can chuyen sang token

| Mau cu | Vai tro cu | Cach xu ly |
|---|---|---|
| `#1f1f1f` | Nen popup/textbox dark | Thay bang `THEME["app_bg"]` hoac `THEME["surface"]`. |
| `#2b2b2b` | Chart/card dark | Thay bang surface light + border. |
| `#242424` | Panel dark | Thay bang surface light. |
| `#f8fafc` | Text tren nen dark | Giu lam surface subtle token, khong dung lam text chinh. |
| `#cbd5e1` | Muted text dark | Thay bang muted text light. |
| `#3f3f46` | Border/progress dark | Thay bang border light. |
| `#22c55e` | Success tren dark | Thay bang `#15803d` cho light contrast. |
| `#ef4444` | Danger | Giu y nghia, doi sang `#dc2626` cho text/status. |
| `#f59e0b` | Warning | Doi sang `#b45309` cho text/status light. |

## Theme token moi

| Token | Gia tri | Vai tro |
|---|---:|---|
| `app_bg` | `#f6f8fb` | Nen tong the. |
| `surface` | `#ffffff` | Card/panel chinh. |
| `surface_muted` | `#eef2f7` | Placeholder/progress background. |
| `surface_subtle` | `#f8fafc` | Section/card phu. |
| `border` | `#d7dde8` | Border panel. |
| `border_soft` | `#e5eaf2` | Border nhe. |
| `text` | `#162033` | Text chinh. |
| `muted` | `#5b677a` | Text phu. |
| `success` | `#15803d` | Tu the dung. |
| `danger` | `#dc2626` | Tu the sai. |
| `warning` | `#b45309` | Dang kiem tra/canh bao. |
| `info` | `#2563eb` | Primary action. |
| `neutral` | `#64748b` | Khong phat hien nguoi/secondary. |

## Ket qua sau dot sua nay

| Khu vuc | Ket qua |
|---|---|
| App theme | Da doi sang `ctk.set_appearance_mode("light")`. |
| Theme | Da them `THEME` token trong `src/4_main_desktop_app.py`. |
| Sidebar | Da chia thanh section: trang thai, nguon dau vao, nhan dien, canh bao, thao tac, phien hien tai. |
| Counters | Da doi text block thanh mini KPI grid. |
| Statistics | Da doi sang dashboard light mode co date selector, KPI, stacked time bar, warnings/session, trend 7 ngay, table phien, risk index va export CSV. |
| Data layer | Da tao `src/statistics_service.py` va `tests/test_statistics_service.py`. |

## Con can QA thu cong

- Chup screenshot main window o 1180x680 va minsize 1080x640.
- Chay ANN mode voi webcam/video file.
- Chay rule-based mode va xem baseline panel.
- Mo dashboard khi co data, khi chon ngay cu, khi database moi chua co data.
- Bam `Export CSV` tu dashboard.
- Kiem tra chart font/label tren man hinh 1366x768.

