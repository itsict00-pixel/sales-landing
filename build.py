#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build.py — Assembla layout.html + blocks/ -> index.html (zero dipendenze).

Come aggiungere un WIDGET o un blocco TRA due blocchi:
  1) crea un file in blocks/ con un prefisso numerico che cada nel "buco" giusto.
     I blocchi del flusso principale sono numerati a passo 10:
        10-hero  20-problema  30-come-funziona  40-benefici
        50-testimonianze  60-offerta  70-faq  80-cta-finale
     Es.: per mettere un widget TRA benefici (40) e testimonianze (50)
          -> crea  blocks/45-mio-widget.html  (solo l'HTML del widget, senza wrapper)
  2) rilancia:  python3 build.py
  3) ricarica il browser.

header.html e footer.html sono il "chrome" fisso (fuori da <main>).
Per riordinare i blocchi: rinomina i prefissi numerici.
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BLOCKS = ROOT / "blocks"

# Stato del sito: True = PRIVATO/bozza (noindex,nofollow su ogni pagina + robots.txt Disallow).
# Metti False SOLO quando vuoi renderlo pubblico/indicizzabile, poi rilancia build.py.
DRAFT = True

def read(p: Path) -> str:
    return p.read_text(encoding="utf-8").strip()

def indent(html: str, pad: str = "    ") -> str:
    return "\n".join((pad + ln) if ln.strip() else ln for ln in html.splitlines())

layout = read(ROOT / "layout.html")
if DRAFT:  # inserisce il meta robots subito prima di </head> su OGNI pagina generata
    layout = layout.replace("</head>", '  <meta name="robots" content="noindex, nofollow" /></head>')
header = read(BLOCKS / "header.html") if (BLOCKS / "header.html").exists() else ""
footer = read(BLOCKS / "footer.html") if (BLOCKS / "footer.html").exists() else ""

# Flusso principale: tutti i file che iniziano con una cifra, in ordine alfabetico/numerico.
main_files = sorted(BLOCKS.glob("[0-9]*.html"))
blocks_html = "\n\n".join(indent(read(f)) for f in main_files)

out = layout
out = out.replace("<!-- @@HEADER@@ -->", header)
out = out.replace("    <!-- @@BLOCKS@@ -->", blocks_html)
out = out.replace("<!-- @@FOOTER@@ -->", footer)

banner = ("<!-- ============================================================\n"
          "     FILE GENERATO da build.py — NON modificare a mano.\n"
          "     Modifica i file in blocks/ (o layout.html) e rilancia: python3 build.py\n"
          "     ============================================================ -->\n")
(ROOT / "index.html").write_text(banner + out + "\n", encoding="utf-8")

print(f"OK -> index.html generato. Blocchi del flusso ({len(main_files)}):")
for f in main_files:
    print("   -", f.name)
print("   [header.html e footer.html montati come chrome fisso]")

# --- Export GoHighLevel: ogni blocco avvolto in .sl (paste-ready) + CSS unico ---
GHL = ROOT / "ghl"
GHL.mkdir(exist_ok=True)

# CSS combinato da incollare UNA volta nel Custom CSS di GHL
css = read(ROOT / "css" / "tokens.css") + "\n\n" + read(ROOT / "css" / "styles.css")
(GHL / "sl-styles.css").write_text(css + "\n", encoding="utf-8")

def wrap_sl(html: str) -> str:
    return '<div class="sl">\n' + indent(html, "  ") + '\n</div>\n'

export = []
if (BLOCKS / "header.html").exists():
    export.append(("header.html", BLOCKS / "header.html"))
export += [(f.name, f) for f in main_files]
if (BLOCKS / "footer.html").exists():
    export.append(("footer.html", BLOCKS / "footer.html"))

for name, path in export:
    (GHL / name).write_text(wrap_sl(read(path)), encoding="utf-8")

print(f"OK -> ghl/ aggiornato: sl-styles.css + {len(export)} blocchi GHL-ready.")

# --- Pagine extra: ogni sottocartella di pages/ = una pagina in più ---
# Stessa layout + stesso header/footer (così il footer è identico su TUTTE le pagine).
# Blocchi numerati come in blocks/. Output: <slug>.html + export in ghl/<slug>/.
PAGES = ROOT / "pages"
if PAGES.exists():
    for page_dir in sorted(p for p in PAGES.iterdir() if p.is_dir()):
        slug = page_dir.name
        pfiles = sorted(page_dir.glob("[0-9]*.html"))
        if not pfiles:
            continue
        pblocks = "\n\n".join(indent(read(f)) for f in pfiles)
        pout = layout
        pout = pout.replace("<!-- @@HEADER@@ -->", header)
        pout = pout.replace("    <!-- @@BLOCKS@@ -->", pblocks)
        pout = pout.replace("<!-- @@FOOTER@@ -->", footer)
        # titolo dedicato (semplice replace del placeholder del layout)
        pout = pout.replace("[BRAND] — [promessa principale in una riga]",
                            "[BRAND] — " + slug.replace("-", " ").title())
        (ROOT / f"{slug}.html").write_text(banner + pout + "\n", encoding="utf-8")
        print(f"OK -> {slug}.html generato ({len(pfiles)} blocchi).")
        gdir = GHL / slug
        gdir.mkdir(exist_ok=True)
        for f in pfiles:
            (gdir / f.name).write_text(wrap_sl(read(f)), encoding="utf-8")
        print(f"        + ghl/{slug}/ ({len(pfiles)} blocchi GHL-ready).")

# --- Bundle di DEPLOY: cartella statica auto-contenuta, pronta per QUALSIASI host ---
# (trascina questa cartella/zip su Netlify Drop, Cloudflare Pages, ecc. → URL permanente).
# È GENERATA: viene ricreata a ogni build. Contiene solo i file runtime (no sorgenti).
DEPLOY = ROOT / "deploy"
if DEPLOY.exists():
    shutil.rmtree(DEPLOY)
DEPLOY.mkdir()
pages_copied = 0
for html in sorted(ROOT.glob("*.html")):
    if html.name == "layout.html":
        continue
    shutil.copy2(html, DEPLOY / html.name)
    pages_copied += 1
for sub in ("css", "js", "assets"):
    src = ROOT / sub
    if src.exists():
        shutil.copytree(src, DEPLOY / sub)
nl = chr(10)
robots = "User-agent: *" + nl + ("Disallow: /" if DRAFT else "Allow: /") + nl
(DEPLOY / "robots.txt").write_text(robots, encoding="utf-8")
print(f"OK -> deploy/ pronto: {pages_copied} pagine + css/js/assets + robots.txt "
      f"({'PRIVATO/noindex' if DRAFT else 'PUBBLICO'}).")
