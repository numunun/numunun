#!/usr/bin/env python3
"""neofetch 스타일 정보 카드(info-card.svg)를 만든다. 내용은 아래 ROWS만 고치면 된다."""
import html
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "info-card.svg"
USER = "numunun"

# ("kv", 왼쪽 라벨, 오른쪽 값) / ("sec", 섹션 제목) / ("gap",) 빈 줄
ROWS = [
    ("host",),
    ("kv", "Focus", "Minecraft Plugins, Web, macOS"),
    ("kv", "OS", "macOS (Apple Silicon)"),
    ("gap",),
    ("sec", "Stack"),
    ("kv", "Plugin", "Paper API, ProtocolLib, Gradle"),
    ("kv", "Frontend", "Next.js, React, Tailwind CSS"),
    ("kv", "Backend", "Supabase (PostgreSQL, RLS)"),
    ("kv", "Desktop", "Swift, SwiftPM, AppKit"),
    ("kv", "Deploy", "Vercel, GitHub Actions"),
    ("gap",),
    ("sec", "Languages"),
    ("kv", "Code", "Kotlin, TypeScript, JavaScript, Swift, C"),
    ("gap",),
    ("sec", "Tools"),
    ("kv", "Dev", "Git, GitHub, IntelliJ IDEA"),
]

W, H = 490, 376
parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">',
    '<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#111722"/><stop offset="1" stop-color="#0d1117"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#bg)"/><rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="#30363d"/><line x1="0" y1="30" x2="{W}" y2="30" stroke="#30363d"/>',
]
for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{20+i*16}" cy="15" r="5" fill="{c}"/>')
parts.append(f'<text x="{W//2}" y="19" fill="#7d8590" font-size="12" text-anchor="middle">{USER}@github: ~$ neofetch</text>')

y = 60
for i, row in enumerate(ROWS):
    kind = row[0]
    if kind == "gap":
        y += 10
        continue
    if kind == "host":
        line_x = 20 + int((len(USER) + 7) * 8.6) + 14
        inner = (f'<text x="20" y="{y}" font-size="14" font-weight="700"><tspan fill="#3fb950">{USER}</tspan>'
                 f'<tspan fill="#7d8590">@</tspan><tspan fill="#22d3ee">github</tspan></text>'
                 f'<line x1="{line_x}" y1="{y-4}" x2="{W-20}" y2="{y-4}" stroke="#30363d"/>')
    elif kind == "sec":
        inner = f'<text x="20" y="{y}" fill="#58a6ff" font-size="12.5" font-weight="700">— {html.escape(row[1])}</text>'
    else:
        inner = (f'<text x="20" y="{y}" fill="#ffa657" font-size="12.5" font-weight="700">{html.escape(row[1])}</text>'
                 f'<text x="124" y="{y}" fill="#c9d1d9" font-size="12.5">{html.escape(row[2])}</text>')
    delay = .15 + i * .055
    parts.append(f'<g opacity="0" transform="translate(0,5)">{inner}'
                 f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur=".4s" fill="freeze"/>'
                 f'<animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" begin="{delay:.2f}s" dur=".4s" fill="freeze"/></g>')
    y += 20.5

parts.append('</svg>')
OUT.write_text(''.join(parts), encoding='utf-8')
print(f"Wrote {OUT} (last row y={y-20.5:.0f}, card height {H})")
