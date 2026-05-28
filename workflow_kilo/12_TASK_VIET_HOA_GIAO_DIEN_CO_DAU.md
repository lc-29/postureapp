# 12 Task Viet Hoa Giao Dien Co Dau

Ngay tao: 2026-05-27

## Trang thai thuc thi 2026-05-27

| Task | Trang thai | Ket qua |
|---|---|---|
| TASK-300 | Done | Da lap inventory text UI vao `reports/UI_VIETNAMESE_TEXT_INVENTORY.md`. |
| TASK-301 | Done | Da chuan hoa font Segoe UI cho CustomTkinter va Matplotlib. |
| TASK-302 | Done | Da Viet hoa man hinh chinh, sidebar, nut, label cau hinh va status. |
| TASK-303 | Done | Da Viet hoa overlay OpenCV bang PIL ImageDraw de ho tro dau tieng Viet. |
| TASK-304 | Done | Da Viet hoa messagebox va loi chinh trong app. |
| TASK-305 | Done | Da Viet hoa dashboard thong ke, KPI, chart, table, empty state va export message. |
| TASK-306 | Done | Da Viet hoa panel baseline va warning rule-based hien thi tren UI. |
| TASK-307 | Done | Da them font helper va test bao ve Unicode. |
| TASK-308 | Done | Da sua cac chuoi mojibake/khong dau tim thay trong UI runtime. |
| TASK-309 | Done | Da them unit test `tests/test_ui_vietnamese_text.py`. |
| TASK-310 | Done | Da cap nhat `reports/GUI_QA_CHECKLIST.md` voi checklist UI tieng Viet co dau. |
| TASK-311 | Done | Da build `dist/PostureDetectionApp/PostureDetectionApp.exe`, smoke test runtime files va tao `release/PostureDetectionApp_0.1.1-vietnamese-ui.zip`. |

## Muc tieu

Tinh chinh app desktop CustomTkinter de toan bo giao dien hien thi **tieng Viet co dau** ro rang, dung encoding, khong bi loi font, khong bi mojibake khi chay bang Python va khi dong goi `.exe`.

Pham vi chinh:

- `src/4_main_desktop_app.py`
- `src/3_database_setup.py`
- `src/config.py` neu co text hien thi
- `src/statistics_service.py` neu co text tra ve dashboard
- `release_docs/README_RUN_APP.md` neu can dong bo text nguoi dung
- QA checklist va deployment build sau khi sua

## Ket luan hien trang

Giao dien hien tai dang dung nhieu chuoi tieng Viet khong dau, vi du:

- `Ung dung phat hien tu the lam viec`
- `Chua bat camera`
- `Nguon dau vao`
- `Nhan dien`
- `Canh bao`
- `Canh bao sau (giay)`
- `Cooldown canh bao (giay)`
- `Lam muot xac suat (frame)`
- `Nguong sai sau lam muot`
- `Bat am thanh canh bao`
- `Luu cai dat`
- `Xem thong ke`
- `Dashboard thong ke tu the`
- `Do tin cay`
- `Thoi gian sai`

Ly do can lam theo task rieng:

- File Python phai luu UTF-8.
- PyInstaller/Windows phai hien thi dung font Unicode.
- Text co dau dai hon, co nguy co tran label/button/sidebar.
- Mot so file hien co co dau bi mojibake trong comment/docstring cua `src/3_database_setup.py`, can tranh lam lan sang UI.

## Nguyen tac sua

- Tat ca file sua phai luu UTF-8.
- Text UI duoc Viet hoa co dau, nhung bien/code/schema database co the giu khong dau neu dang on dinh.
- Khong doi ten cot SQLite, khong doi enum status noi bo.
- Khong doi status code noi bo:
  - `DUNG_TU_THE`
  - `SAI_TU_THE`
  - `KHONG_PHAT_HIEN_NGUOI`
  - `DANG_KIEM_TRA`
- Chi doi text hien thi cho nguoi dung.
- Sau khi sua phai test ca Python dev va PyInstaller build.

## TASK-300: Kiem ke toan bo text hien thi trong app

Muc tieu: lap danh sach chuoi UI can Viet hoa.

Lenh goi y:

```powershell
rg -n "text=|title\\(|messagebox|configure\\(text|tree.heading|draw_text|set\\(" src/4_main_desktop_app.py
```

Can phan loai:

- Main window title.
- Sidebar section title.
- Labels/entries/buttons/switches.
- Messagebox title/body.
- Status label.
- Video overlay text.
- Baseline info panel.
- Dashboard window.
- Chart labels.
- Table headings.
- Export/statistics messages.

