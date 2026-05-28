# 08. Task UI light mode va thong ke app

Ngay cap nhat: 2026-05-27

Pham vi phan tich:

- `src/4_main_desktop_app.py`
- `src/3_database_setup.py`
- `src/10_export_statistics.py`
- `reports/GUI_QA_CHECKLIST.md`
- Du lieu local: `database/posture_app.db`

## Ket luan nhanh

Giao dien hien tai da chay duoc cho demo ky thuat, nhung chua dat muc polished product UI:

- App dang hard-code dark mode: `ctk.set_appearance_mode("dark")`.
- Layout chinh la video ben trai, control panel ben phai, phu hop cho demo realtime.
- Form cau hinh con day chu va nhieu nut text, chua co phan tach ro giua "nguon vao", "che do", "canh bao", "phien hien tai".
- Panel ben phai hien frame count dang la text nhieu dong, kho scan khi dang demo.
- Thong ke da co card, pie chart va bar chart, nhung con nam trong popup rieng va van hard-code mau dark.
- Phan thong ke truc quan o muc co ban, chua co trend theo ngay/gio, timeline phien, bang phien sortable, ty le khong phat hien nguoi, confidence trung binh, hoac risk index.
- Rule-based mode khong luu database, nen thong ke ngay hien tai chi phan anh ANN mode. UI can noi ro dieu nay de tranh hieu sai.

## Kiem chung hien tai

Lenh da chay:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q
# 15 passed, 1 skipped

python -m py_compile src/1_rule_based_baseline.py src/2_extract_features.py src/3_database_setup.py src/4_main_desktop_app.py src/5_train_ann_local.py src/6_evaluate_external.py src/7_video_wise_evaluation.py src/8_compare_algorithms.py src/9_ablation_study.py src/10_export_statistics.py src/11_statistical_analysis.py src/12_temporal_risk_index.py src/posture_baseline.py src/utils.py
# pass
```

Du lieu local dang co:

- `PhienLamViec`: 51 phien.
- `ThongKeNgay`: 9 ngay.
- `NhatKyTuThe`: 880 dong.
- `reports/results/session_risk_index.csv`: co TPRI/risk level theo phien.

## Danh gia giao dien hien tai

### Diem da dap ung

- Co video preview lon, phu hop muc tieu realtime.
- Co start/stop, luu cai dat, xem thong ke.
- Co chon nguon camera/video, thoi gian canh bao, cooldown, mode ANN/rule-based, bat/tat am thanh.
- Co label trang thai, do tin cay, timer sai tu the va overlay tren frame.
- Co cua so thong ke rieng voi card tong quan, pie chart thoi gian dung/sai/khac, bar chart canh bao theo phien.
- Co fallback chart bang `CTkProgressBar` neu thieu matplotlib.

### Diem chua dap ung

- Chua theo yeu cau light mode; nhieu mau dark hard-code trong app va popup thong ke.
- Chua co design token/tap trung mau sac, nen doi theme se phai sua rat nhieu dong.
- Khu control panel dang gom tat ca vao mot cot, thieu nhom logic va do uu tien thi giac.
- Status "DANG KIEM TRA" va counters chua duoc trinh bay nhu dashboard realtime.
- Thong ke popup kho doc tren man hinh nho do 5 card nam cung mot hang va hai chart nam hai cot.
- Danh sach phien la `CTkTextbox`, khong co cot, khong can le, khong sort/filter.
- Chua hien thong ke theo ngay truoc do mac du database co 9 ngay.
- Chua hien timeline/risk theo phien mac du da co script TPRI.
- Chua co export/open report tu UI.
- Chua co QA visual rieng cho light mode, mobile/small viewport khong lien quan nhung can test man hinh 1080x640 va 1366x768.

## Huong thiet ke de xuat

Muc tieu UI moi: light, ro rang, it mau nen dam, phu hop app cong cu/desktop demo.

De xuat bo cuc:

1. Main window
   - Nen tong the: `#f6f8fb`.
   - Video area ben trai giu la trong tam.
   - Sidebar ben phai chia section: Status, Input, Detection, Alert, Actions, Session summary.
   - Status card dung mau xanh/do/vang/xam nhe, chu dam, co chip mode ANN/rule-based.
   - Session summary doi tu text nhieu dong sang mini KPI: frame, correct, incorrect, no person, warning, FPS.

