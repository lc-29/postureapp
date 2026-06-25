from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from docx import Document


ROOT = Path(__file__).resolve().parents[1]
DOCX_PATH = Path(r"D:\LUẬN VĂN 2026\CA_NHAN\BAOCAOKHOAHOC\DANHSACHTAILIEUTHAMKHAOTHAYKHOI.docx")
MAIN_TEX = ROOT / "reports" / "springer_overleaf" / "main_applied_research_final_formatfix.tex"
OUT_ANALYSIS = ROOT / "reports" / "THAYKHOI_RELATED_PAPERS_ANALYSIS.md"
OUT_PATCH = ROOT / "reports" / "THAYKHOI_INSERTION_PATCH.md"


@dataclass
class Paper:
    stt: int
    citation: str
    categories: list[str]
    authors: str
    year: str
    title: str
    source: str
    doi_url: str
    topic: str
    relevance: str
    reason: str


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def extract_entries() -> tuple[list[str], list[tuple[str, str]], list[Paper]]:
    doc = Document(str(DOCX_PATH))
    categories: list[str] = []
    raw_entries: list[tuple[str, str]] = []
    current_category = ""

    for paragraph in doc.paragraphs:
        text = normalize(paragraph.text)
        if not text or text == "NGO HO ANH KHOI’S PAPERS BY FIELDS":
            continue
        if not re.search(r"\(\d{4}", text) and text.upper() == text:
            current_category = text
            categories.append(text)
            continue
        if re.search(r"\(\d{4}", text):
            raw_entries.append((current_category, text))

    grouped: dict[str, dict] = {}
    for category, entry in raw_entries:
        key = normalize(entry.lower())
        grouped.setdefault(key, {"entry": entry, "categories": []})
        if category and category not in grouped[key]["categories"]:
            grouped[key]["categories"].append(category)

    papers: list[Paper] = []
    for idx, item in enumerate(grouped.values(), 1):
        entry = item["entry"]
        categories_for_entry = item["categories"]
        authors, year, title, source, doi_url = parse_citation(entry)
        topic, relevance, reason = classify(entry, categories_for_entry, title)
        papers.append(
            Paper(
                stt=idx,
                citation=entry,
                categories=categories_for_entry,
                authors=authors,
                year=year,
                title=title,
                source=source,
                doi_url=doi_url,
                topic=topic,
                relevance=relevance,
                reason=reason,
            )
        )
    return categories, raw_entries, papers


def parse_citation(entry: str) -> tuple[str, str, str, str, str]:
    year_match = re.search(r"\((\d{4})(?:[^\)]*)\)", entry)
    year = year_match.group(1) if year_match else "Không rõ"
    authors = entry[: year_match.start()].strip().rstrip(",") if year_match else entry.split(".")[0]
    rest = entry[year_match.end() :].strip(" .") if year_match else entry

    quoted = re.search(r'"([^"]+)"', entry)
    if quoted:
        title = quoted.group(1).strip()
        source = normalize(entry[quoted.end() :].strip(" ,.;"))
    else:
        # Most entries follow APA-like "Authors. (Year). Title. Source."
        parts = re.split(r"\.\s+", rest, maxsplit=1)
        title = parts[0].strip(" .")
        source = parts[1].strip() if len(parts) > 1 else ""

    doi_url = ""
    doi_match = re.search(r"https?://\S+", entry)
    if doi_match:
        doi_url = doi_match.group(0).rstrip(".,;")
    else:
        doi_match = re.search(r"\bdoi:\s*(10\.\S+)", entry, flags=re.I)
        if doi_match:
            doi_url = "https://doi.org/" + doi_match.group(1).rstrip(".,;")
    if not doi_url:
        raw_doi = re.search(r"\b10\.\d{4,9}/\S+", entry)
        if raw_doi:
            doi_url = "https://doi.org/" + raw_doi.group(0).rstrip(".,;")

    return authors, year, title, source, doi_url or "Không thấy DOI/link trong file Word"


