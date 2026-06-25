# 19_TASK_RUT_GON_CAU_TRUC_APPLIED_RESEARCH_VA_BO_SUNG_REFERENCES

## Muc tieu

Chinh sua ban thao bai bao nghien cuu khoa hoc cua du an theo huong **Applied Research / Nghien cuu ung dung**, rut gon cac muc nho thanh nhung muc lon chinh, dong thoi bo sung va chon loc danh sach references len khoang **25 nguon lien quan that su**.

Bai sau khi chinh phai giong mot bai bao khoa hoc Springer hon, khong giong bao cao project/luan van qua chi tiet. Van giu dung huong nghien cuu cua du an:

```text
Existing model + new dataset/features + webcam-based desktop application
```

Khong claim mo hinh moi, khong claim state-of-the-art, khong bia so lieu, khong bia DOI, khong bia dataset, khong bia ket qua thuc nghiem.

---

## Nguyen tac bat buoc

- Khong sua code nguon.
- Khong xoa file bao cao cu.
- Khong doi huong sang web/mobile/YOLO/CNN/CNN end-to-end.
- Khong dua chi so ao, bang ao, citation ao.
- Khong tu bia DOI. Neu khong tim thay DOI trong file/project/nguon chinh thong thi ghi ro la khong co DOI hoac can kiem tra lai.
- Khong dung blog/tutorial lam nguon hoc thuat chinh.
- Official documentation nhu MediaPipe, OpenCV, TensorFlow chi dung cho Methodology/Implementation, khong thay the Related Work hoc thuat.
- References phai lien quan den Computer Vision, Human Pose Estimation, MediaPipe/OpenPose, sitting/working posture recognition, ergonomic posture assessment, ML classifier benchmark, hoac dataset/benchmark lien quan.
- Van phong trung lap, ngan gon, co so lieu cu the, tranh cac cum:
  - transformative
  - groundbreaking
  - revolutionary
  - state-of-the-art
  - in summary
  - context-aware multi-stage source-aware
- Neu thieu thong tin, ghi vao report/checklist rieng, khong chen cau tho vao manuscript.

---

## File can doc truoc

Doc cac file sau de nam trang thai hien tai:

```text
reports/SPRINGER_MANUSCRIPT_REVISED.md
reports/SPRINGER_MANUSCRIPT_REVISED_VN.md
reports/SPRINGER_MANUSCRIPT_FINAL_DRAFT.md
reports/SPRINGER_MANUSCRIPT_FINAL_DRAFT_VN.md
reports/SPRINGER_MANUSCRIPT_MAIN_REVISED_VN.md
reports/springer_overleaf/main_revised.tex
reports/FINAL_EVALUATION_REPORT.md
reports/MODEL_SELECTION_REPORT.md
reports/RUNTIME_BENCHMARK.md
reports/EXPERIMENT_PROTOCOL_FINAL.md
reports/FEATURE_SCHEMA_FINAL.md
reports/LITERATURE_METRICS_COMPARISON.md
reports/TAILIEUTHAMKHAO.md
reports/RELATED_PAPERS.bib
reports/FIGURE_EXPORT_TODO.md
```

Neu co file references hoac literature khac trong `reports/`, tu tim bang `rg` voi cac tu khoa:

```text
references
citation
doi
posture
MediaPipe
OpenPose
sitting posture
working posture
ergonomic
```

---

## Cau truc bai bao moi can ap dung

Rut gon bai bao thanh 6 muc lon. Ten muc co the tinh chinh de dung hoc thuat hon, nhung nen theo khung sau:

```text
1. Introduction
2. Related Work
3. Proposed Webcam-Based Posture Monitoring System
4. Experimental Protocol
5. Evaluation and Discussion
6. Conclusion and Future Work
```

Giai thich:

- Muc 3 thay cho cach goi "Our". Khong nen dat tieu de chi la "Our" vi khong chuan hoc thuat.
- Muc 4 gom cac noi dung ve dataset split, feature groups, model protocol, training/evaluation setup.
- Muc 5 gom ket qua, so sanh model, runtime, phan tich loi, han che trong danh gia.
- Neu can trinh bay limitation, dat thanh subsection ngan trong Muc 5 hoac cuoi Muc 6, khong tach thanh mot section lon rieng neu bai dang qua nhieu muc.

---

## Mapping tu cau truc cu sang cau truc moi

### Tu cau truc cu

