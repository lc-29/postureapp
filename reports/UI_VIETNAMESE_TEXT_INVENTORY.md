# UI Vietnamese Text Inventory

Ngày cập nhật: 2026-05-27

## Mục tiêu

Chuẩn hóa các chuỗi giao diện từ tiếng Việt không dấu sang tiếng Việt có dấu cho app desktop CustomTkinter.

## Mapping Chính

| Text hiện tại | Text mới |
|---|---|
| `Ung dung phat hien tu the lam viec` | `Ứng dụng phát hiện tư thế làm việc` |
| `Chua bat camera` | `Chưa bật camera` |
| `Chon nguon va bam Bat dau` | `Chọn nguồn và bấm Bắt đầu` |
| `PHAT HIEN TU THE` | `PHÁT HIỆN TƯ THẾ` |
| `Realtime posture monitoring` | `Giám sát tư thế theo thời gian thực` |
| `Giao dien` | `Giao diện` |
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
| `Export CSV` | `Xuất CSV` |
| `Dong` | `Đóng` |

## Status

| Status code | Text hiển thị |
|---|---|
| `DANG_KIEM_TRA` | `ĐANG KIỂM TRA...` |
| `DUNG_TU_THE` | `TƯ THẾ ĐÚNG` |
| `SAI_TU_THE` | `SAI TƯ THẾ` |
| `KHONG_PHAT_HIEN_NGUOI` | `KHÔNG PHÁT HIỆN NGƯỜI` |

## Dashboard

| Nhóm | Text mới |
|---|---|
| KPI tổng thời gian | `Tổng thời gian` |
| KPI đúng tư thế | `Đúng tư thế` |
| KPI sai tư thế | `Sai tư thế` |
| KPI cảnh báo | `Cảnh báo` |
| KPI độ tin cậy | `Độ tin cậy TB` |
| KPI rủi ro | `Rủi ro cao nhất`, `Rủi ro trung bình` |
| Biểu đồ thời gian | `Tỷ lệ thời gian`, `Đúng tư thế`, `Sai tư thế`, `Không xác định` |
| Biểu đồ cảnh báo | `Cảnh báo theo phiên`, `Số cảnh báo` |
| Xu hướng | `Xu hướng 7 ngày gần nhất`, `Sai tư thế (%)` |
| Bảng phiên | `Bắt đầu`, `Thời lượng`, `Đúng`, `Sai`, `Không người`, `Cảnh báo`, `Tin cậy`, `Rủi ro` |

## Ghi Chú

- Mã trạng thái nội bộ và tên cột SQLite giữ nguyên không dấu để không ảnh hưởng logic.
- Font UI ưu tiên `Segoe UI`.
- Overlay video dùng PIL text rendering để hỗ trợ Unicode thay vì `cv2.putText` trực tiếp.
