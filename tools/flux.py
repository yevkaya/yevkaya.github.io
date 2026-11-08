"""Hero gauge-dynamics panel v3: the full C2 patch of the thesis (Fig. II.1), one large animated SVG.
Sequence (12 s loop): (a) formation ramp — corridor rishons fill outer -> inner and the string closes;
(b) breaking quench — inner rishon pairs empty, a q̄q pair appears at 7 and 8, two short strings remain."""
import math

W, H = 600, 284

raw = {1: (186, 791), 7: (277, 740), 2: (367, 791), 8: (457, 740), 3: (546, 791), 9: (636, 740),
       4: (277, 635), 5: (457, 635), 6: (636, 635), 10: (367, 583), 11: (546, 583), 12: (726, 583)}
S = 0.86
X0, Y0 = 98, 50
v = {k: (X0 + (x - 186) * S, Y0 + (y - 583) * S) for k, (x, y) in raw.items()}
links = {1: (1, 7), 3: (7, 2), 2: (2, 8), 5: (8, 3), 4: (3, 9), 7: (7, 4), 10: (8, 5), 13: (9, 6),
         6: (4, 10), 9: (10, 5), 8: (5, 11), 12: (11, 6), 11: (6, 12)}
OUTER, INNER = (1, 5), (3, 2)
CORR = OUTER + INNER

def f(x): return f"{x:.1f}"
def P(pts): return "M" + " L".join(f"{f(x)} {f(y)}" for x, y in pts)
def lerp(a, b, t): return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
def sub(b, i): return f'{b}<tspan class="fz-sub" dy="3">{i}</tspan><tspan dy="-3"> </tspan>'
def sup(b, i): return f'{b}<tspan class="fz-sub" dy="-5">{i}</tspan><tspan dy="5"> </tspan>'
def text(x, y, s, cls, anchor="middle"): return f'<text class="{cls}" x="{f(x)}" y="{f(y)}" text-anchor="{anchor}">{s}</text>'

def rishon_pts(lid):
    a, b = links[lid]
    return [lerp(v[a], v[b], t) for t in (0.26, 0.74)]

out = []
# defs: soft glow for the string
out.append('<defs><filter id="fz-blur" x="-20%" y="-60%" width="140%" height="220%"><feGaussianBlur stdDeviation="4"/></filter>'
           '<radialGradient id="fz-flash"><stop offset="0" stop-color="#d8fff6" stop-opacity=".9"/><stop offset="1" stop-color="#79e3e1" stop-opacity="0"/></radialGradient></defs>')

# phase indicator
out.append('<g class="fz-phases">'
           '<g class="fz-phase fz-phase-a"><rect x="0" y="0" width="186" height="24" rx="12"/>'
           + text(93, 16, '<tspan class="fz-ital">(a)</tspan> Flux-tube formation', "fz-phase-t") + '</g>'
           '<g class="fz-phase fz-phase-b"><rect x="196" y="0" width="150" height="24" rx="12"/>'
           + text(271, 16, '<tspan class="fz-ital">(b)</tspan> String breaking', "fz-phase-t") + '</g></g>')
out.append(text(600, 16, "C2 patch · R = 4", "fz-meta", "end"))

# links
for lid, (a, b) in links.items():
    out.append(f'<path class="{"fz-link fz-link-corr" if lid in CORR else "fz-link"}" d="{P([v[a], v[b]])}"/>')
# link labels
for lid, (a, b) in links.items():
    (x1, y1), (x2, y2) = v[a], v[b]
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy); nx, ny = -dy / L, dx / L
    if ny > 0 or (abs(ny) < 1e-6 and nx < 0): nx, ny = -nx, -ny
    out.append(text(mx + nx * 12, my + ny * 12 + 3.5, sub("ℓ", lid), "fz-id"))

# string (formation halves, then meson segments and remnant)
half_L = [v[1], v[7], v[2]]
half_R = [v[3], v[8], v[2]]
for cls in ("fz-glow", "fz-str"):
    out.append(f'<path class="{cls} fz-form" d="{P(half_L)}" pathLength="1"/>')
    out.append(f'<path class="{cls} fz-form" d="{P(half_R)}" pathLength="1"/>')
    out.append(f'<path class="{cls} fz-meson" d="{P([v[1], v[7]])}"/>')
    out.append(f'<path class="{cls} fz-meson" d="{P([v[8], v[3]])}"/>')
out.append(f'<path class="fz-remnant" d="{P([v[7], v[2], v[8]])}"/>')

# rishons: base (hollow) everywhere, filled overlays on the corridor
for lid in links:
    for x, y in rishon_pts(lid):
        out.append(f'<circle class="fz-rishon" cx="{f(x)}" cy="{f(y)}" r="3.6"/>')
for lid in OUTER:
    for x, y in rishon_pts(lid):
        out.append(f'<circle class="fz-rishon-on fz-r-outer" cx="{f(x)}" cy="{f(y)}" r="3.6"/>')
