#!/usr/bin/env python3
import requests
import json
import html

# Fetch Feb 7 Federal Register documents
url = "https://www.federalregister.gov/api/v1/documents?publication_date=2026-02-07&per_page=50"
response = requests.get(url, timeout=10)
data = response.json()

stories = []
for i, doc in enumerate(data['results'][:50]):
    title = doc.get('title', 'Untitled').strip()
    abstract_raw = doc.get('abstract')
    if abstract_raw:
        abstract = html.unescape(abstract_raw)[:250].strip()
    else:
        abstract = f"Federal Register Document {doc['document_number']}"
    
    stories.append({
        'num': 133 + i,
        'title': title,
        'abstract': abstract,
        'url': f"https://www.federalregister.gov/d/{doc['document_number']}",
        'source': 'Federal Register'
    })

print(f"Generated {len(stories)} story configs")
for s in stories[:5]:
    print(f"  Story {s['num']}: {s['title'][:50]}...")
