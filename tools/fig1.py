"""Fig. 1 (hero), v7: colour-singlet clusters, flux-tube formation and string breaking on the C2 patch.

Notation of Halimeh et al., PRX Quantum 5, 030358 (2024), Figs. 1, 2 and 7: every vertex is drawn as its triangle
of sites -- the matter site in the centre, one rishon site per link end at the corners; an SU(2) colour singlet is a
lobe that joins two singly occupied sites of the same vertex (Gauss's law: each vertex is a total singlet); a doubly
occupied site is an on-site singlet (halo).  Thesis model: two-colour fermionic matter, six-state two-rishon links
|n_L, n_R> with n_L + n_R = 2 (L at the A end), staggered reference (A empty, B doubly occupied, all links |0,2>);
hopping tunnels a matter-rishon singlet pair between neighbouring vertices; D_v = n_v - sum_l n_(l,v) is conserved.

Clusters
  matter cluster    a q q-bar meson: one active link |1,1> with a matter-rishon singlet at each end
  glueball cluster  the Tr U_p ring resonance.  Tr U_p moves one rishon on every link of a hexagon, alternately
                    R -> L and L -> R, so it annihilates the bare vacuum (all |0,2>); its lowest targets are the two
                    Kekule coverings of a hexagon by three singlet pairs, which it swaps (exhaustive enumeration of
                    the 16 502 gauge-invariant vacuum-sector configurations).  Six singlets swing round the plaquette.
  flux tube         an open chain of rishon-rishon singlets from Q to Q-bar, ending on source-rishon singlets
Storyboard (each discrete frame is checked below: n_L + n_R = 2, D_v, exactly one singlet per singly occupied site)
  vacuum    ring A resonates (glueball cluster) next to the matter clusters on l4 and l12
  insert    Q (vertex 1) and Q-bar (vertex 12) placed by hand: registered corridor sector (l1, l2, l8, l11 reversed,
            both sources screened by one fermion); the sector pins ring A to one covering -> matter clusters
  ramp      m(t) = 0.5 + 3.5 t/4: l6 and l4 annihilate; l12, l10, l3 link up through q q-bar annihilation -> tube
  quench    m: 4 -> 0.5: a q q-bar pair from the vacuum cuts the tube on the central link l10, each half is cut again
            on l3 and l12 -> four short colour-singlet strings (Q q-bar, q q-bar, q q-bar, q Q-bar); l6, l4 re-form
  withdraw  sources removed: the only local move back to the vacuum labels shifts one rishon on every corridor link
            (the light charges re-pair onto l3, l10, l12); ring B resonates and hands the resonance back to ring A
            through the shared covering
Outlines: every colour-singlet object carries one dashed contour (Gaussian convolution field along its skeleton); clusters
  merge into the tube at the joins and the tube pinches into four short strings at the quench (counts checked below).
Runtime: keyframe tracks sampled with sine easing, allocation-free, written only on change; no SVG filters; four svg layers.
Data layer (exact, thesis Ch. IV / Response Report Fig. 2 and Table 4): source classes P_conn, P_1ff, P_2ff, P_0ff and
tau_E^resp of the thesis protocols (kappa = 0, R = 4), drawn as stacked bands; they set the readout and the tube glow.
Inset: static P_conn(m) at R = 4 for kappa = 0, 2, 4 (Table 5, Fig. 3)."""
import json, math, re, os

HERE = os.path.dirname(os.path.abspath(__file__))
SITE_DIR = os.path.join(HERE, "..") if os.path.exists(os.path.join(HERE, "..", "index.html")) else os.path.join(HERE, "..", "Portfolio")
RT = json.load(open(os.path.join(HERE, "rt_data.json")))

W, H = 620, 322
RAW = {1: (186, 791), 7: (276.5, 738.75), 2: (367, 791), 8: (457.5, 738.75), 3: (548, 791), 9: (638.5, 738.75),
       4: (276.5, 634.25), 5: (457.5, 634.25), 6: (638.5, 634.25), 10: (367, 582), 11: (548, 582), 12: (729, 582)}
S, X0, Y0 = 0.86, 100.0, 26.0
V = {k: (X0 + (x - 186) * S, Y0 + (y - 582) * S) for k, (x, y) in RAW.items()}
A_SITES = {1, 2, 3, 4, 5, 6}
LINKS = {1: (1, 7), 3: (2, 7), 2: (2, 8), 5: (3, 8), 4: (3, 9), 7: (4, 7), 10: (5, 8), 13: (6, 9),
         6: (4, 10), 9: (5, 10), 8: (5, 11), 12: (6, 11), 11: (6, 12)}          # (A end = L, B end = R)
PATH = [1, 3, 2, 10, 8, 12, 11]                                                 # corridor 1-7-2-8-5-11-6-12
HEXV = {"A": [7, 2, 8, 5, 10, 4], "B": [8, 3, 9, 6, 11, 5]}
DC, RS = 18.0, 3.3                       # centre-to-corner distance of a vertex triangle, site radius
C30 = math.sqrt(3) / 2
TRI = {"A": [(-C30, -0.5), (C30, -0.5), (0.0, 1.0)], "B": [(0.0, -1.0), (-C30, 0.5), (C30, 0.5)]}
ST = {"v": (0, 2), "a": (1, 1), "r": (2, 0)}

def f(x): return f"{x:.2f}".rstrip("0").rstrip(".")
def lerp(p, q, t): return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)
def dist(p, q): return math.hypot(q[0] - p[0], q[1] - p[1])
def unit(p, q):
    dx, dy = q[0] - p[0], q[1] - p[1]; L = math.hypot(dx, dy); return dx / L, dy / L
def perp(p, q):
    ux, uy = unit(p, q); return -uy, ux
def corner(v, lid):
    a, b = LINKS[lid]; w = b if v == a else a
    ux, uy = unit(V[v], V[w]); return (V[v][0] + ux * DC, V[v][1] + uy * DC)
def tri_pts(v):
    x, y = V[v]; return [(x + dx * DC, y + dy * DC) for dx, dy in TRI["A" if v in A_SITES else "B"]]

P, SV = {}, {}                           # site positions and the vertex each site belongs to
for v in V:
    P[f"m{v}"], SV[f"m{v}"] = V[v], v
for lid, (a, b) in LINKS.items():
    P[f"r{lid}L"], SV[f"r{lid}L"] = corner(a, lid), a
    P[f"r{lid}R"], SV[f"r{lid}R"] = corner(b, lid), b
P["Q"], SV["Q"] = (V[1][0] - C30 * DC, V[1][1] - 0.5 * DC), 1        # free up-left corner of vertex 1
P["Qb"], SV["Qb"] = (V[12][0] + C30 * DC, V[12][1] + 0.5 * DC), 12   # free down-right corner of vertex 12
HEXC = {h: (sum(V[k][0] for k in hv) / 6, sum(V[k][1] for k in hv) / 6) for h, hv in HEXV.items()}
PC = (sum(HEXC[h][0] for h in HEXC) / 2, sum(HEXC[h][1] for h in HEXC) / 2)

# ---------------- time axis ----------------
CYCLE = 36.0
RES_A = (0.0, 0.047, 0.094)              # ring A resonance: K1 -> K2 -> K1
INS = (0.100, 0.118)                     # sources placed by hand
PIN = (0.104, 0.128)                     # ... which pins ring A to K1
U_R0, U_R1 = 0.134, 0.492                # formation ramp, t in [0, 4]
U_Q0, U_Q1 = 0.516, 0.858                # breaking quench, t in [0, 2]; the m = 4 ground state is held in between
WD = (0.864, 0.892)                      # sources removed by hand
UNPIN_B = (0.896, 0.909)                 # ring B starts to resonate
RES_B = (0.909, 0.9365, 0.964)
HAND = (0.967, 0.997)                    # the resonance moves back to ring A
def uR(t): return U_R0 + (U_R1 - U_R0) * t / 4
def uQ(t): return U_Q0 + (U_Q1 - U_Q0) * t / 2
U_STATIC = uQ(1.30)
AX0, AX1 = 34.0, 600.0
AW = AX1 - AX0
def X(u): return AX0 + u * AW
MU_Y0, MU_K = 251.0, 3.5
def Ymu(mu): return MU_Y0 - MU_K * mu
PT, PB = 255.0, 293.0
def Yp(p): return PB - (PB - PT) * p
AY = 295.0
MU_STAR = 9 / 8

def mu_of(u):
    if u < U_R0: return 0.5
    if u <= U_R1: return 0.5 + 3.5 * ((u - U_R0) / (U_R1 - U_R0))
    return 4.0 if u < U_Q0 else 0.5

EV = dict(O6=(uR(0.45), uR(0.85)), O4=(uR(0.95), uR(1.35)),
          J11=(uR(1.60), uR(1.95)), J8=(uR(1.95), uR(2.25)), J2=(uR(2.25), uR(2.50)), J1=(uR(2.45), uR(2.70)),
          B10=(uQ(0.08), uQ(0.66)), B3=(uQ(0.78), uQ(1.24)), B12=(uQ(0.78), uQ(1.24)),
          C6=(uQ(1.38), uQ(1.70)), C4=(uQ(1.52), uQ(1.84)))
def mid(w): return (w[0] + w[1]) / 2

# ---------------- tracks ----------------
def ease(x): return 0.5 - 0.5 * math.cos(math.pi * x)
class Track:
    def __init__(self, tid, typ, v0, smooth=True):
        self.id, self.typ, self.smooth = tid, typ, smooth
        self.keys = [(0.0, tuple(v0))]; self.cur = tuple(v0)
    def to(self, u0, u1, v):
        v = tuple(v)
        if u0 > self.keys[-1][0] + 1e-9:
            self.keys.append((u0, self.cur))
        self.keys.append((u1, v)); self.cur = v
        return self
    def key(self, u, v):
        self.keys.append((u, tuple(v))); self.cur = tuple(v); return self
    def close(self):
        if self.keys[-1][0] < 1:
            self.keys.append((1.0, self.cur))
        assert all(abs(a - b) < 1e-6 for a, b in zip(self.keys[0][1], self.keys[-1][1])), self.id
        us = [k[0] for k in self.keys]
        assert us == sorted(us), (self.id, us)
        return self
    def sample(self, u):
        k = self.keys
        if u <= k[0][0]: return k[0][1]
        for a, b in zip(k, k[1:]):
            if u <= b[0]:
                span = b[0] - a[0]; s = (u - a[0]) / span if span > 0 else 1
                s = ease(s) if self.smooth else s
                return tuple(x + (y - x) * s for x, y in zip(a[1], b[1]))
        return k[-1][1]
    def data(self):
        d = {"id": self.id, "t": self.typ, "k": [[round(u, 5)] + [round(x, 4) for x in v] for u, v in self.keys]}
        if not self.smooth: d["e"] = 0
        if hasattr(self, "seg"): d["s"] = self.seg
        return d
tracks = []
def T(tid, typ, v0, smooth=True):
    t = Track(tid, typ, v0, smooth); tracks.append(t); return t

# --- site occupations: vacuum V0 = ring A in covering K1 (l3, l10, l6) + matter clusters on l4, l12
OCC0 = {}
for v in V:
    OCC0[f"m{v}"] = 0 if v in A_SITES else 2
for lid in LINKS:
    OCC0[f"r{lid}L"], OCC0[f"r{lid}R"] = 0, 2
for lid in (3, 10, 6, 4, 12):
    a, b = LINKS[lid]; OCC0[f"m{a}"] += 1; OCC0[f"m{b}"] -= 1; OCC0[f"r{lid}L"], OCC0[f"r{lid}R"] = 1, 1
OCC = {s: T(f"f1-s-{s}", "occ", (o,)) for s, o in OCC0.items()}
def occ(s, w, val): OCC[s].to(w[0], w[1], (val,))
def link(lid, w, st): occ(f"r{lid}L", w, ST[st][0]); occ(f"r{lid}R", w, ST[st][1])

# --- singlet lobes: (ends, colour layers t = open string / meson, g = glueball, i = screened source)
LOBE = {}
def lobe(name, p, q, layers, init):
    d = {"ln": T(f"f1-lb-{name}", "ln", P[p] + P[q]), "layers": layers}
    for c in layers:
        d[c] = T(f"f1-lb-{name}-{c}", "op", (init.get(c, 0.0),))
    LOBE[name] = d
def lb_to(name, w, p, q): LOBE[name]["ln"].to(w[0], w[1], P[p] + P[q])
def lb_op(name, c, w, val): LOBE[name][c].to(w[0], w[1], (val,))
K1A, K2A = [3, 10, 6], [2, 9, 7]
K1B, K2B = [10, 4, 12], [5, 13, 8]
K1A_L = {"2a": ("m2", "r3L"), "7a": ("m7", "r3R"), "5a": ("m5", "r10L"), "8a": ("m8", "r10R"), "4a": ("m4", "r6L"), "10a": ("m10", "r6R")}
K2A_L = {"2b": ("m2", "r2L"), "8b": ("m8", "r2R"), "5b": ("m5", "r9L"), "10b": ("m10", "r9R"), "4b": ("m4", "r7L"), "7b": ("m7", "r7R")}
MC_L = {"3a": ("m3", "r4L"), "9a": ("m9", "r4R"), "6a": ("m6", "r12L"), "11a": ("m11", "r12R")}
K2B_L = {"3b": ("m3", "r5L"), "8c": ("m8", "r5R"), "6b": ("m6", "r13L"), "9b": ("m9", "r13R"), "5c": ("m5", "r8L"), "11b": ("m11", "r8R")}
K1B_N = ["8a", "5a", "3a", "9a", "6a", "11a"]
for n, (p, q) in K1A_L.items(): lobe(n, p, q, "tg", {"g": 1})
for n, (p, q) in K2A_L.items(): lobe(n, p, q, "g", {})
for n, (p, q) in MC_L.items(): lobe(n, p, q, "tg", {"t": 1})
for n, (p, q) in K2B_L.items(): lobe(n, p, q, "g", {})
lobe("L1", "Q", "m1", "it", {}); lobe("L12", "Qb", "m12", "it", {})

