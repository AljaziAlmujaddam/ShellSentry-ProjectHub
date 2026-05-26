#!/usr/bin/env python3
"""
Regenerate multi-page site from a single-page index.html (all sections in one file).
After splitting, run: python3 merge_pages.py
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

NAV_ITEMS = [
    ("index.html", "Home", "home"),
    ("overview.html", "Overview", "overview"),
    ("features.html", "Features", "features"),
    ("methodology.html", "Methodology", "methodology"),
    ("architecture.html", "Architecture", "architecture"),
    ("in-action.html", "In&nbsp;Action", "in-action"),
    ("findings.html", "Findings", "findings"),
    ("conclusion.html", "Conclusion", "conclusion"),
    ("deliverables.html", "Deliverables", "deliverables"),
    ("team.html", "Team", "team"),
]

# Standalone section files (before merge_pages.py combines them)
SECTION_IDS = [
    "abstract",
    "about",
    "objectives",
    "features",
    "security",
    "methodology",
    "architecture",
    "workflow",
    "stack",
    "in-action",
    "findings",
    "conclusion",
    "deliverables",
    "team",
]

PAGE_TITLES = {
    "home": "ShellSentry | Senior Project Website",
    "abstract": "Abstract | ShellSentry",
    "about": "Project Overview | ShellSentry",
    "objectives": "Project Objectives | ShellSentry",
    "features": "Key Features | ShellSentry",
    "methodology": "Methodology | ShellSentry",
    "security": "Security Features | ShellSentry",
    "architecture": "System Architecture | ShellSentry",
    "workflow": "Interactive Workflow | ShellSentry",
    "stack": "Technology Stack | ShellSentry",
    "in-action": "In Action | ShellSentry",
    "findings": "Key Findings | ShellSentry",
    "conclusion": "Conclusion | ShellSentry",
    "deliverables": "Project Deliverables | ShellSentry",
    "team": "Project Team | ShellSentry",
}


def extract_sections(html: str) -> dict[str, str]:
    sections = {}
    for sid in SECTION_IDS:
        pattern = rf'(<section id="{re.escape(sid)}"[^>]*>.*?</section>)'
        match = re.search(pattern, html, re.DOTALL)
        if not match:
            raise SystemExit(f"Missing section: {sid}")
        sections[sid] = match.group(1)
    return sections


def patch_section_links(section_html: str) -> str:
    return section_html.replace('href="#workflow"', 'href="./architecture.html#workflow"')


def nav_html(current: str) -> str:
    lines = ['          <ul class="nav-links" id="primary-nav-links">']
    for href, label, page_id in NAV_ITEMS:
        attrs = ' aria-current="page"' if page_id == current else ""
        lines.append(f'            <li><a href="./{href}"{attrs}>{label}</a></li>')
    lines.append("          </ul>")
    return "\n".join(lines)


def footer_links_html() -> str:
    return "\n".join(
        f'          <a href="./{href}">{"Home" if pid == "home" else label.replace("&nbsp;", " ")}</a>'
        for href, label, pid in NAV_ITEMS
    )


def institutional_header() -> str:
    return """        <div class="institutional-header">
          <div
            class="institutional-brand"
            role="group"
            aria-label="University affiliation"
          >
            <img
              class="uob-logo"
              src="./images/uob-logo.png"
              alt="University of Bahrain official emblem"
              width="444"
              height="514"
              decoding="async"
            />
            <div class="institutional-text">
              <p class="inst-name">University of Bahrain</p>
              <p class="inst-college">College of Information Technology</p>
              <p class="inst-department">Department of Information Systems</p>
            </div>
          </div>
        </div>"""


def nav_block(current: str) -> str:
    return f"""        <nav class="nav" aria-label="Primary">
          <div class="nav-head">
            <h1 class="brand"><a href="./index.html" class="brand-link">ShellSentry</a></h1>
            <button
              type="button"
              class="nav-toggle"
              id="nav-menu-toggle"
              aria-expanded="false"
              aria-controls="primary-nav-links"
            >
              <span class="nav-toggle-bars" aria-hidden="true">
                <span></span>
                <span></span>
                <span></span>
              </span>
              <span class="sr-only">Menu</span>
            </button>
          </div>
{nav_html(current)}
        </nav>"""


def head_html(title: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <meta
      name="description"
      content="ShellSentry is a secure web platform that translates natural language into validated Bash commands for remote SSH execution."
    />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Sora:wght@500;600;700;800&display=swap"
      rel="stylesheet"
    />
    <link rel="icon" href="./images/shellsentry-logo.png" type="image/png" />
    <link rel="apple-touch-icon" href="./images/shellsentry-logo.png" />
    <link rel="stylesheet" href="./styles.css" />
  </head>
"""


