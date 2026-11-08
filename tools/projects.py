"""Project dialog templates (copy + figure plates Fig. 7-10 from plates.py); spliced into index.html."""
import html, os, re
import plates

# ---------- copy for each project ----------
projects = {
    "msc": dict(meta=("M.Sc. thesis · LMU Munich", "2025—present"),
        title="QGP-Scope: Non-Abelian Gauge Dynamics in a (2+1)D SU(2) Quantum Link Model",
        abstract="The thesis investigates source-supported electric flux, matter screening and real-time response in a finite "
                 "two-rishon SU(2) quantum-link model on an open honeycomb lattice, with its representation, conserved sectors and "
                 "numerical accuracy specified explicitly.",
        facts=[("Research question", "How does an imposed static source pair organise electric flux, and how does dynamical matter screen it, on a loop-bearing honeycomb lattice?"),
               ("Methods", "Exact diagonalisation in pre-specified Gauss-law sectors, Gauss-exact DMRG and TDVP, Krylov propagation and physical-sector thermal calculations, cross-checked by an independent first-principles reconstruction."),
               ("Results", "On the C₂ patch, gauge-invariant sectors of up to 46,829 states (product spaces of 6.7 million) are solved exactly. A thirteen-mass ladder resolves a crossover from screening-like to confinement-like response; the heavy-mass finite-distance force is 1.03 ± 0.01 tₕ/a per link. A mass quench from m = 4 to 0.5 suppresses the source connection throughout the exact window t ≤ 20."),
               ("Supervision", "Prof. Dr. Fabian Grusdt; co-supervision M.Sc. Gaia De Paciani, LMU Munich.")],
        tags=["SU(2) lattice gauge theory", "Quantum link models", "Exact diagonalisation", "DMRG / TDVP", "Cold-atom quantum simulation"],
        actions='<p class="dialog-note">Full text available on request.</p>',
        schem=plates.fig7()),
    "heat": dict(meta=("Peer-reviewed article · First author", "2023"),
        title="Quantum Heat Engine with Level Degeneracy for Oscillator-Shaped Potential Well",
        abstract="A Szilard-like quantum heat engine is built on the level degeneracy produced by inserting a barrier into a positive "
                 "oscillator-shaped well. From the position-dependent energy eigenvalues, the work and efficiency of a Stirling-like "
                 "cycle are computed as functions of angular frequency, well width and temperature.",
        facts=[("Research question", "How do level degeneracy, angular frequency, well width and temperature determine the work and efficiency of a quantum heat engine?"),
               ("Methods", "Quantised spectra of semi-infinite and infinite oscillator-shaped wells with position-dependent mass; work and efficiency of the Stirling-like cycle evaluated analytically and numerically."),
               ("Results", "The cycle delivers positive work in both cases. In the semi-infinite well, work and efficiency depend only on the angular frequency; in the infinite well, also on its width. Both approach the classical limit at large angular frequency and the Carnot limit at low temperature."),
               ("Publication", "Y. Evkaya, Ö. Ökcü and E. Aydiner, Int. J. Theor. Phys. 62, 237 (2023).")],
        tags=["Quantum thermodynamics", "Szilard engine", "Position-dependent mass", "Analytical and numerical modelling"],
        actions='<a class="button button-dialog" href="https://doi.org/10.1007/s10773-023-05498-3" target="_blank" rel="noopener">Journal article <span aria-hidden="true">↗</span></a>',
        schem=plates.fig8()),
    "bsc": dict(meta=("B.Sc. thesis · İstanbul University", "2023—2024"),
        title="Quantum Entanglement in the Non-Hermitian Frustrated Triangular Lattice",
        abstract="The thesis treats non-Hermitian XY and XX frustrated, dimerised, quasi-one-dimensional spin chains in a transverse "
                 "complex field and shows that they can be solved exactly through a fermionic mapping. Thermal and ground-state "
                 "entanglement entropies follow from the resulting spectra.",
        facts=[("Research question", "How do frustration, non-Hermiticity, dimerisation, temperature and field shape the entanglement of XY and XX spin chains?"),
               ("Methods", "Jordan–Wigner fermionisation followed by Fourier and Bogoliubov transformations; thermal entanglement from the free energy and ground-state von Neumann entropy from stationary-state conditions in the long-time limit."),
               ("Results", "Both non-Hermitian models are solved exactly. Their entanglement reaches the classical limit, ln 2, at high temperature and weak field."),
               ("Supervision", "Prof. Dr. Ekrem Aydıner, İstanbul University.")],
        tags=["Non-Hermitian physics", "Frustrated spin chains", "Quantum entanglement", "Exact solution"],
        actions='<p class="dialog-note">Full text available on request.</p>',
        schem=plates.fig9()),
    "muon": dict(meta=("Experimental project · İstanbul University", "2020—2022"),
        title="Cosmic-Muon Scintillation Detector",
        abstract="A plastic-scintillator detector with photomultiplier readout makes naturally occurring cosmic muons observable: "
                 "each transit is recorded as a voltage pulse on an oscilloscope and converted into sound by an LM555 "
                 "voltage-to-frequency circuit.",
        facts=[("Objective", "Make naturally occurring cosmic-muon events directly observable, both electronically and acoustically."),
               ("Methods", "Plastic scintillator and photomultiplier operated at 800 V, LEMO readout on an oscilloscope, and an LM555-based voltage-to-frequency converter driving a speaker."),
               ("Outcome", "Muon pulses were recorded in the time–voltage domain and translated into audible events in the time–frequency domain."),
               ("Supervision", "Prof. Dr. Suat Özkorucuklu, İstanbul University.")],
        tags=["Particle detection", "Scintillation", "Photomultiplier readout", "Signal electronics"],
        actions='<p class="dialog-note">Full text available on request.</p>',
        schem=plates.fig10()),
}

def template(key, p):
    facts = "".join(f"<div><dt>{html.escape(dt)}</dt><dd>{html.escape(dd)}</dd></div>" for dt, dd in p["facts"])
    tags = "".join(f"<span>{html.escape(t)}</span>" for t in p["tags"])
    return f'''      <template id="project-{key}">
        <article class="dialog-project area section section-dark">
          <div class="shell area-grid">
            <div class="dialog-copy area-copy">
              <div class="project-meta"><span>{p["meta"][0]}</span><span>{p["meta"][1]}</span></div>
              <h2 id="project-dialog-title">{p["title"]}</h2>
              <p class="dialog-abstract">{p["abstract"]}</p>
              <dl class="project-facts">{facts}</dl>
              <div class="tags">{tags}</div>
              <div class="dialog-actions">{p["actions"]}</div>
            </div>
            {p["schem"]}
          </div>
        </article>
      </template>
'''

def splice(site_dir):
    p = os.path.join(site_dir, "index.html")
    h = open(p, encoding="utf-8").read()
    for k, pr in projects.items():
        h, n = re.subn(r'[ \t]*<template id="project-%s">.*?</template>\n?' % k, lambda m: template(k, pr), h, count=1, flags=re.S)
        assert n == 1, k
    open(p, "w", encoding="utf-8").write(h)

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    site = os.path.join(here, "..") if os.path.exists(os.path.join(here, "..", "index.html")) else os.path.join(here, "..", "Portfolio")
    splice(site)
    plates.splice_cards(site)
    print("project templates and card thumbnails spliced:", ", ".join(projects))
