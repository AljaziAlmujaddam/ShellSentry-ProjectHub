#!/usr/bin/env python3
"""Merge sections into combined pages and update site navigation."""

import re
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

PAGE_TITLES = {
    "home": "ShellSentry | Senior Project Website",
    "overview": "Project Overview | ShellSentry",
    "features": "Features & Security | ShellSentry",
    "methodology": "Methodology & Stack | ShellSentry",
    "architecture": "Architecture & Workflow | ShellSentry",
    "in-action": "In Action | ShellSentry",
    "findings": "Key Findings | ShellSentry",
    "conclusion": "Conclusion | ShellSentry",
    "deliverables": "Project Deliverables | ShellSentry",
    "team": "Project Team | ShellSentry",
}

REMOVE_FILES = [
    "abstract.html",
    "about.html",
    "objectives.html",
    "security.html",
    "stack.html",
    "workflow.html",
]

COMBINED = {
    "overview.html": ("overview", ["abstract.html", "about.html", "objectives.html"]),
    "features.html": ("features", ["features.html", "security.html"]),
    "methodology.html": ("methodology", ["methodology.html", "stack.html"]),
    "architecture.html": ("architecture", ["architecture.html", "workflow.html"]),
}


def extract_main_section(path: Path) -> str:
    html = path.read_text(encoding="utf-8")
    match = re.search(r"<main>\s*(.*?)\s*</main>", html, re.DOTALL)
    if not match:
        raise SystemExit(f"No <main> in {path}")
    return match.group(1).strip()


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


def build_inner(current: str, main_body: str) -> str:
    return (
        head_html(PAGE_TITLES[current])
        + f'  <body class="page-inner">\n'
        + f'    <header class="site-header" id="top">\n'
        + f'      <div class="container hero-header-stack">\n'
        + institutional_header()
        + "\n"
        + nav_block(current)
        + "\n"
        + "      </div>\n"
        + "    </header>\n"
        + "    <main>\n"
        + main_body
        + "\n    </main>\n\n"
        + footer_html()
    )


def patch_internal_links(html: str) -> str:
    html = html.replace('href="./workflow.html"', 'href="./architecture.html#workflow"')
    html = html.replace('href="#workflow"', 'href="./architecture.html#workflow"')
    return html


def patch_nav_footer(html: str, current: str) -> str:
    html = patch_internal_links(html)
    html = re.sub(r"<title>.*?</title>", f"<title>{PAGE_TITLES.get(current, 'ShellSentry')}</title>", html, count=1)
    html = re.sub(
        r'\s*<ul class="nav-links" id="primary-nav-links">.*?</ul>',
        "\n" + nav_html(current),
        html,
        count=1,
        flags=re.DOTALL,
    )
    html = re.sub(
        r'<div class="footer-links">\s*.*?\s*</div>',
        f"<div class=\"footer-links\">\n{footer_links_html()}\n        </div>",
        html,
        count=1,
        flags=re.DOTALL,
    )
    return html


def build_home() -> str:
    hero_match = re.search(
        r'(<header class="hero".*?</header>)',
        (ROOT / "index.html").read_text(encoding="utf-8"),
        re.DOTALL,
    )
    if not hero_match:
        raise SystemExit("index.html missing hero")
    hero = hero_match.group(1)
    parts = [
        head_html(PAGE_TITLES["home"]),
        '  <body class="page-home">\n',
        hero,
        "\n\n",
        footer_html(),
    ]
    html = "".join(parts)
    return patch_nav_footer(html, "home")


def main() -> None:
    for outfile, (current, sources) in COMBINED.items():
        paths = [ROOT / src for src in sources]
        if not all(p.exists() for p in paths):
            print(f"Skip {outfile} (source files missing)")
            continue
        sections = [extract_main_section(p) for p in paths]
        main_body = "\n\n      ".join(sections)
        (ROOT / outfile).write_text(
            patch_internal_links(build_inner(current, main_body)), encoding="utf-8"
        )
        print(f"Wrote {outfile}")

    for f in REMOVE_FILES:
        p = ROOT / f
        if p.exists():
            p.unlink()
            print(f"Removed {f}")

    for path in sorted(ROOT.glob("*.html")):
        if path.name == "index.html":
            continue
        page_id = path.stem
        if page_id == "in-action":
            page_id = "in-action"
        current = page_id if any(pid == page_id for _, _, pid in NAV_ITEMS) else None
        if current:
            path.write_text(patch_nav_footer(path.read_text(encoding="utf-8"), current), encoding="utf-8")
            print(f"Updated {path.name}")

    (ROOT / "index.html").write_text(build_home(), encoding="utf-8")
    print("Updated index.html")


if __name__ == "__main__":
    main()
