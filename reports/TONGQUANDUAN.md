# Tong Quan Du An De Tai

Ngay cap nhat: 2026-05-28

De tai: **Xay dung ung dung phat hien loi tu the lam viec qua webcam su dung Computer Vision**

## 1. Tom tat ngan de trinh bay voi thay

Du an xay dung mot he thong desktop co kha nang phat hien loi tu the lam viec theo thoi gian thuc bang webcam/video. He thong su dung MediaPipe Pose de trich xuat 33 diem moc co the, dua cac diem moc nay vao mo hinh ANN de phan loai tu the dung/sai, dong thoi ket hop cac chi bao ergonomic rule-based de giai thich cac loi nhu lech vai, nghieng than, lech dau, rut co sau va tay gan mieng/chong cam.

Ngoai viec phan loai tung frame, du an con co ung dung desktop hoan chinh: hien thi camera realtime, canh bao am thanh khi sai tu the lien tuc, luu phien lam viec vao SQLite, dashboard thong ke, light/dark mode, va chi so **Temporal Posture Risk Index (TPRI)** de tong hop rui ro theo phien lam viec.

Huong nghien cuu phu hop de bao cao:

> Su dung mo hinh co san va pipeline Computer Vision pho bien, nhung tap trung vao du lieu thuc nghiem, dac trung ergonomic co kha nang giai thich, quy trinh danh gia, va ung dung realtime hoan chinh.

## 2. Bai toan va muc tieu

### Bai toan

Nguoi dung lam viec voi may tinh trong thoi gian dai thuong gap cac loi tu the:

- Cui dau.
- Rut co.
- Lech vai.
- Nghieng than.
- Chong cam hoac dua tay gan mat.
- Ngoi sai trong thoi gian dai ma khong tu nhan ra.

### Muc tieu cua du an

1. Phat hien tu the dung/sai qua webcam hoac video.
2. Canh bao khi nguoi dung sai tu the lien tuc qua mot nguong thoi gian.
3. Luu thong ke theo phien lam viec.
4. Hien thi dashboard truc quan de nguoi dung biet minh sai tu the bao lau, bi canh bao bao nhieu lan, va phien nao co rui ro cao.
5. Xay dung nen tang du lieu va danh gia de co the viet bao cao nghien cuu khoa hoc.

## 3. Du an hien da lam duoc gi

### 3.1 Ung dung desktop realtime

Ung dung hien tai da co:

- Giao dien desktop bang CustomTkinter.
- Ho tro webcam laptop.
- Ho tro video file.
- Ho tro camera IP/URL neu OpenCV doc duoc.
- Chuyen doi Light/Dark mode.
- Hien thi video realtime.
- Overlay trang thai len khung hinh:
  - `TU THE DUNG`
  - `SAI TU THE`
  - `KHONG PHAT HIEN NGUOI`
  - `DANG KIEM TRA`
- Canh bao am thanh khi sai tu the lien tuc.
- Cooldown canh bao de tranh lap am thanh lien tuc.
- Lam muot xac suat theo frame de giam nhieu.
- Luu cau hinh nguoi dung.
- Dashboard thong ke co tieng Viet co dau.

### 3.2 Xu ly Computer Vision

Pipeline xu ly:

```text
Webcam/Video
-> OpenCV doc frame
-> MediaPipe Pose phat hien 33 landmarks
-> Tao vector 99 dac trung x/y/z
-> StandardScaler chuan hoa
-> ANN phan loai dung/sai
-> Lam muot xac suat theo nhieu frame
-> Canh bao neu sai lien tuc qua nguong
-> Luu SQLite va hien dashboard
```

### 3.3 Du lieu hien co

Theo du lieu local hien tai:

| Nhom du lieu | So luong |
|---|---:|
| Video tu the dung trong `dataset/raw_videos/correct` | 34 |
| Video tu the sai trong `dataset/raw_videos/incorrect` | 50 |
| Tong video raw | 84 |
| External videos correct | 5 |
| External videos incorrect | 5 |
| Tong external videos | 10 |

Bo video raw hien tai duoc quay tren **5 nguoi khac nhau**. Sau khi xoa nguoi thu hai, ten file da duoc chuan hoa lai thanh cac ma lien tuc `P01`, `P02`, `P03`, `P04`, `P05`.

CSV hien co:

| File | Mo ta |
|---|---|
| `dataset/posture_data_2fps.csv` | Du lieu train 2 FPS, gom 99 landmark features va label. |
| `dataset/posture_external_test_2fps.csv` | Du lieu external test 2 FPS. |
| `dataset/processed/posture_external_test_2fps_with_metadata.csv` | External test co them metadata `source_video`, `frame_index`, `participant_id`, `view_angle`. |

