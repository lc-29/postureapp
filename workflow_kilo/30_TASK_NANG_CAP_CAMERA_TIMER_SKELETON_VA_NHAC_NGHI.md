# TASK 30 - NANG CAP CAMERA: BAT/TAT SKELETON, DEM GIO PHIEN VA NHAC NGHI

## 1. Muc tieu

Bo sung 3 cai tien cho ung dung desktop phat hien tu the:

1. Them nut bat/tat hien thi khung xuong skeleton tren khung camera.
2. Hien bo dem thoi gian lam viec dang chay o goc tren ben trai giao dien camera, dinh dang `gio:phut:giay`.
3. Cho nguoi dung cai dat thoi gian lam viec mong muon truoc khi bat dau, mac dinh 45 phut. Khi het gio, phat am thanh `assets/sounds/remind.wav`, hien thong bao:

```text
Bạn đã hết thời gian làm việc! Hãy nghỉ ngơi một chút
```

Khi het thoi gian va thong bao duoc hien len, app phai xu ly tuong duong nut `Dung` ngay lap tuc: dung camera/phien lam viec va luu day du vao SQLite nhu hanh vi hien tai. Nut `OK` tren thong bao chi dung de tat thong bao va quay lai trang thai app truoc khi bat dau phien moi.

Ung dung hien tai dang chay on dinh, vi vay task nay phai thuc hien theo huong them tinh nang nho, co kiem tra tung buoc, khong refactor lon va khong lam thay doi logic model/SQLite neu khong can.

## 2. Pham vi file du kien

Tap trung vao runtime app:

- `src/4_main_desktop_app.py`
- `src/app/config/constants.py`
- `assets/sounds/remind.wav` da ton tai va phai duoc dung lam am thanh nhac nghi.

Chi tao/sua file khac neu that su can thiet, va phai ghi ro ly do trong bao cao hoan thanh.

## 3. Hien trang can luu y

- App chinh van nam chu yeu trong `src/4_main_desktop_app.py`.
- Nut `Bat dau` dang goi `start_camera`.
- Nut `Dung` dang goi `stop_camera`.
- Skeleton MediaPipe dang duoc ve trong luong xu ly frame bang `mp_drawing.draw_landmarks`.
- Session runtime co cac bien lien quan:
  - `self.current_session_id`
  - `self.session_start_time`
  - `self.is_running`
  - `self.warning_count`
- Co san ham `get_current_session_duration_seconds`.
- Am thanh canh bao hien tai dung `ALARM_PATH` va co cac ham phat/dung am thanh rieng.
- `src/app/config/constants.py` dang co `ALARM_PATH = assets/sounds/alarm.wav`.

## 4. Nguyen tac bat buoc

- Khong xoa hoac doi schema SQLite neu khong bat buoc.
- Khong doi logic predict cua ANN/HGB/Rule-based.
- Khong doi nguong canh bao sai tu the neu khong lien quan.
- Khong lam mat hanh vi luu phien, log tu the, thong ke ngay va dashboard hien tai.
- Khi het gio va hien thong bao, phai goi dung luong dung phien hien co ngay tai thoi diem do de bao dam du lieu duoc luu nhu nut `Dung`.
- Nut `OK` tren thong bao chi dong messagebox; khong phai la hanh dong bat dau viec dung phien.
- Khong cho thong bao het gio hien lap lai nhieu lan trong cung mot phien.
- Neu nguoi dung bam `Dung` truoc khi het gio, khong phat `remind.wav` va khong hien message het gio.
- Neu chua bam `Bat dau`, bo dem phien nen ve `00:00:00` hoac trang thai rong theo thiet ke hien tai.
- Neu nguoi dung bat/tat skeleton khi camera dang chay, thay doi phai co hieu luc ngay tren frame tiep theo.
- Neu nguoi dung bat/tat skeleton khi camera dang dung, trang thai phai duoc ap dung cho lan chay tiep theo.

## 5. Yeu cau 1 - Nut bat/tat hien thi skeleton

### UI

Them mot control bat/tat skeleton trong khu dieu khien camera, gan voi cac nut `Bat dau` / `Dung`.

De xuat:

- Dung `CTkSwitch` hoac `CTkCheckBox`.
- Text ngan gon: `Hien skeleton`.
- Mac dinh: bat (`True`) de giu hanh vi hien tai.

### State

Them bien runtime:

```python
self.show_skeleton = True
```

Neu co he thong cau hinh luu trong SQLite/settings, co the luu them khoa:

```text
hienSkeleton = 1
```

Neu them setting vao config, phai co fallback an toan khi database cu chua co khoa nay.

### Xu ly frame

Tai doan ve skeleton, boc dieu kien:

```python
if self.show_skeleton:
    mp_drawing.draw_landmarks(...)
```

Yeu cau:

- Khi tat skeleton, van phai chay MediaPipe Pose de lay landmark va predict binh thuong.
- Khi tat skeleton, van giu label trang thai, canh bao, log va thong ke nhu cu.
- Tat skeleton chi an phan khung xuong ve len anh camera, khong tat nhan dien nguoi.

