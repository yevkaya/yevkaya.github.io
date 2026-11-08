"""Profile-area dialog templates (Fig. 3-6): figure plates with HTML nodes over an SVG layer, spliced into index.html.

Edges are drawn centre-to-centre *behind* opaque node boxes, so they always meet the box border
exactly at any rendered size; direction is shown by a chevron at the visible midpoint."""
import math, html, os, re
import plates

VW, VH = 600, 500

def P(x, y):
    return x / 100 * VW, y / 100 * VH

def chevron(x, y, ang, size=8, cls="sch-tip"):
    """Filled arrow tip pointing along ang (degrees), tip at (x, y)."""
    a = math.radians(ang)
    pts = [(x, y)]
    for sgn in (-1, 1):
        b = a + math.pi + sgn * math.radians(24)
        pts.append((x + size * math.cos(b), y + size * math.sin(b)))
    return (f'<path class="{cls}" d="M{pts[1][0]:.1f} {pts[1][1]:.1f} L{x:.1f} {y:.1f} '
            f'L{pts[2][0]:.1f} {pts[2][1]:.1f} Z"/>')

def quad(p0, c, p1, t):
    return ((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t * t * p1[0],
            (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t * t * p1[1])

def edge(a, b, kind="dash", bow=0.0, t_arrow=0.5):
    (x1, y1), (x2, y2) = a, b
    cls = {"dash": "sch-edge", "flow": "sch-edge sch-edge-flow", "soft": "sch-edge sch-edge-soft", "est": "sch-edge sch-edge-est",
           "dev": "sch-edge sch-edge-dev", "base": "sch-edge sch-edge-base", "devarrow": "sch-edge sch-edge-dev"}[kind if kind != "arrow" else "flow"]
    tip = "sch-tip-gold" if kind == "devarrow" else "sch-tip"
    if kind == "devarrow": kind = "arrow"
    out = []
    if bow:
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        c = ((x1 + x2) / 2 - dy * bow, (y1 + y2) / 2 + dx * bow)
        out.append(f'<path class="{cls}" d="M{x1:.1f} {y1:.1f} Q{c[0]:.1f} {c[1]:.1f} {x2:.1f} {y2:.1f}"/>')
        if kind == "arrow":
            m = quad(a, c, b, t_arrow); m2 = quad(a, c, b, t_arrow + 0.01)
            out.append(chevron(*m, math.degrees(math.atan2(m2[1] - m[1], m2[0] - m[0])), cls=tip))
    else:
        out.append(f'<path class="{cls}" d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}"/>')
        if kind == "arrow":
            mx, my = x1 + (x2 - x1) * t_arrow, y1 + (y2 - y1) * t_arrow
            out.append(chevron(mx, my, math.degrees(math.atan2(y2 - y1, x2 - x1)), cls=tip))
    return "".join(out)

def node(n):
    cls = "map-core" if n.get("core") else f'map-node map-{n.get("cat", "est")}'
    detail = f'<small>{n["detail"]}</small>' if n.get("detail") else ""
    return (f'<div class="{cls}" style="--x:{n["x"]}%;--y:{n["y"]}%">'
            f'<span>{html.escape(n["label"])}</span><strong>{n["title"]}</strong>{detail}</div>')

def hexagon_pts(cx, cy, r, rot=90):
    return [(cx + r * math.cos(math.radians(rot + 60 * i)), cy + r * math.sin(math.radians(rot + 60 * i))) for i in range(6)]

def poly(pts, cls):
    return f'<polygon class="{cls}" points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}"/>'

def ellipse_positions(n, rx, ry, start=-90):
    return [(round(50 + rx * math.cos(math.radians(start + 360 / n * i)), 1),
             round(50 + ry * math.sin(math.radians(start + 360 / n * i)), 1)) for i in range(n)]

# ---------- motifs ----------
def motif_theory():
    r = 34
    w, h = r * math.sqrt(3), r * 1.5
    cx0, cy0 = VW / 2, VH / 2
    out = []
    for row in range(-5, 6):
        for col in range(-7, 8):
            cx = cx0 + col * w + (w / 2 if row % 2 else 0)
            cy = cy0 + row * h
            if -r < cx < VW + r and -r < cy < VH + r:
                out.append(poly(hexagon_pts(cx, cy, r - 1.5, 90), "sch-hex"))
    return "".join(out)

def motif_computation():
    # MPS chain under the solver: tensors A[1..6] with physical legs, bond index chi
    y = VH * 0.52
    xs = [VW * (0.335 + 0.066 * i) for i in range(6)]
    out = [f'<path class="sch-chain" d="M{xs[0] - 16:.1f} {y:.1f} L{xs[-1] + 16:.1f} {y:.1f}"/>']
    for x in xs:
        out.append(f'<path class="sch-chain" d="M{x:.1f} {y:.1f} L{x:.1f} {y + 18:.1f}"/>')
        out.append(f'<rect class="sch-tensor" x="{x - 8:.1f}" y="{y - 8:.1f}" width="16" height="16" rx="3"/>')
    out.append(f'<text class="sch-label" x="{xs[0] - 16:.1f}" y="{y - 16:.1f}" text-anchor="start">|ψ⟩ ≈</text>')
    out.append(f'<text class="sch-label-small" x="{(xs[3] + xs[4]) / 2:.1f}" y="{y - 12:.1f}" text-anchor="middle">χ</text>')
    out.append(f'<text class="sch-label-small" x="{(xs[0] + xs[-1]) / 2:.1f}" y="{y + 36:.1f}" text-anchor="middle">matrix-product state · bond dimension χ</text>')
    return "".join(out)

def motif_ai(rx=37, ry=41, n=5):
    cx, cy = VW / 2, VH / 2
    RXp, RYp = rx / 100 * VW, ry / 100 * VH
    out = [f'<ellipse class="sch-ring-est" cx="{cx}" cy="{cy}" rx="{RXp:.1f}" ry="{RYp:.1f}"/>']
    for k in range(n):
        ang = -90 + 360 / n * (k + 0.5)
        a = math.radians(ang)
        x, y = cx + RXp * math.cos(a), cy + RYp * math.sin(a)
        tx, ty = -RXp * math.sin(a), RYp * math.cos(a)
        out.append(chevron(x, y, math.degrees(math.atan2(ty, tx)), 8))
    return "".join(out)

def motif_industry():
    cx, cy = VW / 2, VH / 2
    out = []
    for rxx, ryy, lab, k in ((180, 135, "ESTABLISHED", "est"), (254, 198, "DEVELOPING", "dev")):
        out.append(f'<ellipse class="sch-ring-{k}" cx="{cx}" cy="{cy}" rx="{rxx:.0f}" ry="{ryy:.0f}"/>')
        out.append(f'<text class="sch-ring-label-{k}" x="{cx:.1f}" y="{cy - ryy - 7:.1f}" text-anchor="middle">{lab}</text>')
    return "".join(out)

# ---------- nodes (cat: est = established, dev = developing, base = foundation / human / tools) ----------
hexpos = ellipse_positions(6, 37, 41)
theory_nodes = [
    dict(id="core", x=50, y=50, core=True, label="Core", title="Non-Abelian lattice gauge dynamics", detail="SU(2) quantum-link models"),
    dict(id="qft",  x=hexpos[0][0], y=hexpos[0][1], cat="base", label="Foundation", title="Quantum field theory"),
    dict(id="qcd",  x=hexpos[1][0], y=hexpos[1][1], cat="dev", label="Developing", title="Lattice QCD"),
    dict(id="ads",  x=hexpos[2][0], y=hexpos[2][1], cat="dev", label="Developing", title="Gauge–gravity duality"),
    dict(id="qi",   x=hexpos[3][0], y=hexpos[3][1], cat="base", label="Perspective", title="Quantum information"),
    dict(id="spin", x=hexpos[4][0], y=hexpos[4][1], cat="est", label="Established", title="Frustrated &amp; non-Hermitian spins"),
    dict(id="gauss",x=hexpos[5][0], y=hexpos[5][1], cat="est", label="Established", title="Gauss law &amp; rishons"),
]
ring = ["qft", "qcd", "ads", "qi", "spin", "gauss"]
CAT = {n["id"]: n.get("cat", "est") for n in theory_nodes}
theory_edges = [(ring[i], ring[(i + 1) % 6], "soft") for i in range(6)] + [("core", k, CAT[k]) for k in ring]

comp_nodes = [
    dict(id="in",   x=16, y=16, cat="base", label="Input", title="Hamiltonian &amp; sectors", detail="Gauss law · symmetry"),
    dict(id="core", x=50, y=16, core=True, label="Core", title="Many-body solvers", detail="ED · DMRG · TDVP · Krylov"),
    dict(id="out",  x=84, y=16, cat="est", label="Output", title="States &amp; dynamics", detail="observables · spectra"),
    dict(id="ver",  x=84, y=84, cat="dev", label="Reliability", title="Independent verification", detail="overlaps · residuals"),
    dict(id="stack",x=16, y=84, cat="base", label="Tools", title="Scientific stack", detail="Python · Julia · ITensors"),
    dict(id="eng",  x=50, y=84, cat="base", label="Infrastructure", title="Research engineering", detail="Linux · SLURM · Git"),
    dict(id="mps_t", x=50, y=50.4, hidden=True, label="", title=""),
    dict(id="mps_b", x=50, y=56.8, hidden=True, label="", title=""),
    dict(id="mps_l", x=30.8, y=52, hidden=True, label="", title=""),
]
comp_edges = [("in", "core", "arrow"), ("core", "out", "arrow"), ("out", "ver", "arrow"),
              ("ver", "core", "devarrow", 0.1, 0.5), ("core", "mps_t", "soft"), ("stack", "mps_l", "base"), ("eng", "mps_b", "base")]

ai_pos = ellipse_positions(5, 37, 41)
ai_nodes = [
    dict(id="core", x=50, y=50, core=True, label="Principle", title="Control stays with the physicist"),
    dict(id="model",  x=ai_pos[0][0], y=ai_pos[0][1], cat="base", label="Human", title="Physical modelling", detail="method choice"),
    dict(id="agent",  x=ai_pos[1][0], y=ai_pos[1][1], cat="dev", label="AI tools", title="Agentic coding", detail="Claude Code · Codex · llama.cpp"),
    dict(id="impl",   x=ai_pos[2][0], y=ai_pos[2][1], cat="est", label="Output", title="Implementation", detail="Python · Julia models"),
    dict(id="verify", x=ai_pos[3][0], y=ai_pos[3][1], cat="est", label="Control", title="Independent verification", detail="identities · references · tests"),
    dict(id="interp", x=ai_pos[4][0], y=ai_pos[4][1], cat="base", label="Human", title="Interpretation", detail="physical meaning · literature"),
]
ai_edges = [("core", n["id"], n["cat"]) for n in ai_nodes if not n.get("core")]

def ring_pos(rx_units, ry_units, ang):
    a = math.radians(ang)
    return (round(50 + rx_units * math.cos(a) / VW * 100, 1), round(50 + ry_units * math.sin(a) / VH * 100, 1))

sim = ring_pos(180, 135, 215)
alg = ring_pos(254, 198, -35)
qec = ring_pos(254, 198, 145)
qml = ring_pos(254, 198, 35)
ind_nodes = [
    dict(id="core", x=50, y=50, core=True, label="Objective", title="Quantum R&amp;D transfer"),
    dict(id="sim",  x=sim[0], y=sim[1], cat="est", label="Established base", title="Quantum simulation"),
    dict(id="alg",  x=alg[0], y=alg[1], cat="dev", label="Developing", title="Quantum algorithms"),
    dict(id="qec",  x=qec[0], y=qec[1], cat="dev", label="Developing", title="Quantum error correction"),
    dict(id="qml",  x=qml[0], y=qml[1], cat="dev", label="Developing", title="Quantum machine learning"),
]
ind_edges = [("core", "sim", "est"), ("core", "alg", "dev"), ("core", "qec", "dev"), ("core", "qml", "dev")]

PLATE = {
    "theory": (3, "Research Map", "theoretical profile · core model and six directions",
               [("est", "established"), ("dev", "developing"), ("base", "foundation · perspective")],
               "Core: the SU(2) quantum-link models of the M.Sc. thesis (Fig. 1, Fig. 7); honeycomb motif of the C₂ patch."),
    "computation": (4, "Numerical Workflow", "Hilbert-space sectors → solvers → verified observables",
                    [("flow", "data flow"), ("dev", "independent check, fed back"), ("base", "tools and infrastructure")],
                    "Exact diagonalisation in Gauss-law sectors up to 46,829 states; tensor networks as matrix-product states of bond dimension χ."),
    "ai": (5, "Controlled Research Loop", "AI-augmented development, human-led",
           [("flow", "loop direction"), ("base", "human decision"), ("dev", "AI tooling"), ("est", "verified output")],
           "Generated work enters the loop only after checks against identities, constraints and reference calculations."),
    "industry": (6, "Maturity Map", "established base · developing directions",
                 [("ring-est", "established"), ("ring-dev", "developing"), ("dev", "direction towards industrial R&amp;D")],
                 "Inner ring: the established simulation base; outer ring: directions in development."),
}

def S(key, nodes, edges, motif, caption, overlay=""):
    vis = [n for n in nodes if not n.get("hidden")]
    return _schematic(key, nodes, vis, edges, motif, caption, overlay)

def _schematic(key, all_nodes, vis_nodes, edges, motif, caption, overlay):
    byid = {n["id"]: n for n in all_nodes}
    svg_edges = []
    for e in edges:
        a, b = byid[e[0]], byid[e[1]]
        kind = e[2] if len(e) > 2 else "dash"
        bow = e[3] if len(e) > 3 else 0.0
        t = e[4] if len(e) > 4 else 0.5
        svg_edges.append(edge(P(a["x"], a["y"]), P(b["x"], b["y"]), kind, bow, t))
    svg = (f'<svg viewBox="0 0 {VW} {VH}" aria-hidden="true" focusable="false"><defs>'
           f'<radialGradient id="sch-fade-{key}" cx="50%" cy="50%" r="60%"><stop offset="55%" stop-color="#fff"/><stop offset="100%" stop-color="#000"/></radialGradient>'
           f'<mask id="sch-fade-mask-{key}"><rect width="{VW}" height="{VH}" fill="url(#sch-fade-{key})"/></mask></defs>'
           f'<g class="sch-motif" mask="url(#sch-fade-mask-{key})">{motif}</g><g class="sch-edges">{"".join(svg_edges)}</g>{overlay}</svg>')
    body = "".join(node(n) for n in vis_nodes)
    fig, title, context, legend, note = PLATE[key]
    return plates.plate(fig, key, title, context, svg + body, legend, note, caption, kind="map")

areas = {
    "theory": dict(
        kicker="01 / Theory", title="Theoretical Profile", title_id="theoretical-profile-title",
        lead="My theoretical work treats lattice gauge theories as constrained quantum many-body systems: how local gauge "
             "constraints shape spectra, screening and real-time dynamics. Developing interests carry these questions towards "
             "continuum field theory, lattice QCD and gauge–gravity duality.",
        groups=[("Established research", "Gauge theories and many-body systems",
                 ["SU(2) quantum-link models in the rishon representation, with Gauss-law sectors and gauge-invariant bases",
                  "Static source response and non-Abelian real-time dynamics on finite lattices",
                  "Effective Hamiltonians for cold-atom implementations of lattice gauge models",
                  "Frustrated and non-Hermitian spin chains, entanglement and quantum thermodynamics"]),
                ("Developing directions", "Field theory and emergent structure",
                 ["Quantum field theory and lattice QCD",
                  "Gauge–gravity duality and holographic Wilson loops",
                  "Quantum-information perspectives on field theories and many-body systems"])],
        schem=S("theory", theory_nodes, theory_edges, motif_theory(), "Research map: a non-Abelian lattice core with six connected directions, on a honeycomb motif")),
    "computation": dict(
        kicker="02 / Computation", title="Computational Profile", title_id="computational-profile-title",
        lead="I build reproducible numerical workflows for ground states, real-time evolution and observables, from exact "
             "calculations in symmetry-resolved Hilbert spaces to compressed tensor-network representations.",
        groups=[("Methods", "Many-body solvers",
                 ["Sparse exact diagonalisation in Gauss-law sectors, DMRG and TDVP for matrix-product states, and Krylov time propagation."]),
                ("Software", "Scientific stack",
                 ["Python, Julia, NumPy, SciPy and Matplotlib; ITensors, ITensorMPS and KrylovKit."]),
                ("Infrastructure", "Research engineering",
                 ["Linux, Bash, SLURM-managed HPC, Git and LaTeX for reproducible parameter sweeps, diagnostics and documentation."]),
                ("Reliability", "Numerical verification",
                 ["Overlaps and residuals, symmetry-sector tests, convergence studies and independent reference calculations as standard checks."])],
        schem=S("computation", comp_nodes, comp_edges, motif_computation(), "Workflow: model and sectors feed the solvers; results are verified independently and fed back")),
    "ai": dict(
        kicker="03 / AI", title="AI-Augmented Research", title_id="ai-augmented-title",
        lead="I use AI systems as tools for research software development, while physical modelling, the choice of numerical "
             "methods, interpretation and validation remain under my direct control.",
        groups=[("Agentic development", "Scientific coding workflows",
                 ["Claude Code and OpenAI Codex assist with implementing, debugging and refactoring Python and Julia many-body codes."]),
                ("Local systems", "Language-model deployment and retrieval",
                 ["Quantised language models deployed locally on Linux CPU hardware with llama.cpp and Jan, together with a prototype for source-grounded retrieval."]),
                ("Research control", "Independent verification",
                 ["Generated code and text are checked against mathematical identities, physical constraints, reference calculations and reproducible tests before use."])],
        schem=S("ai", ai_nodes, ai_edges, motif_ai(), "Research loop: modelling → agentic coding → implementation → verification → interpretation, with control at the centre")),
    "industry": dict(
        kicker="04 / Industry", title="Industrial Interests", title_id="industrial-interests-title",
        lead="I am interested in research and engineering roles that turn rigorous quantum modelling into useful algorithms, "
             "simulation platforms and reliable computational technology.",
        groups=[("Established base", "Quantum simulation",
                 ["Exact and tensor-network simulation of constrained many-body models, with validated and reproducible numerical pipelines."]),
                ("Developing directions", "Algorithms, error correction and machine learning",
                 ["Application-oriented work in quantum algorithms, quantum error correction and quantum machine learning, built on the same numerical foundations."]),
                ("Objective", "Quantum R&D transfer",
                 ["Work that connects scientific software to measurable industrial value."])],
        schem=S("industry", ind_nodes, ind_edges, motif_industry(), "Maturity map: the established simulation base on the inner ring, developing directions on the outer ring")),
}

def template(key, a):
    groups = []
    for label, h3, items in a["groups"]:
        lis = "".join(f"<li>{html.escape(t)}</li>" for t in items)
        groups.append(f'<div class="area-group"><span class="area-group-label">{html.escape(label)}</span><h3>{html.escape(h3)}</h3><ul>{lis}</ul></div>')
    sec_id = {"theory": "theoretical-profile", "computation": "computational-profile", "ai": "ai-augmented-research", "industry": "industrial-interests"}[key]
    return f'''      <template id="profile-{key}">
      <section class="area section section-dark" id="{sec_id}" aria-labelledby="{a["title_id"]}">
        <div class="shell area-grid">
          <div class="area-copy">
            <p class="kicker">{a["kicker"]}</p>
            <h2 id="{a["title_id"]}">{a["title"]}</h2>
            <p class="detail-lead">{a["lead"]}</p>
            <div class="area-groups">{"".join(groups)}</div>
          </div>
          {a["schem"]}
        </div>
      </section>
      </template>
'''

def splice(site_dir):
    p = os.path.join(site_dir, "index.html")
    h = open(p, encoding="utf-8").read()
    for k, a in areas.items():
        h, n = re.subn(r'[ \t]*<template id="profile-%s">.*?</template>\n?' % k, lambda m: template(k, a), h, count=1, flags=re.S)
        assert n == 1, k
    open(p, "w", encoding="utf-8").write(h)

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    site = os.path.join(here, "..") if os.path.exists(os.path.join(here, "..", "index.html")) else os.path.join(here, "..", "Portfolio")
    splice(site)
    print("profile templates spliced:", ", ".join(areas))