# --- active links (|1,1>) and their glow
T_LINKS = [1, 3, 2, 10, 8, 12, 11, 6, 4]
G_LINKS = [3, 2, 10, 9, 6, 7, 4, 12, 5, 13, 8]
AK = {}
for lid in T_LINKS: AK[(lid, "t")] = T(f"f1-ak{lid}t", "op", (1.0 if lid in (4, 12) else 0.0,))
for lid in G_LINKS: AK[(lid, "g")] = T(f"f1-ak{lid}g", "op", (1.0 if lid in K1A else 0.0,))
def ak(lid, c, w, val): AK[(lid, c)].to(w[0], w[1], (val,))
KG = {lid: T(f"f1-kg{lid}", "op", (1.0 if lid in (4, 12) else 0.0,)) for lid in T_LINKS}
RG = {"A": T("f1-rgA", "op", (1,)), "B": T("f1-rgB", "op", (0,))}
HL = {"A": T("f1-hlA", "op", (1,)), "B": T("f1-hlB", "op", (0,))}

# --- every hop is drawn as what it is in the staggered picture: a q q-bar pair created on a link (B -> A tunnelling)
#     or annihilated on it (A -> B).  q = particle on an A site (filled glyph), q-bar = hole on a B site (open glyph).
GLYPHS, HALOS, BURSTS = [], [], {}
def frac(w, a): return w[0] + (w[1] - w[0]) * a
def sub_w(w, a, b): return (frac(w, a), frac(w, b))
def lmid(lid): return lerp(P[f"r{lid}L"], P[f"r{lid}R"], 0.5)
def glyph(gid, kind, pa, pb, wt, wo):
    """glyph moving pa -> pb over wt (eased, constant-speed samples), visible over wo = (in0, in1, out0, out1)"""
    tr = T(gid, "tr", pa, smooth=False).key(wt[0], pa)
    for k in range(1, 15):
        s = ease(k / 14); tr.key(wt[0] + (wt[1] - wt[0]) * k / 14, lerp(pa, pb, s))
    tr.key(max(wt[1], wo[3]) + 0.0015, pa)
    T(gid, "op", (0,)).key(wo[0], (0,)).key(wo[1], (1,)).key(wo[2], (1,)).key(wo[3], (0,))
    GLYPHS.append((gid, kind))
def halo(name, lid, w, r0, r1):
    """converging ring on the link: a vacuum fluctuation about to materialise"""
    T(f"f1-gh-{name}", "burst", (r0, 0)).key(w[0], (r0, 0)).key(frac(w, 0.20), (r1, 0.85)).key(frac(w, 0.27), (r1 * 0.8, 0)) \
        .key(frac(w, 0.27) + 0.001, (r0, 0))
    HALOS.append((name, lid))
def burst(name, lid, u, kind):
    tr = BURSTS.setdefault(name, (lid, T(f"f1-bu-{name}", "burst", (3, 0))))[1]
    if kind == "create":
        tr.key(u - 0.002, (3, 0)).key(u + 0.008, (13, 0.85)).key(u + 0.03, (21, 0)).key(u + 0.031, (3, 0))
    else:
        tr.key(u - 0.003, (3, 0)).key(u + 0.007, (11, 0.7)).key(u + 0.028, (18, 0)).key(u + 0.029, (3, 0))
def pair_create(ev, lid, r0, r1):
    w = EV[ev]; a, b = LINKS[lid]; m = lmid(lid)
    halo(ev, lid, w, r0, r1); burst(ev, lid, frac(w, 0.24), "create")
    glyph(f"f1-gq-{ev}", "q", m, P[f"m{a}"], sub_w(w, 0.24, 0.80), (frac(w, 0.21), frac(w, 0.29), frac(w, 0.74), frac(w, 0.86)))
    glyph(f"f1-gqb-{ev}", "qb", m, P[f"m{b}"], sub_w(w, 0.24, 0.80), (frac(w, 0.21), frac(w, 0.29), frac(w, 0.74), frac(w, 0.86)))
def pair_annihilate(ev, lid):
    w = EV[ev]; a, b = LINKS[lid]; m = lmid(lid)
    glyph(f"f1-gq-{ev}", "q", P[f"m{a}"], m, sub_w(w, 0.06, 0.60), (w[0], frac(w, 0.10), frac(w, 0.55), frac(w, 0.64)))
    glyph(f"f1-gqb-{ev}", "qb", P[f"m{b}"], m, sub_w(w, 0.06, 0.60), (w[0], frac(w, 0.10), frac(w, 0.55), frac(w, 0.64)))
    burst(ev, lid, frac(w, 0.60), "annihilate")

# --- colour-singlet outlines.  Every colour-singlet object (matter cluster, screened source, open string) carries one
#     dashed outline: the level set F = LEV of a Gaussian convolution field along its skeleton (matter site to matter
#     site along the links, plus a stub from each source to its vertex).  Convolution surfaces are additive along the
#     skeleton, so adjacent pieces give exactly the field of the joined piece (no seams), and two pieces approaching
#     each other fuse through a smooth neck.  Each link carries two half-segments, vertex -> link midpoint, with a
#     visible interval [p, q] (0 = vertex, 1 = midpoint) and a weight w: clusters grow out of or shrink into a midpoint
#     (pair creation, annihilation), strings fuse across a link (joins: both halves grow to the midpoint) and pinch
#     apart (string breaking: both halves retract to their vertices).  The outlines thus count the singlets on the patch.
SIG, LEV, GRID = 9.0, 1.68, 2.0          # kernel width, contour level (half-width 13.5 on a straight skeleton), grid step
GX0, GY0 = -14.0, -14.0
GNX, GNY = int((W + 28) / GRID) + 2, int((H + 28) / GRID) + 2
SQPI2 = math.sqrt(math.pi) * SIG / 2
BS_LIST, BI, BW = [], {}, {}
def bseg(name, a, m, p, q, w):
    BI[name] = T(f"f1-bi-{name}", "bi", (p, q)); BW[name] = T(f"f1-bw-{name}", "bw", (w,))
    BI[name].seg = BW[name].seg = len(BS_LIST); BS_LIST.append((name, a, m))
OL_LINKS = [1, 3, 2, 10, 8, 12, 11, 6, 4]
for lid in OL_LINKS:
    a, b = LINKS[lid]; mid_ = lerp(V[a], V[b], 0.5)
    for v in (a, b):
        on = 1.0 if lid in (4, 12) else 0.0
        bseg(f"{lid}.{v}", V[v], mid_, 0.0, 0.0 if lid in (1, 2, 8, 11) else 1.0, on)
for key, v in (("Q", 1), ("Qb", 12)):                     # the stub reaches 4 units past the source, so its cap clears the ring
    ux, uy = unit(V[v], P[key])
    bseg(key, (P[key][0] + 4 * ux, P[key][1] + 4 * uy), V[v], 0.0, 1.0, 0.0)
def ol_iv(name, w, p, q): BI[name].to(w[0], w[1], (p, q))
def ol_w(name, w, val): BW[name].to(w[0], w[1], (val,))
def ol_set(name, u, p=None, q=None, wt=None):
    """instantaneous change, only while the half-segment is invisible (zero length or zero weight)"""
    if p is not None or q is not None:
        cp, cq = BI[name].cur
        BI[name].key(u, (cp, cq)).key(u, (cp if p is None else p, cq if q is None else q))
    if wt is not None:
        BW[name].key(u, BW[name].cur).key(u, (wt,))
def halves(lid): return [f"{lid}.{v}" for v in LINKS[lid]]
# glueball-cluster marker: a dashed circle inside the hexagon that converges when the ring resonance forms
GC = {"A": T("f1-gcA", "burst", (60, 1)), "B": T("f1-gcB", "burst", (72, 0))}

# ======== storyboard ========
# vacuum: ring A resonates K1 <-> K2 (Tr U_p swaps the two Kekule coverings)
a0, am, a1 = RES_A
for n in K1A_L: lb_op(n, "g", (a0, am), 0); lb_op(n, "g", (am, a1), 1)
for n in K2A_L: lb_op(n, "g", (a0, am), 1); lb_op(n, "g", (am, a1), 0)
for lid in K1A: ak(lid, "g", (a0, am), 0); ak(lid, "g", (am, a1), 1); link(lid, (a0, am), "v"); link(lid, (am, a1), "a")
for lid in K2A: ak(lid, "g", (a0, am), 1); ak(lid, "g", (am, a1), 0); link(lid, (a0, am), "a"); link(lid, (am, a1), "v")
# sources placed by hand: registered corridor sector, both sources screened by one fermion
occ("m1", INS, 1); occ("m12", INS, 1)
for lid in (1, 2, 8, 11): link(lid, INS, "r")
lb_op("L1", "i", INS, 1); lb_op("L12", "i", INS, 1)
for n in K1A_L: lb_op(n, "g", PIN, 0); lb_op(n, "t", PIN, 1)
for lid in K1A: ak(lid, "g", PIN, 0); ak(lid, "t", PIN, 1); KG[lid].to(*PIN, (1,))
RG["A"].to(*PIN, (0,)); HL["A"].to(*PIN, (0,))
for key in ("Q", "Qb"): ol_w(key, (frac(INS, 0.45), INS[1] + 0.006), 1)
for lid in K1A:
    for nm in halves(lid): ol_w(nm, PIN, 1)
GC["A"].to(*PIN, (68, 0)).key(PIN[1] + 0.002, (72, 0))
for v in (1, 12):
    T(f"f1-src{v}", "op", (0,)).to(*INS, (1,)).to(*sub_w(WD, 0.0, 0.55), (0,))
    T(f"f1-ins{v}", "burst", (36, 0)).key(INS[0], (36, 0)).key(INS[1], (8.5, 0.9)).key(INS[1] + 0.02, (8.5, 0)) \
        .key(WD[0], (8.5, 0)).key(WD[0] + 0.004, (8.5, 0.9)).key(frac(WD, 0.6), (36, 0))
T("f1-iflash", "op", (0,)).key(INS[0], (0,)).key(mid(INS), (1,)).key(INS[1] + 0.012, (0,))
T("f1-wflash", "op", (0,)).key(WD[0], (0,)).key(frac(WD, 0.45), (1,)).key(WD[1] + 0.012, (0,))

# formation ramp: off-corridor matter clusters annihilate (q and q-bar meet on the link) ...
def annihilate(ev, lid, la, lb_):
    w = EV[ev]; a, b = LINKS[lid]
    occ(f"m{a}", sub_w(w, 0.04, 0.40), 0); occ(f"m{b}", sub_w(w, 0.04, 0.40), 2); link(lid, sub_w(w, 0.30, 0.70), "v")
    lb_op(la, "t", sub_w(w, 0.12, 0.50), 0); lb_op(lb_, "t", sub_w(w, 0.12, 0.50), 0)
    ak(lid, "t", sub_w(w, 0.36, 0.72), 0); KG[lid].to(*sub_w(w, 0.30, 0.70), (0,))
    pair_annihilate(ev, lid)
    for nm in halves(lid): ol_iv(nm, sub_w(w, 0.06, 0.60), 1.0, 1.0); ol_w(nm, sub_w(w, 0.44, 0.63), 0)
annihilate("O6", 6, "4a", "10a")
annihilate("O4", 4, "3a", "9a")
# ... and the corridor joins up: the q q-bar pair at each junction annihilates, the singlets re-pair into one chain
def join(ev, lid, sw):
    w = EV[ev]; a, b = LINKS[lid]
    occ(f"m{a}", sub_w(w, 0.04, 0.40), OCC[f"m{a}"].cur[0] - 1); occ(f"m{b}", sub_w(w, 0.04, 0.40), OCC[f"m{b}"].cur[0] + 1)
    link(lid, sub_w(w, 0.45, 0.90), "a")
    for name, ends in sw: lb_to(name, sub_w(w, 0.08, 0.52), *ends)
    ak(lid, "t", sub_w(w, 0.50, 0.94), 1); KG[lid].to(*sub_w(w, 0.50, 0.94), (1,))
    pair_annihilate(ev, lid)
    for nm in halves(lid): ol_set(nm, w[0], wt=1.0); ol_iv(nm, sub_w(w, 0.06, 0.60), 0.0, 1.0)
join("J11", 11, [("6a", ("r11L", "r12L")), ("L12", ("Qb", "r11R"))])
lb_op("L12", "i", sub_w(EV["J11"], 0.08, 0.52), 0); lb_op("L12", "t", sub_w(EV["J11"], 0.08, 0.52), 1)
join("J8", 8, [("5a", ("r8L", "r10L")), ("11a", ("r8R", "r12R"))])
join("J2", 2, [("2a", ("r2L", "r3L")), ("8a", ("r2R", "r10R"))])
join("J1", 1, [("L1", ("Q", "r1L")), ("7a", ("r1R", "r3R"))])
lb_op("L1", "i", sub_w(EV["J1"], 0.08, 0.52), 0); lb_op("L1", "t", sub_w(EV["J1"], 0.08, 0.52), 1)

# breaking quench: a q q-bar pair from the vacuum cuts the tube on the central link l10; each half is cut again on
# l3 and l12.  Result: four short strings, each a colour singlet: Q-q-bar, q q-bar, q q-bar, q Q-bar.
T("f1-qf", "burst", (20, 0)).key(U_Q0 - 0.001, (20, 0)).key(U_Q0 + 0.008, (70, 0.8)).key(U_Q0 + 0.04, (96, 0)).key(U_Q0 + 0.041, (20, 0))
T("f1-lflash", "op", (0,)).key(U_Q0 - 0.001, (0,)).key(U_Q0 + 0.005, (1,)).key(U_Q0 + 0.05, (0,))
def cut(ev, lid, sw, r0, r1, labels):
    w = EV[ev]; a, b = LINKS[lid]
    pair_create(ev, lid, r0, r1)
    ak(lid, "t", sub_w(w, 0.20, 0.42), 0); KG[lid].to(*sub_w(w, 0.20, 0.42), (0,))
    link(lid, sub_w(w, 0.30, 0.66), "r")
    occ(f"m{a}", sub_w(w, 0.55, 0.85), OCC[f"m{a}"].cur[0] + 1); occ(f"m{b}", sub_w(w, 0.55, 0.85), OCC[f"m{b}"].cur[0] - 1)
    for name, ends in sw: lb_to(name, sub_w(w, 0.50, 0.90), *ends)
    for cid in labels: LQ[cid] = T(cid, "op", (0,)).to(*sub_w(w, 0.78, 0.96), (1,)).to(*sub_w(WD, 0.0, 0.45), (0,))
    for nm in halves(lid): ol_iv(nm, sub_w(w, 0.24, 0.80), 0.0, 0.0)
