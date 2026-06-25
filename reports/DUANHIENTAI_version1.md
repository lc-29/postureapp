# DU AN HIEN TAI - VERSION 1

**De tai:** Xay dung ung dung phat hien loi tu the lam viec qua webcam su dung Computer Vision  
**Ngay tong hop:** 30/05/2026  
**Muc dich file:** Tom tat nhanh de demo va trao doi voi thay huong dan ve quy trinh, ket qua hien tai, so lieu thuc nghiem, diem moi va nhung viec can lam tiep.

---

## 1. Tom tat ngan gon de trinh bay voi thay

Du an hien tai da xay dung duoc mot pipeline hoan chinh cho bai toan phat hien tu the lam viec dung/sai qua webcam hoac video. He thong dung OpenCV de doc camera/video, MediaPipe Pose de trich xuat 33 diem moc co the, sau do tao vector dac trung tu landmark va dua vao mo hinh hoc may de phan loai `Correct posture` va `Incorrect posture`.

Ung dung desktop da co giao dien Tkinter/CustomTkinter, co the mo webcam, IP camera hoac file MP4, hien thi skeleton MediaPipe, chay che do ANN hoac rule-based baseline, canh bao am thanh, lam muot xac suat, cooldown canh bao, luu lich su vao SQLite va hien thi thong ke theo ngay/phien.

Ve nghien cuu, du an dang di theo huong:

> **Existing model + new dataset/features**

Tuc la khong claim tao ra mo hinh AI moi, ma dong gop chinh nam o bo du lieu tu thu thap, metadata, dac trung normalized/ergonomic, baseline co kha nang giai thich, benchmark nhieu mo hinh va tich hop thanh app desktop realtime.

---

## 2. Quy trinh tong the cua du an

```text
Webcam / IP camera / MP4 video
        |
        v
OpenCV doc tung frame
        |
        v
MediaPipe Pose trich xuat 33 landmarks
        |
        v
Tao dac trung:
  - raw_99: 33 landmarks x/y/z
  - normalized_99: landmark da chuan hoa theo co the
  - ergonomic_14: cac chi bao dau, co, vai, than tren, tay
        |
        v
Phan loai tu the:
  - Rule-based baseline
  - ANN/Keras app model
  - Cac model benchmark: Logistic Regression, SVM, Random Forest,
    MLP sklearn, HistGradientBoosting
        |
        v
Lam muot theo nhieu frame + nguong quyet dinh + cooldown canh bao
        |
        v
Canh bao am thanh + hien thi GUI + luu SQLite
        |
        v
Dashboard thong ke / Bao cao / Ket qua thuc nghiem
```

---

## 3. Cac phan da lam duoc trong project

### 3.1 Ung dung desktop

| Hang muc | Trang thai hien tai |
|---|---|
| Mo webcam laptop | Da co |
| Mo IP camera | Da co |
| Mo video MP4 | Da co |
| Hien thi skeleton MediaPipe | Da co |
| Che do ANN | Da co, app hien dang dung ANN/Keras |
| Che do Rule-based Baseline | Da co de doi chieu va giai thich loi |
| Canh bao am thanh `.wav` | Da co |
| Cooldown canh bao | Da co |
| Lam muot xac suat nhieu frame | Da co |
| Chinh nguong sau lam muot | Da co |
| Light mode / dark mode | Da co |
| Luu SQLite | Da co |
| Dashboard thong ke | Da co |
| Xuat ban app desktop | Da co huong dan va build/release co ban |

### 3.2 Database SQLite

Database hien tai: `database/posture_app.db`

| Bang | So dong hien co | Vai tro |
|---|---:|---|
| `NguoiDung` | 1 | Luu nguoi dung mac dinh |
| `CaiDat` | 1 | Luu cau hinh app |
| `PhienLamViec` | 64 | Luu phien lam viec |
| `NhatKyTuThe` | 989 | Luu nhat ky tu the/canh bao |
| `ThongKeNgay` | 10 | Tong hop thong ke theo ngay |
| `ThongTinModel` | 1 | Luu thong tin model |

Y nghia khi demo: phan app khong chi phan loai tung frame, ma con co kha nang ghi nhan lich su de phan tich thoi quen lam viec theo phien/ngay.

---

## 4. Du lieu hien co

### 4.1 Du lieu goc va du lieu da xu ly