def classify(entry: str, categories: list[str], title: str) -> tuple[str, str, str]:
    blob = " ".join([entry, title, " ".join(categories)]).lower()
    if "lung disease" in blob and "x-ray" in blob:
        return (
            "Computer vision/deep learning trong health/medical imaging",
            "Liên quan gián tiếp",
            "Có cùng hướng AI thị giác và sức khỏe, nhưng khác dữ liệu X-ray và không liên quan trực tiếp đến webcam pose landmarks/posture.",
        )
    if "3d space reconstruction" in blob or "gaussian splatting" in blob:
        return (
            "Video-based computer vision/3D reconstruction",
            "Liên quan gián tiếp",
            "Có liên quan đến video/computer vision, nhưng khác mục tiêu vì không xử lý human pose, posture hay health monitoring.",
        )
    if "multi one-class" in blob or "incremental svm" in blob or "continuous learning" in blob or "evolving learning" in blob or "eki" in blob:
        if "glass" in blob or "artifact" in blob or "document" in blob or "digitization" in blob:
            return (
                "Continuous/adaptive machine learning hoặc image/document classification",
                "Ít liên quan",
                "Có nền machine learning/adaptation hoặc nhận dạng ảnh/tài liệu, nhưng miền bài toán xa posture detection.",
            )
    if "stress" in blob:
        return (
            "Health monitoring bằng machine learning trên dữ liệu tabular",
            "Liên quan gián tiếp",
            "Có liên quan sức khỏe và đánh giá theo dữ liệu, nhưng không có computer vision, webcam hoặc posture.",
        )
    if "robot" in blob or "human–robot" in blob or "human-robot" in blob:
        return (
            "Robotics/HCI hoặc realtime interaction",
            "Ít liên quan",
            "Có yếu tố hệ thống tương tác thời gian thực, nhưng tập trung speech/RAG, không phải visual posture monitoring.",
        )
    if "water quality" in blob or "wine" in blob or "mushroom" in blob or "botanical" in blob:
        return (
            "Applied ML trong science/food/environment",
            "Ít liên quan",
            "Có dùng ML ứng dụng, nhưng không liên quan trực tiếp đến computer vision posture hoặc health monitoring bằng webcam.",
        )
    if "gemstone" in blob or "jewelry" in blob:
        return (
            "Image/hardware identification trong gemmology/archeology",
            "Ít liên quan",
            "Có thể có yếu tố nhận dạng ảnh/phần cứng, nhưng miền ứng dụng quá xa tư thế làm việc.",
        )
    if any(term in blob for term in ["chatbot", "word alignment", "llm", "question/answers", "economy"]):
        return (
            "NLP/chatbot/economy",
            "Không nên thêm",
            "Không liên quan đến computer vision, pose estimation, health monitoring hoặc posture detection.",
        )
    if any(term in blob for term in ["malware", "ddos", "blockchain", "security"]):
        return (
            "Security/network",
            "Không nên thêm",
            "Chủ đề bảo mật/mạng không hỗ trợ luận điểm posture detection.",
        )
    if "hotel" in blob or "tourism" in blob or "customer churn" in blob or "brand reputation" in blob or "student dropout" in blob:
        return (
            "Economy/education/tabular prediction",
            "Không nên thêm",
            "Bài toán dự đoán tabular/kinh tế/giáo dục không liên quan trực tiếp đến webcam posture detection.",
        )
    return (
        "Machine learning chung",
        "Ít liên quan",
        "Có liên quan rất rộng đến machine learning, nhưng chưa đủ gần để đưa vào Related Work chính.",
    )


def md_table_row(values: list[str]) -> str:
    return "| " + " | ".join(v.replace("|", "/").replace("\n", " ").strip() for v in values) + " |"


def find_context_snippets() -> dict[str, str]:
    tex = MAIN_TEX.read_text(encoding="utf-8") if MAIN_TEX.exists() else ""
    snippets = {}
    anchors = {
        "introduction_gap": "RGB camera and pose-estimation approaches reduce this hardware barrier",
        "related_rgb": r"\paragraph{RGB camera and pose-landmark-based posture recognition.}",
        "related_reviews": r"\paragraph{Reviews, datasets, and ergonomic context.}",
    }
    for name, anchor in anchors.items():
        idx = tex.find(anchor)
        if idx >= 0:
            snippets[name] = normalize(tex[idx : idx + 900])
    return snippets