LQ = {}
cut("B10", 10, [("8a", ("r2R", "m8")), ("5a", ("r8L", "m5"))], 30, 5, ["f1-lq5", "f1-lqb8"])
cut("B3", 3, [("7a", ("r1R", "m7")), ("2a", ("r2L", "m2"))], 20, 4.2, ["f1-lq2", "f1-lqb7"])
cut("B12", 12, [("11a", ("r8R", "m11")), ("6a", ("r11L", "m6"))], 20, 4.2, ["f1-lq6", "f1-lqb11"])
T("f1-cb", "op", (0,)).to(*sub_w(EV["B10"], 0.0, 0.15), (1,)).to(uQ(1.36), uQ(1.48), (0,))
T("f1-cb1", "op", (1,)).to(*sub_w(EV["B3"], 0.78, 0.92), (0,)).key(uQ(1.50), (0,)).key(uQ(1.50), (1,))
T("f1-cb2", "op", (0,)).to(EV["B3"][1] - 0.001, EV["B3"][1] + 0.011, (1,)).key(uQ(1.50), (1,)).key(uQ(1.50), (0,))
T("f1-ft", "op", (0,)).to(EV["J1"][1] + 0.003, EV["J1"][1] + 0.017, (1,)).to(U_Q0, U_Q0 + 0.011, (0,))
T("f1-cbl", "op", (0,)).to(EV["J1"][1] + 0.003, EV["J1"][1] + 0.017, (1,)).to(uQ(1.36), uQ(1.48), (0,))
T("f1-ol", "op", (0.9,)).to(EV["J1"][1] - 0.006, EV["J1"][1] + 0.004, (1,)).to(EV["J1"][1] + 0.004, EV["J1"][1] + 0.03, (0.9,))
# off-corridor matter clusters re-form from the vacuum
def create(ev, lid, la, lb_):
    w = EV[ev]; a, b = LINKS[lid]
    pair_create(ev, lid, 14, 3.6)
    link(lid, sub_w(w, 0.30, 0.66), "a")
    occ(f"m{a}", sub_w(w, 0.55, 0.85), 1); occ(f"m{b}", sub_w(w, 0.55, 0.85), 1)
    lb_op(la, "t", sub_w(w, 0.55, 0.90), 1); lb_op(lb_, "t", sub_w(w, 0.55, 0.90), 1)
    ak(lid, "t", sub_w(w, 0.30, 0.70), 1); KG[lid].to(*sub_w(w, 0.30, 0.70), (1,))
    for nm in halves(lid): ol_set(nm, w[0], wt=1.0); ol_iv(nm, sub_w(w, 0.24, 0.80), 0.0, 1.0)
create("C6", 6, "4a", "10a")
create("C4", 4, "3a", "9a")
# sources removed by hand: back to the vacuum labels.  The only local change that does this moves one rishon on every
# corridor link; the light charges re-pair from the odd to the even corridor links -> matter clusters l3, l10, l12.
lb_op("L1", "t", sub_w(WD, 0.0, 0.5), 0); lb_op("L12", "t", sub_w(WD, 0.0, 0.5), 0)
for lid in (1, 2, 8, 11):
    link(lid, sub_w(WD, 0.15, 0.85), "v"); ak(lid, "t", sub_w(WD, 0.10, 0.60), 0); KG[lid].to(*sub_w(WD, 0.10, 0.60), (0,))
for lid in (3, 10, 12):
    link(lid, sub_w(WD, 0.15, 0.85), "a"); ak(lid, "t", sub_w(WD, 0.40, 0.95), 1); KG[lid].to(*sub_w(WD, 0.40, 0.95), (1,))
for name, (p_old, q_new) in {"7a": ("r1R", "r3R"), "2a": ("r2L", "r3L"), "8a": ("r2R", "r10R"), "5a": ("r8L", "r10L"),
                             "11a": ("r8R", "r12R"), "6a": ("r11L", "r12L")}.items():
    mv = {"7a": "m7", "2a": "m2", "8a": "m8", "5a": "m5", "11a": "m11", "6a": "m6"}[name]
    lb_to(name, sub_w(WD, 0.25, 0.95), q_new, mv)
    tr = LOBE[name]["ln"]; tr.key(WD[1] + 0.002, P[q_new] + P[mv]).key(WD[1] + 0.002, P[mv] + P[q_new])
for name, ends in (("L1", ("Q", "m1")), ("L12", ("Qb", "m12"))):
    LOBE[name]["ln"].key(WD[1] + 0.002, LOBE[name]["ln"].cur).key(WD[1] + 0.002, P[ends[0]] + P[ends[1]])
for key in ("Q", "Qb", "1.1", "11.12"): ol_w(key, sub_w(WD, 0.05, 0.50), 0)
for nm in ("1.7", "2.2", "2.8", "8.5", "8.11", "11.6"): ol_iv(nm, sub_w(WD, 0.15, 0.85), 0.0, 0.0)
for nm in ("3.2", "3.7", "10.5", "10.8", "12.6", "12.11"): ol_iv(nm, sub_w(WD, 0.15, 0.85), 0.0, 1.0)
for lid in (1, 2, 8, 11):
    for nm in halves(lid): ol_set(nm, WD[1] + 0.003, q=0.0, wt=0.0)
# ring B resonates, then hands the resonance back to ring A through the shared covering K1(A) = K1(B) on l10
for n in K1B_N: lb_op(n, "t", UNPIN_B, 0); lb_op(n, "g", UNPIN_B, 1)
for lid in K1B: ak(lid, "t", UNPIN_B, 0); ak(lid, "g", UNPIN_B, 1); KG[lid].to(*UNPIN_B, (0,))
RG["B"].to(*UNPIN_B, (1,)); HL["B"].to(*UNPIN_B, (1,))
for lid in K1B:
    for nm in halves(lid): ol_w(nm, UNPIN_B, 0)
GC["B"].to(UNPIN_B[0], UNPIN_B[1] + 0.006, (60, 1))
b0, bm, b1 = RES_B
for n in K1B_N: lb_op(n, "g", (b0, bm), 0); lb_op(n, "g", (bm, b1), 1)
for n in K2B_L: lb_op(n, "g", (b0, bm), 1); lb_op(n, "g", (bm, b1), 0)
for lid in K1B: ak(lid, "g", (b0, bm), 0); ak(lid, "g", (bm, b1), 1); link(lid, (b0, bm), "v"); link(lid, (bm, b1), "a")
for lid in K2B: ak(lid, "g", (b0, bm), 1); ak(lid, "g", (bm, b1), 0); link(lid, (b0, bm), "a"); link(lid, (bm, b1), "v")
for n in ("3a", "9a", "6a", "11a"): lb_op(n, "g", HAND, 0); lb_op(n, "t", HAND, 1)
for n in ("2a", "7a", "4a", "10a"): lb_op(n, "t", HAND, 0); lb_op(n, "g", HAND, 1)
for lid in (4, 12): ak(lid, "g", HAND, 0); ak(lid, "t", HAND, 1); KG[lid].to(*HAND, (1,))
for lid in (3, 6): ak(lid, "t", HAND, 0); ak(lid, "g", HAND, 1); KG[lid].to(*HAND, (0,))
RG["B"].to(*HAND, (0,)); RG["A"].to(*HAND, (1,)); HL["B"].to(*sub_w(HAND, 0.0, 0.45), (0,)); HL["A"].to(*sub_w(HAND, 0.55, 1.0), (1,))
for lid in (3, 6):
    for nm in halves(lid): ol_w(nm, HAND, 0)
for lid in (4, 12):
    for nm in halves(lid): ol_w(nm, HAND, 1)
GC["B"].to(*HAND, (68, 0)).key(HAND[1] + 0.001, (72, 0)); GC["A"].to(*HAND, (60, 1))
# formation captions: at the start (glueball in ring A, matter on l4, l12) and at the end (glueball in ring B, matter on
# l3, l6); the formed tube and its breaking are captioned at the shared edge l10, where the string breaks first
T("f1-mfB", "op", (1,)).to(INS[0] - 0.004, INS[0] + 0.008, (0,)).to(*sub_w(HAND, 0.55, 1.0), (1,))
T("f1-mfA", "op", (0,)).to(UNPIN_B[0] + 0.004, UNPIN_B[1] + 0.010, (1,)).to(*sub_w(HAND, 0.0, 0.45), (0,))
for t in tracks:
    t.close()
TR = {t.id + ":" + t.typ: t for t in tracks}

# ======== exactness check of every discrete frame ========
D_VAC = {}
for v in V:
    D_VAC[v] = (0 if v in A_SITES else 2) - sum(0 if v == a else 2 for lid, (a, b) in LINKS.items() if v in (a, b))
def check(u, sector):
    n = {s: TR[f"f1-s-{s}:occ"].sample(u)[0] for s in OCC}
    for s, x in n.items():
        assert abs(x - round(x)) < 1e-6, (u, s, x)
    n = {s: int(round(x)) for s, x in n.items()}
    src = sector == "src"
    for lid in LINKS:
        assert n[f"r{lid}L"] + n[f"r{lid}R"] == 2, (u, lid)
    D = {v: n[f"m{v}"] - sum(n[f"r{lid}L"] if v == a else n[f"r{lid}R"] for lid, (a, b) in LINKS.items() if v in (a, b)) for v in V}
    want = dict(D_VAC)
    if src:
        want.update({1: -1, 7: -2, 2: -2, 8: -2, 5: -2, 11: 0, 6: -2, 12: 1})
    assert D == want, (u, sector, {v: (D[v], want[v]) for v in V if D[v] != want[v]})
    single = {s for s, x in n.items() if x == 1} | ({"Q", "Qb"} if src else set())
    seen = []
    for name, d in LOBE.items():
        if sum(TR[f"f1-lb-{name}-{c}:op"].sample(u)[0] for c in d["layers"]) < 0.5:
            continue
        x1, y1, x2, y2 = d["ln"].sample(u)
        ends = [min(P, key=lambda s: dist(P[s], (x, y))) for x, y in ((x1, y1), (x2, y2))]
        assert all(dist(P[e], (x, y)) < 1e-3 for e, (x, y) in zip(ends, ((x1, y1), (x2, y2)))), (u, name)
        assert SV[ends[0]] == SV[ends[1]] and ends[0] != ends[1], (u, name, ends)
        seen += ends
    assert sorted(seen) == sorted(single), (u, sector, sorted(set(seen) ^ single))
    for lid in LINKS:
        act = sum(TR[f"f1-ak{lid}{c}:op"].sample(u)[0] for c in "tg" if f"f1-ak{lid}{c}:op" in TR)
        assert (act > 0.5) == (n[f"r{lid}L"] == 1), (u, lid, act)
CHECKS = [(0.0, "vac"), (RES_A[1], "vac"), (0.097, "vac"), (0.131, "src"), (uR(0.9), "src"), (uR(1.4), "src"),
          (uR(1.955), "src"), (uR(2.255), "src"), (uR(2.705), "src"), (0.505, "src"), (uQ(0.70), "src"), (uQ(1.30), "src"),
          (uQ(1.37), "src"), (uQ(1.90), "src"), (0.8925, "vac"), (RES_B[1], "vac"), (0.9655, "vac"), (0.9995, "vac")]
for u, sector in CHECKS:
    check(u, sector)

# ======== colour-singlet outlines: field, contour (mirrors the runtime) and their own check ========
def ol_segments(u):
    segs = []
    for name, a, m in BS_LIST:
        p, q = TR[f"f1-bi-{name}:bi"].sample(u); w = TR[f"f1-bw-{name}:bw"].sample(u)[0]
        if w < 0.004 or q - p < 1e-4:
            continue
        segs.append((a[0] + (m[0] - a[0]) * p, a[1] + (m[1] - a[1]) * p, a[0] + (m[0] - a[0]) * q, a[1] + (m[1] - a[1]) * q, w))
    return segs
def ol_loops(u):
    segs = ol_segments(u)
    if not segs:
        return []
    R = 3 * SIG; F = {}
    for ax, ay, bx, by, w in segs:
        L = math.hypot(bx - ax, by - ay); ux, uy = (bx - ax) / L, (by - ay) / L
        for j in range(max(0, math.floor((min(ay, by) - R - GY0) / GRID)), min(GNY - 1, math.ceil((max(ay, by) + R - GY0) / GRID)) + 1):
            y = GY0 + j * GRID
            for i in range(max(0, math.floor((min(ax, bx) - R - GX0) / GRID)), min(GNX - 1, math.ceil((max(ax, bx) + R - GX0) / GRID)) + 1):
                x = GX0 + i * GRID; dx, dy = x - ax, y - ay
                t = dx * ux + dy * uy; d = dx * uy - dy * ux
                if d * d > R * R or t < -R or t > L + R:
                    continue
                F[(i, j)] = F.get((i, j), 0.0) + w * math.exp(-d * d / SIG ** 2) * SQPI2 * (math.erf((L - t) / SIG) + math.erf(t / SIG))
    f_ = lambda i, j: F.get((i, j), 0.0)
    pts, nb = {}, {}
    def ept(e):
        if e not in pts:
            k, ij = e % 2, e // 2; i, j = ij % GNX, ij // GNX
            if k == 0:
                a, b = f_(i, j), f_(i + 1, j); pts[e] = (GX0 + (i + (LEV - a) / (b - a)) * GRID, GY0 + j * GRID)
            else:
                a, b = f_(i, j), f_(i, j + 1); pts[e] = (GX0 + i * GRID, GY0 + (j + (LEV - a) / (b - a)) * GRID)
        return e
    def lk(a, b):
        nb.setdefault(ept(a), []).append(ept(b)); nb.setdefault(b, []).append(a)
    cells = {(i + di, j + dj) for (i, j) in F for di in (-1, 0) for dj in (-1, 0)}
    for i, j in cells:
        v0, v1, v2, v3 = f_(i, j), f_(i + 1, j), f_(i + 1, j + 1), f_(i, j + 1)
        c = (v0 > LEV) | (v1 > LEV) << 1 | (v2 > LEV) << 2 | (v3 > LEV) << 3
        if c in (0, 15):
            continue
        e0, e1, e2, e3 = 2 * (j * GNX + i), 2 * (j * GNX + i + 1) + 1, 2 * ((j + 1) * GNX + i), 2 * (j * GNX + i) + 1
        inside_c = (v0 + v1 + v2 + v3) / 4 > LEV
        table = {1: [(e3, e0)], 2: [(e0, e1)], 3: [(e3, e1)], 4: [(e1, e2)], 6: [(e0, e2)], 7: [(e3, e2)], 8: [(e2, e3)],
                 9: [(e0, e2)], 11: [(e1, e2)], 12: [(e1, e3)], 13: [(e0, e1)], 14: [(e3, e0)],
                 5: [(e0, e1), (e2, e3)] if inside_c else [(e3, e0), (e1, e2)],
                 10: [(e3, e0), (e1, e2)] if inside_c else [(e0, e1), (e2, e3)]}
        for a, b in table[c]:
            lk(a, b)
    loops, seen = [], set()
    for e0_ in nb:
        if e0_ in seen:
            continue
        loop, prev, cur = [], None, e0_
        while cur not in seen:
            seen.add(cur); loop.append(pts[cur])
            n0 = nb[cur]; nxt = n0[0] if n0[0] != prev else n0[-1]
            prev, cur = cur, nxt
        loops.append(loop)
    return loops
