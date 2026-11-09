document.documentElement.classList.add('js');

const header = document.querySelector('[data-header]');
const progress = document.querySelector('.page-progress span');
const menuButton = document.querySelector('.menu-toggle');
const siteNav = document.querySelector('.site-nav');
const navLinks = document.querySelectorAll('.site-nav a');
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ---------- Header, progress bar, mobile menu ---------- */
const updateScrollState = () => {
  const y = window.scrollY;
  const height = document.documentElement.scrollHeight - window.innerHeight;
  header?.classList.toggle('scrolled', y > 24);
  if (progress) progress.style.width = `${height > 0 ? (y / height) * 100 : 0}%`;
};

window.addEventListener('scroll', updateScrollState, { passive: true });
updateScrollState();

menuButton?.addEventListener('click', () => {
  const open = document.body.classList.toggle('menu-open');
  menuButton.setAttribute('aria-expanded', String(open));
});

const closeMenu = () => {
  document.body.classList.remove('menu-open');
  menuButton?.setAttribute('aria-expanded', 'false');
};

navLinks.forEach((link) => link.addEventListener('click', closeMenu));
siteNav?.addEventListener('click', (event) => {
  if (event.target.closest('a')) closeMenu();
});
window.addEventListener('hashchange', closeMenu);

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') closeMenu();
});

/* ---------- Dialogs: one layer for projects, profile areas and contact ---------- */
let lastDialogTrigger = null;

const openDialog = (dialog, trigger) => {
  if (!dialog || typeof dialog.showModal !== 'function' || dialog.open) return false;
  lastDialogTrigger = trigger || null;
  document.body.classList.add('dialog-open');
  dialog.showModal();
  return true;
};

document.querySelectorAll('dialog').forEach((dialog) => {
  dialog.querySelector('[data-dialog-close]')?.addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', (event) => {
    if (event.target === dialog) dialog.close();
  });
  dialog.addEventListener('close', () => {
    if (!document.querySelector('dialog[open]')) document.body.classList.remove('dialog-open');
    const trigger = lastDialogTrigger;
    lastDialogTrigger = null;
    if (trigger && trigger.isConnected && trigger.offsetParent !== null) trigger.focus();
  });
});

// Fill a dialog from a <template>; cloned content is shown at once (no scroll-reveal inside dialogs).
const fillFromTemplate = (dialog, content, templateId) => {
  const template = document.getElementById(templateId);
  if (!dialog || !content || !template) return false;
  const fragment = template.content.cloneNode(true);
  fragment.querySelectorAll('.reveal').forEach((node) => node.classList.add('visible'));
  content.replaceChildren(fragment);
  const heading = content.querySelector('h2[id]');
  if (heading) dialog.setAttribute('aria-labelledby', heading.id);
  dialog.scrollTop = 0;
  return true;
};

const projectDialog = document.querySelector('#project-dialog');
const projectDialogContent = document.querySelector('#project-dialog-content');
const openProject = (key, trigger) => {
  if (fillFromTemplate(projectDialog, projectDialogContent, `project-${key}`)) openDialog(projectDialog, trigger);
};
document.querySelectorAll('[data-project]').forEach((trigger) => {
  trigger.addEventListener('click', () => openProject(trigger.dataset.project, trigger));
});
document.querySelectorAll('[data-open-project]').forEach((trigger) => {
  trigger.addEventListener('click', (event) => {
    event.preventDefault();
    location.hash = '#work';
    setTimeout(() => openProject(trigger.dataset.openProject, trigger), 350);
  });
});

const profileDialog = document.querySelector('#profile-dialog');
const profileDialogContent = document.querySelector('#profile-dialog-content');
const openProfileArea = (key, trigger) => {
  if (fillFromTemplate(profileDialog, profileDialogContent, `profile-${key}`)) openDialog(profileDialog, trigger);
};
document.querySelectorAll('[data-profile]').forEach((trigger) => {
  trigger.addEventListener('click', () => openProfileArea(trigger.dataset.profile, trigger));
});

const contactDialog = document.querySelector('#contact-dialog');
document.querySelectorAll('[data-contact]').forEach((trigger) => {
  trigger.addEventListener('click', (event) => {
    if (openDialog(contactDialog, trigger)) event.preventDefault();
  });
});

