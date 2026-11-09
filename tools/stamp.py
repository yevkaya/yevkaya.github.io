"""Stamp the footer with today's date: <time data-updated datetime="YYYY-MM-DD">Month YYYY</time>.
Run after content changes (or as the last build step); the date is otherwise never updated."""
import os, re, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = next(p for p in (os.path.join(HERE, ".."), os.path.join(HERE, "..", "Portfolio")) if os.path.exists(os.path.join(p, "index.html")))
today = datetime.date.today()
html = open(os.path.join(SITE, "index.html"), encoding="utf-8").read()
new = f'<time data-updated datetime="{today.isoformat()}">{today.strftime("%B %Y")}</time>'
html2, n = re.subn(r'<time data-updated datetime="\d{4}-\d{2}-\d{2}">[^<]*</time>', new, html)
assert n == 1, n
open(os.path.join(SITE, "index.html"), "w", encoding="utf-8").write(html2)
MONTHS = {"tr": ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"],
          "de": ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]}
for lang, names in MONTHS.items():  # localized pages built by tools/i18n.py
    f = os.path.join(SITE, lang, "index.html")
    if os.path.exists(f):
        h = open(f, encoding="utf-8").read()
        h = re.sub(r'<time data-updated datetime="\d{4}-\d{2}-\d{2}">[^<]*</time>', f'<time data-updated datetime="{today.isoformat()}">{names[today.month - 1]} {today.year}</time>', h)
        open(f, "w", encoding="utf-8").write(h)
sm = os.path.join(SITE, "sitemap.xml")
if os.path.exists(sm):
    x = open(sm).read(); open(sm, "w").write(re.sub(r"<lastmod>[^<]*</lastmod>", f"<lastmod>{today.isoformat()}</lastmod>", x))
print("stamped", today)