def inside(pt, loop):
    x, y = pt; c = False
    for (x1, y1), (x2, y2) in zip(loop, loop[1:] + loop[:1]):
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            c = not c
    return c
# expected singlet objects (each must be one outline, enclosing exactly these sites)
OBJ = {
    "vacA": [("m3", "m9"), ("m6", "m11")],
    "pin": [("Q", "m1"), ("Qb", "m12"), ("m2", "m7"), ("m5", "m8"), ("m4", "m10"), ("m3", "m9"), ("m6", "m11")],
    "o6": [("Q", "m1"), ("Qb", "m12"), ("m2", "m7"), ("m5", "m8"), ("m3", "m9"), ("m6", "m11")],
    "o4": [("Q", "m1"), ("Qb", "m12"), ("m2", "m7"), ("m5", "m8"), ("m6", "m11")],
    "j11": [("Q", "m1"), ("m2", "m7"), ("m5", "m8"), ("Qb", "m12", "m6", "m11")],
    "j8": [("Q", "m1"), ("m2", "m7"), ("Qb", "m12", "m6", "m11", "m5", "m8")],
    "tube": [("Q", "m1", "m7", "m2", "m8", "m5", "m11", "m6", "m12", "Qb")],
    "b10": [("Q", "m1", "m7", "m2", "m8"), ("m5", "m11", "m6", "m12", "Qb")],
    "four": [("Q", "m1", "m7"), ("m2", "m8"), ("m5", "m11"), ("m6", "m12", "Qb")],
    "six": [("Q", "m1", "m7"), ("m2", "m8"), ("m5", "m11"), ("m6", "m12", "Qb"), ("m4", "m10"), ("m3", "m9")],
    "wd": [("m2", "m7"), ("m5", "m8"), ("m6", "m11"), ("m4", "m10"), ("m3", "m9")],
    "vacB": [("m2", "m7"), ("m4", "m10")],
}
OL_CHECKS = [(0.0, "vacA"), (RES_A[1], "vacA"), (0.097, "vacA"), (0.131, "pin"), (uR(0.9), "o6"), (uR(1.4), "o4"),
             (uR(1.955), "j11"), (uR(2.255), "j8"), (uR(2.705), "tube"), (0.505, "tube"), (uQ(0.70), "b10"),
             (uQ(1.30), "four"), (uQ(1.37), "four"), (uQ(1.90), "six"), (0.8925, "wd"), (RES_B[1], "vacB"),
             (0.9655, "vacB"), (0.9995, "vacA")]
for u, key in OL_CHECKS:
    loops = ol_loops(u); want = OBJ[key]
    assert len(loops) == len(want), (u, key, len(loops), len(want))
    for obj in want:
        hits = [k for k, lp in enumerate(loops) if all(inside(P[s], lp) for s in obj)]
        assert len(hits) == 1, (u, key, obj, hits)
    for lp in loops:                                     # no outline swallows a site of another object
        sites = {s for s in ("Q", "Qb", *[f"m{v}" for v in V]) if inside(P[s], lp)}
        assert any(sites == set(obj) for obj in want), (u, key, sorted(sites))

# ---------------- exact data ----------------
def data_at(u):
    if u < INS[1] or u > WD[0]:
        return None
    if u <= U_R1:
        d, t = RT["r"], max(0.0, 4 * (u - U_R0) / (U_R1 - U_R0))
    else:
        d, t = RT["q"], (0.0 if u < U_Q0 else min(2.0, 2 * (u - U_Q0) / (U_Q1 - U_Q0)))
    i = min(int(t / 0.025), len(d["t"]) - 2); w = (t - d["t"][i]) / 0.025
    return {k: d[k][i] * (1 - w) + d[k][i + 1] * w for k in ("conn", "f1", "f2", "f0", "tau")}

# ---------------- svg ----------------
svg = []
def text(x, y, s, cls, anchor="middle", extra=""):
    return f'<text class="{cls}" x="{f(x)}" y="{f(y)}" text-anchor="{anchor}"{extra}>{s}</text>'
def sub(b, i, cls="f1-sub"):
    return f'{b}<tspan class="{cls}" dy="2.6">{i}</tspan><tspan dy="-2.6"> </tspan>'
def sup(b, i, cls="f1-sub"):
    return f'{b}<tspan class="{cls}" dy="-4.4">{i}</tspan><tspan dy="4.4"> </tspan>'
def Pd(pts):
    return "M" + " L".join(f"{f(x)} {f(y)}" for x, y in pts)
def P1(pts):
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
def st(tid, typ):
    return TR[f"{tid}:{typ}"].sample(U_STATIC)
def op_style(tid):
    return f'style="opacity:{st(tid, "op")[0]:.3f}"'
def seg(p, q):
    return f"M{f(p[0])} {f(p[1])} L{f(q[0])} {f(q[1])}"

svg.append(
    '<defs>'
    '<radialGradient id="f1-burst-g"><stop offset="0" stop-color="#f2fffd" stop-opacity=".95"/>'
    '<stop offset=".4" stop-color="#8ff0ea" stop-opacity=".35"/><stop offset="1" stop-color="#8ff0ea" stop-opacity="0"/></radialGradient>'
    f'<clipPath id="f1-elapsed"><rect id="f1-elapsed-r" x="{f(AX0 - 3)}" y="230" width="{f(X(U_STATIC) - AX0 + 3)}" height="70"/></clipPath>'
    '</defs>')

# ----- readout -----
D0 = data_at(U_STATIC)
def tdisp(u):
    if u < INS[1] or u > WD[0]: return "vac"
    if u <= U_R1: return f"{max(0.0, 4 * (u - U_R0) / (U_R1 - U_R0)):.2f}"
    if u < U_Q0: return "GS"
    return f"{min(2.0, 2 * (u - U_Q0) / (U_Q1 - U_Q0)):.2f}"
RO_X, RO_V = 9, 128
rows = [("t", tdisp(U_STATIC), "f1-ro-t", "f1-ro-v"),
        (f'µ = 2m/g{sup("", "2")}', f"{mu_of(U_STATIC):.2f}", "f1-ro-mu", "f1-ro-v"),
        (sub("P", "conn"), f"{D0['conn']:.3f}" if D0 else "—", "f1-ro-pc", "f1-ro-v f1-ro-vc"),
        (sub("P", "≥1ff"), f"{D0['f1'] + D0['f2']:.3f}" if D0 else "—", "f1-ro-pf", "f1-ro-v f1-ro-vf"),
        (f'τ{sub("", "E")}', f"{D0['tau']:.3f}" if D0 else "—", "f1-ro-tau", "f1-ro-v")]
svg.append('<g class="f1-ro">')
svg.append('<rect class="f1-panel" x="4" y="3" width="148" height="64" rx="1.5"/>')
svg.append(text(RO_X, 10.2, "READOUT", "f1-ro-h", "start") + text(147, 10.2, "live", "f1-ro-hs", "end"))
for i, (k, v, vid, vcls) in enumerate(rows):
    y = 21.5 + i * 10.6
    svg.append(text(RO_X, y, k, "f1-ro-k", "start") + text(RO_V, y, v, vcls, "end", f' id="{vid}"'))
svg.append(text(RO_V + 3, 21.5 + 4 * 10.6, "J/a", "f1-ro-u", "start"))
svg.append('</g>')

# ----- magnetic-term inset -----
IX0, IX1, IY0, IY1 = 24.0, 146.0, 92.0, 126.0
def ix(m): return IX0 + (m - 0.5) / 3.5 * (IX1 - IX0)
def iy(p): return IY1 - p * (IY1 - IY0)
K = RT["kappa"]
ins = ['<g class="f1-kin">', '<rect class="f1-panel" x="4" y="71" width="148" height="69" rx="1.5"/>']
ins.append(text(9, 78.5, "MAGNETIC TERM", "f1-kin-h", "start") + text(147, 78.5, f'κ Tr{sub("U", "p")}', "f1-kin-hm", "end"))
ins.append(text(9, 87, f'static {sub("P", "conn")}(m), R = 4', "f1-kin-s", "start"))
ins.append(f'<path class="f1-kin-ax" d="M{f(IX0)} {f(IY0)} L{f(IX0)} {f(IY1)} L{f(IX1)} {f(IY1)}"/>')
ins.append(f'<path class="f1-kin-half" d="M{f(IX0)} {f(iy(0.5))} L{f(IX1)} {f(iy(0.5))}"/>')
ins.append(text(IX0 - 3, iy(1) + 2.4, "1", "f1-kin-n", "end") + text(IX0 - 3, iy(0) + 1.6, "0", "f1-kin-n", "end"))
for m, lab in ((0.5, "½"), (2, "2"), (4, "4")):
    ins.append(f'<path class="f1-kin-ax" d="M{f(ix(m))} {f(IY1)} L{f(ix(m))} {f(IY1 + 2)}"/>' + text(ix(m), IY1 + 8.5, lab, "f1-kin-n"))
ins.append(text(ix(1.25), IY1 + 8.5, "m", "f1-kin-m"))
def series(key, cls):
    pts = K[key]; out = []
    for (m0, p0, b0), (m1, p1, b1) in zip(pts, pts[1:]):
        out.append(f'<path class="{cls}{" is-switch" if b0 != b1 else ""}" d="{Pd([(ix(m0), iy(p0)), (ix(m1), iy(p1))])}"/>')
    for (m, p, b) in pts:
        out.append(f'<circle class="{cls}-d {"is-p" if b == "P" else "is-e"}" cx="{f(ix(m))}" cy="{f(iy(p))}" r="1.7"/>')
    return out
ins += series("4", "f1-kin-k4") + series("2", "f1-kin-k2") + series("0", "f1-kin-k0")
ins.append(text(ix(2.85), iy(0.84) - 3.2, "κ = 0", "f1-kin-l f1-kin-l0", "middle"))
ins.append(text(ix(2.6), iy(0.25), "κ = 2", "f1-kin-l f1-kin-l2", "middle"))
ins.append(text(ix(4) - 1.5, iy(0.318) + 8.6, "κ = 4", "f1-kin-l f1-kin-l4", "end"))
ins.append(f'<path id="f1-kin-mk" class="f1-kin-mk" d="M{f(ix(mu_of(U_STATIC)))} {f(IY0 - 1)} L{f(ix(mu_of(U_STATIC)))} {f(IY1)}"/>')
ins.append('</g>')
svg.extend(ins)

# ----- underlay (its own compositor layer): glow of the glueball rings and of the off-corridor bonds -----
under = ['<defs><radialGradient id="f1-plaq-g"><stop offset="0" stop-color="#e2c27e" stop-opacity=".12"/>'
         '<stop offset="1" stop-color="#e2c27e" stop-opacity="0"/></radialGradient></defs>']
for h, hv in HEXV.items():
    ring = [V[k] for k in hv]; c = HEXC[h]
    under.append(f'<g id="f1-rg{h}" class="f1-rg" {op_style(f"f1-rg{h}")}>'
                 f'<circle cx="{f(c[0])}" cy="{f(c[1])}" r="58" fill="url(#f1-plaq-g)"/>'
                 f'<path class="f1-rg-g1" d="{Pd(ring + [ring[0]])} Z"/><path class="f1-rg-g2" d="{Pd(ring + [ring[0]])} Z"/></g>')

# ----- vertices: triangles of sites -----
svg.append('<g class="f1-tris">' + "".join(f'<path class="f1-tri" d="{Pd(tri_pts(v))} Z"/>' for v in V) + '</g>')
svg.append('<g class="f1-links">' + "".join(f'<path class="f1-lk" d="{seg(P[f"r{lid}L"], P[f"r{lid}R"])}"/>' for lid in LINKS) + '</g>')
# link glow: the corridor follows P_conn (runtime), the off-corridor matter clusters stay quiet
def kg(lid):
    d = seg(P[f"r{lid}L"], P[f"r{lid}R"])
    return f'<g id="f1-kg{lid}" class="f1-kg" {op_style(f"f1-kg{lid}")}><path class="f1-kg1" d="{d}"/><path class="f1-kg2" d="{d}"/></g>'
D0c = D0["conn"] if D0 else 0
tube_markup = "".join(kg(l) for l in PATH)
under.append('<g class="f1-bondglow">' + "".join(kg(l) for l in T_LINKS if l not in PATH) + '</g>')
akl = []
for (lid, c) in AK:
    akl.append(f'<path id="f1-ak{lid}{c}" class="f1-ak f1-ak-{c}" d="{seg(P[f"r{lid}L"], P[f"r{lid}R"])}" {op_style(f"f1-ak{lid}{c}")}/>')
svg.append('<g class="f1-aks">' + "".join(akl) + '</g>')
svg.append(f'<g id="f1-lflash" class="f1-lflash" {op_style("f1-lflash")}>'
           + "".join(f'<path class="f1-link-flash" d="{seg(P[f"r{lid}L"], P[f"r{lid}R"])}"/>' for lid in LINKS) + '</g>')
svg.append(f'<g id="f1-iflash" class="f1-iflash" {op_style("f1-iflash")}>'
           + "".join(f'<path class="f1-link-iflash" d="{seg(P[f"r{lid}L"], P[f"r{lid}R"])}"/>' for lid in (1, 2, 8, 11)) + '</g>')