def selected_papers(papers: list[Paper]) -> list[Paper]:
    # No direct posture/human-pose paper is present. Select at most one indirect item
    # with the strongest topical overlap: health-oriented computer vision.
    selected = [p for p in papers if "Lung Disease" in p.title or "lung disease" in p.title.lower()]
    return selected[:1]


def write_analysis(categories: list[str], raw_entries: list[tuple[str, str]], papers: list[Paper]) -> None:
    selected = selected_papers(papers)
    count_by_relevance = defaultdict(int)
    for paper in papers:
        count_by_relevance[paper.relevance] += 1

    lines: list[str] = []
    lines.append("# PHÂN TÍCH BÀI BÁO CỦA THẦY KHÔI CÓ THỂ TRÍCH DẪN")
    lines.append("")
    lines.append("## 1. Tổng quan file Word")
    lines.append("")
    lines.append(f"- File đọc: `{DOCX_PATH}`")
    lines.append(f"- Tổng số dòng tài liệu raw trong file Word: {len(raw_entries)}")
    lines.append(f"- Tổng số bài/tài liệu unique sau khi gộp trùng: {len(papers)}")
    lines.append(f"- Số nhóm lĩnh vực trong file Word: {len(categories)}")
    lines.append(f"- Số bài có thể liên quan gián tiếp: {count_by_relevance.get('Liên quan gián tiếp', 0)}")
    lines.append(f"- Số bài ít liên quan: {count_by_relevance.get('Ít liên quan', 0)}")
    lines.append(f"- Số bài không nên thêm: {count_by_relevance.get('Không nên thêm', 0)}")
    lines.append(f"- Số bài nên thêm vào bản thảo hiện tại: {len(selected)} bài, và chỉ nên xem là liên quan gián tiếp.")
    lines.append("")
    lines.append("Nhận xét chính: trong danh sách không thấy bài nào trực tiếp về sitting posture recognition, human pose estimation, MediaPipe Pose, webcam-based monitoring hoặc ergonomic posture feedback. Vì vậy không nên thêm nhiều bài của thầy vào Related Work, tránh làm loãng bài báo.")
    lines.append("")
    lines.append("## 2. Bảng đánh giá toàn bộ bài báo")
    lines.append("")
    lines.append("| STT | Tên bài | Tác giả | Năm | Nguồn | DOI/URL | Nhóm lĩnh vực | Chủ đề chính | Mức độ liên quan | Lý do |")
    lines.append("| ---: | ------- | ------- | --- | ----- | ------- | ------------- | ------------ | ---------------- | ----- |")
    for paper in papers:
        lines.append(
            md_table_row(
                [
                    str(paper.stt),
                    paper.title,
                    paper.authors,
                    paper.year,
                    paper.source or "Không rõ nguồn trong dòng trích dẫn",
                    paper.doi_url,
                    "; ".join(paper.categories),
                    paper.topic,
                    paper.relevance,
                    paper.reason,
                ]
            )
        )
    lines.append("")
    lines.append("## 3. Top bài nên thêm")
    lines.append("")
    if not selected:
        lines.append("Không có bài nào đủ gần để khuyến nghị thêm vào References chính.")
    else:
        lines.append("Không có bài nào thật sự trực tiếp. Nếu thầy hướng dẫn muốn có liên kết học thuật với nhóm nghiên cứu của thầy, chỉ nên thêm tối đa 1 bài sau:")
        lines.append("")
        for paper in selected:
            lines.append(f"### {paper.title}")
            lines.append("")
            lines.append(f"- Mức độ: {paper.relevance}.")
            lines.append("- Vì sao liên quan: cùng hướng AI thị giác/deep learning trong bối cảnh sức khỏe, nhưng khác dữ liệu và mục tiêu; bài hiện tại dùng webcam pose landmarks cho posture monitoring, không dùng X-ray.")
            lines.append("- Nên dùng ở phần: Introduction hoặc Related Work, với vai trò nền bối cảnh health-oriented visual AI, không phải Related Work trực tiếp về posture.")
            lines.append("- Có nên thêm vào References chính không: có thể thêm nếu thầy muốn, nhưng nên ghi câu chèn thật rõ là liên quan gián tiếp.")
            lines.append(f"- DOI/URL: `{paper.doi_url}`")
    lines.append("")
    lines.append("## 4. Vị trí chèn đề xuất trong bài báo hiện tại")
    lines.append("")
    snippets = find_context_snippets()
    if selected:
        paper = selected[0]
        lines.append(f"### Paper được chọn: {paper.title}")
        lines.append("")
        lines.append("- Vị trí chèn khuyến nghị: `Introduction`, sau đoạn nói về nhu cầu hệ thống webcam chi phí thấp hoặc sau đoạn nêu hạn chế sensor/depth/RGB-D.")
        lines.append("- Không nên chèn vào đoạn `Pose-landmark-based posture analysis` như một bài posture trực tiếp, vì bài X-ray không dùng pose landmarks.")
        lines.append("- Câu trước/câu sau gợi ý:")
        lines.append("")
        lines.append("> Previous posture monitoring studies have used pressure sensors, force sensors, motion-capture devices, smart chairs, RGB-D cameras, and RGB camera systems.")
        lines.append("")
        lines.append("- Câu tiếng Anh đề xuất để chèn:")
        lines.append("")
        lines.append("> Image-based health AI has also been studied in clinical imaging tasks such as X-ray-based lung disease diagnosis (Khiem et al., 2026); however, the present work differs by using webcam-derived pose landmarks for non-clinical working posture monitoring and real-time feedback.")
        lines.append("")
        lines.append("- Lý do: câu này đặt bài của thầy vào bối cảnh AI thị giác trong sức khỏe nhưng vẫn phân biệt rõ nó không phải nền tảng trực tiếp của posture detection.")
        if snippets.get("introduction_gap"):
            lines.append("")
            lines.append("Đoạn liên quan trong LaTeX hiện tại để tham chiếu:")
            lines.append("")
            lines.append("```text")
            lines.append(snippets["introduction_gap"])
            lines.append("```")
    else:
        lines.append("Không đề xuất chèn citation mới.")
    lines.append("")
    lines.append("## 5. APA 7 references cho các bài được chọn")
    lines.append("")
    if selected:
        lines.append("- Khiem, N. M., Quyen, P. N., Quang, T. D., & Anh-Khoi, N. H. (2026). Leveraging deep learning for lung disease diagnosis and classification through X-ray imaging. In N. Goyal, T. N. Nguyen, M. Lata, & G. A. Ogunmola (Eds.), *Proceedings of the International Conference on Sustainable Computing. ICSC 2025. Lecture Notes in Electrical Engineering* (Vol. 1530). Springer. https://doi.org/10.1007/978-981-95-6063-9_16")
    else:
        lines.append("Không có reference mới được chọn.")
    lines.append("")
    lines.append("## 6. Các bài không nên thêm và lý do")
    lines.append("")
    lines.append("- Nhóm chatbot, LLM, word alignment, economy QA benchmark: không liên quan đến computer vision/posture/health monitoring.")
    lines.append("- Nhóm security, malware, DDoS, blockchain/networking: lệch hoàn toàn khỏi chủ đề.")
    lines.append("- Nhóm economy, tourism, hotel booking, banking churn, education dropout: chủ yếu là tabular prediction hoặc NLP/economy, không hỗ trợ Related Work posture.")
    lines.append("- Nhóm gemmology/archeology/hardware gemstone: có yếu tố nhận dạng hoặc thiết bị, nhưng miền ứng dụng quá xa; chỉ nên dùng nếu bài báo mở rộng rất mạnh sang continuous learning/image identification, hiện không cần.")
    lines.append("- Nhóm robotics speech/RAG: có yếu tố real-time HCI nhưng không phải visual human monitoring.")
    lines.append("")
    lines.append("## 7. Cần kiểm tra thủ công")
    lines.append("")
    missing = [p for p in papers if p.doi_url == "Không thấy DOI/link trong file Word"]
    lines.append(f"- Có {len(missing)} bài không thấy DOI/link trong file Word.")
    lines.append("- Các bài thiếu DOI/link không nên chèn vào References chính cho đến khi xác minh được DOI/URL/venue chính thức.")
    lines.append("- Các bài năm 2026 cần kiểm tra trạng thái xuất bản chính thức nếu dùng trong bản nộp hội thảo.")
    lines.append("- Bài được đề xuất chèn có DOI trong file Word, nhưng vì là liên quan gián tiếp nên vẫn cần thầy xác nhận có thật sự muốn thêm hay không.")
    lines.append("")
    OUT_ANALYSIS.write_text("\n".join(lines), encoding="utf-8")


