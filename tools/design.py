"""Inject the managed font block (top) and design-system block (bottom) into styles.css."""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
# works from the build folder (tools/ next to Portfolio/) and from Portfolio/tools/
CSS = next(p for p in (os.path.join(HERE, "..", "styles.css"), os.path.join(HERE, "..", "Portfolio", "styles.css")) if os.path.exists(p))
FIG1 = os.path.join(HERE, "..", "gen", "fig1.css")   # optional: Fig. 1 needs no CSS keyframes any more

LATIN = "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"
LATIN_EXT = "U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF"
GREEK = "U+0370-0377,U+037A-037F,U+0384-038A,U+038C,U+038E-03A1,U+03A3-03FF"

def face(fam, file, weight, style, rng):
    return (f"@font-face {{ font-family: '{fam}'; src: url('assets/fonts/{file}') format('woff2'); "
            f"font-weight: {weight}; font-style: {style}; font-display: swap; unicode-range: {rng}; }}")

faces = []
for w, st in (("500", "normal"), ("600", "normal"), ("500", "italic")):
    faces.append(face("Cormorant Garamond", f"cormorant-garamond-latin-{w}-{st}.woff2", w, st, LATIN))
    faces.append(face("Cormorant Garamond", f"cormorant-garamond-latin-ext-{w}-{st}.woff2", w, st, LATIN_EXT))
for st in ("normal", "italic"):
    faces.append(face("Newsreader", f"newsreader-latin-wght-{st}.woff2", "200 800", st, LATIN))
    faces.append(face("Newsreader", f"newsreader-latin-ext-wght-{st}.woff2", "200 800", st, LATIN_EXT))
for w in ("400", "500"):
    faces.append(face("IBM Plex Mono", f"ibm-plex-mono-latin-{w}-normal.woff2", w, "normal", LATIN))
    faces.append(face("IBM Plex Mono", f"ibm-plex-mono-latin-ext-{w}-normal.woff2", w, "normal", LATIN_EXT))
for st in ("normal", "italic"):
    faces.append(face("STIX Two Text", f"stix-two-text-latin-400-{st}.woff2", "400", st, LATIN))
    faces.append(face("STIX Two Text", f"stix-two-text-latin-ext-400-{st}.woff2", "400", st, LATIN_EXT))
    faces.append(face("STIX Two Text", f"stix-two-text-greek-400-{st}.woff2", "400", st, GREEK))

faces.append("@font-face { font-family: 'STIX Two Math'; src: url('assets/fonts/stix-two-math-subset.woff2') format('woff2'); font-weight: 400; font-style: normal; font-display: swap; }")
FONTS = ("/* ===== FONTS (managed; self-hosted, SIL OFL — no third-party requests) ===== */\n"
         + "\n".join(faces) + "\n/* ===== END FONTS ===== */\n")