```text
Introduction
Related Work
Proposed Method
Dataset and Feature Extraction
Experimental Setup
Results and Discussion
Desktop Application Implementation
Limitations
Data, Code, and Ethics Note
Conclusion and Future Work
References
```

### Sang cau truc moi

```text
1. Introduction
   - Giu van de thuc te.
   - Giu research gap.
   - Giu 3 dong gop chinh.
   - Rut gon cac cau qua dai hoac qua giong bao cao.

2. Related Work
   - Giu 3 nhom:
     1. Sensor-based and depth-camera-based posture recognition.
     2. RGB vision-based posture recognition.
     3. Pose-landmark-based posture analysis using OpenPose/MediaPipe.
   - Moi nhom phai co nhan xet ve han che/gap.
   - Doan cuoi phai chot research gap va dan sang de xuat cua bai.

3. Proposed Webcam-Based Posture Monitoring System
   - Gop Proposed Method + Desktop Application Implementation + phan feature extraction can thiet.
   - Mo ta pipeline:
     Webcam/IP camera/MP4 -> OpenCV -> MediaPipe Pose -> Feature Construction -> Classifier -> Temporal Smoothing -> Warning -> SQLite Logging.
   - Giu Algorithm 1 neu co.
   - Giu cong thuc feature normalization neu co va giai thich bien.
   - Trinh bay app nhu mot implementation de kiem chung pipeline, khong viet nhu quang cao san pham.

4. Experimental Protocol
   - Gop Dataset and Feature Extraction + Experimental Setup.
   - Trinh bay dataset theo split, khong qua file-oriented.
   - Trinh bay feature groups: raw_99, normalized_99, ergonomic_14, combined.
   - Trinh bay models: Rule-based, ANN/Keras, Logistic Regression, SVM RBF, Random Forest, MLP sklearn, HistGradientBoosting.
   - Noi ro ANN la model tich hop trong app, HGB la selected experimental model.
   - Noi ro threshold 0.65 va cach dien giai threshold calibration.
   - Noi ro metric va cong thuc Accuracy, Precision, Recall, F1-score, MCC neu co.

5. Evaluation and Discussion
   - Gop Results and Discussion + Limitations.
   - Giu bang:
     - Dataset distribution.
     - Rule-based vs ANN.
     - Top classifier/feature comparison.
     - Final selected model.
     - Participant-wise evaluation.
     - Runtime FPS.
   - Moi bang phai co doan giai thich ngay sau bang.
   - Dua phan limitation thanh subsection ngan:
     - 5 participants.
     - External set only P01.
     - Project-specific labels.
     - No expert ergonomic annotation.
     - No public benchmark evaluation yet.
     - Full GUI FPS not yet measured.
     - App currently uses ANN/HGB option can be clarified depending on actual app state.

6. Conclusion and Future Work
   - Khong citation.
   - Khong dua so lieu moi.
   - Nhac lai dong gop va ket qua chinh.
   - Future work ngan gon:
     - more participants;
     - expert annotation/RULA/REBA;
     - public benchmark such as MultiPosture if suitable;
     - stronger subject-independent validation;
     - multi-class posture labels;
     - complete product packaging if needed.
```

---

## References: yeu cau bo sung len khoang 25 nguon

Hien tai project co khoang 20 link/tai lieu trich dan. Nhiem vu la kiem tra lai va bo sung them de tong danh sach chon loc khoang **25 references chat luong**.

### Buoc 1. Kiem ke references hien co

Doc:

```text
reports/TAILIEUTHAMKHAO.md
reports/RELATED_PAPERS.bib
reports/LITERATURE_METRICS_COMPARISON.md
reports/springer_overleaf/main_revised.tex
```

Tao bang kiem ke:

```text
reports/REFERENCES_25_SELECTION_AUDIT.md
```

Bang can co cot:

```text
STT | Ten tai lieu | Tac gia/nam | Link/DOI/URL | Loai nguon | Phan dung trong bai | Giu/Loai | Ly do
```

### Buoc 2. Tim them nguon lien quan

Can tim them tren Google Scholar, Crossref, IEEE Xplore, Springer, ScienceDirect, MDPI, Sensors, IEEE Access, arXiv hoac trang dataset chinh thuc.

Neu dung web search, chi lay thong tin tu nguon co the kiem tra:

- Publisher page.
- DOI page.
- arXiv page.
- IEEE/Springer/Elsevier/MDPI official page.
- GitHub/dataset page chinh thuc neu la dataset/tool.
- Official documentation neu la MediaPipe/OpenCV/TensorFlow.

Khong lay citation tu blog tong hop neu khong co nguon goc.

