# PHÂN TÍCH ĐỒNG BỘ TÀI KHOẢN VÀ DỮ LIỆU ONLINE

Ngày rà soát: 27/06/2026  
Dự án: Xây dựng ứng dụng phát hiện lỗi tư thế làm việc qua webcam sử dụng Computer Vision

## Phạm vi và quy ước trạng thái

Báo cáo này chỉ đọc mã nguồn, cấu trúc CSDL và artifact hiện có. Không có mã nguồn, schema SQLite, giao diện, model hoặc dữ liệu nào được sửa trong lần phân tích này.

Các ký hiệu được dùng:

- **Đã triển khai**: có mã nguồn và đang nằm trên luồng chạy chính.
- **Có mã, chưa kiểm thử đầy đủ**: đã có implementation nhưng bằng chứng kiểm thử chưa bao phủ toàn bộ GUI/bản đóng gói.
- **Thiết kế đề xuất**: chưa có trong dự án.
- **Hướng phát triển**: không nên đưa vào phạm vi bắt buộc trước bảo vệ.

Kết luận ngắn:

> Dự án hiện là ứng dụng local-first. Tài khoản, OTP, cấu hình, phiên và thống kê đều nằm trong SQLite. Chưa có Auth trực tuyến, UUID cloud, token, hàng đợi đồng bộ hoặc tải dữ liệu đa thiết bị. Phương án phù hợp nhất là **Supabase Auth + Supabase PostgreSQL/RLS + SQLite cache/outbox**, triển khai tối thiểu theo hướng chỉ đồng bộ dữ liệu tổng hợp của phiên, giữ toàn bộ suy luận AI và dữ liệu chi tiết tại máy.

---

## 1. Tóm tắt kiến trúc hiện tại

### 1.1. Tệp khởi động và luồng thực thi thật

| Thành phần | Trạng thái | Căn cứ mã nguồn |
|---|---|---|
| Entry point dùng khi chạy source | Đã triển khai | `run_app.bat` gọi `python src/4_main_desktop_app.py`; hàm `main()` tạo `PostureApp` tại `src/4_main_desktop_app.py:4128` |
| Entry point package mới | Đã triển khai ở mức wrapper | `src/app/main.py:14` import lại module `4_main_desktop_app` và gọi `legacy_app.main()` |
| GUI thực tế | Đã triển khai | Class `PostureApp` vẫn nằm trong `src/4_main_desktop_app.py:634` |
| Controller mới | Chưa triển khai | `src/app/controllers/app_controller.py`, `auth_controller.py`, `camera_controller.py` chỉ là placeholder |
| UI package mới | Chưa triển khai | `src/app/ui/main_window.py`, `auth_view.py`, `dashboard_view.py` chỉ là placeholder |
| Repository mới | Phần lớn chưa triển khai | Chỉ `src/app/repositories/database.py:get_db_connection()` có logic; các repository user/settings/session/posture log vẫn là placeholder |
| Model service mới | Đã có logic | `src/app/services/model_service.py` tải HGB, threshold và tạo feature matrix |

Như vậy, cấu trúc `src/app/` chưa thay thế implementation cũ. Khi thiết kế đồng bộ, không được giả định controller/repository đã hoạt động. Nên triển khai cloud thành service/repository riêng rồi tích hợp từng bước vào `PostureApp`.

### 1.2. Bản đồ module nghiệp vụ

| Nghiệp vụ | Tệp/hàm thực tế |
|---|---|
| Đăng ký, đăng nhập, OTP | `src/auth_service.py`; các hàm `register_and_send_otp()`, `verify_registration_otp()`, `authenticate_user()` |
| Form xác thực | `PostureApp.show_auth_screen()`, `handle_login()`, `handle_send_registration_otp()`, `handle_verify_registration_otp()` |
| Kết nối SQLite | `src/app/repositories/database.py:get_db_connection()` gọi `src/runtime_paths.py:ensure_runtime_database()` |
| Schema và migration local | `src/3_database_setup.py:create_tables()`, `create_indexes()`, `ensure_thongke_ngay_user_scope()` |
| Cài đặt người dùng | `PostureApp.load_cai_dat()`, `save_cai_dat_from_gui()`, `save_cai_dat_silent()` |
| Phiên làm việc | `PostureApp.start_phien_lam_viec()`, `end_phien_lam_viec()` |
| Nhật ký/cảnh báo | `PostureApp.insert_nhat_ky_tu_the()`, `handle_warning_logic()`, `handle_status_logging()` |
| Thống kê ngày | `PostureApp.update_thong_ke_ngay()` |
| Dashboard | `src/statistics_service.py:get_dashboard_data()` và `PostureApp.show_statistics()` |
| Xuất CSV | `PostureApp.export_statistics_from_ui()` gọi `src/10_export_statistics.py` |
| ANN | `PostureApp.load_ai_components()`, `predict_frame_ann()` |
| HGB | `src/app/services/model_service.py` và `PostureApp.predict_frame_hgb()` |
| Rule-based | `PostureApp.predict_frame_rule_based()`; cố ý không lưu CSDL |
| Đường dẫn runtime/PyInstaller | `src/runtime_paths.py` |

### 1.3. Vị trí tài nguyên và dữ liệu

| Loại | Development/source | Bản PyInstaller theo thiết kế |
|---|---|---|
| SQLite | `D:\posture_detection_app\database\posture_app.db` | `%LOCALAPPDATA%\PostureDetectionApp\posture_app.db` |
| ANN | `models/ann_best.keras` | Resource cục bộ đóng gói |
| ANN scaler | `models/scaler.pkl` | Resource cục bộ đóng gói |
| HGB chính | `models/registry/hist_gradient_boosting__ergonomic_v2_with_view/model.pkl` | Chưa được thêm vào `build_scripts/posture_app.spec` hiện tại |
| HGB threshold | `.../threshold.json`, giá trị `0.76` | Chưa được thêm vào spec hiện tại |
| HGB feature schema artifact | `.../feature_schema.json`, 31 cột | Tồn tại nhưng GUI hiện không đọc để validate |
| Âm thanh | `assets/sounds/alarm.wav` | Có trong PyInstaller spec |

`src/runtime_paths.py:writable_database_path()` có hai hành vi:

- Chạy source: dùng `PROJECT_ROOT/database/posture_app.db`.
- Chạy frozen: dùng `%LOCALAPPDATA%\PostureDetectionApp\posture_app.db`.
- Có thể override bằng `POSTURE_APP_DB` hoặc `POSTURE_APP_USER_DATA_DIR`.

### 1.4. Trạng thái kiểm thử quan sát được

Đã chạy:

```text
pytest tests/test_auth_service.py
       tests/test_statistics_service.py
       tests/test_model_registry_service.py
       tests/test_feature_schema.py -q
```

Kết quả: **15 passed, 2 failed**.

Hai lỗi nằm trong `tests/test_statistics_service.py`: test fixture vẫn tạo schema cũ không có `NguoiDung` và không có `PhienLamViec.maNguoiDung`, trong khi service hiện yêu cầu schema theo người dùng. Đây là dấu hiệu test chưa theo kịp migration user-scoped; không đủ căn cứ để nói toàn bộ statistics test đang xanh.

---

## 2. Vấn đề của SQLite hiện tại

### 2.1. Trường hợp không mất dữ liệu

- Khi cập nhật hoặc thay file `.exe` trên cùng máy mà không xóa `%LOCALAPPDATA%\PostureDetectionApp`, dữ liệu frozen có thể vẫn còn.
- Khi đóng và mở lại app bình thường, SQLite được giữ lại.
- `ensure_runtime_database()` chỉ tạo hoặc nâng schema nếu cần, không reset database trong luồng khởi động.
- Khi chạy source, dữ liệu còn nếu thư mục `database/` của project không bị xóa hoặc thay thế.

### 2.2. Trường hợp có thể mất dữ liệu

- Xóa thủ công file `posture_app.db`.
- Xóa thư mục project khi chạy source.
- Xóa profile Windows, cài lại hệ điều hành hoặc mất ổ đĩa.
- Trình gỡ cài đặt xóa luôn thư mục AppData. Dự án hiện chưa có bằng chứng về hành vi của installer/uninstaller.
- Máy bị hỏng trước khi sao lưu.
- Người dùng chuyển sang máy khác: máy mới tạo SQLite riêng, không có tài khoản/lịch sử cũ.

### 2.3. AppData giải quyết được gì và không giải quyết được gì

AppData giải quyết quyền ghi khi ứng dụng nằm trong `Program Files` và giúp tách dữ liệu khỏi file cài đặt. AppData **không phải cloud backup** và không tạo danh tính dùng chung giữa nhiều thiết bị.

### 2.4. Hạn chế cốt lõi

`maNguoiDung` là `INTEGER AUTOINCREMENT` cục bộ. Cùng một người có thể có `maNguoiDung=4` trên máy A nhưng là ID khác trên máy B. Vì vậy không thể dùng khóa này làm danh tính đa thiết bị. Cần thêm một UUID trực tuyến ổn định, nhưng vẫn nên giữ `maNguoiDung` làm khóa nội bộ để tránh phá các quan hệ SQLite đang hoạt động.

---

## 3. Các bảng và dữ liệu đang được lưu

Snapshot SQLite tại thời điểm rà soát:

- 7 bảng nghiệp vụ.
- 3 dòng `NguoiDung`.
- 50 dòng `PhienLamViec`.
- 279 dòng `NhatKyTuThe`.
- 10 dòng `ThongKeNgay`.
- 2 dòng `CaiDat`.
- Không có phiên chưa kết thúc và không có nhật ký mồ côi tại thời điểm kiểm tra.

Không ghi email, hash hoặc OTP cụ thể vào báo cáo.

### 3.1. Schema và phân loại đồng bộ

| Bảng | Khóa/quan hệ | Vai trò hiện tại | Đề nghị cloud |
|---|---|---|---|
| `NguoiDung` | PK `maNguoiDung`; email unique | Tài khoản local, hash mật khẩu, trạng thái xác thực | Không upload password hash. Dùng Supabase Auth làm danh tính; local chỉ lưu ánh xạ `maNguoiDung` với `cloud_user_id` |
| `EmailOtp` | PK `maOtp`; FK `maNguoiDung`, cascade | OTP đăng ký local | Không đồng bộ. Khi dùng cloud Auth, để Supabase xử lý email confirmation/OTP |
| `CaiDat` | PK `maCaiDat`; FK `maNguoiDung`, cascade | Cảnh báo, âm thanh, camera, đường dẫn model, theme, smoothing | Giai đoạn 1 giữ local. Giai đoạn 2 chỉ sync thuộc tính portable; không sync camera URL, local file path, model/scaler path |
| `PhienLamViec` | PK `maPhien`; FK `maNguoiDung`, cascade | Tổng hợp một phiên ANN/HGB | **Bắt buộc đồng bộ ở giai đoạn 1**, sau khi loại/sanitise `giaTriNguon` và `ghiChu` |
| `NhatKyTuThe` | PK `maNhatKy`; FK nullable `maPhien`, `ON DELETE SET NULL` | Log khi đổi trạng thái/cảnh báo, không phải mỗi frame | Giữ local trong giai đoạn 1. Không sync log theo frame để giảm dữ liệu và rủi ro riêng tư |
| `ThongKeNgay` | PK `maThongKe`; unique `(maNguoiDung, ngay)` | Cache tổng hợp cho dashboard | Không dùng như nguồn cloud chính. Tái tạo từ `work_sessions`; local có thể rebuild sau khi pull |
| `ThongTinModel` | PK `maModel`; không FK user | Metadata ANN demo | Giữ local. Nếu cần version model online thì làm ở giai đoạn 2 |

### 3.2. Không có bảng cảnh báo riêng

Cảnh báo hiện được lưu theo hai cách:

- Tổng số trong `PhienLamViec.soLanCanhBao`.
- Dòng chi tiết trong `NhatKyTuThe` với `daCanhBao=1` và `loaiCanhBao`.

Không nên tạo cloud table cảnh báo chi tiết trong giai đoạn 1. `warning_count` trong phiên là đủ cho dashboard đa thiết bị.

### 3.3. Dữ liệu bắt buộc đồng bộ

- UUID phiên `sync_id`.
- UUID tài khoản trực tuyến `user_id`.
- Thời điểm bắt đầu/kết thúc.
- Loại nguồn ở mức khái quát: `webcam`, `ip_camera`, `video_file`.
- Tổng frame, frame đúng/sai/không người.
- Thời gian đúng/sai.
- Số cảnh báo.
- Độ tin cậy trung bình.
- `model_id`, `feature_set`, `decision_threshold` để biết phiên dùng cấu hình nào.
- `created_at`, `updated_at`, trạng thái xóa mềm nếu triển khai.

