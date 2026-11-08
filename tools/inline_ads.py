"""Inline the AdS figure into index.html with scoped classes, page fonts and dy-based scripts."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, "..") if os.path.exists(os.path.join(HERE, "..", "index.html")) else os.path.join(HERE, "..", "Portfolio")
SRC = os.path.join(SITE, "assets", "images", "ads-wilson-worldsheet.svg")
HTML = os.path.join(SITE, "index.html")

s = open(SRC).read()
s = re.sub(r'<\?xml[^>]*>\s*', '', s)
# scripts: dy-based so they also work where baseline-shift is unsupported
s = re.sub(r'<tspan class="sup">(.*?)</tspan>', r'<tspan class="ads-sup" dy="-7">\1</tspan><tspan dy="7"> </tspan>', s)
s = re.sub(r'<tspan class="sub">(.*?)</tspan>', r'<tspan class="ads-sub" dy="4">\1</tspan><tspan dy="-4"> </tspan>', s)
# ids
s = s.replace('id="arrow"', 'id="ads-arrow"').replace('url(#arrow)', 'url(#ads-arrow)')
s = s.replace('id="sheet"', 'id="ads-sheet"').replace('url(#sheet)', 'url(#ads-sheet)')
# classes
def pref(m):
    return 'class="' + " ".join(c if c.startswith("ads-") else "ads-" + c for c in m.group(1).split()) + '"'
s = re.sub(r'class="([^"]+)"', pref, s)
# style: scope everything under .ads-svg and use the page's math font
a, b = s.index("<style>"), s.index("</style>")
style = s[a + 7:b]
style = style.replace('font-family:"Times New Roman",Times,serif', 'font-family:var(--math)')
style = style.replace('.sup{font-size:11px;baseline-shift:super}', '.sup{font-size:11px}').replace('.sub{font-size:12px;baseline-shift:sub}', '.sub{font-size:12px}')
style = re.sub(r'(^|[}\n])\s*text\{', r'\1.ads-svg text{', style)
style = re.sub(r'\.([a-z][a-z0-9-]*)', lambda m: "." + (m.group(1) if m.group(1).startswith("ads") else "ads-" + m.group(1)), style)
style = style.replace(".ads-ads-svg", ".ads-svg")
# selectors like ".ads-s5-mesh.ads-s5-back" already fine; ensure every rule is scoped
rules = re.findall(r'([^{}]+)\{([^{}]*)\}', style)
scoped = "\n".join(f"{','.join(('.ads-svg ' + x.strip()) if not x.strip().startswith('.ads-svg') else x.strip() for x in sel.split(','))}{{{body}}}" for sel, body in rules)
s = s[:a] + "<style>\n" + scoped + "\n</style>" + s[b + 8:]
s = s.replace('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 390"', '<svg class="ads-diagram ads-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 390"', 1)

h = open(HTML).read()
m = re.search(r'<img class="ads-diagram" src="assets/images/ads-wilson-worldsheet.svg"[^>]*/>', h, flags=re.S)
if m:
    h = h[:m.start()] + s.strip() + h[m.end():]
else:
    m = re.search(r'<svg class="ads-diagram ads-svg".*?</svg>', h, flags=re.S)
    h = h[:m.start()] + s.strip() + h[m.end():]
open(HTML, "w").write(h)
print("inlined; style rules:", len(rules))
