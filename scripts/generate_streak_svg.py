#!/usr/bin/env python3

import datetime, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from theme import *

ROOT = Path(__file__).resolve().parent.parent
data = json.loads((ROOT / "data" / "profile.json").read_text(encoding="utf-8"))
days = data["days"]

MAX_WEEKS = 53

MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
CELL, GAP, LEFT, TOP = 12, 3, 56, 84
last = datetime.date.fromisoformat(days[-1]["date"])
first = last - datetime.timedelta(days=(last.weekday() + 1) % 7 + (MAX_WEEKS - 1) * 7)
days = [d for d in days if datetime.date.fromisoformat(d["date"]) >= first]
start = datetime.date.fromisoformat(days[0]["date"])
offset = (start.weekday() + 1) % 7
weeks = (offset + len(days) + 6) // 7
W = 860
H = TOP + 7 * (CELL + GAP) + 42

p = window(W, H, f"{USER}@github: ~$ git log --graph --since='1 year ago'")
p.append(f'<style>'
         f'.c{{transform-box:fill-box;transform-origin:center;opacity:0;animation:pop .5s ease-out both}}'
         f'.g{{animation:pop .5s ease-out both,glow .9s ease-out both}}'
         f'@keyframes pop{{0%{{opacity:0;transform:scale(.1)}}60%{{opacity:1;transform:scale(1.15)}}100%{{opacity:1;transform:scale(1)}}}}'
         f'@keyframes glow{{0%,40%{{filter:brightness(2.6)}}100%{{filter:brightness(1)}}}}'
         f'@media (prefers-reduced-motion:reduce){{.c{{opacity:1!important;animation:none!important}}}}'
         f'</style>')

# 위쪽 요약 줄
p.append(f'<text x="22" y="52" font-size="13" fill="{MUTED}"><tspan fill="{GREEN}" font-weight="700">{data["total"]:,}</tspan>'
         f' contributions · <tspan fill="{CYAN}" font-weight="700">{data["active_days"]}</tspan> active days in the last year</text>')

last_month = None
for w in range(weeks):
    d = start + datetime.timedelta(days=w * 7 - offset)
    if d.month != last_month:
        if last_month is None and d.day > 8:   # 첫 달이 잘려 있으면 라벨 생략
            last_month = d.month
            continue
        last_month = d.month
        p.append(f'<text x="{LEFT + w*(CELL+GAP)}" y="{TOP-8}" fill="{MUTED}" font-size="11">{MONTHS[d.month-1]}</text>')
for name, row in [("Mon", 1), ("Wed", 3), ("Fri", 5)]:
    p.append(f'<text x="22" y="{TOP + row*(CELL+GAP) + CELL - 2}" fill="{MUTED}" font-size="11">{name}</text>')

max_order = weeks + 6 * .55
for i, d in enumerate(days):
    k = i + offset
    w, r = k // 7, k % 7
    x, y = LEFT + w * (CELL + GAP), TOP + r * (CELL + GAP)
    delay = round((w + r * .55) / max_order * 2.8, 3)
    cls = "c g" if d["level"] else "c"
    tip = f'{d["count"]} on {d["date"]}'
    p.append(f'<rect class="{cls}" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" fill="{HEAT[d["level"]]}" style="animation-delay:{delay}s"><title>{tip}</title></rect>')

# 오늘 칸 표시 (깜빡이는 테두리)
k = len(days) - 1 + offset
tx, ty = LEFT + (k // 7) * (CELL + GAP), TOP + (k % 7) * (CELL + GAP)
p.append(f'<rect x="{tx-1.5}" y="{ty-1.5}" width="{CELL+3}" height="{CELL+3}" rx="3.5" fill="none" stroke="{CYAN}" stroke-width="1.2">'
         f'<animate attributeName="opacity" values="1;.15;1" dur="1.6s" repeatCount="indefinite"/></rect>')

# 아래 범례
ly = H - 20
p.append(f'<text x="22" y="{ly}" fill="{MUTED}" font-size="11">best day · <tspan fill="{ORANGE}">{data["best_day"]["count"]}</tspan> on {data["best_day"]["date"].replace("-", ".")}</text>')
lx = W - 22 - 5 * 15 - 70
p.append(f'<text x="{lx}" y="{ly}" fill="{MUTED}" font-size="11">Less</text>')
for i, c in enumerate(HEAT):
    p.append(f'<rect x="{lx + 34 + i*15}" y="{ly-10}" width="12" height="12" rx="2.5" fill="{c}"/>')
p.append(f'<text x="{lx + 34 + 5*15 + 4}" y="{ly}" fill="{MUTED}" font-size="11">More</text>')
p.append('</svg>')

out = sys.argv[2] if len(sys.argv) > 2 else str(ROOT / "contrib-heatmap.svg")
Path(out).write_text("".join(p), encoding="utf-8")
print(f"Wrote {out}")