/* ---------- Views: the hero is the landing; #profile / #work replace it like separate pages ---------- */
const views = Array.from(document.querySelectorAll('[data-view]'));

const scrollToWithOffset = (el, behavior) => {
  const top = el.getBoundingClientRect().top + window.scrollY - 84;
  window.scrollTo({ top: Math.max(top, 0), behavior });
};

// Deep links to the profile areas open the profile branch and the matching dialog.
const profileAreaByHash = {
  'theoretical-profile': 'theory',
  'computational-profile': 'computation',
  'ai-augmented-research': 'ai',
  'industrial-interests': 'industry'
};

const currentView = () => (document.body.dataset.view && document.body.dataset.view !== 'home' ? document.body.dataset.view : null);

const route = (scroll) => {
  const hash = decodeURIComponent(location.hash.replace('#', ''));
  let activeView = null;
  let target = null;
  let openArea = null;
  let openContact = false;

  if (hash === 'contact') {
    activeView = currentView();
    openContact = true;
  } else if (profileAreaByHash[hash]) {
    activeView = 'profile';
    openArea = profileAreaByHash[hash];
  } else if (hash && hash !== 'top' && hash !== 'explore') {
    const el = document.getElementById(hash);
    if (el) {
      target = el;
      const owner = el.closest('[data-view]');
      if (owner) activeView = owner.dataset.view;
    }
  }

  views.forEach((view) => view.classList.toggle('is-active', view.dataset.view === activeView));
  document.body.dataset.view = activeView || 'home';
  navLinks.forEach((link) => {
    const name = link.getAttribute('href').replace('#', '');
    if (name === activeView) link.setAttribute('aria-current', 'page');
    else link.removeAttribute('aria-current');
  });

  if (openArea) openProfileArea(openArea, null);
  if (openContact) openDialog(contactDialog, null);
  if (!scroll || openContact) return;

  const behavior = reduceMotion ? 'auto' : 'smooth';
  const opensBranchTop = target && activeView && target.previousElementSibling?.classList.contains('view-bar');
  if (target && !opensBranchTop) {
    requestAnimationFrame(() => scrollToWithOffset(target, behavior));
  } else {
    window.scrollTo({ top: 0, behavior: 'auto' });
  }
};

window.addEventListener('hashchange', () => route(true));
route(Boolean(location.hash));
// The browser applies its own fragment scroll after load; re-apply ours so a branch opens at its top.
if (location.hash) window.addEventListener('load', () => route(true), { once: true });

/* ---------- Scroll reveal ---------- */
const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        revealObserver.unobserve(entry.target);
      }
    });
  },
  { rootMargin: '0px 0px -7% 0px', threshold: 0.08 }
);

document.querySelectorAll('.reveal').forEach((node) => revealObserver.observe(node));
const yearNode = document.querySelector('[data-year]');
if (yearNode) yearNode.textContent = new Date().getFullYear();

/* ---------- Contact address (assembled client-side to keep it out of harvester lists) ---------- */
document.querySelectorAll('[data-mail][data-host]').forEach((a) => {
  const address = `${a.dataset.mail}@${a.dataset.host}`;
  a.href = `mailto:${address}`;
  const label = a.querySelector('[data-mail-text]');
  if (label) label.textContent = address;
});

/* ---------- Hero lattice canvas ---------- */
const canvas = document.querySelector('.lattice-canvas');

