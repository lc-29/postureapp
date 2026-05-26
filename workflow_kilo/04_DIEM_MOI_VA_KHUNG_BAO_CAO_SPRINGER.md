# 04. Diem moi va khung bao cao theo dinh dang Springer

## Danh gia diem moi hien tai

Du an hien co diem moi theo huong ung dung/tich hop he thong, khong phai diem moi thuat toan manh. Neu viet bao cao nghien cuu khoa hoc, nen trinh bay trung thuc la mot he thong phat hien va canh bao tu the lam viec realtime dua tren landmark, ket hop baseline co the giai thich va ANN nhe.

### Diem moi co the khai thac

1. He thong realtime end-to-end cho tu the lam viec:
   - Tu webcam/video/IP camera den canh bao va thong ke SQLite.
   - Khong chi dung o model offline.

2. Bieu dien landmark nhe:
   - Dung 33 landmark MediaPipe Pose va 99 dac trung `(x, y, z)`.
   - Phu hop may ca nhan, khong can anh raw dua vao model.

3. Ket hop hai lop quyet dinh:
   - Rule-based ergonomic baseline de giai thich loi: lech vai, nghieng than, dau lech truc, cui dau, tay gan mieng/chong cam.
   - ANN binary classifier de hoc mau tu du lieu thu thap.

4. Bo du lieu rieng cho moi truong lam viec:
   - Co nhieu goc quay: front, side 30, side 90.
   - Co tap external video rieng.

5. Ung dung co logging hanh vi:
   - Luu phien lam viec, nhat ky canh bao, thong ke ngay.
   - Co kha nang phan tich thoi gian dung/sai va so lan canh bao.

6. Heuristic phat hien tay gan mieng/chong cam:
   - MediaPipe Pose khong co landmark cam chinh xac.
   - Du an dung trung diem mieng va diem ban tay gan nhat, chuan hoa theo do rong vai.

### Diem moi can cuong hoa truoc khi nop bai

- Danh gia external test bang script rieng.
- Danh gia video-wise/person-wise split de tranh leakage frame gan nhau.
- So sanh rule-based vs ANN.
- Threshold sweep va ablation study.
- Mo ta dataset ro: so nguoi, dieu kien quay, label protocol.

## Goc dat tieu de bai bao

Lua chon an toan:

```text
A Lightweight Landmark-Based Real-Time System for Desk Posture Detection and Feedback
```

Lua chon nhan manh hybrid:

```text
Hybrid Rule-Based and Neural Landmark Analysis for Real-Time Desk Posture Monitoring
```

Lua chon gan voi ung dung:

```text
A Real-Time Webcam-Based Posture Monitoring Application Using MediaPipe Landmarks and a Lightweight ANN
```

## Cau truc bai bao Springer goi y

### Title

Ngan, ro bai toan, tranh noi qua ve clinical/medical.

### Abstract

Nen gom:

- Problem: sai tu the lam viec keo dai.
- Method: MediaPipe Pose, 99 landmark features, ANN, rule-based baseline, realtime app.
- Data: so video/mau train, external test neu da co.
- Results: accuracy/F1 local va external.
- Contribution: lightweight realtime app + interpretable baseline + logging.
- Limitation: dataset con nho, can validate them tren nhieu nguoi.

### Keywords

Posture detection; MediaPipe Pose; ergonomic monitoring; artificial neural network; real-time feedback; human pose estimation.

### 1. Introduction

Noi nen co:

- Tac hai cua sai tu the lam viec keo dai.
- Nhu cau giai phap chi dung webcam, it xam lan.
- Khoang trong: nhieu nghien cuu chi offline, thieu ung dung realtime co logging va feedback.
- Dong gop cua bai:
  - Pipeline landmark nhe.
  - Baseline rule-based co the giai thich.
  - ANN va danh gia tren du lieu rieng/external.
  - Ung dung desktop canh bao va thong ke.

### 2. Related Work

Can tim va trich dan nguon that cho:

- Human pose estimation va MediaPipe Pose.
- Ergonomic/posture assessment.
- Webcam-based posture detection.
- ML classifiers cho posture: ANN/SVM/KNN/CNN/LSTM.
- Real-time feedback systems.

Khong tu tao citation. Dung `reports/RELATED_WORK_TODO.md` sau TASK-028.

### 3. Materials and Methods

Nen chia:

1. System overview.
2. Data acquisition.
3. Pose landmark extraction.
4. Feature representation.
5. Rule-based baseline.
6. ANN classifier.
7. Realtime warning and logging.
8. Evaluation protocol.

### 4. Experiments

Can co:

- Dataset split hien tai: train/validation/test.
- External test.
- Neu lam duoc: video-wise/person-wise split.
- Metrics: accuracy, precision, recall, F1, confusion matrix.
- Baselines: rule-based vs ANN.
- Threshold sweep.

### 5. Results

Bang bat buoc:

| Table | Noi dung |
|---|---|
| Table 1 | Dataset distribution by class and split. |
| Table 2 | ANN architecture and parameters. |
| Table 3 | Local test metrics. |
| Table 4 | External test metrics. |
| Table 5 | Rule-based vs ANN comparison. |
| Table 6 | Ablation/threshold results neu co. |

Hinh nen co:

- Pipeline architecture.
- GUI screenshot.
- Sample pose landmarks.
- Training curves.
- Confusion matrix.
- SQLite/reporting workflow.

### 6. Discussion

Noi ve:

- Vi sao landmark feature nhe va du cho app realtime.
- ANN dat ket qua cao nhung can than voi leakage.
- Rule-based giup giai thich canh bao.
- External test va domain shift.
- Gioi han cua MediaPipe khi che mat, anh sang kem, goc quay la.

### 7. Limitations

Nen ghi ro:

- Dataset con nho va co the chua da dang.
- Frame-wise split co the thoi phong ket qua.
- Chua phai cong cu chan doan y te.
- Can nghien cuu voi nhieu nguoi, nhieu camera va dieu kien anh sang.
- Can danh gia tac dong canh bao len hanh vi nguoi dung trong thoi gian dai.

### 8. Conclusion

Tom tat he thong, ket qua, ung dung, va huong mo rong.

### Declarations

Springer thuong can cac muc:

- Funding.
- Conflict of interest.
- Ethics approval.
- Consent to participate.
- Consent for publication.
- Data availability.
- Code availability.
- Author contributions.

Neu la do an ca nhan, co the ghi placeholder va dien sau theo yeu cau truong/tap chi.

## Canh bao ve ket qua 99,8%

Ket qua local test hien tai rat cao:

- Accuracy: 0,998186.
- F1 incorrect: 0,998481.
- Confusion matrix: `[[665, 1], [2, 986]]`.

Trong bao cao, khong nen chi dua vao con so nay. Ly do: split hien tai theo frame co the de frame gan nhau cua cung video/nguoi xuat hien o ca train va test. Can bo sung external/video-wise/person-wise evaluation de ket qua co gia tri khoa hoc hon.

## Cau phat bieu dong gop de dung trong paper

```text
The main contribution of this work is an end-to-end, lightweight, webcam-based desk posture monitoring system that combines interpretable ergonomic rules with a compact neural classifier over MediaPipe pose landmarks, and integrates real-time feedback with session-level logging for practical workplace monitoring.
```

Ban tieng Viet:

```text
Dong gop chinh cua nghien cuu la mot he thong giam sat tu the lam viec realtime, nhe, dua tren webcam, ket hop cac luat cong thai hoc co the giai thich voi bo phan lop ANN gon nhe tren dac trung landmark MediaPipe, dong thoi tich hop canh bao va ghi nhan thong ke theo phien lam viec.
```
