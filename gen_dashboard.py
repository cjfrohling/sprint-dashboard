#!/usr/bin/env python3
import html
import subprocess

COLORS = ['#5c6bc0','#26a69a','#ef5350','#ff7043','#66bb6a','#42a5f5','#ab47bc','#8d6e63','#26c6da']
assignee_color_map = {}
color_index = [0]

def get_color(name):
    if name not in assignee_color_map:
        assignee_color_map[name] = COLORS[color_index[0] % len(COLORS)]
        color_index[0] += 1
    return assignee_color_map[name]

def initials(name):
    parts = name.split()
    if len(parts) >= 2:
        return parts[0][0].upper() + parts[-1][0].upper()
    return name[:2].upper()

def priority_color(p):
    return {'Highest':'#c62828','High':'#e64a19','Medium':'#455a64','Low':'#2e7d32'}.get(p,'#455a64')

in_progress = [
    {"key":"WPD-4359","summary":"Claude Sprint 78","assignee":"Nageswara Rao Recharla","priority":"Medium"},
    {"key":"WPD-4403","summary":"[FE] Dry Run of Launch","assignee":"Chris Schultz","priority":"Highest"},
    {"key":"WPD-4357","summary":"Claude Sprint 78","assignee":"Ganesh Abothula","priority":"Medium"},
    {"key":"WPD-4356","summary":"Claude Sprint 78","assignee":"Lenin johnson","priority":"Medium"},
    {"key":"WPD-4346","summary":"[Prod] JP - Press Release filtering does not work for By Product category","assignee":"Ganesh Abothula","priority":"Medium"},
    {"key":"WPD-4360","summary":"Claude Sprint 78","assignee":"Swetha Kalluri","priority":"Medium"},
    {"key":"WPD-4353","summary":"[FE] Component Distribution Approach with AI (Claude) (Due July 3rd)","assignee":"Nick Karch","priority":"Highest"},
    {"key":"WPD-4454","summary":"[QA Env] WPD4112_bug7 Filtering: Results of UI and LSCS query do not match","assignee":"Krishna Kodicherla","priority":"Medium"},
    {"key":"WPD-4364","summary":"[CRITICAL] [QA Env] Blogs QA | Homepage - Issues in Performance, Accessibility, w3c validator scans","assignee":"Chris Schultz","priority":"High"},
    {"key":"WPD-4434","summary":"(ot.digital) Enablement production push","assignee":"Nageswara Rao Recharla","priority":"Medium"},
    {"key":"WPD-4287","summary":"[BE] Evaluate Fix for longer translations","assignee":"Krishna Kodicherla","priority":"Highest"},
    {"key":"WPD-4451","summary":"[QA Env] Blogs | Database bloat is still higher than expected","assignee":"Chris Schultz","priority":"High"},
    {"key":"WPD-3963","summary":"[Dev QA] | solutions.ot.com | fr | homepage, information mgmt, predictive maintenance page | iPhone | In \"Contact Us\" form the mobile number field not optimized for 10-digit number","assignee":"Jean Alexandre","priority":"Medium"},
    {"key":"WPD-4352","summary":"[FE] Component Distribution Approach with AI (Claude) (Due July 3rd)","assignee":"Chris Schultz","priority":"Highest"},
    {"key":"WPD-4358","summary":"Claude Sprint 78","assignee":"Krishna Kodicherla","priority":"Medium"},
    {"key":"WPD-3655","summary":"[FE] Global Font Change to accommodate for longer translations ","assignee":"Nick Karch","priority":"Highest"},
    {"key":"WPD-3899","summary":"[FE][BP2] Apply new color and typography tokens to tooltip component ","assignee":"Chris Schultz","priority":"Medium"},
    {"key":"WPD-3593","summary":"(Apps) Search results updates","assignee":"Lenin johnson","priority":"Medium"},
    {"key":"WPD-4237","summary":"[Content] (C19 Update) Marquee on Homepage Blip Resolution","assignee":"Jenny Luke","priority":"Medium"},
    {"key":"WPD-4381","summary":"[FE] Social Share capability ","assignee":"Chris Schultz","priority":"Medium"},
]

