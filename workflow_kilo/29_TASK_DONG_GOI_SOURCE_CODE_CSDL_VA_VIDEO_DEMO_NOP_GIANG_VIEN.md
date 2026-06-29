# TASK 29 - ĐÓNG GÓI SOURCE CODE, SQLITE VÀ VIDEO DEMO NỘP GIẢNG VIÊN

## 1. Mục tiêu

Tạo gói nộp source code tối thiểu nhưng đầy đủ để giảng viên có thể:

1. Mở và đọc source code của ứng dụng.
2. Mở cơ sở dữ liệu SQLite có dữ liệu demo.
3. Cài thư viện từ `requirements.txt`.
4. Chạy ứng dụng trực tiếp từ source code.
5. Thử nhận diện bằng webcam hoặc hai video demo được cung cấp.
6. Kiểm tra chức năng đăng nhập, đăng ký và gửi OTP thật bằng tài khoản email
   demo dành riêng cho dự án.

Đây là gói **source code chạy từ Python**, không phải bản EXE/PyInstaller.

Tên file ZIP bắt buộc:

```text
DuongLyCu_223650_DH22TIN01.zip
```

## 2. Nguyên tắc thực hiện

- Chỉ sao chép file vào thư mục staging mới; không di chuyển, sửa hoặc xóa file gốc.
- Không dùng `.venv`, `build`, `dist` hoặc `release` làm nguồn chạy.
- Không đóng gói toàn bộ project.
- Không đưa mật khẩu hoặc Gmail App Password của tài khoản email cá nhân vào
  ZIP.
- Được đưa cấu hình SMTP thật vào ZIP chỉ khi đó là tài khoản Gmail demo dành
  riêng cho dự án, không chứa thư cá nhân và chủ tài khoản chấp nhận thu hồi
  App Password ngay sau khi giảng viên chấm xong.
- Không đưa lịch sử Git, cache Python hay kết quả nghiên cứu không cần cho runtime vào ZIP.
- Nếu cần làm sạch dữ liệu nhạy cảm trong SQLite, chỉ thao tác trên **bản sao trong staging**.
- Không reset hoặc ghi đè `database/posture_app.db` gốc.
- Sau khi tạo ZIP phải giải nén sang một thư mục kiểm tra mới và chạy kiểm tra từ bản giải nén.

## 3. Đường dẫn dự án

```text
D:\posture_detection_app
```

Tạo vùng staging:

```text
D:\posture_detection_app\submission\DuongLyCu_223650_DH22TIN01
```

File kết quả:

```text
D:\DuongLyCu_223650_DH22TIN01.zip
```

Nếu thư mục staging đã tồn tại, kiểm tra đường dẫn tuyệt đối nằm trong
`D:\posture_detection_app\submission` trước khi xóa bản staging cũ. Nếu file
ZIP đã tồn tại, chỉ được xóa sau khi xác nhận đường dẫn tuyệt đối chính xác là
`D:\DuongLyCu_223650_DH22TIN01.zip`.

## 4. Cấu trúc ZIP bắt buộc

```text
DuongLyCu_223650_DH22TIN01/
├── README_HUONG_DAN_CHAY.md
├── requirements.txt
├── run_app.bat
├── src/
│   ├── 3_database_setup.py
│   ├── 4_main_desktop_app.py
│   ├── 12_temporal_risk_index.py
│   ├── auth_service.py
│   ├── feature_schema.py
│   ├── posture_baseline.py
│   ├── runtime_paths.py
│   ├── statistics_service.py
│   └── app/
├── assets/
│   └── sounds/
│       └── alarm.wav
├── models/
│   ├── ann_best.keras
│   ├── scaler.pkl
│   └── registry/
│       ├── hist_gradient_boosting__ergonomic_v2_with_view/
│       │   ├── model.pkl
│       │   ├── feature_schema.json
│       │   ├── metrics.json
│       │   └── threshold.json
│       └── hist_gradient_boosting__normalized_99/
│           ├── model.pkl
│           ├── feature_schema.json
│           ├── metrics.json
│           └── threshold.json
├── database/
│   └── posture_app.db
├── config/
│   ├── email_otp.example.config
│   └── email_otp.local.config
└── demo_videos/
    ├── P01_correct_side_90_004.mp4
    └── P01_incorrect_001.mp4
```

Phải sao chép nguyên vẹn toàn bộ package `src/app/`, bao gồm các file
`__init__.py` và các thư mục con cần thiết.

## 5. Hai video demo bắt buộc

Sao chép:

```text
D:\posture_detection_app\dataset\raw_videos\correct\P01_correct_side_90_004.mp4
D:\posture_detection_app\dataset\raw_videos\incorrect\P01_incorrect_001.mp4
```

