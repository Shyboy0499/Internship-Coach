#!/usr/bin/env python3
"""Draw this repo's GitHub star history as light and dark SVG charts.

Unlike hosted star charts, which start at the first star, the x-axis here
starts when the repository was created, so the chart covers the repo's whole
life. Uses only the standard library, so it runs on a stock GitHub runner.

Usage:
    GITHUB_TOKEN=... python3 star_history.py --repo owner/name --out DIR

Writes DIR/star-history-light.svg and DIR/star-history-dark.svg.
"""

import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.request
from xml.sax.saxutils import escape

API = "https://api.github.com"

# Reference data-viz palette: series slot 1 (blue), chart chrome and ink,
# validated against each surface.
THEMES = {
    "light": {
        "surface": "#fcfcfb",
        "border": "rgba(11,11,11,0.10)",
        "series": "#2a78d6",
        "ink": "#0b0b0b",
        "ink2": "#52514e",
        "muted": "#898781",
        "grid": "#e1e0d9",
        "axis": "#c3c2b7",
    },
    "dark": {
        "surface": "#1a1a19",
        "border": "rgba(255,255,255,0.10)",
        "series": "#3987e5",
        "ink": "#f0efec",
        "ink2": "#c3c2b7",
        "muted": "#898781",
        "grid": "#2c2c2a",
        "axis": "#383835",
    },
}

WIDTH, HEIGHT = 800, 360
PAD_LEFT, PAD_RIGHT, PAD_TOP, PAD_BOTTOM = 56, 88, 76, 56
FONT = "system-ui, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def get(path, accept="application/vnd.github+json"):
    """GET an API path; return (parsed JSON, next page number or None)."""
    req = urllib.request.Request(API + path, headers={
        "Accept": accept,
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "star-history-chart",
    })
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        # Follow pages by number on the same path: the Link URLs point at
        # /repositories/<id>/..., which some proxies don't allow.
        link = resp.headers.get("Link", "")
        match = re.search(r'[?&]page=(\d+)[^>]*>;\s*rel="next"', link)
        return json.load(resp), (int(match.group(1)) if match else None)


def star_dates_from_stargazers(repo):
    """Exact star dates from the stargazer list (needs list access)."""
    dates, page_no = [], 1
    while page_no:
        page, page_no = get(f"/repos/{repo}/stargazers?per_page=100&page={page_no}",
                            accept="application/vnd.github.star+json")
        dates += [dt.date.fromisoformat(s["starred_at"][:10]) for s in page]
    return dates


def star_dates_from_history(repo):
    """Daily star counts from the stargazer history endpoint (fallback)."""
    dates, page_no = [], 1
    while page_no:
        page, page_no = get(f"/repos/{repo}/stargazers/history?page={page_no}")
        for week in page:
            start = dt.datetime.fromtimestamp(week["week"], dt.timezone.utc).date()
            for offset, count in enumerate(week["days"]):
                dates += [start + dt.timedelta(days=offset)] * count
    return dates


def star_dates(repo):
    try:
        return star_dates_from_stargazers(repo)
    except urllib.error.HTTPError as err:
        if err.code not in (401, 403, 404, 422):
            raise
        print(f"stargazer list unavailable (HTTP {err.code}); using history endpoint",
              file=sys.stderr)
        return star_dates_from_history(repo)


def cumulative(dates, start, end):
    """[(day, total stars by end of day)] for every day from start to end."""
    per_day = {}
    for day in dates:
        day = min(max(day, start), end)
        per_day[day] = per_day.get(day, 0) + 1
    series, total, day = [], 0, start
    while day <= end:
        total += per_day.get(day, 0)
        series.append((day, total))
        day += dt.timedelta(days=1)
    return series


def nice_max(value):
    """A clean y-axis top with headroom; at least 5, so a few stars don't fill the plot."""
    target = max(value, 4) * 1.1
    magnitude = 1
    while True:
        for step in (1, 1.5, 2, 2.5, 3, 4, 5, 6, 8):
            top = step * magnitude
            if top >= target and float(top).is_integer():
                return int(top)
        magnitude *= 10


def compact(n):
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}".rstrip("0").rstrip(".") + "M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}".rstrip("0").rstrip(".") + "K"
    return str(n)


def month_starts(start, end):
    """First day of each month strictly after start, up to end."""
    year, month = start.year, start.month
    out = []
    while True:
        month += 1
        if month == 13:
            year, month = year + 1, 1
        day = dt.date(year, month, 1)
        if day > end:
            return out
        out.append(day)


