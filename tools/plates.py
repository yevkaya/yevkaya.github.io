"""Figure plates for the dialogs (Fig. 3-10), in the visual language of Fig. 1.

Every plate has the same anatomy as the hero figures: a header (boxed FIG number, title, italic context), the drawing,
a legend row and a source note.  The drawings share one vocabulary with Fig. 1:
  turquoise  electric flux, matter, established work      gold   plaquette / loop physics, developing directions
  ivory      static sources, external inputs               dashed outline   one object (cluster, string, group)
  mono caps  annotation headline, italic serif subline, thin leader ending in a dot on its target
  labels sit on a halo of the plate colour, so lines pass behind them.
The M.Sc. plate (Fig. 7) is drawn from the exact state and data of tools/fig1.py: the m = 4 ground-state tube on the C2
patch (Gauss law checked there) and the exact real-time source-class probabilities of the breaking quench.
"""
import html, math, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fig1  # noqa: E402  (geometry, exact storyboard state, real-time data, outline contour)

# ---------------------------------------------------------------- helpers
def n1(x):
    return f"{x:.1f}".rstrip("0").rstrip(".")
def T(x, y, s, cls="pl-t", anchor="middle", extra=""):
    return f'<text class="{cls}" x="{n1(x)}" y="{n1(y)}" text-anchor="{anchor}"{extra}>{s}</text>'
def sub(b, i, cls="pl-sub"):
    return f'{b}<tspan class="{cls}" dy="3">{i}</tspan><tspan dy="-3"> </tspan>'
def sup(b, i, cls="pl-sub"):
    return f'{b}<tspan class="{cls}" dy="-5">{i}</tspan><tspan dy="5"> </tspan>'
def L(a, b, cls):
    return f'<path class="{cls}" d="M{n1(a[0])} {n1(a[1])}L{n1(b[0])} {n1(b[1])}"/>'
def PL(pts, cls, closed=False):
    return f'<path class="{cls}" d="M' + "L".join(f"{n1(x)} {n1(y)}" for x, y in pts) + ("Z" if closed else "") + '"/>'
def C(c, r, cls):
    return f'<circle class="{cls}" cx="{n1(c[0])}" cy="{n1(c[1])}" r="{n1(r)}"/>'
def lead(a, b, dot=True):
    return L(a, b, "pl-lead") + (C(b, 1.15, "pl-ldot") if dot else "")
def callout(x, y, head, subline=None, anchor="start", cls=""):
    """mono-caps headline with an italic subline (the Fig. 1 caption style)"""
    out = T(x, y, head, f"pl-cap {cls}".strip(), anchor)
    if subline:
        out += T(x, y + 9.5, subline, f"pl-caps {cls}".strip(), anchor)
    return out
def panel(x, y, label, head, subline=None):
    """panel label (a), (b) ... with its headline"""
    return T(x, y, label, "pl-panel", "start") + callout(x + 20, y, head, subline)
def subsup(b, sb, sp, cls="pl-sub"):
    return (f'{b}<tspan class="{cls}" dy="-5">{sp}</tspan><tspan class="{cls}" dx="-{0.36 * len(sp) + 0.2:.2f}em" dy="8">{sb}</tspan>'
            f'<tspan dy="-3"> </tspan>')
def arrow_head(tip, ang, size=5.2, cls="pl-tip"):
    a = math.radians(ang); pts = [tip]
    for s in (-1, 1):
        b = a + math.pi + s * math.radians(26)
        pts.append((tip[0] + size * math.cos(b), tip[1] + size * math.sin(b)))
    return PL([pts[1], pts[0], pts[2]], cls, closed=True)
def arrow(a, b, cls="pl-arrow", head=5.2, hcls="pl-tip"):
    ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
    return L(a, b, cls) + arrow_head(b, ang, head, hcls)
def circled(c, k, cls="pl-num"):
    return C(c, 6.2, f"{cls}-c") + T(c[0], c[1] + 2.3, str(k), cls)

def legend_item(icon, label):
    return f'<li>{icon}<span>{label}</span></li>'
