#!/usr/bin/env python3
"""
Multi-source world news monitoring pipeline
Hunts for major breaking news across SEC, USGS, NOAA, FDA, etc.
"""

import requests
import json
import datetime
import urllib.parse
from datetime import datetime, timedelta

def monitor_sec_edgar():
    """Monitor SEC EDGAR for major M&A filings (>$100M)"""
    print("[SEC EDGAR] Monitoring for major M&A transactions...")
    try:
        url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&type=8-K&dateb=&owner=exclude&count=100&output=xml"
        headers = {"User-Agent": "Claude-Haiku-NewsAgent/1.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            print(f"[SEC EDGAR] ✓ Retrieved 8-K filings")
            return resp.text
    except Exception as e:
        print(f"[SEC EDGAR] ✗ Error: {e}")
    return None

def monitor_usgs_earthquakes():
    """Monitor USGS for significant earthquakes (M5.5+)"""
    print("[USGS] Monitoring for earthquakes M5.5+...")
    try:
        # Get earthquakes from last 7 days with magnitude >= 5.5
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=7)
        
        url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_date.isoformat()}Z&endtime={end_date.isoformat()}Z&minmagnitude=5.5"
        headers = {"User-Agent": "Claude-Haiku-NewsAgent/1.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            earthquakes = data.get('features', [])
            print(f"[USGS] ✓ Found {len(earthquakes)} earthquakes M5.5+")
            return earthquakes
    except Exception as e:
        print(f"[USGS] ✗ Error: {e}")
    return []

def monitor_noaa_space_weather():
    """Monitor NOAA for space weather alerts"""
    print("[NOAA] Monitoring space weather...")
    try:
        url = "https://services.swpc.noaa.gov/products/alerts.json"
        headers = {"User-Agent": "Claude-Haiku-NewsAgent/1.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            alerts = resp.json()
            print(f"[NOAA] ✓ Retrieved space weather alerts")
            return alerts
    except Exception as e:
        print(f"[NOAA] ✗ Error: {e}")
    return []

def monitor_hackernews():
    """Monitor HackerNews for breaking tech news"""
    print("[HackerNews] Monitoring top stories...")
    try:
        # Get top stories
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        headers = {"User-Agent": "Claude-Haiku-NewsAgent/1.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            story_ids = resp.json()[:30]  # Top 30
            print(f"[HackerNews] ✓ Retrieved {len(story_ids)} top stories")
            
            stories = []
            for story_id in story_ids[:5]:  # Get details for top 5
                try:
                    story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                    story_resp = requests.get(story_url, headers=headers, timeout=5)
                    if story_resp.status_code == 200:
                        stories.append(story_resp.json())
                except:
                    pass
            return stories
    except Exception as e:
        print(f"[HackerNews] ✗ Error: {e}")
    return []

def monitor_cisa_kev():
    """Monitor CISA Known Exploited Vulnerabilities"""
    print("[CISA KEV] Checking for new vulnerabilities...")
    try:
        url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
        headers = {"User-Agent": "Claude-Haiku-NewsAgent/1.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            vulnerabilities = data.get('vulnerabilities', [])
            print(f"[CISA KEV] ✓ Retrieved {len(vulnerabilities)} known exploited vulnerabilities")
            # Return most recent ones
            return sorted(vulnerabilities, key=lambda x: x.get('dateAdded', ''), reverse=True)[:10]
    except Exception as e:
        print(f"[CISA KEV] ✗ Error: {e}")
    return []

if __name__ == "__main__":
    print(f"\n{'='*60}")
    print(f"HAIKU NEWS MONITOR - Day 308")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"{'='*60}\n")
    
    # Run all monitors
    results = {
        'usgs_earthquakes': monitor_usgs_earthquakes(),
        'noaa_alerts': monitor_noaa_space_weather(),
        'hackernews': monitor_hackernews(),
        'cisa_kev': monitor_cisa_kev(),
        'timestamp': datetime.now().isoformat()
    }
    
    # Try SEC last as it sometimes has issues
    sec_data = monitor_sec_edgar()
    
    # Save results
    with open('monitor_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"Monitoring complete. Results saved to monitor_results.json")
    print(f"{'='*60}\n")
    
    # Print summary
    print("SUMMARY:")
    print(f"  - USGS Earthquakes (M5.5+): {len(results['usgs_earthquakes'])}")
    print(f"  - NOAA Alerts: {len(results['noaa_alerts'])}")
    print(f"  - HackerNews Top: {len(results['hackernews'])}")
    print(f"  - CISA KEV Recent: {len(results['cisa_kev'])}")

