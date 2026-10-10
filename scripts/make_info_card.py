#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from theme import *

OUT = Path(__file__).resolve().parent.parent / "info-card.svg"

# ("kv", 라벨, 값) / ("sec", 섹션 제목) / ("gap",) 빈 줄
ROWS = [
    ("host",),
    ("kv", "Focus", "Minecraft Plugins, Web, macOS"),
    ("kv", "OS", "macOS (Apple Silicon)"),
    ("gap",),
    ("sec", "Stack"),
    ("kv", "Plugin", "Paper API, ProtocolLib, Gradle"),
    ("kv", "Web", "Next.js, React, Tailwind CSS"),
    ("kv", "Backend", "Supabase (PostgreSQL, RLS)"),
    ("kv", "Desktop", "Swift, SwiftPM, AppKit"),
    ("kv", "Deploy", "Vercel, GitHub Actions"),
    ("gap",),
    ("sec", "Languages"),
    ("kv", "Code", "Kotlin, TypeScript, JavaScript, Java, Swift, C"),
    ("kv", "Tools", "Git, VS Code, IntelliJ IDEA"),
]
PALETTE = ["#484f58", "#ff7b72", "#3fb950", "#d29922", "#58a6ff", "#bc8cff", "#39c5cf", "#e6edf3"]

W, H = 490, 376
p = window(W, H, f"{USER}@github: ~$ neofetch")

y, i = 60, 0
for row in ROWS:
    kind = row[0]
    if kind == "gap":
        y += 9
        continue
    if kind == "host":
        line_x = 20 + int((len(USER) + 7) * 8.6) + 14
        inner = (f'<text x="20" y="{y}" font-size="14" font-weight="700"><tspan fill="{GREEN}">{USER}</tspan>'
                 f'<tspan fill="{MUTED}">@</tspan><tspan fill="{CYAN}">github</tspan></text>'
                 f'<line x1="{line_x}" y1="{y-4}" x2="{W-20}" y2="{y-4}" stroke="{BORDER}" stroke-dasharray="2 3"/>')
    elif kind == "sec":
        inner = f'<text x="20" y="{y}" fill="{BLUE}" font-size="12.5" font-weight="700">— {esc(row[1])}</text>'
    else:
        inner = (f'<text x="20" y="{y}" fill="{ORANGE}" font-size="12.5" font-weight="700">{esc(row[1])}</text>'
                 f'<text x="112" y="{y}" fill="{MUTED}" font-size="12.5">:</text>'
                 f'<text x="124" y="{y}" fill="{TEXT}" font-size="12.5">{esc(row[2])}</text>')
    p.append(fade_in(inner, .15 + i * .055, dy=5))
    y += 20.5
    i += 1

# neofetch 하단 색상 블록
y += 2
blocks = "".join(f'<rect x="{20 + k*26}" y="{y}" width="22" height="12" rx="2" fill="{c}"/>' for k, c in enumerate(PALETTE))
p.append(fade_in(blocks, .15 + i * .055, dy=5))
p.append('</svg>')
OUT.write_text("".join(p), encoding="utf-8")
print(f"Wrote {OUT} (blocks at y={y}, card height {H})")