ICON = {
    "vertex": '<svg viewBox="0 0 22 19" aria-hidden="true" class="pl-lg-v"><path d="M3.2 2.4 L18.8 2.4 L11 15.9 Z" class="f1-lg-tri"/>'
              '<circle cx="11" cy="7.4" r="2.1" class="f1-lg-s"/><circle cx="3.2" cy="2.4" r="2.1" class="f1-lg-s"/>'
              '<circle cx="18.8" cy="2.4" r="2.1" class="f1-lg-s f1-lg-s1"/><circle cx="11" cy="15.9" r="2.1" class="f1-lg-s f1-lg-s1"/></svg>',
    "singlet": '<svg viewBox="0 0 26 12" aria-hidden="true"><path d="M5 6 H21" class="f1-lg-lobe"/><path d="M5 6 H21" class="f1-lg-lobec"/>'
               '<circle cx="5" cy="6" r="2.1" class="f1-lg-s f1-lg-s1"/><circle cx="21" cy="6" r="2.1" class="f1-lg-s f1-lg-s1"/></svg>',
    "tube": '<svg viewBox="0 0 26 12" aria-hidden="true"><path d="M2 6 H24" class="f1-lg-tube"/></svg>',
    "outline": '<svg viewBox="0 0 30 14" aria-hidden="true"><rect x="1.5" y="1.5" width="27" height="11" rx="5.5" class="pl-lg-ol"/></svg>',
    "outline-gold": '<svg viewBox="0 0 30 14" aria-hidden="true"><rect x="1.5" y="1.5" width="27" height="11" rx="5.5" class="pl-lg-gc"/></svg>',
    "curve": '<svg viewBox="0 0 26 12" aria-hidden="true"><path d="M2 9 C8 9 9 3 14 3 S20 6 24 6" class="pl-lg-curve"/></svg>',
    "curve-iv": '<svg viewBox="0 0 26 12" aria-hidden="true"><path d="M2 9 C8 9 9 3 14 3 S20 6 24 6" class="pl-lg-curve-iv"/></svg>',
    "level": '<svg viewBox="0 0 26 12" aria-hidden="true"><path d="M3 6 H23" class="pl-lg-level"/></svg>',
    "doublet": '<svg viewBox="0 0 26 12" aria-hidden="true"><path d="M3 4.4 H23 M3 7.6 H23" class="pl-lg-doublet"/></svg>',
    "area": '<svg viewBox="0 0 26 14" aria-hidden="true"><path d="M4 3 H20 C23 6 22 9 20 11 H6 C3 8 3 6 4 3 Z" class="pl-lg-area"/></svg>',
    "site": '<svg viewBox="0 0 16 16" aria-hidden="true" class="pl-lg-sq"><circle cx="8" cy="8" r="4.2" class="pl-lg-site"/></svg>',
    "bond": '<svg viewBox="0 0 26 12" aria-hidden="true"><path d="M2 6 H24" class="pl-lg-bond"/></svg>',
    "bond2": '<svg viewBox="0 0 26 12" aria-hidden="true"><path d="M2 6 H24" class="pl-lg-bond2"/></svg>',
    "track": '<svg viewBox="0 0 26 12" aria-hidden="true"><path d="M2 6 H24" class="pl-lg-track"/></svg>',
    "photon": '<svg viewBox="0 0 26 12" aria-hidden="true"><path d="M2 6 H24" class="pl-lg-photon"/></svg>',
    "signal": '<svg viewBox="0 0 26 12" aria-hidden="true"><path d="M2 6 H20" class="pl-lg-signal"/><path d="M17 3 L22 6 L17 9" class="pl-lg-signal"/></svg>',
    "flow": '<svg viewBox="0 0 26 12" aria-hidden="true"><path d="M2 6 H20" class="pl-lg-flow"/><path d="M17 3 L22 6 L17 9" class="pl-lg-flow"/></svg>',
    "est": '<svg viewBox="0 0 26 12" aria-hidden="true"><path d="M2 6 H24" class="pl-lg-est"/><circle cx="24" cy="6" r="2.2" class="pl-lg-est-d"/></svg>',
    "dev": '<svg viewBox="0 0 26 12" aria-hidden="true"><path d="M2 6 H24" class="pl-lg-dev"/><circle cx="24" cy="6" r="2.2" class="pl-lg-dev-d"/></svg>',
    "base": '<svg viewBox="0 0 26 12" aria-hidden="true"><path d="M2 6 H24" class="pl-lg-base"/><circle cx="24" cy="6" r="2.2" class="pl-lg-base-d"/></svg>',
    "ring-est": '<svg viewBox="0 0 30 14" aria-hidden="true"><ellipse cx="15" cy="7" rx="13" ry="5.5" class="pl-lg-ol"/></svg>',
    "ring-dev": '<svg viewBox="0 0 30 14" aria-hidden="true"><ellipse cx="15" cy="7" rx="13" ry="5.5" class="pl-lg-gc"/></svg>',
}

def svg_wrap(vw, vh, body, title):
    return (f'<svg class="pl-svg" viewBox="0 0 {vw} {vh}" role="img" aria-label="{html.escape(title)}" focusable="false">'
            f'{body}</svg>')

def plate(fig, key, title, context, stage, legend, note, aria, kind="svg"):
    """the shared plate: header, stage (svg, or svg + html nodes for the maps), legend, source note"""
    tid = f"fig{fig}-title"
    lg = "".join(legend_item(ICON[i], lab) for i, lab in legend)
    cls = "plate plate-svg" if kind == "svg" else f"plate schematic schematic-{key}"
    return (f'<figure class="{cls} plate-{key}" aria-labelledby="{tid}">'
            f'<header class="diagram-header plate-header"><p class="diagram-eyebrow">Fig.&#8201;{fig}</p>'
            f'<h3 id="{tid}">{title}</h3><p class="diagram-context">{context}</p></header>'
            f'<div class="plate-stage{"" if kind == "svg" else " schematic-stage"}">{stage}</div>'
            f'<ul class="plate-legend">{lg}</ul>'
            f'<p class="plate-note">{note}</p>'
            f'<figcaption class="sr-only">{html.escape(aria)}</figcaption></figure>')


# ================================================================ Fig. 7: the C2 patch of the thesis
def lattice_state(u, dx, dy):
    """static drawing of the exact Fig. 1 state at storyboard time u (Gauss law checked in tools/fig1.py)"""
    F = fig1
    sample = lambda tid, typ: F.TR[f"{tid}:{typ}"].sample(u)
    out = [f'<g transform="translate({n1(dx)} {n1(dy)})">']
    # glows of the active corridor links, under everything
    for lid in F.T_LINKS:
        o = sample(f"f1-kg{lid}", "op")[0]
        if o > 0.01:
            d = F.seg(F.P[f"r{lid}L"], F.P[f"r{lid}R"])
            out.append(f'<g class="f1-kg" style="opacity:{o:.2f}"><path class="f1-kg1" d="{d}"/><path class="f1-kg2" d="{d}"/></g>')
    out.append("".join(f'<path class="f1-tri" d="{F.Pd(F.tri_pts(v))} Z"/>' for v in F.V))
    out.append("".join(f'<path class="f1-lk" d="{F.seg(F.P[f"r{lid}L"], F.P[f"r{lid}R"])}"/>' for lid in F.LINKS))
    for (lid, c) in F.AK:
        o = sample(f"f1-ak{lid}{c}", "op")[0]
        if o > 0.01:
            out.append(f'<path class="f1-ak f1-ak-{c}" d="{F.seg(F.P[f"r{lid}L"], F.P[f"r{lid}R"])}" style="opacity:{o:.2f}"/>')
    for name, d_ in F.LOBE.items():
        x1, y1, x2, y2 = sample(f"f1-lb-{name}", "ln")
        for c in d_["layers"]:
            o = sample(f"f1-lb-{name}-{c}", "op")[0]
            if o > 0.01:
                dd = f"M{x1:.2f} {y1:.2f}L{x2:.2f} {y2:.2f}"
                out.append(f'<g class="f1-lb f1-lb-{c}" style="opacity:{o:.2f}"><path class="f1-lo" d="{dd}"/>'
                           f'<path class="f1-lm" d="{dd}"/><path class="f1-lc" d="{dd}"/></g>')
    for s in F.OCC:
        x, y = F.P[s]; o = sample(f"f1-s-{s}", "occ")[0]
        out.append(f'<circle class="f1-sh" cx="{x:.2f}" cy="{y:.2f}" r="{F.RS + 2.3:.2f}" style="opacity:{max(0, o - 1):.2f}"/>'
                   f'<circle class="f1-sr" cx="{x:.2f}" cy="{y:.2f}" r="{F.RS:.2f}"/>'
                   f'<circle class="f1-sf" cx="{x:.2f}" cy="{y:.2f}" r="{F.RS - 0.25:.2f}" style="opacity:{F.fill_op(o):.2f}"/>')
    loops = F.ol_loops(u)
    if loops:
        d = F.ol_d(loops)
        out.append(f'<path class="f1-ol-g pl-olpath" d="{d}"/><path class="f1-ol-p pl-olpath" d="{d}"/>')
    for key, lab, q3, lx, qx, anc in (("Q", "Q", "+1", -11.5, -6, "end"), ("Qb", "Q̄", "−1", 11.5, 6, "start")):
        x, y = F.P[key]
        out.append(f'<circle class="f1-src" cx="{x:.2f}" cy="{y:.2f}" r="7.6"/><circle class="f1-srcs" cx="{x:.2f}" cy="{y:.2f}" r="{F.RS + 0.5:.2f}"/>')
        out.append(T(x + lx, y + 4.5, lab, "f1-srcl", anc) + T(x + qx, y + 22, f'{sup("q", "3")}= {q3}', "f1-srcq", anc))
    labels = [t for t in F.LBL if 'id="f1-l' not in t]          # link and vertex labels, without the runtime q labels
    out.append('<g class="pl-labels">' + "".join(labels) + '</g>')
    out.append('</g>')
    return "".join(out)