2. Statistics window
   - Chuyen thanh dashboard light mode.
   - Hang dau: KPI cards: total time, correct time, incorrect time, warning count, sessions, average confidence.
   - Hang chart: stacked time bar hoac donut, warnings by session, daily trend 7 ngay.
   - Bang phien: cot start/end, duration, correct %, incorrect %, no-person %, warnings, avg confidence, risk level neu co.
   - Them empty state va data quality note.

3. Code
   - Tao theme constants trong mot khu vuc rieng hoac module `src/ui_theme.py`.
   - Tach logic tao stats data khoi logic ve widget.
   - Khong refactor model/camera trong cung task voi UI.

## Quy trinh lam

Lam theo thu tu task, moi task nen verify rieng:

1. Lam theme token va light mode truoc.
2. Sua main layout nhung giu behavior.
3. Sua dashboard thong ke.
4. Tach data/query cho statistics.
5. Them QA va screenshot.

Trang thai task:

- `Todo`: chua lam.
- `Doing`: dang lam.
- `Blocked`: can du lieu/hardware.
- `Done`: da verify.

## Backlog task tuan tu

### TASK-055 - Lap inventory UI hien tai va mau hard-code

Uu tien: P0

Trang thai: Done

Muc tieu: biet chinh xac tat ca diem can doi khi chuyen sang light mode.

Pham vi:

- `src/4_main_desktop_app.py`
- Tao `reports/UI_INVENTORY.md`

Cach lam:

1. Liet ke cac khu UI: main window, video frame, sidebar, baseline panel, status labels, statistics popup, charts, dialogs.
2. Liet ke mau hard-code dang dung: `#1f1f1f`, `#2b2b2b`, `#242424`, `#f8fafc`, `#cbd5e1`, `#3f3f46`, v.v.
3. Ghi mau nao la semantic color: success, danger, warning, info, neutral.
4. Ghi widget nao dang co nguy co khong hop light mode.

Verify:

```powershell
Get-Content reports/UI_INVENTORY.md
```

Done khi:

- Co bang inventory ro rang de task sau sua khong sot.

Bang chung: `reports/UI_INVENTORY.md`.

### TASK-056 - Tao theme token light mode

Uu tien: P0

Trang thai: Done

Muc tieu: co bo mau va style tap trung, khong tiep tuc rai mau hard-code.

Pham vi:

- `src/4_main_desktop_app.py`
- Co the tao `src/ui_theme.py` neu muon tach file

Cach lam:

1. Doi `ctk.set_appearance_mode("dark")` thanh `ctk.set_appearance_mode("light")`.
2. Tao constants cho mau nen, surface, border, text, muted text, success, danger, warning, info.
3. De xuat palette:
   - App background: `#f6f8fb`
   - Surface: `#ffffff`
   - Surface muted: `#eef2f7`
   - Border: `#d7dde8`
   - Text: `#162033`
   - Muted text: `#5b677a`
   - Success: `#15803d`
   - Danger: `#dc2626`
   - Warning: `#b45309`
   - Info: `#2563eb`
4. Doi `STATUS_COLORS` sang mau doc tot tren nen sang.
5. Khong doi layout trong task nay, chi doi theme/token va mau co ban.

Verify:

```powershell
python -m py_compile src/4_main_desktop_app.py
```

Manual verify:

```powershell
.\.venv\Scripts\python.exe src/4_main_desktop_app.py
```

Done khi:

- App mo duoc light mode.
- Khong con mau dark chinh o main window.

Bang chung: `ctk.set_appearance_mode("light")` va `THEME` token trong `src/4_main_desktop_app.py`.

### TASK-057 - Refactor main layout thanh sidebar co nhom ro rang

Uu tien: P0

Trang thai: Done

Muc tieu: giao dien chinh de scan hon khi demo, khong con sidebar la mot chuoi input/nut dai.

Pham vi:

- `src/4_main_desktop_app.py`

Cach lam:

1. Giu video preview ben trai.
2. Doi `control_frame` thanh sidebar gom section:
   - Header app va status.
   - Source/Input.
   - Detection mode.
   - Alert settings.
   - Actions.
   - Live session summary.
