# Springer New Dataset Final Checklist

## Format và độ dài

- [x] Dùng Springer LNCS `llncs.cls`.
- [x] Tác giả là Ly-Cu DUONG và Van-Phuc VO.
- [x] PDF có 11 trang, không vượt quá 13 trang.
- [x] Không chỉnh font hoặc margin để ép trang.
- [x] Abstract 199 từ, dưới 250 từ.
- [x] Có 5 keywords.
- [x] Chỉ có sáu section lớn theo hướng Applied Research.

## Dataset và protocol

- [x] Development là P01-P05, 94 video, 12,680 frame.
- [x] External là P06-P07, 23 video, 4,556 frame.
- [x] Correct/Incorrect lần lượt là 5,206/7,474 ở development.
- [x] Correct/Incorrect lần lượt là 2,001/2,555 ở external.
- [x] Participant overlap bằng rỗng.
- [x] Source-video overlap bằng rỗng.
- [x] Nhãn được mô tả là project-specific.
- [x] Không claim expert ergonomic annotation.

## Model và kết quả

- [x] Benchmark mặc định có đủ 9 phương pháp.
- [x] Bảng benchmark chung chỉ dùng threshold 0.50.
- [x] HGB mặc định đạt Accuracy 87.34% và F1 89.01%.
- [x] HGB selected dùng `ergonomic_v2_with_view`, 31 feature.
- [x] HGB selected dùng threshold 0.76.
- [x] Selected metrics là Accuracy 89.31%, Precision 93.48%, Recall 87.01%, F1 90.13%, MCC 0.7875.
- [x] Confusion matrix là TN=1,846, FP=155, FN=332, TP=2,223.
- [x] ANN được mô tả là neural baseline/application model ban đầu.
- [x] Rule-based Recall 100% được giải thích cùng FP=2,001 và MCC=0.
- [x] Có participant-wise P06/P07.
- [x] Runtime HGB là 25.27-25.80 FPS.
- [x] Runtime được gọi là processing benchmark, không phải full GUI FPS.

## Claim và hạn chế

- [x] Không claim state-of-the-art.
- [x] Không claim mô hình pose estimation mới.
- [x] Không so sánh trực tiếp như leaderboard với nghiên cứu khác.
- [x] Ghi rõ threshold 0.76 được chọn trên P06-P07.
- [x] Không gọi kết quả calibrated là blind external test.
- [x] Có limitation về participant, nhãn, public benchmark, GUI FPS và ethics.
- [x] Conclusion không có citation và không thêm kết quả mới.

## Hình, bảng và references

- [x] Có 4 figure environment.
- [x] Có 5 bảng.
- [x] Hình mới dùng tiếng Anh.
- [x] Hình metric được tạo từ CSV kết quả mới.
- [x] Không dùng confusion matrix cũ.
- [x] Không có `[Insert Fig...]`.
- [x] Không có `This information should be completed before submission`.
- [x] Không có Algorithm 1.
- [x] Có 25 references.
- [x] Tất cả 25 references đều được nhắc trong nội dung.
- [x] Không thêm DOI hoặc tài liệu mới không được kiểm chứng.

## Kiểm tra build

- [x] Tectonic build thành công.
- [x] Không có missing reference hoặc undefined cross-reference.
- [x] Không có overfull box.
- [x] Đã render và kiểm tra trực quan toàn bộ 11 trang.
- [x] Không có hình/bảng bị cắt hoặc tràn lề.
- [x] Bản cũ không bị xóa hoặc ghi đè.