### 3.4 Ket qua danh gia hien tai

Ket qua external test hien tai:

| Chi so | Gia tri |
|---|---:|
| So frame external test | 1697 |
| Accuracy | 79.316% |
| Precision lop sai tu the | 94.599% |
| Recall lop sai tu the | 65.985% |
| F1-score lop sai tu the | 77.743% |
| Macro F1 | 79.213% |
| MCC | 62.933% |
| ROC-AUC | 95.046% |
| PR-AUC | 95.747% |

Tai threshold 0.5, mo hinh co precision cao voi lop sai tu the, nghia la khi he thong bao sai thi kha chac. Tuy nhien recall con thap, nghia la van co mot so frame sai tu the bi bo sot. Khi giam threshold xuong 0.10, F1 lop sai tang len khoang 79.903%, phu hop hon voi bai toan canh bao neu uu tien giam bo sot.

## 4. Neu thay hoi: Diem moi cua du an la gi?

Nen tra loi theo huong:

> Diem moi cua du an khong nam o viec phat minh lai MediaPipe hay tao mot kien truc deep learning moi, ma nam o viec xay dung mot he thong webcam-based hoan chinh, co du lieu thuc nghiem rieng, co dac trung ergonomic co kha nang giai thich, co canh bao realtime, co logging theo phien, va co chi so rui ro theo thoi gian de danh gia tu the lam viec.

Chi tiet cac diem moi/co dong gop:

### 4.1 He thong end-to-end thay vi chi la notebook phan loai

Nhieu bai demo chi dung model de phan loai anh/frame. Du an nay xay dung day du pipeline:

```text
Camera/video -> nhan dien pose -> phan loai -> canh bao -> luu phien -> dashboard -> dong goi app desktop
```

Gia tri:

- Co the demo truc tiep.
- Gan voi bai toan thuc te cua nguoi lam viec voi may tinh.
- Co kha nang trien khai nhu mot san pham desktop.

### 4.2 Ket hop ANN voi rule-based ergonomic indicators

ANN dung de phan loai dung/sai dua tren landmark.

Rule-based ergonomic indicators dung de giai thich tai sao tu the co the sai:

- Lech vai.
- Nghieng vai.
- Nghieng than.
- Dau lech khoi truc vai.
- Mui gan ngang vai / rut co qua sau.
- Tay gan mieng / chong cam.

Gia tri moi:

- ANN cho kha nang hoc pattern tu du lieu.
- Rule-based cho kha nang giai thich.
- Khi demo, nguoi xem khong chi thay "sai tu the", ma con thay cac dau hieu hinh hoc lien quan.

### 4.3 Bo du lieu tu quay nhieu video, nhieu goc nhin

Du an co 84 video raw:

- 34 video dung.
- 50 video sai.
- Nhieu goc quay: front, side 30, side 90.
- 5 nguoi khac nhau sau khi chuan hoa participant ID.

Day la diem co gia tri vi bai toan tu the lam viec phu thuoc nhieu vao:

- Nguoi quay.
- Goc camera.
- Anh sang.
- Khoang cach den camera.
- Kieu sai tu the.

Tuy nhien, khi viet paper khong nen noi day la "benchmark dataset moi" neu chua public dataset va chua co metadata day du. Nen noi:

> Chung toi xay dung mot bo du lieu thuc nghiem rieng phuc vu danh gia so bo cho bai toan phat hien loi tu the lam viec qua webcam.

### 4.4 Co metadata de danh gia video-wise/person-wise

`source_video` la cot cho biet moi frame trong CSV den tu video nao. Cot nay rat quan trong vi giup danh gia cong bang hon.

Neu khong co `source_video`, viec chia train/test theo frame co the bi ro ri du lieu: frame gan nhau trong cung video rat giong nhau, neu mot so frame vao train va mot so frame vao test thi ket qua co the dep gia tao.

Huong dung hon:

- Train/test tach theo video.
- Train/test tach theo nguoi.
- Bao cao per-video va per-participant.

Day la diem thuyet phuc voi thay vi cho thay du an co y thuc ve kiem chung khoa hoc.

### 4.5 Temporal Posture Risk Index (TPRI)

TPRI la chi so rui ro theo phien, thang 0-100.

No khong chi nhin tung frame dung/sai, ma tong hop:

- Ty le thoi gian sai tu the.
- Sai tu the keo dai.
- So lan canh bao theo gio.
- Ty le khong phat hien nguoi / do tin cay thap.

Cong thuc:

```text
risk = 100 * (
  0.40 * ty_le_thoi_gian_sai
  + 0.25 * ty_le_sai_keo_dai
  + 0.20 * ty_le_canh_bao_theo_gio
  + 0.15 * ty_le_khong_phat_hien_nguoi
)
```

