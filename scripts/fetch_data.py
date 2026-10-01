#!/usr/bin/env python3
import datetime, json, os, sys, urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).parent))
from theme import USER, TZ

OUT = Path(__file__).resolve().parent.parent / "data" / "profile.json"
TOKEN = os.environ.get("GH_TOKEN", "")


def get(url, auth=False):
    req = urllib.request.Request(url, headers={"User-Agent": "numunun-profile"})
    if auth and TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def streaks(days, today):
    days = [d for d in days if datetime.date.fromisoformat(d["date"]) <= today]
    i = len(days) - 1
    if i >= 0 and days[i]["count"] == 0:
        i -= 1
    end = i
    while i >= 0 and days[i]["count"] > 0:
        i -= 1
    current = {"length": end - i, "start": days[i + 1]["date"] if end > i else None,
               "end": days[end]["date"] if end > i else None}
    # 최장 스트릭
    best = {"length": 0, "start": None, "end": None}
    run_start = None
    for k, d in enumerate(days):
        if d["count"] > 0:
            run_start = k if run_start is None else run_start
            if k - run_start + 1 > best["length"]:
                best = {"length": k - run_start + 1, "start": days[run_start]["date"], "end": d["date"]}
        else:
            run_start = None
    return days, current, best


def languages():
    repos = get(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner", auth=True)
    total = {}
    for repo in repos:
        if repo["fork"] or repo["name"].lower() == USER.lower():
            continue  # 포크와 이 프로필 저장소는 제외
        for lang, size in get(repo["languages_url"], auth=True).items():
            total[lang] = total.get(lang, 0) + size
    s = sum(total.values()) or 1
    ranked = sorted(total.items(), key=lambda x: -x[1])
    return [{"name": k, "percent": round(v * 100 / s, 1)} for k, v in ranked]


def main():
    today = datetime.datetime.now(ZoneInfo(TZ)).date()
    raw = get(f"https://github-contributions-api.jogruber.de/v4/{USER}?y=last")
    days, current, best = streaks(raw["contributions"], today)

    try:
        langs = languages()
    except Exception as e:  # API가 잠깐 실패하면 이전 값을 그대로 쓴다
        print(f"language fetch failed: {e}", file=sys.stderr)
        langs = json.loads(OUT.read_text())["languages"] if OUT.exists() else []

    top = max(days, key=lambda d: d["count"])
    data = {
        "user": USER,
        "today": today.isoformat(),
        "total": sum(d["count"] for d in days),
        "active_days": sum(d["count"] > 0 for d in days),
        "current_streak": current,
        "longest_streak": best,
        "best_day": {"date": top["date"], "count": top["count"]},
        "languages": langs,
        "days": [{"date": d["date"], "count": d["count"], "level": d["level"]} for d in days],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=1), encoding="utf-8")
    print(f"Wrote {OUT}: total={data['total']} current={current['length']} longest={best['length']}")


if __name__ == "__main__":
    main()