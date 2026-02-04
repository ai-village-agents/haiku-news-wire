#!/usr/bin/env python3
import json
import urllib.request
import sys
from datetime import datetime

# Fetch Federal Register documents - try different dates
dates = ['2026-02-06', '2026-02-05', '2026-02-04']
all_docs = []

for date in dates:
    try:
        url = f"https://www.federalregister.gov/api/v1/documents?publication_date={date}&per_page=100"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
        
        docs = data.get('results', [])
        all_docs.extend(docs)
        print(f"Fetched {len(docs)} documents from {date}", file=sys.stderr)
        
        if len(all_docs) >= 100:
            break
    except Exception as e:
        print(f"Error fetching {date}: {e}", file=sys.stderr)

selected_docs = all_docs[:100]
print(f"Using {len(selected_docs)} documents for stories 363-{362+len(selected_docs)}", file=sys.stderr)

# Generate HTML stories
for idx, doc in enumerate(selected_docs):
    story_num = 363 + idx
    
    title = doc.get('title', 'Untitled Document')
    abstract = doc.get('abstract', 'No description available')
    agency = doc.get('agency_names', ['Federal Agency'])[0] if doc.get('agency_names') else 'Federal Agency'
    pub_date = doc.get('publication_date', '2026-02-07')
    doc_number = doc.get('document_number', 'Unknown')
    html_url = doc.get('html_url', '#')
    doc_type = doc.get('document_type', 'Document')
    
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Story {story_num}: {title[:60]}</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; background-color: #f5f5f5;">
<article style="background-color: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
<h1 style="margin-top: 0; color: #1976d2;">{title}</h1>
<div style="font-size: 12px; color: #666; margin: 10px 0;">
  <strong>Agency:</strong> {agency} | <strong>Published:</strong> {pub_date} | <strong>Story ID:</strong> {story_num}
</div>
<h2>Overview</h2>
<p>{abstract}</p>

<h2>Document Details</h2>
<p><strong>Document Type:</strong> {doc_type}<br>
<strong>Document Number:</strong> {doc_number}<br>
<strong>Agency:</strong> {agency}<br>
<strong>Publication Date:</strong> {pub_date}</p>

<h2>Federal Register Action</h2>
<p>This action represents a formal government notice in the Federal Register, indicating policy changes, regulations, notices, or proposed rules from {agency}. The document is subject to federal administrative procedures and public comment periods as applicable.</p>

<h2>Additional Information</h2>
<p><a href="{html_url}" target="_blank">View full document on Federal Register</a></p>

<hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
<footer style="font-size: 12px; color: #999;">
<p>Source: Federal Register API</p>
<p>Government Policy | {datetime.now().strftime('%B %d, %Y')}</p>
</footer>
</article>
</body>
</html>"""
    
    # Write story file
    filename = f"story_{story_num}.html"
    with open(filename, 'w') as f:
        f.write(html)

print(f"\nSuccessfully generated {len(selected_docs)} Federal Register stories", file=sys.stderr)
