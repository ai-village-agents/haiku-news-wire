import requests
import json
from datetime import datetime

# Fetch Feb 7 Federal Register documents
url = "https://www.federalregister.gov/api/v1/documents?publication_date=2026-02-07&per_page=40"
response = requests.get(url, timeout=10)
data = response.json()

print(f"Fetched {len(data['results'])} Feb 7 documents")

# Filter for high-value document types
high_value_types = ['Rule', 'Notice', 'Proposed Rule']
stories = []

for doc in data['results']:
    if doc.get('document_type') in high_value_types or 'Alert' in doc.get('title', ''):
        story = {
            'title': doc.get('title', 'No Title'),
            'abstract': doc.get('abstract', '')[:300],
            'source': 'Federal Register',
            'url': f"https://www.federalregister.gov/documents/{doc['html_url'].split('/')[-1]}",
            'document_number': doc.get('document_number'),
            'agencies': [a.get('name', 'Unknown') for a in doc.get('agencies', [])[:2]],
            'publication_date': doc.get('publication_date')
        }
        stories.append(story)

print(json.dumps(stories, indent=2))
