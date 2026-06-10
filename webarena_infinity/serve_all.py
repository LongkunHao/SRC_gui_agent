#!/usr/bin/env python3
"""Launch all app servers on separate ports and serve a home page linking to each.

Usage:
    python3 serve_all.py                        # home :9000, apps :9001+
    python3 serve_all.py --test-mode            # apps start with test panel sidebar
    python3 serve_all.py --demo                 # test mode with task subset from demo_tasks.json
    python3 serve_all.py --port 8000            # custom base port
    python3 serve_all.py --host 0.0.0.0         # bind all interfaces

Local access (copy the ssh command printed at startup):
    ssh -N -L 9000:localhost:9000 -L 9001:localhost:9001 ... ec2-user@<HOST>
"""

import argparse
import http.server
import json
import os
import signal
import socketserver
import subprocess
import sys
import textwrap
from pathlib import Path

REPO_ROOT = Path(__file__).parent
APPS_DIR = REPO_ROOT / "apps"
ABLATIONS_DIR = APPS_DIR / "ablations"
SKIP_DIRS = {"app-description", "user-manuals", "ablations"}
DEMO_TASKS_PATH = REPO_ROOT / "demo_tasks.json"

# The 10 environments from the blog post, with display metadata
DEMO_APPS = {
    "handshake-career-exploration": {
        "title": "Career Exploration",
        "source": "Handshake",
        "domain": "Careers",
        "tasks": 200,
        "desc": "Browse jobs, employers, events, and career center appointments as a university student.",
    },
    "gitlab-plan-and-track": {
        "title": "Project Planning",
        "source": "GitLab",
        "domain": "DevOps",
        "tasks": 140,
        "desc": "Issue tracking, epics, milestones, iterations, Kanban boards, and label management.",
    },
    "xero-invoicing": {
        "title": "Accounting & Invoicing",
        "source": "Xero",
        "domain": "Finance",
        "tasks": 120,
        "desc": "Manage invoices, quotes, credit notes, repeating invoices, and branding themes.",
    },
    "paypal-my-wallet": {
        "title": "Personal Wallet",
        "source": "PayPal",
        "domain": "Finance",
        "tasks": 140,
        "desc": "Payment methods, multi-currency balances, crypto, debit card, rewards, and gift cards.",
    },
    "elation-clinical-records": {
        "title": "Clinical Records",
        "source": "Elation EHR",
        "domain": "Healthcare",
        "tasks": 120,
        "desc": "Patient charts, visit notes, vaccinations, vitals, problem lists, and care plans.",
    },
    "elation-prescriptions": {
        "title": "Prescription Management",
        "source": "Elation EHR",
        "domain": "Healthcare",
        "tasks": 120,
        "desc": "Prescribe medications, manage refill requests, reconcile meds, and configure Rx settings.",
    },
    "gmail": {
        "title": "Email Management",
        "source": "Gmail",
        "domain": "Productivity",
        "tasks": 60,
        "desc": "Inbox triage, labels, filters, compose, and settings for a full-featured email client.",
    },
    "gmail-accounts-and-contacts": {
        "title": "Accounts & Contacts",
        "source": "Gmail",
        "domain": "Productivity",
        "tasks": 120,
        "desc": "Contact management, labels, delegation, import/export, merge suggestions, and security.",
    },
    "superhuman-general": {
        "title": "Email Client",
        "source": "Superhuman",
        "domain": "Productivity",
        "tasks": 120,
        "desc": "Keyboard-first email with split inbox, snippets, reminders, read receipts, and calendar.",
    },
    "linear-account-settings": {
        "title": "Account Settings",
        "source": "Linear",
        "domain": "Project Mgmt",
        "tasks": 120,
        "desc": "Profile, preferences, notifications, sessions, API keys, and OAuth app management.",
    },
    "figma-slides-nodocs": {
        "title": "Slide Presentations",
        "source": "Figma",
        "domain": "Design",
        "tasks": 0,
        "desc": "Dark-themed slide editor with canvas workspace, object editing, templates, and collaboration.",
    },
}