blocked = [
    {"key":"WPD-4257","summary":"[WEB CMS] Create new skin for SaaS navigation ","assignee":"Jenny Luke","priority":"Highest","block_reason":""},
    {"key":"WPD-4380","summary":"Remove Analytics tag from Customer Story landing page filtering option","assignee":"Krishna Kodicherla","priority":"High","block_reason":""},
    {"key":"WPD-4288","summary":"[WEB CMS] Customer Story DCR update script for logo revamp","assignee":"Krishna Kodicherla","priority":"Medium","block_reason":""},
    {"key":"WPD-3902","summary":"[FE] Dynamic Footer + Header","assignee":"Nick Karch","priority":"High","block_reason":""},
    {"key":"WPD-4078","summary":"[WEB CMS] New C44.5 Variant ","assignee":"Ganesh Abothula","priority":"High","block_reason":""},
    {"key":"WPD-4323","summary":"[DMTH] - changes to publish workflow","assignee":"Srinivas Jayaram Rao","priority":"Medium","block_reason":""},
    {"key":"WPD-4206","summary":"[FE][BP2] Research for Prefixing tailwind classes","assignee":"Nick Karch","priority":"High","block_reason":""},
]

qa_in_progress = [
    {"key":"WPD-4111","summary":"[CS Datasource] Develop utility to auto-update feed JSON","assignee":"Srinivas Jayaram Rao","priority":"Medium"},
]

ready_for_production = [
]
worklogs_by_author = {
    "Ganesh Abothula": [
        {"key":"WPD-4346","summary":"[Prod] JP - Press Release filtering does not work for By Product category","timeSpent":"2h"},
        {"key":"WPD-4466","summary":"[QA Env] WPD4112_bug8 Generic, Partner, Ot trusts Ot not displayed in Cards nor is displayed when sorted via filter","timeSpent":"4h"},
        {"key":"WPD-4467","summary":"[QA Env] WPD4112_bug9 Missing Reset button/hyperlink","timeSpent":"2h"},
    ],
    "Nick Karch": [
        {"key":"WPD-4353","summary":"[FE] Component Distribution Approach with AI (Claude) (Due July 3rd)","timeSpent":"7m"},
    ],
    "Krishna Kodicherla": [
        {"key":"WPD-4454","summary":"[QA Env] WPD4112_bug7 Filtering: Results of UI and LSCS query do not match","timeSpent":"4h"},
        {"key":"WPD-4454","summary":"[QA Env] WPD4112_bug7 Filtering: Results of UI and LSCS query do not match","timeSpent":"4h"},
    ],
    "Patrick Galego": [
        {"key":"WPD-4445","summary":"[UX] Review the 7 prototype pages and deliver UX recommendations (Due July 7th)","timeSpent":"6h"},
    ],
}

# Pre-seed color map in a consistent order
for t in in_progress + blocked + qa_in_progress:
    get_color(t['assignee'])
for a in worklogs_by_author:
    get_color(a)

def card_html(t):
    name = t['assignee'] or 'Unassigned'
    color = get_color(name)
    init = initials(name)
    pc = priority_color(t['priority'])
    key = t['key']
    # summary already escaped if needed (& handled above), escape the rest
    summary = t['summary']
    priority = t['priority']
    return f"""        <div class="card">
          <div class="card-key"><a href="https://opentexthq.atlassian.net/browse/{key}" target="_blank" rel="noopener">{key}</a></div>
          <div class="card-summary">{summary}</div>
          <div class="card-meta">
            <div class="avatar" style="background:{color}" title="{html.escape(name)}">{init}</div>
            <span class="assignee-name">{html.escape(name)}</span>
            <span class="priority-badge" style="background:{pc}">{priority}</span>
          </div>
        </div>"""

