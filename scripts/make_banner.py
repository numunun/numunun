#!/usr/bin/env python3
"""맨 위 배너(banner.svg): 빛나는 픽셀 로고 + 타이핑되는 소개 문구."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from theme import *

ROOT = Path(__file__).resolve().parent.parent

# 여기 문구만 바꾸면 된다. 한 줄씩 차례로 타이핑되고 계속 반복된다.
TAGLINES = [
    "building Minecraft plugins with Kotlin",
    "shipping web apps on Next.js + Supabase",
    "hacking on tiny macOS tools in Swift",
]

LOGO = [
    "███╗   ██╗██╗   ██╗███╗   ███╗██╗   ██╗███╗   ██╗██╗   ██╗███╗   ██╗",
    "████╗  ██║██║   ██║████╗ ████║██║   ██║████╗  ██║██║   ██║████╗  ██║",
    "██╔██╗ ██║██║   ██║██╔████╔██║██║   ██║██╔██╗ ██║██║   ██║██╔██╗ ██║",
    "██║╚██╗██║██║   ██║██║╚██╔╝██║██║   ██║██║╚██╗██║██║   ██║██║╚██╗██║",
    "██║ ╚████║╚██████╔╝██║ ╚═╝ ██║╚██████╔╝██║ ╚████║╚██████╔╝██║ ╚████║",
    "╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═══╝",
]

W, H = 860, 226
CW, CH = 9.6, 17
LX = (W - len(LOGO[0]) * CW) / 2
LY = 58

defs = (f'<linearGradient id="logo" gradientUnits="userSpaceOnUse" x1="{LX}" y1="0" x2="{LX+len(LOGO[0])*CW}" y2="0">'
        f'<stop offset="0" stop-color="{GREEN}"/><stop offset=".55" stop-color="{CYAN}"/><stop offset="1" stop-color="{PURPLE}"/>'
        f'<animate attributeName="x1" values="{LX};{LX-400};{LX}" dur="8s" repeatCount="indefinite"/>'
        f'<animate attributeName="x2" values="{LX+len(LOGO[0])*CW};{LX+len(LOGO[0])*CW+400};{LX+len(LOGO[0])*CW}" dur="8s" repeatCount="indefinite"/></linearGradient>'
        f'<filter id="glow" x="-10%" y="-30%" width="120%" height="160%"><feGaussianBlur stdDeviation="3.5" result="b"/>'
        f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
        f'<pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#1f2630"/></pattern>'
        f'<clipPath id="reveal"><rect x="{LX}" y="{LY-4}" width="0" height="{CH*6+8}">'
        f'<animate attributeName="width" from="0" to="{len(LOGO[0])*CW+4}" begin=".2s" dur="1.2s" fill="freeze" calcMode="spline" keySplines=".3 .7 .2 1" keyTimes="0;1"/></rect></clipPath>')

p = window(W, H, f"{USER}@github: ~ — zsh", defs)
p.append(f'<rect x="1" y="31" width="{W-2}" height="{H-32}" fill="url(#dots)"/>')

face, shade = [], []
for i, line in enumerate(LOGO):
    for j, ch in enumerate(line):
        if ch == " ":
            continue
        x, y = LX + j * CW, LY + i * CH
        if ch == "█":
            face.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{CW+.4:.1f}" height="{CH+.4:.1f}"/>')
        else:
            shade.append(f'<rect x="{x+CW*.2:.1f}" y="{y+CH*.2:.1f}" width="{CW*.6:.1f}" height="{CH*.6:.1f}"/>')
p.append(f'<g clip-path="url(#reveal)"><g fill="#1b4d3a">{"".join(shade)}</g>'
         f'<g fill="url(#logo)" filter="url(#glow)">{"".join(face)}</g></g>')

# 스캔라인 한 줄이 로고를 훑고 지나감
p.append(f'<rect x="{LX-10}" y="{LY}" width="{len(LOGO[0])*CW+20}" height="2" fill="{CYAN}" opacity=".0">'
         f'<animate attributeName="y" values="{LY};{LY+CH*6};{LY+CH*6}" keyTimes="0;.25;1" dur="5s" begin="1.6s" repeatCount="indefinite"/>'
         f'<animate attributeName="opacity" values=".5;.5;0" keyTimes="0;.25;.26" dur="5s" begin="1.6s" repeatCount="indefinite"/></rect>')

# 타이핑 줄: 각 문구가 쳐지고 → 잠깐 머물고 → 지워진다
TY = H - 42
PROMPT = f"{USER} ~ $ "
CHW = 8.4                      # 14px 고정폭 글자 폭(textLength로 고정)
px = (W - (len(PROMPT) + max(map(len, TAGLINES))) * CHW) / 2
tx = px + len(PROMPT) * CHW
p.append(f'<text y="{TY}" font-size="14" font-weight="700">'
         f'<tspan x="{px:.1f}" fill="{GREEN}">{USER}</tspan>'
         f'<tspan x="{px + (len(USER)+1)*CHW:.1f}" fill="{MUTED}">~</tspan>'
         f'<tspan x="{px + (len(USER)+3)*CHW:.1f}" fill="{CYAN}">$</tspan></text>')

per = 4.5
total = per * len(TAGLINES)
for i, line in enumerate(TAGLINES):
    L = len(line) * CHW
    a = i * per / total
    t = lambda s: round(a + s / total, 4)
    # 0→1.6s 한 글자씩 타이핑, 3.6s까지 정지, 4.2s까지 지우기
    steps = len(line)
    vals, times = ["0", "0"], ["0", f"{t(0)}"]
    for s in range(1, steps + 1):
        vals.append(f"{s*CHW:.1f}"); times.append(f"{t(1.6*s/steps)}")
    vals.append(f"{L:.1f}"); times.append(f"{t(3.6)}")
    for s in range(steps - 1, -1, -1):
        vals.append(f"{s*CHW:.1f}"); times.append(f"{t(3.6 + .6*(steps-s)/steps)}")
    vals.append("0"); times.append("1")
    p.append(f'<clipPath id="t{i}"><rect x="{tx:.1f}" y="{TY-16}" height="22" width="0">'
             f'<animate attributeName="width" values="{";".join(vals)}" keyTimes="{";".join(times)}" '
             f'dur="{total}s" repeatCount="indefinite" calcMode="discrete"/></rect></clipPath>')
    p.append(f'<text x="{tx:.1f}" y="{TY}" font-size="14" fill="{BRIGHT}" textLength="{L:.1f}" clip-path="url(#t{i})">{esc(line)}</text>')
    # 커서
    p.append(f'<rect y="{TY-13}" width="8" height="16" fill="{GREEN}" opacity="0">'
             f'<animate attributeName="x" values="{";".join(f"{tx+float(v):.1f}" for v in vals)}" keyTimes="{";".join(times)}" '
             f'dur="{total}s" repeatCount="indefinite" calcMode="discrete"/>'
             f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;{t(0)};{t(4.3)};{min(t(4.3)+.0001,1)};1" '
             f'dur="{total}s" repeatCount="indefinite" calcMode="discrete"/></rect>')

p.append('</svg>')
(ROOT / "banner.svg").write_text("".join(p), encoding="utf-8")
print("Wrote banner.svg")