def discover_apps():
    apps = []
    # Scan top-level apps and ablation subdirectory
    search_dirs = [APPS_DIR]
    if ABLATIONS_DIR.is_dir():
        search_dirs.append(ABLATIONS_DIR)
    for parent in search_dirs:
        for app_dir in sorted(parent.iterdir()):
            if not app_dir.is_dir() or app_dir.name in SKIP_DIRS:
                continue
            if not (app_dir / "server.py").exists() or not (app_dir / "index.html").exists():
                continue

            title = app_dir.name.replace("-", " ").title()
            desc_file = app_dir / "APP_DESCRIPTION.md"
            if desc_file.exists():
                for line in desc_file.read_text().splitlines()[:10]:
                    if line.startswith("#"):
                        raw = line.lstrip("#").strip()
                        for suffix in [" — App Description", " - App Description"]:
                            if raw.endswith(suffix):
                                raw = raw[: -len(suffix)]
                        title = raw
                        break

            task_count = 0
            tasks_file = app_dir / "real-tasks.json"
            if tasks_file.exists():
                try:
                    task_count = len(json.loads(tasks_file.read_text()))
                except Exception:
                    pass

            # Extract summary from APP_DESCRIPTION.md
            description = ""
            if desc_file.exists():
                lines = desc_file.read_text().splitlines()
                in_summary = False
                for line in lines:
                    if line.strip().lower() == "## summary":
                        in_summary = True
                        continue
                    if in_summary:
                        if line.startswith("##"):
                            break
                        stripped = line.strip()
                        if stripped:
                            description = stripped
                            break

            # Key includes ablations/ prefix for ablation apps
            if parent == ABLATIONS_DIR:
                app_key = f"ablations/{app_dir.name}"
                is_ablation = True
            else:
                app_key = app_dir.name
                is_ablation = False

            apps.append({
                "name": app_dir.name,
                "key": app_key,
                "dir": str(app_dir),
                "title": title,
                "description": description,
                "task_count": task_count,
                "is_ablation": is_ablation,
            })
    return apps


_DOMAIN_COLORS = {
    "Healthcare": "#3b82f6",
    "Productivity": "#8b5cf6",
    "Finance": "#2d9d5e",
    "Design": "#f43f8e",
    "DevOps": "#e55b5b",
    "Project Mgmt": "#6366f1",
    "Careers": "#e07c34",
}

# Display order for domain sections
_DOMAIN_ORDER = ["Productivity", "Healthcare", "Finance", "Design", "DevOps", "Project Mgmt", "Careers"]

_DOMAIN_DESCRIPTIONS = {
    "Productivity": "Email clients, contacts, and communication tools",
    "Healthcare": "Electronic health records and clinical workflows",
    "Finance": "Payments, invoicing, and accounting",
    "Design": "Creative and presentation tools",
    "DevOps": "Issue tracking and project planning",
    "Project Mgmt": "Settings and workspace configuration",
    "Careers": "Job search and career exploration",
}


