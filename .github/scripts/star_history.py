#!/usr/bin/env python3
"""Draw this repo's GitHub star history in the star-history.com style.

The chart matches star-history.com's hand-drawn look (xkcd font, wobbly
lines, "Star History" title, legend), with one difference: the date axis
starts when the repository was created instead of at the first star, so the
chart covers the repo's whole life.

The core uses only the standard library. If fontTools is installed, the
embedded font is trimmed to the characters the chart uses, which keeps each
SVG small.

Usage:
    GITHUB_TOKEN=... python3 star_history.py --repo owner/name --out DIR

Writes DIR/star-history-light.svg and DIR/star-history-dark.svg.

Credits: chart style adapted from star-history.com (MIT License). The xkcd
Script font is by the ipython/xkcd-font contributors, licensed under Creative
Commons Attribution-NonCommercial 3.0; it is downloaded at run time and
embedded in the generated images, not stored in this repository.
"""

import argparse
import base64
import datetime as dt
import io
import json
import math
import os
import re
import sys
import urllib.error
import urllib.request
from bisect import bisect_right
from xml.sax.saxutils import escape

API = "https://api.github.com"
FONT_URL = ("https://raw.githubusercontent.com/ipython/xkcd-font/master/"
            "xkcd-script/font/xkcd-script.woff")

# star-history.com's defaults: 600 wide, 3:2, first series color per theme.
WIDTH = 600
HEIGHT = WIDTH * 2 // 3
MARGIN = {"top": 60, "right": 30, "bottom": 50, "left": 70}
THEMES = {
    "light": {"background": "white", "stroke": "black", "line": "#dd4528"},
    "dark": {"background": "#0d1117", "stroke": "white", "line": "#ff6b6b"},
}
FALLBACK_FONTS = "xkcd, 'xkcd Script', 'Humor Sans', 'Comic Neue', 'Comic Sans MS', cursive"
MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July",
               "August", "September", "October", "November", "December"]
DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


# --- Data -------------------------------------------------------------------

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


