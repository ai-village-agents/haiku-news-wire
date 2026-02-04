import json
from html import escape
from pathlib import Path

DATA_FILE = Path("feb_5_6_documents.json")
START_INDEX = 77
COUNT = 50
OUTPUT_PATTERN = "story{index}.html"


def load_documents(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_agency_name(doc: dict) -> str:
    agencies = doc.get("agencies") or []
    if not agencies:
        return "Unknown Agency"
    return agencies[0].get("name") or agencies[0].get("raw_name") or "Unknown Agency"


def build_html(doc: dict) -> str:
    title = escape(doc.get("title") or "Untitled")
    agency = escape(get_agency_name(doc))
    pub_date = escape(doc.get("publication_date") or "Unknown date")
    abstract_raw = doc.get("abstract") or ""
    abstract = escape(abstract_raw[:300])
    link = escape(doc.get("html_url") or "#")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; background: #f7f7f7; }}
        .story {{ background: #fff; padding: 24px; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.08); }}
        h1 {{ margin: 0 0 12px; font-size: 26px; color: #1a237e; }}
        .meta {{ color: #555; margin-bottom: 18px; }}
        .meta span {{ display: inline-block; margin-right: 16px; }}
        .abstract {{ line-height: 1.6; margin-bottom: 18px; }}
        a {{ color: #0d47a1; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="story">
        <h1>{title}</h1>
        <div class="meta">
            <span><strong>Agency:</strong> {agency}</span>
            <span><strong>Publication Date:</strong> {pub_date}</span>
        </div>
        <div class="abstract">
            <strong>Abstract:</strong> {abstract or "No abstract available."}
        </div>
        <div>
            <a href="{link}" target="_blank" rel="noopener">Read full document</a>
        </div>
    </div>
</body>
</html>
"""


def main():
    documents = load_documents(DATA_FILE)[:COUNT]
    for offset, doc in enumerate(documents):
        index = START_INDEX + offset
        html = build_html(doc)
        output_path = Path(OUTPUT_PATTERN.format(index=index))
        output_path.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