### 3.4. Dữ liệu chỉ nên giữ local

- Video, ảnh webcam.
- 33 landmark và feature từng frame.
- Đường dẫn video cục bộ.
- URL camera IP/RTSP; URL có thể chứa địa chỉ nội bộ hoặc thông tin đăng nhập.
- `NhatKyTuThe` chi tiết trong giai đoạn 1.
- Password hash/salt local, OTP hash/salt.
- SMTP password.
- Model, scaler và feature artifact.
- Đường dẫn model/scaler/sound.

### 3.5. Dữ liệu có thể tái tạo

`ThongKeNgay` có thể tái tạo từ các phiên đã kết thúc. Trên cloud nên dùng view hoặc truy vấn aggregate từ `work_sessions`, không upload số liệu ngày từ từng máy như một nguồn độc lập. Nếu hai máy cùng cập nhật tổng ngày bằng phép ghi đè, có nguy cơ lost update và đếm sai.

---

## 4. Luồng đăng ký, đăng nhập và phiên làm việc hiện tại

### 4.1. Đăng ký local

1. `PostureApp.handle_send_registration_otp()` đọc email/mật khẩu.
2. Thread nền mở SQLite qua `get_db_connection()`.
3. `register_and_send_otp()` tạo hoặc dùng lại user chưa xác thực.
4. `create_user()` băm mật khẩu bằng PBKDF2-HMAC-SHA256, 260.000 vòng, salt ngẫu nhiên 16 byte.
5. OTP 6 chữ số được sinh bằng `secrets.randbelow()`.
6. OTP được hash SHA-256 trên email + OTP + salt.
7. OTP có TTL 5 phút và tối đa 5 lần thử.
8. Email gửi trực tiếp bằng SMTP từ máy desktop.
9. `verify_registration_otp()` đánh dấu `emailDaXacThuc=1`.
10. `current_user_id` được gán bằng `maNguoiDung` local.

SMTP đọc từ biến môi trường hoặc `config/email_otp.local.config`. File local này đang tồn tại và được `.gitignore`; mã nguồn không in OTP hay password ra log. Tuy nhiên đây vẫn là mô hình gửi email từ client, không phù hợp để phân phối rộng vì bí mật SMTP không thể được bảo vệ trong `.exe`.

### 4.2. Đăng nhập local

1. `handle_login()` gọi `authenticate_user()`.
2. Service tìm user bằng email trong SQLite.
3. Kiểm tra email đã xác thực và so sánh PBKDF2 bằng `hmac.compare_digest()`.
4. Cập nhật `lanDangNhapCuoi`.
5. GUI chỉ giữ `current_user_id` trong bộ nhớ.
6. Không có JWT, refresh token hoặc session cloud.
7. `logout_current_user()` dừng camera nếu cần, xóa state trong bộ nhớ và quay lại form đăng nhập.

### 4.3. Ràng buộc dữ liệu theo người dùng

- `CaiDat`, `PhienLamViec`, `ThongKeNgay` dùng trực tiếp `maNguoiDung`.
- `NhatKyTuThe` không có `maNguoiDung`; quyền sở hữu được suy ra qua `maPhien`.
- Dashboard truyền `user_id=self.current_user_id`.
- Export lọc `PhienLamViec`/`ThongKeNgay` bằng `maNguoiDung` và join nhật ký qua phiên.

Phân vùng local theo người dùng đã có, nhưng chưa phải phân quyền bảo mật ở cloud.

### 4.4. Luồng phiên làm việc

#### Bắt đầu

1. `start_camera()` đọc mode và cấu hình GUI.
2. Với ANN/HGB, app lưu cài đặt local.
3. `load_ai_components()` tải model local và MediaPipe Pose.
4. Mở `cv2.VideoCapture`.
5. Reset bộ đếm.
6. Với ANN/HGB, `start_phien_lam_viec()` insert một dòng `PhienLamViec`.
7. Rule-based cố ý không tạo phiên CSDL.

#### Trong phiên

- `update_frame()` đọc frame và gọi `predict_frame()`.
- `handle_warning_logic()` xác nhận sai tư thế theo thời lượng/cooldown.
- `handle_status_logging()` chỉ ghi khi trạng thái thay đổi hoặc có cảnh báo, không ghi mọi frame.
- Mỗi lần ghi nhật ký đang mở kết nối và commit riêng.

#### Kết thúc

1. `stop_camera()` giải phóng camera/MediaPipe.
2. `end_phien_lam_viec()` cập nhật aggregate của phiên.
3. Commit `PhienLamViec`.
4. Sau đó gọi `update_thong_ke_ngay()` trong một kết nối/transaction khác.
5. Đặt `current_session_id=None`.

Vì update phiên và update ngày là hai transaction riêng, app có thể có phiên đã hoàn thành nhưng thống kê ngày chưa cập nhật nếu tiến trình dừng giữa hai bước. Statistics service có khả năng rebuild một phần từ phiên, nhưng chưa có quy trình recovery chính thức khi khởi động.

### 4.5. Dashboard và export

- `show_statistics()` gọi `get_dashboard_data()` trên SQLite.
- Dashboard chỉ đọc local, không có merge cloud.
- Risk index được tính lại từ aggregate phiên trong `statistics_service.enrich_session()`.
- Export source gọi `src/10_export_statistics.py` và lọc theo user local.
- Bản frozen hiện thông báo không hỗ trợ xuất CSV.
- Không tìm thấy chức năng xóa lịch sử người dùng trong GUI hiện tại.

### 4.6. Thời điểm phù hợp nhất để đồng bộ

Không sync theo frame. Thời điểm tốt nhất:

1. Khi kết thúc phiên: trong cùng transaction SQLite, hoàn tất `PhienLamViec` và thêm một outbox event `session_upsert`.
2. Sau commit: worker nền thử upload, không chặn GUI.
3. Khi app khởi động và có session cloud hợp lệ: retry pending.
4. Sau đăng nhập online: pull cloud về local trước khi mở dashboard.
5. Khi mạng trở lại: retry theo exponential backoff.

