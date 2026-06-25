# Thesis Chapter Outline

Ngay cap nhat: 2026-05-28

## Chuong 1. Gioi thieu

- Boi canh sai tu the khi lam viec voi may tinh.
- Van de can giai quyet: canh bao sai tu the bang webcam, khong can cam bien.
- Muc tieu de tai.
- Pham vi: desktop app, webcam/video, binary correct/incorrect.
- Dong gop chinh.

## Chuong 2. Co so ly thuyet va cong trinh lien quan

- Computer Vision va pose estimation.
- MediaPipe Pose landmarks.
- Machine learning cho tabular pose features.
- Ergonomic posture assessment.
- Camera-based vs sensor-based posture monitoring.
- Khoang trong nghien cuu: thieu he thong app realtime co logging, dashboard, temporal risk.

## Chuong 3. Phuong phap de xuat

- Tong quan pipeline.
- Thu thap dataset va metadata.
- Trich xuat landmarks.
- Feature schema:
  - raw_99
  - normalized_99
  - ergonomic_14
  - combined feature sets
- Model registry va model selection.
- Threshold calibration.
- Temporal smoothing va Temporal Posture Risk Index.
- Kien truc desktop app.

## Chuong 4. Cai dat he thong

- Cau truc source code.
- Tkinter/CustomTkinter UI.
- MediaPipe/OpenCV pipeline.
- Model loading va inference.
- SQLite logging.
- Dashboard thong ke.
- Dong goi desktop app.

## Chuong 5. Thuc nghiem va danh gia

- Dataset statistics.
- Experimental protocol final.
- Model comparison.
- Threshold calibration.
- Final external evaluation.
- Participant-wise evaluation.
- Video-wise hard-case analysis.
- Feature importance.
- Temporal smoothing.
- Runtime benchmark.

## Chuong 6. Thao luan

- Ket qua tot nhat va y nghia.
- Vi sao normalized landmarks hieu qua.
- Loi con lai va hard-case taxonomy.
- So sanh ngu canh voi literature.
- Gioi han: external P01 only, dataset nho, binary labels, no clinical validation.

## Chuong 7. Ket luan va huong phat trien

- Tong ket he thong va ket qua.
- Huong mo rong dataset.
- Multi-class posture taxonomy.
- Tich hop model final vao app.
- Expert ergonomic validation.
- Public metadata/landmark dataset.