| Tap du lieu | So dong | So cot | Nhan `Correct` | Nhan `Incorrect` | Ghi chu |
|---|---:|---:|---:|---:|---|
| `dataset/posture_data.csv` | 5,377 | 100 | 2,169 | 3,208 | CSV landmark ban dau |
| `dataset/posture_data_2fps.csv` | 11,022 | 100 | 4,438 | 6,584 | Lay mau 2 FPS |
| `dataset/processed/posture_data_2fps_with_metadata.csv` | 11,022 | 108 | 4,438 | 6,584 | Co metadata |
| `dataset/processed/posture_data_2fps_combined_features.csv` | 11,022 | 122 | 4,438 | 6,584 | Co raw/metadata/ergonomic/combined features |
| `dataset/processed/posture_external_test_2fps_with_metadata.csv` | 1,658 | 108 | 768 | 890 | External corrected set |
| `dataset/processed/posture_external_test_2fps_combined_features.csv` | 1,658 | 122 | 768 | 890 | External set co combined features |

### 4.2 Video va nguoi tham gia

| Thanh phan | So luong | Ghi chu |
|---|---:|---|
| Raw training videos | 84 | Du lieu tu thu thap |
| Correct raw videos | 34 | Video tu the dung |
| Incorrect raw videos | 50 | Video tu the sai |
| External videos | 10 | 5 correct, 5 incorrect |
| Tong video trong manifest | 94 | 84 raw + 10 external |
| So nguoi trong raw dataset | 5 | P01-P05 |
| So nguoi trong external set | 1 | Hien chi co P01 |

Metadata hien co trong CSV gom cac truong nhu:

```text
source_video, frame_index, timestamp_sec, sample_fps,
video_fps, participant_id, view_angle, camera_type
```

Ghi chu quan trong khi trao doi voi thay: nhan `Correct/Incorrect` hien la nhan theo video/du an, chua phai nhan duoc xac nhan boi chuyen gia ergonomic, RULA hay REBA.

---

## 5. Dac trung dang dung

### 5.1 Nhom dac trung

| Feature set | So dac trung | Y nghia |
|---|---:|---|
| `raw_99` | 99 | 33 MediaPipe landmarks, moi diem gom x/y/z |
| `normalized_99` | 99 | Landmark duoc chuan hoa theo trung diem vai va scale theo co the |
| `ergonomic_14` | 14 | Cac chi bao hinh hoc co the giai thich ve dau, co, vai, than tren, tay |
| `combined_raw_ergonomic` | 113 | Raw landmarks + ergonomic features |
| `combined_normalized_ergonomic` | 113 | Normalized landmarks + ergonomic features |

### 5.2 Cac ergonomic features chinh

| Feature | Y nghia |
|---|---|
| `shoulder_y_diff` | Do lech cao/thap giua hai vai |
| `shoulder_tilt_angle` | Goc nghieng cua duong vai |
| `torso_lean_angle` | Do nghieng than tren |
| `head_offset_x` | Do lech ngang cua mui so voi trung diem vai |
| `nose_to_shoulder_y` | Vi tri doc cua mui so voi vai |
| `nose_shoulder_clearance_ratio` | Ti le khoang cach mui-vai, dung de nhan biet rut co/cui dau |
| `neck_compression_detected` | Co bao rut co sau |
| `left_hand_mouth_ratio` | Khoang cach tay trai den mieng/cam |
| `right_hand_mouth_ratio` | Khoang cach tay phai den mieng/cam |
| `chin_rest_detected` | Co bao tay gan mieng/cam/chong cam |
| `shoulder_width` | Do rong vai |
| `torso_length` | Do dai than tren proxy |
| `head_shoulder_distance` | Khoang cach dau-vai |
| `min_hand_mouth_ratio` | Khoang cach gan nhat giua tay va mieng/cam |

Diem co the noi voi thay:

> Diem moi khong phai la MediaPipe, vi MediaPipe la cong cu co san. Diem moi nam o cach em tao bo du lieu rieng, them metadata, chuan hoa landmark theo co the, them cac dac trung ergonomic co kha nang giai thich, roi benchmark nhieu mo hinh tren cung protocol.

---

## 6. Cac mo hinh va baseline

### 6.1 Model app hien tai

App desktop hien dang dung:

```text
ANN/Keras classifier
Dense 128 -> BatchNorm -> Dropout
Dense 64  -> BatchNorm -> Dropout
Dense 32  -> Dropout
Dense 1 sigmoid
```

Artifact lien quan:

```text
models/ann_best.keras
models/scaler.pkl
```

### 6.2 Baseline co kha nang giai thich

Rule-based baseline dung cac nguong hinh hoc de phat hien loi:

| Nhom rule | Y nghia |
|---|---|
| Vai lech | Hai vai khong can bang |
| Vai nghieng | Duong vai nghieng qua nguong |
| Than tren nghieng | Than tren nghieng ve mot phia |
| Dau lech | Mui/dau lech so voi trung diem vai |
| Mui gan vai | Kha nang cui dau/rut co |
| Tay gan mieng/cam | Kha nang chong cam |

Baseline nay khong phai de dat accuracy cao nhat, ma de lam moc doi chieu va giai thich tai sao mot tu the co the bi coi la sai.

### 6.3 Model benchmark da thu

Da benchmark cac mo hinh:

```text
Rule-based baseline
ANN/Keras
Logistic Regression
SVM RBF
Random Forest
MLP sklearn
HistGradientBoosting
```

Model tot nhat trong protocol hien tai:

```text
hist_gradient_boosting__normalized_99
threshold = 0.65
```

Luu y khi demo: app hien tai van dung ANN/Keras. HistGradientBoosting la model tot nhat trong thuc nghiem/benchmark, can tich hop vao app neu muon san pham cuoi cung dung model tot nhat.

---

## 7. Ket qua thuc nghiem hien tai

### 7.1 ANN app model so voi rule-based baseline

Danh gia tren corrected external set: 1,658 frame, 10 video external, P01.

| Model | Accuracy | Precision Incorrect | Recall Incorrect | F1 Incorrect | MCC |
|---|---:|---:|---:|---:|---:|
| Rule-based baseline | 67.49% | 63.49% | 92.81% | 75.40% | 37.56% |
| ANN/Keras app model | 90.17% | 95.61% | 85.62% | 90.34% | 80.90% |

Nhan xet:

- Rule-based co recall cao, tuc la bat duoc nhieu frame sai tu the.
- Nhung rule-based precision thap, nghia la de bao nham tu the dung thanh sai.
- ANN can bang tot hon, accuracy va F1 cao hon baseline.
- ANN tang F1 lop `Incorrect` tu 75.40% len 90.34%.

### 7.2 Model tot nhat sau benchmark va threshold calibration

Model: `hist_gradient_boosting__normalized_99`  
Threshold: `0.65`  
Tap danh gia: corrected external frame-level set, 1,658 frame.

| Metric | Gia tri |
|---|---:|
| Accuracy | 96.50% |
| Precision Incorrect | 96.22% |
| Recall Incorrect | 97.30% |
| F1 Incorrect | 96.76% |
| Macro F1 | 96.48% |
| MCC | 92.97% |
| ROC-AUC | 99.09% |
| PR-AUC | 99.21% |
| Brier score | 0.0339 |
| False Positive | 34 |
| False Negative | 24 |

Confusion matrix co the dien giai:

|  | Du doan Correct | Du doan Incorrect |
|---|---:|---:|
| That Correct | 734 | 34 |
| That Incorrect | 24 | 866 |

Nhan xet:

- Ket qua nay tot nhat trong protocol local hien tai.
- Tuy nhien threshold 0.65 da duoc hieu chinh tren corrected external set, nen khi viet bao phai noi trung thuc la **calibrated external performance**, khong coi nhu hold-out doc lap tuyet doi.
- Khong duoc claim state-of-the-art vi external set nho va moi co P01.

### 7.3 Bang xep hang mot so model benchmark

| Model | Feature set | Accuracy | Precision Incorrect | Recall Incorrect | F1 Incorrect | MCC |
|---|---|---:|---:|---:|---:|---:|
| HistGradientBoosting | `normalized_99` | 95.96% | 95.07% | 97.53% | 96.28% | 91.89% |
| Random Forest | `normalized_99` | 95.90% | 94.67% | 97.87% | 96.24% | 91.79% |
| SVM RBF | `ergonomic_14` | 95.36% | 96.89% | 94.38% | 95.62% | 90.72% |
| SVM RBF | `normalized_99` | 94.51% | 92.82% | 97.30% | 95.01% | 89.04% |
| Random Forest | `combined_normalized_ergonomic` | 94.27% | 91.89% | 97.98% | 94.83% | 88.65% |