def write_patch(papers: list[Paper]) -> None:
    selected = selected_papers(papers)
    lines: list[str] = []
    lines.append("# THAYKHOI_INSERTION_PATCH")
    lines.append("")
    lines.append("File này chỉ là patch gợi ý. Không tự động sửa LaTeX/PDF ở bước này.")
    lines.append("")
    if not selected:
        lines.append("Không có bài nào đủ gần để đề xuất patch chèn citation.")
        OUT_PATCH.write_text("\n".join(lines), encoding="utf-8")
        return

    lines.append("## 1. Citation đề xuất")
    lines.append("")
    lines.append("- In-text citation: `(Khiem et al., 2026)`")
    lines.append("- Mức liên quan: liên quan gián tiếp, dùng để nói về health-oriented visual AI, không phải posture detection trực tiếp.")
    lines.append("")
    lines.append("## 2. Câu chèn đề xuất trong `main_applied_research_final_formatfix.tex`")
    lines.append("")
    lines.append("### Vị trí")
    lines.append("")
    lines.append("Section `Introduction`, sau câu/đoạn:")
    lines.append("")
    lines.append("```tex")
    lines.append("Previous posture monitoring studies have used pressure sensors, force sensors, motion-capture devices, smart chairs, RGB-D cameras, and RGB camera systems.")
    lines.append("```")
    lines.append("")
    lines.append("### Câu thêm")
    lines.append("")
    lines.append("```tex")
    lines.append("Image-based health AI has also been studied in clinical imaging tasks such as X-ray-based lung disease diagnosis (Khiem et al., 2026); however, the present work differs by using webcam-derived pose landmarks for non-clinical working posture monitoring and real-time feedback.")
    lines.append("```")
    lines.append("")
    lines.append("### Lưu ý")
    lines.append("")
    lines.append("- Không chèn câu này vào Conclusion.")
    lines.append("- Không dùng câu này để claim rằng bài X-ray là nền tảng trực tiếp của posture detection.")
    lines.append("- Nếu muốn Related Work thật tập trung, có thể không chèn citation này.")
    lines.append("")
    lines.append("## 3. Reference APA 7 cần thêm")
    lines.append("")
    lines.append("```text")
    lines.append("Khiem, N. M., Quyen, P. N., Quang, T. D., & Anh-Khoi, N. H. (2026). Leveraging deep learning for lung disease diagnosis and classification through X-ray imaging. In N. Goyal, T. N. Nguyen, M. Lata, & G. A. Ogunmola (Eds.), Proceedings of the International Conference on Sustainable Computing. ICSC 2025. Lecture Notes in Electrical Engineering (Vol. 1530). Springer. https://doi.org/10.1007/978-981-95-6063-9_16")
    lines.append("```")
    lines.append("")
    lines.append("## 4. Nếu dùng BibTeX")
    lines.append("")
    lines.append("```bibtex")
    lines.append("@incollection{khiem2026lung_xray,")
    lines.append("  author    = {Khiem, N. M. and Quyen, P. N. and Quang, T. D. and Anh-Khoi, N. H.},")
    lines.append("  title     = {Leveraging Deep Learning for Lung Disease Diagnosis and Classification Through X-ray Imaging},")
    lines.append("  booktitle = {Proceedings of the International Conference on Sustainable Computing. ICSC 2025},")
    lines.append("  series    = {Lecture Notes in Electrical Engineering},")
    lines.append("  volume    = {1530},")
    lines.append("  publisher = {Springer},")
    lines.append("  year      = {2026},")
    lines.append("  doi       = {10.1007/978-981-95-6063-9_16},")
    lines.append("  url       = {https://doi.org/10.1007/978-981-95-6063-9_16}")
    lines.append("}")
    lines.append("```")
    lines.append("")
    OUT_PATCH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    categories, raw_entries, papers = extract_entries()
    write_analysis(categories, raw_entries, papers)
    write_patch(papers)
    print(OUT_ANALYSIS)
    print(OUT_PATCH)


if __name__ == "__main__":
    main()