def footer_html() -> str:
    return f"""    <footer class="footer">
      <div class="container footer-wrap">
        <div class="footer-meta">
          <p>
            &copy; ShellSentry Secure Natural Language To Bash Execution 2026. All
            rights reserved.
          </p>
          <p>
            <a href="mailto:info@shellsentry.site">info@shellsentry.site</a>
          </p>
        </div>
        <div class="footer-links">
{footer_links_html()}
        </div>
        <div class="footer-social">
        </div>
        <a class="back-top" href="#top" aria-label="Back to top">↑ Top</a>
      </div>
    </footer>

    <script src="./script.js"></script>
  </body>
</html>
"""


def hero_html() -> str:
    return f"""    <header class="hero" id="top">
      <div class="container hero-header-stack">
{institutional_header()}
{nav_block("home")}
      </div>
      <div class="hero-orbs" aria-hidden="true">
        <span class="orb orb-1"></span>
        <span class="orb orb-2"></span>
        <span class="orb orb-3"></span>
        <span class="orb orb-4"></span>
        <span class="orb orb-5"></span>
      </div>

      <div class="hero-content container reveal">
        <div class="hero-grid">
          <div>
            <span class="tag">Cybersecurity + AI Graduation Project</span>
            <h2>Secure Natural Language to Bash Execution</h2>
            <p>
              ShellSentry helps users run Linux administration tasks on remote
              machines by converting plain English requests into safe, validated
              Bash commands.
            </p>
            <div class="hero-command">
              <span class="dot"></span>
              <span class="dot"></span>
              <span class="dot"></span>
              <code>$ "Check disk usage on all servers" -> df -h</code>
            </div>
            <div class="hero-actions">
              <a class="btn" href="./architecture.html">View Architecture</a>
              <a class="btn btn-outline" href="./team.html">Team</a>
            </div>
            <div class="hero-metrics">
              <div class="metric">
                <span class="metric-value">7</span>
                <span class="metric-label">Execution Stages</span>
              </div>
              <div class="metric">
                <span class="metric-value">2</span>
                <span class="metric-label">Validation Layers</span>
              </div>
              <div class="metric">
                <span class="metric-value">100%</span>
                <span class="metric-label">Security Focused</span>
              </div>
            </div>
          </div>
          <aside class="hero-dashboard floaty">
            <div class="dashboard-header">
              <span class="dash-dot"></span>
              <span class="dash-dot"></span>
              <span class="dash-dot"></span>
              <p>AI Command Execution Console</p>
            </div>
            <div class="dashboard-row">
              <span class="label">Request</span>
              <code>Analyze listening ports and suggest hardening.</code>
            </div>
            <div class="dashboard-row">
              <span class="label">Generated</span>
              <code>ss -tlnp && ufw status verbose</code>
            </div>
            <div class="dashboard-status">
              <div><span>Validation</span><strong>Passed</strong></div>
              <div><span>Risk Score</span><strong>Low</strong></div>
              <div><span>Target</span><strong>3 Servers</strong></div>
            </div>
            <div class="dashboard-log">
              <p>&gt; Sanitizer check complete...</p>
              <p>&gt; Policy checker approved command.</p>
              <p>&gt; SSH execution completed in 2.4s.</p>
            </div>
          </aside>
        </div>
      </div>
    </header>"""


def site_header(current: str) -> str:
    return f"""    <header class="site-header" id="top">
      <div class="container hero-header-stack">
{institutional_header()}
{nav_block(current)}
      </div>
    </header>"""


def build_home() -> str:
    return "".join(
        [
            head_html(PAGE_TITLES["home"]),
            '  <body class="page-home">\n',
            hero_html(),
            "\n\n",
            footer_html(),
        ]
    )


def build_inner(current: str, section_html: str) -> str:
    return (
        head_html(PAGE_TITLES.get(current, "ShellSentry"))
        + '  <body class="page-inner">\n'
        + site_header(current)
        + "\n    <main>\n      "
        + section_html
        + "\n    </main>\n\n"
        + footer_html()
    )


def main() -> None:
    source = (ROOT / "index.html").read_text(encoding="utf-8")
    if '<section id="abstract"' not in source:
        raise SystemExit(
            "index.html has no sections. Restore a single-page index with all <section> blocks."
        )

    sections = extract_sections(source)

    for sid in SECTION_IDS:
        filename = "in-action.html" if sid == "in-action" else f"{sid}.html"
        section = patch_section_links(sections[sid])
        (ROOT / filename).write_text(build_inner(sid, section), encoding="utf-8")
        print(f"Wrote {filename}")

    (ROOT / "index.html").write_text(build_home(), encoding="utf-8")
    print("Wrote index.html")

    merge = ROOT / "merge_pages.py"
    if merge.exists():
        subprocess.run([sys.executable, str(merge)], check=True)


if __name__ == "__main__":
    main()
