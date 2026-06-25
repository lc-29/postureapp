# THAYKHOI_INSERTION_PATCH

File này chỉ là patch gợi ý. Không tự động sửa LaTeX/PDF ở bước này.

## 1. Citation đề xuất

- In-text citation: `(Khiem et al., 2026)`
- Mức liên quan: liên quan gián tiếp, dùng để nói về health-oriented visual AI, không phải posture detection trực tiếp.

## 2. Câu chèn đề xuất trong `main_applied_research_final_formatfix.tex`

### Vị trí

Section `Introduction`, sau câu/đoạn:

```tex
Previous posture monitoring studies have used pressure sensors, force sensors, motion-capture devices, smart chairs, RGB-D cameras, and RGB camera systems.
```

### Câu thêm

```tex
Image-based health AI has also been studied in clinical imaging tasks such as X-ray-based lung disease diagnosis (Khiem et al., 2026); however, the present work differs by using webcam-derived pose landmarks for non-clinical working posture monitoring and real-time feedback.
```

### Lưu ý

- Không chèn câu này vào Conclusion.
- Không dùng câu này để claim rằng bài X-ray là nền tảng trực tiếp của posture detection.
- Nếu muốn Related Work thật tập trung, có thể không chèn citation này.

## 3. Reference APA 7 cần thêm

```text
Khiem, N. M., Quyen, P. N., Quang, T. D., & Anh-Khoi, N. H. (2026). Leveraging deep learning for lung disease diagnosis and classification through X-ray imaging. In N. Goyal, T. N. Nguyen, M. Lata, & G. A. Ogunmola (Eds.), Proceedings of the International Conference on Sustainable Computing. ICSC 2025. Lecture Notes in Electrical Engineering (Vol. 1530). Springer. https://doi.org/10.1007/978-981-95-6063-9_16
```

## 4. Nếu dùng BibTeX

```bibtex
@incollection{khiem2026lung_xray,
  author    = {Khiem, N. M. and Quyen, P. N. and Quang, T. D. and Anh-Khoi, N. H.},
  title     = {Leveraging Deep Learning for Lung Disease Diagnosis and Classification Through X-ray Imaging},
  booktitle = {Proceedings of the International Conference on Sustainable Computing. ICSC 2025},
  series    = {Lecture Notes in Electrical Engineering},
  volume    = {1530},
  publisher = {Springer},
  year      = {2026},
  doi       = {10.1007/978-981-95-6063-9_16},
  url       = {https://doi.org/10.1007/978-981-95-6063-9_16}
}
```