Gia tri moi:

- Chuyen ket qua tu frame-level sang session-level.
- Phu hop voi bai toan suc khoe/lao dong vi nguoi dung can biet ca phien lam viec co rui ro ra sao.
- Dashboard co the hien "rui ro trung binh" va "rui ro cao nhat" theo ngay.

### 4.6 Co quy trinh danh gia nghiem tuc hon demo thong thuong

Du an hien da co:

- External test set.
- Confusion matrix.
- Threshold sweep.
- ROC-AUC.
- PR-AUC.
- So sanh ANN voi rule-based baseline.
- Wilson confidence interval.
- McNemar paired test.

Dieu nay cho thay du an khong chi demo cam tinh, ma co so lieu kiem chung.

### 4.7 Co ung dung dong goi thanh san pham demo

Du an da co:

- Desktop app.
- Database runtime.
- Dashboard.
- Ban build PyInstaller `.exe`.
- Release zip.

Day la diem manh khi demo vi thay co the thay he thong chay duoc nhu mot ung dung that.

## 5. Diem nao khong nen noi qua

Khi thay hoi, nen tranh cac claim sau:

| Khong nen noi | Ly do |
|---|---|
| Mo hinh cua em la state-of-the-art | Chua co so sanh cung dataset voi cac nghien cuu manh. |
| MediaPipe landmark la dac trung moi | MediaPipe va pose landmarks da pho bien. |
| ANN la mo hinh moi | ANN dense classifier la mo hinh co san/co ban. |
| Dataset cua em la benchmark moi | Chua public, chua day du metadata/consent/protocol. |
| He thong co gia tri chan doan y te | Day la cong cu ho tro nhac nho tu the, khong phai thiet bi y te. |

Nen noi:

> Du an la mot he thong ung dung hoan chinh, co pipeline realtime, co du lieu tu thu thap, co dac trung ergonomic giai thich duoc, co danh gia external, va co chi so rui ro theo phien.

## 6. So voi nguoi khac thi khac o dau?

### 6.1 So voi cac demo dung webcam thong thuong

Khac biet:

- Khong chi detect pose, ma co ANN phan loai dung/sai.
- Khong chi hien frame, ma co canh bao theo thoi gian.
- Co luu session va dashboard.
- Co risk index theo phien.
- Co build app desktop.

### 6.2 So voi cac nghien cuu sensor chair/IMU

Nghien cuu dung cam bien ghe/IMU thuong co accuracy cao hon, nhung can phan cung rieng.

Du an nay:

- Chi can webcam.
- De trien khai hon.
- Chi phi thap.
- Phu hop voi laptop/work-from-home.

Han che:

- Phu thuoc anh sang, goc camera, MediaPipe landmark.
- Accuracy hien tai thap hon nhieu nghien cuu sensor/depth camera.

### 6.3 So voi cac nghien cuu chi bao cao accuracy

Du an nay co them:

- Canh bao realtime.
- Log theo phien.
- Dashboard.
- TPRI.
- Error/statistical analysis.

Day la khac biet ve **he thong ung dung va danh gia theo thoi gian**, khong chi phan loai tung frame.

## 7. Cach tra loi nhanh cac cau hoi thay co the hoi

### Cau hoi 1: Du an cua em moi o diem nao?

Tra loi:

> Diem moi cua em nam o viec tich hop thanh mot he thong hoan chinh cho bai toan tu the lam viec: webcam/video dau vao, MediaPipe landmarks, ANN phan loai, rule-based ergonomic indicators de giai thich loi, canh bao realtime, luu SQLite, dashboard thong ke, va TPRI de danh gia rui ro theo phien. Em khong claim MediaPipe hay ANN la moi, ma dong gop la pipeline ung dung, bo dac trung ergonomic va cach danh gia theo phien.

### Cau hoi 2: source_video la gi?

Tra loi:

> source_video la metadata cho biet moi frame trong CSV duoc trich tu video nao. No khong phai la file video trong CSV. Cot nay giup chia train/test theo video, tranh viec frame gan nhau trong cung video bi chia lan vao ca train va test.

### Cau hoi 3: Tai sao khong push video len GitHub?

Tra loi:

> Video raw rat nang va co yeu to rieng tu nguoi tham gia, nen em khong push len GitHub. Thay vao do, em luu metadata, CSV landmark da trich xuat, script trich xuat, va co the backup video bang o cung/cloud rieng. Neu can artifact, em co the cung cap link rieng hoac chi public landmark CSV.

### Cau hoi 4: Ket qua hien tai co tot khong?

Tra loi:

> Tren external test 1697 frame, ANN dat accuracy khoang 79.3%, F1 lop sai khoang 77.7%, ROC-AUC khoang 95.0% va PR-AUC khoang 95.7%. Ket qua nay tot hon rule-based baseline trong du an, nhung em chua claim tot hon cac nghien cuu khac vi dataset, sensor va protocol khac nhau.

### Cau hoi 5: Tai sao precision cao nhung recall chua cao?

Tra loi:

> Precision cao nghia la khi he thong bao sai thi kha chac. Recall chua cao nghia la van bo sot mot so tu the sai. Voi ung dung canh bao, co the giam threshold tu 0.5 xuong khoang 0.1 de tang recall va F1 lop sai. Day la ly do em co threshold sweep de chon nguong phu hop voi muc tieu ung dung.

### Cau hoi 6: Neu phat trien thanh bai bao, em se lam gi tiep?

Tra loi:

> Em se chuan hoa metadata cho 84 video, trich xuat lai CSV co source_video/frame_index/participant_id, danh gia video-wise va participant-wise, them ergonomic features, benchmark SVM/KNN/Random Forest/XGBoost/ANN, lam ablation study va error analysis. Huong bai bao se la mo hinh co san nhung du lieu, dac trung va quy trinh danh gia ro rang.

### Cau hoi 7: Tai sao can TPRI?

Tra loi:

> Accuracy theo frame chi cho biet tung frame dung hay sai. Trong thuc te, nguoi dung can biet ca phien lam viec co rui ro khong. TPRI tong hop thoi gian sai, sai keo dai, so lan canh bao va ty le mat nguoi/de tin cay thap thanh diem 0-100, giup dashboard danh gia rui ro theo phien/ngay.

## 8. Han che hien tai can noi ro

Du an con cac han che:

1. Dataset con nho, moi 84 video raw va external 10 video.
2. Can chuan hoa lai metadata de chung minh ro so nguoi tham gia.
3. Train CSV chinh hien chua co metadata, can trich xuat lai voi `--include-metadata`.
4. Chua co participant-wise validation day du.
5. Chua benchmark day du nhieu mo hinh ML tren cung split.
6. Chua co ablation study cho bo dac trung ergonomic.
7. Chua co runtime benchmark chinh thuc FPS/latency/CPU/RAM.
8. Chua public raw video do dung luong va quyen rieng tu.

Khi trinh bay, nen noi ro:

> Phien ban hien tai da du demo va co nen tang nghien cuu. Cac buoc tiep theo se tap trung vao chuan hoa du lieu, danh gia video-wise/person-wise, va benchmark de tang do tin cay khoa hoc.

## 9. Lo trinh ngan sau demo

### Buoc 1: Chuan hoa metadata

Tao file:

```text
dataset/metadata/video_manifest.csv
```

Cot de xuat:

```text
source_video,label,participant_id,view_angle,posture_type,duration_sec,fps,width,height,total_frames,file_size_mb,split,notes
```

### Buoc 2: Trich xuat lai CSV co metadata

Lenh:

```powershell
python src/2_extract_features.py --input-root dataset/raw_videos --sample-fps 2 --include-metadata --output dataset/processed/posture_data_2fps_with_metadata.csv
```

### Buoc 3: Danh gia theo video va theo nguoi

Can lam:

- Video-wise evaluation.
- Participant-wise evaluation.
- Leave-one-participant-out tren 5 nguoi.

### Buoc 4: Them ergonomic feature set

Them cac dac trung:

```text
shoulder_y_diff
shoulder_tilt_angle
torso_lean_angle
head_offset_x
nose_to_shoulder_y
nose_shoulder_clearance_ratio
neck_compression_detected
left_hand_mouth_ratio
right_hand_mouth_ratio
chin_rest_detected
visibility_mean
```

### Buoc 5: Benchmark va ablation

So sanh:

```text
Rule-based
Logistic Regression
KNN
SVM
Random Forest
Gradient Boosting / XGBoost
ANN
```

Ablation:

```text
Raw landmarks only
Ergonomic features only
Raw + ergonomic
Raw + ergonomic + temporal/session features
```

## 10. Cau chot nen noi khi demo

Co the ket thuc demo bang cau:

> Du an hien tai khong chi dung Computer Vision de nhan dien tu the theo tung frame, ma da phat trien thanh mot he thong desktop hoan chinh cho giam sat tu the lam viec. Dong gop chinh cua em la pipeline ung dung realtime, bo chi bao ergonomic co kha nang giai thich, du lieu video tu thu thap nhieu goc nhin, va chi so rui ro theo phien TPRI. Huong tiep theo cua em la chuan hoa metadata, danh gia theo video/theo nguoi, va benchmark nhieu mo hinh de hoan thien thanh bai bao nghien cuu khoa hoc.