Nhan xet:

- `normalized_99` dang cho ket qua rat tot.
- `ergonomic_14` it feature hon nhung van dat ket qua cao voi SVM RBF, nen co gia tri giai thich va co the viet thanh ablation study.
- Combined features khong luon tot hon normalized_99, cho thay viec them feature phai duoc kiem chung chu khong mac dinh la tot hon.

### 7.4 Danh gia theo nguoi tham gia

Protocol: leave-one-participant-out tren raw dataset.

| Held-out participant | So frame | Accuracy | Precision Incorrect | Recall Incorrect | F1 Incorrect | MCC |
|---|---:|---:|---:|---:|---:|---:|
| P01 | 3,524 | 90.81% | 98.28% | 84.88% | 91.09% | 82.64% |
| P02 | 1,225 | 79.35% | 77.87% | 91.55% | 84.16% | 56.55% |
| P03 | 2,208 | 93.03% | 99.85% | 90.05% | 94.70% | 85.55% |
| P04 | 1,815 | 86.67% | 79.37% | 100.00% | 88.50% | 75.92% |
| P05 | 2,250 | 93.56% | 95.63% | 94.24% | 94.93% | 86.11% |

Tong hop:

| Chi so | Gia tri trung binh |
|---|---:|
| Mean Accuracy | 88.68% |
| Mean F1 Incorrect | 90.67% |
| Mean Macro F1 | 87.93% |
| Mean MCC | 77.35% |

Nhan xet:

- Ket qua theo nguoi tham gia cho thay model co kha nang tong quat o muc kha, nhung chua dong deu.
- P02 la nguoi kho nhat, F1 Incorrect 84.16%, MCC 56.55%.
- Day la diem can noi thang voi thay: du lieu con it nguoi nen can them participant de ket qua vung hon.

### 7.5 Runtime/FPS

Benchmark tren 3 video dai dien, resolution 640x360, MediaPipe complexity 1, toi da 120 frame/video.

| View angle | Processed frames | Pose detection rate | Mean latency | P95 latency | Estimated FPS |
|---|---:|---:|---:|---:|---:|
| front | 52 | 100.00% | 35.32 ms | 38.81 ms | 28.32 FPS |
| side_30 | 120 | 100.00% | 35.67 ms | 43.08 ms | 28.03 FPS |
| side_90 | 120 | 100.00% | 34.09 ms | 38.95 ms | 29.34 FPS |

Nhan xet:

- Toc do xu ly MediaPipe + classifier dat khoang 28-29 FPS, phu hop de demo gan realtime.
- Day la benchmark xu ly frame, chua phai full GUI FPS vi GUI con co ve skeleton, Tkinter scheduling, camera buffering, am thanh va ghi SQLite.

---

## 8. Diem moi cua du an nen noi voi thay

Nen trinh bay theo cach khiem ton, khong noi la mo hinh moi hay state-of-the-art:

1. **Du lieu tu thu thap cho bai toan tu the lam viec**
   - 84 video raw, 5 nguoi tham gia, 11,022 frame lay mau 2 FPS.
   - Co external corrected set 10 video, 1,658 frame.
   - Co metadata: video nguon, frame, thoi gian, participant, view angle, camera type.

2. **Bo dac trung co cau truc ro rang**
   - So sanh `raw_99`, `normalized_99`, `ergonomic_14` va cac feature combined.
   - Normalized landmarks giup giam phu thuoc vao kich thuoc co the/vi tri camera.
   - Ergonomic features giup giai thich cac loi dau, co, vai, than tren, tay.

3. **Co baseline giai thich duoc**
   - Rule-based khong chi de so sanh, ma con giup giai thich tai sao tu the bi coi la sai.
   - Day la diem can thiet khi trinh bay voi thay va khi viet bao.

4. **Co benchmark nhieu mo hinh**
   - Khong chi dung ANN.
   - Da so sanh Logistic Regression, SVM, Random Forest, MLP, HistGradientBoosting.
   - Co model selection theo F1 Incorrect, Recall Incorrect va MCC.

5. **Co app desktop end-to-end**
   - Doc webcam/video.
   - Hien skeleton.
   - Canh bao realtime.
   - Luu SQLite.
   - Dashboard thong ke.
   - Co light/dark mode va cac tham so canh bao.

