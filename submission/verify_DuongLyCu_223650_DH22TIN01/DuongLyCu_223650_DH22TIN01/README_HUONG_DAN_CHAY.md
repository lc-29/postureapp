# HƯỚNG DẪN CHẠY ỨNG DỤNG PHÁT HIỆN TƯ THẾ

## Thông tin sinh viên

- Họ tên: Dương Lý Cử
- MSSV: 223650
- Lớp: DH22TIN01

Đây là gói source code Python, model AI, SQLite có dữ liệu demo và hai video
để giảng viên kiểm tra trực tiếp. Ứng dụng hỗ trợ webcam, video file và camera
IP. Hệ thống chỉ hỗ trợ nhắc nhở tư thế, không phải công cụ chẩn đoán y tế.

## 1. Yêu cầu máy

- Windows 10 hoặc Windows 11 64-bit.
- Python 3.10 hoặc Python 3.11 64-bit.
- Khuyến nghị RAM từ 8 GB.
- Cần Internet trong lần đầu cài thư viện và khi gửi OTP.
- Webcam không bắt buộc vì gói đã có hai video demo.

Không khuyến nghị Python 3.12 trở lên vì phiên bản TensorFlow/MediaPipe trong
gói có thể không tương thích.

## 2. Cài đặt thư viện

Mở PowerShell tại thư mục `DuongLyCu_223650_DH22TIN01`, sau đó chạy:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Nếu PowerShell chặn kích hoạt môi trường ảo:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 3. Chạy ứng dụng

Sau khi kích hoạt môi trường ảo:

```powershell
python src\4_main_desktop_app.py
```

Hoặc nhấp đúp `run_app.bat` sau khi đã tạo `.venv` và cài thư viện.

Lần đầu khởi động có thể chậm vì TensorFlow, MediaPipe và các model cần được
nạp vào bộ nhớ.

## 4. Tài khoản demo

Database đã có dữ liệu lịch sử và tài khoản demo:

```text
Email: demo.posture@example.com
Mật khẩu: Demo@123
```

Tài khoản này đã xác thực email và có thể dùng để vào app ngay, không cần OTP.

## 5. Kiểm tra bằng webcam hoặc video

Tại ô nguồn đầu vào:

- Webcam mặc định: nhập `0`.
- Nếu máy có nhiều camera: thử `1`.
- Video tư thế đúng: chọn file
  `demo_videos\P01_correct_side_90_004.mp4`.
- Video tư thế sai: chọn file
  `demo_videos\P01_incorrect_001.mp4`.

Có thể nhập đường dẫn tương đối như trên hoặc dùng đường dẫn đầy đủ tới video
trong thư mục vừa giải nén.

Giao diện hiện có ba chế độ:

- `ANN`
- `HistGradientBoosting (balanced best)`
- `HistGradientBoosting (high recall demo)`
- Ngoài ra có `Rule-based Baseline` để đối chiếu luật hình học.

## 6. Cơ sở dữ liệu SQLite

File database:

```text
database\posture_app.db
```

Có thể mở bằng DB Browser for SQLite. Database chứa tài khoản demo, cấu hình,
phiên làm việc, nhật ký tư thế, thống kê ngày và thông tin model. Dữ liệu OTP
cũ và thông tin tài khoản cá nhân đã được xóa hoặc ẩn danh trong bản nộp.

Ứng dụng chạy từ source sử dụng trực tiếp file SQLite này. Không chạy
`src\3_database_setup.py` nếu muốn giữ dữ liệu demo hiện có, vì script đó dành
cho việc khởi tạo/reset database.

## 7. Đăng ký và gửi OTP thật

Gói nộp đã có `config\email_otp.local.config` để ứng dụng gửi OTP thật qua
SMTP. Máy cần kết nối Internet. Để kiểm tra:

1. Mở ứng dụng.
2. Chọn đăng ký tài khoản.
3. Nhập email mà người kiểm tra có thể mở hộp thư.
4. Nhập mật khẩu hợp lệ và bấm gửi OTP.
5. Lấy mã trong email rồi nhập vào ứng dụng để xác thực.

Thông tin gửi SMTP là thông tin bí mật. Không chia sẻ công khai file ZIP hoặc
file `config\email_otp.local.config`.

Nếu cấu hình có sẵn đã hết hiệu lực, người kiểm tra có thể dùng Gmail của mình:

```powershell
Copy-Item config\email_otp.example.config config\email_otp.local.config -Force
```

Sau đó điền Gmail và Gmail App Password vào file local. Gmail cần bật xác minh
hai bước. Có thể cấu hình bằng biến môi trường:

```powershell
$env:POSTURE_APP_FROM_EMAIL="your_email@gmail.com"
$env:POSTURE_APP_EMAIL_PASSWORD="your_gmail_app_password"
```

Không dùng mật khẩu đăng nhập Gmail chính. Sau khi hoàn tất chấm bài, sinh viên
sẽ thu hồi App Password đã dùng cho bản demo.

## 8. Cấu trúc chính

```text
src\                 Source code cần để chạy ứng dụng
assets\              Âm thanh cảnh báo
models\              ANN, scaler và hai model HGB của giao diện
database\            SQLite có dữ liệu demo
config\              Cấu hình mẫu và cấu hình SMTP runtime
demo_videos\         Hai video kiểm tra tư thế đúng/sai
requirements.txt     Danh sách thư viện Python
run_app.bat           Chạy nhanh sau khi đã cài môi trường
```

Dataset train, script train, notebook, benchmark và bản EXE không nằm trong
gói này vì không cần thiết để chạy ứng dụng.

## 9. Lỗi thường gặp

| Lỗi | Cách xử lý |
|---|---|
| Không cài được TensorFlow/MediaPipe | Dùng Python 3.10 hoặc 3.11 64-bit và tạo lại `.venv`. |
| PowerShell chặn activate | Dùng `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`. |
| Không mở được webcam | Đóng Camera, Zoom, Teams; thử camera `0` hoặc `1`. |
| Không đọc được video | Kiểm tra đường dẫn; dùng hai video có sẵn trong `demo_videos`. |
| Không gửi được OTP | Kiểm tra Internet, cấu hình SMTP và hiệu lực Gmail App Password. |
| Không nghe âm thanh | Kiểm tra loa và `assets\sounds\alarm.wav`. |
| App khởi động chậm | Chờ model và MediaPipe nạp xong trong lần đầu. |

## 10. Kiểm tra source tùy chọn

```powershell
python -m compileall -q src
```

Nếu lệnh không in lỗi thì source đã biên dịch cú pháp thành công.