def download(url):
    """Fetch a non-API URL; return (bytes, content type)."""
    req = urllib.request.Request(url, headers={"User-Agent": "star-history-chart"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read(), resp.headers.get_content_type()


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


def line_points(dates, start, end):
    """Cumulative (day, stars) points: the start, both sides of each rise, the end."""
    per_day = {}
    for day in dates:
        day = min(max(day, start), end)
        per_day[day] = per_day.get(day, 0) + 1
    points, total = [(start, 0)], 0
    for day in sorted(per_day):
        before = day - dt.timedelta(days=1)
        if before > points[-1][0]:
            points.append((before, total))
        total += per_day[day]
        if day == points[-1][0]:
            points[-1] = (day, total)
        else:
            points.append((day, total))
    if end > points[-1][0]:
        points.append((end, total))
    return points


# --- Assets -----------------------------------------------------------------

def font_data_url(text):
    """The xkcd font as a data URL, trimmed to `text` when fontTools is available."""
    try:
        font, _ = download(FONT_URL)
    except (urllib.error.URLError, OSError) as err:
        print(f"couldn't download the xkcd font ({err}); using fallback fonts",
              file=sys.stderr)
        return None
    try:
        from fontTools import subset
        from fontTools.ttLib import TTFont

        tt = TTFont(io.BytesIO(font))
        subsetter = subset.Subsetter()
        subsetter.populate(text=text)
        subsetter.subset(tt)
        tt.flavor = "woff"
        buf = io.BytesIO()
        tt.save(buf)
        font = buf.getvalue()
    except ImportError:
        pass
    return "data:font/woff;base64," + base64.b64encode(font).decode("ascii")


def avatar_data_url(avatar_url):
    """The repo owner's avatar as a data URL (images in README SVGs can't load URLs)."""
    if not avatar_url:
        return None
    sep = "&" if "?" in avatar_url else "?"
    try:
        data, mime = download(f"{avatar_url}{sep}s=44")
    except (urllib.error.URLError, OSError) as err:
        print(f"couldn't download the avatar ({err}); drawing without it", file=sys.stderr)
        return None
    return f"data:{mime};base64," + base64.b64encode(data).decode("ascii")


# --- Scales and ticks (matching d3, which star-history.com uses) -------------

def tick_step(stop, count):
    """d3's tickStep for a domain of [0, stop]."""
    raw = stop / count
    power = math.floor(math.log10(raw))
    step = 10 ** power
    error = raw / step
    if error >= math.sqrt(50):
        step *= 10
    elif error >= math.sqrt(10):
        step *= 5
    elif error >= math.sqrt(2):
        step *= 2
    return step


def y_axis(total, min_top=50, max_ticks=5):
    """Star-count axis: (top, ticks), stepping by 10 or 20 stars while the repo
    is small, then by larger round numbers, so a few stars stay a small bump
    instead of filling the chart."""
    steps = [10, 20]
    magnitude = 10
    while steps[-1] * max_ticks < total:
        steps += [5 * magnitude, 10 * magnitude, 20 * magnitude]
        magnitude *= 10
    step = next(s for s in steps if s * max_ticks >= total)
    top = max(min_top, -(-total // step) * step)
    return top, list(range(0, top + 1, step))


def format_number(n, unit):
    """star-history.com's axis numbers: 950, 1.2K, 3M."""
    if unit == 1:
        return str(n)
    if unit == 1_000_000:
        return f"{n // 1_000_000}M" if n % 1_000_000 == 0 else f"{n / 1_000_000:.1f}M"
    return f"{n // 1000}K" if n % 1000 == 0 else f"{n / 1000:.1f}K"


def number_unit(n):
    return 1_000_000 if n >= 1_000_000 else 1000 if n >= 300 else 1


def every(kind, step, start, end):
    """Dates of a d3 time interval (day/week/month/year .every(step)) in [start, end]."""
    out = []
    if kind == "day":
        day = start
        while day <= end:
            if (day.day - 1) % step == 0:
                out.append(day)
            day += dt.timedelta(days=1)
    elif kind == "week":
        day = start + dt.timedelta(days=(6 - start.weekday()) % 7)  # Sundays
        while day <= end:
            out.append(day)
            day += dt.timedelta(days=7 * step)
    elif kind == "month":
        year, month = start.year, start.month
        while True:
            day = dt.date(year, month, 1)
            if day > end:
                break
            if day >= start and (month - 1) % step == 0:
                out.append(day)
            year, month = (year + 1, 1) if month == 12 else (year, month + 1)
    else:  # year
        for year in range(start.year, end.year + 1):
            day = dt.date(year, 1, 1)
            if start <= day <= end and year % step == 0:
                out.append(day)
    return out


def x_ticks(start, end, count=5):
    """d3 time-scale ticks for a date domain, at day resolution or coarser."""
    intervals = [("day", 1, 1), ("day", 2, 2), ("week", 1, 7), ("month", 1, 30),
                 ("month", 3, 90), ("year", 1, 365)]
    target = max((end - start).days, 1) / count
    i = bisect_right([d for _, _, d in intervals], target)
    if i == len(intervals):
        years = (end.year - start.year) or 1
        step = max(1, int(tick_step(years, count)))
        return every("year", step, start, end)
    if i == 0:
        kind, step, _ = intervals[0]
    else:
        lower, upper = intervals[i - 1], intervals[i]
        kind, step, _ = lower if target / lower[2] < upper[2] / target else upper
    return every(kind, step, start, end)


def format_date(day):
    """d3's default multi-scale time format, at day resolution."""
    if day.month == 1 and day.day == 1:
        return str(day.year)
    if day.day == 1:
        return MONTH_NAMES[day.month - 1]
    if day.weekday() == 6:  # Sunday: week boundary
        return f"{MONTH_NAMES[day.month - 1][:3]} {day.day:02d}"
    return f"{DAY_NAMES[day.weekday()]} {day.day:02d}"


def monotone_path(points):
    """SVG path through points using d3's curveMonotoneX."""
    def sign(v):
        return -1 if v < 0 else 1

    def slope3(x0, y0, x1, y1, x2, y2):
        h0, h1 = x1 - x0, x2 - x1
        s0 = (y1 - y0) / h0 if h0 else 0
        s1 = (y2 - y1) / h1 if h1 else 0
        p = (s0 * h1 + s1 * h0) / (h0 + h1) if h0 + h1 else 0
        return (sign(s0) + sign(s1)) * min(abs(s0), abs(s1), 0.5 * abs(p))

    def slope2(x0, y0, x1, y1, t):
        h = x1 - x0
        return (3 * (y1 - y0) / h - t) / 2 if h else t

    def bezier(x0, y0, x1, y1, t0, t1):
        dx = (x1 - x0) / 3
        return (f"C{x0 + dx:.2f},{y0 + dx * t0:.2f},{x1 - dx:.2f},{y1 - dx * t1:.2f},"
                f"{x1:.2f},{y1:.2f}")

    pts = []
    for p in points:
        if not pts or p != pts[-1]:
            pts.append(p)
    if len(pts) == 1:
        return f"M{pts[0][0]:.2f},{pts[0][1]:.2f}Z"
    d = [f"M{pts[0][0]:.2f},{pts[0][1]:.2f}"]
    if len(pts) == 2:
        d.append(f"L{pts[1][0]:.2f},{pts[1][1]:.2f}")
        return "".join(d)
    t0 = None
    for k in range(2, len(pts)):
        (x0, y0), (x1, y1), (x2, y2) = pts[k - 2], pts[k - 1], pts[k]
        t1 = slope3(x0, y0, x1, y1, x2, y2)
        start_slope = slope2(x0, y0, x1, y1, t1) if t0 is None else t0
        d.append(bezier(x0, y0, x1, y1, start_slope, t1))
        t0 = t1
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    d.append(bezier(x0, y0, x1, y1, t0, slope2(x0, y0, x1, y1, t0)))
    return "".join(d)


# --- Drawing ----------------------------------------------------------------

def render(repo, points, theme_name, font_url, avatar_url):
    t = THEMES[theme_name]
    stroke = t["stroke"]
    start, end = points[0][0], points[-1][0]
    total = points[-1][1]
    top, star_ticks = y_axis(total)
    chart_w = WIDTH - MARGIN["left"] - MARGIN["right"]
    chart_h = HEIGHT - MARGIN["top"] - MARGIN["bottom"]
    span = max((end - start).days, 1)

    def x(day):
        return chart_w * (day - start).days / span

    def y(value):
        return chart_h * (1 - value / top)

    font_family = "xkcd" if font_url else FALLBACK_FONTS
    star_word = "star" if total == 1 else "stars"
    out = []
    add = out.append

    add(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" '
        f'style="stroke-width: 3; font-family: {font_family}; background: {t["background"]};" '
        f'role="img" aria-labelledby="title desc">')
    add(f'<title id="title">Star History of {escape(repo)}</title>')
    add(f'<desc id="desc">GitHub stars for {escape(repo)} from {MONTH_NAMES[start.month - 1]} '
        f'{start.day}, {start.year} to {MONTH_NAMES[end.month - 1]} {end.day}, {end.year}: '
        f'{total:,} {star_word}.</desc>')
    add("<!-- Chart style adapted from star-history.com (MIT). xkcd Script font by the "
        "ipython/xkcd-font contributors, CC BY-NC 3.0. -->")
    add("<defs>")
    if font_url:
        add(f'<style type="text/css">@font-face {{ font-family: "xkcd"; '
            f'src: url({font_url}) format("woff"); }}</style>')
    add('<filter id="xkcdify" filterUnits="userSpaceOnUse" x="-5" y="-5" width="100%" height="100%">'
        '<feTurbulence type="fractalNoise" baseFrequency="0.05" result="noise"/>'
        '<feDisplacementMap scale="5" xChannelSelector="R" yChannelSelector="G" '
        'in="SourceGraphic" in2="noise"/></filter>')
    add('<clipPath id="clip-circle-title"><circle r="11" '
        f'cx="{WIDTH * 0.5 - 73}" cy="23"/></clipPath>')
    add("</defs>")
    add(f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{t["background"]}" stroke="none"/>')

    # Title, owner avatar, and axis labels.
    add(f'<text x="50%" y="30" text-anchor="middle" style="font-size: 20px; font-weight: bold; '
        f'fill: {stroke};">Star History</text>')
    if avatar_url:
        add(f'<image x="{WIDTH * 0.5 - 84}" y="12" width="22" height="22" '
            f'href="{avatar_url}" xlink:href="{avatar_url}" clip-path="url(#clip-circle-title)"/>')
    add(f'<text x="50%" y="{HEIGHT - 10}" text-anchor="middle" '
        f'style="font-size: 17px; fill: {stroke};">Date</text>')
    offset_y = (2 if total > 100000 else 8 if total > 10000 else 12 if total > 1000
                else 20 if total > 100 else 24)
    add(f'<text text-anchor="end" dy=".75em" transform="rotate(-90)" y="{offset_y}" '
        f'x="{math.floor(100 / 2 - HEIGHT / 2)}" style="font-size: 17px; fill: {stroke};">'
        f'GitHub Stars</text>')

    add(f'<g transform="translate({MARGIN["left"]},{MARGIN["top"]})">')

    # X axis: a hand-drawn baseline and d3-style date ticks.
    add(f'<g transform="translate(0,{chart_h})" fill="none" text-anchor="middle">')
    add(f'<path d="M0.5,0V0.5H{chart_w + 0.5}V0" filter="url(#xkcdify)" '
        f'style="stroke: {stroke};"/>')
    # Label where the axis starts (e.g. "Dec 2025"), since that's the point of
    # starting at the repo's creation; drop regular ticks that would collide.
    ticks = [(0.0, f"{MONTH_NAMES[start.month - 1][:3]} {start.year}", "start")]
    ticks += [(x(day), format_date(day), "middle") for day in x_ticks(start, end)
              if x(day) > 80]
    for tx, label, anchor in ticks:
        add(f'<text x="{tx + 0.5:.1f}" y="6" dy="0.71em" text-anchor="{anchor}" '
            f'style="font-family: {font_family}; font-size: 16px; fill: {stroke};">'
            f'{label}</text>')
    add("</g>")

    # Y axis: hand-drawn line, small tick marks, star-history number format.
    add('<g fill="none" text-anchor="end">')
    add(f'<path d="M-1,{chart_h + 0.5}H0.5V0.5H-1" filter="url(#xkcdify)" '
        f'style="stroke: {stroke};"/>')
    unit = None
    for value in star_ticks:
        yy = y(value) + 0.5
        add(f'<line x2="-1" y1="{yy:.1f}" y2="{yy:.1f}" stroke="{stroke}"/>')
        if value == 0:
            continue
        unit = unit or number_unit(value)
        add(f'<text x="-7" y="{yy:.1f}" dy="0.32em" '
            f'style="font-family: {font_family}; font-size: 16px; fill: {stroke};">'
            f'{format_number(value, unit)}</text>')
    add("</g>")

    # The star line, smoothed like d3's curveMonotoneX, through the wobble filter.
    path = monotone_path([(x(day), y(value)) for day, value in points])
    add(f'<path d="{path}" fill="none" stroke="{t["line"]}" filter="url(#xkcdify)"/>')

    # Legend, top left.
    legend_x, legend_y = 8, 5
    width = max(len(repo) * 7.5 + 8 + 7 + 14, len(repo) * 7 + 8 + 14 + 6)
    add(f'<rect x="{legend_x}" y="{legend_y}" width="{width:.1f}" height="32" rx="5" ry="5" '
        f'fill-opacity="0.85" stroke-width="2" filter="url(#xkcdify)" '
        f'style="fill: {t["background"]}; stroke: {stroke};"/>')
    add(f'<rect x="{legend_x + 7}" y="{legend_y + 12}" width="8" height="8" rx="2" ry="2" '
        f'filter="url(#xkcdify)" style="fill: {t["line"]};"/>')
    add(f'<text x="{legend_x + 7 + 8 + 6}" y="{legend_y + 20}" '
        f'style="font-size: 15px; fill: {stroke};">{escape(repo)}</text>')

    add("</g></svg>")
    return "\n".join(out) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY"),
                        help="owner/name (default: $GITHUB_REPOSITORY)")
    parser.add_argument("--start", help="first day on the date axis, YYYY-MM-DD "
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
    points = line_points(star_dates(repo), start, today)

    # Every character the chart can draw, so the trimmed font covers them all.
    glyphs = ("Star History Date GitHub Stars " + repo + "0123456789.KM "
              + " ".join(MONTH_NAMES + DAY_NAMES))
    font_url = font_data_url(glyphs)
    avatar_url = avatar_data_url(info.get("owner", {}).get("avatar_url"))

    os.makedirs(args.out, exist_ok=True)
    for theme in THEMES:
        path = os.path.join(args.out, f"star-history-{theme}.svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(render(repo, points, theme, font_url, avatar_url))
        print(f"wrote {path} ({os.path.getsize(path) // 1024} KB)")
    print(f"{repo}: {points[-1][1]} stars from {start} to {today}")


if __name__ == "__main__":
    main()