6. **Co danh gia theo nhieu goc**
   - External frame-level.
   - Video-wise error analysis.
   - Participant-wise evaluation.
   - Runtime FPS.
   - Threshold calibration.
   - Feature/model comparison.

---

## 9. Nhung diem can noi ro de tranh bi hoi kho

### 9.1 Khong nen claim

Khong nen noi:

```text
Mo hinh cua em la state-of-the-art.
MediaPipe landmarks la dac trung moi.
ANN cua em la mo hinh moi.
Ket qua 96.50% chung minh he thong tot hon cac nghien cuu khac.
```

Nen noi:

```text
He thong cua em di theo huong existing model + new dataset/features.
Dong gop chinh la pipeline webcam desktop, bo du lieu tu thu thap,
feature schema, ergonomic indicators, baseline giai thich, benchmark nhieu model
va danh gia realtime/app logging.
```

### 9.2 Han che hien tai

| Han che | Anh huong | Huong khac phuc |
|---|---|---|
| Dataset moi co 5 nguoi | Do tong quat chua cao | Quay them nguoi, them gioi tinh/than hinh/khoang cach camera |
| External set chi co P01 | External chua da dang | Tao external set cho P02-P05 hoac nguoi moi |
| Nhan Correct/Incorrect la project-specific | Chua co chuan ergonomic chuyen gia | Moi thay/chuyen gia xem nhan, hoac bo sung RULA/REBA |
| HGB la model benchmark tot nhat nhung app dang dung ANN | App chua dung model tot nhat | Tich hop model registry/HGB vao app |
| Full GUI FPS chua do | Chua biet FPS thuc khi ve GUI + logging | Do FPS khi app chay that voi webcam |
| Chua benchmark public dataset | Bai bao chua co doi chieu public benchmark | Thu MultiPosture/SitPose neu con thoi gian |

---

## 10. Kich ban demo ngan voi thay

### Buoc 1 - Gioi thieu bai toan

Noi ngan:

> De tai cua em la xay dung ung dung phat hien loi tu the lam viec qua webcam. He thong huong toi moi truong hoc tap/lam viec voi laptop, khong can cam bien vat ly hay camera do sau.

### Buoc 2 - Noi pipeline

Noi ngan:

> Pipeline hien tai gom OpenCV doc webcam/video, MediaPipe Pose trich xuat 33 landmarks, tao raw/normalized/ergonomic features, sau do phan loai Correct/Incorrect bang ANN hoac cac model hoc may. App co canh bao am thanh, smoothing, cooldown va luu SQLite de thong ke theo phien.

### Buoc 3 - Noi du lieu

Noi ngan:

> Dataset tu thu thap hien co 84 video raw tren 5 nguoi, lay mau thanh 11,022 frame o 2 FPS, trong do 4,438 frame dung va 6,584 frame sai. External corrected set co 10 video, 1,658 frame, hien moi co P01 nen em xem day la han che can mo rong.

### Buoc 4 - Noi ket qua

Noi ngan:

> Tren external set, ANN app model dat accuracy 90.17% va F1 lop sai 90.34%, cao hon rule-based baseline 67.49% accuracy va 75.40% F1. Sau khi benchmark nhieu model, HistGradientBoosting voi normalized_99 dat ket qua tot nhat: accuracy 96.50%, F1 lop sai 96.76%, MCC 92.97%, nhung model nay hien la ket qua thuc nghiem, chua tich hop vao app.

### Buoc 5 - Mo app demo

Thu tu demo nen lam:

1. Chay app desktop.
2. Chon input webcam hoac video MP4.
3. Chay ANN mode.
4. Cho thay skeleton MediaPipe va nhan Correct/Incorrect.
5. Co tinh ngoai sai tu the de app canh bao.
6. Giai thich smoothing/cooldown/threshold.
7. Mo dashboard/thong ke.
8. Neu co thoi gian, chuyen qua Rule-based Baseline de so sanh giai thich.

### Buoc 6 - Noi viec can lam tiep

Noi ngan:

> Huong tiep theo cua em la mo rong dataset them nguoi, chuan hoa nhan bang y kien chuyen gia/RULA/REBA neu co the, tich hop model benchmark tot nhat vao app, do full GUI FPS, va neu viet bao Springer thi se trinh bay theo huong existing model + new dataset/features.

