import os
import re

css_styles = """
<head>
  <title> Lichess Bot Leaderboard </title>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Raleway">
  <link rel="stylesheet" href="/css/site.css">
  <link rel="icon" href="https://raw.githubusercontent.com/TheYoBots/libot-lb/master/images/favicon.ico" type="image/x-icon" />
</head>
"""

page_nav_html = """
<body>
  <div id="pageNav">
    <button id="backBtn" class="nav-btn" aria-label="Go back" title="Back">
      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M15 18l-6-6 6-6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
    </button>
    <a href="/" class="nav-link" id="homeBtn" aria-label="Home" title="Home">
      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M3 9.5L12 3l9 6.5V21a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1V9.5z" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>
    </a>
  </div>
  <button id="themeToggle" aria-pressed="false" title="Toggle light / dark" aria-label="Toggle theme"></button>
  <main>
    <div class="card">
"""

closing_main_and_footer = """
    </div>
  </main>
"""

footer_styles = """
<footer class="page-footer">
  <p>
    <a href="https://github.com/TheYoBots/libot-lb">
      <img class="github-logo" src="https://github.com/fluidicon.png" alt="GitHub Icon">
    </a>
    Made by <a href="https://github.com/TheYoBots">Yohaan Seth Nathan</a>
  </p>
</footer>
"""

# Dictionary for filename display name mapping - O(1) lookup instead of multiple conditionals
FILENAME_DISPLAY_MAP = {
    "chess960.md": "chess 960.md",
    "threeCheck.md": "three-check.md",
    "kingOfTheHill.md": "king of the hill.md",
    "racingKings.md": "racing kings.md"
}

# Pre-compile regex patterns for better performance
SEPARATOR_RE = re.compile(r'^\s*-+\s*\|\s*-+\s*\|\s*-+')
CELL_SPLIT_RE = re.compile(r'\s*\|\s*')

def generate_h1_tag(filename):
    title = os.path.splitext(filename)[0].capitalize()
    return f'<h1>{title} Leaderboard</h1>'

def markdown_table_to_html(markdown_table):
    raw_rows = [r.strip() for r in markdown_table.split('\n') if r.strip()]
    rows = [r for r in raw_rows if not SEPARATOR_RE.search(r)]

    if not rows:
        return '<table class="w3-table w3-striped"></table>'

    html_parts = ['<table class="w3-table w3-striped">']

    header_cells = CELL_SPLIT_RE.split(rows[0])
    html_parts.append('  <thead>')
    html_parts.append('    <tr>')
    for cell in header_cells:
        html_parts.append(f'      <th>{cell}</th>')
    html_parts.append('    </tr>')
    html_parts.append('  </thead>')

    html_parts.append('  <tbody>')
    for row in rows[1:]:
        cells = CELL_SPLIT_RE.split(row)
        html_parts.append('    <tr>')
        for cell in cells:
            cell = cell.strip()
            if cell.startswith('@'):
                username = cell[1:]
                cell_html = f'<td><a href="https://lichess.org/@/{username}">{cell}</a></td>'
            else:
                cell_html = f'<td>{cell}</td>'
            html_parts.append(f'      {cell_html}')
        html_parts.append('    </tr>')
    html_parts.append('  </tbody>')

    html_parts.append('</table>')
    return '\n'.join(html_parts)

directories = ['bot_leaderboard', 'unrestricted_bot_leaderboard']

for directory in directories:
    for filename in os.listdir(directory):
        if filename.endswith('.md'):
            with open(os.path.join(directory, filename), 'r') as md_file:
                # Use dictionary lookup with default fallback
                display_filename = FILENAME_DISPLAY_MAP.get(filename, filename)
                h1_tag = generate_h1_tag(display_filename)

                markdown_table = md_file.read()
                html_table = markdown_table_to_html(markdown_table)

                styled_html_table = css_styles + page_nav_html + h1_tag + html_table + closing_main_and_footer + footer_styles + "\n<script src=\"/js/theme.js\" defer></script>\n</body>\n"

                html_filename = os.path.splitext(filename)[0] + '.html'
                with open(os.path.join(directory, html_filename), 'w') as html_file:
                    html_file.write(styled_html_table)