def column_html(icon, title, tickets, col_class, empty_msg):
    count = len(tickets)
    if tickets:
        body = "\n".join(card_html(t) for t in tickets)
    else:
        body = f'        <div class="empty-col">{empty_msg}</div>'
    return f"""      <div class="column {col_class}">
        <div class="col-header">
          <span>{icon} {title}</span>
          <span class="col-count">{count}</span>
        </div>
        <div class="col-body">
{body}
        </div>
      </div>"""

def worklog_person_html(author, entries):
    color = get_color(author)
    init = initials(author)
    rows = ""
    for e in entries:
        key = e['key']
        summary = html.escape(e['summary'])
        time = html.escape(e['timeSpent'])
        rows += f"""              <div class="worklog-entry">
                <div class="worklog-key"><a href="https://opentexthq.atlassian.net/browse/{key}" target="_blank" rel="noopener">{key}</a></div>
                <div class="worklog-summary">{summary}</div>
                <div class="worklog-time">{time}</div>
              </div>\n"""
    return f"""          <div class="worklog-person">
            <div class="worklog-person-header">
              <div class="worklog-avatar" style="background:{color}">{init}</div>
              <span class="worklog-person-name">{html.escape(author)}</span>
            </div>
            <div class="worklog-entries">
{rows}            </div>
          </div>"""

board = "\n".join([
    column_html("🥾","In Progress", in_progress, "col-in-progress",""),
    column_html("🪨","Blocked", blocked, "col-blocked",""),
    column_html("🔭","QA In Progress", qa_in_progress, "col-qa",""),
    column_html("🏔️","Ready for Prod", ready_for_production, "col-ready",
                "🌨️ The summit is clear. No tickets waiting for production."),
])

if worklogs_by_author:
    wl_cards = "\n".join(worklog_person_html(a, e) for a, e in worklogs_by_author.items())
    worklog_body = f'        <div class="worklog-grid">\n{wl_cards}\n        </div>'
else:
    worklog_body = '        <div class="no-worklog">🌲 No time logged on Monday, Jun 29 2026.</div>'

now_str = subprocess.check_output(['date', '+%Y-%m-%d %H:%M MDT']).decode().strip()

