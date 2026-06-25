# SPRINGER CRITICAL FIX TODO FOR CODEX

File cần sửa chính: `main.tex` / source tạo `main.pdf`  
File PDF hiện tại đã kiểm tra: `main.pdf`  
Mục tiêu: chỉnh bản thảo thành bài báo khoa học Springer chắc hơn, giảm rủi ro bị bắt lỗi về thực nghiệm, dataset, bảng/hình, references và tính tái lập.

---

## 0. Nguyên tắc sửa

- Không viết lại toàn bộ bài nếu không cần.
- Không bịa số liệu, DOI, dataset, hardware, threshold, protocol.
- Không đổi hướng project sang web/mobile/YOLO/CNN.
- Không claim state-of-the-art.
- Không sửa code nguồn nếu không được yêu cầu.
- Nếu thiếu thông tin trong project, ghi vào `SPRINGER_CRITICAL_FIX_REPORT.md` thay vì tự điền.
- Giữ hướng nghiên cứu: **existing model + new dataset/features + webcam desktop application**.
- Giữ cách viết trung lập, ngắn, có số liệu, không dùng văn phong quảng cáo.

---

# 1. Lỗi cần sửa mức CAO

## 1.1. Làm rõ threshold calibration có dùng external set hay không

### Vấn đề hiện tại

Trong bài đang viết:

- Corrected external set không dùng để train và được dùng cho main external evaluation.
- Sau đó lại nói threshold calibration chọn threshold 0.65 cho final protocol.
- Nếu threshold 0.65 được chọn bằng chính corrected external set, thì corrected external set không còn là independent hold-out test hoàn toàn.

### Việc Codex cần làm

Tìm trong project các file liên quan:

- `MODEL_SELECTION_REPORT.md`
- `FINAL_EVALUATION_REPORT.md`
- `EXPERIMENT_PROTOCOL_FINAL.md`
- các script evaluation/model registry nếu cần:
  - `23_final_evaluation_protocol.py`
  - `21_train_model_registry.py`
  - các file threshold sweep/calibration nếu có.

Xác định rõ:

1. Threshold 0.65 được chọn trên tập nào?
2. Corrected external set có được dùng để chọn threshold không?
3. Final selected model có được đánh giá trên đúng tập đã dùng để calibration không?

### Cách sửa trong bài

Nếu threshold được chọn trên development/validation set, sửa thành:

> The decision threshold was calibrated on the development validation split. The corrected external set was not used for model training or threshold selection and was used only for final reporting.

Nếu threshold được chọn trên corrected external set, sửa thành:

> The threshold was calibrated on the corrected external set. Therefore, the reported result should be interpreted as calibrated external performance rather than a strictly independent hold-out test.

Nếu không tìm thấy thông tin, sửa thành:

> The project artifacts do not clearly specify whether threshold calibration was performed on the development set or on the corrected external set. Therefore, the selected threshold result is reported as a calibrated protocol result, and a strictly independent threshold-selection protocol should be added before formal submission.

Đồng thời ghi rõ trong `SPRINGER_CRITICAL_FIX_REPORT.md`.

---

## 1.2. Làm rõ labeling protocol

### Vấn đề hiện tại

Bài hiện chỉ nói labels được gán ở video/sample generation stage theo source posture class. Cách viết này trung thực nhưng chưa đủ để reviewer hiểu ground truth.

### Việc Codex cần làm

Tìm trong project:

- folder dataset/raw_videos nếu có;
- `video_manifest.csv`;
- scripts extract features;
- các README/dataset notes;
- tên thư mục/video có `correct`, `incorrect`, `slouch`, `forward`, `side`, v.v.;
- file external correction nếu có.

Xác định và viết rõ:

1. Correct posture được định nghĩa/gán như thế nào?
2. Incorrect posture gồm các lỗi nào?
3. Nhãn được gán theo video, segment hay frame?
4. Ai gán nhãn hoặc gán nhãn dựa theo quy tắc nào?
5. External corrected set được “corrected” như thế nào?
6. Có expert ergonomic annotation không? Nếu không, giữ limitation rõ ràng.

### Đoạn nên thêm vào Section 4 Dataset and Feature Extraction

Chỉ dùng nếu đúng với project:

> Correct videos were recorded when participants were instructed to maintain the intended upright working posture. Incorrect videos were recorded when participants intentionally performed visible working-posture errors such as forward head position, shoulder imbalance, torso leaning, neck compression, chin resting, or hand-to-mouth support. Labels were assigned at the video or segment level and then inherited by sampled frames during feature extraction. The corrected external set was manually checked at the project level to reduce label noise. No independent ergonomic expert annotation or inter-rater agreement was available.

Nếu project không có thông tin về external correction, bỏ câu đó và ghi vào report.

---

## 1.3. Bổ sung bảng rule-based baseline threshold

### Vấn đề hiện tại

Rule-based baseline được mô tả là dùng manually defined geometric thresholds, nhưng bài chưa có bảng threshold hoặc điều kiện cụ thể. Điều này làm baseline khó tái lập.

### Việc Codex cần làm

Đọc code rule-based, ưu tiên:

- `posture_baseline.py`
- `1_rule_based_baseline.py`
- `8_compare_algorithms.py`
- các config threshold trong app nếu có.

Trích đúng:

- feature/rule name;
- condition;
- threshold;
- meaning.

### Bảng cần thêm vào Proposed Method hoặc Appendix nếu bài quá dài

Tạo bảng dạng:

| Rule indicator | Condition | Threshold | Interpretation |
|---|---|---:|---|
| Shoulder tilt | ... | ... | Shoulder imbalance |
| Torso lean | ... | ... | Leaning posture |
| Head offset | ... | ... | Head displacement |
| Neck compression | ... | ... | Neck compression cue |
| Hand-mouth ratio | ... | ... | Chin/hand support cue |

Nếu không tìm thấy threshold trong code:

- không bịa;
- ghi rõ trong report: “Rule thresholds are described in code but not fully recoverable from available artifacts” hoặc “threshold values not found”.
- trong paper chỉ viết baseline logic, không đưa bảng threshold giả.

---

## 1.4. Bổ sung bảng định nghĩa ergonomic/geometric features

### Vấn đề hiện tại

Bài có liệt kê ergonomic features nhưng chưa định nghĩa đủ để người đọc tái lập. Ít nhất cần giải thích feature lấy từ landmark nào và ý nghĩa gì.

### Việc Codex cần làm

Đọc:

- `FEATURE_SCHEMA_FINAL.md`
- feature extraction scripts;
- final feature schema CSV/report.

Thêm bảng:

| Feature | Definition | Main landmarks | Purpose |
|---|---|---|---|
| `shoulder_width` | distance between left and right shoulders | left shoulder, right shoulder | body scale |
| `shoulder_tilt_angle` | angle of shoulder line | left shoulder, right shoulder | shoulder imbalance |
| `torso_lean_angle` | angle between shoulder midpoint and hip midpoint | shoulders, hips | torso leaning |
| `head_offset_x` | horizontal offset of nose from shoulder midpoint | nose, shoulders | head displacement |
| `nose_shoulder_clearance_ratio` | ... | nose, shoulders | neck/head relation |
| `neck_compression_detected` | binary indicator from head/shoulder relation | nose, shoulders | neck compression cue |
| `min_hand_mouth_ratio` | minimum normalized hand-mouth distance | wrists, mouth landmarks | hand/chin support |

Không bịa công thức nếu không có. Nếu có công thức trong code, trích đúng.

---

## 1.5. Thêm thông tin hardware cho runtime benchmark

### Vấn đề hiện tại

Bài hiện nói hardware details are not recorded. Nhưng runtime FPS là kết quả quan trọng, thiếu hardware làm kết quả yếu.

### Việc Codex cần làm

Tìm trong project hoặc OS notes:

- CPU;
- RAM;
- GPU nếu có;
- OS;
- camera/video resolution;
- input frame size;
- model complexity của MediaPipe nếu có;
- runtime command/script.

Nếu không có thông tin, giữ limitation nhưng tạo TODO rõ ràng.

### Cách sửa

Nếu tìm được thông tin, thêm vào Experimental Setup:

> Runtime tests were performed on [CPU], [RAM], [OS], using [input resolution]. No dedicated GPU was used for inference.

Nếu không tìm được, giữ câu hiện tại nhưng thêm trong Limitations:

> Hardware information was not recorded in the current artifacts; therefore, FPS values should be interpreted as project-level measurements rather than hardware-normalized benchmarks.

---

# 2. Lỗi cần sửa mức TRUNG BÌNH