3. Tao helper `create_section(parent, title)` neu giup giam lap code.
4. Doi counters trong `info_label` thanh mini KPI labels hoac compact grid.
5. Giu tat ca command hien tai: start, stop, save, stats.
6. Khong them icon neu chua co icon lib trong repo.

Verify:

```powershell
python -m py_compile src/4_main_desktop_app.py
```

Manual verify:

- App mo tren 1180x680 khong overflow.
- Sidebar doc duoc o minsize 1080x640.
- Start/Stop/Save/Stats van bam duoc.

Done khi:

- Control panel co nhom logic ro.
- Counter realtime khong con la text block kho doc.

Bang chung: sidebar da co section va mini KPI labels trong `src/4_main_desktop_app.py`.

### TASK-058 - Lam moi video area va baseline info panel theo light mode

Uu tien: P1

Trang thai: Done

Muc tieu: khu video va baseline debug nhin nhu mot tool surface sang, khong bi cam giac dark-theme con sot.

Pham vi:

- `src/4_main_desktop_app.py`

Cach lam:

1. Video frame nen trang, border nhe.
2. Placeholder "Chua bat camera" co subtitle ngan: "Chon nguon va bam Bat dau".
3. Baseline info panel doi thanh table/rows compact thay vi text block dai.
4. Warnings baseline hien bang list ngan, khong chi la chuoi multi-line.
5. Dam bao overlay tren video van doc duoc vi overlay nam tren frame anh, co the giu mau hien tai neu can.

Verify:

```powershell
python -m py_compile src/4_main_desktop_app.py
```

Manual verify:

- ANN mode an baseline panel.
- Rule-based mode hien baseline panel ro va khong day video qua muc.

Done khi:

- Light mode nhat quan ca video area va baseline panel.

Bang chung: video frame/baseline panel dung surface light va border token.

### TASK-059 - Thiet ke lai statistics popup thanh dashboard light mode

Uu tien: P0

Trang thai: Done

Muc tieu: phan thong ke truc quan, de doc, phu hop bao cao/demo.

Pham vi:

- `src/4_main_desktop_app.py`

Cach lam:

1. Doi background popup tu `#1f1f1f` sang light token.
2. Card KPI light surface, border nhe, title/value can le ro.
3. Chia dashboard thanh:
   - KPI row.
   - Time distribution chart.
   - Warnings/session chart.
   - Session table.
4. Tren man hinh hep, dung grid 1 cot thay vi ep 2 chart ngang neu can.
5. Them KPI:
   - Correct ratio.
   - Incorrect ratio.
   - No-person/unknown time ratio.
   - Average confidence neu co.
6. Empty state ro rang khi chua co data.

Verify:

```powershell
python -m py_compile src/4_main_desktop_app.py
```

Manual verify:

- Bam `Xem thong ke` khi co data.
- Bam `Xem thong ke` khi database moi/chua co phien.
- Text khong trang tren nen trang, khong con chart dark.

Done khi:

- Statistics window nhin nhu dashboard light mode, khong chi la popup dark doi mau mot phan.

Bang chung: `show_statistics` render dashboard light mode bang `render_statistics_dashboard`.

### TASK-060 - Doi chart tu pie-only sang bieu do de so sanh tot hon

Uu tien: P1

Trang thai: Done

Muc tieu: thong ke truc quan hon pie chart hien tai.

Pham vi:

- `src/4_main_desktop_app.py`

Cach lam:

1. Giu donut/pie neu muon, nhung bo sung stacked horizontal bar cho correct/incorrect/unknown.
2. Warnings by session chart nen gioi han 10-15 phien gan nhat de khong chen chu.
3. Them chart daily trend 7 ngay tu `ThongKeNgay`: total work, incorrect ratio, warnings.
4. Dung mau light chart:
   - Figure face: `#ffffff`
   - Axis/text: `#162033`
   - Grid: `#d7dde8`
5. Fallback chart cung doi sang light mode.

Verify:

```powershell
python -m py_compile src/4_main_desktop_app.py
```

Manual verify:

- Chart co nhan truc/legend de hieu.
- Nhieu phien trong ngay khong lam nhan x-axis chen nhau.

Done khi:

- Statistics khong chi tra loi "hom nay dung/sai bao nhieu", ma con cho thay xu huong va phien nao co nhieu canh bao.

Bang chung: da co stacked time distribution, warnings/session va daily trend chart.