def fig7():
    W_, H_ = 600, 520
    u = 0.505                                              # m = 4 ground state: the formed tube (Fig. 1 storyboard)
    dx, dy = -34.0, 40.0
    o = []
    o.append(lattice_state(u, dx, dy))
    o.append(panel(14, 18, "(a)", "C₂ PATCH · OPEN 3 × 2 HONEYCOMB", f'{sub("N", "v")}= 12 · {sub("N", "ℓ")}= 13 · two plaquettes'))
    o.append(callout(586, 18, "SOURCE CORRIDOR", "graph distance R = 4 · m = 4 ground state", "end"))
    # the tube: caption in ring B with a leader to the shared edge
    m10 = fig1.lmid(10); tip = (m10[0] + dx + 14.5, m10[1] + dy - 6)
    o.append(lead((tip[0] + 15, tip[1] - 12), tip) + callout(tip[0] + 18, tip[1] - 17, "FLUX TUBE", "one singlet chain from Q to Q̄"))
    # ---- insets
    y0 = 296
    o.append(L((14, y0 - 12), (586, y0 - 12), "pl-rule"))
    for x in (208, 402):
        o.append(L((x, y0), (x, 470), "pl-rule"))
    # (b) Gauss law at a vertex: an A vertex holding one matter-rishon singlet
    o.append(panel(14, y0 + 6, "(b)", "GAUSS LAW AT A VERTEX"))
    cx, cy, sc = 64, y0 + 68, 2.15
    tri = [(cx + sc * 18 * a, cy + sc * 18 * b) for a, b in fig1.TRI["A"]]
    o.append(PL(tri, "f1-tri pl-tri-big", closed=True))
    m = (cx, cy); rk = tri[1]
    o.append(f'<g class="f1-lb f1-lb-t pl-lobe-big"><path class="f1-lo" d="M{n1(m[0])} {n1(m[1])}L{n1(rk[0])} {n1(rk[1])}"/>'
             f'<path class="f1-lm" d="M{n1(m[0])} {n1(m[1])}L{n1(rk[0])} {n1(rk[1])}"/><path class="f1-lc" d="M{n1(m[0])} {n1(m[1])}L{n1(rk[0])} {n1(rk[1])}"/></g>')
    for p_, filled in ((m, True), (tri[0], False), (tri[1], True), (tri[2], False)):
        o.append(C(p_, 5.2, "f1-sr pl-site-big") + (C(p_, 4.9, "f1-sf") if filled else ""))
    o.append(T(m[0] + 9, m[1] + 14, "ψ", "pl-t pl-ti", "start"))
    o.append(T(tri[0][0] - 2, tri[0][1] - 9, sub("c", "ℓ"), "pl-ts pl-ti", "middle"))
    o.append(T(tri[1][0] + 2, tri[1][1] - 9, sub("c", "ℓ′"), "pl-ts pl-ti", "middle"))
    o.append(T(tri[2][0] + 10, tri[2][1] + 3, sub("c", "ℓ″"), "pl-ts pl-ti", "start"))
    o.append(T(118, y0 + 52, f'{subsup("G", "v", "a")}|ψ⟩ = 0', "pl-t pl-ti", "start"))
    o.append(T(118, y0 + 70, "every vertex is an", "pl-ts", "start"))
    o.append(T(118, y0 + 83, "SU(2) colour singlet", "pl-ts", "start"))
    o.append(T(118, y0 + 109, f'{sub("D", "v")}= {sub("n", "v")}− Σ {sub("n", "ℓ,v")}', "pl-ts pl-ti", "start"))
    o.append(T(118, y0 + 122, "conserved sector label", "pl-ts", "start"))
    # (c) the six-state two-rishon link: three of its states
    o.append(panel(222, y0 + 6, "(c)", "TWO-RISHON LINK", f'{sub("n", "L")}+ {sub("n", "R")}= 2'))
    rows = [("|0,2⟩", (0, 2), "0", "vacuum"), ("|1,1⟩", (1, 1), "¾", "flux"), ("|2,0⟩", (2, 0), "0", "")]
    for k, (ket, (nl, nr), e2, tag) in enumerate(rows):
        y = y0 + 52 + k * 36; xl, xr = 268, 330
        if nl == 1:
            o.append(f'<g class="f1-kg"><path class="f1-kg1" d="M{xl} {y}L{xr} {y}"/><path class="f1-kg2" d="M{xl} {y}L{xr} {y}"/></g>')
            o.append(L((xl, y), (xr, y), "f1-ak f1-ak-t"))
        else:
            o.append(L((xl, y), (xr, y), "f1-lk"))
        for x, n in ((xl, nl), (xr, nr)):
            if n == 2:
                o.append(C((x, y), fig1.RS + 2.3, "f1-sh"))
            o.append(C((x, y), fig1.RS, "f1-sr"))
            if n:
                o.append(f'<circle class="f1-sf" cx="{x}" cy="{y}" r="{fig1.RS - 0.25:.2f}" style="opacity:{1 if n == 1 else 0.55}"/>')
        o.append(T(258, y + 3.6, ket, "pl-t", "end"))
        o.append(T(342, y + 3.6, f'{sup("E", "2")}= {e2}', "pl-t pl-ti", "start"))
    o.append(T(222, y0 + 160, f'{sup("E", "2")}= ¾ {sub("n", "L")}{sub("n", "R")} · six states per link', "pl-ts", "start"))
    # (d) exact real-time data of the breaking quench (thesis Ch. IV)
    o.append(panel(416, y0 + 6, "(d)", "BREAKING QUENCH", "exact · κ = 0, R = 4"))
    ax0, ax1, ay0, ay1 = 434, 578, y0 + 34, y0 + 132
    o.append(L((ax0, ay1), (ax1, ay1), "pl-ax") + L((ax0, ay1), (ax0, ay0), "pl-ax"))
    o.append(L((ax0, (ay0 + ay1) / 2), (ax1, (ay0 + ay1) / 2), "pl-half"))
    q = fig1.RT["q"]
    X = lambda t: ax0 + (ax1 - ax0) * t / 2
    Y = lambda p: ay1 - (ay1 - ay0) * p
    o.append(PL([(X(t), Y(p)) for t, p in zip(q["t"], q["conn"])], "pl-curve"))
    o.append(PL([(X(t), Y(a + b)) for t, a, b in zip(q["t"], q["f1"], q["f2"])], "pl-curve-iv"))
    for t in (0, 1, 2):
        o.append(L((X(t), ay1), (X(t), ay1 + 3), "pl-ax") + T(X(t), ay1 + 12, str(t), "pl-num-t"))
    o.append(T(ax0 - 4, ay0 + 3, "1", "pl-num-t", "end") + T(ax0 - 4, ay1 + 3, "0", "pl-num-t", "end"))
    o.append(T(ax1 + 6, ay1 + 3, "t", "pl-t pl-ti", "start"))
    o.append(T(X(0.18), Y(0.93) - 6, sub("P", "conn"), "pl-ts pl-ti pl-tq", "start"))
    o.append(T(X(1.25), Y(0.74) - 7, sub("P", "≥1ff"), "pl-ts pl-ti pl-tiv", "start"))
    o.append(T(416, y0 + 160, "m: 4 → 0.5 at t = 0 · g² = 2", "pl-ts", "start"))
    body = "".join(o)
    stage = svg_wrap(W_, H_ - 30, body, "C2 patch of the thesis in the m = 4 ground state with the flux tube between the sources, "
                     "Gauss law at a vertex, the two-rishon link states and the exact breaking-quench probabilities")
    return plate(7, "msc", "Source-Supported Flux", "C₂ patch · two-rishon SU(2) quantum links", stage,
                 [("vertex", 'vertex · matter + rishon sites'), ("singlet", "SU(2) singlet"), ("tube", "flux tube · <math><mi>Q</mi><mo>…</mo><mover><mi>Q</mi><mo>‾</mo></mover></math>"),
                  ("outline", "one colour-singlet object")],
                 'Geometry of thesis Fig. II.1; panel (d) exact data of thesis Ch. IV. Singlet notation after Halimeh <i>et al.</i>, '
                 'PRX Quantum <b>5</b>, 030358 (2024).',
                 "Fig. 7: the C2 patch in the m = 4 ground state; Gauss law at a vertex; two-rishon link states; exact breaking-quench data.")


