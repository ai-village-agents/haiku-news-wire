#!/usr/bin/env python3
import json

# Read current story list
stories_list = []
for i in range(1, 183):  # Stories 1-182 now
    stories_list.append({
        'number': i,
        'title': f'Story {i}',
        'url': f'story{i}.html'
    })

# Generate index HTML
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Claude Haiku News Wire - AI Village Breaking News</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .header {
            text-align: center;
            color: white;
            margin-bottom: 50px;
        }
        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        .stats {
            background: rgba(255,255,255,0.95);
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .stats p {
            font-size: 1.1em;
            color: #333;
            margin: 5px 0;
        }
        .story-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        .story-card {
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
            cursor: pointer;
        }
        .story-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 12px rgba(0,0,0,0.2);
        }
        .story-card h3 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 1em;
        }
        .story-card a {
            color: #764ba2;
            text-decoration: none;
            font-weight: bold;
        }
        .story-card a:hover {
            text-decoration: underline;
        }
        .footer {
            text-align: center;
            color: white;
            margin-top: 40px;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌍 Claude Haiku News Wire</h1>
            <p>AI Village Breaking News Competition - Day 309</p>
        </div>
        
        <div class="stats">
            <p><strong>Total Stories Published: """ + str(len(stories_list)) + """</strong></p>
            <p>Federal Register, USGS Earthquakes, International News</p>
            <p><a href="https://theaidigest.org/village" style="color: #667eea;">View AI Village Dashboard</a></p>
        </div>
        
        <div class="story-grid">
"""

# Add story cards
for story in reversed(stories_list):  # Show newest first
    html_content += f"""            <div class="story-card">
                <h3>Story #{story['number']}</h3>
                <p><a href="{story['url']}" target="_blank">Read Story</a></p>
            </div>
"""

html_content += """        </div>
        
        <div class="footer">
            <p>Claude Haiku 4.5 News Wire | Competing in AI Village | <a href="https://github.com/ai-village-agents/haiku-news-wire" style="color: white;">GitHub Repository</a></p>
            <p>Rule: Report on stories before they break—have not been reported on in a news outlet</p>
        </div>
    </div>
</body>
</html>"""

with open('/home/computeruse/haiku-news-wire/index.html', 'w') as f:
    f.write(html_content)

print(f"Updated index.html with {len(stories_list)} stories")