## 2.1. Sửa Table 1 không trộn video-level và frame-level

### Vấn đề hiện tại

Table 1 có dòng `Full video manifest`, trong khi bảng đang nói dataset splits. Dòng này trộn video-level với frame-level.

### Sửa đề xuất

Table 1 chỉ giữ:

| Split | Videos | Participants | Samples | Correct | Incorrect |
|---|---:|---:|---:|---:|---:|
| Development/training set | 84 | 5 | 11,022 | 4,438 (40.26%) | 6,584 (59.74%) |
| Corrected external set | 10 | 1 | 1,658 | 768 (46.32%) | 890 (53.68%) |

Sau bảng, thêm câu:

> The full video manifest contains 94 videos, including 84 development videos and 10 corrected external videos. At the video level, 39 videos are labeled Correct and 55 videos are labeled Incorrect.

---

## 2.2. Sửa header Table 3, Table 4, Table 5 cho rõ positive class

### Vấn đề hiện tại

Trong PDF, các bảng dùng `Precision`, `Recall`, `F1` nhưng không luôn ghi rõ đây là class Incorrect. Dù text có giải thích positive class, bảng nên tự rõ nghĩa.

### Việc cần sửa

Đổi header:

- `Precision` -> `Precision Inc.`
- `Recall` -> `Recall Inc.`
- `F1` -> `F1 Inc.`

Hoặc nếu đủ chỗ:

- `Precision Incorrect`
- `Recall Incorrect`
- `F1 Incorrect`

---

## 2.3. Thêm MCC vào Table 4 nếu có dữ liệu

### Vấn đề hiện tại

Model selection dùng MCC làm tie-breaker, nhưng Table 4 trong PDF không có MCC.

### Việc cần sửa

Nếu dữ liệu MCC có trong model registry, thêm MCC vào Table 4.

Nếu bảng quá rộng, rút gọn Table 4 thành:

| Rank | Model | Feature group | Accuracy | Recall Inc. | F1 Inc. | MCC |
|---:|---|---|---:|---:|---:|---:|

---

## 2.4. Thêm FP và FN vào Table 5

### Vấn đề hiện tại

Text nói final selected model có 34 false positives và 24 false negatives, nhưng Table 5 chưa có FP/FN.

### Việc cần sửa

Thêm hai cột:

| FP | FN |
|---:|---:|
| 34 | 24 |

---

## 2.5. Bổ sung GUI screenshot trong Implementation

### Vấn đề hiện tại

Bài có phần Desktop Application Implementation nhưng chưa có screenshot GUI thật. Hiện có logging flow nhưng chưa có hình app.

### Việc cần làm

Nếu project có ảnh GUI:

- thêm hình:
  - `Fig. X. Desktop application interface showing webcam input, MediaPipe overlay, posture prediction, and warning status.`
- đặt trong Section 7.

Nếu chưa có:

- tạo TODO trong report:
  - chạy app;
  - chụp màn hình webcam/video test;
  - che thông tin riêng tư nếu có;
  - export PNG độ phân giải tốt.

Không bịa hình.

---

## 2.6. Kiểm tra Fig. 5 temporal smoothing

### Vấn đề hiện tại

Fig. 5 cần thể hiện rõ temporal smoothing. Nếu hình không có raw probability, smoothed probability, threshold hoặc warning event, nó chưa đủ thuyết phục.

### Việc cần làm

Kiểm tra figure file. Nếu có thể, tạo lại hình gồm:

- raw prediction/probability;
- smoothed probability;
- decision threshold;
- warning region/event.

Caption đề xuất:

> Fig. X. Temporal smoothing example showing raw prediction scores, smoothed scores, decision threshold, and warning region.

---

# 3. Lỗi cần sửa mức THẤP nhưng nên làm

## 3.1. Bổ sung 3–5 references để đủ khoảng 20–30 nguồn

### Vấn đề hiện tại

Bài hiện có 18 references. Nên tăng lên khoảng 22–24 nếu có nguồn chất lượng.

### Nguồn nên bổ sung nếu đã có trong project

Ưu tiên:

1. ergonomic/workplace health hoặc musculoskeletal disorders;
2. RULA gốc nếu nhắc RULA;
3. REBA gốc nếu nhắc REBA;
4. Google AI Edge / MediaPipe Pose official documentation nếu cần mô tả implementation;
5. thêm 1 public benchmark/dataset liên quan nếu phù hợp.

