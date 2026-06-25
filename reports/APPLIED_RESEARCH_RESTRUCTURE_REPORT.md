# APPLIED_RESEARCH_RESTRUCTURE_REPORT

Ngày tạo: 2026-06-03

Task thực thi:

```text
workflow_kilo/19_TASK_RUT_GON_CAU_TRUC_APPLIED_RESEARCH_VA_BO_SUNG_REFERENCES.md
```

## 1. File đã tạo

| File | Vai trò |
|---|---|
| `reports/SPRINGER_MANUSCRIPT_APPLIED_RESEARCH_RESTRUCTURED.md` | Bản thảo tiếng Anh đã rút gọn theo hướng Applied Research. |
| `reports/SPRINGER_MANUSCRIPT_APPLIED_RESEARCH_RESTRUCTURED_VN.md` | Bản tiếng Việt đối chiếu cùng cấu trúc 6 mục. |
| `reports/REFERENCES_25_SELECTION_AUDIT.md` | Audit 25 references chính và các nguồn nên loại/chỉ tham khảo kỹ thuật. |
| `reports/RELATED_PAPERS_25_SELECTED.bib` | BibTeX chọn lọc 25 nguồn dùng cho Overleaf hoặc chuyển citation style. |
| `reports/APPLIED_RESEARCH_RESTRUCTURE_REPORT.md` | Báo cáo tự kiểm tra task này. |

Không ghi đè các file cũ như `SPRINGER_MANUSCRIPT_REVISED.md`, `SPRINGER_MANUSCRIPT_FINAL_DRAFT.md` hoặc `reports/springer_overleaf/main_revised.tex`.

## 2. Cấu trúc bài mới

Bài đã được rút còn 6 mục lớn đúng hướng Applied Research:

```text
1. Introduction
2. Related Work
3. Proposed Webcam-Based Posture Monitoring System
4. Experimental Protocol
5. Evaluation and Discussion
6. Conclusion and Future Work
```

Các nội dung cũ được gộp lại như sau:

| Nội dung cũ | Được đưa vào mục mới |
|---|---|
| Proposed Method | Mục 3 |
| Dataset and Feature Extraction | Mục 4 |
| Experimental Setup | Mục 4 |
| Results and Discussion | Mục 5 |
| Desktop Application Implementation | Mục 3 và Mục 5 |
| Limitations | Cuối Mục 5 |
| Conclusion and Future Work | Mục 6 |

## 3. References đã xử lý

Tổng references chính được chọn: **25 nguồn**.

Nhóm nguồn:

| Nhóm | Số nguồn | Ghi chú |
|---|---:|---|
| Human pose estimation / MediaPipe / OpenPose | 5 | BlazePose, MediaPipe, OpenPose, MediaPipe Pose, Google AI Edge docs. |
| Sitting/working posture recognition | 7 | Chen, Estrada, Kulikajevas, Chaikhamwang, Carneros-Prado, Tlili, Zeng. |
| Sensor/pressure/depth baseline | 6 | Luna-Perejon, Bourahmoune, Tsai, Feradov, Wang, Odesola. |
| Review/tổng quan | 4 | Nadeem, Krauter, Roggio, Jiang. |
| Ergonomic foundation | 2 | RULA và REBA. |
| Dataset/benchmark | 1 | MultiPosture Zenodo. |

Nguồn được bổ sung hoặc nhấn mạnh thêm so với bản đang dùng:

- McAtamney & Corlett (1993) - RULA.
- Hignett & McAtamney (2000) - REBA.
- Luna-Perejon et al. (2021) - IoT device + ANN.
- Chaikhamwang et al. (2025) - MediaPipe/computer vision office syndrome platform.
- Tlili et al. (2022) - ML algorithms for sitting posture monitoring.

Nguồn không đưa vào references chính:

- Google Research Blog về BlazePose.
- LearnOpenCV tutorial.
- Roboflow dataset links.
- Hugging Face dataset link.
- LSP-YOLO vì lệch hướng YOLO.
- SitLLM vì lệch hướng pressure sensor + LLM.

## 4. Checklist tự kiểm tra