def render(repo, series, theme_name, updated):
    t = THEMES[theme_name]
    start, end = series[0][0], series[-1][0]
    total = series[-1][1]
    y_top = nice_max(total)
    plot_w = WIDTH - PAD_LEFT - PAD_RIGHT
    plot_h = HEIGHT - PAD_TOP - PAD_BOTTOM
    span = max((end - start).days, 1)

    def x(day):
        return PAD_LEFT + plot_w * (day - start).days / span

    def y(value):
        return PAD_TOP + plot_h * (1 - value / y_top)

    base = y(0)
    out = []
    add = out.append
    star_word = "star" if total == 1 else "stars"
    title = f"{repo} GitHub stars"
    desc = (f"Cumulative GitHub stars for {repo} from {start:%B} {start.day}, {start.year} "
            f"to {end:%B} {end.day}, {end.year}: {total:,} {star_word}.")

    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="t d">')
    add(f'<title id="t">{escape(title)}</title><desc id="d">{escape(desc)}</desc>')
    add(f'<rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{HEIGHT - 1}" rx="12" '
        f'fill="{t["surface"]}" stroke="{t["border"]}"/>')
    add(f'<g font-family="{FONT}">')

    # Title and subtitle: the title names the single series, so no legend box.
    add(f'<text x="{PAD_LEFT - 32}" y="34" font-size="17" font-weight="600" '
        f'fill="{t["ink"]}">Star history</text>')
    add(f'<text x="{PAD_LEFT - 32}" y="56" font-size="13" fill="{t["ink2"]}">'
        f'{escape(repo)} · since {MONTHS[start.month - 1]} {start.day}, {start.year} · '
        f'updated {MONTHS[updated.month - 1]} {updated.day}, {updated.year}</text>')

    # Gridlines and y ticks: solid hairlines, recessive, on whole numbers.
    ticks = next(d for d in (5, 4, 6, 3, 2, 1) if y_top % d == 0)
    for i in range(ticks + 1):
        value = y_top * i // ticks
        yy = y(value)
        color = t["axis"] if i == 0 else t["grid"]
        add(f'<line x1="{PAD_LEFT}" x2="{PAD_LEFT + plot_w}" y1="{yy:.1f}" y2="{yy:.1f}" '
            f'stroke="{color}" stroke-width="1"/>')
        add(f'<text x="{PAD_LEFT - 10}" y="{yy + 4:.1f}" font-size="12" text-anchor="end" '
            f'fill="{t["muted"]}" style="font-variant-numeric: tabular-nums">'
            f'{compact(int(value))}</text>')

    # X ticks: one per month, month names on the first line and the year on
    # a second line under the first tick and each January, so labels never
    # collide. Thin out to every 2nd/3rd month on long histories.
    marks = ([start] if start.day == 1 else []) + month_starts(start, end)
    step = 1 if len(marks) <= 12 else 2 if len(marks) <= 24 else 3
    labelled_year = False
    for i, day in enumerate(marks):
        xx = x(day)
        add(f'<line x1="{xx:.1f}" x2="{xx:.1f}" y1="{base:.1f}" y2="{base + 5:.1f}" '
            f'stroke="{t["axis"]}" stroke-width="1"/>')
        if i % step:
            continue
        add(f'<text x="{xx:.1f}" y="{base + 20:.1f}" font-size="12" text-anchor="middle" '
            f'fill="{t["muted"]}">{MONTHS[day.month - 1]}</text>')
        if not labelled_year or day.month == 1:
            add(f'<text x="{xx:.1f}" y="{base + 35:.1f}" font-size="11" text-anchor="middle" '
                f'fill="{t["muted"]}">{day.year}</text>')
            labelled_year = True

    # The series: a step line (stars arrive at a moment) over a 10% area wash.
    points = [(x(series[0][0]), y(series[0][1]))]
    previous = series[0][1]
    for day, value in series[1:]:
        if value != previous:
            xx = x(day)
            points += [(xx, y(previous)), (xx, y(value))]
            previous = value
    points.append((x(end), y(total)))
    line = " ".join(f"{px:.1f},{py:.1f}" for px, py in points)
    area = f"{points[0][0]:.1f},{base:.1f} {line} {points[-1][0]:.1f},{base:.1f}"
    add(f'<polygon points="{area}" fill="{t["series"]}" fill-opacity="0.10"/>')
    add(f'<polyline points="{line}" fill="none" stroke="{t["series"]}" stroke-width="2" '
        f'stroke-linejoin="round" stroke-linecap="round"/>')

    # End-dot with a 2px surface ring, and the current total as a direct label.
    ex, ey = points[-1]
    add(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="6" fill="{t["surface"]}"/>')
    add(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="4" fill="{t["series"]}"/>')
    add(f'<text x="{ex + 12:.1f}" y="{ey + 5:.1f}" font-size="14" font-weight="600" '
        f'fill="{t["ink"]}">{total:,}</text>')
    add(f'<text x="{ex + 12:.1f}" y="{ey + 21:.1f}" font-size="12" '
        f'fill="{t["ink2"]}">{star_word}</text>')

    add("</g></svg>")
    return "\n".join(out) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY"),
                        help="owner/name (default: $GITHUB_REPOSITORY)")
    parser.add_argument("--start", help="first day on the x-axis, YYYY-MM-DD "
                        "(default: the day the repository was created)")
    parser.add_argument("--out", default=".", help="directory for the SVG files")
    args = parser.parse_args()
    if not args.repo:
        parser.error("--repo is required outside GitHub Actions")

    info, _ = get(f"/repos/{args.repo}")
    repo = info["full_name"]
    start = (dt.date.fromisoformat(args.start) if args.start
             else dt.date.fromisoformat(info["created_at"][:10]))
    today = dt.datetime.now(dt.timezone.utc).date()

    dates = star_dates(repo)
    series = cumulative(dates, start, today)
    os.makedirs(args.out, exist_ok=True)
    for theme in THEMES:
        path = os.path.join(args.out, f"star-history-{theme}.svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(render(repo, series, theme, today))
        print(f"wrote {path}")
    print(f"{repo}: {series[-1][1]} stars from {start} to {today}")


if __name__ == "__main__":
    main()