DESIGN = r"""
/* ===== DESIGN SYSTEM v4 (managed) ===== */
:root {
  --display: 'Cormorant Garamond', 'Cormorant', 'Iowan Old Style', Georgia, serif;
  --text: 'Newsreader', 'STIX Two Text', 'Iowan Old Style', Georgia, serif;
  --mono: 'IBM Plex Mono', ui-monospace, 'SFMono-Regular', Menlo, monospace;
  --math: 'STIX Two Text', 'Newsreader', 'Times New Roman', serif;
  --serif: var(--text);
  --ivory: #efe7d6;
  --gold: #e2c27e;
  --flux: #8ff0ea;
}
body { font-family: var(--text); font-optical-sizing: auto; text-rendering: optimizeLegibility; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; font-kerning: normal; }

/* display: headlines and titles */
.hero h1, .eyebrow strong, .wordmark-text, .diagram-header h3, .section-heading h2, .profile-card h3, .project h3,
.dialog-copy h2, .profile-detail h2, .explore-inner h2, .explore-card h3, .area-copy h2, .contact-dialog .contact-card h2,
.contact-card h2, .direction h2, .detail-panel h3, .footer-grid strong, .area-group h3 {
  font-family: var(--display); font-weight: 500; font-feature-settings: "kern", "liga", "dlig" 0;
}
.hero h1 em, .explore-card h3 em { font-family: var(--display); font-style: italic; font-weight: 500; }

/* instrument labels: mono, tracked uppercase */
.kicker, .diagram-eyebrow, .profile-card-index, .project-meta, .detail-panel > span, .capability-list article > span,
.contact-meta, .view-bar-current, .explore-index, .area-group-label, .map-core span, .map-node span,
.profile-card-link, .explore-link, .project-facts dt, .tags span, .site-nav a, .button, .availability {
  font-family: var(--mono); font-weight: 400; font-style: normal;
}
.kicker, .diagram-eyebrow, .profile-card-index, .project-meta, .area-group-label, .explore-index, .view-bar-current,
.map-core span, .map-node span, .project-facts dt, .contact-meta { letter-spacing: 0.14em; text-transform: uppercase; }

/* MathML: journal-grade typesetting with the self-hosted STIX Two Math subset */
math { font-family: 'STIX Two Math', math; font-size: 1.04em; }
.f1-ham math { font-size: 1.08em; }
.f1-legend math { font-size: 1.04em; }
.diagram-formula math { font-size: 1.04em; }
/* math in diagrams and formulas */
.diagram-formula, .holography-caption, .sch-text, .sch-text-soft, .sch-text-small, .sch-text-id, .sch-label,
.sch-label-small, .f1 text { font-family: var(--math); }
.sch-text-label, .sch-ring-label { font-family: var(--mono); letter-spacing: 0.16em; }

/* ---------- Fig. 1: real-time dynamics on the C2 patch (driven by assets/js/fig1.js) ---------- */
.flux-c2 { margin: 12px 0 0; container-type: inline-size; }
.f1 { display: block; width: 100%; height: auto; overflow: visible; -webkit-user-select: none; user-select: none; }
.f1 text { font-family: var(--math); }
.f1-sub { font-size: 72%; }
/* readout */
.f1-panel { fill: rgba(232, 246, 237, 0.022); stroke: rgba(220, 245, 231, 0.13); stroke-width: 0.6; }
.f1-ro-h { fill: rgba(121, 227, 225, 0.8); font-family: var(--mono) !important; font-size: 6.6px; letter-spacing: 0.18em; }
.f1-ro-hs { fill: rgba(232, 246, 237, 0.38); font-family: var(--mono) !important; font-size: 6.2px; letter-spacing: 0.14em; }
.f1-ro-k { fill: rgba(232, 246, 237, 0.74); font-size: 10.5px; font-style: italic; }
.f1-ro-v { fill: #eef6f1; font-family: var(--mono) !important; font-size: 9px; letter-spacing: 0.04em; }
.f1-ro-c { fill: rgba(232, 246, 237, 0.46); font-family: var(--mono) !important; font-size: 6.6px; letter-spacing: 0.16em; text-transform: uppercase; }
.f1-ro-b { fill: var(--flux); font-size: 10.5px; font-style: italic; }
/* lattice */
.f1-link { fill: none; stroke: rgba(170, 225, 214, 0.2); stroke-width: 1; }
.f1-link-flash { fill: none; stroke: rgba(170, 245, 236, 0.6); stroke-width: 1.3; }
.f1-lid { fill: rgba(232, 246, 237, 0.32); font-size: 9.6px; font-style: italic; }
.f1-sub-id { font-style: normal; }
.f1-vid { fill: rgba(232, 246, 237, 0.36); font-family: var(--mono) !important; font-size: 7.6px; letter-spacing: 0.04em; }
.f1-str { fill: none; stroke: var(--flux); stroke-width: 2.4; stroke-linecap: round; }
.f1-str-glow { fill: none; stroke: rgba(121, 227, 225, 0.6); stroke-width: 9; stroke-linecap: round; filter: url(#f1-glow); }
.f1-burst { fill: url(#f1-burst-g); pointer-events: none; }
.f1-qflash { fill: url(#f1-flash-g); pointer-events: none; }
.f1-r { fill: var(--flux); }
.f1-r-vac { fill-opacity: 0.42; }
.f1-site { fill: #07100e; stroke: rgba(236, 232, 220, 0.78); stroke-width: 1; }
.f1-q { fill: var(--ivory); }
.f1-q-static { fill-opacity: 0.5; }
.f1-src { fill: none; stroke: rgba(239, 231, 214, 0.72); stroke-width: 0.9; stroke-dasharray: 2.2 2.3; }
.f1-srcl { fill: #f4eddd; font-size: 15px; font-style: italic; }
.f1-srcq { fill: rgba(239, 231, 214, 0.62); font-size: 10px; font-style: italic; }
.f1-ch { fill: #fbf6ea; font-size: 13px; font-style: italic; }
/* closed loop: gauge sector */
.f1-loop-fill { fill: rgba(226, 194, 126, 0.045); }
.f1-loop-ring { fill: none; stroke: var(--gold); stroke-width: 2.1; stroke-linejoin: round; stroke-linecap: round; }
.f1-loop-glow { fill: none; stroke: rgba(226, 194, 126, 0.5); stroke-width: 8.5; stroke-linejoin: round; filter: url(#f1-glow); }
.f1-loop-glint { fill: none; stroke: #fff4d8; stroke-width: 2.6; stroke-linecap: round; stroke-dasharray: 0.07 0.93; }
.f1-plaq-t { fill: var(--gold); font-size: 13.5px; font-style: italic; }
.f1-plaq-c { fill: rgba(226, 194, 126, 0.72); font-family: var(--mono) !important; font-size: 6.4px; letter-spacing: 0.16em; text-transform: uppercase; }
/* time axis */
.f1-mustar { fill: none; stroke: rgba(239, 231, 214, 0.34); stroke-width: 0.8; stroke-dasharray: 2 2.6; }
.f1-mustar-t { fill: rgba(239, 231, 214, 0.55); font-size: 8.8px; font-style: italic; }
.f1-trace-dim { fill: none; stroke: rgba(239, 231, 214, 0.2); stroke-width: 1.1; stroke-linejoin: round; }
.f1-trace { fill: none; stroke: #f4eddd; stroke-width: 1.35; stroke-linejoin: round; }
.f1-tl-num { fill: rgba(232, 246, 237, 0.55); font-family: var(--mono) !important; font-size: 8px; }
.f1-tl-mu { fill: rgba(232, 246, 237, 0.78); font-size: 12.5px; font-style: italic; }
.f1-ax-dim { stroke: rgba(232, 246, 237, 0.18); stroke-width: 1.2; }
.f1-ax { stroke: var(--flux); stroke-width: 1.6; stroke-linecap: round; }
.f1-ax-brk { stroke: rgba(232, 246, 237, 0.45); stroke-width: 0.9; }
.f1-tick { stroke: rgba(232, 246, 237, 0.34); stroke-width: 0.8; }
.f1-anchor { fill: rgba(239, 231, 214, 0.62); }
.f1-capw { fill: rgba(232, 246, 237, 0.62); }
.f1-cap { font-family: var(--mono); font-size: 7.4px; letter-spacing: 0.16em; }
.f1-cap-m { font-size: 9.6px; font-style: italic; fill: rgba(232, 246, 237, 0.78); }
.f1-cap2 { fill: rgba(232, 246, 237, 0.52); font-size: 8.8px; font-style: italic; }
.f1-ph-line { stroke: rgba(239, 231, 214, 0.45); stroke-width: 0.7; stroke-dasharray: 1.4 1.8; }
.f1-ph-dot { fill: #fbf6ea; }
.f1-ph-ring { fill: #07100e; stroke: var(--flux); stroke-width: 1.3; }
.f1-ph-core { fill: var(--flux); }
.f1-ph-halo { fill: none; stroke: rgba(143, 240, 234, 0.4); stroke-width: 0.8; transform-box: fill-box; transform-origin: center;
  animation: f1-halo 2.4s ease-out infinite; }
@keyframes f1-halo { 0% { opacity: 0.9; transform: scale(0.65); } 100% { opacity: 0; transform: scale(1.55); } }
.f1.is-dragging .f1-ph-halo, .f1.is-paused .f1-ph-halo { animation: none; opacity: 0; }
.f1-hit { fill: transparent; cursor: ew-resize; touch-action: pan-y; pointer-events: all; }
.f1.is-dragging .f1-hit { cursor: grabbing; }
.f1-ctrl { outline: none; }
.f1-play { cursor: pointer; }
.f1-play-ring { fill: rgba(143, 240, 234, 0.06); stroke: rgba(143, 240, 234, 0.55); stroke-width: 0.9; transition: fill 160ms ease; }
.f1-play:hover .f1-play-ring { fill: rgba(143, 240, 234, 0.16); }
.f1-ic-pause rect, .f1-ic-play { fill: var(--flux); }
.f1-ic-play { display: none; }
.f1.is-paused .f1-ic-play { display: inline; }
.f1.is-paused .f1-ic-pause { display: none; }
.f1-ctrl:focus-visible .f1-play-ring { stroke: #fff; stroke-width: 1.5; }
.f1-slider:focus-visible ~ .f1-ph .f1-ph-ring, .f1-tl:focus-within .f1-ph-ring { stroke-width: 1.8; }
html:not(.js) .f1-play, html:not(.js) .f1-hit { display: none; }

/* the copy stays pinned while the plates scroll, where the screen is tall enough to show all of it */
@media (min-width: 821px) and (min-height: 760px) { .hero-copy { position: sticky; top: 100px; } }
/* figure plates: a quiet frame with gold registration corners */
@media (min-width: 821px) {
  .hero-theory-visual .theory-panel { position: relative; margin: 0 !important; padding: 18px 22px 16px !important;
    border: 1px solid rgba(239, 231, 214, 0.075) !important;
    background: linear-gradient(180deg, rgba(11, 26, 23, 0.74), rgba(7, 16, 14, 0.52)); }
  .hero-theory-visual .theory-panel + .theory-panel { margin-top: 18px !important; }
  .hero-theory-visual .theory-panel::before { --c: rgba(226, 194, 126, 0.6); position: absolute; inset: -1px; pointer-events: none; content: "";
    background:
      linear-gradient(var(--c), var(--c)) left top / 13px 1px no-repeat, linear-gradient(var(--c), var(--c)) left top / 1px 13px no-repeat,
      linear-gradient(var(--c), var(--c)) right top / 13px 1px no-repeat, linear-gradient(var(--c), var(--c)) right top / 1px 13px no-repeat,
      linear-gradient(var(--c), var(--c)) left bottom / 13px 1px no-repeat, linear-gradient(var(--c), var(--c)) left bottom / 1px 13px no-repeat,
      linear-gradient(var(--c), var(--c)) right bottom / 13px 1px no-repeat, linear-gradient(var(--c), var(--c)) right bottom / 1px 13px no-repeat; }
  .flux-block .diagram-header { padding-bottom: 10px; margin-bottom: 4px; border-bottom: 1px solid rgba(239, 231, 214, 0.06); }
  .flux-block .diagram-header::after { margin-left: auto; color: rgba(143, 240, 234, 0.62); content: "INTERACTIVE · DRAG t";
    font-family: var(--mono); font-size: 0.56rem; letter-spacing: 0.18em; text-transform: none; white-space: nowrap; }
  .holography-panel .diagram-header { padding-bottom: 10px; border-bottom: 1px solid rgba(239, 231, 214, 0.06); }
  .flux-c2 { margin-top: 10px; }
}
/* v4: hand-inserted sources, vacuum bonds, glueball loops */
.f1-ins { fill: none; stroke: rgba(244, 237, 221, 0.9); stroke-width: 1.1; stroke-dasharray: 3 2.4; pointer-events: none; }
.f1-vacband { fill: rgba(232, 246, 237, 0.02); stroke: rgba(232, 246, 237, 0.08); stroke-width: 0.5; stroke-dasharray: 1.4 1.8; }
.f1-vact { fill: rgba(232, 246, 237, 0.42); font-size: 6.6px; font-style: italic; }
.f1-hand { fill: rgba(244, 237, 221, 0.78); }
.f1-handt { fill: rgba(244, 237, 221, 0.66); font-family: var(--mono) !important; font-size: 6.4px; letter-spacing: 0.03em; }
.f1-bondglow { opacity: 0.32; }
.f1-lg-tube { stroke: var(--flux); stroke-width: 3; stroke-linecap: round; }
/* v5: colour-singlet clusters, in the notation of Halimeh et al., PRX Quantum 5, 030358 (2024) */
.f1-tri { fill: rgba(205, 232, 224, 0.05); stroke: rgba(205, 232, 224, 0.2); stroke-width: 0.75; stroke-linejoin: round; }
.f1-lk { fill: none; stroke: rgba(205, 232, 224, 0.36); stroke-width: 0.9; }
.f1-ak { fill: none; stroke-width: 1.5; stroke-linecap: round; }
.f1-ak-t { stroke: var(--flux); }
.f1-ak-g { stroke: var(--gold); }
.f1-kg path { fill: none; stroke-linecap: round; }
.f1-kg1 { stroke: rgba(121, 227, 225, 0.11); stroke-width: 13; }
.f1-kg2 { stroke: rgba(121, 227, 225, 0.2); stroke-width: 6; }
.f1-lb path { fill: none; stroke-linecap: round; }
.f1-lo { stroke-width: 15; stroke-opacity: 0.08; }
.f1-lm { stroke-width: 9.4; stroke-opacity: 0.42; }
.f1-lc { stroke-width: 3.6; stroke-opacity: 0.4; }
.f1-lb-t path { stroke: #7fe9e2; } .f1-lb-t .f1-lc { stroke: #e9fffc; }
.f1-lb-g path { stroke: #e2c27e; } .f1-lb-g .f1-lc { stroke: #fff4da; }
.f1-lb-i path { stroke: #efe7d6; } .f1-lb-i .f1-lm { stroke-opacity: 0.3; } .f1-lb-i .f1-lc { stroke: #ffffff; stroke-opacity: 0.32; }
.f1-sr { fill: #07100e; stroke: rgba(236, 232, 220, 0.66); stroke-width: 0.85; }
.f1-sf { fill: #f3eee2; }
.f1-sh { fill: rgba(239, 231, 214, 0.06); stroke: rgba(239, 231, 214, 0.34); stroke-width: 0.8; }
.f1-mv { pointer-events: none; }
.f1-mv-h { fill: rgba(244, 237, 221, 0.2); }
.f1-mv-c { fill: #fffaf0; }
.f1-srcs { fill: #f4eddd; stroke: #07100e; stroke-width: 0.8; }
.f1-rg path { fill: none; stroke-linejoin: round; }
.f1-rg-g1 { stroke: rgba(226, 194, 126, 0.07); stroke-width: 17; }
.f1-rg-g2 { stroke: rgba(226, 194, 126, 0.13); stroke-width: 7.5; }
.f1-g { pointer-events: none; }
.f1-g-h { fill: rgba(143, 240, 234, 0.16); }
.f1-g-c { fill: #f6fffd; }
.f1-g-o { fill: #07100e; stroke: #f6fffd; stroke-width: 1.15; }
.f1-ghalo { fill: none; stroke: rgba(143, 240, 234, 0.85); stroke-width: 0.9; stroke-dasharray: 2.2 2.4; }
.f1-gs { fill: rgba(232, 246, 237, 0.55); font-family: var(--mono) !important; font-size: 5.6px; letter-spacing: 0.12em; }
.f1-gs-l { fill: none; stroke: rgba(232, 246, 237, 0.28); stroke-width: 0.6; stroke-dasharray: 1 1.6; }
.f1-plaq-s { fill: rgba(226, 194, 126, 0.58); font-size: 7.2px; font-style: italic; }
.f1-link-iflash { fill: none; stroke: rgba(244, 237, 221, 0.75); stroke-width: 1.4; }
.f1-co-l { fill: none; stroke: rgba(143, 240, 234, 0.42); stroke-width: 0.6; }
.f1-co-t { fill: rgba(143, 240, 234, 0.84); font-family: var(--mono) !important; font-size: 6.2px; letter-spacing: 0.16em; }
.f1-co-s { fill: rgba(143, 240, 234, 0.6); font-size: 7.4px; font-style: italic; }
.f1-co-m { display: none; }
/* v7: the figure is a stack of four svg layers with one viewBox -- glow underlay, tube glow (its opacity follows
   P_conn on the compositor), the interactive figure, and the annotations: colour-singlet outlines, glueball markers,
   captions.  Each layer is its own compositor layer, so what changes in one never repaints the others. */
.f1-stage { position: relative; }
.f1-stage > svg.f1 { position: relative; }
.f1-layer { position: absolute; top: 0; left: 0; width: 100%; height: 100%; overflow: visible; pointer-events: none;
  -webkit-user-select: none; user-select: none; will-change: transform; }
.f1-tglow { will-change: transform, opacity; }
.f1-layer text { font-family: var(--math); }
.f1-ol path, .f1-gc circle { fill: none; stroke-linejoin: round; }
.f1-ol-g { stroke: rgba(143, 240, 234, 0.075); stroke-width: 4.6; }
.f1-ol-p { stroke: rgba(143, 240, 234, 0.82); stroke-width: 0.85; stroke-linecap: round; stroke-dasharray: 3.3 2.5; }
.f1-gc-g { stroke: rgba(226, 194, 126, 0.075); stroke-width: 4.6; }
.f1-gc-c { stroke: rgba(226, 194, 126, 0.85); stroke-width: 0.85; stroke-linecap: round; stroke-dasharray: 3.3 2.5; }
.f1-co-dot { fill: rgba(143, 240, 234, 0.8); }
.f1-labels text { paint-order: stroke; stroke: rgba(9, 21, 18, 0.92); stroke-width: 3.2px; stroke-linejoin: round; }
.f1-tl-hex { fill: none; stroke: rgba(226, 194, 126, 0.62); stroke-width: 0.8; stroke-linejoin: round; }
.f1-lg-tri { fill: rgba(205, 232, 224, 0.08); stroke: rgba(205, 232, 224, 0.42); stroke-width: 1; stroke-linejoin: round; }
.f1-lg-s { fill: #07100e; stroke: rgba(236, 232, 220, 0.75); stroke-width: 0.9; }
.f1-lg-s1 { fill: #f3eee2; }
.f1-lg-lobe { fill: none; stroke: #7fe9e2; stroke-opacity: 0.45; stroke-width: 6.6; stroke-linecap: round; }
.f1-lg-lobec { fill: none; stroke: #e9fffc; stroke-opacity: 0.4; stroke-width: 2.4; stroke-linecap: round; }
.f1-lg-closedc { fill: none; stroke: rgba(226, 194, 126, 0.35); stroke-width: 5.4; stroke-linejoin: round; }
.f1-legend svg.f1-lg-v { width: 1.2em; height: 1.05em; }
.f1-note { margin: 0.9cqi 0 0; color: rgba(232, 246, 237, 0.4); font-family: var(--text); font-size: clamp(7.5px, 1.45cqi, 10.5px); font-style: italic; text-align: right; }
.f1-note b { font-weight: 600; font-style: normal; }
.f1-caption { margin-top: 1.3cqi; color: rgba(232, 246, 237, 0.46); font-size: clamp(7.5px, 1.4cqi, 10.2px); line-height: 1.5; text-align: left; }
.f1-caption b { color: rgba(232, 246, 237, 0.68); font-weight: 500; }
.f1-caption sub { font-size: 0.75em; line-height: 0; }
/* v3: live readout, exact class bands, magnetic-term inset */
.f1-ro-vc { fill: var(--flux); }
.f1-ro-vf { fill: #f4eddd; }
.f1-ro-u { fill: rgba(232, 246, 237, 0.42); font-family: var(--mono) !important; font-size: 6.6px; letter-spacing: 0.06em; }
.f1-cls-dim .f1-bc { fill: rgba(143, 240, 234, 0.1); }
.f1-cls-dim .f1-b1 { fill: rgba(239, 231, 214, 0.07); }
.f1-cls-dim .f1-b2 { fill: rgba(239, 231, 214, 0.045); }
.f1-cls-dim .f1-b0 { fill: rgba(170, 190, 184, 0.03); }
.f1-cls-lit .f1-bc { fill: rgba(143, 240, 234, 0.4); }
.f1-cls-lit .f1-b1 { fill: rgba(239, 231, 214, 0.3); }
.f1-cls-lit .f1-b2 { fill: rgba(239, 231, 214, 0.15); }
.f1-cls-lit .f1-b0 { fill: rgba(170, 190, 184, 0.08); }
.f1-blc, .f1-bl1, .f1-bl2 { fill: none; stroke-linejoin: round; }
.f1-cls-dim .f1-blc { stroke: rgba(143, 240, 234, 0.28); stroke-width: 0.7; }
.f1-cls-dim .f1-bl1, .f1-cls-dim .f1-bl2 { stroke: rgba(239, 231, 214, 0.14); stroke-width: 0.5; }
.f1-cls-lit .f1-blc { stroke: var(--flux); stroke-width: 1.15; }
.f1-cls-lit .f1-bl1 { stroke: rgba(244, 237, 221, 0.7); stroke-width: 0.7; }
.f1-cls-lit .f1-bl2 { stroke: rgba(244, 237, 221, 0.35); stroke-width: 0.5; }
.f1-pframe { fill: none; stroke: rgba(232, 246, 237, 0.14); stroke-width: 0.6; stroke-dasharray: 1.2 2; }
.f1-bt { font-size: 7.6px; font-style: italic; pointer-events: none; }
.f1-bt-c { fill: #e6fffb; }
.f1-bt-f { fill: #fbf6ea; }
.f1-bt-s { fill: rgba(251, 246, 234, 0.72); font-size: 6.2px; }
.f1-ph-pdot { fill: var(--flux); stroke: #07100e; stroke-width: 0.8; }
.f1-plaq-c2 { fill: rgba(226, 194, 126, 0.62); font-size: 7.4px; font-style: italic; }
.f1-kin-h { fill: var(--gold); font-family: var(--mono) !important; font-size: 6.6px; letter-spacing: 0.18em; }
.f1-kin-hm { fill: var(--gold); font-size: 9px; font-style: italic; }
.f1-kin-s { fill: rgba(232, 246, 237, 0.52); font-size: 7.6px; font-style: italic; }
.f1-kin-ax { fill: none; stroke: rgba(232, 246, 237, 0.28); stroke-width: 0.6; }
.f1-kin-half { fill: none; stroke: rgba(232, 246, 237, 0.14); stroke-width: 0.5; stroke-dasharray: 1 1.8; }
.f1-kin-n { fill: rgba(232, 246, 237, 0.48); font-family: var(--mono) !important; font-size: 6.2px; }
.f1-kin-m { fill: rgba(232, 246, 237, 0.55); font-size: 7.6px; font-style: italic; }
.f1-kin-k0 { fill: none; stroke: var(--flux); stroke-width: 1; stroke-linejoin: round; }
.f1-kin-k0-d { fill: var(--flux); }
.f1-kin-k2 { fill: none; stroke: var(--gold); stroke-width: 1; stroke-linejoin: round; }
.f1-kin-k2-d.is-e { fill: var(--gold); }
.f1-kin-k2-d.is-p { fill: #07100e; stroke: var(--gold); stroke-width: 0.9; }
.f1-kin-k4 { fill: none; stroke: rgba(226, 194, 126, 0.55); stroke-width: 0.8; stroke-dasharray: 2 1.6; }
.f1-kin-k0.is-switch, .f1-kin-k2.is-switch { stroke-dasharray: 1.6 1.6; opacity: 0.8; }
.f1-kin-k4-d { fill: #07100e; stroke: rgba(226, 194, 126, 0.6); stroke-width: 0.8; }
.f1-kin-l { font-size: 7.4px; font-style: italic; }
.f1-kin-l0 { fill: var(--flux); }
.f1-kin-l2 { fill: var(--gold); }
.f1-kin-l4 { fill: rgba(226, 194, 126, 0.7); }
.f1-kin-mk { fill: none; stroke: rgba(244, 237, 221, 0.6); stroke-width: 0.7; stroke-dasharray: 1.2 1.6; }
.f1-kin-t { fill: rgba(232, 246, 237, 0.5); font-size: 7px; font-style: italic; }

.f1-ham { display: flex; align-items: flex-start; justify-content: space-between; gap: 0.5em; margin: 1.6cqi 0 0;
  padding-top: 1.6cqi; border-top: 1px solid rgba(220, 245, 231, 0.09); color: #e8f1ec; font-family: var(--math);
  font-size: clamp(8.5px, 2.12cqi, 14px); line-height: 1.2; white-space: nowrap; }
.f1-ham-h { padding-right: 0.1em; }
.f1-term, .f1-ham-h { display: grid; grid-template-rows: 2.15em auto; justify-items: center; align-items: center; }
.f1-term small { margin-top: 0.55em; padding-top: 0.4em; border-top: 1px solid currentColor; font-family: var(--mono);
  font-size: 0.5em; letter-spacing: 0.16em; text-transform: uppercase; opacity: 0.62; }
.f1-term-m { color: var(--ivory); }
.f1-term-e { color: var(--flux); }
.f1-term-b { color: var(--gold); }
.f1-term-c { color: rgba(232, 246, 237, 0.45); }
.f1-legend { display: flex; flex-wrap: nowrap; justify-content: space-between; gap: 0.8em; margin: 1.5cqi 0 0; padding: 1.5cqi 0 0; border-top: 1px solid rgba(220, 245, 231, 0.09);
  list-style: none; color: rgba(232, 246, 237, 0.56); font-family: var(--text); font-size: clamp(8px, 1.7cqi, 12px); white-space: nowrap; }
.f1-legend li { display: flex; align-items: center; gap: 0.45em; }
.f1-legend svg { width: 2.1em; height: 0.95em; flex: none; }
.f1-legend svg.f1-lg-hex { width: 1.15em; height: 1.05em; }
.f1-lg-site { fill: none; stroke: rgba(236, 232, 220, 0.75); stroke-width: 1; }
.f1-lg-q { fill: var(--ivory); }
.f1-lg-r { fill: var(--flux); }
.f1-lg-open { stroke: var(--flux); stroke-width: 2.2; stroke-linecap: round; }
.f1-lg-closed { fill: none; stroke: var(--gold); stroke-width: 2; stroke-linejoin: round; }


/* ---------- Hero, elevated ---------- */
.hero {
  background:
    radial-gradient(110% 80% at 80% 14%, rgba(64, 158, 138, 0.13), transparent 56%),
    radial-gradient(70% 55% at 6% 104%, rgba(226, 194, 126, 0.045), transparent 62%),
    linear-gradient(160deg, #050c0a 0%, #0a1512 54%, #060d0b 100%);
}
.hero::before {
  /* grain: plain alpha at .014 matches the former overlay blend at .075 on this dark ground (mean difference 0.02/255),
     without making every frame re-blend the whole hero backdrop when something beneath it moves */
  position: absolute; inset: 0; z-index: 1; pointer-events: none; content: ""; opacity: 0.014;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 .6 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}
.hero::after { opacity: 0.16; }
.lattice-canvas { opacity: 0.38; }

.wordmark { gap: 14px; }
.wordmark-mark { width: 38px; height: 38px; border-color: rgba(239, 231, 214, 0.32); color: var(--ivory);
  font-family: var(--display); font-size: 1.02rem; font-style: italic; font-weight: 600; letter-spacing: 0.03em; }
.wordmark-text { color: #f1ece1; font-size: 1.16rem; font-weight: 600; letter-spacing: 0.015em; }
.site-nav { gap: 34px; }
.site-nav a { font-size: 0.66rem; letter-spacing: 0.18em; text-transform: uppercase; opacity: 0.74; }
.site-nav .nav-cta { padding: 11px 17px; border-color: rgba(239, 231, 214, 0.28); }
.site-nav .nav-cta:hover, .site-nav .nav-cta:focus-visible { border-color: var(--flux); color: var(--flux); }

.eyebrow { margin-bottom: min(28px, 3.1vh); }
.eyebrow span { background: rgba(239, 231, 214, 0.5); }
.eyebrow strong { color: #f3efe6; font-size: clamp(2.3rem, min(3.9vw, 6.3vh), 3.9rem); letter-spacing: -0.01em; line-height: 0.95; }
.eyebrow small { margin-top: 4px; color: rgba(143, 240, 234, 0.82); font-family: var(--mono); font-size: clamp(0.62rem, 0.74vw, 0.72rem);
  letter-spacing: 0.22em; text-transform: uppercase; }
.hero h1 { color: #f3efe6; font-size: clamp(2.8rem, min(5.25vw, 8.5vh), 5.2rem); letter-spacing: -0.016em; line-height: 0.92; }
.hero h1 em { color: var(--flux); letter-spacing: -0.012em; }
.hero-intro { max-width: 35.5em; margin-top: min(26px, 2.9vh); color: rgba(236, 240, 232, 0.7); font-size: clamp(0.94rem, min(1.1vw, 1.95vh), 1.1rem); line-height: 1.68; }
.hero-actions { gap: 14px; margin-top: min(30px, 3.3vh); }
.button { min-height: 48px; gap: 16px; padding: 14px 22px; font-size: 0.66rem; font-weight: 500; letter-spacing: 0.2em; text-transform: uppercase; }
.button-primary { color: #04110e; background: var(--flux); }
.button-primary:hover, .button-primary:focus-visible { background: #e6fffb; }
.button-ghost { border-color: rgba(239, 231, 214, 0.26); }
.button span[aria-hidden] { font-family: var(--text); font-size: 1rem; letter-spacing: 0; }

.hero-ledger { display: grid; max-width: 36rem; margin: min(28px, 3.1vh) 0 0; padding: 0; grid-template-columns: repeat(3, minmax(0, 1fr));
  border-top: 1px solid rgba(239, 231, 214, 0.12); }
.hero-ledger div { padding: 14px 20px 0 0; margin-right: 20px; border-right: 1px solid rgba(239, 231, 214, 0.08); }
.hero-ledger div:last-child { margin-right: 0; padding-right: 0; border-right: 0; }
.hero-ledger dt { color: rgba(143, 240, 234, 0.62); font-family: var(--mono); font-size: 0.58rem; letter-spacing: 0.22em; text-transform: uppercase; }
.hero-ledger dd { display: flex; align-items: center; gap: 9px; margin: 7px 0 0; color: rgba(236, 240, 232, 0.8); font-size: 0.9rem; line-height: 1.35; }
.hero-ledger a { color: inherit; text-decoration: none; background: linear-gradient(currentColor, currentColor) 0 100% / 100% 1px no-repeat;
  background-color: transparent; padding-bottom: 1px; transition: color 180ms ease; }
.hero-ledger a:hover, .hero-ledger a:focus-visible { color: var(--flux); }
.hero-ledger .signal-dot { width: 6px; height: 6px; flex: none; }

/* hero: a wide column for the figure plates; the copy stays in view while the plates scroll */
@media (min-width: 821px) {
  :root { --shell: min(1320px, calc(100vw - 80px)); }
  .hero-grid { min-height: calc(100svh - 96px); align-items: start; padding-top: 100px; padding-bottom: 64px;
    grid-template-columns: minmax(0, 0.8fr) minmax(0, 1.2fr); gap: clamp(36px, 3.6vw, 64px); }
  .hero { overflow: clip; }
  .hero-copy { align-self: start; }
  .hero-theory-visual { max-width: 800px; width: 100%; justify-self: end; }
  .hero h1 { font-size: clamp(2.6rem, 4.3vw, 4.5rem); }
  .eyebrow strong { font-size: clamp(2.2rem, 3.5vw, 3.5rem); }
}
/* figure plates: one-line headers */
@media (min-width: 821px) {
  .diagram-header { display: flex; flex-wrap: wrap; align-items: baseline; gap: 2px 12px; margin-bottom: 10px; }
  .diagram-eyebrow { width: auto; margin: 0; padding: 3px 7px 2px; border: 1px solid rgba(239, 231, 214, 0.22); }
  .diagram-context::before { content: none; }
  .diagram-context { margin: 0; font-size: 0.84rem; }
  .holography-panel { margin-top: 14px !important; padding-top: 12px !important; }
  .ads-stage { width: 84%; margin: 0 auto; }
}
/* figure plates */
.diagram-eyebrow { color: rgba(239, 231, 214, 0.78); font-size: 0.6rem; letter-spacing: 0.22em; }
.diagram-eyebrow span { margin: 0 0.35em; color: rgba(143, 240, 234, 0.6); }
.diagram-header h3 { color: #f1ece1; font-size: clamp(1.4rem, 1.85vw, 1.85rem); letter-spacing: -0.005em; }
.diagram-context { color: rgba(214, 228, 220, 0.62); font-style: italic; }
@media (min-width: 821px) {
  .holography-panel { margin-top: 20px; padding-top: 16px; border-top: 1px solid rgba(239, 231, 214, 0.08); }
}
.ads-stage svg { position: relative; display: block; }
.diagram-formula { color: #ecf3ee; }

.js body:not([data-view="home"]) .wordmark-text { color: var(--ink); }

/* narrow figure columns (short laptop screens): keep each figure header on one line */
.hero-theory-visual { container-type: inline-size; }
@media (min-width: 821px) {
  @container (max-width: 500px) {
    .diagram-header { gap: 2px 9px; }
    .diagram-header h3 { font-size: 1.2rem; }
    .diagram-context { font-size: 0.72rem; }
  }
}
/* narrow figure columns: the legend wraps into two rows */
@container (max-width: 520px) {
  .f1-legend { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); justify-content: start; gap: 0.4em 1.4em; }
}
/* Fig. 1 on narrow screens: declutter the lattice, wrap the Hamiltonian and legend */
@media (max-width: 820px) {
  @container (max-width: 560px) {
    .f1-lid, .f1-vid { display: none; }
    .f1-ch { font-size: 15px; }
    .f1-ro-k { font-size: 11.5px; } .f1-ro-v { font-size: 10px; } .f1-ro-u { display: none; }
    .f1-cap { font-size: 9px; letter-spacing: 0.1em; } .f1-cap-m { font-size: 11px; } .f1-cap2 { font-size: 10.5px; }
    .f1-tl-num { font-size: 10px; } .f1-mustar-t { font-size: 10.5px; } .f1-tl-mu { font-size: 14px; }
    .f1-play { transform-box: fill-box; transform-origin: center; transform: scale(1.7); }
    .f1-ph-ring { r: 5.6; }
    .f1-ham { flex-wrap: wrap; justify-content: flex-start; gap: 0.7em 0.9em; padding-left: 2.1em; font-size: 11.5px; }
    .f1-ham-h { margin-left: -2.1em; }
    .f1-legend { display: grid; grid-template-columns: 1fr 1fr; gap: 0.7em 1em; font-size: 10.5px; white-space: normal; }
    .f1-legend li:first-child { grid-column: 1 / -1; }
    .f1-co-t { font-size: 9.5px; letter-spacing: 0.1em; } .f1-co-d { display: none; } .f1-co-m { display: inline; }
    .f1-plaq-t { font-size: 18px; } .f1-plaq-c { font-size: 9.5px; letter-spacing: 0.1em; } .f1-plaq-s { font-size: 10.5px; }
    .f1-srcq { font-size: 12px; }
    .f1-gs { font-size: 7.5px; }
    .f1-note { font-size: 9.5px; }
  }
}

@media (max-width: 820px) {
  .eyebrow small { letter-spacing: 0.14em; }
  .hero-ledger { grid-template-columns: 1fr; }
  .hero-ledger div { margin-right: 0; padding: 12px 0 0; border-right: 0; }
}

/* generated choreography */
__FIG1_KEYFRAMES__

@media (prefers-reduced-motion: reduce) {
  .f1-ph-halo { animation: none; opacity: 0; }
}
/* ---------- v8: every card carries an ink thumbnail of its figure plate ---------- */
.card-fig { position: absolute; right: clamp(26px, 3.2vw, 44px); bottom: clamp(22px, 2.8vw, 38px); display: flex; flex-direction: column;
  align-items: flex-end; gap: 5px; pointer-events: none; }
.card-fig svg { display: block; width: 118px; height: 63px; overflow: visible; opacity: 0.78; transition: opacity 220ms ease, transform 220ms var(--ease); }
.profile-card:hover .card-fig svg, .profile-card:focus-visible .card-fig svg, .project:hover .card-fig svg, .project:focus-within .card-fig svg { opacity: 1; transform: translateY(-2px); }
.card-fig-n { color: #7b8983; font-family: var(--mono); font-size: 0.56rem; letter-spacing: 0.2em; text-transform: uppercase; }
.cf-ink { fill: none; stroke: rgba(28, 98, 94, 0.42); stroke-width: 1; stroke-linejoin: round; }
.cf-dash { stroke-dasharray: 2.6 2.2; }
.cf-key { fill: none; stroke: #1f8f89; stroke-width: 2.1; stroke-linecap: round; stroke-linejoin: round; }
.cf-key-l { fill: none; stroke: #1f8f89; stroke-width: 1.2; stroke-dasharray: 3 2.2; }
.cf-lev { stroke: #1f8f89; stroke-width: 1.3; }
.cf-gold { fill: none; stroke: #b08a3e; stroke-width: 1.1; stroke-dasharray: 3 2.2; }
.cf-gold-l { fill: none; stroke: #b08a3e; stroke-width: 1.1; stroke-dasharray: 3 2.2; }
.cf-dot { fill: #f7f4ec; stroke: #2a6f6b; stroke-width: 1; }
.cf-src { fill: #f7f4ec; stroke: #1b3e3b; stroke-width: 1.4; }
.cf-core { fill: #f7f4ec; stroke: #1f8f89; stroke-width: 1.2; }
.cf-trk { stroke: #1b3e3b; stroke-width: 1.3; stroke-dasharray: 3 2; }
.cf-tipk { fill: #1f8f89; }
.project-body, .profile-card { padding-bottom: max(clamp(32px, 4vw, 52px), 104px); }
@media (max-width: 560px) { .card-fig svg { width: 96px; height: 51px; } }
/* ---------- v8: Fig. 2 legend in the language of Fig. 1 ---------- */
.ads-legend { justify-content: center; gap: 0.5em 1.4em; margin-top: 1.4cqi; flex-wrap: wrap; }
.ads-lg-plane { fill: rgba(143, 213, 192, 0.06); stroke: rgba(122, 175, 158, 0.75); stroke-width: 1; }
.ads-lg-loop { fill: none; stroke: #d5f8e9; stroke-width: 1.5; }
.ads-lg-mesh { fill: none; stroke: rgba(150, 216, 197, 0.85); stroke-width: 1.1; }
.ads-lg-back { stroke-opacity: 0.4; stroke-dasharray: 2 2.4; }
.ads-lg-rad { fill: none; stroke: #a0c6b7; stroke-width: 1.1; }
.holography-caption .f1-note { text-align: center; }
/* ---------- v8: figure plates (Fig. 3-10) -- the anatomy and vocabulary of Fig. 1 in every dialog ---------- */
.plate { position: relative; margin: 0; padding: 16px 20px 14px; border: 1px solid rgba(239, 231, 214, 0.075);
  background: linear-gradient(180deg, rgba(11, 26, 23, 0.74), rgba(7, 16, 14, 0.52)); container-type: inline-size; }
.plate::before { --c: rgba(226, 194, 126, 0.6); position: absolute; inset: -1px; pointer-events: none; content: "";
  background:
    linear-gradient(var(--c), var(--c)) left top / 13px 1px no-repeat, linear-gradient(var(--c), var(--c)) left top / 1px 13px no-repeat,
    linear-gradient(var(--c), var(--c)) right top / 13px 1px no-repeat, linear-gradient(var(--c), var(--c)) right top / 1px 13px no-repeat,
    linear-gradient(var(--c), var(--c)) left bottom / 13px 1px no-repeat, linear-gradient(var(--c), var(--c)) left bottom / 1px 13px no-repeat,
    linear-gradient(var(--c), var(--c)) right bottom / 13px 1px no-repeat, linear-gradient(var(--c), var(--c)) right bottom / 1px 13px no-repeat; }
.plate .diagram-header { display: flex; flex-wrap: wrap; align-items: baseline; gap: 2px 12px; margin: 0 0 8px; padding-bottom: 10px;
  border-bottom: 1px solid rgba(239, 231, 214, 0.06); }
.plate .diagram-eyebrow { width: auto; margin: 0; padding: 3px 7px 2px; border: 1px solid rgba(239, 231, 214, 0.22); font-size: 0.6rem; }
.plate .diagram-header h3 { margin: 0; font-size: clamp(1.12rem, 1.5vw, 1.42rem); }
.plate .diagram-context { margin: 0; font-size: 0.82rem; }
.plate .diagram-context::before { content: none; }
.plate-stage { position: relative; }
.plate-svg .plate-stage svg { position: static; display: block; width: 100%; height: auto; overflow: visible; }
.plate-legend { display: flex; flex-wrap: wrap; gap: 0.45em 1.25em; margin: 10px 0 0; padding: 10px 0 0; border-top: 1px solid rgba(220, 245, 231, 0.07);
  list-style: none; color: rgba(232, 246, 237, 0.56); font-family: var(--text); font-size: 0.74rem; line-height: 1.2; }
.plate-legend li { display: flex; align-items: center; gap: 0.45em; }
.plate-legend svg { width: 2.1em; height: 0.95em; flex: none; overflow: visible; }
.plate-legend svg.pl-lg-v { width: 1.2em; height: 1.05em; }
.plate-legend svg.pl-lg-sq { width: 1em; height: 1em; }
.plate-legend sub { font-size: 72%; }
.plate-note { margin: 8px 0 0; color: rgba(232, 246, 237, 0.4); font-family: var(--text); font-size: 0.7rem; font-style: italic; line-height: 1.4; text-align: right; }
.plate-note b { font-weight: 600; font-style: normal; }
.plate.schematic { width: 100%; }
.plate.schematic .plate-legend svg { position: static; inset: auto; display: block; width: 2.1em; height: 0.95em; }
.plate.schematic .plate-legend svg.pl-lg-sq { width: 1em; height: 1em; }
.plate.schematic figcaption.sr-only { margin: 0; }
/* drawing vocabulary */
.pl-svg text { font-family: var(--math); }
.pl-t { fill: rgba(236, 244, 239, 0.88); font-size: 11.5px; }
.pl-ts { fill: rgba(232, 246, 237, 0.56); font-size: 9.6px; }
.pl-ti { font-style: italic; }
.pl-big { font-size: 15px; }
.pl-sub { font-size: 72%; }
.pl-cap { fill: rgba(143, 240, 234, 0.86); font-family: var(--mono) !important; font-size: 7px; letter-spacing: 0.16em; }
.pl-caps { fill: rgba(143, 240, 234, 0.6); font-size: 8.4px; font-style: italic; }
.pl-panel { fill: rgba(239, 231, 214, 0.72); font-family: var(--mono) !important; font-size: 7.4px; letter-spacing: 0.06em; }
.pl-lead { fill: none; stroke: rgba(143, 240, 234, 0.42); stroke-width: 0.6; }
.pl-ldot { fill: rgba(143, 240, 234, 0.85); }
.pl-rule { stroke: rgba(220, 245, 231, 0.09); stroke-width: 0.8; }
.pl-ax { fill: none; stroke: rgba(232, 246, 237, 0.34); stroke-width: 0.8; }
.pl-half { fill: none; stroke: rgba(232, 246, 237, 0.18); stroke-width: 0.6; stroke-dasharray: 1.4 2; }
.pl-num-t { fill: rgba(232, 246, 237, 0.5); font-family: var(--mono) !important; font-size: 7px; }
.pl-curve { fill: none; stroke: #79e3e1; stroke-width: 1.4; stroke-linejoin: round; stroke-linecap: round; }
.pl-curve-iv { fill: none; stroke: rgba(244, 237, 221, 0.8); stroke-width: 1.1; stroke-linejoin: round; }
.pl-area { fill: rgba(121, 227, 225, 0.09); }
.pl-tq { fill: #8ff0ea; }
.pl-tiv { fill: rgba(244, 237, 221, 0.88); }
.pl-gc { fill: none; stroke: rgba(226, 194, 126, 0.85); stroke-width: 0.85; stroke-dasharray: 3.3 2.5; stroke-linecap: round; }
.pl-olpath { fill: none; stroke-linejoin: round; pointer-events: none; }
.pl-level { stroke: rgba(121, 227, 225, 0.5); stroke-width: 1; }
.pl-level-d { stroke: #79e3e1; stroke-width: 1.25; }
.pl-tip { fill: #79e3e1; }
.pl-tip-iv { fill: rgba(244, 237, 221, 0.88); }
.pl-arrow { fill: none; stroke: rgba(121, 227, 225, 0.62); stroke-width: 1; }
.pl-arrow-iv { fill: none; stroke: rgba(244, 237, 221, 0.72); stroke-width: 1; }
.pl-num-c, .pl-step-c { fill: #0a1714; stroke: rgba(239, 231, 214, 0.55); stroke-width: 0.75; }
.pl-num { fill: rgba(239, 231, 214, 0.92); font-family: var(--mono) !important; font-size: 6.6px; }
.pl-step-c { stroke: rgba(121, 227, 225, 0.62); }
.pl-step-end { stroke: rgba(226, 194, 126, 0.9); }
.pl-step { fill: #8ff0ea; font-family: var(--mono) !important; font-size: 8px; }
.pl-dotc { fill: #f3eee2; }
.pl-site { fill: #07100e; stroke: rgba(236, 232, 220, 0.66); stroke-width: 0.85; }
.pl-spin { fill: none; stroke: #f3eee2; stroke-width: 1.2; }
.pl-bond { stroke: rgba(121, 227, 225, 0.78); stroke-linecap: round; }
.pl-bond-s { stroke-width: 2.4; }
.pl-bond-w { stroke-width: 1.1; }
.pl-bond2 { stroke: rgba(205, 232, 224, 0.42); stroke-width: 0.9; stroke-dasharray: 3 2.6; }
.pl-q { fill: #e2c27e; font-size: 13px; font-style: italic; }
.pl-box { fill: rgba(13, 29, 24, 0.9); stroke: rgba(220, 245, 231, 0.24); stroke-width: 0.9; }
.pl-box-strong { stroke: rgba(121, 227, 225, 0.5); }
.pl-grid { stroke: rgba(121, 227, 225, 0.1); stroke-width: 0.7; }
.pl-track { stroke: rgba(244, 237, 221, 0.9); stroke-width: 1.5; stroke-linecap: round; }
.pl-track-in { stroke-dasharray: 3 2.4; stroke-opacity: 0.6; }
.pl-photon { stroke: rgba(232, 246, 237, 0.5); stroke-width: 0.9; stroke-dasharray: 1.6 2.2; }
.pl-cathode { stroke: rgba(226, 194, 126, 0.85); stroke-width: 1.6; stroke-linecap: round; }
.pl-signal { fill: none; stroke: rgba(121, 227, 225, 0.66); stroke-width: 1.1; }
.pl-signal-thin { fill: none; stroke: rgba(121, 227, 225, 0.55); stroke-width: 0.9; stroke-linejoin: round; }
.pl-wave { fill: none; stroke: rgba(121, 227, 225, 0.6); stroke-width: 1; }
.pl-halo { fill: rgba(143, 240, 234, 0.16); }
.pl-tri-big { stroke-width: 0.9; }
.pl-labels text, text.pl-hl, .pl-svg .f1-srcl, .pl-svg .f1-srcq { paint-order: stroke; stroke: rgba(9, 21, 18, 0.92); stroke-width: 3.2px; stroke-linejoin: round; }
/* legend icons */
.pl-lg-ol { fill: none; stroke: rgba(143, 240, 234, 0.85); stroke-width: 1.1; stroke-dasharray: 3 2.2; }
.pl-lg-gc { fill: none; stroke: rgba(226, 194, 126, 0.9); stroke-width: 1.1; stroke-dasharray: 3 2.2; }
.pl-lg-curve { fill: none; stroke: #79e3e1; stroke-width: 1.6; }
.pl-lg-curve-iv { fill: none; stroke: rgba(244, 237, 221, 0.85); stroke-width: 1.4; }
.pl-lg-level { stroke: rgba(121, 227, 225, 0.6); stroke-width: 1.3; }
.pl-lg-doublet { stroke: #79e3e1; stroke-width: 1.3; }
.pl-lg-area { fill: rgba(121, 227, 225, 0.18); stroke: #79e3e1; stroke-width: 1; }
.pl-lg-site { fill: #07100e; stroke: rgba(236, 232, 220, 0.75); stroke-width: 1.2; }
.pl-lg-bond { stroke: rgba(121, 227, 225, 0.85); stroke-width: 2.4; stroke-linecap: round; }
.pl-lg-bond2 { stroke: rgba(205, 232, 224, 0.55); stroke-width: 1.2; stroke-dasharray: 3 2.4; }
.pl-lg-track { stroke: rgba(244, 237, 221, 0.9); stroke-width: 1.8; stroke-linecap: round; }
.pl-lg-photon { stroke: rgba(232, 246, 237, 0.65); stroke-width: 1.2; stroke-dasharray: 1.8 2.2; }
.pl-lg-signal, .pl-lg-flow { fill: none; stroke: rgba(121, 227, 225, 0.8); stroke-width: 1.3; }
.pl-lg-est { stroke: rgba(121, 227, 225, 0.7); stroke-width: 1.2; } .pl-lg-est-d { fill: #79e3e1; }
.pl-lg-dev { stroke: rgba(226, 194, 126, 0.75); stroke-width: 1.1; stroke-dasharray: 3 2.4; } .pl-lg-dev-d { fill: #e2c27e; }
.pl-lg-base { stroke: rgba(239, 231, 214, 0.5); stroke-width: 1.1; stroke-dasharray: 1.4 2.4; } .pl-lg-base-d { fill: rgba(239, 231, 214, 0.85); }
/* the profile maps: nodes as annotations, coloured by maturity, on the plate ground */
.plate.schematic .map-core, .plate.schematic .map-node { --cat: rgba(121, 227, 225, 0.7); border: 0; border-top: 1px solid var(--cat);
  background: #0a1815; box-shadow: 0 0 0 5px #0a1815; backdrop-filter: none; }
.plate.schematic .map-node { padding: 9px 11px 10px; }
.plate.schematic .map-core { border: 1px solid rgba(121, 227, 225, 0.5); box-shadow: 0 0 0 5px #0a1815, 0 0 30px rgba(121, 227, 225, 0.1); }
.plate.schematic .map-node span { color: rgba(143, 240, 234, 0.9); }
.plate.schematic .map-dev { --cat: rgba(226, 194, 126, 0.8); }
.plate.schematic .map-dev span { color: #e2c27e; }
.plate.schematic .map-base { --cat: rgba(239, 231, 214, 0.55); }
.plate.schematic .map-base span { color: rgba(239, 231, 214, 0.78); }
.plate.schematic .map-core strong, .plate.schematic .map-node strong { color: #eef4ef; }
.sch-edge-est { stroke: rgba(121, 227, 225, 0.5); stroke-dasharray: none; stroke-width: 1; }
.sch-edge-dev { stroke: rgba(226, 194, 126, 0.55); stroke-dasharray: 3.3 2.5; stroke-width: 0.95; }
.sch-edge-base { stroke: rgba(239, 231, 214, 0.32); stroke-dasharray: 1.4 2.6; stroke-width: 1; }
.sch-ring-est { fill: none; stroke: rgba(143, 240, 234, 0.55); stroke-width: 1; stroke-dasharray: 3.3 2.5; stroke-linecap: round; }
.sch-ring-dev { fill: none; stroke: rgba(226, 194, 126, 0.55); stroke-width: 1; stroke-dasharray: 3.3 2.5; stroke-linecap: round; }
.sch-ring-label-est { fill: rgba(143, 240, 234, 0.7); font-family: var(--mono); font-size: 8px; letter-spacing: 0.22em; }
.sch-ring-label-dev { fill: rgba(226, 194, 126, 0.75); font-family: var(--mono); font-size: 8px; letter-spacing: 0.22em; }
.plate .sch-hex { stroke: rgba(121, 227, 225, 0.075); }
.plate .sch-tip { fill: #79e3e1; }
.plate .sch-tip-gold { fill: #e2c27e; }
/* narrow plates: the drawings keep a legible size and scroll sideways */
@container (max-width: 520px) {
  .plate-svg .plate-stage { overflow-x: auto; -webkit-overflow-scrolling: touch; }
  .plate-svg .plate-stage svg { width: 560px; max-width: none; }
  .plate { padding: 12px 12px 10px; }
  .plate-legend { font-size: 0.7rem; gap: 0.4em 1em; }
}
@media (max-width: 820px) { .plate { margin-top: 6px; } }

/* ---- footer meta: update stamp and source link ---- */
.footer-meta { gap: 3px; text-align: center; }
.footer-meta time { color: #d9e4de; }
.footer-grid .footer-meta a { color: #becac4; font-size: inherit; text-decoration: underline; text-decoration-color: rgba(190, 202, 196, 0.45); text-underline-offset: 2px; }
.footer-grid .footer-meta a:hover { color: var(--mint); text-decoration-color: currentColor; }
.dialog-note { margin: 0; color: var(--ink-soft); font-family: var(--text); font-size: 0.9rem; font-style: italic; }
/* ===== END DESIGN SYSTEM v4 ===== */
"""

def build():
    css = open(CSS).read()
    css = re.sub(r"/\* ===== FONTS \(managed.*?/\* ===== END FONTS ===== \*/\n", "", css, flags=re.S)
    css = re.sub(r"\n/\* ===== DESIGN SYSTEM v4 \(managed\) ===== \*/.*?/\* ===== END DESIGN SYSTEM v4 ===== \*/\n", "\n", css, flags=re.S)
    design = DESIGN.replace("__FIG1_KEYFRAMES__", open(FIG1).read() if os.path.exists(FIG1) else "")
    css = FONTS + css.rstrip() + "\n" + design
    open(CSS, "w").write(css)
    print("styles.css:", len(css))

if __name__ == "__main__":
    build()
