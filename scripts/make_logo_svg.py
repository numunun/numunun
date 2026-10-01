#!/usr/bin/env python3
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "numunun-ascii.svg"
LOGO = [
    "███╗   ██╗██╗   ██╗███╗   ███╗██╗   ██╗███╗   ██╗██╗   ██╗███╗   ██╗",
    "████╗  ██║██║   ██║████╗ ████║██║   ██║████╗  ██║██║   ██║████╗  ██║",
    "██╔██╗ ██║██║   ██║██╔████╔██║██║   ██║██╔██╗ ██║██║   ██║██╔██╗ ██║",
    "██║╚██╗██║██║   ██║██║╚██╔╝██║██║   ██║██║╚██╗██║██║   ██║██║╚██╗██║",
    "██║ ╚████║╚██████╔╝██║ ╚═╝ ██║╚██████╔╝██║ ╚████║╚██████╔╝██║ ╚████║",
    "╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═══╝",
]
COMMANDS = [
    ("$ uname -a", "#22d3ee"),
    ("plugins · web · macOS", "#c9d1d9"),
    ("$ pwd", "#22d3ee"),
    ("/home/numunun/projects", "#c9d1d9"),
    ("$ echo $STATUS", "#22d3ee"),
    ("building_something=true", "#39d353"),
]

W, H = 370, 376
parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">',
    '<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#111722"/><stop offset="1" stop-color="#0d1117"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#bg)"/><rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="#30363d"/><line x1="0" y1="30" x2="{W}" y2="30" stroke="#30363d"/>',
]
for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{20+i*16}" cy="15" r="5" fill="{c}"/>')
parts.append(f'<text x="{W//2}" y="19" fill="#7d8590" font-size="12" text-anchor="middle">numunun@github: ~$ figlet numunun</text>')

CW = (W - 36) / len(LOGO[0])
CH = CW * 2
top = 95
for i, line in enumerate(LOGO):
    cells = []
    for j, ch in enumerate(line):
        if ch == " ":
            continue
        x, yy = 18 + j * CW, top + i * CH
        if ch == "█":
            cells.append(f'<rect x="{x:.2f}" y="{yy:.2f}" width="{CW+.3:.2f}" height="{CH+.3:.2f}" fill="#39d353"/>')
        else:
            cells.append(f'<rect x="{x+CW*.25:.2f}" y="{yy+CH*.25:.2f}" width="{CW*.6:.2f}" height="{CH*.6:.2f}" fill="#0e4429"/>')
    parts.append(f'<g opacity="0">{"".join(cells)}'
                 f'<animate attributeName="opacity" from="0" to="1" begin="{.15+i*.09:.2f}s" dur=".35s" fill="freeze"/></g>')
y = 212
for i, (line, color) in enumerate(COMMANDS):
    parts.append(f'<text x="22" y="{y}" fill="{color}" font-size="12.5" opacity="0">{html.escape(line)}'
                 f'<animate attributeName="opacity" from="0" to="1" begin="{.9+i*.12:.2f}s" dur=".35s" fill="freeze"/></text>')
    y += 22
parts.append('</svg>')
OUT.write_text(''.join(parts), encoding='utf-8')
print(f"Wrote {OUT}")