if (canvas && !reduceMotion) {
  // The lattice is static, so it is rendered once per resize into the (hidden) canvas and shown as an image: a
  // cached bitmap the compositor never has to re-upload, unlike a live canvas layer. The drifting particles are a
  // dozen small dots whose walks along the lattice edges are computed once per resize and handed to the browser as
  // Web Animations of transform and opacity. These run on the compositor thread: the main thread does no work per
  // frame and the page is never re-layered or re-painted while the dots move, so the figures keep the frame budget.
  const base = canvas.getContext('2d');
  const image = document.createElement('img');
  image.className = 'lattice-canvas';
  image.alt = '';
  image.decoding = 'async';
  image.setAttribute('aria-hidden', 'true');
  canvas.after(image);
  canvas.style.display = 'none';
  const layer = document.createElement('div');
  layer.className = 'lattice-dots';
  layer.setAttribute('aria-hidden', 'true');
  image.after(layer);
  let width = 0;
  let height = 0;
  let onScreen = true;
  let fadeMask = false;
  let dotOpacity = 1;
  let imageUrl = '';
  let resizeTimer = 0;
  const nodes = [];
  const particles = [];

  const computeNeighbours = () => {
    const max = width < 700 ? 100 : 126;
    nodes.forEach((node) => {
      node.neighbours = nodes
        .filter((other) => other !== node && Math.hypot(other.x - node.x, other.y - node.y) < max)
        .slice(0, 3);
    });
  };

  // Particles follow the image's CSS mask: full strength up to 42% of the width, 18% beyond 60%.
  const fade = (x) => {
    if (!fadeMask) return 1;
    const f = x / width;
    return f <= 0.42 ? 1 : f >= 0.6 ? 0.18 : 1 - (0.82 * (f - 0.42)) / 0.18;
  };

  // A random walk along the drawn edges that never turns straight back; the animation runs it forth and back.
  const walk = (adjacency, start, steps) => {
    const path = [start];
    let previous = -1;
    let current = start;
    for (let s = 0; s < steps; s += 1) {
      const onward = adjacency[current].filter((n) => n !== previous);
      const pool = onward.length ? onward : adjacency[current];
      if (!pool.length) break;
      const next = pool[Math.floor(Math.random() * pool.length)];
      path.push(next);
      previous = current;
      current = next;
    }
    return path;
  };

  const animateParticles = () => {
    particles.forEach((particle) => particle.animation?.cancel());
    if (typeof layer.animate !== 'function') return;
    const index = new Map(nodes.map((node, i) => [node, i]));
    const adjacency = nodes.map(() => []);
    nodes.forEach((node, i) => {
      node.neighbours.forEach((other) => {
        const j = index.get(other);
        if (!adjacency[i].includes(j)) adjacency[i].push(j);
        if (!adjacency[j].includes(i)) adjacency[j].push(i);
      });
    });
    const inside = [];
    nodes.forEach((node, i) => {
      if (node.x >= 0 && node.x <= width && node.y >= 0 && node.y <= height) inside.push(i);
    });
    if (!inside.length) return;
    particles.forEach((particle) => {
      const path = walk(adjacency, inside[Math.floor(Math.random() * inside.length)], 14);
      const lengths = [0];
      for (let k = 1; k < path.length; k += 1) {
        const a = nodes[path[k - 1]];
        const b = nodes[path[k]];
        lengths.push(lengths[k - 1] + Math.hypot(b.x - a.x, b.y - a.y));
      }
      const total = lengths[lengths.length - 1];
      if (!total) return;
      const keyframes = path.map((i, k) => ({
        offset: lengths[k] / total,
        transform: `translate3d(${nodes[i].x.toFixed(1)}px, ${nodes[i].y.toFixed(1)}px, 0)`,
        opacity: dotOpacity * fade(nodes[i].x),
      }));
      const duration = (total / (10 + Math.random() * 16)) * 1000;   // 10 to 26 px per second
      particle.animation = particle.dot.animate(keyframes, { duration, iterations: Infinity, direction: 'alternate', easing: 'linear' });
      particle.animation.currentTime = Math.random() * 2 * duration;
      if (!onScreen) particle.animation.pause();
    });
  };

  const resize = () => {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    width = image.clientWidth;
    height = image.clientHeight;
    if (!width || !height) return;
    canvas.width = Math.round(width * dpr);
    canvas.height = Math.round(height * dpr);
    base.setTransform(dpr, 0, 0, dpr, 0, 0);
    const cs = getComputedStyle(image);
    fadeMask = (cs.maskImage || cs.webkitMaskImage || 'none') !== 'none';
    // The image's opacity is folded into each dot: group opacity on the layer would force the compositor to redraw
    // an offscreen surface the size of the hero on every frame.
    dotOpacity = parseFloat(cs.opacity) || 1;
    nodes.length = 0;

    const spacingX = width < 700 ? 88 : 112;
    const spacingY = spacingX * 0.86;
    for (let row = -1; row < height / spacingY + 2; row += 1) {
      for (let col = -1; col < width / spacingX + 2; col += 1) {
        const offset = row % 2 === 0 ? 0 : spacingX / 2;
        nodes.push({ x: col * spacingX + offset, y: row * spacingY });
      }
    }
    computeNeighbours();

    base.clearRect(0, 0, width, height);
    base.lineWidth = 0.6;
    base.strokeStyle = 'rgba(85, 203, 200, 0.16)';
    nodes.forEach((node) => {
      node.neighbours.forEach((other) => {
        base.beginPath();
        base.moveTo(node.x, node.y);
        base.lineTo(other.x, other.y);
        base.stroke();
      });
    });
    base.fillStyle = 'rgba(121, 227, 225, 0.35)';
    base.beginPath();
    nodes.forEach((node) => {
      base.moveTo(node.x + 1.1, node.y);
      base.arc(node.x, node.y, 1.1, 0, Math.PI * 2);
    });
    base.fill();
    canvas.toBlob((blob) => {
      if (!blob) return;
      if (imageUrl) URL.revokeObjectURL(imageUrl);
      imageUrl = URL.createObjectURL(blob);
      image.src = imageUrl;
    });

    const count = Math.round(Math.max(7, width / 180));
    while (particles.length < count) {
      const dot = document.createElement('span');
      layer.appendChild(dot);
      particles.push({ dot, animation: null });
    }
    while (particles.length > count) {
      const particle = particles.pop();
      particle.animation?.cancel();
      particle.dot.remove();
    }
    animateParticles();
  };

  // The hero is display:none while a branch is open; it has no size then, so re-measure on return.
  const resizeIfVisible = () => {
    if (image.clientWidth > 0 && image.clientWidth !== width) resize();
  };

  resize();
  // Pause the dots while the hero is scrolled out of view.
  if ('IntersectionObserver' in window) {
    new IntersectionObserver((entries) => {
      entries.forEach((entry) => { onScreen = entry.isIntersecting; });
      resizeIfVisible();
      particles.forEach((particle) => {
        if (!particle.animation) return;
        if (onScreen) particle.animation.play();
        else particle.animation.pause();
      });
    }).observe(image);
  }
  window.addEventListener('resize', () => { clearTimeout(resizeTimer); resizeTimer = setTimeout(resize, 120); }, { passive: true });
  window.addEventListener('hashchange', () => requestAnimationFrame(resizeIfVisible));
}