def build_homepage(apps, host, base_port, demo_mode=False):
    if demo_mode:
        show_apps = [a for a in apps if a["name"] in DEMO_APPS]
        for a in show_apps:
            meta = DEMO_APPS[a["name"]]
            a["display_title"] = meta["title"]
            a["source"] = meta["source"]
            a["domain"] = meta["domain"]
    else:
        show_apps = apps
        for a in show_apps:
            a["display_title"] = a["title"]
            a["source"] = ""
            a["domain"] = ""

    total_tasks = sum(DEMO_APPS[a["name"]].get("tasks", 0) for a in show_apps if a["name"] in DEMO_APPS) if demo_mode else sum(a["task_count"] for a in show_apps)

    # Group apps by domain
    from collections import OrderedDict
    grouped = OrderedDict()
    for domain in _DOMAIN_ORDER:
        domain_apps = [a for a in show_apps if a.get("domain") == domain]
        if domain_apps:
            grouped[domain] = domain_apps
    # Catch any ungrouped
    grouped_names = {a["name"] for apps_list in grouped.values() for a in apps_list}
    ungrouped = [a for a in show_apps if a["name"] not in grouped_names]
    if ungrouped:
        grouped["Other"] = ungrouped

    def make_card(app):
        source = app.get("source", "")
        task_n = DEMO_APPS.get(app["name"], {}).get("tasks", app["task_count"])
        desc = DEMO_APPS.get(app["name"], {}).get("desc", "")
        desc_html = f'<div class="card-desc">{desc}</div>' if desc else ""
        return f"""\
          <a class="card" data-port="{app['port']}" href="#">
            <div class="card-name">{app['display_title']}</div>
            {desc_html}
            <div class="card-meta">
              <span class="source">{source}</span>
              <span class="tasks">{task_n} tasks</span>
            </div>
          </a>"""

    sections_html = []
    for domain, domain_apps in grouped.items():
        dc = _DOMAIN_COLORS.get(domain, "#6366f1")
        desc = _DOMAIN_DESCRIPTIONS.get(domain, "")
        cards = [make_card(a) for a in domain_apps]
        sections_html.append(f"""\
      <section class="domain-section">
        <div class="domain-header">
          <div class="domain-dot" style="background:{dc}"></div>
          <div class="domain-info">
            <span class="domain-name">{domain}</span>
            <span class="domain-desc">{desc}</span>
          </div>
          <span class="domain-count">{len(domain_apps)}</span>
        </div>
        <div class="card-row">
{chr(10).join(cards)}
        </div>
      </section>""")

    return textwrap.dedent(f"""\
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WebArena-Infinity</title>
    <style>
      *,*::before,*::after{{margin:0;padding:0;box-sizing:border-box}}
      body{{
        font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
        background:#fff;color:#111;
        min-height:100vh;
        display:flex;flex-direction:column;
        -webkit-font-smoothing:antialiased;
      }}

      /* Header */
      header{{
        display:grid;grid-template-columns:1fr auto 1fr;
        align-items:center;
        padding:14px 32px;
        border-bottom:1px solid #e5e5e5;
      }}
      .logo{{
        font-size:14px;font-weight:700;letter-spacing:-.02em;color:#111;
        display:flex;align-items:center;gap:8px;text-decoration:none;
      }}
      nav{{display:flex;gap:4px;justify-self:center;}}
      nav a{{
        font-size:12px;font-weight:500;color:#888;text-decoration:none;
        padding:5px 14px;border-radius:6px;transition:all .15s;
      }}
      nav a:hover{{color:#111;background:#f5f5f5;}}
      nav a.active{{color:#111;background:#f0f0f0;font-weight:600;}}
      .logo-mark{{
        width:20px;height:20px;border-radius:5px;
        background:#111;color:#fff;
        display:flex;align-items:center;justify-content:center;
        font-size:10px;font-weight:800;
      }}
      .header-right{{
        display:flex;gap:20px;align-items:center;justify-self:end;
        font-size:11px;color:#999;
      }}
      .header-right .stat{{font-weight:600;color:#555}}
      .pill{{
        padding:3px 10px;border-radius:100px;
        background:#f0fdf4;color:#16a34a;
        font-weight:600;font-size:10px;
      }}

      /* Main */
      main{{
        flex:1;
        max-width:960px;width:100%;margin:0 auto;
        padding:24px 32px 20px;
      }}
      .page-title{{
        font-size:16px;font-weight:700;color:#111;
        letter-spacing:-.02em;margin-bottom:1px;
      }}
      .page-sub{{
        font-size:11.5px;color:#999;margin-bottom:22px;
      }}

      /* Domain sections */
      .domain-section{{
        margin-bottom:18px;
      }}
      .domain-header{{
        display:flex;align-items:center;gap:8px;
        margin-bottom:8px;
      }}
      .domain-dot{{
        width:8px;height:8px;border-radius:50%;flex-shrink:0;
      }}
      .domain-info{{
        flex:1;display:flex;align-items:baseline;gap:8px;
      }}
      .domain-name{{
        font-size:12px;font-weight:700;color:#222;
      }}
      .domain-desc{{
        font-size:10.5px;color:#aaa;font-weight:400;
      }}
      .domain-count{{
        font-size:10px;color:#bbb;font-weight:500;
        background:#f5f5f5;padding:1px 7px;border-radius:8px;
      }}

      /* Card row — wrapping grid */
      .card-row{{
        display:flex;flex-wrap:wrap;gap:10px;
      }}

      /* Cards — fixed width, don't stretch */
      .card{{
        width:210px;flex-shrink:0;
        background:#fafafa;
        border:1px solid #ebebeb;
        border-radius:10px;
        padding:16px 16px 14px;
        text-decoration:none;color:inherit;
        display:flex;flex-direction:column;
        transition:border-color .15s,box-shadow .15s,background .15s;
        cursor:pointer;
      }}
      .card:hover{{
        border-color:#ccc;
        box-shadow:0 2px 12px rgba(0,0,0,.06);
        background:#fff;
      }}
      .card-name{{
        font-size:13px;font-weight:650;color:#111;
        line-height:1.3;letter-spacing:-.01em;
        margin-bottom:6px;
      }}
      .card-desc{{
        font-size:10.5px;color:#888;line-height:1.45;
        display:-webkit-box;-webkit-line-clamp:2;
        -webkit-box-orient:vertical;overflow:hidden;
        flex:1;
      }}
      .card-meta{{
        display:flex;align-items:center;justify-content:space-between;
        margin-top:12px;
        padding-top:10px;
        border-top:1px solid #eee;
      }}
      .source{{
        font-size:10px;color:#aaa;
      }}
      .tasks{{
        font-size:10px;color:#bbb;font-weight:500;
      }}

      /* Footer */
      footer{{
        text-align:center;padding:12px 24px;
        border-top:1px solid #f0f0f0;
        font-size:10px;color:#bbb;
      }}

      @media(max-width:640px){{
        .card-row{{flex-direction:column;}}
        main{{padding:16px;}}
        header{{padding:12px 16px;}}
      }}
    </style>
    </head>
    <body>

    <header>
      <a class="logo" href="https://webarena.dev/webarena-infinity">
        <div class="logo-mark">W</div>
        WebArena-Infinity
      </a>
      <nav>
        <a href="/" class="active">Environments</a>
        <a href="/reports">Agent Reports</a>
      </nav>
      <div class="header-right">
        <span><span class="stat">{len(show_apps)}</span> environments</span>
        <span><span class="stat">{total_tasks:,}</span> tasks</span>
        <span class="pill">Live</span>
      </div>
    </header>

    <main>
      <div class="page-title">Environments</div>
      <div class="page-sub">Click any environment to explore. Each includes a test panel with sample tasks.</div>
{chr(10).join(sections_html)}
    </main>

    <footer>WebArena-Infinity</footer>

    <script>
      document.querySelectorAll('.card[data-port]').forEach(function(a){{
        a.href=location.protocol+'//'+location.hostname+':'+a.dataset.port;
        a.target='_blank';
      }});
    </script>
    </body>
    </html>""")


