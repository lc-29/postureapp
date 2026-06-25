from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

try:
    import requests
except Exception as exc:  # pragma: no cover
    print(f"NO_REQUESTS: {exc}")
    sys.exit(1)


ROOT = Path(__file__).resolve().parents[1]
REF_SOURCE = ROOT / "reports" / "SPRINGER_MANUSCRIPT_APPLIED_RESEARCH_RESTRUCTURED.md"
OUT_JSON = ROOT / "reports" / "REFERENCE_LINK_CHECK_25.json"

HEADERS = {"User-Agent": "Mozilla/5.0 reference-checker (academic link validation)"}


def extract_refs() -> list[str]:
    text = REF_SOURCE.read_text(encoding="utf-8")
    refs = text.split("## References", 1)[1].strip().splitlines()
    return [ref.strip() for ref in refs if ref.strip()]


def extract_url(ref: str) -> str:
    match = re.search(r"https?://\S+", ref)
    if not match:
        return ""
    return match.group(0).rstrip(".,;").replace("*", "")


def page_title(html: str) -> str:
    match = re.search(r"<title[^>]*>(.*?)</title>", html or "", flags=re.I | re.S)
    if not match:
        return ""
    return re.sub(r"\s+", " ", match.group(1)).strip()[:180]


def doi_metadata_title(url: str) -> tuple[bool, str]:
    if "doi.org/" not in url.lower():
        return False, ""
    doi = url.split("doi.org/", 1)[1]
    try:
        response = requests.get(
            url,
            headers={**HEADERS, "Accept": "application/vnd.citationstyles.csl+json"},
            allow_redirects=True,
            timeout=20,
        )
        content_type = response.headers.get("content-type", "").lower()
        if response.status_code == 200 and "json" in content_type:
            data = response.json()
            return True, (data.get("title") or "").strip()[:220]
    except Exception:
        pass

    try:
        response = requests.get(
            "https://api.crossref.org/works/" + doi,
            headers=HEADERS,
            timeout=20,
        )
        if response.status_code == 200:
            data = response.json().get("message", {})
            titles = data.get("title") or []
            return bool(titles), (titles[0] if titles else "").strip()[:220]
    except Exception:
        pass
    return False, ""


def check_url(stt: int, ref: str) -> dict:
    url = extract_url(ref)
    result = {
        "stt": stt,
        "url": url,
        "status": None,
        "ok_http": False,
        "final": "",
        "page_title": "",
        "doi_meta_ok": False,
        "doi_title": "",
        "error": "",
        "ref": ref,
    }
    try:
        response = requests.get(
            url,
            headers=HEADERS,
            allow_redirects=True,
            timeout=20,
        )
        result["status"] = response.status_code
        result["ok_http"] = 200 <= response.status_code < 400
        result["final"] = response.url
        result["page_title"] = page_title(response.text)
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {str(exc)[:160]}"

    meta_ok, title = doi_metadata_title(url)
    result["doi_meta_ok"] = meta_ok
    result["doi_title"] = title
    return result


def main() -> None:
    results = []
    for i, ref in enumerate(extract_refs(), 1):
        results.append(check_url(i, ref))
        time.sleep(0.15)
    OUT_JSON.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(OUT_JSON)
    for item in results:
        title = item["doi_title"] or item["page_title"] or item["error"]
        print(
            "{stt:02d} status={status} ok={ok_http} doi_meta={doi_meta_ok} url={url}".format(
                **item
            )
        )
        print("    final=", item["final"][:180])
        print("    title=", title[:220])


if __name__ == "__main__":
    main()