/* ---------- Fig. 2: the worldsheet sags into the bulk (one quiet 10 s loop) ---------- */
(() => {
  const svg = document.querySelector('svg.ads-svg');
  if (!svg) return;
  const $ = (id) => svg.querySelector('#' + id);
  const clipF = $('ads-clip-fr'), clipB = $('ads-clip-br'), slice = $('ads-slice'), contour = $('ads-contour'),
        zdot = $('ads-zdot'), result = $('ads-result'), sheetF = $('ads-sheet-f'), sheetB = $('ads-sheet-b'), btn = $('ads-play');
  if (!clipF || !clipB || !slice || !contour || !zdot || !result) return;
  // projection of the drawing: (x, y, z) -> (302 + 174x + 52y, 138 - 46y + 166z); the loop has R = 1
  const OX = 302, OY = 138, RZ = 166, T = 10000;
  const ease = (u) => 0.5 - 0.5 * Math.cos(Math.PI * Math.min(1, Math.max(0, u)));
  const slicePath = (z) => {
    const rho = Math.sqrt(Math.max(0, 1 - z * z)); let d = '';
    for (let i = 0; i <= 48; i++) {
      const a = (i / 48) * 2 * Math.PI, x = rho * Math.cos(a), y = rho * Math.sin(a);
      d += (i ? 'L' : 'M') + (OX + 174 * x + 52 * y).toFixed(2) + ' ' + (OY - 46 * y + RZ * z).toFixed(2);
    }
    return d + 'Z';
  };
  const setDepth = (z) => {              // reveal the surface down to depth z (front and back rims separately)
    const rho = Math.sqrt(Math.max(0, 1 - z * z));
    clipF.setAttribute('height', (OY + RZ * z + 46 * rho + 2).toFixed(1));
    clipB.setAttribute('height', (OY + RZ * z - 46 * rho + 2).toFixed(1));
    zdot.setAttribute('cy', (92 + RZ * z).toFixed(1));
    slice.setAttribute('d', z > 0.015 && z < 0.985 ? slicePath(z) : '');
  };
  const render = (t) => {                // t in [0, T)
    // A: 0–2.2 s the contour is drawn
    contour.style.strokeDasharray = '1';
    contour.style.strokeDashoffset = (1 - ease(t / 2200)).toFixed(4);
    // B: 2.2–7.0 s the sheet sags into the bulk (hidden during A, faded in as it starts)
    if (t < 2200) { clipF.setAttribute('height', '0'); clipB.setAttribute('height', '0'); slice.setAttribute('d', ''); zdot.setAttribute('cy', '92'); }
    else setDepth(ease((t - 2200) / 4800));
    // C: 7.0–8.2 s the result appears; 9.3–10 s everything but the loop fades for the restart
    const out = t > 9300 ? 1 - (t - 9300) / 700 : 1;
    sheetF.style.opacity = sheetB.style.opacity = (Math.min(1, Math.max(0, (t - 2200) / 700)) * out).toFixed(3);
    result.style.fillOpacity = (ease((t - 7000) / 1200) * out).toFixed(3);
    if (t > 9300) { contour.style.strokeDashoffset = ((t - 9300) / 700).toFixed(4); slice.setAttribute('d', ''); }
  };
  const finalState = () => {             // the completed picture, for reduced motion and for the paused state
    contour.style.strokeDasharray = ''; contour.style.strokeDashoffset = '';
    sheetF.style.opacity = sheetB.style.opacity = '1';
    clipF.setAttribute('height', '400'); clipB.setAttribute('height', '400');
    slice.setAttribute('d', ''); zdot.setAttribute('cy', (92 + RZ).toFixed(1));
    result.style.fillOpacity = '1';
  };

  let playing = true, visible = true, raf = 0, start = null, elapsed = 0;   // autoplays; the ▶/⏸ control is the opt-out
  const setPlaying = (p) => {
    playing = p; start = null;
    svg.classList.toggle('ads-playing', p);
    if (btn) btn.setAttribute('aria-label', p ? 'Pause the animation' : 'Play the animation');
    if (p) run();
  };
  const frame = (now) => {
    raf = 0;
    if (!visible || !playing) return;
    if (start === null) start = now - elapsed;
    elapsed = (now - start) % T; if (now - start >= T) start = now - elapsed;
    render(elapsed);
    raf = requestAnimationFrame(frame);
  };
  const run = () => { if (!raf && visible && playing) raf = requestAnimationFrame(frame); };
  if (btn) {
    const toggle = () => setPlaying(!playing);
    btn.addEventListener('click', toggle);
    btn.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(); } });
  }
  if ('IntersectionObserver' in window) {
    new IntersectionObserver((es) => { es.forEach((e) => { visible = e.isIntersecting; }); if (visible) { start = null; run(); } }, { threshold: 0.15 }).observe(svg);
  }
  document.addEventListener('visibilitychange', () => { if (!document.hidden) { start = null; run(); } });
  if (reduceMotion && !svg.closest('.hero')) { finalState(); setPlaying(false); } else setPlaying(true);
})();

/* ---------- Home: scale the figure plates so the landing fits one screen on desktop ---------- */
(() => {
  const vis = document.querySelector('.hero-theory-visual');
  if (!vis) return;
  const apply = (z) => {
    if (z >= 0.999) { vis.style.transform = ''; vis.style.marginBottom = ''; return; }
    vis.style.transform = 'scale(' + z.toFixed(4) + ')';
    vis.style.marginBottom = (-vis.offsetHeight * (1 - z)).toFixed(1) + 'px';
  };
  const fit = () => {
    apply(1);
    if (document.body.dataset.view !== 'home' || innerWidth < 821 || innerHeight < 640) return;
    let z = 1;
    for (let i = 0; i < 8; i++) {
      const over = document.documentElement.scrollHeight - innerHeight;
      if (over <= 0) break;
      const h = vis.offsetHeight * z;            // rendered height of the plates
      z = Math.max(0.3, z * (h - over - 4) / h);
      apply(z);
    }
  };
  addEventListener('resize', fit);
  addEventListener('hashchange', () => setTimeout(fit, 50));
  addEventListener('load', () => { fit(); [250, 800, 1600].forEach((ms) => setTimeout(fit, ms)); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
  fit();
})();