### Goi y nhom nguon can co

Danh sach 25 references nen can bang theo cac nhom:

```text
1. Human pose estimation / MediaPipe / BlazePose / OpenPose: 4-6 nguon.
2. Sitting posture / working posture recognition using RGB or pose landmarks: 6-8 nguon.
3. Sensor-based, pressure-based, RGB-D/depth-camera posture recognition: 3-5 nguon.
4. Ergonomic assessment / RULA / REBA / musculoskeletal risk: 2-4 nguon.
5. Dataset/benchmark lien quan: 2-4 nguon.
6. Official documentation for implementation: 2-3 nguon.
```

### Cac nguon nen uu tien kiem tra

Kiem tra trong project truoc, neu da co thi giu va chuan hoa:

- BlazePose / MediaPipe Pose paper.
- MediaPipe framework.
- OpenPose paper.
- MultiPosture dataset.
- SitPose hoac sitting posture dataset lien quan neu co nguon chinh thuc.
- Carneros-Prado et al. IEEE Access neu lien quan sitting posture.
- Estrada et al. 2023 neu lien quan posture/vision.
- Chen 2019 OpenPose sitting posture neu co trong references.
- Nadeem et al. sitting posture review neu co.
- Krauter et al. sitting posture recognition and feedback review neu co.
- Kulikajevas et al. 2021 neu lien quan pose/ergonomics.
- Roggio et al. 2024 review neu lien quan posture/ergonomics.
- ALIGN realtime sitting posture neu co.
- Tsai et al. pressure sensor baseline neu co.
- RULA/REBA foundational ergonomic assessment papers neu can dung cho Discussion/Future Work.

Neu mot nguon khong tim thay thong tin chac chan, dua vao audit voi trang thai:

```text
Can kiem tra lai tren Google Scholar/Crossref/Publisher
```

Khong dua vao danh sach references chinh neu khong xac minh duoc.

---

## File dau ra can tao

Tao cac file moi, khong xoa file cu:

```text
reports/SPRINGER_MANUSCRIPT_APPLIED_RESEARCH_RESTRUCTURED.md
reports/SPRINGER_MANUSCRIPT_APPLIED_RESEARCH_RESTRUCTURED_VN.md
reports/REFERENCES_25_SELECTION_AUDIT.md
reports/RELATED_PAPERS_25_SELECTED.bib
reports/APPLIED_RESEARCH_RESTRUCTURE_REPORT.md
```

Neu chinh sua duoc Overleaf source, tao them file moi:

```text
reports/springer_overleaf/main_applied_research.tex
```

Neu build PDF thanh cong, xuat them:

```text
reports/springer_overleaf/main_applied_research.pdf
```

Khong ghi de `main_revised.tex` tru khi nguoi dung yeu cau.

---

## Yeu cau noi dung ban tieng Anh

### Title

De xuat tieu de trung lap, vi du:

```text
Webcam-Based Working Posture Error Detection Using MediaPipe Pose and Lightweight Machine Learning
```

Khong dung title claim qua manh.

### Abstract

- Duoi 250 tu.
- Co 5 y:
  1. van de;
  2. phuong phap;
  3. dataset;
  4. ket qua chinh;
  5. dong gop.
- Khong citation trong Abstract.
- Khong liet ke qua nhieu thu vien.

### Keywords

3-5 keywords, vi du:

```text
Working posture detection; MediaPipe Pose; Human pose estimation; Machine learning; Webcam-based monitoring
```

### Introduction

Can co:

- Van de sai tu the khi lam viec voi may tinh.
- Nhu cau giai phap webcam chi phi thap, khong tiep xuc.
- Han che cua sensor/smart chair/RGB-D/depth camera hoac cac nghien cuu thieu desktop end-to-end.
- Research gap.
- 3 contributions ngan gon.

### Related Work

Khong liet ke tai lieu roi rac. Moi doan phai so sanh va dan ra gap.

### Proposed System

Can co pipeline, algorithm, feature groups, classifier, smoothing, warning, logging.

### Experimental Protocol

Phai co:

- Development set: 84 videos, 5 participants P01-P05, 11,022 samples, 4,438 Correct, 6,584 Incorrect.
- Corrected external set: 10 videos, P01, 1,658 samples, 768 Correct, 890 Incorrect.
- Labels are project-specific.
- External set only P01.
- Models compared.
- Threshold 0.65 and its interpretation.
- Metrics.

### Evaluation and Discussion

Phai giu cac so lieu that trong project:

- Rule-based external: Accuracy 67.49%, F1 Incorrect 75.40%.
- ANN external: Accuracy 90.17%, F1 Incorrect 90.34%.
- Final selected model: `hist_gradient_boosting__normalized_99`.
- Final selected model external/calibrated performance:
  - Accuracy 96.50%.
  - Precision Incorrect 96.22%.
  - Recall Incorrect 97.30%.
  - F1 Incorrect 96.76%.
  - MCC 92.97%.
  - FP 34.
  - FN 24.
- Participant-wise raw dataset: Mean F1 Incorrect 90.67%.
- Runtime:
  - front 28.32 FPS.
  - side_30 28.03 FPS.
  - side_90 29.34 FPS.

Neu phat hien so lieu trong report moi khac voi tren, uu tien so lieu trong file ket qua moi nhat va ghi vao restructure report.

---

## Yeu cau ban tieng Viet

Tao ban tieng Viet doi chieu:

```text
reports/SPRINGER_MANUSCRIPT_APPLIED_RESEARCH_RESTRUCTURED_VN.md
```

Ban tieng Viet phai:

- Giu cung cau truc 6 muc.
- Giu cung bang va so lieu.
- Khong can dich may moc tung chu, nhung phai dung nghia hoc thuat.
- Dung thuat ngu nhat quan:
  - Tu the dung.
  - Tu the sai.
  - Moc co the MediaPipe Pose.
  - He thong giam sat tu the dua tren webcam.
  - Baseline dua tren luat.
  - Mo hinh ANN/Keras trong ung dung.
  - Mo hinh HistGradientBoosting duoc chon trong thuc nghiem.

---

## Kiem tra references cuoi cung

Trong `REFERENCES_25_SELECTION_AUDIT.md`, can tong hop thanh 5 nhom:

```text
A. Nguon bat buoc nen giu.
B. Nguon nen giu cho MediaPipe/OpenPose/Human Pose Estimation.
C. Nguon nen giu cho posture recognition/ergonomics.
D. Nguon dataset/benchmark.
E. Nguon nen loai hoac chi tham khao ky thuat.
```

Danh sach references chinh trong manuscript nen co khoang 25 nguon, uu tien peer-reviewed. Neu chi co 23-24 nguon that su phu hop thi chap nhan 23-24 hon la chen nguon yeu cho du so.

---

## Checklist tu kiem tra sau khi lam xong

Tao file:

```text
reports/APPLIED_RESEARCH_RESTRUCTURE_REPORT.md
```

Trong file nay phai tra loi cac cau sau:

```text
1. Bai da rut gon con 6 muc lon chua?
2. Cac tieu de muc co dung huong Applied Research khong?
3. Abstract co duoi 250 tu khong?
4. Keywords co 3-5 tu khoa khong?
5. Related Work co chot research gap khong?
6. Proposed System co pipeline va pseudocode khong?
7. Dataset co trinh bay theo split thay vi chi theo ten file khong?
8. Experiment co phan biet ANN app model va HGB selected experimental model khong?
9. Evaluation co dung so lieu that tu project khong?
10. Co con citation/DOI/dataset nao chua xac minh khong?
11. Tong references chon loc la bao nhieu?
12. Co nguon blog/tutorial nao bi dung nhu paper hoc thuat khong?
13. Co claim state-of-the-art hoac model moi khong?
14. Conclusion co citation khong?
15. Cac han che hoc thuat co duoc neu trung thuc khong?
```

---

## Tieu chi hoan thanh

Task duoc xem la hoan thanh khi co du cac file:

```text
reports/SPRINGER_MANUSCRIPT_APPLIED_RESEARCH_RESTRUCTURED.md
reports/SPRINGER_MANUSCRIPT_APPLIED_RESEARCH_RESTRUCTURED_VN.md
reports/REFERENCES_25_SELECTION_AUDIT.md
reports/RELATED_PAPERS_25_SELECTED.bib
reports/APPLIED_RESEARCH_RESTRUCTURE_REPORT.md
```

Neu co the build Overleaf/PDF:

```text
reports/springer_overleaf/main_applied_research.tex
reports/springer_overleaf/main_applied_research.pdf
```

Bao cao cuoi cung cho nguoi dung can noi ro:

- Da tao/sua file nao.
- Cau truc bai moi gom nhung muc nao.
- References hien co bao nhieu nguon duoc giu/chon.
- Them duoc bao nhieu nguon moi va nguon do thuoc nhom nao.
- Con thieu gi de nop hoi thao Springer.

