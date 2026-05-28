# Hướng Dẫn Chạy Posture Detection App

## Cách mở app

Mo file:

```text
PostureDetectionApp.exe
```

Lần đầu mở app có thể chậm vì app load TensorFlow, MediaPipe và model posture.

## Chọn nguồn đầu vào

### Webcam laptop

Nhap:

```text
0
```

Nếu webcam không mở được, thử `1` hoặc đóng các ứng dụng đang dùng camera.

### Video file

Nhập đường dẫn video, ví dụ:

```text
D:\Videos\demo_posture.mp4
```

Nếu video HEVC/H.265 không đọc được, hãy convert sang MP4 H.264.

### Camera IP

Nhập URL camera:

```text
http://...
rtsp://...
```

## Thao tác trong app

- `Bắt đầu`: chạy nhận diện.
- `Dừng`: dừng camera/video và lưu thống kê phiên.
- `Lưu cài đặt`: lưu camera, cảnh báo, smoothing, Light/Dark.
- `Xem thống kê`: mở dashboard phiên/ngày.
- `Light/Dark`: đổi giao diện.
- `Làm mượt xác suất`: số frame dùng để làm mượt dự đoán ANN.
- `Ngưỡng sai sau làm mượt`: ngưỡng xác suất để xem là sai tư thế.

## Dữ liệu runtime

Database của app nằm tại:

```text
%LOCALAPPDATA%\PostureDetectionApp\posture_app.db
```

Đây là nơi app lưu phiên làm việc, log cảnh báo và cấu hình người dùng.

## Lỗi thường gặp

| Lỗi | Cách xử lý |
|---|---|
| Windows SmartScreen cảnh báo | Bấm `More info` -> `Run anyway` nếu tin nguồn app. |
| App mở chậm | Bình thường trong lần đầu do load model và thư viện AI. |
| Không mở webcam | Đóng Zoom/Teams/Camera app, thử camera index `0` hoặc `1`. |
| Không đọc video | Convert video sang MP4 H.264. |
| Không có âm thanh | Kiểm tra loa và file `assets/sounds/alarm.wav` trong folder app. |

## Giới hạn

App là công cụ hỗ trợ nhắc nhở tư thế, không phải công cụ chẩn đoán y tế hay chứng nhận ergonomic.