Nếu app crash giữa phiên, lần khởi động sau cần đánh dấu phiên là `interrupted`, chốt aggregate đã có nếu hợp lệ và đưa vào queue. Chưa có logic này trong dự án.

---

## 5. So sánh các phương án

| Tiêu chí | A. AppData + backup | B. Supabase + SQLite | C. Firebase + SQLite | D. FastAPI + DB |
|---|---|---|---|---|
| Phù hợp code Python hiện tại | Cao | **Cao** | Trung bình | Trung bình |
| Thay đổi | Thấp | Trung bình | Trung bình-cao | Cao |
| Rủi ro làm hỏng app | Thấp | Trung bình, kiểm soát được bằng adapter | Trung bình-cao | Cao |
| Auth đa thiết bị | Không | **Có** | Có | Có |
| Đồng bộ lịch sử | Chỉ thủ công | **Có** | Có | Có |
| Offline | Có | **Có qua SQLite/outbox** | Có qua SQLite; Python desktop phải tự thiết kế | Có qua SQLite; tự thiết kế |
| Phân quyền | Không áp dụng cloud | **RLS theo `auth.uid()`** | Firestore Rules nếu dùng client REST đúng cách | Tự viết authorization cho mọi endpoint |
| Bí mật trong desktop | Không cloud | Chỉ publishable key; service role bị cấm | Web API key có thể public, nhưng tuyệt đối không nhúng service account | Chỉ API base URL; server giữ DB/JWT secrets |
| Python desktop SDK | Không cần | **Có `supabase-py`** | Python chủ yếu là server/Admin SDK; end-user flow phải dùng REST hoặc bridge | Có HTTP client; backend phải tự xây |
| Vận hành server | Không | Supabase quản lý | Firebase quản lý | **Phải tự triển khai và bảo trì** |
| Kịp trước bảo vệ | Chỉ giải quyết backup | **Khả thi nếu giới hạn scope** | Khó hơn B | Rủi ro cao |
| Mức công việc | Thấp | **Trung bình** | Trung bình-cao | Cao |

### 5.1. Phương án A

Ưu điểm: ít thay đổi, AppData đã có trong frozen build. Có thể bổ sung export/restore database.

Hạn chế: không có danh tính online, không đa thiết bị, người dùng phải tự quản lý backup. Chỉ phù hợp như fallback hoặc kế hoạch tối thiểu nếu không đủ thời gian làm cloud.

### 5.2. Phương án B

Supabase Auth dùng JWT và tích hợp PostgreSQL với RLS. Python client hỗ trợ Auth và upsert. Publishable key được thiết kế cho môi trường public như desktop; bảo mật dữ liệu phải do JWT + RLS quyết định, không dựa vào việc giấu key.

Ưu điểm chính với dự án:

- Python client phù hợp.
- Schema quan hệ gần SQLite hiện tại.
- `user_id UUID` liên kết trực tiếp `auth.users`.
- Upsert theo UUID thuận lợi cho idempotency.
- RLS kiểm soát từng dòng.
- Không phải tự triển khai API server trước bảo vệ.

Rủi ro:

- Cần thiết kế token storage trên desktop.
- Cần test RLS bằng hai tài khoản.
- Cần outbox và xử lý lỗi mạng.
- Không được dùng `service_role` trong app.

### 5.3. Phương án C

Firebase Auth có REST API cho email/password. Tuy nhiên Firestore Python library là server client, dùng Application Default Credentials/service account và bypass Firestore Security Rules. Không được đóng gói service account vào desktop.

Muốn triển khai an toàn phải:

- Gọi Firebase Auth REST để lấy ID/refresh token.
- Gọi Firestore REST bằng user token hoặc viết một backend trung gian.
- Tự xử lý refresh token, mapping document và offline queue.

Phương án này vẫn làm được nhưng phức tạp hơn Supabase đối với ứng dụng Python desktop hiện tại.

### 5.4. Phương án D

FastAPI cho phép tự xây OAuth2/JWT, nhưng dự án phải tự chịu trách nhiệm:

- Hash mật khẩu, reset password, email verification.
- JWT access/refresh, revoke, rotation.
- Authorization theo user.
- API versioning, logging, rate limit.
- Deploy HTTPS, giám sát, backup và cập nhật server.

Nếu dùng MongoDB Atlas, desktop không được kết nối trực tiếp bằng URI có database username/password. Chuỗi kết nối phải nằm trên server. Phương án D phù hợp sản phẩm dài hạn khi nhóm có năng lực DevOps, không phù hợp deadline bảo vệ hiện tại.

---

## 6. Phương án được khuyến nghị

### Chọn phương án B

> **Supabase Auth + Supabase PostgreSQL có RLS + SQLite cache/outbox.**

Lý do:

1. Giải quyết đúng yêu cầu đăng nhập cùng tài khoản trên máy A/B.
2. Gần mô hình quan hệ hiện có hơn Firestore.
3. Có Python SDK cho Auth và data.
4. Không cần tự vận hành FastAPI trước bảo vệ.
5. Cho phép giữ AI, video và landmark hoàn toàn local.
6. Có thể triển khai tăng dần, cloud lỗi không làm camera/model dừng.
7. Publishable key có thể nằm trong desktop nếu toàn bộ bảng public bật RLS đúng.

### Phạm vi bắt buộc trước bảo vệ

- Auth online email/password.
- Ánh xạ local user với Supabase UUID.
- Sync aggregate của `PhienLamViec`.
- Pull phiên cloud về cache SQLite.
- Dashboard chỉ đọc cache local đã merge theo `sync_id`.
- Outbox pending khi mất mạng.
- RLS được test bằng hai user.
- AI hoạt động khi cloud lỗi.

### Không nên cố làm trước bảo vệ

- Sync từng `NhatKyTuThe`.
- Realtime subscription.
- Multi-master edit phức tạp.
- Đồng bộ đường dẫn camera/model.
- Admin portal.
- MongoDB hoặc backend thứ hai.

---

## 7. Kiến trúc đề xuất