### TASK-061 - Thay danh sach phien textbox bang bang phien co cot

Uu tien: P1

Trang thai: Done

Muc tieu: phien trong ngay doc duoc nhu bang, co ty le va canh bao ro rang.

Pham vi:

- `src/4_main_desktop_app.py`

Cach lam:

1. Thay `CTkTextbox` session list bang grid row hoac `ttk.Treeview` style light.
2. Cot toi thieu:
   - Ma phien
   - Bat dau
   - Thoi luong
   - Dung %
   - Sai %
   - Khong co nguoi %
   - Canh bao
   - FPS/frames hoac confidence trung binh
3. Format duration va percentage ro rang.
4. Neu qua nhieu dong, dung scroll.

Verify:

```powershell
python -m py_compile src/4_main_desktop_app.py
```

Manual verify:

- Bang hien dung voi 0 phien, 1 phien, nhieu phien.
- Cot khong bi cat o width 1000.

Done khi:

- Nguoi demo co the nhin tung phien va so sanh nhanh.

Bang chung: `create_session_table` dung `ttk.Treeview`.

### TASK-062 - Tich hop Temporal Risk Index vao statistics UI

Uu tien: P1

Trang thai: Done

Muc tieu: dua diem moi TPRI vao dashboard thay vi chi nam o report CSV.

Pham vi:

- `src/12_temporal_risk_index.py`
- `src/4_main_desktop_app.py`
- `reports/TEMPORAL_RISK_INDEX_METHOD.md`

Cach lam:

1. Tach core compute TPRI thanh ham co the import ma khong can CLI.
2. Trong statistics UI, tinh risk cho cac phien hom nay tu database hoac doc `session_risk_index.csv` neu vua generate.
3. Hien risk level trong bang phien: LOW/MEDIUM/HIGH/CRITICAL.
4. Them KPI: highest risk today, average risk today.
5. Ghi note: TPRI la diem ho tro bao cao/demo, khong phai chan doan y te.

Verify:

```powershell
python -m py_compile src/4_main_desktop_app.py src/12_temporal_risk_index.py
.\.venv\Scripts\python.exe -m pytest tests/test_temporal_risk_index.py -q
```

Manual verify:

- Statistics popup hien risk cho ngay co phien.
- Neu chua co log, hien data quality note thay vi crash.

Done khi:

- Dashboard co thong tin rui ro theo phien, khong chi frame count.

Bang chung: `src/statistics_service.py` tinh `riskIndex`/`riskLevel`; dashboard hien highest/average risk va risk theo phien.

### TASK-063 - Tach query thong ke khoi UI widget

Uu tien: P1

Trang thai: Done

Muc tieu: de test thong ke ma khong can mo Tkinter.

Pham vi:

- Tao `src/statistics_service.py`
- `src/4_main_desktop_app.py`
- Tao `tests/test_statistics_service.py`

Cach lam:

1. Chuyen `get_today_statistics` va `get_today_session_statistics` hoac ban moi sang service function.
2. Service nhan `db_path`, `date_text`.
3. Tra ve dict/list da tinh san percentage, duration, no-person ratio, avg confidence.
4. UI chi render data.
5. Unit test dung SQLite temp file voi schema toi thieu.