# --- Agent results data (from final_results.md) ---
# env key -> report filename (matches reports-static/{model}/{env_key}.html)
_ENV_REPORT_KEYS = {
    "Clinical Records": "elation-clinical-records",
    "Prescription Mgmt": "elation-prescriptions",
    "Personal Wallet": "paypal-my-wallet",
    "Accounting & Invoicing": "xero-invoicing",
    "Email Management": "gmail",
    "Account Settings": "linear-account-settings",
    "Project Planning": "gitlab-plan-and-track",
    "Accounts & Contacts": "gmail-accounts-and-contacts",
    "Career Exploration": "handshake-career-exploration",
    "Email Client": "superhuman-general",
}

_AGENT_RESULTS = {
    "Gemini 3 Flash w/ Browser Use": {
        "key": "gemini", "total_score": "873/1,260", "total_rate": "69.3%",
        "envs": [
            ("Personal Wallet", "PayPal", "124/140", "88.6%"),
            ("Clinical Records", "Elation EHR", "98/120", "81.7%"),
            ("Prescription Mgmt", "Elation EHR", "97/120", "80.8%"),
            ("Accounting & Invoicing", "Xero", "97/120", "80.8%"),
            ("Email Management", "Gmail", "45/60", "75.0%"),
            ("Account Settings", "Linear", "88/120", "73.3%"),
            ("Project Planning", "GitLab", "89/140", "63.6%"),
            ("Accounts & Contacts", "Gmail", "74/120", "61.7%"),
            ("Career Exploration", "Handshake", "101/200", "50.5%"),
            ("Email Client", "Superhuman", "60/120", "50.0%"),
        ],
    },
    "Qwen-3.5-Plus": {
        "key": "qwen", "total_score": "608/1,260", "total_rate": "48.3%",
        "envs": [
            ("Personal Wallet", "PayPal", "100/140", "71.4%"),
            ("Account Settings", "Linear", "79/120", "65.8%"),
            ("Email Management", "Gmail", "34/60", "56.7%"),
            ("Accounting & Invoicing", "Xero", "67/120", "55.8%"),
            ("Clinical Records", "Elation EHR", "65/120", "54.2%"),
            ("Career Exploration", "Handshake", "101/200", "50.5%"),
            ("Prescription Mgmt", "Elation EHR", "50/120", "41.7%"),
            ("Project Planning", "GitLab", "52/140", "37.1%"),
            ("Accounts & Contacts", "Gmail", "40/120", "33.3%"),
            ("Email Client", "Superhuman", "31/120", "25.8%"),
        ],
    },
    "Kimi-k2.5": {
        "key": "kimi", "total_score": "545/1,260", "total_rate": "43.3%",
        "envs": [
            ("Personal Wallet", "PayPal", "99/140", "70.7%"),
            ("Email Management", "Gmail", "42/60", "70.0%"),
            ("Account Settings", "Linear", "65/120", "54.2%"),
            ("Accounting & Invoicing", "Xero", "63/120", "52.5%"),
            ("Career Exploration", "Handshake", "100/200", "50.0%"),
            ("Clinical Records", "Elation EHR", "60/120", "50.0%"),
            ("Accounts & Contacts", "Gmail", "48/120", "40.0%"),
            ("Project Planning", "GitLab", "55/140", "39.3%"),
            ("Prescription Mgmt", "Elation EHR", "28/120", "23.3%"),
            ("Email Client", "Superhuman", "18/120", "15.0%"),
        ],
    },
}