Đến:

```text
demo_videos\P01_correct_side_90_004.mp4
demo_videos\P01_incorrect_001.mp4
```

Không đưa các video khác hoặc toàn bộ thư mục `dataset` vào gói nộp.

## 6. Source code được phép đưa vào

Chỉ đưa các module runtime sau:

- `src/4_main_desktop_app.py`: entrypoint ứng dụng.
- `src/3_database_setup.py`: tạo và cập nhật schema SQLite.
- `src/12_temporal_risk_index.py`: tính chỉ số rủi ro cho thống kê.
- `src/auth_service.py`: đăng nhập, đăng ký, OTP và SMTP.
- `src/feature_schema.py`: xây dựng đặc trưng cho model.
- `src/posture_baseline.py`: chế độ rule-based.
- `src/runtime_paths.py`: xác định đường dẫn tài nguyên và SQLite.
- `src/statistics_service.py`: dữ liệu dashboard thống kê.
- Toàn bộ `src/app/`: cấu hình, repository, service và utility của app.

Không đưa các script train, trích xuất dataset, benchmark, tạo biểu đồ,
notebook hoặc đánh giá nghiên cứu vào ZIP.

Trước khi đóng gói, dùng tìm kiếm import và chạy `compileall` để xác nhận danh
sách trên không thiếu dependency Python nội bộ. Nếu phát hiện module runtime
thực sự cần thêm, được phép bổ sung module đó và phải ghi lại lý do trong báo
cáo hoàn thành task.

## 7. Model được phép đưa vào

Chỉ đưa model mà giao diện hiện tại sử dụng:

### ANN

```text
models\ann_best.keras
models\scaler.pkl
```

### HistGradientBoosting

```text
models\registry\hist_gradient_boosting__ergonomic_v2_with_view\
models\registry\hist_gradient_boosting__normalized_99\
```

Không đưa:

- `models/full_protocol_benchmark/`
- `models/local_training/`
- Các model registry khác không xuất hiện trong lựa chọn của GUI.
- Ảnh, log, checkpoint hoặc artifact train không cần cho runtime.

## 8. SQLite có dữ liệu demo

Nguồn:

```text
D:\posture_detection_app\database\posture_app.db
```

Đích:

```text
database\posture_app.db
```

Yêu cầu:

1. Database trong ZIP phải vượt qua `PRAGMA integrity_check`.
2. Giữ lại dữ liệu demo ở các bảng phiên làm việc, nhật ký và thống kê.
3. Xóa OTP còn hiệu lực hoặc dữ liệu OTP không cần thiết khỏi bản sao.
4. Không để email cá nhân, mật khẩu SMTP hoặc thông tin nhạy cảm trong bản nộp.
5. Nếu database cần tài khoản để đăng nhập, tạo hoặc giữ một tài khoản demo và
   ghi thông tin đăng nhập demo trong README.
6. Không thay đổi database gốc.
7. Kiểm tra ứng dụng chạy từ source thực sự sử dụng
   `database\posture_app.db` trong thư mục đã giải nén.

Nếu việc ẩn danh tài khoản có nguy cơ làm hỏng khóa ngoại hoặc đăng nhập, dừng
và báo rõ trước khi thay đổi dữ liệu; không tự ý phá cấu trúc database.

## 9. Chức năng OTP gửi email thật

Phải đưa vào:

```text
src\auth_service.py
config\email_otp.example.config
config\email_otp.local.config
```

`config\email_otp.local.config` phải dùng thông tin của một tài khoản Gmail
demo dành riêng cho dự án. Không dùng Gmail cá nhân, Gmail trường học chính
hoặc tài khoản có dữ liệu quan trọng.

Tuyệt đối không đưa vào ZIP:

```text
config\email_otp.local.ini
```

Yêu cầu đối với tài khoản gửi OTP:

1. Là tài khoản mới hoặc tài khoản chỉ dùng cho demo dự án.
2. Đã bật xác minh hai bước.
3. Dùng Gmail App Password, không dùng mật khẩu đăng nhập chính.
4. Không có email cá nhân, tài liệu, liên hệ hoặc dữ liệu quan trọng.
5. Chỉ chia sẻ ZIP qua Drive giới hạn người nhận là giảng viên; không đặt link
   công khai.
6. Không ghi App Password ra terminal, log, báo cáo hoàn thành hoặc câu trả lời
   của Codex.
7. Sau khi giảng viên chấm xong, thu hồi App Password tại Google Account và
   đổi mật khẩu nếu nghi ngờ file đã bị chia sẻ ra ngoài.

