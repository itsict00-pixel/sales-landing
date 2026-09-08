# Sales Landing — [BRAND]

Landing page di vendita. Progetto statico (HTML + CSS a design-token, zero dipendenze).
Costruita insieme a Claude Code seguendo una pipeline a fasi.

## Come si guarda in locale
Non serve installare nulla. Apri `index.html` nel browser, **oppure** avvia un server statico:

```bash
# con Python (già presente sul Mac)
cd "sales-landing" && python3 -m http.server 4321
# poi apri http://localhost:4321
```

## Struttura (modulare a blocchi)
```
sales-landing/
├── layout.html         # scheletro pagina (head/body) coi segnaposto @@HEADER@@ @@BLOCKS@@ @@FOOTER@@
├── blocks/             # i pezzi del sito SENZA wrapper di pagina
│   ├── header.html     #   chrome fisso (nav)
│   ├── 10-hero.html    #   ↓ flusso principale, numerato a passo 10
│   ├── 20-problema.html
│   ├── 30-come-funziona.html
│   ├── 40-benefici.html
│   ├── 50-testimonianze.html
│   ├── 60-offerta.html
│   ├── 70-faq.html
│   ├── 80-cta-finale.html
│   └── footer.html     #   chrome fisso
├── build.py            # ricuce layout + blocks → index.html  (python3 build.py)
├── index.html          # GENERATO — non modificare a mano
├── css/
│   ├── tokens.css      # design token (FASE 4) — palette, font, spacing
│   └── styles.css      # stili e componenti (basati sui token)
├── js/main.js          # form accessibile + interazioni
├── assets/             # immagini, OG image, favicon (FASE 8)
├── copy/               # i testi reali, sezione per sezione (FASE 3)
└── docs/               # brief, strategia, direzione visiva (FASI 0-2)
```

## ✏️ Modificare il sito (workflow)
1. Apri il blocco giusto in `blocks/` e modificalo (è solo l'HTML della sezione, niente wrapper).
2. Rilancia la build: `python3 build.py`
3. Ricarica il browser.

## ➕ Aggiungere un WIDGET tra due blocchi
I blocchi sono numerati a passo 10 → c'è sempre spazio per infilarne uno in mezzo.
- Widget **tra Benefici (40) e Testimonianze (50)**? Crea `blocks/45-mio-widget.html`
  con dentro solo l'HTML del widget (un `<section>…</section>` o un embed), poi `python3 build.py`.
- Per **riordinare** i blocchi: rinomina i prefissi numerici.

## Pipeline (stato)
- [ ] **Fase 0** — Brief & posizionamento → `docs/brief.md`  ·  `/wearemarketers-posizionamento`, `/deep-research`
- [ ] **Fase 1** — Strategia & sezioni → `docs/strategy.md`  ·  `/nielsen-e-cro`
- [ ] **Fase 2** — Brand & identità → `docs/design-direction.md`  ·  `/frontend-design`, `/brand`, `/ui-ux-pro-max`
- [ ] **Fase 3** — Copywriting → `copy/`  ·  `/copywriting-ai`, `/psicologia-persuasione`
- [ ] **Fase 4** — Design system → `css/tokens.css`  ·  `/design-system`, `/ui-styling`
- [ ] **Fase 5** — Build UI → `index.html` + `css/styles.css`  ·  `/ui-styling`, `/frontend-design`
- [ ] **Fase 6** — CRO & usability → `/anthropic-skills:nielsen-e-cro`
- [ ] **Fase 7** — QA (a11y/perf/test) → `/ui-ux-pro-max`, `/testing-strategy`, `/code-review`
- [ ] **Fase 8** — Asset marketing → `assets/`  ·  `/banner-design`, `/design`
- [ ] **Fase 9** — Deploy & handoff → `/deploy-checklist`, `/documentation`

## Produzione (più avanti)
Per la build di produzione installeremo **Node.js** e migreremo ad **Astro + Tailwind**
(asset ottimizzati, immagini responsive, SEO). Lo scaffold statico attuale è il punto di partenza.