```text
                    +-----------------------------+
                    | Supabase Auth               |
Desktop Python ---> | email/password, JWT, UUID   |
      |             +--------------+--------------+
      |                            |
      | user JWT                   | auth.uid()
      v                            v
+------------------+     +-----------------------------+
| CloudAuthService | --> | Supabase PostgreSQL + RLS   |
| SyncService      |     | profiles, work_sessions     |
+--------+---------+     | daily_statistics view       |
         |               +-----------------------------+
         |
         | local transaction / retry / pull
         v
+------------------------------------------------------+
| SQLite cache/offline                                  |
| NguoiDung mapping, PhienLamViec, ThongKeNgay cache,  |
| NhatKyTuThe local-only, DongBoHangDoi                 |
+------------------------------------------------------+
         |
         v
+------------------------------------------------------+
| OpenCV + MediaPipe + ANN/HGB/Rule-based local        |
| Không phụ thuộc cloud cho suy luận webcam            |
+------------------------------------------------------+
```

### Nguồn dữ liệu chính

- Cloud là nguồn chính cho **các phiên đã sync**.
- SQLite là nguồn chính tạm thời cho **bản ghi pending/offline** và là cache hiển thị.
- Dashboard không query cloud và local rồi cộng trực tiếp. Worker pull/upsert cloud vào SQLite theo `sync_id`, sau đó dashboard chỉ đọc SQLite để tránh đếm trùng.

### Chế độ mất mạng

- Nếu đã từng đăng nhập và còn ánh xạ local hợp lệ, app cho phép vào chế độ offline với user cache.
- AI, cảnh báo và SQLite tiếp tục hoạt động.
- Thanh trạng thái cần hiển thị `Offline - chưa đồng bộ`.
- Nếu máy chưa từng đăng nhập online, không thể xác nhận tài khoản cloud; có thể cho phép chế độ demo local riêng nhưng không được gọi là đăng nhập cloud.

---

## 8. Thiết kế dữ liệu cloud đề xuất

Đây chỉ là thiết kế, chưa tạo migration.

### 8.1. `profiles`

| Cột | Kiểu | Ràng buộc |
|---|---|---|
| `user_id` | UUID | PK, FK đến `auth.users.id` |
| `display_name` | TEXT | Nullable |
| `created_at` | TIMESTAMPTZ | UTC, server default |
| `updated_at` | TIMESTAMPTZ | UTC |

RLS: user chỉ được select/update dòng có `user_id = auth.uid()`.

### 8.2. `work_sessions`

| Cột | Kiểu | Ý nghĩa |
|---|---|---|
| `sync_id` | UUID | PK, sinh tại desktop trước khi ghi local |
| `user_id` | UUID | FK `auth.users.id`, bắt buộc |
| `device_id` | UUID | Optional, chỉ để chẩn đoán |
| `started_at` | TIMESTAMPTZ | UTC |
| `ended_at` | TIMESTAMPTZ | UTC, nullable khi interrupted |
| `session_state` | TEXT | `completed`, `interrupted` |
| `source_type` | TEXT | `webcam`, `ip_camera`, `video_file`; không chứa URL/path |
| `total_frames` | BIGINT | Aggregate |
| `correct_frames` | BIGINT | Aggregate |
| `incorrect_frames` | BIGINT | Aggregate |
| `no_person_frames` | BIGINT | Aggregate |
| `correct_seconds` | DOUBLE PRECISION | Aggregate |
| `incorrect_seconds` | DOUBLE PRECISION | Aggregate |
| `warning_count` | INTEGER | Aggregate |
| `average_confidence` | DOUBLE PRECISION | Aggregate |
| `model_id` | TEXT | Ví dụ HGB hiện tại |
| `feature_set` | TEXT | `ergonomic_v2_with_view` |
| `decision_threshold` | DOUBLE PRECISION | `0.76` nếu dùng HGB balanced |
| `record_version` | INTEGER | Bắt đầu từ 1 |
| `created_at` | TIMESTAMPTZ | Server time |
| `updated_at` | TIMESTAMPTZ | Server time |
| `deleted_at` | TIMESTAMPTZ | Giai đoạn 2 |

RLS tối thiểu:

- SELECT: `auth.uid() IS NOT NULL AND auth.uid() = user_id`.
- INSERT: `auth.uid() = user_id`.
- UPDATE/DELETE: chỉ owner; không cho đổi `user_id`.
- Không cấp quyền cho role `anon`.

### 8.3. `daily_statistics`

Nên là view hoặc RPC aggregate từ `work_sessions`, nhóm theo `user_id` và ngày. Không để client A/B cùng upload phép cộng dồn ngày.

Các giá trị:

- `session_count`.
- `work_seconds`.
- `correct_seconds`.
- `incorrect_seconds`.
- `warning_count`.
- Tỷ lệ được tính từ tổng thời gian.

Nếu dùng view trong Supabase, phải kiểm tra chế độ `security_invoker`/RLS theo phiên bản PostgreSQL và không tạo view bypass RLS.

### 8.4. `user_settings` - giai đoạn 2

Chỉ sync:

- Thời gian xác nhận cảnh báo.
- Cooldown.
- Bật/tắt âm thanh.
- Theme.
- Smoothing window.
- Preference model mode nếu cần.

Không sync:

- `nguonCamera`.
- URL IP camera.
- `duongDanAmThanh`.
- `duongDanModel`.
- `duongDanScaler`.

### 8.5. Bổ sung SQLite dự kiến

Không thay PK/FK INTEGER hiện tại. Bổ sung:

#### `NguoiDung`

- `cloudUserId TEXT UNIQUE NULL`.
- `migrationStatus TEXT`.
- `migratedAt TEXT`.

#### `PhienLamViec`

- `syncId TEXT UNIQUE`.
- `syncStatus TEXT`: `pending`, `synced`, `failed`.
- `syncUpdatedAt TEXT`.
- `cloudVersion INTEGER`.
- `deletedAt TEXT` ở giai đoạn 2.

#### `DongBoHangDoi`

- `maHangDoi INTEGER PRIMARY KEY`.
- `entityType TEXT`.
- `entitySyncId TEXT`.
- `operation TEXT`: `upsert`, `delete`.
- `payloadJson TEXT`.
- `attemptCount INTEGER`.
- `nextRetryAt TEXT`.
- `lastError TEXT`.
- `createdAt TEXT`.
- UNIQUE `(entityType, entitySyncId, operation)` hoặc cơ chế coalesce event.

---

## 9. Thiết kế đồng bộ

### 9.1. Upload