svg.append(f'<g id="f1-wflash" class="f1-iflash" {op_style("f1-wflash")}>'
           + "".join(f'<path class="f1-link-iflash" d="{seg(P[f"r{lid}L"], P[f"r{lid}R"])}"/>' for lid in PATH) + '</g>')
# singlet lobes
lb = ['<g class="f1-lobes">']
for name, d in LOBE.items():
    x1, y1, x2, y2 = st(f"f1-lb-{name}", "ln"); dd = f"M{x1:.2f} {y1:.2f}L{x2:.2f} {y2:.2f}"
    lb.append(f'<g id="f1-lb-{name}">')
    for c in d["layers"]:
        lb.append(f'<g id="f1-lb-{name}-{c}" class="f1-lb f1-lb-{c}" {op_style(f"f1-lb-{name}-{c}")}>'
                  f'<path class="f1-lo" d="{dd}"/><path class="f1-lm" d="{dd}"/><path class="f1-lc" d="{dd}"/></g>')
    lb.append('</g>')
lb.append('</g>')
svg.extend(lb)
# sites: ring, fill (one fermion), on-site singlet halo (two fermions; the inert pair is drawn quieter)
def fill_op(o): return o if o <= 1 else 1 - 0.45 * (o - 1)
sites = ['<g class="f1-sites">']
for s in OCC:
    x, y = P[s]; o = st(f"f1-s-{s}", "occ")[0]
    sites.append(f'<g id="f1-s-{s}" class="f1-st"><circle class="f1-sh" cx="{f(x)}" cy="{f(y)}" r="{f(RS + 2.3)}" style="opacity:{max(0, o - 1):.3f}"/>'
                 f'<circle class="f1-sr" cx="{f(x)}" cy="{f(y)}" r="{f(RS)}"/>'
                 f'<circle class="f1-sf" cx="{f(x)}" cy="{f(y)}" r="{f(RS - 0.25)}" style="opacity:{fill_op(o):.3f}"/></g>')
sites.append('</g>')
svg.extend(sites)
# vacuum-pair glyphs: q (particle on an A site, filled) and q-bar (hole on a B site, open); halos and bursts
for name, lid in HALOS:
    m = lmid(lid); r, o = st(f"f1-gh-{name}", "burst")
    svg.append(f'<circle id="f1-gh-{name}" class="f1-ghalo" cx="{f(m[0])}" cy="{f(m[1])}" r="{f(r)}" style="opacity:{o:.3f}"/>')
for gid, kind in GLYPHS:
    x, y = st(gid, "tr")
    core = '<circle class="f1-g-c" r="2.25"/>' if kind == "q" else '<circle class="f1-g-o" r="2.05"/>'
    svg.append(f'<g id="{gid}" class="f1-g f1-g-{kind}" transform="translate({f(x)} {f(y)})" {op_style(gid)}>'
               f'<circle class="f1-g-h" r="6.4"/>{core}</g>')
for name, (lid, tr) in BURSTS.items():
    m = lerp(P[f"r{lid}L"], P[f"r{lid}R"], 0.5); r, o = tr.sample(U_STATIC)
    svg.append(f'<circle id="f1-bu-{name}" class="f1-burst" cx="{f(m[0])}" cy="{f(m[1])}" r="{f(r)}" style="opacity:{o:.3f}"/>')

# ----- sources (placed by hand) -----
SRC = {1: ("Q", "+1", "Q", (-11.5, 4.5), (-11, 16), "end", "end"), 12: ("Q̄", "−1", "Qb", (11.5, 4.5), (W - 3 - P["Qb"][0], 19.5), "start", "end")}
for v, (lab, q3, key, (lx, ly), (qx, qy), anc, qanc) in SRC.items():
    x, y = P[key]; r, o = st(f"f1-ins{v}", "burst")
    svg.append(f'<circle id="f1-ins{v}" class="f1-ins" cx="{f(x)}" cy="{f(y)}" r="{f(r)}" style="opacity:{o:.3f}"/>')
    svg.append(f'<g id="f1-src{v}" class="f1-srcg" {op_style(f"f1-src{v}")}><circle class="f1-src" cx="{f(x)}" cy="{f(y)}" r="7.6"/>'
               f'<circle class="f1-srcs" cx="{f(x)}" cy="{f(y)}" r="{f(RS + 0.5)}"/>'
               + text(x + lx, y + ly, lab, "f1-srcl", anc) + text(x + qx, y + qy, f'{sup("q", "3")}= {q3}', "f1-srcq", qanc) + '</g>')

# ----- labels -----
LBL = []
for lid, (a, b) in LINKS.items():
    pa, pb = P[f"r{lid}L"], P[f"r{lid}R"]; mx, my = (pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2
    nx, ny = perp(pa, pb)
    hs = [h for h, hv in HEXV.items() if a in hv and b in hv]
    if len(hs) == 2:
        nx, ny = -1.0, 0.0
    else:
        c = HEXC[hs[0]] if hs else PC
        if (mx + nx - c[0]) ** 2 + (my + ny - c[1]) ** 2 < (mx - c[0]) ** 2 + (my - c[1]) ** 2:
            nx, ny = -nx, -ny
    if lid in (4, 6, 7):
        nx, ny = -nx, -ny
    off = 12.0 if len(hs) == 2 else 10.5     # clear of the bond glow; the label halo cuts the outline, not the glow
    dy = 15 if len(hs) == 2 else 0          # the shared edge carries the central pair creation: label below it
    LBL.append(text(mx + nx * off, my + ny * off + 3 + dy, sub("ℓ", lid, "f1-sub f1-sub-id"), "f1-lid"))
VLBL = {2: (12.5, 9, "start"), 3: (12.5, 9, "start"), 4: (-13.5, 9, "end"), 5: (0, -14.5, "middle"), 6: (13.5, 9, "start"),
        7: (-13.5, -5, "end"), 8: (0, 22.5, "middle"), 9: (13.5, -5, "start"), 10: (13.5, -5, "start"), 11: (-12.5, -9, "end")}
for v, (dx, dy, anc) in VLBL.items():
    LBL.append(text(V[v][0] + dx, V[v][1] + dy, v, "f1-vid", anc))
CH = {"f1-lq5": (V[5][0] + 11, V[5][1] + 13, "q", "start"), "f1-lqb8": (V[8][0] - 11, V[8][1] - 9.5, "q̄", "end"),
      "f1-lq2": (V[2][0] - 12, V[2][1] + 13, "q", "end"), "f1-lqb7": (V[7][0] + 12, V[7][1] - 6, "q̄", "start"),
      "f1-lq6": (V[6][0] - 12, V[6][1] + 9, "q", "end"), "f1-lqb11": (V[11][0] + 12, V[11][1] - 9.5, "q̄", "start")}
for cid, (x, y, s_, anc) in CH.items():
    LBL.append(text(x, y, s_, "f1-ch", anc, f' id="{cid}" {op_style(cid)}'))
# ----- annotation layer (its own compositor layer): singlet outlines, glueball markers, captions -----
def ol_d(loops):
    """closed quadratic B-splines through the contour points; each loop is oriented one way and starts at its extreme
    point along (0.8, 0.6), so the dash pattern stays put while the outline morphs (identical to the runtime)"""
    out = []
    for lp in loops:
        area = sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(lp, lp[1:] + lp[:1]))
        if area < 0:
            lp = lp[::-1]
        k0 = min(range(len(lp)), key=lambda k: 0.8 * lp[k][0] + 0.6 * lp[k][1])
        lp = lp[k0:] + lp[:k0]
        pts = [lp[0]]
        for q_ in lp[1:]:
            if math.hypot(q_[0] - pts[-1][0], q_[1] - pts[-1][1]) >= OL_STEP:
                pts.append(q_)
        n = len(pts)
        if n < 3:
            continue
        md = lambda a, b: ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        r1 = lambda x: f"{round(x * 10) / 10:g}"
        m0 = md(pts[-1], pts[0]); d = f"M{r1(m0[0])} {r1(m0[1])}"
        for k in range(n):
            q_ = md(pts[k], pts[(k + 1) % n]); d += f"Q{r1(pts[k][0])} {r1(pts[k][1])} {r1(q_[0])} {r1(q_[1])}"
        out.append(d + "Z")
    return "".join(out)
OL_STEP = 2.2
ann = ['<defs><radialGradient id="f1-flash-g"><stop offset="0" stop-color="#e9fffb" stop-opacity=".6"/>'
       '<stop offset=".45" stop-color="#8ff0ea" stop-opacity=".14"/><stop offset="1" stop-color="#8ff0ea" stop-opacity="0"/></radialGradient></defs>']
r, o = st("f1-qf", "burst")
ann.append(f'<circle id="f1-qf" class="f1-qflash" cx="{f(PC[0])}" cy="{f(PC[1])}" r="{f(r)}" style="opacity:{o:.3f}"/>')
OL0 = ol_d(ol_loops(U_STATIC))
ann.append(f'<g id="f1-ol" class="f1-ol" {op_style("f1-ol")}><path id="f1-ol-g" class="f1-ol-g" d="{OL0}"/>'
           f'<path id="f1-ol-p" class="f1-ol-p" d="{OL0}"/></g>')
ann.append('<g class="f1-labels">' + "".join(LBL) + '</g>')
for h in HEXV:
    c = HEXC[h]; r, o = st(f"f1-gc{h}", "burst")
    ann.append(f'<g id="f1-gc{h}" class="f1-gc" style="opacity:{o:.3f}">'
               f'<circle class="f1-gc-g" cx="{f(c[0])}" cy="{f(c[1])}" r="{f(r)}"/><circle class="f1-gc-c" cx="{f(c[0])}" cy="{f(c[1])}" r="{f(r)}"/></g>')
    ann.append(f'<g id="f1-hl{h}" class="f1-hl" {op_style(f"f1-hl{h}")}>' + text(c[0], c[1] - 1, f'Tr {sub("U", "p")}', "f1-plaq-t")
               + '<g class="f1-co-d">' + text(c[0], c[1] + 10.5, "GLUEBALL FORMATION", "f1-plaq-c")
               + text(c[0], c[1] + 20, "ring resonance · κ &gt; 0", "f1-plaq-s") + '</g>'
               + '<g class="f1-co-m">' + text(c[0], c[1] + 12.5, "GLUEBALL", "f1-plaq-c") + text(c[0], c[1] + 23, "FORMATION", "f1-plaq-c")
               + '</g></g>')
# matter formation: caption at the centre of the free ring, one leader to each matter-cluster outline
def mf_caption(cid, h, lids):
    c = HEXC[h]; side = 1 if h == "B" else -1
    body = []
    for lid, y0 in zip(lids, (c[1] - 8.5, c[1] + 13.5)):
        a, b = LINKS[lid]; m = lerp(V[a], V[b], 0.5)
        dx, dy = c[0] - m[0], c[1] - m[1]; L = math.hypot(dx, dy)
        tip = (m[0] + dx / L * 16.5, m[1] + dy / L * 16.5)
        body.append(f'<path class="f1-co-l" d="{seg((c[0] + side * 9, y0), tip)}"/>'
                    f'<circle class="f1-co-dot" cx="{f(tip[0])}" cy="{f(tip[1])}" r="1.1"/>')
    body.append('<g class="f1-co-d">' + text(c[0], c[1] + 1.5, "MATTER FORMATION", "f1-co-t")
                + text(c[0], c[1] + 10.5, "q q̄ colour singlets", "f1-co-s") + '</g>'
                + '<g class="f1-co-m">' + text(c[0], c[1] - 0.5, "MATTER", "f1-co-t") + text(c[0], c[1] + 9.5, "FORMATION", "f1-co-t") + '</g>')
    return f'<g id="{cid}" class="f1-co f1-mf" {op_style(cid)}>' + "".join(body) + '</g>'
ann.append(mf_caption("f1-mfB", "B", (12, 4)))
ann.append(mf_caption("f1-mfA", "A", (6, 3)))
# the formed tube and its breaking are captioned at the shared edge l10, where the string breaks first
m10 = lmid(10); CX_, CY_ = 356.0, 101.0
ann.append(f'<g id="f1-cbl" class="f1-co" {op_style("f1-cbl")}><path class="f1-co-l" d="{seg((m10[0] + 4.5, m10[1] - 2), (CX_ - 3.5, CY_ + 2.5))}"/></g>')
ann.append(f'<g id="f1-ft" class="f1-co" {op_style("f1-ft")}>'
           + '<g class="f1-co-d">' + text(CX_, CY_, "FLUX TUBE FORMED", "f1-co-t", "start") + text(CX_, CY_ + 9, "one singlet chain from Q to Q̄", "f1-co-s", "start") + '</g>'
           + '<g class="f1-co-m">' + text(CX_, CY_ - 2, "FLUX TUBE", "f1-co-t", "start") + text(CX_, CY_ + 8, "FORMED", "f1-co-t", "start") + '</g></g>')
ann.append(f'<g id="f1-cb" class="f1-co" {op_style("f1-cb")}>'
           + '<g class="f1-co-d">' + text(CX_, CY_, "STRING BREAKING", "f1-co-t", "start")
           + text(CX_, CY_ + 9, "q q̄ pair from the vacuum", "f1-co-s", "start", f' id="f1-cb1" {op_style("f1-cb1")}')
           + text(CX_, CY_ + 9, "four short strings", "f1-co-s", "start", f' id="f1-cb2" {op_style("f1-cb2")}') + '</g>'
           + '<g class="f1-co-m">' + text(CX_, CY_ - 2, "STRING", "f1-co-t", "start") + text(CX_, CY_ + 8, "BREAKING", "f1-co-t", "start") + '</g></g>')

