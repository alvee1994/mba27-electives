import os
import re
import json

def parse_html_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    rows = re.findall(r'<tr.*?>(.*?)</tr>', content, re.DOTALL)
    courses = []
    
    for row in rows[1:]: 
        cols = re.findall(r'<td.*?>(.*?)</td>', row, re.DOTALL)
        if len(cols) == 4:
            # Extract href and title
            title_match = re.search(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', cols[0], re.DOTALL)
            href = "#"
            title = "Unknown Course"
            if title_match:
                href = title_match.group(1)
                title = title_match.group(2)
            else:
                title = re.sub(r'<[^>]+>', '', cols[0]).strip()
            
            # extra notes in the title column
            extra_notes_match = re.search(r'</a>.*?</span>(.*)', cols[0], re.DOTALL)
            extra_notes = ""
            if extra_notes_match:
                extra_notes = re.sub(r'<[^>]+>', '', extra_notes_match.group(1)).strip()
            
            faculty = re.sub(r'<[^>]+>', '', cols[1]).strip()
            faculty = faculty.replace('&nbsp;', ' ').strip()
            
            subject = re.sub(r'<[^>]+>', '', cols[2]).strip()
            subject = subject.replace('&amp;', '&').strip()
            
            notes = re.sub(r'<[^>]+>', '', cols[3]).strip()
            
            if extra_notes:
                if notes:
                    notes = extra_notes + " - " + notes
                else:
                    notes = extra_notes
                    
            # Clean up entities
            title = title.replace('&amp;', '&').replace('&nbsp;', ' ')
            
            courses.append({
                "title": title.strip(),
                "href": href,
                "faculty": faculty,
                "subject": subject,
                "notes": notes.strip()
            })
    return courses

weekday_courses = parse_html_file('weekday_electives.html')
weekend_courses = parse_html_file('weekend_electives.html')

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MBA Electives 2026 Navigation</title>
    <meta name="description" content="Easy navigation for 2026 MBA Electives, including weekday and weekend courses.">
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #0f172a;
            --text-color: #f8fafc;
            --card-bg: rgba(255, 255, 255, 0.03);
            --card-border: rgba(255, 255, 255, 0.05);
            --primary: #38bdf8;
            --primary-hover: #0ea5e9;
            --accent: #c084fc;
        }}
        
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        
        body {{
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            line-height: 1.6;
            background-image: 
                radial-gradient(at 0% 0%, rgba(56, 189, 248, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(192, 132, 252, 0.15) 0px, transparent 50%);
            background-attachment: fixed;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 4rem 2rem;
        }}
        
        header {{
            text-align: center;
            margin-bottom: 4rem;
            animation: fadeInDown 0.8s ease-out;
        }}
        
        h1 {{
            font-size: 3.5rem;
            font-weight: 800;
            margin-bottom: 1rem;
            background: linear-gradient(to right, var(--primary), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        p.subtitle {{
            font-size: 1.2rem;
            color: #94a3b8;
            max-width: 600px;
            margin: 0 auto;
        }}
        
        .resources {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-bottom: 5rem;
            animation: fadeInUp 0.8s ease-out 0.2s both;
        }}
        
        .resource-card {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
            backdrop-filter: blur(10px);
            transition: transform 0.3s ease, box-shadow 0.3s ease, background 0.3s ease;
            text-decoration: none;
            color: inherit;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }}
        
        .resource-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            background: rgba(255, 255, 255, 0.05);
            border-color: rgba(255, 255, 255, 0.1);
        }}
        
        .resource-icon {{
            font-size: 3rem;
            margin-bottom: 1rem;
        }}
        
        .resource-title {{
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }}
        
        .section-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 2rem;
            border-bottom: 1px solid var(--card-border);
            padding-bottom: 1rem;
        }}
        
        .section-header h2 {{
            font-size: 2rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .tabs {{
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
            justify-content: center;
        }}
        
        .tab-btn {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            color: var(--text-color);
            padding: 0.75rem 2rem;
            border-radius: 30px;
            font-family: inherit;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            backdrop-filter: blur(5px);
        }}
        
        .tab-btn.active {{
            background: linear-gradient(135deg, var(--primary), var(--accent));
            border-color: transparent;
            box-shadow: 0 4px 15px rgba(56, 189, 248, 0.3);
        }}
        
        .tab-btn:hover:not(.active) {{
            background: rgba(255, 255, 255, 0.1);
        }}
        
        .course-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 1.5rem;
            display: none;
            animation: fadeIn 0.5s ease-out;
        }}
        
        .course-grid.active {{
            display: grid;
        }}
        
        .course-card {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 1.5rem;
            backdrop-filter: blur(10px);
            transition: transform 0.3s ease, border-color 0.3s ease;
            display: flex;
            flex-direction: column;
            position: relative;
            overflow: hidden;
        }}
        
        .course-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(to bottom, var(--primary), var(--accent));
            opacity: 0;
            transition: opacity 0.3s ease;
        }}
        
        .course-card:hover {{
            transform: translateY(-3px);
            border-color: rgba(255, 255, 255, 0.15);
        }}
        
        .course-card:hover::before {{
            opacity: 1;
        }}
        
        .course-subject {{
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--primary);
            margin-bottom: 0.5rem;
            font-weight: 600;
        }}
        
        .course-title {{
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 1rem;
            line-height: 1.3;
        }}
        
        .course-title a {{
            color: var(--text-color);
            text-decoration: none;
            transition: color 0.2s ease;
        }}
        
        .course-title a:hover {{
            color: var(--primary);
        }}
        
        .course-faculty {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: #cbd5e1;
            font-size: 0.95rem;
            margin-bottom: 0.5rem;
        }}
        
        .course-notes {{
            margin-top: auto;
            padding-top: 1rem;
            font-size: 0.85rem;
            color: #94a3b8;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
        }}
        
        .course-notes strong {{
            color: #f87171;
            font-weight: 600;
        }}
        
        @keyframes fadeInDown {{
            from {{ opacity: 0; transform: translateY(-20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        
        @media (max-width: 768px) {{
            h1 {{ font-size: 2.5rem; }}
            .container {{ padding: 2rem 1rem; }}
            .course-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>

<div class="container">
    <header>
        <h1>MBA Electives 2026</h1>
        <p class="subtitle">Your central hub for finding and exploring elective courses. Access schedules, overviews, and draft outlines all in one place.</p>
    </header>

    <div class="resources">
        <a href="Electives Overview 2026_UPDATED 1 June.pdf" target="_blank" class="resource-card">
            <div class="resource-icon">📄</div>
            <div class="resource-title">Electives Overview</div>
            <p style="color: #94a3b8; font-size: 0.9rem;">Updated June 1, 2026</p>
        </a>
        <a href="Electives Schedule_2026_1 JUNE.pdf" target="_blank" class="resource-card">
            <div class="resource-icon">🗓️</div>
            <div class="resource-title">Electives Schedule</div>
            <p style="color: #94a3b8; font-size: 0.9rem;">Updated June 1, 2026</p>
        </a>
    </div>

    <div class="tabs">
        <button class="tab-btn active" onclick="showTab('weekday')">Weekday Electives</button>
        <button class="tab-btn" onclick="showTab('weekend')">Weekend Electives</button>
    </div>

    <div id="weekday" class="course-grid active">
        {"".join([f'''
        <div class="course-card">
            <div class="course-subject">{c["subject"]}</div>
            <h3 class="course-title"><a href="{c["href"]}" target="_blank">{c["title"]}</a></h3>
            <div class="course-faculty">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
                {c["faculty"]}
            </div>
            {f'<div class="course-notes">{c["notes"].replace("FT MBA Only", "<strong>FT MBA Only</strong>").replace("FTMBA Only", "<strong>FT MBA Only</strong>").replace("EMBA / GEMBA Only", "<strong>EMBA/GEMBA Only</strong>")}</div>' if c["notes"] else ''}
        </div>
        ''' for c in weekday_courses])}
    </div>

    <div id="weekend" class="course-grid">
        {"".join([f'''
        <div class="course-card">
            <div class="course-subject">{c["subject"]}</div>
            <h3 class="course-title"><a href="{c["href"]}" target="_blank">{c["title"]}</a></h3>
            <div class="course-faculty">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
                {c["faculty"]}
            </div>
            {f'<div class="course-notes">{c["notes"].replace("FT MBA Only", "<strong>FT MBA Only</strong>").replace("FTMBA Only", "<strong>FT MBA Only</strong>").replace("EMBA / GEMBA Only", "<strong>EMBA/GEMBA Only</strong>").replace("EMBA/GEMBA Only", "<strong>EMBA/GEMBA Only</strong>")}</div>' if c["notes"] else ''}
        </div>
        ''' for c in weekend_courses])}
    </div>
</div>

<script>
    function showTab(tabId) {{
        // Hide all grids
        document.querySelectorAll('.course-grid').forEach(grid => {{
            grid.classList.remove('active');
        }});
        
        // Remove active class from buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {{
            btn.classList.remove('active');
        }});
        
        // Show selected grid and activate button
        document.getElementById(tabId).classList.add('active');
        event.currentTarget.classList.add('active');
    }}
</script>

</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("Generated index.html successfully.")
