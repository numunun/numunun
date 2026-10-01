#!/usr/bin/env python3
import datetime, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from theme import *

ROOT = Path(__file__).resolve().parent.parent
data = json.loads((ROOT / "data" / "profile.json").read_text(encoding="utf-8"))
today = data["today"]

LANG_COLORS = {
    "Kotlin": "#A97BFF", "TypeScript": "#3178c6", "JavaScript": "#f1e05a", "Swift": "#F05138",
    "C": "#a8b9cc", "HTML": "#e34c26", "CSS": "#663399", "Python": "#3572A5", "Java": "#b07219",
    "Shell": "#89e051", "PLpgSQL": "#336790", "Objective-C": "#438eff", "Rust": "#dea584",
}


def fmt(d):
    if not d:
        return "—"
    if d == today:
        return "Today"
    dt = datetime.date.fromisoformat(d)
    return dt.strftime("%m.%d") if dt.year == int(today[:4]) else dt.strftime("%Y.%m.%d")


def rng(s, current=False):
    if not s["start"]:
        return "no streak yet"
    end = "Present" if current else fmt(s["end"])  # 현재 스트릭은 항상 오늘(KST)까지 이어진 것
    return f'{fmt(s["start"])} → {end}' if (current or s["start"] != s["end"]) else fmt(s["start"])


cur, best = data["current_streak"], data["longest_streak"]
tiles = [
    ("TOTAL", f'{data["total"]:,}', "contributions · 1y", GREEN),
    ("CURRENT STREAK", f'{cur["length"]}d', rng(cur, current=True), ORANGE),
    ("LONGEST STREAK", f'{best["length"]}d', rng(best), PURPLE),
    ("BEST DAY", str(data["best_day"]["count"]), fmt(data["best_day"]["date"]), CYAN),
]

langs = data["languages"][:6]
other = round(100 - sum(l["percent"] for l in langs), 1)
if other >= 0.1:
    langs.append({"name": "Other", "percent": other})

W = 860
TW, TH, TGAP, TX0, TY0 = 196, 92, 12, 22, 48
BAR_Y = TY0 + TH + 46
legend_rows = (len(langs) + 3) // 4
H = BAR_Y + 26 + legend_rows * 20 + 14 if langs else TY0 + TH + 22

p = window(W, H, f"{USER}@github: ~$ ./status.sh --tz {TZ}")

for i, (label, value, sub, color) in enumerate(tiles):
    x = TX0 + i * (TW + TGAP)
    inner = (f'<rect x="{x}" y="{TY0}" width="{TW}" height="{TH}" rx="9" fill="#161b22" stroke="{BORDER}"/>'
             f'<rect x="{x}" y="{TY0+14}" width="3" height="{TH-28}" rx="1.5" fill="{color}"/>'
             f'<text x="{x+18}" y="{TY0+24}" fill="{MUTED}" font-size="10.5" font-weight="700" letter-spacing="1.2">{label}</text>'
             f'<text x="{x+18}" y="{TY0+58}" fill="{color}" font-size="30" font-weight="800" font-family="{SANS}">{esc(value)}</text>'
             f'<text x="{x+18}" y="{TY0+78}" fill="{TEXT}" font-size="11.5">{esc(sub)}</text>')
    if label == "CURRENT STREAK" and cur["length"] > 0:  # 살아있는 스트릭은 맥박 점
        inner += (f'<circle cx="{x+TW-18}" cy="{TY0+20}" r="4" fill="{ORANGE}">'
                  f'<animate attributeName="r" values="3;5;3" dur="1.2s" repeatCount="indefinite"/>'
                  f'<animate attributeName="opacity" values="1;.4;1" dur="1.2s" repeatCount="indefinite"/></circle>')
    p.append(fade_in(inner, .1 + i * .12))

if langs:
    p.append(fade_in(f'<text x="22" y="{BAR_Y-12}" fill="{BLUE}" font-size="12.5" font-weight="700">— languages</text>'
                     f'<text x="{W-22}" y="{BAR_Y-12}" fill="{MUTED}" font-size="11" text-anchor="end">public repos · by bytes</text>', .55))
    bw = W - 44
    p.append(f'<clipPath id="barclip"><rect x="22" y="{BAR_Y}" width="0" height="10" rx="5">'
             f'<animate attributeName="width" from="0" to="{bw}" begin=".7s" dur="1.1s" fill="freeze" calcMode="spline" keySplines=".2 .8 .2 1" keyTimes="0;1"/></rect></clipPath>')
    p.append(f'<rect x="22" y="{BAR_Y}" width="{bw}" height="10" rx="5" fill="#161b22"/>')
    segs, x = [], 22.0
    for l in langs:
        w = bw * l["percent"] / 100
        segs.append(f'<rect x="{x:.2f}" y="{BAR_Y}" width="{w+.5:.2f}" height="10" fill="{LANG_COLORS.get(l["name"], MUTED)}"/>')
        x += w
    p.append(f'<g clip-path="url(#barclip)">{"".join(segs)}</g>')
    for i, l in enumerate(langs):
        cx, cy = 22 + (i % 4) * (bw / 4), BAR_Y + 34 + (i // 4) * 20
        inner = (f'<circle cx="{cx+5:.1f}" cy="{cy-4}" r="5" fill="{LANG_COLORS.get(l["name"], MUTED)}"/>'
                 f'<text x="{cx+16:.1f}" y="{cy}" fill="{TEXT}" font-size="12">{esc(l["name"])} '
                 f'<tspan fill="{MUTED}">{l["percent"]}%</tspan></text>')
        p.append(fade_in(inner, 1.2 + i * .07, dy=4))

p.append('</svg>')
(ROOT / "stats.svg").write_text("".join(p), encoding="utf-8")
print("Wrote stats.svg")