def build_reports_page():
    """Build the agent reports HTML page."""
    agent_sections = []
    for agent_name, data in _AGENT_RESULTS.items():
        rows = []
        model_key = data["key"]
        for env_name, source, score, rate in data["envs"]:
            pct = float(rate.rstrip("%"))
            bar_color = "#16a34a" if pct >= 60 else "#eab308" if pct >= 40 else "#dc2626"
            env_key = _ENV_REPORT_KEYS.get(env_name, "")
            report_link = f' <a class="r-link" href="/reports-static/{model_key}/{env_key}.html" target="_blank">report</a>' if env_key else ""
            rows.append(f"""\
            <tr>
              <td class="r-env">{env_name} <span class="r-src">{source}</span>{report_link}</td>
              <td class="r-score">{score}</td>
              <td class="r-rate">
                <div class="r-bar-bg"><div class="r-bar" style="width:{pct}%;background:{bar_color}"></div></div>
                <span>{rate}</span>
              </td>
            </tr>""")

        agent_sections.append(f"""\
      <div class="agent-card">
        <div class="agent-header">
          <span class="agent-name">{agent_name}</span>
          <span class="agent-total">{data['total_score']} &middot; {data['total_rate']}</span>
        </div>
        <table class="r-table">
          <thead><tr><th>Environment</th><th>Score</th><th>Pass Rate</th></tr></thead>
          <tbody>
{''.join(rows)}
          </tbody>
        </table>
      </div>""")

    return textwrap.dedent(f"""\
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WebArena-Infinity &middot; Agent Reports</title>
    <style>
      *,*::before,*::after{{margin:0;padding:0;box-sizing:border-box}}
      body{{
        font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
        background:#fff;color:#111;min-height:100vh;
        display:flex;flex-direction:column;
        -webkit-font-smoothing:antialiased;
      }}
      header{{
        display:grid;grid-template-columns:1fr auto 1fr;
        align-items:center;
        padding:14px 32px;border-bottom:1px solid #e5e5e5;
      }}
      .logo{{font-size:14px;font-weight:700;letter-spacing:-.02em;color:#111;display:flex;align-items:center;gap:8px;text-decoration:none;}}
      .logo-mark{{width:20px;height:20px;border-radius:5px;background:#111;color:#fff;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:800;}}
      nav{{display:flex;gap:4px;justify-self:center;}}
      nav a{{
        font-size:12px;font-weight:500;color:#888;text-decoration:none;
        padding:5px 14px;border-radius:6px;transition:all .15s;
      }}
      nav a:hover{{color:#111;background:#f5f5f5;}}
      nav a.active{{color:#111;background:#f0f0f0;font-weight:600;}}

      main{{flex:1;max-width:960px;width:100%;margin:0 auto;padding:24px 32px 20px;}}
      .page-title{{font-size:16px;font-weight:700;color:#111;letter-spacing:-.02em;margin-bottom:1px;}}
      .page-sub{{font-size:11.5px;color:#999;margin-bottom:22px;}}

      .agents{{display:flex;flex-direction:column;gap:20px;}}
      .agent-card{{
        border:1px solid #ebebeb;border-radius:10px;overflow:hidden;
      }}
      .agent-header{{
        display:flex;align-items:center;justify-content:space-between;
        padding:12px 16px;background:#fafafa;border-bottom:1px solid #ebebeb;
      }}
      .agent-name{{font-size:13px;font-weight:700;color:#111;}}
      .agent-total{{font-size:12px;font-weight:600;color:#555;}}

      .r-table{{width:100%;border-collapse:collapse;font-size:11.5px;}}
      .r-table th{{
        text-align:left;padding:7px 16px;font-size:10px;font-weight:600;
        color:#999;text-transform:uppercase;letter-spacing:.04em;
        border-bottom:1px solid #f0f0f0;
      }}
      .r-table td{{padding:6px 16px;border-bottom:1px solid #f8f8f8;}}
      .r-table tr:last-child td{{border-bottom:none;}}
      .r-table tr:hover{{background:#fafafa;}}
      .r-env{{font-weight:500;color:#222;}}
      .r-src{{font-weight:400;color:#aaa;font-size:10px;}}
      .r-link{{font-size:10px;color:#6366f1;text-decoration:none;font-weight:500;margin-left:6px;}}
      .r-link:hover{{text-decoration:underline;}}
      .r-score{{color:#666;font-weight:500;white-space:nowrap;}}
      .r-rate{{display:flex;align-items:center;gap:8px;white-space:nowrap;}}
      .r-bar-bg{{width:60px;height:6px;background:#f0f0f0;border-radius:3px;overflow:hidden;flex-shrink:0;}}
      .r-bar{{height:100%;border-radius:3px;}}

      footer{{text-align:center;padding:12px 24px;border-top:1px solid #f0f0f0;font-size:10px;color:#bbb;}}
      @media(max-width:640px){{main{{padding:16px;}}header{{padding:12px 16px;}}}}
    </style>
    </head>
    <body>
    <header>
      <a class="logo" href="https://webarena.dev/webarena-infinity">
        <div class="logo-mark">W</div>
        WebArena-Infinity
      </a>
      <nav>
        <a href="/">Environments</a>
        <a href="/reports" class="active">Agent Reports</a>
      </nav>
    </header>
    <main>
      <div class="page-title">Agent Reports</div>
      <div class="page-sub">Final evaluation results (3 repetitions, merged). Sorted by pass rate per agent.</div>
      <div class="agents">
{chr(10).join(agent_sections)}
      </div>
    </main>
    <footer>WebArena-Infinity</footer>
    </body>
    </html>""")