1. Sinh `sync_id=UUIDv4` khi bắt đầu phiên.
2. Khi kết thúc phiên, update aggregate và insert/update outbox trong **cùng transaction SQLite**.
3. Commit local trước.
4. Worker đọc queue `pending`.
5. Gọi Supabase `upsert` với đầy đủ `sync_id` và `user_id`.
6. Thành công thì đánh dấu `synced`.
7. Timeout/lỗi mạng thì tăng `attemptCount`, ghi lỗi không nhạy cảm và lên lịch retry.

### 9.2. Vì sao dùng upsert

Mạng có thể đứt sau khi cloud đã ghi nhưng trước khi client nhận response. Retry bằng `insert` có thể tạo trùng. `upsert` theo PK `sync_id` làm thao tác idempotent. Cloud cần unique constraint trên `sync_id`.

### 9.3. Tải dữ liệu xuống

Sau login:

1. Lấy `cloud_user_id` từ Auth session.
2. Query các phiên của user theo `updated_at > last_pull_at`.
3. Upsert vào SQLite theo `syncId`.
4. Không ghi đè local `pending` bằng bản cloud cũ hơn.
5. Rebuild `ThongKeNgay` từ toàn bộ phiên local đã merge.
6. Dashboard đọc SQLite.

### 9.4. Tránh gửi trùng

- UUID sinh trước khi upload.
- Unique cloud PK.
- Unique local `syncId`.
- Queue operation được coalesce.
- Chỉ đánh dấu synced sau response thành công.

### 9.5. App đóng giữa chừng

- Outbox đã commit vẫn còn.
- Lần mở sau tiếp tục retry.
- Phiên chưa có `ended_at` cần được đánh dấu interrupted trước khi sync.
- Không xóa queue khi chỉ mới bắt đầu request.

### 9.6. Một tài khoản trên hai máy

Phiên thông thường là append-only và mỗi máy sinh UUID khác, nên không xung đột. Không cho sửa aggregate phiên đã kết thúc trong giai đoạn 1. Daily statistics được derive nên không có xung đột cộng dồn.

### 9.7. Xử lý xóa

Hiện GUI chưa có xóa lịch sử. Không cần sync delete ở giai đoạn 1. Giai đoạn 2 dùng `deleted_at` và outbox tombstone; mọi thiết bị pull tombstone và ẩn/xóa cache tương ứng.

### 9.8. Thời gian và múi giờ

Mã hiện dùng `datetime.now().isoformat()` không kèm timezone. Dữ liệu mới phải:

- Ghi UTC có offset hoặc epoch.
- Cloud dùng `TIMESTAMPTZ`.
- Chỉ đổi sang Asia/Ho_Chi_Minh khi hiển thị.
- Dữ liệu legacy phải được gắn giả định timezone trong migration log; không âm thầm xem naive time là UTC.

### 9.9. Dashboard không đếm trùng

Không union hai nguồn tại UI. Quy tắc:

> Pull cloud vào SQLite theo `sync_id` -> merge pending local -> rebuild daily cache -> dashboard chỉ đọc SQLite.

### 9.10. Migration tài khoản SQLite cũ

Không thể chuyển trực tiếp tài khoản hiện tại thành tài khoản Supabase chỉ bằng cách copy `matKhauHash` và `matKhauSalt`. Hash PBKDF2 local không phải thông tin đăng nhập mà Supabase Auth có thể nhận từ desktop. Không dùng `service_role` hoặc Admin API trong client để nhập user.

Quy trình demo an toàn:

1. Người dùng đăng ký hoặc đăng nhập tài khoản Supabase bằng email.
2. Mật khẩu được nhập lại vào Auth online qua TLS; không đọc ngược hash local.
3. Sau login thành công, app tìm local account cùng email đã xác thực.
4. Hiển thị số phiên local dự kiến gắn và yêu cầu người dùng xác nhận.
5. Ghi `cloudUserId` vào đúng dòng `NguoiDung`.
6. Sinh `syncId` cho các phiên cũ chưa có UUID.
7. Thêm outbox event, không upload ngay trong transaction migration.
8. Ghi `migrationStatus='queued'` và một `migrationBatchId`.
9. Sau khi toàn bộ event thành công, đổi sang `migrationStatus='completed'` và ghi `migratedAt`.

Chống chạy lặp:

- `cloudUserId` unique trong SQLite.
- `syncId` unique local/cloud.
- Mỗi phiên chỉ được thêm vào một migration batch.
- Khi chạy lại, bỏ qua phiên đã `synced` hoặc đã có queue hợp lệ.

Tài khoản `Admin` không có email/hash không được tự động đưa lên cloud. Nếu lịch sử legacy đang gắn Admin, phải yêu cầu người dùng chọn rõ tài khoản online nhận dữ liệu và xác nhận thủ công. Snapshot hiện tại có 50 phiên gắn với một tài khoản email local đã xác thực; không được suy ra rằng mọi dữ liệu legacy đều thuộc tài khoản đang đăng nhập nếu chưa đối chiếu `maNguoiDung`.

### 9.11. Kiểm soát bảo mật bắt buộc

- Không lưu hoặc log mật khẩu plaintext.
- Không upload `matKhauHash`, `matKhauSalt`, `otpHash`, `otpSalt`.
- Không log OTP, JWT, refresh token hoặc request body đăng nhập.
- Không nhúng Supabase `service_role` key hay PostgreSQL connection string vào `.exe`.
- Desktop chỉ dùng project URL và publishable key; mọi bảng exposed phải bật RLS.
- Không xem publishable key là bí mật. PyInstaller có thể bị giải nén, nên quyền phải dựa trên JWT/RLS.
- `user_id` trong payload không đủ để xác thực; RLS phải so sánh với `auth.uid()`.
- Không cho client update owner `user_id`.
- Access token chỉ giữ trong memory khi có thể; refresh token lưu bằng Windows Credential Manager hoặc keyring hệ điều hành, không plaintext SQLite.
- Không kết nối trực tiếp MongoDB Atlas/PostgreSQL bằng database credential từ desktop.
- Chỉ dùng HTTPS.
- Không sync video, ảnh, landmark, RTSP URL hoặc local file path.
- Lỗi cloud phải được rút gọn trước khi ghi log; không ghi token/PII.
- SMTP credential local hiện chỉ phù hợp demo source. Khi dùng Supabase Auth, không phân phối SMTP password trong client.

---