Done khi:

- Co bang mapping text cu -> text moi trong `reports/UI_VIETNAMESE_TEXT_INVENTORY.md`.

## TASK-301: Tao bang mapping tieng Viet co dau

Muc tieu: chuan hoa cach dung tu truoc khi sua code.

File can tao:

- `reports/UI_VIETNAMESE_TEXT_INVENTORY.md`

Bang mapping mau:

| Text hien tai | Text moi |
|---|---|
| `Ung dung phat hien tu the lam viec` | `Ứng dụng phát hiện tư thế làm việc` |
| `Chua bat camera` | `Chưa bật camera` |
| `Chon nguon va bam Bat dau` | `Chọn nguồn và bấm Bắt đầu` |
| `PHAT HIEN TU THE` | `PHÁT HIỆN TƯ THẾ` |
| `Trang thai hien tai` | `Trạng thái hiện tại` |
| `Nguon dau vao` | `Nguồn đầu vào` |
| `Nhan dien` | `Nhận diện` |
| `Canh bao` | `Cảnh báo` |
| `Canh bao sau (giay)` | `Cảnh báo sau (giây)` |
| `Cooldown canh bao (giay)` | `Thời gian chờ giữa cảnh báo (giây)` |
| `Lam muot xac suat (frame)` | `Làm mượt xác suất (frame)` |
| `Nguong sai sau lam muot` | `Ngưỡng sai sau làm mượt` |
| `Bat am thanh canh bao` | `Bật âm thanh cảnh báo` |
| `Bat dau` | `Bắt đầu` |
| `Dung` | `Dừng` |
| `Luu cai dat` | `Lưu cài đặt` |
| `Xem thong ke` | `Xem thống kê` |
| `Do tin cay` | `Độ tin cậy` |
| `Thoi gian sai` | `Thời gian sai` |
| `Khong nguoi` | `Không người` |
| `Dashboard thong ke tu the` | `Dashboard thống kê tư thế` |

Done khi:

- Mapping du de sua code.
- Cac text dai duoc rut gon hop ly de khong tran UI.

## TASK-302: Sua text main UI trong `src/4_main_desktop_app.py`

Muc tieu: sidebar va main screen hien tieng Viet co dau.

Can sua:

- Window title.
- Placeholder video.
- Section title:
  - `Giao diện`
  - `Trạng thái hiện tại`
  - `Nguồn đầu vào`
  - `Nhận diện`
  - `Cảnh báo`
  - `Thao tác`
  - `Phiên hiện tại`
- Entry labels:
  - `Camera, IP hoặc video`
  - `Chế độ`
  - `Cảnh báo sau (giây)`
  - `Thời gian chờ giữa cảnh báo (giây)`
  - `Làm mượt xác suất (frame)`
  - `Ngưỡng sai sau làm mượt`
- Buttons/switch:
  - `Bắt đầu`
  - `Dừng`
  - `Lưu cài đặt`
  - `Xem thống kê`
  - `Bật âm thanh cảnh báo`
- Metric cards:
  - `Tổng frame`
  - `Đúng`
  - `Sai`
  - `Không người`
  - `Cảnh báo`
  - `FPS`

Done khi:

- App init duoc.
- Sidebar khong bi tran text o kich thuoc 1080x640.

## TASK-303: Sua status text va overlay video

Muc tieu: status hien thi co dau nhung code noi bo giu nguyen.

Can sua mapping hien thi:

| Status code | Text hien thi moi |
|---|---|
| `DANG_KIEM_TRA` | `ĐANG KIỂM TRA` |
| `DUNG_TU_THE` | `TƯ THẾ ĐÚNG` |
| `SAI_TU_THE` | `SAI TƯ THẾ` |
| `KHONG_PHAT_HIEN_NGUOI` | `KHÔNG PHÁT HIỆN NGƯỜI` |

Can sua:

- `STATUS_TEXT`
- `draw_frame_overlay()` neu co text `P(sai)` co the giu hoac doi thanh `P(sai)`.
- `update_status_ui()`
- timer text:
  - `Đã cảnh báo`
  - `Thời gian sai`
  - `Đang kiểm tra...`

Done khi:

- Overlay video hien dung Unicode.
- Khong anh huong logic logging/status.

## TASK-304: Sua messagebox va validation errors

Muc tieu: tat ca popup loi/thanh cong co dau.

Can sua cac nhom:

- Loi database.
- Loi cai dat.
- Loi khoi dong.
- Loi export CSV.
- Thanh cong luu cai dat.
- Thong bao doi theme khi camera dang chay.
- Validation:
  - `Thời gian cảnh báo phải là số.`
  - `Thời gian chờ cảnh báo phải là số.`
  - `Số frame làm mượt phải là số.`
  - `Ngưỡng sai sau làm mượt phải là số.`
  - `Ngưỡng sai sau làm mượt phải nằm trong [0.01, 0.99].`

Done khi:

- Popup hien co dau.
- Khong co chuoi khong dau trong messagebox chinh.

## TASK-305: Sua dashboard thong ke

Muc tieu: cua so thong ke doc tu nhien bang tieng Viet co dau.

Can sua:

- Window title: `Dashboard thống kê tư thế`
- Subtitle.
- Empty states:
  - `Chưa có dữ liệu thống kê cho ngày đã chọn.`
  - `Chưa có dữ liệu`
  - `Chưa có dữ liệu phiên`
  - `Chưa có phiên trong ngày đã chọn.`
- KPI:
  - `Tổng thời gian`
  - `Đúng tư thế`
  - `Sai tư thế`
  - `Cảnh báo`
  - `Độ tin cậy`
  - `Risk`
- Chart labels:
  - `Số cảnh báo`
  - `Sai tư thế (%)`
- Table headings:
  - `Bắt đầu`
  - `Thời lượng`
  - `Đúng`
  - `Sai`
  - `Không người`
  - `Cảnh báo`
  - `Tin cậy`
  - `Risk`

Done khi:

- Dashboard light/dark hien dung dau.
- Table heading khong bi cat qua nhieu.

## TASK-305A: Viet hoa toan bo KPI trong dashboard thong ke

Muc tieu: cac the thong ke tong quan trong cua so `Xem thống kê` phai hien tieng Viet co dau va de hieu voi nguoi dung cuoi.

Can kiem tra/sua cac text dang tao trong:

- `show_statistics()`
- `render_statistics_content()`
- `create_stat_card()`

Danh sach KPI can Viet hoa:

| Hien tai/nhom y nghia | Text de xuat |
|---|---|
| Tong thoi gian | `Tổng thời gian` |
| Dung tu the | `Đúng tư thế` |
| Sai tu the | `Sai tư thế` |
| Khong xac dinh / no person | `Không xác định` hoặc `Không phát hiện người` |
| Canh bao | `Cảnh báo` |
| Do tin cay | `Độ tin cậy` |
| Risk / highest risk | `Mức rủi ro` |
| Average risk | `Rủi ro trung bình` |
| Highest risk | `Rủi ro cao nhất` |

Yeu cau hien thi:

- Neu dung tu `Risk`, can thong nhat la `Rủi ro` trong UI, co the giu `TPRI` trong chu thich ky thuat.
- Gia tri phan tram giu dinh dang `xx.x%`.
- Thoi gian van dung `h/p/s` neu muon ngan gon, nhung label phai co dau.

Done khi:

- Cac KPI khong con text khong dau.
- Nguoi dung khong can biet code van hieu chi so.

## TASK-305B: Viet hoa bieu do trong dashboard thong ke

Muc tieu: tat ca bieu do/progress chart trong dashboard hien label co dau.

Can sua cac ham:

- `draw_time_distribution_chart()`
- `draw_time_distribution_fallback()`
- `draw_warning_chart()`
- `draw_warning_chart_fallback()`
- `draw_trend_chart()`

Text de xuat:

| Nhom | Text de xuat |
|---|---|
| Time distribution title | `Tỷ lệ thời gian tư thế` |
| Correct time | `Đúng tư thế` |
| Incorrect time | `Sai tư thế` |
| Unknown/no person | `Không phát hiện người` |
| Warning chart title | `Cảnh báo theo phiên` |
| Warning y-axis | `Số cảnh báo` |
| Trend title | `Xu hướng 7 ngày` |
| Incorrect ratio y-axis | `Sai tư thế (%)` |
| Warning legend | `Cảnh báo` |

Yeu cau:

- Matplotlib phai hien duoc dau tieng Viet. Neu bi loi font, set font family chung `Segoe UI`.
- Fallback progress bar cung phai Viet hoa.
- Khong de label qua dai lam cat truc/legend; neu dai thi xuong dong hoac rut gon.

Done khi:

- Bieu do light/dark hien text co dau.
- Khong bi mojibake trong chart.

## TASK-305C: Viet hoa bang phien lam viec

Muc tieu: bang danh sach phien trong dashboard phai hien cot co dau va gia tri de hieu.

Can sua ham:

- `render_sessions_table()`

Cot de xuat:

| Column key | Heading moi |
|---|---|
| `started` | `Bắt đầu` |
| `duration` | `Thời lượng` |
| `correct` | `Đúng` |
| `incorrect` | `Sai` |
| `unknown` | `Không người` |
| `warnings` | `Cảnh báo` |
| `confidence` | `Tin cậy` |
| `risk` | `Rủi ro` |

Gia tri can Viet hoa:

- `LOW` -> `Thấp`
- `MEDIUM` -> `Trung bình`
- `HIGH` -> `Cao`
- `CRITICAL` -> `Rất cao`
- `ok` -> `Ổn`
- `no_frame_summary` -> `Thiếu thống kê frame`
- `missing_end_time` -> `Thiếu thời điểm kết thúc`

Done khi:

- Bang doc duoc bang tieng Viet.
- Cot khong bi hep qua; neu can tang width cua cua so dashboard hoac cot.

## TASK-305D: Viet hoa bo chon ngay, trang thai rong va export trong dashboard

Muc tieu: cac text phu trong man hinh thong ke khong bi sot.

Can sua:

- Label/heading cua date selector neu co.
- Button:
  - `Export CSV` -> co the giu `Export CSV` hoac doi `Xuất CSV`.
  - `Dong` -> `Đóng`.
- Empty states:
  - `Chưa có dữ liệu thống kê cho ngày đã chọn.`
  - `Chưa có dữ liệu`
  - `Chưa có dữ liệu phiên`
  - `Chưa có dữ liệu xu hướng`
  - `Chưa có phiên trong ngày đã chọn.`
- Current session note:
  - `Phiên hiện tại sẽ được lưu sau khi bấm Dừng. Frame: ..., đúng: ..., sai: ..., không có người: ..., cảnh báo: ...`
- Export message:
  - `Đã export thống kê vào reports/results.`
  - `Không export được thống kê: ...`
  - Với bản desktop đã đóng gói: `Bản desktop đã đóng gói chỉ hỗ trợ xem thống kê trong app. Hãy dùng bản source Python nếu cần export CSV nghiên cứu.`

Done khi:

- Dashboard khong con chuoi khong dau trong cac state phu.
- Button khong bi cat chu.

## TASK-305E: QA rieng cho giao dien thong ke

Muc tieu: kiem tra dashboard sau khi Viet hoa co dau bang mat that.

Checklist:

| Hang muc | Light | Dark | Ghi chu |
|---|---|---|---|
| Tieu de `Dashboard thống kê tư thế` hien dung |  |  |  |
| Subtitle co dau dung |  |  |  |
| KPI `Tổng thời gian`, `Đúng tư thế`, `Sai tư thế` khong bi cat |  |  |  |
| Bieu do ty le thoi gian hien dau dung |  |  |  |
| Bieu do canh bao theo phien hien dau dung |  |  |  |
| Xu huong 7 ngay hien dau dung |  |  |  |
| Bang phien hien heading co dau |  |  |  |
| Empty state database moi hien co dau |  |  |  |
| Nut `Xuất CSV`/`Đóng` khong bi cat |  |  |  |
| Messagebox export co dau |  |  |  |

Done khi:

- Cap nhat `reports/GUI_QA_CHECKLIST.md`.
- Neu co the, luu screenshot:
  - `reports/figures/dashboard_vietnamese_light.png`
  - `reports/figures/dashboard_vietnamese_dark.png`

## TASK-306: Sua baseline info panel

Muc tieu: che do Rule-based Baseline hien text co dau de demo de hieu.

Can sua:

- `Baseline: chưa chạy`
- `Chế độ: Rule-based Baseline`
- `Trạng thái`
- `Cảnh báo`
- `Đặc trưng`
- `Độ lệch vai y`
- `Góc nghiêng vai`
- `Góc nghiêng thân`
- `Độ lệch đầu x`
- `Mũi so với vai y`
- `Khoảng cách mũi-vai tỉ lệ`
- `Rụt cổ sâu`
- `Độ tin cậy landmark`
- `Tay trái gần miệng tỉ lệ`
- `Tay phải gần miệng tỉ lệ`
- `Phát hiện chống cằm`
- `Số lần cảnh báo baseline`

Done khi:

- Baseline panel doc duoc.
- Text wrap khong tran khung.

## TASK-307: Xu ly font Unicode trong CustomTkinter

Muc tieu: dam bao dau tieng Viet hien dep tren Windows.

Can lam:

- Chon font mac dinh co ho tro tieng Viet:
  - `Segoe UI`
  - fallback Windows mac dinh.
- Tao constant:

```python
APP_FONT_FAMILY = "Segoe UI"
```

- Thay cac `ctk.CTkFont(...)` quan trong thanh:

```python
ctk.CTkFont(family=APP_FONT_FAMILY, size=..., weight=...)
```

Khong can sua toan bo neu CustomTkinter da dung Segoe UI on dinh, nhung nen sua:

- Title label.
- Status label.
- Section title.
- Buttons.
- Dashboard title/KPI.

Done khi:

- Khong bi loi o/?, mojibake, dau bi mat.
- Font nhin dong nhat.

## TASK-308: Kiem tra encoding va mojibake

Muc tieu: tranh loi `Ä‘`, `á»`, `Æ°` xuat hien trong UI.

Lenh goi y:

```powershell
rg -n "Ä|á»|áº|Æ|Â|Ã" src reports workflow_kilo release_docs
```

Can lam:

- Neu chuoi mojibake nam trong comment/docstring thi co the ghi task cleanup rieng.
- Neu nam trong text UI thi phai sua ngay.
- Dam bao file Python luu UTF-8.

Done khi:

- Khong con mojibake trong text UI runtime.

## TASK-309: Cap nhat test/smoke test UI text

Muc tieu: dam bao app init va text co dau khong crash.

Can tao hoac cap nhat test:

- `tests/test_ui_vietnamese_text.py`

Noi dung test toi thieu:

- Import `src/4_main_desktop_app.py`.
- Kiem tra `STATUS_TEXT["DUNG_TU_THE"] == "TƯ THẾ ĐÚNG"`.
- Kiem tra mot vai mapping co dau.
- Kiem tra cac chuoi quan trong la `str` Unicode.

Lenh verify:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q
```

Done khi:

- Test pass.

## TASK-310: QA giao dien manual

Muc tieu: xem bang mat that, vi test tu dong khong bat duoc loi tran text.

Checklist:

| Hang muc | Light | Dark | Ghi chu |
|---|---|---|---|
| Main title co dau dung |  |  |  |
| Sidebar khong tran o 1080x640 |  |  |  |
| Label canh bao co dau dung |  |  |  |
| Button khong bi cat chu |  |  |  |
| Status `TƯ THẾ ĐÚNG` doc duoc |  |  |  |
| Status `SAI TƯ THẾ` doc duoc |  |  |  |
| Dashboard title/KPI co dau dung |  |  |  |
| Table headings khong bi loi font |  |  |  |
| Messagebox loi/thanh cong co dau dung |  |  |  |

Done khi:

- Cap nhat `reports/GUI_QA_CHECKLIST.md`.
- Neu can, chup screenshot `reports/figures/gui_vietnamese_light.png` va `gui_vietnamese_dark.png`.

## TASK-311: Rebuild desktop app

Muc tieu: ban `.exe` cung hien tieng Viet co dau.

Lenh:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q
.\.venv\Scripts\pyinstaller.exe --clean --noconfirm build_scripts/posture_app.spec
powershell -ExecutionPolicy Bypass -File build_scripts/smoke_test_dist.ps1
```

Sau do package release:

```powershell
powershell -ExecutionPolicy Bypass -File build_scripts/package_release.ps1 -Version "0.1.1-vietnamese-ui"
```

Done khi:

- `dist/PostureDetectionApp/PostureDetectionApp.exe` mo len hien co dau.
- Release zip moi duoc tao.

## TASK-312: Cap nhat release notes

Muc tieu: ghi ro ban moi da Viet hoa UI.

Can cap nhat:

- `release/VERSION.txt`
- `reports/DEPLOYMENT_RELEASE_NOTES.md`
- `release_docs/README_RUN_APP.md` neu text screenshot/huong dan thay doi.

Noi dung:

- Version: `0.1.1-vietnamese-ui`
- Change:
  - Vietnamese accented UI.
  - UTF-8 text audit.
  - Font QA for Windows.

Done khi:

- Release notes khop voi build moi.

## Thu tu uu tien

1. TASK-300
2. TASK-301
3. TASK-302
4. TASK-303
5. TASK-304
6. TASK-305
7. TASK-305A
8. TASK-305B
9. TASK-305C
10. TASK-305D
11. TASK-305E
12. TASK-306
13. TASK-307
14. TASK-308
15. TASK-309
16. TASK-310
17. TASK-311
18. TASK-312

## Definition of Done

- Toan bo UI nguoi dung thay duoc hien tieng Viet co dau.
- App chay bang Python khong loi Unicode.
- App build PyInstaller khong loi Unicode.
- Light/Dark mode deu doc duoc.
- Sidebar/dashboard khong tran text nghiem trong.
- `pytest` pass.
- Smoke test dist pass.
- Co release notes cho ban Viet hoa UI.