# ----- time axis -----
tl = ['<g class="f1-tl">']
mu_tr = [(X(0), Ymu(0.5)), (X(U_R0), Ymu(0.5)), (X(U_R1), Ymu(4)), (X(U_Q0), Ymu(4)), (X(U_Q0), Ymu(0.5)), (X(1), Ymu(0.5))]
tl.append(f'<path class="f1-mustar" d="M{f(AX0)} {f(Ymu(MU_STAR))} L{f(AX1)} {f(Ymu(MU_STAR))}"/>')
tl.append(text(AX1, Ymu(MU_STAR) - 3.2, 'µ* = 9/8', "f1-mustar-t", "end"))
tl.append(f'<path class="f1-trace-dim" d="{Pd(mu_tr)}"/>')
tl.append(f'<path class="f1-trace" d="{Pd(mu_tr)}" clip-path="url(#f1-elapsed)"/>')
tl.append(text(9, Ymu(2.25) + 3.5, "µ", "f1-tl-mu", "start"))
def bands(seg_):
    d = RT[seg_]
    idx = list(range(0, len(d["t"]), 2)); idx += [] if idx[-1] == len(d["t"]) - 1 else [len(d["t"]) - 1]
    xs = [X(uR(d["t"][i])) if seg_ == "r" else X(uQ(d["t"][i])) for i in idx]
    c1 = [d["conn"][i] for i in idx]
    c2 = [a + d["f1"][i] for a, i in zip(c1, idx)]
    c3 = [a + d["f2"][i] for a, i in zip(c2, idx)]
    c0 = [0.0] * len(xs); c4 = [1.0] * len(xs)
    def area(lo, hi):
        top = [(x, Yp(v)) for x, v in zip(xs, hi)]; bot = [(x, Yp(v)) for x, v in zip(xs[::-1], lo[::-1])]
        return P1(top + bot) + " Z"
    def line(v):
        return P1([(x, Yp(y)) for x, y in zip(xs, v)])
    return dict(conn=area(c0, c1), f1=area(c1, c2), f2=area(c2, c3), f0=area(c3, c4), lc=line(c1), l1=line(c2), l2=line(c3))
BR, BQ = bands("r"), bands("q")
for layer, clip in (("dim", ""), ("lit", ' clip-path="url(#f1-elapsed)"')):
    tl.append(f'<g class="f1-cls f1-cls-{layer}"{clip}>')
    for B in (BR, BQ):
        tl.append(f'<path class="f1-b0" d="{B["f0"]}"/><path class="f1-b2" d="{B["f2"]}"/>'
                  f'<path class="f1-b1" d="{B["f1"]}"/><path class="f1-bc" d="{B["conn"]}"/>'
                  f'<path class="f1-bl2" d="{B["l2"]}"/><path class="f1-bl1" d="{B["l1"]}"/><path class="f1-blc" d="{B["lc"]}"/>')
    tl.append('</g>')
HEXI = [(math.cos(math.radians(90 + 60 * k)), -math.sin(math.radians(90 + 60 * k))) for k in range(6)]
for u0, u1 in ((0, U_R0), (U_Q1, 1)):
    tl.append(f'<rect class="f1-vacband" x="{f(X(u0) + 1)}" y="{f(PT)}" width="{f(X(u1) - X(u0) - 2)}" height="{f(PB - PT)}"/>')
    tl.append(text((X(u0) + X(u1)) / 2, PT + 13, "vacuum", "f1-vact"))
for (r0, r1) in ((RES_A[0], RES_A[2]), (UNPIN_B[0], HAND[1])):     # glueball-cluster windows
    cx = X((r0 + r1) / 2); cy = PT + 21.5
    tl.append(f'<path class="f1-tl-hex" d="{Pd([(cx + 3.4 * a, cy + 3.4 * b) for a, b in HEXI])} Z"/>')
tl.append(f'<path class="f1-pframe" d="M{f(X(U_R0))} {f(PT)} L{f(X(U_R1))} {f(PT)} M{f(X(U_Q0))} {f(PT)} L{f(X(U_Q1))} {f(PT)}"/>')
gx = (X(U_R1) + X(U_Q0)) / 2
tl.append(f'<path class="f1-gs-l" d="M{f(gx)} {f(PT + 2)} L{f(gx)} {f(PT + 9)} M{f(gx)} {f(PB - 9)} L{f(gx)} {f(PB - 2)}"/>')
tl.append(text(gx, (PT + PB) / 2 + 2.2, "GS", "f1-gs"))
tl.append(text(AX0 - 5, Yp(1) + 2.6, "1", "f1-tl-num", "end") + text(AX0 - 5, Yp(0.5) + 2.6, "½", "f1-tl-num", "end"))
tl.append(text(9, Yp(0.5) + 3.5, "P", "f1-tl-mu", "start"))
def band_label(seg_, t, which, label, cls):
    d = RT[seg_]; i = int(round(t / 0.025))
    c1 = d["conn"][i]; c2 = c1 + d["f1"][i]; c3 = c2 + d["f2"][i]
    lo, hi = {"conn": (0, c1), "f1": (c1, c2), "f2": (c2, c3), "f0": (c3, 1)}[which]
    x = X(uR(t)) if seg_ == "r" else X(uQ(t))
    return text(x, Yp((lo + hi) / 2) + 2.4, label, cls)
tl.append(band_label("r", 3.55, "conn", sub("P", "conn"), "f1-bt f1-bt-c"))
tl.append(band_label("r", 0.6, "f1", sub("P", "1ff"), "f1-bt f1-bt-f"))
tl.append(band_label("q", 0.16, "conn", sub("P", "conn"), "f1-bt f1-bt-c"))
tl.append(band_label("q", 1.72, "f1", sub("P", "1ff"), "f1-bt f1-bt-f"))
tl.append(band_label("q", 1.72, "f2", sub("P", "2ff"), "f1-bt f1-bt-s"))
tl.append(band_label("q", 1.72, "f0", sub("P", "0ff"), "f1-bt f1-bt-s"))
gap0, gap1 = (U_R1 + U_Q0) / 2 - 0.012, (U_R1 + U_Q0) / 2 + 0.012
for u0, u1 in ((0, gap0), (gap1, 1)):
    tl.append(f'<path class="f1-ax-dim" d="M{f(X(u0))} {f(AY)} L{f(X(u1))} {f(AY)}"/>')
    tl.append(f'<path class="f1-ax" d="M{f(X(u0))} {f(AY)} L{f(X(u1))} {f(AY)}" clip-path="url(#f1-elapsed)"/>')
for dx in (-2.2, 2.2):
    xm = (X(gap0) + X(gap1)) / 2 + dx
    tl.append(f'<path class="f1-ax-brk" d="M{f(xm - 1.8)} {f(AY + 3.6)} L{f(xm + 1.8)} {f(AY - 3.6)}"/>')
for t in range(0, 5):
    h = 3.2 if t in (0, 4) else 1.8
    tl.append(f'<path class="f1-tick" d="M{f(X(uR(t)))} {f(AY - h)} L{f(X(uR(t)))} {f(AY + h)}"/>')
for t in (0, 0.5, 1, 1.5, 2):
    h = 3.2 if t in (0, 2) else 1.8
    tl.append(f'<path class="f1-tick" d="M{f(X(uQ(t)))} {f(AY - h)} L{f(X(uQ(t)))} {f(AY + h)}"/>')
for u, lab, up in ((sum(INS) / 2, "+ Q Q̄", False), (sum(WD) / 2, "− Q Q̄", True)):
    x = X(u)
    tl.append(f'<path class="f1-hand" d="M{f(x - 2.6)} {f(AY - 6.4)} L{f(x + 2.6)} {f(AY - 6.4)} L{f(x)} {f(AY - 2.4)} Z"/>' if not up else
              f'<path class="f1-hand" d="M{f(x - 2.6)} {f(AY - 2.4)} L{f(x + 2.6)} {f(AY - 2.4)} L{f(x)} {f(AY - 6.4)} Z"/>')
    tl.append(text(x, PB - 5, lab, "f1-handt"))
tl.append(text(X(uR(0)), AY + 11, "0", "f1-tl-num") + text(X(U_R1), AY + 11, "4", "f1-tl-num")
          + text(X(U_Q0), AY + 11, "0", "f1-tl-num") + text(X(U_Q1), AY + 11, "2", "f1-tl-num")
          + text(AX1 + 12, AY + 3.5, "t", "f1-tl-mu", "end"))
tl.append(text(X((U_R0 + U_R1) / 2), AY + 11,
               '<tspan class="f1-cap">FORMATION RAMP</tspan><tspan class="f1-cap-m" dx="5">m(t) = 0.5 + 3.5t/4</tspan>', "f1-capw"))
tl.append(text(X((U_Q0 + U_Q1) / 2), AY + 11,
               '<tspan class="f1-cap">BREAKING QUENCH</tspan><tspan class="f1-cap-m" dx="5">m: 4 → 0.5</tspan>', "f1-capw"))
px = X(U_STATIC); pmu = mu_of(U_STATIC)
tl.append(f'<g id="f1-ph" class="f1-ph"><path id="f1-ph-l" class="f1-ph-line" d="M{f(px)} 235 L{f(px)} {f(AY)}"/>'
          f'<circle id="f1-ph-d" class="f1-ph-dot" cx="{f(px)}" cy="{f(Ymu(pmu))}" r="2.3"/>'
          f'<circle id="f1-ph-p" class="f1-ph-pdot" cx="{f(px)}" cy="{f(Yp(D0["conn"]) if D0 else PB)}" r="2.4" style="opacity:{1 if D0 else 0}"/>'
          f'<circle id="f1-ph-halo" class="f1-ph-halo" cx="{f(px)}" cy="{f(AY)}" r="7"/>'
          f'<circle id="f1-ph-ring" class="f1-ph-ring" cx="{f(px)}" cy="{f(AY)}" r="4.4"/>'
          f'<circle id="f1-ph-c" class="f1-ph-core" cx="{f(px)}" cy="{f(AY)}" r="1.6"/></g>')
tl.append(f'<g id="f1-slider" class="f1-ctrl" tabindex="0" role="slider" aria-label="Time t: drag to scrub the evolution" '
          f'aria-valuemin="0" aria-valuemax="100" aria-valuenow="{round(U_STATIC * 100)}">'
          f'<title>Drag to move through time</title>'
          f'<rect id="f1-hit" class="f1-hit" x="{f(AX0 - 8)}" y="233" width="{f(AW + 16)}" height="{f(AY + 8 - 233)}"/></g>')
tl.append(f'<g id="f1-play" class="f1-ctrl f1-play" tabindex="0" role="button" aria-label="Pause the time evolution">'
          f'<circle class="f1-play-ring" cx="14" cy="{f(AY)}" r="8.5"/>'
          f'<g class="f1-ic-pause"><rect x="10.6" y="{f(AY - 3.6)}" width="2.2" height="7.2" rx=".5"/><rect x="15.2" y="{f(AY - 3.6)}" width="2.2" height="7.2" rx=".5"/></g>'
          f'<path class="f1-ic-play" d="M11.6 {f(AY - 4.2)} L18.2 {f(AY)} L11.6 {f(AY + 4.2)} Z"/></g>')
tl.append('</g>')
svg.extend(tl)

desc = ("Interactive figure on the C2 honeycomb patch in the colour-singlet notation of Halimeh et al. (PRX Quantum 5, 030358, 2024): "
        "each vertex is a triangle of sites with the matter site in the centre and one rishon site per link end at the corners; a lobe "
        "joining two sites of a vertex is an SU(2) colour singlet, a halo marks a doubly occupied site. A draggable time axis runs through "
        "a full cycle. In the vacuum a glueball cluster, six singlets around one hexagon swapped between two coverings by the plaquette "
        "term Tr U_p, sits next to two matter clusters, quark-antiquark singlet pairs across one link. Static sources Q and Q-bar are "
        "then placed by hand at the two tips; they pin the ring into matter clusters. During the formation ramp m(t) = 0.5 + 3.5 t/4 the "
        "off-corridor clusters annihilate and the corridor clusters join, pair by pair, into one flux tube: a chain of rishon singlets "
        "from Q to Q-bar. After the breaking quench m: 4 to 0.5 a vacuum pair cuts the chain, the pieces shrink onto the screened sources, "
        "the matter clusters return; once the sources are removed the glueball cluster resonates again. Under the axis, stacked bands give "
        "the exact source-class probabilities of the thesis protocols at R = 4; an inset shows the static connection probability for "
        "plaquette couplings kappa = 0, 2, 4.")
svg_markup = (f'<svg class="f1" viewBox="0 0 {W} {H}" role="group" aria-labelledby="f1-title" aria-describedby="f1-desc">'
              '<title id="f1-title">Fig. 1 — colour-singlet clusters, flux-tube formation and string breaking on the C2 patch</title>'
              f'<desc id="f1-desc">{desc}</desc>' + "".join(svg) + '</svg>')
def layer(cls, body, attrs=""):
    return f'<svg class="f1-layer {cls}" viewBox="0 0 {W} {H}" aria-hidden="true" focusable="false"{attrs}>' + body + '</svg>'
stage_markup = ('<div class="f1-stage">' + layer("f1-under", "".join(under))
                + layer("f1-tglow", tube_markup, f' id="f1-tube" style="opacity:{0.15 + 0.85 * D0c:.3f}"')
                + svg_markup + layer("f1-ann", "".join(ann)) + '</div>')