| Câu hỏi | Kết quả |
|---|---|
| 1. Bài đã rút gọn còn 6 mục lớn chưa? | Có. |
| 2. Các tiêu đề mục có đúng hướng Applied Research không? | Có. Mục 3 dùng `Proposed Webcam-Based Posture Monitoring System`, không dùng tiêu đề mơ hồ như `Our`. |
| 3. Abstract có dưới 250 từ không? | Có, kiểm tra nhanh được 198 từ. |
| 4. Keywords có 3-5 từ khóa không? | Có, 5 keywords. |
| 5. Related Work có chốt research gap không? | Có. Đoạn cuối nêu rõ gap webcam-only desktop pipeline + features + baseline + classifiers + runtime + logging. |
| 6. Proposed System có pipeline không? | Có. Mục 3 giữ pipeline text và mô tả real-time loop ở mức module; đã bỏ pseudocode Algorithm 1 để bài gọn và giống paper hơn. |
| 7. Dataset có trình bày theo split thay vì chỉ theo tên file không? | Có. Table 1 theo Development/training set, Corrected external set, Full video manifest. |
| 8. Experiment có phân biệt ANN app model và HGB selected experimental model không? | Có. Bài nói ANN/Keras là application model, HGB là selected experimental model; app demo hiện có thêm lựa chọn HGB. |
| 9. Evaluation có dùng số liệu thật từ project không? | Có. Số liệu lấy từ `FINAL_EVALUATION_REPORT.md`, `MODEL_SELECTION_REPORT.md`, `RUNTIME_BENCHMARK.md`. |
| 10. Có còn citation/DOI/dataset nào chưa xác minh không? | Có một số nguồn cần xem full paper trước nộp chính thức, đặc biệt Chaikhamwang et al. (2025). Không có DOI tự bịa. |
| 11. Tổng references chọn lọc là bao nhiêu? | 25. |
| 12. Có nguồn blog/tutorial nào bị dùng như paper học thuật không? | Không. Blog/tutorial được đưa vào nhóm loại hoặc chỉ tham khảo kỹ thuật. |
| 13. Có claim vượt trội tổng quát hoặc model mới không? | Không. Bài ghi rõ không đề xuất pose estimator/model mới và không khẳng định vượt trội tổng quát so với các nghiên cứu trước. |
| 14. Conclusion có citation không? | Không. |
| 15. Các hạn chế học thuật có được nêu trung thực không? | Có. Nêu 5 participants, external set only P01, labels project-specific, no expert annotation, no public benchmark, calibrated external protocol, no full GUI FPS. |

## 5. Điểm còn rủi ro học thuật

1. **External set còn hẹp**: corrected external set chỉ có P01, nên chưa đủ mạnh để claim tổng quát hóa cho nhiều người dùng.
2. **Threshold calibration**: threshold 0.65 gắn với corrected external protocol, nên kết quả 96.50% nên viết là calibrated corrected-external performance, không phải independent hold-out.
3. **Nhãn chưa có chuyên gia ergonomic**: Correct/Incorrect là nhãn project-specific, chưa có RULA/REBA hoặc chuyên gia xác nhận.
4. **Public benchmark chưa chạy**: MultiPosture đã được đưa vào references/future work, nhưng project chưa benchmark thật trên dataset này.
5. **Full GUI FPS chưa đo**: hiện chỉ có processing FPS, chưa đo toàn bộ app gồm Tkinter, render, audio, camera buffering và SQLite logging.
6. **Một số nguồn mới cần đọc full text trước submission**: đặc biệt nguồn gần đây hoặc không phải venue mạnh như IJACSA.

## 6. Hướng xử lý tiếp theo trước khi nộp Springer

Ưu tiên cao:

1. Chuyển bản Markdown mới sang LaTeX/Overleaf nếu muốn thay thế `main_revised.tex`.
2. Đảm bảo citation style đồng nhất theo yêu cầu hội thảo: author-year hoặc numeric.
3. Xuất hình thật cho Fig. 1-6 nếu bản PDF cần nộp ngay.
4. Ghi rõ phần hardware thực nghiệm nếu có thể: CPU, RAM, GPU, webcam.
5. Nếu còn thời gian, tách một validation set riêng để chọn threshold, rồi dùng corrected external set chỉ để report final.

Ưu tiên trung bình:

1. Chạy public benchmark MultiPosture sau khi kiểm tra license và mapping nhãn.
2. Bổ sung annotation chuyên gia hoặc mapping RULA/REBA ở mức pilot.
3. Đo full GUI FPS bằng app thật.

Không nên làm ngay nếu gấp:

1. Đổi hướng sang YOLO/CNN/end-to-end deep learning.
2. Thêm quá nhiều references không liên quan chỉ để tăng số lượng.
3. Claim vượt nghiên cứu khác nếu không cùng dataset/protocol.
