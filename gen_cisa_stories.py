#!/usr/bin/env python3
import json
import urllib.request
import sys
from datetime import datetime

# Fetch CISA KEV data
url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
except Exception as e:
    print(f"Error fetching CISA data: {e}", file=sys.stderr)
    sys.exit(1)

vulns = data.get('vulnerabilities', [])
print(f"Total vulnerabilities in CISA KEV: {len(vulns)}", file=sys.stderr)

# Sort by dateAdded descending (most recent first)
vulns_sorted = sorted(vulns, key=lambda x: x.get('dateAdded', ''), reverse=True)

# Take top 30 for stories 183-212
story_vulns = vulns_sorted[:30]

print(f"Selected {len(story_vulns)} vulnerabilities for stories", file=sys.stderr)

# Generate HTML stories
for idx, vuln in enumerate(story_vulns):
    story_num = 183 + idx
    
    cve = vuln.get('cveID', 'Unknown')
    vendor = vuln.get('vendorProject', 'Unknown')
    product = vuln.get('product', 'Unknown')
    vuln_name = vuln.get('vulnerabilityName', 'Unknown')
    date_added = vuln.get('dateAdded', 'Unknown')
    description = vuln.get('shortDescription', 'No description')
    due_date = vuln.get('dueDate', 'Unknown')
    ransomware = vuln.get('knownRansomwareCampaignUse', 'Unknown')
    notes = vuln.get('notes', '')
    
    # Create HTML story
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Story {story_num}: {cve} - {vendor}</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; background-color: #f5f5f5;">
<article style="background-color: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
<h1 style="margin-top: 0; color: #d32f2f;">{cve}: Critical {vendor} {product} Vulnerability</h1>
<div style="font-size: 12px; color: #666; margin: 10px 0;">
  <strong>Published:</strong> {date_added} | <strong>Story ID:</strong> {story_num}
</div>
<h2>Vulnerability Details</h2>
<p><strong>Vendor:</strong> {vendor}<br>
<strong>Product:</strong> {product}<br>
<strong>Vulnerability:</strong> {vuln_name}<br>
<strong>CVE ID:</strong> {cve}</p>

<h2>Description</h2>
<p>{description}</p>

<h2>Remediation Timeline</h2>
<p><strong>Added to CISA KEV Catalog:</strong> {date_added}<br>
<strong>Federal Action Required By:</strong> {due_date}<br>
<strong>Known Ransomware Campaign Use:</strong> {ransomware}</p>

<h2>Required Actions</h2>
<p>Federal agencies and critical infrastructure operators must apply vendor mitigations immediately. For vulnerabilities without available mitigations, discontinuation of use is required. All agencies subject to BOD 22-01 must comply with the specified remediation timeline.</p>

<h2>References</h2>
<p>{notes}</p>

<hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
<footer style="font-size: 12px; color: #999;">
<p>Source: CISA Known Exploited Vulnerabilities Catalog</p>
<p>Breaking News | Cybersecurity Intelligence | {datetime.now().strftime('%B %d, %Y')}</p>
</footer>
</article>
</body>
</html>"""
    
    # Write story file
    filename = f"story_{story_num}.html"
    with open(filename, 'w') as f:
        f.write(html)
    
    print(f"✓ Generated {filename}: {cve} - {vendor}", file=sys.stderr)

print(f"\nSuccessfully generated {len(story_vulns)} CISA KEV stories", file=sys.stderr)
