# GUI QA Checklist

| Test case | Ket qua | Ngay test | Nguoi test | Screenshot/Artifact | Ghi chu |
|---|---|---|---|---|---|
| Khoi dong app sau khi chay `python src/3_database_setup.py` |  |  |  |  |  |
| Main window dung light mode, khong con panel dark bi sot |  |  |  |  |  |
| Chuyen Light -> Dark khi camera chua chay khong crash |  |  |  |  |  |
| Chuyen Dark -> Light khi camera chua chay khong crash |  |  |  |  |  |
| Thu doi theme khi camera dang chay hien thong bao yeu cau dung camera truoc |  |  |  |  |  |
| Chon Dark, bam Luu cai dat, dong/mo lai app van giu Dark |  |  |  |  |  |
| Dashboard mo trong Dark mode van doc duoc chart/table |  |  |  |  |  |
| Sidebar khong overflow o 1080x640 |  |  |  |  |  |
| Sidebar chia dung section: trang thai, nguon, nhan dien, canh bao, thao tac, phien hien tai |  |  |  |  |  |
| Mini KPI phien hien tai cap nhat frame/dung/sai/khong nguoi/canh bao/FPS |  |  |  |  |  |
| Mau status doc duoc voi `DANG_KIEM_TRA` |  |  |  |  |  |
| Mau status doc duoc voi `DUNG_TU_THE` |  |  |  |  |  |
| Mau status doc duoc voi `SAI_TU_THE` |  |  |  |  |  |
| Mau status doc duoc voi `KHONG_PHAT_HIEN_NGUOI` |  |  |  |  |  |
| ANN mode voi webcam |  |  |  |  |  |
| ANN mode voi file video |  |  |  |  |  |
| Rule-based mode voi webcam |  |  |  |  |  |
| Rule-based mode voi file video |  |  |  |  |  |
| Baseline panel light mode hien feature/warning ro rang |  |  |  |  |  |
| Baseline rut co vua van nhan la dung |  |  |  |  | Co the verify them bang unit test. |
| Baseline mui gan ngang vai/rut co sau nhan la sai |  |  |  |  | Co the verify them bang unit test. |
| Baseline panel hien `khoang cach mui-vai ti le` va `rut co sau` |  |  |  |  |  |
| Start/Stop nhieu lan khong crash |  |  |  |  |  |
| Bat/tat am thanh canh bao |  |  |  |  |  |
| Database co them phien sau khi stop ANN mode |  |  |  |  |  |
| Dashboard thong ke light mode mo duoc |  |  |  |  |  |
| Dashboard hien KPI tong thoi gian/dung/sai/canh bao/confidence/risk |  |  |  |  |  |
| Dashboard chart ty le thoi gian doc duoc |  |  |  |  |  |
| Dashboard chart canh bao theo phien doc duoc |  |  |  |  |  |
| Dashboard trend 7 ngay doc duoc |  |  |  |  |  |
| Bang phien hien dung cot: bat dau, thoi luong, dung, sai, khong nguoi, canh bao, tin cay, risk |  |  |  |  |  |
| Date selector doi ngay va reload dashboard dung |  |  |  |  |  |
| Dashboard no-data state khong crash voi database moi |  |  |  |  |  |
| Nut Export CSV sinh file trong `reports/results` |  |  |  |  |  |
| Thieu `models/ann_best.keras` co thong bao de hieu |  |  |  |  |  |
| Thieu `models/scaler.pkl` co thong bao de hieu |  |  |  |  |  |
| Thieu database co huong dan chay setup |  |  |  |  |  |
| Video HEVC/H.265 duoc bao loi/huong dan convert |  |  |  |  |  |

Quy uoc ket qua: Pass, Fail, Blocked, Not tested.

## QA bổ sung cho giao diện tiếng Việt có dấu

| Test case | Ket qua | Ngay test | Nguoi test | Screenshot/Artifact | Ghi chu |
|---|---|---|---|---|---|
| Tiêu đề app hiển thị `Ứng dụng phát hiện tư thế làm việc` |  |  |  |  |  |
| Placeholder camera hiển thị `Chưa bật camera` và không lỗi font |  |  |  |  |  |
| Sidebar hiển thị đúng dấu ở `Nguồn đầu vào`, `Nhận diện`, `Cảnh báo`, `Thao tác`, `Phiên hiện tại` |  |  |  |  |  |
| Label `Ngưỡng sai sau làm mượt`, `Độ tin cậy`, `Thời gian sai` không bị cắt chữ |  |  |  |  |  |
| Overlay video hiển thị được `TƯ THẾ ĐÚNG`, `SAI TƯ THẾ`, `KHÔNG PHÁT HIỆN NGƯỜI`, `Độ tin cậy` |  |  |  |  |  |
| Dashboard title hiển thị `Dashboard thống kê tư thế` |  |  |  |  |  |
| Dashboard KPI hiển thị `Tổng thời gian`, `Đúng tư thế`, `Sai tư thế`, `Rủi ro`, `Cảnh báo` |  |  |  |  |  |
| Biểu đồ hiển thị `Tỷ lệ thời gian`, `Số cảnh báo`, `Sai tư thế (%)` đúng dấu |  |  |  |  |  |
| Bảng phiên hiển thị heading `Bắt đầu`, `Thời lượng`, `Không người`, `Tin cậy`, `Rủi ro` |  |  |  |  |  |
| Nút `Xuất CSV` và `Đóng` không bị cắt chữ |  |  |  |  |  |
| Bản `.exe` sau đóng gói không hiện mojibake dạng `Ä‘`, `á»`, `Æ°` |  |  |  |  |  |