LG_TRI = "M3.2 2.4 L18.8 2.4 L11 15.9 Z"
extra = f'''<ul class="f1-legend">
  <li><svg viewBox="0 0 22 19" aria-hidden="true" class="f1-lg-v"><path d="{LG_TRI}" class="f1-lg-tri"/><circle cx="11" cy="7.4" r="2.1" class="f1-lg-s"/><circle cx="3.2" cy="2.4" r="2.1" class="f1-lg-s"/><circle cx="18.8" cy="2.4" r="2.1" class="f1-lg-s f1-lg-s1"/><circle cx="11" cy="15.9" r="2.1" class="f1-lg-s f1-lg-s1"/></svg>vertex · matter + rishon sites</li>
  <li><svg viewBox="0 0 26 12" aria-hidden="true"><path d="M5 6 H21" class="f1-lg-lobe"/><path d="M5 6 H21" class="f1-lg-lobec"/><circle cx="5" cy="6" r="2.1" class="f1-lg-s f1-lg-s1"/><circle cx="21" cy="6" r="2.1" class="f1-lg-s f1-lg-s1"/></svg>SU(2) singlet</li>
  <li><svg viewBox="0 0 30 12" aria-hidden="true"><path d="M3 6 H9" class="f1-lg-lobe"/><path d="M21 6 H27" class="f1-lg-lobe"/><path d="M9 6 H21" class="f1-lg-open"/><circle cx="3" cy="6" r="1.9" class="f1-lg-s f1-lg-s1"/><circle cx="9" cy="6" r="1.9" class="f1-lg-s f1-lg-s1"/><circle cx="21" cy="6" r="1.9" class="f1-lg-s f1-lg-s1"/><circle cx="27" cy="6" r="1.9" class="f1-lg-s f1-lg-s1"/></svg>matter cluster</li>
  <li><svg viewBox="0 0 22 22" aria-hidden="true" class="f1-lg-hex"><path d="M11 2.2 L18.6 6.6 L18.6 15.4 L11 19.8 L3.4 15.4 L3.4 6.6 Z" class="f1-lg-closed"/><path d="M11 2.2 L18.6 6.6 L18.6 15.4 L11 19.8 L3.4 15.4 L3.4 6.6 Z" class="f1-lg-closedc"/></svg>glueball cluster</li>
  <li><svg viewBox="0 0 26 12" aria-hidden="true"><path d="M2 6 H24" class="f1-lg-tube"/></svg><span>flux tube · <math><mi>Q</mi><mo>…</mo><mover><mi>Q</mi><mo>‾</mo></mover></math></span></li>
</ul>
<div class="f1-ham" aria-label="Hamiltonian of the honeycomb model, Eq. (II.8) of the thesis">
  <span class="f1-ham-h"><math><mi>H</mi><mo>=</mo></math></span>
  <span class="f1-term f1-term-m"><math><mo form="prefix">−</mo><msub><mi>t</mi><mi mathvariant="normal">h</mi></msub><msub><mo largeop="false" movablelimits="true">∑</mo><mi>ℓ</mi></msub><mo stretchy="false">(</mo><msubsup><mi>ψ</mi><mi mathvariant="normal">A</mi><mo>†</mo></msubsup><msub><mi>U</mi><mi>ℓ</mi></msub><msub><mi>ψ</mi><mi mathvariant="normal">B</mi></msub><mo>+</mo><mtext>h.c.</mtext><mo stretchy="false">)</mo></math><small>hopping</small></span>
  <span class="f1-term f1-term-m"><math><mo>+</mo><mi>m</mi><msub><mo largeop="false">∑</mo><mi>v</mi></msub><msub><mi>η</mi><mi>v</mi></msub><msub><mi>n</mi><mi>v</mi></msub></math><small>mass</small></span>
  <span class="f1-term f1-term-e"><math><mo>+</mo><mfrac><msup><mi>g</mi><mn>2</mn></msup><mn>2</mn></mfrac><msub><mo largeop="false">∑</mo><mi>ℓ</mi></msub><msubsup><mi>E</mi><mi>ℓ</mi><mn>2</mn></msubsup></math><small>electric</small></span>
  <span class="f1-term f1-term-b"><math><mo>−</mo><mi>κ</mi><msub><mo largeop="false">∑</mo><mi>p</mi></msub><mo stretchy="false">(</mo><mi>Tr</mi><mspace width="0.18em"></mspace><msub><mi>U</mi><mi>p</mi></msub><mo>+</mo><mtext>h.c.</mtext><mo stretchy="false">)</mo></math><small>magnetic</small></span>
  <span class="f1-term f1-term-c"><math><mo>+</mo><mo>⋯</mo></math><small>constraints</small></span>
</div>
<p class="f1-note f1-caption"><b>Bands</b> under the time axis: exact source classes of the thesis protocols (<i>g</i>² = 2, <i>κ</i> = 0, <i>R</i> = 4); turquoise connected, ivory flux-free endpoints. <b>Inset:</b> static <i>P</i><sub>conn</sub>(<i>m</i>) at <i>R</i> = 4 for <i>κ</i> = 0, 2, 4; open markers mark the plaquette (loop) branch; <i>κ</i> ≤ 2 leaves the <i>m</i> = 4 string intact (<i>κ</i>* ≈ 3.03), and <i>µ</i>* = 9/8 separates string from one-pair states. Each link carries two rishons, <i>n</i><sub>L</sub> + <i>n</i><sub>R</sub> = 2. Singlet notation after Halimeh <i>et al.</i>, PRX Quantum <b>5</b>, 030358 (2024).</p>'''

# ---------------- runtime ----------------
CFG = dict(AX0=AX0, AW=AW, UR0=U_R0, UR1=U_R1, UQ0=U_Q0, UQ1=U_Q1, INS1=INS[1], WD0=WD[0], MY=MU_Y0, MK=MU_K, PT=PT, PB=PB,
           AY=AY, CYCLE=CYCLE, USTATIC=U_STATIC, IX0=IX0, IX1=IX1, IY0=IY0, IY1=IY1,
           SIG=SIG, LEV=LEV, GRID=GRID, GX0=GX0, GY0=GY0, GNX=GNX, GNY=GNY, STEP=OL_STEP,
           BG=[[round(a[0], 3), round(a[1], 3), round(m[0], 3), round(m[1], 3)] for _, a, m in BS_LIST])
