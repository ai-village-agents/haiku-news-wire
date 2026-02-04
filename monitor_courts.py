import urllib.request
import time
from datetime import datetime

courts = {
    'ICC': 'https://www.icc-cpi.int/news',
    'ECHR': 'https://www.echr.coe.int/press',
    'ECJ': 'https://curia.europa.eu/jcms/jcms/T_en/',
    'ICJ': 'https://www.icj-cij.org/en/news',
    'ITLOS': 'https://www.itlos.org/en/main/news'
}

print(f"[{datetime.now().strftime('%H:%M:%S')}] Monitoring international courts for Feb 4 publications...")
for name, url in courts.items():
    try:
        response = urllib.request.urlopen(url, timeout=5)
        content = response.read().decode('utf-8', errors='ignore')
        # Simple check for "February 4" or "Feb 4" or "4 February"
        if any(x in content for x in ['February 4', 'Feb 4', '4 February', '4 Feb', '2026-02-04']):
            print(f"✓ {name} - Found Feb 4 content!")
        else:
            print(f"- {name} - No Feb 4 content detected")
    except Exception as e:
        print(f"✗ {name} - Error: {str(e)[:30]}")