for lid in INNER:
    for x, y in rishon_pts(lid):
        out.append(f'<circle class="fz-rishon-on fz-r-inner" cx="{f(x)}" cy="{f(y)}" r="3.6"/>')

# quench flash at vertex 2
out.append(f'<circle class="fz-flash" cx="{f(v[2][0])}" cy="{f(v[2][1])}" r="26" fill="url(#fz-flash)"/>')

# matter sites
for k, (x, y) in v.items():
    if k in (1, 3):
        continue
    if k <= 6:
        out.append(f'<circle class="fz-site" cx="{f(x)}" cy="{f(y)}" r="5.6"/>')
    else:
        out.append(f'<rect class="fz-site" x="{f(x - 5.2)}" y="{f(y - 5.2)}" width="10.4" height="10.4" rx="1"/>')
    if k in (4, 5, 6):
        out.append(text(x - 13, y + 3.5, k, "fz-id"))
    elif k >= 10:
        out.append(text(x, y - 11, k, "fz-id"))
    elif k == 2:
        out.append(text(x, y - 11, k, "fz-id"))
    elif k in (7, 8):
        out.append(text(x - 13, y + 3.5, k, "fz-id"))
    else:
        out.append(text(x + 13, y + 3.5, k, "fz-id"))

# created pair at 7 (q̄) and 8 (q)
for k, lab, dx in ((7, "q̄", -16), (8, "q", 16)):
    x, y = v[k]
    out.append(f'<g class="fz-pair"><circle class="fz-halo" cx="{f(x)}" cy="{f(y)}" r="12"/>'
               f'<rect class="fz-site fz-site-on" x="{f(x - 5.2)}" y="{f(y - 5.2)}" width="10.4" height="10.4" rx="1"/>'
               + text(x + dx, y - 9, lab, "fz-q") + '</g>')

# static sources
for k, q, lab, side in ((1, "+1", "Q", -1), (3, "−1", "Q̄", 1)):
    x, y = v[k]
    out.append(f'<circle class="fz-src-ring" cx="{f(x)}" cy="{f(y)}" r="11"/><circle class="fz-src" cx="{f(x)}" cy="{f(y)}" r="5.8"/>')
    out.append(text(x + side * 17, y + 16, f'{lab}<tspan class="fz-q-src"> · {sup("q", "3")}= {q}</tspan>', "fz-q", "end" if side < 0 else "start"))

# timeline
ty = 254
segs = [(0.00, 0.08, "sources"), (0.08, 0.40, "ramp"), (0.40, 0.55, "string"), (0.55, 0.66, "quench"), (0.66, 0.92, "two mesons")]
tx0, tx1 = 0, 600
out.append(f'<path class="fz-axis" d="M{tx0} {ty} L{tx1} {ty}"/>')
for a, b, lab in segs:
    xa = tx0 + (tx1 - tx0) * a
    out.append(f'<path class="fz-tick" d="M{f(xa)} {ty - 3} L{f(xa)} {ty + 3}"/>')
    out.append(text(tx0 + (tx1 - tx0) * (a + b) / 2, ty + 15, lab, "fz-tl"))
out.append(f'<circle class="fz-marker" cx="{tx0}" cy="{ty}" r="3.4"/>')

# legend
ly = 282
out.append(f'<circle class="fz-site" cx="5" cy="{ly - 4}" r="4.2"/><rect class="fz-site" x="13" y="{ly - 8}" width="8" height="8" rx="1"/>'
           + text(28, ly, "A / B matter", "fz-leg", "start"))
out.append(f'<circle class="fz-rishon" cx="118" cy="{ly - 4}" r="3"/><circle class="fz-rishon-on" cx="128" cy="{ly - 4}" r="3"/>'
           + text(138, ly, f'rishons {sub("n", "L")}, {sub("n", "R")}', "fz-leg", "start"))
out.append(f'<path class="fz-str" d="M236 {ly - 4} L262 {ly - 4}"/>' + text(270, ly, "electric flux", "fz-leg", "start"))
out.append(text(600, ly, f'{sub("G", "v")}|ψ⟩ = 0 · {sup("E", "2")}{sub("", "ℓ")}= ¾ {sub("n", "L")}{sub("n", "R")}', "fz-leg", "end"))

svg = (f'<svg class="flux-svg flux-svg-c2" viewBox="0 0 {W} {H}" role="img" aria-label="The C2 honeycomb patch of the thesis: '
       'twelve matter vertices and thirteen links with two rishons each. (a) After static SU(2) sources are inserted at vertices 1 and 3, '
       'rishon pairs along the four-link corridor fill from both ends and an electric flux string forms. (b) In the breaking quench '
       'the inner rishon pairs empty while a quark–antiquark pair is created at vertices 7 and 8, leaving two short strings that screen the sources.">'
       + "".join(out) + '</svg>')

if __name__ == "__main__":
    open("flux3.svg.html", "w").write(svg)
    print(len(svg))