## 10. Danh sách tệp dự kiến cần chỉnh sửa

Đây là kế hoạch, chưa sửa file.

| Tệp | Chức năng hiện tại | Thay đổi dự kiến | Rủi ro/phụ thuộc |
|---|---|---|---|
| `src/4_main_desktop_app.py` | GUI và orchestration thật | Gọi Auth/Sync service, trạng thái offline/sync, enqueue sau kết thúc phiên | File lớn, blast radius cao; cần thay nhỏ từng bước |
| `src/auth_service.py` | Auth/OTP local | Giữ như adapter migration tạm; không dùng làm Auth cloud chính | Không được chuyển hash PBKDF2 sang Supabase |
| `src/app/services/cloud_auth_service.py` mới | Chưa có | Supabase signup/signin/signout/session refresh | Token storage, lỗi mạng |
| `src/app/services/sync_service.py` mới | Chưa có | Push/pull/retry/background worker | Thread safety với Tkinter/SQLite |
| `src/app/repositories/sync_repository.py` mới | Chưa có | Outbox và sync state local | Transaction/idempotency |
| `src/app/repositories/session_repository.py` | Placeholder | Chuyển SQL phiên khỏi GUI, upsert theo sync ID | Phải giữ hành vi hiện tại |
| `src/app/repositories/user_repository.py` | Placeholder | Mapping local ID - cloud UUID, migration flag | Tránh gắn nhầm lịch sử |
| `src/app/repositories/settings_repository.py` | Placeholder | Tách cài đặt portable/device-specific | Giai đoạn 2 |
| `src/app/repositories/database.py` | Kết nối SQLite | Context manager/transaction helper nếu cần | Không đổi path |
| `src/3_database_setup.py` | Schema/migration local | Thêm cột sync và outbox bằng migration không phá dữ liệu | Bắt buộc backup và test DB cũ |
| `src/runtime_paths.py` | AppData/resource paths | Gần như giữ nguyên; có thể thêm đường dẫn token/cache không nhạy cảm | Không lưu token plaintext |
| `src/statistics_service.py` | Dashboard local | Rebuild từ session đã merge; giữ filter user | Test hiện có đang lỗi schema cũ |
| `src/10_export_statistics.py` | Export CSV local | Có thể thêm `sync_id/sync_status`, vẫn lọc user | Không export token |
| `src/app/services/model_service.py` | HGB local | Không phụ thuộc cloud; nên validate `feature_schema.json` trước inference | Hiện chưa load schema artifact |
| `src/app/config/constants.py` | Model mode/artifact | Không chứa secret; cloud URL/key nên ở config public riêng | Publishable key không phải secret |
| `requirements.txt` | Dependency runtime | Thêm `supabase` và thư viện OS keyring nếu chọn | Kiểm tra tương thích PyInstaller |
| `build_scripts/posture_app.spec` | Đóng gói | Thêm Supabase dependency, HGB model/schema/threshold mới | Spec hiện chưa đóng gói HGB registry mới |
| `tests/test_cloud_auth_service.py` mới | Chưa có | Mock Auth và lỗi mạng | Không gọi production project |
| `tests/test_sync_service.py` mới | Chưa có | Retry/upsert/idempotency/conflict | Cần fake cloud |
| `tests/test_statistics_service.py` | Test schema cũ | Cập nhật fixture user-scoped | Hiện có 2 test fail |

---

## 11. Kế hoạch triển khai theo thứ tự

### Giai đoạn 1 - Phải làm trước bảo vệ

#### Bước 0. Chốt baseline và backup

- Backup SQLite hiện tại.
- Chạy test auth/statistics/model.
- Ghi checksum model.

Tiêu chí qua bước: mở app, login local, chạy HGB, kết thúc phiên và dashboard vẫn hoạt động.

#### Bước 1. Tạo Supabase project và schema cloud

- Bật email/password Auth.
- Tạo `profiles`, `work_sessions`, daily view.
- Bật RLS.
- Không tạo service-role credential trong repo.

Tiêu chí: user A không đọc/ghi được row user B bằng publishable key.

#### Bước 2. Thêm CloudAuthService độc lập

- Signup/signin/signout.
- Lấy UUID.
- Timeout và offline error không làm crash.
- Lưu refresh token bằng Windows Credential Manager/keyring, không plaintext SQLite.

Tiêu chí: đăng ký/login được trên hai máy hoặc hai profile test.

#### Bước 3. Migration SQLite additive

- Thêm mapping UUID, sync ID, sync status và outbox.
- Không đổi PK/FK hiện tại.
- Chạy migration nhiều lần không lỗi.

Tiêu chí: database cũ mở được, số dòng/quan hệ không đổi.

#### Bước 4. Enqueue phiên

- Hoàn tất session + queue trong một transaction.
- Không sync nhật ký chi tiết.

Tiêu chí: mất mạng vẫn kết thúc phiên và có queue pending.

#### Bước 5. Upload idempotent

- Upsert theo UUID.
- Retry không tạo duplicate.
- Không upload path/IP/video/landmark.

Tiêu chí: gửi cùng session 2 lần vẫn chỉ có 1 cloud row.

#### Bước 6. Pull và cache

- Pull theo user UUID.
- Upsert SQLite.
- Rebuild daily stats.

Tiêu chí: máy B đăng nhập thấy phiên máy A.

#### Bước 7. Migration tài khoản cũ

- Online signup/login.
- User xác nhận gắn lịch sử.
- Tạo sync ID và queue đúng một lần.

Tiêu chí: chạy migration lại không upload trùng.

#### Bước 8. Đóng gói và regression

- Thêm HGB artifact/cloud dependency vào spec.
- Test khi cloud timeout.
- Test HGB offline.

Tiêu chí: `.exe` chạy HGB cục bộ khi không có Internet và sync lại khi có mạng.

### Giai đoạn 2 - Hướng phát triển

- Sync cài đặt portable.
- Soft delete/tombstone.
- Quản lý thiết bị/session.
- Conflict resolution có version.
- Tự động backup/export.
- Model-version metadata online.
- Mã hóa local nâng cao.
- Realtime update nếu thực sự cần.

---

## 12. Kịch bản kiểm thử

