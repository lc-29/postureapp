# UI Acceptance Notes

Ngay cap nhat: 2026-05-27

## Code verification

Da verify bang lenh:

```powershell
python -m py_compile src/4_main_desktop_app.py src/statistics_service.py
.\.venv\Scripts\python.exe -m pytest tests/test_statistics_service.py -q
```

Ket qua:

- `py_compile`: pass.
- `tests/test_statistics_service.py`: 2 passed.

## Thay doi da co

- App chuyen sang light mode.
- App co control Light/Dark trong sidebar.
- Sidebar duoc chia section ro rang.
- Counters realtime duoc doi thanh mini KPI.
- Dashboard thong ke light mode co date selector, KPI, time distribution, warnings/session, 7-day trend, table phien, risk index va export CSV.
- Dashboard/chart/table dung palette hien tai khi mo trong Light hoac Dark mode.
- Da them data service rieng de test thong ke khong can mo GUI.
- Da cap nhat GUI QA checklist cho light mode/dashboard.
- Da them baseline neck-compression rule QA tai `reports/BASELINE_RULE_QA.md`.

## Manual acceptance con can thuc hien

| Hang muc | Trang thai | Ghi chu |
|---|---|---|
| Screenshot main window chua start | Pending | Can moi truong GUI thuc te. |
| Screenshot ANN running voi webcam/video | Pending | Can webcam hoac video demo. |
| Screenshot rule-based running | Pending | Can webcam hoac video demo. |
| Screenshot statistics dashboard co data | Pending | Can mo app va bam `Xem thong ke`. |
| Test export CSV tu dashboard | Pending | Can thao tac GUI. |
| Test layout 1080x640 va 1366x768 | Pending | Can quan sat truc tiep. |
| Test Light/Dark persistence qua nut Luu cai dat | Pending | Can thao tac GUI dong/mo lai app. |
| Test rut co vua/sau bang webcam/video | Pending | Unit test da pass, van can video thuc te. |

Khong commit screenshot neu anh co thong tin rieng tu hoac hinh anh nguoi dung.