html_out = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>&#x26F0;&#xFE0F; Trail Status Dashboard &mdash; WPD</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: #1a2f3a;
      color: #d4e3ec;
      min-height: 100vh;
    }}

    /* HERO */
    .hero {{
      background: linear-gradient(135deg, #0d1b2a 0%, #1a3a5c 40%, #2d5a8e 75%, #3d7a9e 100%);
      position: relative;
      overflow: hidden;
      padding: 44px 32px 0;
      text-align: center;
    }}
    .hero-content {{ position: relative; z-index: 1; padding-bottom: 12px; }}
    .hero h1 {{ font-size: 2.5rem; font-weight: 700; color: #e8f4f8; letter-spacing: -0.5px; }}
    .hero .subtitle {{ color: #a8d0e6; margin-top: 8px; font-size: 0.95rem; }}
    .hero .badge {{
      display: inline-block; margin-top: 12px; padding: 4px 16px;
      background: rgba(168,208,230,0.15); border: 1px solid rgba(168,208,230,0.35);
      border-radius: 20px; color: #a8d0e6; font-size: 0.8rem;
    }}
    .hero svg {{ display: block; width: 100%; margin-top: -8px; }}

    /* STATS BAR */
    .stats-bar {{
      background: #2d4a5e; padding: 14px 32px;
      display: flex; gap: 14px; justify-content: center; flex-wrap: wrap;
    }}
    .stat-box {{
      text-align: center; padding: 12px 28px;
      background: rgba(0,0,0,0.25); border-radius: 8px; min-width: 130px;
    }}
    .stat-box .count {{ font-size: 2.1rem; font-weight: 700; line-height: 1; }}
    .stat-box .label {{ font-size: 0.77rem; color: #8b9ba8; margin-top: 4px; }}
    .c-ip {{ color: #5b8fa8; }} .c-bl {{ color: #e57373; }}
    .c-qa {{ color: #e8a838; }} .c-rp {{ color: #81c784; }}

    /* BOARD */
    .board {{
      padding: 22px 20px; display: grid;
      grid-template-columns: repeat(4, 1fr); gap: 18px;
      max-width: 1700px; margin: 0 auto;
    }}
    @media (max-width: 1150px) {{ .board {{ grid-template-columns: repeat(2,1fr); }} }}
    @media (max-width: 640px)  {{ .board {{ grid-template-columns: 1fr; }} }}

    .column {{ display: flex; flex-direction: column; }}
    .col-header {{
      padding: 10px 14px; border-radius: 8px 8px 0 0;
      font-weight: 600; font-size: 0.84rem;
      display: flex; align-items: center; justify-content: space-between;
    }}
    .col-count {{
      background: rgba(255,255,255,0.22); border-radius: 12px;
      padding: 1px 9px; font-size: 0.73rem;
    }}
    .col-body {{
      border: 2px solid; border-top: none;
      border-radius: 0 0 8px 8px; overflow: hidden; flex: 1;
    }}
    .col-in-progress .col-header {{ background: #2471a3; }}
    .col-in-progress .col-body   {{ border-color: #5b8fa8; }}
    .col-blocked .col-header     {{ background: #c0392b; }}
    .col-blocked .col-body       {{ border-color: #e57373; }}
    .col-qa .col-header          {{ background: #d68910; }}
    .col-qa .col-body            {{ border-color: #e8a838; }}
    .col-ready .col-header       {{ background: #1e8449; }}
    .col-ready .col-body         {{ border-color: #81c784; }}

    /* CARDS */
    .card {{
      padding: 9px 12px;
      border-bottom: 1px solid rgba(255,255,255,0.06);
      background: #1e3545; transition: background 0.15s;
    }}
    .card:last-child {{ border-bottom: none; }}
    .card:hover {{ background: #253f52; }}
    .card-key a {{
      color: #a8d0e6; text-decoration: none;
      font-size: 0.74rem; font-weight: 600;
    }}
    .card-key a:hover {{ text-decoration: underline; }}
    .card-summary {{ color: #c8dde8; font-size: 0.81rem; margin: 3px 0 0; line-height: 1.35; }}
    .card-meta {{
      display: flex; align-items: center; gap: 5px;
      margin-top: 7px; flex-wrap: wrap;
    }}
    .avatar {{
      width: 18px; height: 18px; border-radius: 50%;
      display: flex; align-items: center; justify-content: center;
      font-size: 0.54rem; font-weight: 700; color: #fff; flex-shrink: 0;
    }}
    .assignee-name {{ font-size: 0.71rem; color: #8b9ba8; }}
    .priority-badge {{
      font-size: 0.64rem; font-weight: 600; padding: 1px 6px;
      border-radius: 3px; color: #fff; margin-left: auto;
    }}
    .empty-col {{
      padding: 24px 14px; text-align: center;
      color: #8b9ba8; font-size: 0.82rem; font-style: italic;
      background: #1e3545;
    }}

    /* WORKLOG */
    .worklog-section {{
      max-width: 1700px; margin: 6px auto 28px; padding: 0 20px;
    }}
    .worklog-header {{
      background: #2e5944; padding: 12px 18px;
      border-radius: 8px 8px 0 0;
      font-weight: 600; font-size: 0.88rem; color: #a8d8b0;
    }}
    .worklog-body {{
      background: #1e3545; border: 2px solid #2e5944;
      border-top: none; border-radius: 0 0 8px 8px; padding: 16px;
    }}
    .worklog-grid {{
      display: flex; flex-wrap: wrap; gap: 14px;
    }}
    .worklog-person {{
      flex: 1 1 310px; background: #243e50;
      border-radius: 8px; overflow: hidden;
    }}
    .worklog-person-header {{
      display: flex; align-items: center; gap: 10px;
      padding: 10px 14px; background: rgba(0,0,0,0.18);
      border-bottom: 1px solid rgba(255,255,255,0.07);
    }}
    .worklog-avatar {{
      width: 28px; height: 28px; border-radius: 50%;
      display: flex; align-items: center; justify-content: center;
      font-size: 0.68rem; font-weight: 700; color: #fff;
    }}
    .worklog-person-name {{ font-weight: 600; font-size: 0.84rem; color: #c8dde8; }}
    .worklog-entries {{ padding: 4px 0; }}
    .worklog-entry {{
      display: grid; grid-template-columns: 88px 1fr 68px;
      gap: 8px; padding: 6px 14px;
      border-bottom: 1px solid rgba(255,255,255,0.04);
      align-items: start;
    }}
    .worklog-entry:last-child {{ border-bottom: none; }}
    .worklog-key a {{
      color: #a8d0e6; text-decoration: none;
      font-size: 0.73rem; font-weight: 600;
    }}
    .worklog-key a:hover {{ text-decoration: underline; }}
    .worklog-summary {{ font-size: 0.77rem; color: #8b9ba8; line-height: 1.3; }}
    .worklog-time {{ font-size: 0.74rem; color: #c9a86c; font-weight: 600; text-align: right; }}
    .no-worklog {{ padding: 20px; text-align: center; color: #8b9ba8; font-style: italic; }}

    /* FOOTER */
    footer {{
      text-align: center; padding: 16px;
      color: #8b9ba8; font-size: 0.74rem;
      border-top: 1px solid #2d4a5e; margin-top: 8px;
    }}
  </style>
</head>
<body>

  <!-- HERO -->
  <header class="hero">
    <div class="hero-content">
      <h1>&#x26F0;&#xFE0F; Trail Status Dashboard</h1>
      <div class="subtitle">Web Programs Development &middot; June 30, 2026 &middot; opentexthq.atlassian.net</div>
      <span class="badge">&#x1F3D5;&#xFE0F; Current Sprint Only &middot; WPD</span>
    </div>
    <svg viewBox="0 0 1440 120" preserveAspectRatio="none">
      <path d="M0,90 L80,60 L150,80 L250,30 L340,70 L420,20 L500,60 L580,40 L660,75 L740,10 L820,55 L900,35 L980,65 L1060,15 L1140,50 L1220,30 L1320,70 L1440,40 L1440,120 L0,120 Z" fill="#1a3a5c" opacity="0.6"/>
      <path d="M0,110 L60,85 L120,100 L200,60 L280,95 L380,50 L460,80 L520,65 L620,95 L700,40 L800,75 L880,55 L960,90 L1040,45 L1140,80 L1220,55 L1320,85 L1440,65 L1440,120 L0,120 Z" fill="#152535"/>
      <path d="M700,40 L720,18 L740,40 Z" fill="#fff" opacity="0.9"/>
    </svg>
  </header>

  <!-- STATS BAR -->
  <div class="stats-bar">
    <div class="stat-box">
      <div class="count c-ip">{len(in_progress)}</div>
      <div class="label">&#x1F97E; In Progress</div>
    </div>
    <div class="stat-box">
      <div class="count c-bl">{len(blocked)}</div>
      <div class="label">&#x1FAA8; Blocked</div>
    </div>
    <div class="stat-box">
      <div class="count c-qa">{len(qa_in_progress)}</div>
      <div class="label">&#x1F52D; QA In Progress</div>
    </div>
    <div class="stat-box">
      <div class="count c-rp">{len(ready_for_production)}</div>
      <div class="label">&#x1F3D4;&#xFE0F; Ready for Prod</div>
    </div>
  </div>

  <!-- BOARD -->
  <div class="board">
{board}
  </div>

  <!-- WORKLOG -->
  <div class="worklog-section">
    <div class="worklog-header">&#x1F332; Time Logged &mdash; Last Business Day &nbsp;&#x1F4C5; Monday, Jun 29 2026</div>
    <div class="worklog-body">
{worklog_body}
    </div>
  </div>

  <!-- FOOTER -->
  <footer>
    &#x26F0;&#xFE0F; Trail Status Dashboard &middot; Current Sprint &middot; WPD &middot; Time logged: last business day &middot; Generated {html.escape(now_str)}
  </footer>

</body>
</html>"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_out)

print("index.html written successfully")