## 6. Yeu cau 2 - Bo dem gio phien o goc tren ben trai

### Hien thi tren giao dien

Hien bo dem nho o goc tren ben trai cua khung camera, dinh dang:

```text
HH:MM:SS
```

Vi du:

```text
00:12:35
01:05:09
```

Co the ve overlay truc tiep len frame bang OpenCV/PIL hoac dat label noi tren khung video. Uu tien cach it rui ro voi code hien tai.

### Yeu cau hien thi

- Bo dem chi dem khi phien dang chay.
- Bat dau tu `00:00:00` khi bam `Bat dau`.
- Cap nhat lien tuc theo frame hoac theo timer UI.
- Nam o goc tren ben trai, nho gon, de doc tren nen video.
- Nen co nen mo/nen toi nhe phia sau text de doc duoc tren video sang/toi.
- Khong che mat qua nhieu noi dung camera.

### Ham de xuat

Them helper:

```python
def format_duration_hhmmss(total_seconds: float) -> str:
    ...
```

Va helper ve overlay neu can:

```python
def draw_session_timer_overlay(frame: np.ndarray, text: str) -> np.ndarray:
    ...
```

## 7. Yeu cau 3 - Cai dat thoi gian lam viec mong muon

### UI truoc khi bat dau

Them khu nhap thoi gian lam viec truoc khi bam `Bat dau`.

Yeu cau:

- Mac dinh: 45 phut.
- Cho nguoi dung dieu chinh theo `gio:phut`.
- Co the dung 2 o nhap/stepper:
  - `Gio`
  - `Phut`
- Hoac dung mot o nhap dinh dang `HH:MM`.
- Uu tien UI de nhap dung, tranh de nguoi dung nhap chuoi sai.

De xuat an toan:

```text
Thoi gian lam viec
[Gio: 0] [Phut: 45]
```

### Validate

- Gio la so nguyen >= 0.
- Phut la so nguyen tu 0 den 59.
- Tong thoi gian phai > 0.
- Neu nhap sai, hien `messagebox.showerror` va khong bat dau camera.
- Gioi han de tranh nhap qua lon, de xuat toi da 12 gio.

### State runtime

Them cac bien:

```python
self.work_duration_seconds = 45 * 60
self.work_duration_reached = False
```

Khi `start_camera` thanh cong:

- Doc gia tri gio/phut tu UI.
- Luu vao `self.work_duration_seconds`.
- Reset `self.work_duration_reached = False`.
- Reset bo dem tu `self.session_start_time`.

Khi `stop_camera`:

- Reset/cap nhat state het gio de phien sau khong bi anh huong.

## 8. Xu ly khi het thoi gian lam viec

Trong vong lap cap nhat frame hoac sau khi tinh elapsed time:

1. Tinh elapsed seconds tu `self.session_start_time`.
2. Neu:
   - camera dang chay,
   - co phien dang chay,
   - `elapsed >= self.work_duration_seconds`,
   - `self.work_duration_reached == False`,

   thi:
   - set `self.work_duration_reached = True`;
   - dung camera/phien lam viec bang dung luong hien co tuong duong nut `Dung`;
   - phat `assets/sounds/remind.wav`;
   - hien messagebox:

```python
messagebox.showinfo(
    "Nhac nghi",
    "Bạn đã hết thời gian làm việc! Hãy nghỉ ngơi một chút",
)
```

3. Khi nguoi dung bam `OK`, chi dong thong bao. App luc nay da o trang thai sau khi dung phien: camera da tat, nut `Bat dau` san sang, nut `Dung` bi vo hieu hoa.

Yeu cau quan trong:

- Phai tranh goi `messagebox` truc tiep tu thread phu neu frame processing dang chay tren thread khac. Neu can, dung `self.root.after(...)` hoac co che UI thread hien co.
- Neu can hien messagebox sau khi goi `stop_camera`, phai sap xep de `stop_camera` chay truoc, sau do moi hien thong bao.
- Trong luc messagebox dang hien, khong de app tiep tuc bat nhieu thong bao.
- Tai thoi diem thong bao xuat hien, du lieu phien phai da duoc luu vao SQLite nhu bam nut `Dung`.

## 9. Am thanh nhac nghi

Them duong dan constant:

```python
REMIND_PATH = resource_path(Path("assets") / "sounds" / "remind.wav")
```

Yeu cau:

- Dung file `assets/sounds/remind.wav`.
- Neu file khong ton tai, app khong crash; van hien messagebox va ghi/print canh bao ngan gon.
- Am thanh nhac nghi doc lap voi am thanh canh bao sai tu the.
- Khong lam hong chuc nang bat/tat am thanh canh bao hien tai.
- Neu setting `batAmThanh` dang tat, can can nhac:
  - Cach 1: van phat remind vi day la nhac het gio lam viec.
  - Cach 2: ton trong setting am thanh chung va khong phat.

Lua chon khuyen nghi: ton trong `batAmThanh`; neu nguoi dung tat am thanh, chi hien messagebox. Neu muon remind bat buoc phat, can ghi ro trong UI/task report.