class HomeHandler(http.server.BaseHTTPRequestHandler):
    html = ""
    reports_html = ""
    app_count = 0

    def do_GET(self):
        if self.path == "/api/health":
            body = json.dumps({"status": "ok", "apps": self.app_count}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif self.path == "/reports":
            body = self.reports_html.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif self.path.startswith("/reports-static/"):
            # Serve static report HTML files
            rel = self.path[len("/reports-static/"):]
            fpath = REPO_ROOT / "reports-static" / rel
            if fpath.is_file() and fpath.suffix == ".html":
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Transfer-Encoding", "chunked")
                self.end_headers()
                with open(fpath, "rb") as f:
                    while True:
                        chunk = f.read(65536)
                        if not chunk:
                            break
                        self.wfile.write(f"{len(chunk):x}\r\n".encode())
                        self.wfile.write(chunk)
                        self.wfile.write(b"\r\n")
                self.wfile.write(b"0\r\n\r\n")
            else:
                self.send_error(404)
        else:
            body = self.html.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    def log_message(self, format, *args):
        pass


def main():
    parser = argparse.ArgumentParser(description="Launch all Mirror-Mirror app servers")
    parser.add_argument("--port", type=int, default=9000, help="Base port (home page); apps get port+1, port+2, ... (default: 9000)")
    parser.add_argument("--host", default="localhost", help="Bind address (default: localhost)")
    parser.add_argument("--test-mode", action="store_true", help="Start app servers with in-browser test panel")
    parser.add_argument("--demo", action="store_true", help="Test mode with task subset from demo_tasks.json")
    parser.add_argument("--demo-tasks", type=str, default=str(DEMO_TASKS_PATH),
                        help=f"Path to demo task config (default: {DEMO_TASKS_PATH})")
    args = parser.parse_args()

    # --demo implies --test-mode
    if args.demo:
        args.test_mode = True

    # Load demo task config if in demo mode
    demo_config = {}
    if args.demo:
        demo_path = Path(args.demo_tasks)
        if demo_path.exists():
            with open(demo_path) as f:
                demo_config = json.load(f)
            # Remove non-task keys like _comment
            demo_config = {k: v for k, v in demo_config.items() if not k.startswith("_")}
            print(f"Demo mode: loaded task config from {demo_path}")
        else:
            print(f"WARNING: demo tasks file not found: {demo_path}, using all tasks")


    apps = discover_apps()
    if not apps:
        print("No apps found in apps/")
        sys.exit(1)

    # In demo mode, only start the 10 blog-post environments
    if args.demo:
        apps = [a for a in apps if a["name"] in DEMO_APPS]

    processes = []

    def cleanup(sig=None, frame=None):
        print(f"\nStopping {len(processes)} servers...")
        for p in processes:
            try:
                p.terminate()
            except OSError:
                pass
        for p in processes:
            try:
                p.wait(timeout=3)
            except subprocess.TimeoutExpired:
                p.kill()
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    # Start each app server
    print(f"Starting {len(apps)} app servers...")
    for i, app in enumerate(apps):
        port = args.port + 1 + i
        app["port"] = port
        cmd = [sys.executable, "server.py", "--port", str(port)]

        # Build env: inherit current env, add demo task filter if applicable
        env = os.environ.copy()
        task_ids = demo_config.get(app["key"], []) if demo_config else []

        # Only enable test mode if there are tasks to show
        demo_meta = DEMO_APPS.get(app["name"], {})
        has_tasks = demo_meta.get("tasks", 0) > 0 if args.demo else True
        if args.test_mode and has_tasks:
            cmd.append("--test-mode")
        if task_ids:
            env["MM_DEMO_TASKS"] = ",".join(task_ids)

        proc = subprocess.Popen(
            cmd,
            cwd=app["dir"],
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        processes.append(proc)
        suffix = f" ({len(task_ids)} demo tasks)" if task_ids else ""
        print(f"  :{port}  {app['title']}{suffix}")

    # Build and serve home page + reports page
    html = build_homepage(apps, args.host, args.port, demo_mode=args.demo)
    HomeHandler.html = html
    HomeHandler.reports_html = build_reports_page()
    HomeHandler.app_count = len(apps)

    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.TCPServer((args.host, args.port), HomeHandler)

    host_display = args.host if args.host != "0.0.0.0" else "localhost"
    last_port = args.port + len(apps)

    # Print SSH tunnel command
    ports = " ".join(f"-L {p}:localhost:{p}" for p in range(args.port, last_port + 1))
    print(f"\nServing at http://{host_display}:{args.port}")
    if args.demo:
        print("Demo mode: enabled (test panel with task subset)")
    elif args.test_mode:
        print("Test mode: enabled")
    print(f"\nSSH tunnel (run on your local machine):")
    print(f"  ssh -N {ports} -i ~/.ssh/mirror-mirror.pem ec2-user@<HOST>")
    print(f"\nPress Ctrl+C to stop.\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        cleanup()


if __name__ == "__main__":
    main()
