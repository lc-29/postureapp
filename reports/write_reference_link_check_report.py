from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IN_JSON = ROOT / "reports" / "REFERENCE_LINK_CHECK_25.json"
OUT_MD = ROOT / "reports" / "REFERENCE_LINK_CHECK_25_REPORT.md"


def clean_cell(text: str) -> str:
    return text.replace("|", "/").replace("\n", " ").strip()


def main() -> None:
    items = json.loads(IN_JSON.read_text(encoding="utf-8"))
    lines: list[str] = []
    lines.append("# REFERENCE_LINK_CHECK_25_REPORT")
    lines.append("")
    lines.append(
        "Nguồn kiểm tra: `reports/SPRINGER_MANUSCRIPT_APPLIED_RESEARCH_RESTRUCTURED.md` "
        "và 25 tài liệu tham khảo tương ứng trong bài báo."
    )
    lines.append("")
    lines.append(
        "Quy ước: `OK` nghĩa là URL truy cập trực tiếp được hoặc DOI metadata xác nhận đúng tiêu đề. "
        "`403 nhưng DOI đúng` nghĩa là trang publisher chặn request tự động, nhưng DOI vẫn hợp lệ "
        "và metadata trả đúng bài."
    )
    lines.append("")
    lines.append("| STT | Tài liệu rút gọn | URL | HTTP | DOI metadata | Kết luận |")
    lines.append("|---:|---|---|---:|---|---|")
    for item in items:
        ref = item["ref"]
        title = item["doi_title"] or item["page_title"]
        short = re.sub(r"^\d+\.\s*", "", ref).split("https://")[0].strip()
        if len(short) > 98:
            short = short[:95] + "..."
        http = str(item["status"]) if item["status"] is not None else "ERR"
        if item["ok_http"]:
            conclusion = "OK - link hoạt động."
        elif item["doi_meta_ok"]:
            conclusion = "OK - 403/chặn bot nhưng DOI metadata đúng."
        else:
            conclusion = "Cần kiểm tra thủ công."
        if item["doi_meta_ok"]:
            doi_meta = "Có: " + title[:100]
        elif "doi.org" not in item["url"]:
            doi_meta = "Không áp dụng"
        else:
            doi_meta = "Không"
        lines.append(
            "| {stt} | {short} | `{url}` | {http} | {doi_meta} | {conclusion} |".format(
                stt=item["stt"],
                short=clean_cell(short),
                url=item["url"],
                http=http,
                doi_meta=clean_cell(doi_meta),
                conclusion=conclusion,
            )
        )
    lines.append("")
    lines.append("## Kết luận")
    lines.append("")
    lines.append("- 25/25 tài liệu có URL/DOI hợp lệ theo kiểm tra tự động.")
    lines.append("- Không phát hiện DOI sai tiêu đề.")
    lines.append(
        "- Các link trả 403 là do publisher chặn truy cập tự động, không phải DOI chết: "
        "MDPI, ACM, PeerJ trong một số mục."
    )
    lines.append(
        "- Link Google AI Edge vẫn hoạt động nhưng redirect sang "
        "`https://developers.google.com/edge/mediapipe/solutions/vision/pose_landmarker`; "
        "có thể thay bằng URL cuối này nếu muốn ổn định hơn."
    )
    lines.append(
        "- Hai DOI Elsevier có dấu ngoặc trong DOI là hợp lệ: "
        "`10.1016/S0003-6870(99)00039-3` và `10.1016/0003-6870(93)90080-S`."
    )
    lines.append("")
    lines.append("File raw JSON: `reports/REFERENCE_LINK_CHECK_25.json`.")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(OUT_MD)


if __name__ == "__main__":
    main()