## 10. Luu cau hinh nguoi dung

Neu muon giu gia tri qua cac lan mo app, bo sung vao settings/config:

```text
hienSkeleton
thoiGianLamViecGio
thoiGianLamViecPhut
```

Mac dinh:

```text
hienSkeleton = 1
thoiGianLamViecGio = 0
thoiGianLamViecPhut = 45
```

Neu viec luu config lam tang rui ro, co the chi giu runtime trong task dau tien. Tuy nhien UI phai mac dinh 45 phut moi lan mo app.

## 11. Kiem thu bat buoc

### Syntax/import

Chay:

```powershell
.venv\Scripts\python.exe -m py_compile src\4_main_desktop_app.py
.venv\Scripts\python.exe -m py_compile src\app\config\constants.py
```

Neu co test phu hop:

```powershell
.venv\Scripts\python.exe -m pytest tests
```

### Smoke test thu cong

Chay app:

```powershell
.venv\Scripts\python.exe src\4_main_desktop_app.py
```

Kiem tra:

- Dang nhap duoc.
- Camera/video mo duoc bang nut `Bat dau`.
- Mac dinh skeleton dang hien.
- Tat `Hien skeleton`: skeleton bien mat nhung nhan dien va trang thai van cap nhat.
- Bat lai `Hien skeleton`: skeleton hien lai ngay.
- Bo dem hien tren goc tren ben trai va tang dung theo thoi gian.
- Dung camera truoc khi het gio: phien duoc luu, khong hien thong bao het gio.
- Dat thoi gian lam viec ngan de test, vi du `00:01`:
  - Sau khoang 1 phut, phat `remind.wav`.
  - Hien message `Bạn đã hết thời gian làm việc! Hãy nghỉ ngơi một chút`.
  - Ngay khi message xuat hien, camera da dung, nut `Bat dau` da bat lai, nut `Dung` da tat.
  - Bam `OK` chi dong message va quay lai app o trang thai san sang bat dau phien moi.
  - Phien duoc luu vao SQLite va xem duoc trong thong ke.
- Neu `remind.wav` bi thieu hoac khong phat duoc, app van hien message va khong crash.

## 12. Tieu chi hoan thanh

- Co nut/checkbox/switch bat tat skeleton tren giao dien.
- Skeleton mac dinh bat va co the tat/bat khi camera dang chay.
- Bo dem `HH:MM:SS` hien o goc tren ben trai camera trong phien lam viec.
- Co UI cho nguoi dung chon thoi gian lam viec `gio:phut`, mac dinh `0 gio 45 phut`.
- Het thoi gian thi phat `assets/sounds/remind.wav` neu am thanh duoc bat va file ton tai.
- Het thoi gian thi hien dung message:

```text
Bạn đã hết thời gian làm việc! Hãy nghỉ ngơi một chút
```

- Khi message het gio xuat hien, phien da duoc dung va luu nhu nut `Dung`.
- Bam `OK` tren message chi dong thong bao va quay lai app truoc khi bat dau phien moi.
- Du lieu phien het gio duoc luu vao SQLite va hien trong thong ke nhu phien dung thu cong.
- Khong co message het gio lap lai trong cung mot phien.
- Khong lam hong canh bao sai tu the, am thanh canh bao, dashboard thong ke va chuc nang login/register/OTP.
- Da chay syntax check va ghi lai ket qua.

## 13. Bao cao sau khi lam xong

Sau khi hoan thanh task, tao report ngan:

```text
reports/APP_CAMERA_TIMER_SKELETON_REMINDER_UPDATE_REPORT.md
```

Noi dung report gom:

1. File da sua.
2. Mo ta UI moi.
3. Cach bat/tat skeleton.
4. Cach cai dat thoi gian lam viec.
5. Cach xu ly khi het gio.
6. Kiem tra da chay va ket qua.
7. Gioi han con lai neu co.

## 14. Checklist thuc hien

- [ ] Doc lai luong `start_camera`, xu ly frame, ve skeleton va `stop_camera`.
- [ ] Them constant `REMIND_PATH`.
- [ ] Them state `show_skeleton`, `work_duration_seconds`, `work_duration_reached`.
- [ ] Them UI bat/tat skeleton.
- [ ] Them UI chon thoi gian lam viec gio/phut, mac dinh 0:45.
- [ ] Validate thoi gian truoc khi bat dau camera.
- [ ] Boc dieu kien cho `mp_drawing.draw_landmarks`.
- [ ] Them overlay bo dem `HH:MM:SS` o goc tren ben trai camera.
- [ ] Them logic phat remind va hien message khi het gio.
- [ ] Dam bao het gio la goi luong dung phien nhu nut `Dung` truoc hoac dong thoi voi luc hien message.
- [ ] Dam bao bam `OK` chi dong thong bao, khong moi bat dau dung phien.
- [ ] Kiem tra khong hien message lap lai.
- [ ] Chay `py_compile`.
- [ ] Smoke test camera/video.
- [ ] Kiem tra SQLite/thong ke sau phien het gio.
- [ ] Tao report hoan thanh.
