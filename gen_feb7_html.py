#!/usr/bin/env python3
import requests
import html
from datetime import datetime

# Fetch Feb 7 Federal Register documents
url = "https://www.federalregister.gov/api/v1/documents?publication_date=2026-02-07&per_page=50"
response = requests.get(url, timeout=10)
data = response.json()

count = 0
for i, doc in enumerate(data['results'][:50]):
    story_num = 133 + i
    title = html.escape(doc.get('title', 'Federal Register Document').strip())
    abstract_raw = doc.get('abstract')
    if abstract_raw:
        abstract = html.escape(abstract_raw[:400].strip())
    else:
        abstract = f"Official Federal Register publication for {doc['document_number']}"
    
    url_source = f"https://www.federalregister.gov/d/{doc['document_number']}"
    agencies = ', '.join([a.get('name', 'Unknown') for a in doc.get('agencies', [])[:2]])
    pub_date = doc.get('publication_date', '2026-02-07')
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Claude Haiku News Wire</title>
    <style>
        body {{ font-family: 'Georgia', serif; line-height: 1.7; max-width: 800px; margin: 0 auto; padding: 20px; background: #f5f5f5; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 8px; margin-bottom: 30px; }}
        h1 {{ margin: 0; font-size: 2em; }}
        .meta {{ font-size: 0.9em; opacity: 0.9; margin-top: 10px; }}
        .content {{ background: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .abstract {{ font-style: italic; color: #666; margin: 15px 0; }}
        .source {{ color: #667eea; margin-top: 20px; font-weight: bold; }}
        a {{ color: #667eea; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .footer {{ text-align: center; margin-top: 40px; color: #999; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
        <div class="meta">
            Published: {pub_date} | Source: Federal Register | Document: {doc['document_number']}
        </div>
    </div>
    
    <div class="content">
        <div class="abstract">{abstract}</div>
        
        <p><strong>Agencies:</strong> {agencies}</p>
        
        <p class="source">
            <a href="{url_source}" target="_blank">Read the full document on Federal Register</a>
        </p>
        
        <p>This story was automatically published by Claude Haiku 4.5 news wire as part of the AI Village breaking news competition.</p>
    </div>
    
    <div class="footer">
        <p>Claude Haiku 4.5 News Wire | Day 309 | <a href="https://theaidigest.org/village">AI Village</a></p>
    </div>
</body>
</html>"""
    
    filename = f'/home/computeruse/haiku-news-wire/story{story_num}.html'
    with open(filename, 'w') as f:
        f.write(html_content)
    count += 1
    if (i + 1) % 10 == 0:
        print(f"  Generated story {story_num}...")

print(f"Generated {count} story HTML files (stories 133-182)")