Không thêm nguồn không dùng trong thân bài. Không bịa DOI.

---

## 3.2. Sửa capitalization trong References

### Vấn đề hiện tại

Một số tên riêng bị lowercase do BibTeX:

- Blazepose -> BlazePose
- Openpose -> OpenPose
- Mediapipe -> MediaPipe
- iot -> IoT
- covid-19 -> COVID-19
- kolmogorov-arnold -> Kolmogorov-Arnold

### Việc cần làm

Sửa BibTeX title bằng `{}`:

```bibtex
title = {{BlazePose}: On-device real-time body pose tracking}
title = {{OpenPose}: Realtime multi-person 2D pose estimation using part affinity fields}
title = {{MediaPipe}: A framework for building perception pipelines}
title = {An {IoT} device for sitting posture classification using artificial neural networks}
title = { ... during {COVID-19}}
title = {A comparison between multilayer perceptrons and {Kolmogorov-Arnold} networks ...}
```

---

## 3.3. Kiểm tra lại reference Sahoo et al. 2026

### Vấn đề hiện tại

Reference Sahoo et al. 2026 có năm 2026. Cần xác minh DOI và trạng thái published.

### Việc cần làm

- Kiểm DOI `10.3390/a19010048` trong project/references.
- Nếu không chắc, đưa vào report.
- Nếu không cần thiết cho argument chính, có thể loại khỏi References để giảm rủi ro.

---

## 3.4. Thêm Data/Code/Ethics note nếu venue cho phép

### Lý do

Dataset có video người thật. Bài nên có một đoạn ngắn về quyền riêng tư và khả năng chia sẻ dữ liệu.

### Đoạn đề xuất

> The raw videos are not planned for public release because they may contain identifiable participants. Extracted landmark features can be shared after anonymization if required by the venue and if participant consent permits. The collected data were used only for academic evaluation in this project.

Nếu chưa có consent, không claim đã có consent.

---

# 4. Các điểm KHÔNG nên sửa quá tay

- Không biến bài thành luận văn bằng cách thêm quá nhiều mô tả GUI.
- Không thêm quá nhiều references chỉ để đủ số lượng.
- Không claim model HGB đang chạy trong app nếu app hiện dùng ANN.
- Không so sánh trực tiếp với các paper khác như leaderboard.
- Không mở rộng sang multi-class posture nếu dataset chưa có nhãn.
- Không thêm RULA/REBA vào phương pháp chính nếu chưa thật sự dùng; chỉ để future work hoặc background.

---

# 5. Checklist sau khi sửa

Codex phải kiểm tra lại:

- [ ] Threshold calibration đã rõ dùng tập nào.
- [ ] Nếu threshold dùng external set, đã ghi rõ calibrated external performance.
- [ ] Labeling protocol rõ hơn.
- [ ] Table 1 không trộn video-level và frame-level.
- [ ] Rule-based baseline có threshold table hoặc report ghi rõ không tìm thấy threshold.
- [ ] Ergonomic features có definition table.
- [ ] Hardware runtime có hoặc limitation rõ.
- [ ] Table 3/4/5 header ghi rõ Incorrect class.
- [ ] Table 4 có MCC nếu dùng MCC làm tie-breaker.
- [ ] Table 5 có FP/FN.
- [ ] Có GUI screenshot hoặc TODO rõ.
- [ ] References capitalization đúng.
- [ ] References khoảng 20–30 nếu có nguồn chất lượng.
- [ ] Không bịa DOI.
- [ ] Không claim state-of-the-art.
- [ ] Không có câu giống quảng cáo sản phẩm.
- [ ] Không có thông tin “should be completed before submission”.
- [ ] Không có placeholder hình chưa xử lý trong bản nộp.

---

# 6. Output yêu cầu

Sau khi sửa, tạo các file:

1. `main_revised.pdf`
2. `main_revised.tex` hoặc source tương ứng nếu có
3. `SPRINGER_CRITICAL_FIX_REPORT.md`

Trong `SPRINGER_CRITICAL_FIX_REPORT.md`, ghi bảng:

| Issue | Fixed? | Location | What changed | Remaining risk |
|---|---|---|---|---|

Nếu thông tin không tìm thấy trong project, ghi rõ:

> Not fixed because the required information was not found in the current project artifacts. No value was invented.