| STT | Kịch bản | Kết quả mong đợi |
|---:|---|---|
| 1 | Đăng ký máy A, đăng nhập máy B | Cùng Supabase UUID; không tạo hai profile |
| 2 | Tạo phiên máy A, tải lịch sử máy B | Máy B có đúng một phiên cùng `sync_id` |
| 3 | Mất mạng khi kết thúc phiên | Phiên local hoàn tất, queue `pending`, GUI không crash |
| 4 | Có mạng lại | Worker upload, trạng thái thành `synced` |
| 5 | Gửi lặp một phiên | Cloud vẫn một row do upsert/unique UUID |
| 6 | Xóa app máy A | Dữ liệu đã sync vẫn còn; dữ liệu pending chưa sync có thể mất nếu AppData bị xóa |
| 7 | User A truy cập dữ liệu B | Bị RLS từ chối |
| 8 | Cloud lỗi | Camera, MediaPipe, HGB, cảnh báo và SQLite vẫn hoạt động |
| 9 | GUI chưa login cloud nhưng có offline profile hợp lệ | HGB local vẫn load; sync tạm dừng |
| 10 | Gắn dữ liệu SQLite cũ | Chỉ gắn đúng local user và chỉ chạy một lần |
| 11 | Crash sau cloud write trước response | Retry không tạo duplicate |
| 12 | Hai máy tạo phiên cùng lúc | Hai UUID riêng; daily aggregate không lost update |
| 13 | Token hết hạn | Refresh an toàn; thất bại thì yêu cầu login, không xóa pending data |
| 14 | Refresh token bị xóa khỏi keyring | App chuyển về login; SQLite không mất |
| 15 | RLS INSERT giả `user_id` khác | Bị từ chối |
| 16 | Payload chứa `giaTriNguon` RTSP/path | Field không được upload |
| 17 | Phiên bị ngắt do mất điện | Khởi động lại đánh dấu interrupted và enqueue hợp lệ |
| 18 | Pull lại nhiều lần | Dashboard không đếm trùng |
| 19 | Rule-based | Không tạo cloud session nếu giữ hành vi hiện tại |
| 20 | PyInstaller offline | HGB model, threshold và feature logic đều có trong bundle |

---

## 13. Những nội dung có thể trình bày với Hội đồng

### Câu trả lời ngắn

> Ứng dụng vẫn giữ SQLite vì nhận diện tư thế cần phản hồi nhanh và phải hoạt động khi mất Internet. Cloud chỉ quản lý tài khoản trực tuyến và lưu dữ liệu tổng hợp của các phiên như thời gian làm việc, số frame đúng/sai và số cảnh báo. Video, ảnh webcam, landmark từng frame, đường dẫn camera và model không được upload. Khi kết thúc phiên, dữ liệu được lưu vào SQLite trước rồi đưa vào hàng đợi; có mạng thì upsert lên cloud, mất mạng thì ứng dụng vẫn chạy và đồng bộ lại sau. Nếu xóa ứng dụng, dữ liệu đã đồng bộ còn trên cloud, còn dữ liệu chưa đồng bộ có thể mất nếu SQLite cũng bị xóa. Model HGB, feature extraction và ngưỡng được tải từ artifact cục bộ, nên suy luận AI không phụ thuộc máy chủ. Phiên bản hiện tại mới có SQLite và tài khoản local; chỉ được tuyên bố hỗ trợ đa thiết bị sau khi Auth, RLS, upload, pull và các kịch bản kiểm thử đã hoàn thành.

### Hạn chế phải nói trung thực

- Hiện chưa có cloud implementation.
- Chưa có sync queue.
- Test statistics đang có 2 lỗi do fixture schema cũ.
- Feature schema JSON tồn tại nhưng GUI chưa validate artifact này.
- PyInstaller spec hiện chưa chứa HGB registry mới.
- Full GUI/cloud failure test chưa thực hiện.

---

## 14. Kết luận

### Trạng thái hiện tại

Hệ thống đã có:

- Đăng ký/login/OTP local.
- PBKDF2 password hash.
- Dữ liệu tách theo `maNguoiDung` trong SQLite.
- AppData cho frozen build.
- Phiên, nhật ký, thống kê và dashboard local.
- Model ANN/HGB và MediaPipe chạy local.

Hệ thống chưa có:

- Tài khoản trực tuyến.
- UUID cloud.
- JWT/refresh token.
- Row Level Security.
- Upload/pull.
- Outbox/retry.
- Đăng nhập đa thiết bị.
- Cloud backup.

### Việc nên làm ngay

Chọn Supabase Auth + PostgreSQL/RLS + SQLite outbox/cache, nhưng chỉ triển khai scope tối thiểu: Auth, mapping UUID, sync aggregate phiên, pull lịch sử và offline retry.

### Phần chỉ nên ghi là hướng phát triển

Sync cài đặt, soft delete, conflict phức tạp, quản lý thiết bị, model registry online và realtime subscription.

### Điều kiện để tuyên bố hỗ trợ đa thiết bị

Chỉ được tuyên bố sau khi:

1. Máy A/B đăng nhập cùng UUID.
2. Phiên A xuất hiện đúng một lần ở B.
3. Offline queue retry thành công.
4. RLS cô lập user A/B.
5. Xóa local không xóa cloud data.
6. AI/HGB vẫn chạy khi cloud lỗi.
7. Migration user cũ idempotent.
8. Bản PyInstaller đã đóng gói và kiểm thử đầy đủ artifact HGB/cloud client.

---

## Nguồn kỹ thuật chính thức đã đối chiếu

- Supabase Auth và JWT: <https://supabase.com/docs/guides/auth>
- Supabase publishable key cho desktop: <https://supabase.com/docs/guides/getting-started/api-keys>
- Supabase Row Level Security: <https://supabase.com/docs/guides/database/postgres/row-level-security>
- Supabase Python Auth: <https://supabase.com/docs/reference/python/auth-api>
- Supabase Python upsert: <https://supabase.com/docs/reference/python/upsert>
- Supabase session/access/refresh token: <https://supabase.com/docs/guides/auth/sessions>
- Supabase password security: <https://supabase.com/docs/guides/auth/password-security>
- Firebase client/server libraries: <https://firebase.google.com/docs/firestore/client/libraries>
- Firebase Firestore quickstart và service account: <https://firebase.google.com/docs/firestore/quickstart>
- Firebase Auth REST: <https://firebase.google.com/docs/reference/rest/auth>
- FastAPI OAuth2/JWT: <https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/>