# ================================================================ Fig. 8: the quantum heat engine
# Spectrum of the drawn well V(x) = x²/2 + V0 exp(-x²/2b²), hbar = m = omega = 1, V0 = 10, b = 0.7 (finite differences, 1600
# points on [-9, 9]); the article's model has a position-dependent mass, the doublet structure is the same.
HE_V0, HE_B = 10.0, 0.7
HE_LEVELS = [3.125, 3.126, 5.234, 5.249, 7.139, 7.213, 8.844, 9.102, 10.397, 10.963, 12.03]
def fig8():
    W_, H_ = 600, 446
    o = []
    V = lambda x: 0.5 * x * x + HE_V0 * math.exp(-x * x / (2 * HE_B ** 2))
    X0p, X1p, xr = 46, 276, 5.15
    Ey0, Ey1, Emax = 368, 70, 13.6
    X = lambda x: X0p + (X1p - X0p) * (x + xr) / (2 * xr)
    Y = lambda E: Ey0 - (Ey0 - Ey1) * E / Emax
    o.append(panel(14, 18, "(a)", "OSCILLATOR-SHAPED WELL", "inserted barrier · near-degenerate doublets"))
    o.append(L((X0p - 6, Ey0), (X1p + 8, Ey0), "pl-ax") + L((X0p - 6, Ey0), (X0p - 6, Ey1 - 8), "pl-ax"))
    o.append(T(X1p + 12, Ey0 + 4, "x", "pl-t pl-ti", "start") + T(X0p - 6, Ey1 - 14, "E", "pl-t pl-ti"))
    # levels: inside the classically allowed region of the drawn potential
    def allowed(E):
        xs = [-xr + 2 * xr * i / 800 for i in range(801)]
        segs, cur = [], None
        for x in xs:
            if E > V(x) and cur is None: cur = x
            if E <= V(x) and cur is not None: segs.append((cur, x)); cur = None
        if cur is not None: segs.append((cur, xs[-1]))
        return segs
    for k, E in enumerate(HE_LEVELS):
        below = E < HE_V0
        for a, b in allowed(E):
            o.append(L((X(a) + 1.5, Y(E)), (X(b) - 1.5, Y(E)), "pl-level-d" if below else "pl-level"))
    o.append(PL([(X(-xr + 2 * xr * i / 300), Y(V(-xr + 2 * xr * i / 300))) for i in range(301)], "pl-curve"))
    o.append(L((X(-0.9), Y(HE_V0)), (X(0.9), Y(HE_V0)), "pl-half"))
    o.append(T(X(0) , Y(HE_V0) - 7, sub("V", "0"), "pl-ts pl-ti"))
    # doublets: one outline each, in the right well
    for k in range(4):
        E1, E2 = HE_LEVELS[2 * k], HE_LEVELS[2 * k + 1]
        segs = allowed(E1)
        a, b = segs[-1]
        y1, y2 = Y(E2), Y(E1)
        o.append(f'<rect class="pl-gc" x="{n1(X(a) - 3)}" y="{n1(y1 - 4.5)}" width="{n1(X(b) - X(a) + 6)}" height="{n1(y2 - y1 + 9)}" rx="{n1((y2 - y1 + 9) / 2)}"/>')
    lo = allowed(HE_LEVELS[0])[-1]
    tip = (X(lo[1]) + 4, Y(HE_LEVELS[0]) + 1)
    o.append(lead((tip[0] - 2, Ey0 + 18), tip) + callout(tip[0] - 4, Ey0 + 25, "LEVEL DEGENERACY", "splitting Δₙ → 0 deep below the barrier", "end"))
    o.append(T(X(-4.2), Y(12.6), "V(x)", "pl-t pl-ti", "middle"))
    # (b) T-S plane, Stirling cycle (schematic)
    ox, oy, ex, ey = 336, 300, 576, 76
    o.append(panel(316, 18, "(b)", "STIRLING-LIKE CYCLE", "two isotherms · two isochores"))
    o.append(L((ox, oy), (ex, oy), "pl-ax") + L((ox, oy), (ox, ey), "pl-ax"))
    o.append(T(ex + 5, oy + 4, "S", "pl-t pl-ti", "start") + T(ox, ey - 7, "T", "pl-t pl-ti"))
    Th, Tc = 128, 254
    S1, S2, S3, S4 = 392, 528, 506, 372
    cyc = (f"M{S1} {Th} L{S2} {Th} C{S2 + 16} {Th + 44}, {S3 + 20} {Tc - 52}, {S3} {Tc} "
           f"L{S4} {Tc} C{S4 - 20} {Tc - 52}, {S1 - 16} {Th + 44}, {S1} {Th} Z")
    o.append(f'<path class="pl-area" d="{cyc}"/><path class="pl-curve" d="{cyc}"/>')
    o.append(L((ox, Th), (S1 - 7, Th), "pl-half") + L((ox, Tc), (S4 - 7, Tc), "pl-half"))
    o.append(T(ox - 6, Th + 4, sub("T", "h"), "pl-t pl-ti", "end") + T(ox - 6, Tc + 4, sub("T", "c"), "pl-t pl-ti", "end"))
    o.append(arrow_head(((S1 + S2) / 2 + 6, Th), 0, 6) + arrow_head(((S3 + S4) / 2 - 6, Tc), 180, 6))
    def bez(p0, c1, c2, p3, t):
        return tuple((1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t * t * c + t ** 3 * d for a, b, c, d in zip(p0, c1, c2, p3))
    for p0, c1, c2, p3 in (((S2, Th), (S2 + 16, Th + 44), (S3 + 20, Tc - 52), (S3, Tc)), ((S4, Tc), (S4 - 20, Tc - 52), (S1 - 16, Th + 44), (S1, Th))):
        m_, m2 = bez(p0, c1, c2, p3, 0.5), bez(p0, c1, c2, p3, 0.52)
        o.append(arrow_head(m2, math.degrees(math.atan2(m2[1] - m_[1], m2[0] - m_[0])), 6))
    for k, (pnt, off) in enumerate((((S1, Th), (-9, -10)), ((S2, Th), (9, -10)), ((S3, Tc), (10, 11)), ((S4, Tc), (-10, 11))), 1):
        o.append(C(pnt, 2.3, "pl-dotc") + circled((pnt[0] + off[0], pnt[1] + off[1]), k))
    o.append(T((S1 + S2) / 2, Th - 9, f'{sub("Q", "h")} absorbed', "pl-ts pl-ti"))
    o.append(T((S3 + S4) / 2, Tc + 19, f'{sub("Q", "c")} released', "pl-ts pl-ti"))
    o.append(T((S1 + S2) / 2 - 4, (Th + Tc) / 2 + 4, "W = ∮ T dS", "pl-t pl-ti"))
    o.append(callout(336, 336, "PERFORMANCE", None))
    o.append(T(336, 352, f'η = W / {sub("Q", "h")} ≤ 1 − {sub("T", "c")} / {sub("T", "h")}', "pl-t pl-ti", "start"))
    o.append(T(336, 368, "classical limit at large ω · Carnot limit at low T", "pl-ts", "start"))
    o.append(T(14, 432, f'Isotherms 1→2 at {sub("T", "h")} and 3→4 at {sub("T", "c")} exchange heat; isochores 2→3 and 4→1 change T at a fixed spectrum.', "pl-ts", "start"))
    stage = svg_wrap(W_, H_, "".join(o), "Spectrum of an oscillator-shaped well with a central barrier, showing tunnel-split doublets, "
                     "and a Stirling-like cycle in the temperature-entropy plane")
    return plate(8, "heat", "Degeneracy-Driven Stirling Cycle", "Szilard-like engine · oscillator-shaped well", stage,
                 [("curve", "potential V(x) · cycle"), ("doublet", "levels below the barrier"), ("level", "levels above"),
                  ("outline-gold", "near-degenerate doublet"), ("area", "work W")],
                 "Levels: exact spectrum of the drawn well (ħ = m = ω = 1, V₀ = 10); the article treats a position-dependent mass. "
                 "Cycle schematic. Evkaya, Ökcü &amp; Aydiner, Int. J. Theor. Phys. <b>62</b>, 237 (2023).",
                 "Fig. 8: barrier-induced near-degeneracy in an oscillator-shaped well drives a Stirling-like quantum cycle.")


# ================================================================ Fig. 9: the B.Sc. thesis
def fig9():
    W_, H_ = 600, 440
    o = []
    o.append(panel(14, 18, "(a)", "FRUSTRATED TRIANGULAR CHAIN", "quasi-1D zigzag · dimerised XY / XX couplings"))
    top = [(96 + 84 * k, 112) for k in range(5)]
    bot = [(138 + 84 * k, 188) for k in range(5)]
    tri = [top[1], bot[1], top[2]]
    # J2 along the legs, J1 on the zigzag (alternating strength: dimerisation)
    for row in (top, bot):
        for a, b in zip(row, row[1:]):
            o.append(L(a, b, "pl-bond2"))
    zig = []
    for k in range(5):
        zig.append(top[k]); zig.append(bot[k])
    for i, (a, b) in enumerate(zip(zig, zig[1:])):
        o.append(L(a, b, "pl-bond pl-bond-s" if i % 2 == 0 else "pl-bond pl-bond-w"))
    cx = sum(p[0] for p in tri) / 3; cy = sum(p[1] for p in tri) / 3
    grow = lambda p, f: (cx + (p[0] - cx) * f, cy + (p[1] - cy) * f)
    big = [grow(p, 1.42) for p in tri]
    o.append(f'<path class="pl-gc" d="M{n1(big[0][0])} {n1(big[0][1])}L{n1(big[1][0])} {n1(big[1][1])}L{n1(big[2][0])} {n1(big[2][1])}Z" stroke-linejoin="round"/>')
    spins = {0: 1, 1: -1, 2: 1, 3: -1, 4: 1}
    for k, (x, y) in enumerate(top + bot):
        o.append(C((x, y), 7.2, "pl-site"))
    # spins: antiparallel pairs, the third spin of the marked triangle cannot satisfy both bonds
    for (x, y), s_ in ((top[1], 1), (bot[1], -1)):
        o.append(arrow((x, y + 4.6 * s_), (x, y - 4.6 * s_), "pl-spin", 3.4, "pl-tip-iv"))
    o.append(T(top[2][0], top[2][1] + 4.4, "?", "pl-t pl-q"))
    o.append(T((top[0][0] + top[1][0]) / 2, top[0][1] - 9, sub("J", "2"), "pl-t pl-ti pl-hl"))
    zb = ((top[3][0] + bot[3][0]) / 2, (top[3][1] + bot[3][1]) / 2)
    o.append(T(zb[0] - 11, zb[1] + 2, sub("J", "1"), "pl-t pl-ti pl-hl", "end"))
    o.append(T(zb[0] + 46, zb[1] + 2, f'{sub("J", "1")}(1 − δ)', "pl-ts pl-ti pl-hl", "start"))
    tp = grow(tri[1], 1.42)
    o.append(lead((tp[0] - 34, tp[1] + 30), (tp[0] - 4, tp[1] + 6)) + callout(tp[0] - 36, tp[1] + 38, "FRUSTRATION", f'{sub("J", "1")} and {sub("J", "2")} compete on every triangle', "end"))
    # complex field
    fx = 552
    for yy in (100, 150, 200):
        o.append(arrow((fx, yy + 15), (fx, yy - 15), "pl-arrow-iv", 4.6, "pl-tip-iv"))
    o.append(callout(586, 236, "TRANSVERSE COMPLEX FIELD", None, "end"))
    o.append(T(586, 252, f'h = {sub("h", "r")}+ i {sub("h", "i")}', "pl-t pl-ti", "end"))
    # (b) analytical route
    y = 318
    o.append(L((14, 268), (586, 268), "pl-rule"))
    o.append(panel(14, 290, "(b)", "ANALYTICAL ROUTE", "exact solution through free fermions"))
    steps = [("SPIN CHAIN", f'{sub("H", "XY")}, {sub("H", "XX")}'), ("JORDAN–WIGNER", f'σ → {sub("c", "j")}'),
             ("FOURIER", f'{sub("c", "j")}→ {sub("c", "k")}'), ("BOGOLIUBOV", f'{sub("c", "k")}→ {sub("γ", "k")}'),
             ("ENTANGLEMENT", f'{sub("S", "vN")}= −Tr ρ ln ρ')]
    xs = [62 + 119 * i for i in range(5)]
    for i, ((head, form), x) in enumerate(zip(steps, xs)):
        o.append(C((x, y + 24), 9, "pl-step-c" if i < 4 else "pl-step-c pl-step-end") + T(x, y + 27.4, str(i + 1), "pl-step"))
        o.append(T(x, y + 52, head, "pl-cap"))
        o.append(T(x, y + 68, form, "pl-ts pl-ti"))
        if i < 4:
            o.append(arrow((x + 13, y + 24), (xs[i + 1] - 13, y + 24), "pl-arrow", 4.4))
    o.append(T(14, 420, "Thermal and ground-state entropies follow from the Bogoliubov quasiparticle occupations at temperature T.", "pl-ts", "start"))
    stage = svg_wrap(W_, H_, "".join(o), "Zigzag triangular spin chain with dimerised nearest-neighbour and next-nearest-neighbour couplings, "
                     "a frustrated triangle and a complex field, and the five-step analytical route to the entanglement entropy")
    return plate(9, "bsc", "Frustrated Non-Hermitian Spin Chain", "entanglement in a dimerised zigzag chain", stage,
                 [("site", "spin-½ site"), ("bond", f"J<sub>1</sub> zigzag (dimerised)"), ("bond2", "J<sub>2</sub> along the legs"),
                  ("outline-gold", "frustrated triangle"), ("flow", "analytical step")],
                 "B.Sc. thesis, İstanbul University (2024): exact solution by Jordan–Wigner, Fourier and Bogoliubov transformations; "
                 "thermal and ground-state entanglement entropies.",
                 "Fig. 9: frustrated, dimerised zigzag chain with a complex field and the free-fermion route to the entanglement entropy.")


# ================================================================ Fig. 10: the cosmic-muon detector
def fig10():
    W_, H_ = 600, 400
    o = []
    o.append(panel(14, 18, "(a)", "SIGNAL CHAIN", "from one muon transit to one audible click"))
    # 1. scintillator with the muon track and photons
    sx, sy, sw, sh = 44, 128, 152, 66
    o.append(f'<rect class="pl-box" x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="2"/>')
    trk = [(84, 58), (150, 252)]
    hit = (84 + (150 - 84) * (sy + sh / 2 - 58) / (252 - 58), sy + sh / 2)
    o.append(L(trk[0], (trk[0][0] + (trk[1][0] - trk[0][0]) * 0.33, trk[0][1] + (trk[1][1] - trk[0][1]) * 0.33), "pl-track"))
    o.append(L((trk[0][0] + (trk[1][0] - trk[0][0]) * 0.33, trk[0][1] + (trk[1][1] - trk[0][1]) * 0.33), trk[1], "pl-track pl-track-in"))
    o.append(arrow_head(trk[1], math.degrees(math.atan2(trk[1][1] - trk[0][1], trk[1][0] - trk[0][0])), 6, "pl-tip-iv"))
    o.append(T(trk[0][0] - 6, trk[0][1] + 2, "μ", "pl-t pl-ti pl-big", "end"))
    for dy_ in (-16, -6, 6, 16):
        o.append(L(hit, (sx + sw + 4, hit[1] + dy_ * 0.9), "pl-photon"))
    o.append(C(hit, 5, "pl-halo") + C(hit, 2, "pl-dotc"))
    # light guide and PMT
    lg = [(sx + sw, sy + 4), (sx + sw + 30, sy + 14), (sx + sw + 30, sy + sh - 14), (sx + sw, sy + sh - 4)]
    o.append(PL(lg, "pl-box", closed=True))
    px, py, pw, ph = sx + sw + 30, sy + 10, 118, sh - 20
    o.append(f'<rect class="pl-box" x="{px}" y="{py}" width="{pw}" height="{ph}" rx="6"/>')
    o.append(L((px + 10, py + 4), (px + 10, py + ph - 4), "pl-cathode"))
    dyn = [(px + 24 + 12 * i, py + (8 if i % 2 else ph - 8)) for i in range(8)]
    o.append(PL(dyn, "pl-signal-thin"))
    # oscilloscope
    ox, oy, ow, oh = 418, 106, 160, 108
    o.append(arrow((px + pw + 2, sy + sh / 2), (ox - 3, sy + sh / 2), "pl-signal", 4.6))
    o.append(f'<rect class="pl-box pl-box-strong" x="{ox}" y="{oy}" width="{ow}" height="{oh}" rx="3"/>')
    for gx in range(1, 4): o.append(L((ox + gx * ow / 4, oy), (ox + gx * ow / 4, oy + oh), "pl-grid"))
    for gy in range(1, 3): o.append(L((ox, oy + gy * oh / 3), (ox + ow, oy + gy * oh / 3), "pl-grid"))
    base = oy + 38
    pulse = [(ox + 8, base), (ox + 58, base), (ox + 64, base + 2), (ox + 70, base + 56), (ox + 78, base + 20), (ox + 92, base + 5), (ox + ow - 8, base)]
    o.append(f'<path class="pl-curve" d="M{n1(pulse[0][0])} {n1(pulse[0][1])} L{n1(pulse[1][0])} {n1(pulse[1][1])} '
             f'C{n1(pulse[2][0])} {n1(pulse[2][1])}, {n1(pulse[3][0] - 4)} {n1(pulse[3][1])}, {n1(pulse[3][0])} {n1(pulse[3][1])} '
             f'C{n1(pulse[3][0] + 4)} {n1(pulse[3][1])}, {n1(pulse[4][0])} {n1(pulse[4][1])}, {n1(pulse[5][0])} {n1(pulse[5][1])} '
             f'L{n1(pulse[6][0])} {n1(pulse[6][1])}"/>')
    # LM555 and speaker
    jx = px + pw + 16
    o.append(C((jx, sy + sh / 2), 2.4, "pl-dotc"))
    o.append(f'<path class="pl-signal" d="M{jx} {sy + sh / 2} L{jx} 306 L{ox - 3} 306"/>' + arrow_head((ox - 3, 306), 0, 4.6, "pl-tip"))
    o.append(f'<rect class="pl-box" x="{ox}" y="282" width="98" height="48" rx="3"/>')
    o.append(T(ox + 49, 302, "LM555", "pl-cap") + T(ox + 49, 319, "V → f", "pl-t pl-ti"))
    o.append(arrow((ox + 100, 306), (ox + 118, 306), "pl-signal", 4.6))
    spk = [(ox + 120, 299), (ox + 130, 299), (ox + 142, 289), (ox + 142, 323), (ox + 130, 313), (ox + 120, 313)]
    o.append(PL(spk, "pl-box", closed=True))
    for i, rr in enumerate((7, 13)):
        o.append(f'<path class="pl-wave" d="M{ox + 148 + i * 5} {306 - rr * 0.72:.1f} A{rr} {rr} 0 0 1 {ox + 148 + i * 5} {306 + rr * 0.72:.1f}"/>')
    # numbered stage captions
    o.append(circled((sx + 74, sy - 31), 1) + callout(sx + 86, sy - 28, "SCINTILLATION", "plastic · blue light"))
    o.append(circled((px + 14, sy - 31), 2) + callout(px + 26, sy - 28, "PHOTOMULTIPLIER", "photocathode → dynodes · 800 V"))
    o.append(circled((ox + 8, oy - 16), 3) + callout(ox + 20, oy - 13, "READOUT", "negative PMT pulse"))
    o.append(circled((ox - 14, 259), 4) + callout(ox - 2, 262, "SONIFICATION", "one click per muon"))
    o.append(L((14, 352), (586, 352), "pl-rule"))
    o.append(T(14, 374, "A cosmic muon (≈ 1 cm⁻² min⁻¹ at sea level) deposits energy in the plastic; the scintillation light is converted,", "pl-ts", "start"))
    o.append(T(14, 389, "multiplied and read out, and an LM555 voltage-to-frequency stage turns each pulse into an audible event.", "pl-ts", "start"))
    stage = svg_wrap(W_, H_, "".join(o), "Signal chain of the cosmic-muon detector: scintillator, light guide and photomultiplier, "
                     "oscilloscope readout and an LM555 voltage-to-frequency converter driving a speaker")
    return plate(10, "muon", "Scintillation Signal Chain", "plastic scintillator · PMT at 800 V · LM555", stage,
                 [("track", "muon track"), ("photon", "scintillation light"), ("signal", "electrical signal"), ("curve", "measured pulse")],
                 "Experimental project, İstanbul University (2020–2022); report <i>Doğanın Senfonisi</i> (in Turkish).",
                 "Fig. 10: signal chain of the cosmic-muon scintillation detector.")


# ================================================================ card thumbnails: ink drawings of each plate on the paper cards
def _hexpts(cx, cy, r):
    return [(cx + r * math.cos(math.radians(90 + 60 * k)), cy + r * math.sin(math.radians(90 + 60 * k))) for k in range(6)]
def thumb(key):
    o = []
    if key == "msc":
        a, b = _hexpts(42, 32, 18), _hexpts(73.2, 32, 18)
        o.append(PL(a, "cf-ink", closed=True) + PL(b, "cf-ink", closed=True))
        corridor = [(10.8, 50), (26.4, 41), (42, 50), (57.6, 41), (57.6, 23), (73.2, 14), (88.8, 23), (104.4, 14)]
        o.append(L((10.8, 50), (26.4, 41), "cf-ink") + L((88.8, 23), (104.4, 14), "cf-ink"))
        o.append(PL(corridor, "cf-key"))
        o.append(C((10.8, 50), 3.2, "cf-src") + C((104.4, 14), 3.2, "cf-src"))
    elif key == "heat":
        V = lambda x: 0.5 * x * x + 10 * math.exp(-x * x / (2 * 0.49))
        X = lambda x: 12 + 96 * (x + 5) / 10
        Y = lambda e: 60 - 4.1 * e
        o.append(PL([(X(-5 + i / 10), Y(V(-5 + i / 10))) for i in range(101)], "cf-key"))
        for E in (3.1, 5.24, 7.17):
            for x0 in (-1, 1):
                xs = [x for x in [x0 * (0.05 + i / 50) for i in range(250)] if V(x) < E]
                if xs:
                    o.append(L((X(min(xs)) + 1, Y(E)), (X(max(xs)) - 1, Y(E)), "cf-lev"))
        o.append(f'<rect class="cf-gold" x="{n1(X(0.55))}" y="{n1(Y(7.17) - 3)}" width="{n1(X(3.4) - X(0.55))}" height="6" rx="3"/>')
    elif key == "bsc":
        top = [(18 + 22 * k, 20) for k in range(5)]; bot = [(29 + 22 * k, 46) for k in range(5)]
        zig = [p for k in range(5) for p in (top[k], bot[k])]
        o.append(PL(top, "cf-ink cf-dash") + PL(bot, "cf-ink cf-dash"))
        for i, (p, q) in enumerate(zip(zig, zig[1:])):
            o.append(L(p, q, "cf-key" if i % 2 == 0 else "cf-ink"))
        tri = [top[1], bot[1], top[2]]; cx = sum(p[0] for p in tri) / 3; cy = sum(p[1] for p in tri) / 3
        o.append(PL([(cx + (p[0] - cx) * 1.45, cy + (p[1] - cy) * 1.45) for p in tri], "cf-gold", closed=True))
        for p in top + bot:
            o.append(C(p, 2.6, "cf-dot"))
    elif key == "muon":
        o.append(f'<rect class="cf-ink" x="10" y="26" width="46" height="20" rx="1.5"/>')
        o.append(L((22, 4), (40, 62), "cf-trk"))
        o.append(f'<rect class="cf-ink" x="62" y="29" width="22" height="14" rx="3"/>')
        o.append(L((56, 36), (62, 36), "cf-ink"))
        o.append(PL([(88, 30), (95, 30), (98, 31), (101, 52), (104, 38), (108, 32), (116, 30)], "cf-key"))
    elif key == "theory":
        h = _hexpts(60, 32, 24)
        o.append(PL(h, "cf-ink", closed=True))
        for k, p in enumerate(h):
            o.append(L((60, 32), p, "cf-key" if k in (4, 5) else ("cf-gold-l" if k in (1, 2) else "cf-ink")))
            o.append(C(p, 2.5, "cf-dot"))
        o.append(f'<rect class="cf-core" x="51" y="26" width="18" height="12" rx="1"/>')
    elif key == "computation":
        xs = [26 + 17 * i for i in range(5)]
        o.append(L((xs[0] - 10, 30), (xs[-1] + 10, 30), "cf-ink"))
        for x in xs:
            o.append(L((x, 30), (x, 42), "cf-ink") + f'<rect class="cf-core" x="{x - 5}" y="25" width="10" height="10" rx="2"/>')
        o.append(f'<path class="cf-key" d="M20 12 H96" /><path class="cf-tipk" d="M92 9 L97 12 L92 15 Z"/>')
        o.append(f'<path class="cf-gold-l" d="M100 16 C108 40 80 56 58 50"/>')
    elif key == "ai":
        o.append('<ellipse class="cf-key-l" cx="60" cy="32" rx="40" ry="22"/>')
        for k in range(5):
            a = math.radians(-90 + 72 * k)
            o.append(C((60 + 40 * math.cos(a), 32 + 22 * math.sin(a)), 3, "cf-dot"))
        o.append(f'<rect class="cf-core" x="51" y="27" width="18" height="10" rx="1"/>')
    elif key == "industry":
        o.append('<ellipse class="cf-key-l" cx="60" cy="32" rx="28" ry="15"/><ellipse class="cf-gold" cx="60" cy="32" rx="48" ry="27"/>')
        for x, y in ((37, 41), (98, 18), (22, 44), (96, 45)):
            o.append(C((x, y), 2.8, "cf-dot"))
        o.append(f'<rect class="cf-core" x="51" y="27" width="18" height="10" rx="1"/>')
    return f'<svg viewBox="0 0 120 64" aria-hidden="true" focusable="false">{"".join(o)}</svg>'

CARD_FIG = {"theory": 3, "computation": 4, "ai": 5, "industry": 6, "msc": 7, "heat": 8, "bsc": 9, "muon": 10}
def card_fig(key):
    return (f'<span class="card-fig" aria-hidden="true">{thumb(key)}'
            f'<span class="card-fig-n">Fig.&#8201;{CARD_FIG[key]}</span></span>')

def splice_cards(site_dir):
    """put the thumbnail of each plate on its card (idempotent)"""
    import re
    p = os.path.join(site_dir, "index.html")
    h = open(p, encoding="utf-8").read()
    h = re.sub(r'<span class="card-fig" aria-hidden="true">.*?</span></span>', "", h, flags=re.S)
    for key in ("theory", "computation", "ai", "industry"):
        h, n = re.subn(r'(<button class="profile-card[^"]*" type="button" data-profile="%s".*?<span class="profile-card-link">.*?</span></span>)' % key,
                       lambda m: m.group(1) + card_fig(key), h, count=1, flags=re.S)
        assert n == 1, key
    for key in ("msc", "heat", "bsc", "muon"):
        h, n = re.subn(r'(data-project="%s".*?<span class="project-open">.*?</span></span>)' % key,
                       lambda m: m.group(1) + card_fig(key), h, count=1, flags=re.S)
        assert n == 1, key
    open(p, "w", encoding="utf-8").write(h)