Verify:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_statistics_service.py -q
python -m py_compile src/statistics_service.py src/4_main_desktop_app.py
```

Done khi:

- Logic thong ke co test rieng, khong bi tron voi code widget.

Bang chung: `src/statistics_service.py`, `tests/test_statistics_service.py`.

### TASK-064 - Them date filter cho statistics

Uu tien: P2

Trang thai: Done

Muc tieu: xem lai ngay cu thay vi chi xem hom nay.

Pham vi:

- `src/4_main_desktop_app.py`
- `src/statistics_service.py` neu da co TASK-063

Cach lam:

1. Them combobox/list ngay tu `ThongKeNgay`.
2. Default la hom nay.
3. Khi doi ngay, reload KPI/charts/table.
4. Neu ngay khong co data, hien empty state.

Verify:

```powershell
python -m py_compile src/4_main_desktop_app.py
```

Manual verify:

- Chon ngay 2026-05-26 neu database local co data.
- Dashboard reload dung.

Done khi:

- Statistics khong bi gioi han vao ngay hien tai.

Bang chung: dashboard co `CTkComboBox` ngay va reload theo ngay duoc chon.

### TASK-065 - Them export/open report trong statistics UI

Uu tien: P2

Trang thai: Done

Muc tieu: nguoi dung lay du lieu thong ke de dua vao bao cao nhanh hon.

Pham vi:

- `src/4_main_desktop_app.py`
- `src/10_export_statistics.py`

Cach lam:

1. Them nut `Export CSV` trong statistics window.
2. Goi logic export tu `src/10_export_statistics.py` hoac subprocess an toan.
3. Sau khi export, messagebox hien output dir.
4. Co nut mo thu muc `reports/results` neu hop ly tren Windows.

Verify:

```powershell
python -m py_compile src/4_main_desktop_app.py src/10_export_statistics.py
```

Manual verify:

- Bam Export CSV sinh/ghi de file trong `reports/results`.

Done khi:

- Tu UI co the lay CSV thong ke ma khong can terminal.

Bang chung: nut `Export CSV` goi `src/10_export_statistics.py`.

### TASK-066 - Cap nhat GUI QA checklist cho light mode va dashboard

Uu tien: P0

Trang thai: Done

Muc tieu: co checklist test dung voi UI moi.

Pham vi:

- `reports/GUI_QA_CHECKLIST.md`

Cach lam:

1. Them case light mode:
   - Main window light mode khong con mau dark sot.
   - Sidebar khong overflow o 1080x640.
   - Status color doc duoc voi correct/incorrect/no-person/checking.
   - Statistics dashboard light mode.
2. Them case statistics:
   - No data state.
   - One session.
   - Many sessions.
   - Date filter neu co.
   - Risk level neu co.
   - Export CSV neu co.
3. Them cot screenshot path neu can.

Verify:

```powershell
Get-Content reports/GUI_QA_CHECKLIST.md
```

Done khi:

- Checklist phu hop UI moi, khong chi test chuc nang cu.

Bang chung: `reports/GUI_QA_CHECKLIST.md` da them case light mode/dashboard.

### TASK-067 - Chup screenshot va viet UI acceptance notes

Uu tien: P1

Trang thai: Blocked

Muc tieu: co bang chung giao dien da hoan thien.

Pham vi:

- `reports/UI_ACCEPTANCE_NOTES.md`
- `reports/figures/` hoac duong dan screenshot local

Cach lam:

1. Chup main window chua start.
2. Chup ANN running voi video/webcam.
3. Chup rule-based running.
4. Chup statistics dashboard co data.
5. Ghi nhan kich thuoc man hinh, ngay test, nguoi test, ket qua.
6. Khong commit anh co thong tin rieng tu neu khong muon cong khai.

Verify:

```powershell
Get-Content reports/UI_ACCEPTANCE_NOTES.md
```

Done khi:

- Co note va screenshot path de doi chieu giao dien.

Bang chung hien tai: `reports/UI_ACCEPTANCE_NOTES.md` da tao note; screenshot/manual QA van can thao tac GUI.

### TASK-068 - Sua encoding con lai trong database setup comments

Uu tien: P2

Trang thai: Done

Muc tieu: file lien quan GUI/database khong con mojibake trong docstring/comment.

Pham vi:

- `src/3_database_setup.py`

Cach lam:

1. Sua comment/docstring bi loi encoding.
2. Khong doi SQL schema, default data hoac logic.
3. Chi sua text.

Verify:

```powershell
python -m py_compile src/3_database_setup.py
```

Done khi:

- Comment/docstring doc duoc, khong con `Táº¡o`, `Báº£ng`, v.v.

Bang chung: kiem tra `src/3_database_setup.py` cho thay comment/docstring dang doc duoc; khong can doi logic.

## Thu tu de xuat

Lam theo cac dot sau:

1. Dot 1 - Nen tang UI: TASK-055, TASK-056, TASK-057.
2. Dot 2 - Hoan thien main app: TASK-058, TASK-066.
3. Dot 3 - Dashboard thong ke: TASK-059, TASK-060, TASK-061.
4. Dot 4 - Chat luong du lieu thong ke: TASK-062, TASK-063, TASK-064.
5. Dot 5 - Giao hang: TASK-065, TASK-067, TASK-068.

Neu can lam nhanh de demo, uu tien TASK-056, TASK-057, TASK-059, TASK-066 truoc.
