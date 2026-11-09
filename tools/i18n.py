"""Build the Turkish and German pages (tr/index.html, de/index.html) from the English index.html.

The English page is the source of truth; its text units (block leaves such as <p>, <h2>, <li>, <dt>, <dd>, the
<title>, visible inline text, and a fixed set of attributes) are extracted verbatim with their inline markup and
looked up in tools/i18n/strings.<lang>.json. Inline SVG figures, <script> and <style> are never touched: figure
lettering stays English, as in a published paper. Units without a translation are left in English and listed.

  python3 tools/i18n.py extract   → writes tools/i18n/strings.en.json (the keys to translate; values = keys)
  python3 tools/i18n.py build     → writes tr/index.html and de/index.html, patches hreflang into index.html
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = next(p for p in (os.path.join(HERE, ".."), os.path.join(HERE, "..", "Portfolio")) if os.path.exists(os.path.join(p, "index.html")))
SITE = os.path.abspath(SITE)
I18N = os.path.join(HERE, "i18n")
LANGS = {"tr": "Türkçe", "de": "Deutsch"}
BASE = "https://yevkaya.com"

LEAF = {"p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "dt", "dd", "title", "figcaption", "label", "button", "th", "td", "summary", "legend", "option"}
BLOCK = LEAF | {"div", "section", "ul", "ol", "dl", "figure", "header", "footer", "nav", "table", "tr", "thead", "tbody", "dialog", "article", "aside", "svg", "canvas", "form", "main", "body", "html", "head", "blockquote", "details", "picture"}
SKIP = {"script", "style", "svg", "noscript", "canvas"}
VOID = {"br", "img", "meta", "link", "input", "hr", "source", "wbr", "area", "base", "col", "embed", "param", "track"}
ATTRS = {"aria-label", "alt", "title", "placeholder"}
TOKEN = re.compile(r"<!--.*?-->|<[^>]+>|[^<]+", re.S)
TAG = re.compile(r"<(/?)([a-zA-Z][\w:-]*)")


def tokenize(html):
    """yield (kind, start, end, name) with kind in open/close/void/text/comment."""
    for m in TOKEN.finditer(html):
        t = m.group(0)
        if t.startswith("<!--"):
            yield "comment", m.start(), m.end(), None
        elif t.startswith("<"):
            if t.startswith("<!") or t.startswith("<?"):
                yield "comment", m.start(), m.end(), None; continue
            tm = TAG.match(t); name = tm.group(2).lower()
            if tm.group(1): yield "close", m.start(), m.end(), name
            elif name in VOID or t.endswith("/>"): yield "void", m.start(), m.end(), name
            else: yield "open", m.start(), m.end(), name
        else:
            yield "text", m.start(), m.end(), None


def units(html):
    """Return a list of (start, end) spans of inner HTML that form translation units, outermost-leaf first."""
    toks = list(tokenize(html))
    # element tree as (name, open_tok_idx, close_tok_idx)
    stack, elems = [], []
    for i, (k, s, e, n) in enumerate(toks):
        if k == "open": stack.append((n, i))
        elif k == "close":
            for j in range(len(stack) - 1, -1, -1):
                if stack[j][0] == n:
                    elems.append((n, stack[j][1], i)); del stack[j:]; break
    elems.sort(key=lambda x: x[1])
    def inner(el):
        return toks[el[1]][2], toks[el[2]][1]
    def has_block_child(el):
        depth = 0
        for k, s, e, n in toks[el[1] + 1: el[2]]:
            if k == "open":
                if depth == 0 and n in BLOCK: return True
                depth += 1
            elif k == "close": depth -= 1
            elif k == "void" and n in BLOCK and depth == 0: return True
        return False
    def is_skip_el(el):
        return el[0] in SKIP or 'class="lang-switch"' in html[toks[el[1]][1]:toks[el[1]][2]]
    def in_skip(el):
        for other in elems:
            if is_skip_el(other) and other[1] <= el[1] and other[2] >= el[2]: return True
        return False
    spans = []
    for el in elems:
        if el[0] in LEAF and not in_skip(el) and not has_block_child(el):
            s, e = inner(el)
            if re.search(r"[A-Za-z]", html[s:e]): spans.append((s, e))
    # pass 2: stray text inside inline containers (nav links, spans, buttons' spans) not covered yet
    covered = lambda s, e: any(a <= s and e <= b for a, b in spans)
    for i, (k, s, e, n) in enumerate(toks):
        if k != "text" or not re.search(r"[A-Za-z]", html[s:e]) or covered(s, e): continue
        # parent element: innermost elem containing this token
        parents = [el for el in elems if el[1] < i < el[2]]
        if not parents: continue
        par = max(parents, key=lambda el: el[1])
        if any(is_skip_el(el) for el in parents): continue
        if par[0] not in BLOCK and not has_block_child(par):
            a, b = inner(par)
            if not covered(a, b): spans.append((a, b))
        else:
            spans.append((s, e))
    spans = sorted(set(spans))
    # drop spans nested inside other spans
    out = []
    for s, e in spans:
        if out and s >= out[-1][0] and e <= out[-1][1]: continue
        out.append((s, e))
    return out


def attr_units(html):
    out = []
    for m in re.finditer(r'\s(aria-label|alt|title|placeholder)="([^"]*)"', html):
        if re.search(r"[A-Za-z]", m.group(2)) and m.group(2) not in ("Language", "Dil", "Sprache"): out.append((m.start(2), m.end(2)))
    for m in re.finditer(r'<meta\s+(?:name="description"|property="og:(?:title|description)")\s+content="([^"]*)"', html, re.S):
        out.append((m.start(1), m.end(1)))
    for m in re.finditer(r'<meta\s+(?:name="description"|property="og:(?:title|description)")\s+content="([^"]*)"', html.replace("\n", " "), re.S):
        pass
    return out


TIME = re.compile(r'<time data-updated datetime="\d{4}-\d{2}-\d{2}">[^<]*</time>')


def norm(s):
    return TIME.sub("<time/>", re.sub(r"\s+", " ", s)).strip()


def all_units(html):
    spans = units(html) + attr_units(html)
    spans = sorted(set(spans))
    return spans


def extract():
    html = open(os.path.join(SITE, "index.html"), encoding="utf-8").read()
    keys = []
    for s, e in all_units(html):
        k = norm(html[s:e])
        if k and k not in keys: keys.append(k)
    os.makedirs(I18N, exist_ok=True)
    json.dump({k: k for k in keys}, open(os.path.join(I18N, "strings.en.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(keys), "units →", os.path.join(I18N, "strings.en.json"))


def switcher(cur):
    """relative links so the pages work at the site root and in a sub-path preview alike"""
    items = []
    up = "" if cur == "en" else "../"
    for code, href in (("en", up or "./"), ("tr", up + "tr/"), ("de", up + "de/")):
        cls = ' aria-current="page"' if code == cur else ""
        items.append(f'<a href="{href}" lang="{code}" hreflang="{code}"{cls}>{code.upper()}</a>')
    label = {"en": "Language", "tr": "Dil", "de": "Sprache"}[cur]
    return f'<div class="lang-switch" aria-label="{label}">' + "".join(items) + "</div>"


def hreflang_block():
    return ('    <link rel="alternate" hreflang="en" href="https://yevkaya.com/" />\n'
            '    <link rel="alternate" hreflang="tr" href="https://yevkaya.com/tr/" />\n'
            '    <link rel="alternate" hreflang="de" href="https://yevkaya.com/de/" />\n'
            '    <link rel="alternate" hreflang="x-default" href="https://yevkaya.com/" />\n')


def relativise(html):
    """asset paths for a page one directory below the root"""
    return re.sub(r'(href|src)="(assets/|styles\.css|script\.js)', r'\1="../\2', html)


def patch_common(html, lang):
    html = re.sub(r'[ \t]*<link rel="alternate" hreflang="[^"]*" href="[^"]*" />\n', "", html)
    html = html.replace('    <link rel="canonical"', hreflang_block() + '    <link rel="canonical"', 1)
    html = re.sub(r'\n[ \t]*<div class="lang-switch"[^>]*>.*?</div>', "", html, flags=re.S)
    html = re.sub(r'(<nav id="site-nav"[^>]*>.*?)(\n[ \t]*</nav>)', lambda m: m.group(1) + "\n        " + switcher(lang) + m.group(2), html, count=1, flags=re.S)
    return html


def build():
    src = open(os.path.join(SITE, "index.html"), encoding="utf-8").read()
    # the English page: absolute paths, hreflang, switcher
    en = patch_common(src, "en")
    if en != src:
        open(os.path.join(SITE, "index.html"), "w", encoding="utf-8").write(en)
        print("index.html: hreflang + language switch patched")
    src = en
    for lang, label in LANGS.items():
        d = load_dict(lang)
        html = src; missing = []
        for s, e in sorted(all_units(src), reverse=True):
            k = norm(src[s:e])
            if k in d and d[k]:
                rep = d[k]
                if "<time/>" in rep:
                    t = TIME.search(src[s:e]); rep = rep.replace("<time/>", t.group(0) if t else "")
                html = html[:s] + rep + html[e:]
            elif k in d:
                pass  # explicitly kept in English (names, formulae, citations)
            else:
                missing.append(k)
        html = relativise(html)
        html = html.replace('<html lang="en">', f'<html lang="{lang}">', 1)
        html = html.replace('<link rel="canonical" href="https://yevkaya.com/" />', f'<link rel="canonical" href="https://yevkaya.com/{lang}/" />')
        html = html.replace('<meta property="og:url" content="https://yevkaya.com/" />', f'<meta property="og:url" content="https://yevkaya.com/{lang}/" />')
        html = html.replace('<meta property="og:locale" content="en_US" />', "")
        html = html.replace('<meta property="og:type" content="website" />', '<meta property="og:type" content="website" />\n    <meta property="og:locale" content="%s" />' % {"tr": "tr_TR", "de": "de_DE"}[lang])
        html = re.sub(r'<div class="lang-switch"[^>]*>.*?</div>', switcher(lang), html, flags=re.S)
        # JSON-LD: translate the plain-string values that have entries
        def ld(m):
            body = m.group(1)
            for k, v in d.items():
                if "<" in k: continue
                body = body.replace(f'"{k}"', f'"{v}"')
            return m.group(0).replace(m.group(1), body)
        html = re.sub(r'<script type="application/ld\+json">(.*?)</script>', ld, html, flags=re.S)
        # footer month
        html = re.sub(r'(<time data-updated datetime="(\d{4})-(\d{2})-\d{2}">)[^<]*(</time>)', lambda m: m.group(1) + month(lang, int(m.group(3))) + " " + m.group(2) + m.group(4), html)
        out = os.path.join(SITE, lang); os.makedirs(out, exist_ok=True)
        open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(html)
        print(f"{lang}/index.html written; {len(missing)} units left in English")
        for k in missing: print("   ·", k[:110])


def load_dict(lang):
    """tools/i18n/<lang>.py holds translations indexed by position in strings.en.json (None = keep English);
    the merged English→translation dictionary is also written to strings.<lang>.json for reference."""
    import importlib.util
    en = list(json.load(open(os.path.join(I18N, "strings.en.json"), encoding="utf-8")))
    spec = importlib.util.spec_from_file_location(lang, os.path.join(I18N, f"{lang}.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    unknown = sorted(i for i in m.T if i >= len(en))
    if unknown: print(f"{lang}.py: indices beyond the English list ignored: {unknown}")
    d = {en[i]: (v if v is not None else en[i]) for i, v in m.T.items() if i < len(en)}
    d.update(getattr(m, "EXTRA", {}))
    json.dump(d, open(os.path.join(I18N, f"strings.{lang}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return d


def month(lang, m):
    names = {"tr": ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"],
             "de": ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]}
    return names[lang][m - 1]


if __name__ == "__main__":
    {"extract": extract, "build": build}[sys.argv[1]]()