---

## 11. Cau hoi thay co the hoi va cach tra loi

### Cau 1: Diem moi cua de tai la gi?

Tra loi goi y:

> Diem moi cua em khong nam o viec tao pose estimator moi. Em dung MediaPipe Pose co san, nhung dong gop nam o pipeline ung dung hoan chinh cho tu the lam viec qua webcam, bo du lieu tu thu thap co metadata, feature schema raw/normalized/ergonomic, baseline rule-based co kha nang giai thich, benchmark nhieu model va app desktop realtime co SQLite logging.

### Cau 2: Tai sao khong dung moi rule-based?

Tra loi goi y:

> Rule-based de giai thich tot nhung de bao nham vi nguong co dinh kho phu hop moi nguoi va moi goc camera. Ket qua external cho thay rule-based accuracy 67.49%, F1 Incorrect 75.40%, trong khi ANN dat 90.17% accuracy va 90.34% F1 Incorrect.

### Cau 3: Tai sao HGB tot hon ANN nhung app van dung ANN?

Tra loi goi y:

> ANN la model da tich hop trong app tu dau. Sau do em benchmark them nhieu model va thay HistGradientBoosting voi normalized_99 tot hon trong protocol hien tai. Viec tiep theo la tich hop model registry/HGB vao app de san pham dung model tot nhat.

### Cau 4: Dataset da du manh de viet bao chua?

Tra loi goi y:

> Dataset hien co du de lam demo va viet ban thao nghien cuu ung dung ban dau, nhung de bai bao thuyet phuc hon can them nguoi tham gia, them external set da dang hon, va neu co the can nhan duoc doi chieu boi chuyen gia ergonomic hoac RULA/REBA.

### Cau 5: Ket qua 96.50% co phai la tot hon nghien cuu khac khong?

Tra loi goi y:

> Em khong claim nhu vay vi moi nghien cuu dung dataset, cam bien, nhan va protocol khac nhau. Ket qua 96.50% chi la trong protocol local cua em sau calibration tren corrected external set. Diem dung de claim an toan la model benchmark tot hon baseline va ANN trong cung du lieu/protocol cua du an.

---

## 12. Viec can lam tiep theo theo thu tu uu tien

### Uu tien cao

1. Tich hop model tot nhat `hist_gradient_boosting__normalized_99` vao app hoac ghi ro app chi dung ANN.
2. Quay them external videos cho P02-P05 hoac nguoi moi.
3. Do full GUI FPS khi chay webcam that, co ve skeleton, audio, smoothing va SQLite.
4. Chuan hoa file demo: chon video ngan, goc nhin ro, co ca dung va sai.
5. Chup screenshot app khi chay de dua vao bao cao/bai bao.

### Uu tien trung binh

1. Them nhan chi tiet hon: cui dau, lech vai, nghieng than, rut co, chong cam.
2. Them expert annotation hoac checklist ergonomic neu thay yeu cau.
3. Chay benchmark tren public dataset neu tim duoc dataset phu hop.
4. Them ablation ro hon: raw_99 vs normalized_99 vs ergonomic_14 vs combined.
5. Viet them phan error analysis theo video va theo nguoi.

### Chua nen lam luc nay

1. Doi huong sang YOLO/CNN/web/mobile neu khong co yeu cau.
2. Claim mo hinh moi hoac state-of-the-art.
3. Lam qua nhieu tinh nang GUI phu trong khi dataset/evaluation chua manh.
4. Doi kien truc lon truoc ngay demo.

---

## 13. Cau noi tong ket nen dung khi demo

> Hien tai du an cua em da co pipeline hoan chinh tu webcam/video den MediaPipe Pose, feature extraction, ANN/rule-based detection, canh bao realtime, SQLite logging va dashboard thong ke. Ve thuc nghiem, dataset tu thu thap co 84 video raw tren 5 nguoi va 11,022 frame lay mau 2 FPS. ANN app model dat 90.17% accuracy va 90.34% F1 lop sai tren corrected external set. Sau benchmark, model HistGradientBoosting voi normalized_99 dat 96.50% accuracy va 96.76% F1 lop sai trong protocol hien tai. Huong tiep theo cua em la mo rong dataset, tich hop model tot nhat vao app, do full GUI FPS va lam nhan ergonomic chat che hon de phuc vu luan van/bai bao.