Trước khi đóng gói, Codex phải:

1. Xác nhận `config\email_otp.local.config` tồn tại và có đủ `fromEmail`,
   `password`, `smtpHost`, `smtpPort`, `useTls`.
2. Không in giá trị `password` khi kiểm tra.
3. Gửi một OTP thử đến địa chỉ kiểm thử do sinh viên kiểm soát và xác nhận SMTP
   hoạt động. Không đưa mã OTP thử vào báo cáo.
4. Xóa OTP thử khỏi bản sao SQLite trước khi nén nếu OTP đó không cần cho demo.
5. Nếu cấu hình hiện tại là tài khoản cá nhân hoặc không xác định được đây là
   tài khoản demo, dừng task và yêu cầu sinh viên cung cấp tài khoản demo; không
   tự ý đóng gói secret cá nhân.

README phải giải thích:

1. Gói nộp đã có cấu hình tài khoản demo để gửi OTP thật.
2. Giảng viên chỉ cần có Internet, đăng ký bằng email nhận OTP và kiểm tra hộp
   thư để lấy mã.
3. Nếu cấu hình demo đã được thu hồi hoặc hết hiệu lực, có thể thay bằng cấu
   hình của người kiểm tra bằng cách sao chép lại file mẫu:

```powershell
Copy-Item config\email_otp.example.config config\email_otp.local.config
```

4. Điền email gửi và Gmail App Password của người kiểm tra.
5. Có thể dùng các biến môi trường:

```powershell
$env:POSTURE_APP_FROM_EMAIL="your_email@gmail.com"
$env:POSTURE_APP_EMAIL_PASSWORD="your_gmail_app_password"
```

Không ghi Gmail App Password trực tiếp trong README. Secret chỉ được nằm trong
`config\email_otp.local.config` của bản nộp riêng cho giảng viên.

## 10. Nội dung README bắt buộc

Tạo mới:

```text
README_HUONG_DAN_CHAY.md
```

README phải viết tiếng Việt có dấu, lưu UTF-8 và bao gồm:

### 10.1. Thông tin sinh viên

```text
Họ tên: Dương Lý Cử
MSSV: 223650
Lớp: DH22TIN01
```

### 10.2. Yêu cầu máy

- Windows 10/11 64-bit.
- Python 3.10 hoặc Python 3.11 64-bit.
- Khuyến nghị RAM từ 8 GB.
- Internet trong lần đầu cài thư viện.
- Webcam hoặc một trong hai video demo.

### 10.3. Cài đặt

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Nếu PowerShell chặn activate:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 10.4. Chạy ứng dụng

```powershell
python src\4_main_desktop_app.py
```

Hoặc nhấp đúp:

```text
run_app.bat
```

### 10.5. Nguồn video

- Webcam mặc định: nhập `0`.
- Video tư thế đúng:

```text
demo_videos\P01_correct_side_90_004.mp4
```

- Video tư thế sai:

```text
demo_videos\P01_incorrect_001.mp4
```

README phải nói rõ đường dẫn tương đối hoặc hướng dẫn chọn file từ thư mục đã
giải nén, không dùng đường dẫn tuyệt đối trên máy sinh viên.

### 10.6. SQLite

- File: `database\posture_app.db`.
- Có thể mở bằng DB Browser for SQLite.
- Ghi tài khoản/mật khẩu demo nếu có.
- Giải thích dữ liệu lịch sử và thống kê đã được chuẩn bị để kiểm tra.

### 10.7. OTP

Ghi hướng dẫn sử dụng OTP thật từ mục 9, nêu rõ cần Internet và cảnh báo không
chia sẻ ZIP ra ngoài. Không hiển thị Gmail App Password trong README.

### 10.8. Lỗi thường gặp

- Không mở được webcam: đóng Camera/Zoom/Teams, thử `0` hoặc `1`.
- Không cài được TensorFlow/MediaPipe: dùng Python 3.10/3.11 64-bit.
- PowerShell chặn activate: dùng `Set-ExecutionPolicy -Scope Process`.
- Không gửi được OTP: kiểm tra Internet, SMTP và Gmail App Password.
- Video không đọc được: kiểm tra đường dẫn và codec; hai video kèm theo phải
  được dùng làm dữ liệu demo chuẩn.
- Lần đầu load model có thể chậm.

## 11. `run_app.bat`

Được phép dùng file hiện tại nhưng phải kiểm tra nó chạy đúng khi được gọi tại
thư mục gốc của gói đã giải nén.

Nội dung mong muốn:

```bat
@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo Chua tim thay moi truong ao .venv.
    echo Hay lam theo README_HUONG_DAN_CHAY.md de cai dat.
    pause
    exit /b 1
)
".venv\Scripts\python.exe" "src\4_main_desktop_app.py"
pause
```

Chỉ sửa `run_app.bat` gốc nếu được xác định là thay đổi phù hợp với project.
Nếu không muốn sửa file gốc, tạo phiên bản đã cải thiện trong staging.

## 12. Thành phần tuyệt đối không được đưa vào ZIP

```text
.git\
.agents\
.tools\
.venv\
.pytest_cache\
__pycache__\
build\
dist\
release\
dataset\
docs\
notebooks\
outputs\
reports\
springer_overleaf\
tmp\
tools\
uml_chuong_3\
workflow_kilo\
config\email_otp.local.ini
*.zip cũ
*.pyc
```

Ngoại lệ duy nhất đối với `dataset` là hai video cụ thể ở mục 5, nhưng chúng
phải được sao chép sang `demo_videos/`, không giữ cấu trúc `dataset/`.

Ngoại lệ duy nhất đối với secret là `config\email_otp.local.config` của tài
khoản Gmail demo riêng cho dự án, theo đầy đủ điều kiện an toàn tại mục 9.

## 13. Kiểm tra trước khi nén

Thực hiện tối thiểu:

```powershell
python -m compileall -q src
```

Kiểm tra tồn tại và load được:

- ANN Keras.
- Scaler.
- Hai model HGB.
- Hai file threshold/schema HGB.
- File âm thanh.
- Hai video demo.
- SQLite.

Kiểm tra SQLite:

```sql
PRAGMA integrity_check;
```

Kết quả bắt buộc:

```text
ok
```

Kiểm tra video bằng OpenCV:

- Mở được cả hai video.
- Đọc được ít nhất một frame.
- Ghi nhận kích thước, FPS và số frame trong báo cáo hoàn thành.

## 14. Nén và kiểm tra lại từ ZIP

1. Tạo `DuongLyCu_223650_DH22TIN01.zip` sao cho trong ZIP có một thư mục gốc
   tên `DuongLyCu_223650_DH22TIN01`.
2. Giải nén ZIP sang:

```text
D:\posture_detection_app\submission\verify_DuongLyCu_223650_DH22TIN01
```

3. Không dùng file từ project gốc trong quá trình kiểm tra.
4. Từ thư mục vừa giải nén:
   - Kiểm tra compile source.
   - Kiểm tra import entrypoint và các module nội bộ.
   - Kiểm tra load model/scaler.
   - Kiểm tra SQLite integrity và số dòng các bảng chính.
   - Kiểm tra đọc hai video.
5. Nếu có thể, chạy smoke test giao diện từ môi trường hiện tại và xác nhận app
   mở tới màn hình đăng nhập. Không để tiến trình GUI chạy nền sau khi test.

## 15. Tiêu chí hoàn thành

- Có file:

```text
D:\DuongLyCu_223650_DH22TIN01.zip
```

- ZIP có đúng một thư mục gốc cùng tên.
- Source trong ZIP chạy độc lập sau khi cài `requirements.txt`.
- Không phụ thuộc đường dẫn tuyệt đối `D:\posture_detection_app`.
- Có đúng hai video demo yêu cầu.
- Không có toàn bộ dataset hoặc script train/benchmark không cần thiết.
- Có SQLite hợp lệ và dữ liệu demo.
- Có đầy đủ model mà GUI cho phép chọn.
- Có chức năng OTP, file cấu hình mẫu và SMTP secret chỉ thuộc tài khoản demo
  riêng cho dự án.
- Chức năng OTP gửi được email thật bằng tài khoản demo riêng cho dự án.
- Không có secret của tài khoản email cá nhân.
- README nhắc thu hồi Gmail App Password sau khi chấm xong.
- Có README tiếng Việt hướng dẫn cài đặt, chạy, video, SQLite, tài khoản demo,
  OTP và xử lý lỗi.
- Báo cáo dung lượng ZIP, SHA-256 và kết quả từng bước kiểm tra.

## 16. Đầu ra Codex cần báo cáo

Sau khi hoàn thành, trả lời ngắn gọn:

1. Đường dẫn file ZIP.
2. Dung lượng file ZIP.
3. SHA-256.
4. Danh sách source/model/database/video đã đưa vào.
5. Kết quả compile/import/model/SQLite/video/smoke test.
6. Các thay đổi làm sạch dữ liệu demo.
7. Kết quả kiểm tra OTP, nhưng không được in email đầy đủ, App Password hoặc mã
   OTP.
8. Cảnh báo còn lại, nếu có.