RTJS = {s: {k: RT[s][k] for k in ("conn", "f1", "f2", "tau")} for s in ("r", "q")}
DATA = [t.data() for t in tracks]
JS = r"""/* Fig. 1 runtime: generated by tools/fig1.py — colour-singlet clusters (matter and glueball), hand-inserted sources,
   flux-tube formation and string breaking; bands and readout: exact real-time data of the thesis (Ch. IV). */
(() => {
  const svg = document.querySelector('svg.f1');
  if (!svg) return;
  const C = __CFG__;
  const RAW = __DATA__;
  const RT = __RT__;
  const $ = (id) => document.getElementById(id);
  const ease = (x) => 0.5 - 0.5 * Math.cos(Math.PI * x);
  // Allocation-free sampling: each track keeps its value buffer, the last applied value and its current segment.
  const tracks = [];
  for (const t of RAW) {
    if (t.t === 'bi' || t.t === 'bw') {
      const n = t.k[0].length - 1;
      tracks.push({ el: null, type: t.t, s: t.s, k: t.k, e: t.e !== 0, v: new Float64Array(n), pv: new Float64Array(n).fill(NaN), seg: 0 });
      continue;
    }
    const el = $(t.id);
    if (!el) continue;
    const n = t.k[0].length - 1;
    const tr = { el, type: t.t, k: t.k, e: t.e !== 0, v: new Float64Array(n), pv: new Float64Array(n).fill(NaN), seg: 0, hidden: false };
    if (t.t === 'ln') tr.paths = Array.from(el.querySelectorAll('path'));
    if (t.t === 'occ') { tr.fill = el.querySelector('.f1-sf'); tr.halo = el.querySelector('.f1-sh'); }
    if (t.t === 'burst') tr.circles = el.tagName.toLowerCase() === 'g' ? Array.from(el.querySelectorAll('circle')) : [el];
    tracks.push(tr);
  }
  const sample = (t, u) => {
    const k = t.k, v = t.v, n = v.length, last = k.length - 1;
    if (u <= k[0][0]) { for (let j = 0; j < n; j++) v[j] = k[0][j + 1]; return; }
    let i = t.seg;
    if (i >= last || u < k[i][0]) i = 0;
    while (i < last && u > k[i + 1][0]) i++;
    t.seg = i;
    if (i >= last) { for (let j = 0; j < n; j++) v[j] = k[last][j + 1]; return; }
    const a = k[i], b = k[i + 1], span = b[0] - a[0];
    let p = span > 0 ? (u - a[0]) / span : 1;
    if (t.e) p = ease(p);
    for (let j = 0; j < n; j++) v[j] = a[j + 1] + (b[j + 1] - a[j + 1]) * p;
  };
  const changed = (t, eps) => {
    const v = t.v, pv = t.pv; let c = false;
    for (let j = 0; j < v.length; j++) if (!(Math.abs(v[j] - pv[j]) <= eps)) c = true;
    if (c) pv.set(v);
    return c;
  };
  const show = (t, on) => { if (on === t.hidden) { t.el.style.visibility = on ? '' : 'hidden'; t.hidden = !on; } };
  const apply = (t) => {
    const v = t.v;
    switch (t.type) {
      case 'op':
        if (!changed(t, 0.002)) return;
        if (v[0] < 0.003) show(t, false); else { show(t, true); t.el.style.opacity = v[0].toFixed(3); }
        break;
      case 'occ': {
        if (!changed(t, 0.002)) return;
        const o = Math.max(0, Math.min(2, v[0]));
        t.fill.style.opacity = (o <= 1 ? o : 1 - 0.45 * (o - 1)).toFixed(3);
        t.halo.style.opacity = Math.max(0, o - 1).toFixed(3);
        break;
      }
      case 'ln': {
        if (!changed(t, 0.01)) return;
        const d = 'M' + v[0].toFixed(2) + ' ' + v[1].toFixed(2) + 'L' + v[2].toFixed(2) + ' ' + v[3].toFixed(2);
        for (const p of t.paths) p.setAttribute('d', d);
        break;
      }
      case 'tr':
        if (!changed(t, 0.01)) return;
        t.el.setAttribute('transform', 'translate(' + v[0].toFixed(2) + ' ' + v[1].toFixed(2) + ')');
        break;
      case 'burst':
        if (!changed(t, 0.003)) return;
        if (v[1] < 0.003) show(t, false);
        else { show(t, true); const r = v[0].toFixed(2); for (const c of t.circles) c.setAttribute('r', r); t.el.style.opacity = v[1].toFixed(3); }
        break;
      case 'bi':
        if (!changed(t, 1e-4)) return;
        bp[t.s] = v[0]; bq[t.s] = v[1]; olDirty = true;
        break;
      case 'bw':
        if (!changed(t, 1e-4)) return;
        bw[t.s] = v[0]; olDirty = true;
        break;
    }
  };

  // Colour-singlet outlines (mirrors ol_loops / ol_d in tools/fig1.py): a Gaussian convolution field along the visible
  // half-segments, sampled on a fixed lattice, contoured by marching squares; recomputed only on frames where a
  // half-segment moves or fades.
  const BG = C.BG, NBS = BG.length;
  const bp = new Float64Array(NBS), bq = new Float64Array(NBS), bw = new Float64Array(NBS);
  const SIG = C.SIG, LEV = C.LEV, GR = C.GRID, GX0 = C.GX0, GY0 = C.GY0, GNX = C.GNX, GNY = C.GNY;
  const REACH = 3 * SIG, R2 = REACH * REACH, S2 = SIG * SIG, SQ = (Math.sqrt(Math.PI) * SIG) / 2, STEP2 = C.STEP * C.STEP;
  const FLD = new Float32Array(GNX * GNY);
  const NE = 2 * GNX * GNY;
  const PX = new Float32Array(NE), PY = new Float32Array(NE), NA = new Int32Array(NE), NBR = new Int32Array(NE);
  const EG = new Uint32Array(NE), VIS = new Uint32Array(NE);
  const touched = [], act = [], lx = [], ly = [];
  // each half-segment keeps its own (unweighted) field patch; it is recomputed only when the segment moves
  const CW = 64, PATCH = BG.map(() => ({ arr: new Float32Array(CW * CW), ax: NaN, ay: NaN, bx: NaN, by: NaN, i0: 0, j0: 0, ni: 0, nj: 0 }));
  const patch = (s, ax, ay, bx, by) => {
    const c = PATCH[s];
    if (c.ax === ax && c.ay === ay && c.bx === bx && c.by === by) return c;
    c.ax = ax; c.ay = ay; c.bx = bx; c.by = by;
    const L = Math.hypot(bx - ax, by - ay), ux = (bx - ax) / L, uy = (by - ay) / L;
    c.i0 = Math.max(0, Math.floor((Math.min(ax, bx) - REACH - GX0) / GR)); const i1 = Math.min(GNX - 1, Math.ceil((Math.max(ax, bx) + REACH - GX0) / GR));
    c.j0 = Math.max(0, Math.floor((Math.min(ay, by) - REACH - GY0) / GR)); const j1 = Math.min(GNY - 1, Math.ceil((Math.max(ay, by) + REACH - GY0) / GR));
    c.ni = Math.min(CW, i1 - c.i0 + 1); c.nj = Math.min(CW, j1 - c.j0 + 1);
    const arr = c.arr;
    for (let jj = 0; jj < c.nj; jj++) {
      const dy = GY0 + (c.j0 + jj) * GR - ay, row = jj * CW;
      for (let ii = 0; ii < c.ni; ii++) {
        const dx = GX0 + (c.i0 + ii) * GR - ax, t = dx * ux + dy * uy, h = dx * uy - dy * ux;
        arr[row + ii] = h * h > R2 || t < -REACH || t > L + REACH ? 0 : gau((h * h) / S2) * (erf((L - t) / SIG) + erf(t / SIG));
      }
    }
    return c;
  };
  let gen = 0, olDirty = true;
  const olG = $('f1-ol-g'), olP = $('f1-ol-p');
  // erf and the Gaussian are read from tables (linear interpolation, error < 1e-5): the field costs a few lookups per sample
  const TN = 512, ERF_X = 3.5, ERF_T = new Float32Array(Math.ceil(ERF_X * TN) + 2), GAU_T = new Float32Array(9 * TN + 2);
  for (let k = 0; k < ERF_T.length; k++) {
    const x = k / TN, t = 1 / (1 + 0.3275911 * x);
    ERF_T[k] = 1 - ((((1.061405429 * t - 1.453152027) * t + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x);
  }
  for (let k = 0; k < GAU_T.length; k++) GAU_T[k] = Math.exp(-k / TN);
  const erf = (x) => {
    const a = (x < 0 ? -x : x) * TN;
    if (a >= ERF_X * TN) return x < 0 ? -1 : 1;
    const k = a | 0, f = a - k, y = ERF_T[k] + (ERF_T[k + 1] - ERF_T[k]) * f;
    return x < 0 ? -y : y;
  };
  const gau = (z) => { const a = z * TN, k = a | 0, f = a - k; return GAU_T[k] + (GAU_T[k + 1] - GAU_T[k]) * f; };
  const ept = (e) => {
    if (EG[e] === gen) return;
    EG[e] = gen; NA[e] = -1; NBR[e] = -1; touched.push(e);
    const ij = e >> 1, i = ij % GNX, j = (ij - i) / GNX;
    if ((e & 1) === 0) { const a = FLD[ij], b = FLD[ij + 1]; PX[e] = GX0 + (i + (LEV - a) / (b - a)) * GR; PY[e] = GY0 + j * GR; }
    else { const a = FLD[ij], b = FLD[ij + GNX]; PX[e] = GX0 + i * GR; PY[e] = GY0 + (j + (LEV - a) / (b - a)) * GR; }
  };
  const lk = (a, b) => {
    ept(a); ept(b);
    if (NA[a] < 0) NA[a] = b; else NBR[a] = b;
    if (NA[b] < 0) NA[b] = a; else NBR[b] = a;
  };
  const loopPath = () => {
    const n0 = lx.length;
    let area = 0;
    for (let k = 0; k < n0; k++) { const k1 = (k + 1) % n0; area += lx[k] * ly[k1] - lx[k1] * ly[k]; }
    if (area < 0) { lx.reverse(); ly.reverse(); }
    let k0 = 0, best = Infinity;
    for (let k = 0; k < n0; k++) { const s = 0.8 * lx[k] + 0.6 * ly[k]; if (s < best) { best = s; k0 = k; } }
    const xs = [lx[k0]], ys = [ly[k0]];
    for (let m = 1; m < n0; m++) {
      const k = (k0 + m) % n0, dx = lx[k] - xs[xs.length - 1], dy = ly[k] - ys[ys.length - 1];
      if (dx * dx + dy * dy >= STEP2) { xs.push(lx[k]); ys.push(ly[k]); }
    }
    const n = xs.length;
    if (n < 3) return '';
    const r1 = (x) => Math.round(x * 10) / 10;
    let d = 'M' + r1((xs[n - 1] + xs[0]) / 2) + ' ' + r1((ys[n - 1] + ys[0]) / 2);
    for (let k = 0; k < n; k++) {
      const k1 = k + 1 < n ? k + 1 : 0;
      d += 'Q' + r1(xs[k]) + ' ' + r1(ys[k]) + ' ' + r1((xs[k] + xs[k1]) / 2) + ' ' + r1((ys[k] + ys[k1]) / 2);
    }
    return d + 'Z';
  };
  const drawOutlines = () => {
    act.length = 0;
    let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
    for (let s = 0; s < NBS; s++) {
      const w = bw[s], p = bp[s], q = bq[s];
      if (w < 0.004 || q - p < 1e-4) continue;
      const g = BG[s];
      const ax = g[0] + (g[2] - g[0]) * p, ay = g[1] + (g[3] - g[1]) * p, bx = g[0] + (g[2] - g[0]) * q, by = g[1] + (g[3] - g[1]) * q;
      act.push(ax, ay, bx, by, w, s);
      x0 = Math.min(x0, ax, bx); x1 = Math.max(x1, ax, bx); y0 = Math.min(y0, ay, by); y1 = Math.max(y1, ay, by);
    }
    let d = '';
    if (act.length) {
      gen += 1; touched.length = 0;
      const i0 = Math.max(0, Math.floor((x0 - REACH - GX0) / GR)), i1 = Math.min(GNX - 1, Math.ceil((x1 + REACH - GX0) / GR));
      const j0 = Math.max(0, Math.floor((y0 - REACH - GY0) / GR)), j1 = Math.min(GNY - 1, Math.ceil((y1 + REACH - GY0) / GR));
      for (let j = j0; j <= j1; j++) FLD.fill(0, j * GNX + i0, j * GNX + i1 + 1);
      for (let k = 0; k < act.length; k += 6) {
        const c = patch(act[k + 5], act[k], act[k + 1], act[k + 2], act[k + 3]), w = act[k + 4] * SQ, arr = c.arr;
        for (let jj = 0; jj < c.nj; jj++) {
          const row = (c.j0 + jj) * GNX + c.i0, prow = jj * CW;
          for (let ii = 0; ii < c.ni; ii++) FLD[row + ii] += w * arr[prow + ii];
        }
      }
      for (let j = j0; j < j1; j++) {
        for (let i = i0; i < i1; i++) {
          const o = j * GNX + i, v0 = FLD[o], v1 = FLD[o + 1], v2 = FLD[o + GNX + 1], v3 = FLD[o + GNX];
          const c = (v0 > LEV ? 1 : 0) | (v1 > LEV ? 2 : 0) | (v2 > LEV ? 4 : 0) | (v3 > LEV ? 8 : 0);
          if (c === 0 || c === 15) continue;
          const e0 = 2 * o, e1 = 2 * (o + 1) + 1, e2 = 2 * (o + GNX), e3 = 2 * o + 1;
          switch (c) {
            case 1: case 14: lk(e3, e0); break;
            case 2: case 13: lk(e0, e1); break;
            case 3: case 12: lk(e3, e1); break;
            case 4: case 11: lk(e1, e2); break;
            case 6: case 9: lk(e0, e2); break;
            case 7: case 8: lk(e3, e2); break;
            case 5: if ((v0 + v1 + v2 + v3) / 4 > LEV) { lk(e0, e1); lk(e2, e3); } else { lk(e3, e0); lk(e1, e2); } break;
            case 10: if ((v0 + v1 + v2 + v3) / 4 > LEV) { lk(e3, e0); lk(e1, e2); } else { lk(e0, e1); lk(e2, e3); } break;
          }
        }
      }
      for (const e of touched) {
        if (VIS[e] === gen) continue;
        lx.length = 0; ly.length = 0;
        let prev = -1, cur = e;
        while (cur >= 0 && VIS[cur] !== gen) {
          VIS[cur] = gen; lx.push(PX[cur]); ly.push(PY[cur]);
          const nx = NA[cur] !== prev ? NA[cur] : NBR[cur];
          prev = cur; cur = nx;
        }
        d += loopPath();
      }
    }
    olG.setAttribute('d', d); olP.setAttribute('d', d);
  };
  const setText = (node, s) => { if (node.textContent !== s) node.textContent = s; };
  const setAttr = (node, a, s) => { if (node.getAttribute(a) !== s) node.setAttribute(a, s); };
  const dataAt = (u) => {
    if (u < C.INS1 || u > C.WD0) return null;
    let d, t;
    if (u <= C.UR1) { d = RT.r; t = Math.max(0, (4 * (u - C.UR0)) / (C.UR1 - C.UR0)); }
    else { d = RT.q; t = u < C.UQ0 ? 0 : Math.min(2, (2 * (u - C.UQ0)) / (C.UQ1 - C.UQ0)); }
    const n = d.conn.length, x = Math.min(t / 0.025, n - 1.0001), i = Math.floor(x), w = x - i;
    const g = (a) => a[i] * (1 - w) + a[i + 1] * w;
    return { conn: g(d.conn), ff: g(d.f1) + g(d.f2), tau: g(d.tau) };
  };
  const muOf = (u) => (u < C.UR0 ? 0.5 : u <= C.UR1 ? 0.5 + 3.5 * ((u - C.UR0) / (C.UR1 - C.UR0)) : u < C.UQ0 ? 4 : 0.5);
  const phase = (u) => (u < C.INS1 ? 'vacuum: glueball cluster and matter clusters' : u < C.UR0 ? 'sources inserted' : u <= C.UR1 ? 'formation ramp'
    : u < C.UQ0 ? 'm = 4 ground state, flux tube' : u <= C.UQ1 ? 'breaking quench' : u < C.WD0 ? 'after the quench' : 'vacuum, sources removed');
  const tOf = (u) => (u < C.INS1 || u > C.WD0 ? null : u <= C.UR1 ? Math.max(0, (4 * (u - C.UR0)) / (C.UR1 - C.UR0))
    : u < C.UQ0 ? 'GS' : Math.min(2, (2 * (u - C.UQ0)) / (C.UQ1 - C.UQ0)));
  const ixm = (m) => C.IX0 + ((m - 0.5) / 3.5) * (C.IX1 - C.IX0);
  const el = {
    t: $('f1-ro-t'), mu: $('f1-ro-mu'), pc: $('f1-ro-pc'), pf: $('f1-ro-pf'), tau: $('f1-ro-tau'),
    clip: $('f1-elapsed-r'), phl: $('f1-ph-l'), phd: $('f1-ph-d'), php: $('f1-ph-p'),
    ring: $('f1-ph-ring'), core: $('f1-ph-c'), halo: $('f1-ph-halo'), tube: $('f1-tube'),
    kmk: $('f1-kin-mk'), slider: $('f1-slider'), hit: $('f1-hit'), play: $('f1-play'),
  };
  let u = 0, shownU = -1;
  const render = (uu) => {
    u = ((uu % 1) + 1) % 1;
    for (const t of tracks) { sample(t, u); apply(t); }
    if (olDirty) { olDirty = false; drawOutlines(); }
    const mu = muOf(u), t = tOf(u), x = C.AX0 + u * C.AW, d = dataAt(u);
    setText(el.t, t === null ? 'vac' : typeof t === 'string' ? t : t.toFixed(2));
    setText(el.mu, mu.toFixed(2));
    setText(el.pc, d ? d.conn.toFixed(3) : '—');
    setText(el.pf, d ? d.ff.toFixed(3) : '—');
    setText(el.tau, d ? d.tau.toFixed(3) : '—');
    el.clip.setAttribute('width', (x - C.AX0 + 3).toFixed(2));
    el.phl.setAttribute('d', 'M' + x.toFixed(2) + ' 235 L' + x.toFixed(2) + ' ' + C.AY);
    el.phd.setAttribute('cx', x.toFixed(2)); el.phd.setAttribute('cy', (C.MY - C.MK * mu).toFixed(2));
    el.php.setAttribute('cx', x.toFixed(2));
    el.php.setAttribute('cy', (d ? C.PB - (C.PB - C.PT) * d.conn : C.PB).toFixed(2));
    el.php.style.opacity = d ? 1 : 0;
    for (const c of [el.ring, el.core, el.halo]) c.setAttribute('cx', x.toFixed(2));
    const km = ixm(mu).toFixed(2);
    setAttr(el.kmk, 'd', 'M' + km + ' ' + (C.IY0 - 1) + ' L' + km + ' ' + C.IY1);
    const to = (0.15 + 0.85 * (d ? d.conn : 0)).toFixed(3);
    if (el.tube.style.opacity !== to) el.tube.style.opacity = to;
    if (Math.abs(u - shownU) > 0.004) {
      shownU = u;
      el.slider.setAttribute('aria-valuenow', String(Math.round(u * 100)));
      el.slider.setAttribute('aria-valuetext', phase(u) + (typeof t === 'number' ? ', t = ' + t.toFixed(2) : '') +
        ', mu = ' + mu.toFixed(2) + (d ? ', connection probability ' + d.conn.toFixed(3) : ''));
    }
  };

  const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let playing = !reduce, visible = true, dragging = false, last = null;
  const setPlaying = (p) => {
    playing = p; last = null;
    svg.classList.toggle('is-paused', !p);
    el.play.setAttribute('aria-label', p ? 'Pause the time evolution' : 'Play the time evolution');
  };
  const frame = (ts) => {
    if (playing && visible && !dragging) {
      if (last !== null) render(u + Math.min(0.1, (ts - last) / 1000) / C.CYCLE);
      last = ts;
    } else last = null;
    requestAnimationFrame(frame);
  };
  render(reduce ? C.USTATIC : 0);
  setPlaying(!reduce);
  svg.f1Seek = (x) => { setPlaying(false); render(x); };
  requestAnimationFrame(frame);

  if ('IntersectionObserver' in window) {
    new IntersectionObserver((es) => { for (const e of es) visible = e.isIntersecting; }, { threshold: 0.05 }).observe(svg);
  }
  const uFrom = (e) => {
    const m = svg.getScreenCTM(); if (!m) return u;
    const pt = svg.createSVGPoint(); pt.x = e.clientX; pt.y = e.clientY;
    const p = pt.matrixTransform(m.inverse());
    return Math.min(0.9999, Math.max(0, (p.x - C.AX0) / C.AW));
  };
  el.hit.addEventListener('pointerdown', (e) => {
    if (e.button !== undefined && e.button > 0) return;
    dragging = true; svg.classList.add('is-dragging');
    try { el.hit.setPointerCapture(e.pointerId); } catch (_) {}
    setPlaying(false); render(uFrom(e)); e.preventDefault();
  });
  el.hit.addEventListener('pointermove', (e) => { if (dragging) render(uFrom(e)); });
  const end = () => { dragging = false; svg.classList.remove('is-dragging'); };
  el.hit.addEventListener('pointerup', end);
  el.hit.addEventListener('pointercancel', end);
  el.hit.addEventListener('lostpointercapture', end);
  const toggle = () => setPlaying(!playing);
  el.play.addEventListener('click', toggle);
  el.play.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(); } });
  el.slider.addEventListener('keydown', (e) => {
    const step = { ArrowRight: 0.01, ArrowUp: 0.01, ArrowLeft: -0.01, ArrowDown: -0.01, PageUp: 0.1, PageDown: -0.1 }[e.key];
    if (step !== undefined) { e.preventDefault(); setPlaying(false); render(Math.min(0.9999, Math.max(0, u + step))); }
    else if (e.key === 'Home') { e.preventDefault(); setPlaying(false); render(0); }
    else if (e.key === 'End') { e.preventDefault(); setPlaying(false); render(0.9999); }
    else if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); toggle(); }
  });
})();
"""

def splice_index(svg_markup, extra):
    p = os.path.join(SITE_DIR, "index.html")
    html = open(p, encoding="utf-8").read()
    new_fig = '<figure class="flux-c2">\n                ' + svg_markup + '\n                ' + extra.replace("\n", "\n                ") + '\n              </figure>'
    html, n = re.subn(r'<figure class="flux-c2">.*?</figure>', lambda m: new_fig, html, count=1, flags=re.S)
    assert n == 1
    if 'assets/js/fig1.js' not in html:
        html = html.replace('<script src="script.js', '<script src="assets/js/fig1.js?v=1" defer></script>\n    <script src="script.js', 1)
    if os.environ.get("FIG1_V"):         # cache-buster: set FIG1_V=<n> when fig1.js changes; otherwise kept as is
        html = re.sub(r'assets/js/fig1\.js\?v=\d+', 'assets/js/fig1.js?v=%d' % int(os.environ["FIG1_V"]), html)
    open(p, "w", encoding="utf-8").write(html)

if __name__ == "__main__":
    os.chdir(HERE)
    js = (JS.replace("__CFG__", json.dumps(CFG)).replace("__DATA__", json.dumps(DATA, separators=(",", ":")))
            .replace("__RT__", json.dumps(RTJS, separators=(",", ":"))))
    os.makedirs(os.path.join(SITE_DIR, "assets", "js"), exist_ok=True)
    open(os.path.join(SITE_DIR, "assets", "js", "fig1.js"), "w").write(js)
    splice_index(stage_markup, extra)
    print(len(svg_markup), "svg chars;", len(tracks), "tracks;", len(js), "js chars;", len(CHECKS), "frames Gauss-checked")
