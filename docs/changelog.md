# Changelog

Tutte le modifiche rilevanti al progetto sono documentate in questa pagina.
Il formato segue [Keep a Changelog](https://keepachangelog.com/it/1.0.0/).

---

## [2.1.0] — 2026-06-14

### Corretto

- **RecursionError / TemplateSyntaxError**: convertiti i commenti `{# … #}` multi-riga in `{% comment %} … {% endcomment %}` in `modal.html`, `masonry_grid.html` e `sidebar.html`. Django non supporta `{# #}` su più righe: i tag `{% %}` interni venivano valutati causando errori a runtime.
- Typo `descriptio n` → `description` in `pyproject.toml`.
- `feature_grid.html`: `col_class` spostato dalla colonna al `.row` con `row-cols-md-*` (pattern Bootstrap-idiomatic, compatibile con `<div class="col">` nei figli).
- `sidebar.html`: script JS inline estratto in `static/agesci_theme/js/sidebar.js` e caricato con `<script src defer>` per compatibilità CSP e caching.

### Modificato

- `.ag-scroll-area` introdotto come unico container con scroll verticale, sostituendo `overflow-y: auto` su `<main>`. Il footer è ora fratello di `<main>` all'interno di `.ag-scroll-area` e occupa tutta la larghezza (viewport − sidebar), indipendentemente dal `max-width` del `.container` di `<main>`.
- `ag-sidebar`: aggiunto `position: relative; z-index: 2` per sovrastare visivamente il footer quando si trovano in prossimità.
- Blocco `{% block breadcrumb %}` rimosso da `.ag-scroll-area`; la breadcrumb viene ora resa in `ag-header-bottom` di `header.html` quando `breadcrumb_items` è presente nel contesto (altrimenti mostra `header_search` / `header_actions` come fallback).

### Demo (`example_project`)

- Sidebar visibile nella home con link alla nuova pagina `/components/`.
- Nuova pagina `/components/` con tutti gli 11 componenti opzionali: Hero (4 varianti), Breadcrumb, Feature Grid, Jumbotron, Badge, Button, Dropdown, List group, Modal (sm/default/lg), Masonry Grid.
- `breadcrumb_items` passato da entrambe le view per mostrare la breadcrumb nell'header su ogni pagina.
- `mark_safe()` sui contenuti HTML del masonry grid per evitare escape indesiderato.

---

## [2.0.0] — 2026-06-13

### ⚠ Breaking changes

- `base.html` completamente riprogettato: i blocchi `navbar`, `nav_items`,
  `brand_url`, `brand_text`, `breadcrumb` e `subnav` **non esistono più**.
  Sostituiti dai nuovi blocchi dell'header a due barre (vedi sotto).
- `partials/navbar.html` rimosso → sostituito da `partials/header.html`.
- Footer ridisegnato: nuovi blocchi al posto delle sole tre colonne della v1.

### Aggiunto

**Header a due barre con offcanvas mobile**
- Barra superiore (`ag-header-top`): logo + voci di navigazione con icona
  sopra e testo sotto (stile Bootstrap "headers", ultimo esempio).
- Barra inferiore (`ag-header-bottom`): campo di ricerca opzionale + pulsanti
  azione.
- Su mobile/tablet: hamburger → pannello offcanvas Bootstrap.
- Nuovi blocchi: `header`, `brand_url`, `brand_text`, `header_nav`,
  `offcanvas_nav`, `header_search`, `header_actions`.

**Sidebar collapsible**
- Nuovo partial `partials/sidebar.html`: sidebar che si riduce a sole icone
  via toggle, stato salvato in `localStorage`.
- Varianti: `dark` (sfondo primario) e `light` (sfondo chiaro).
- Attivata sovrascrivendo il blocco `sidebar` in `base.html`; nessuna
  modifica al layout se il blocco rimane vuoto.
- Nuovo blocco: `sidebar_items`.

**Footer ridisegnato**
- Struttura con colonna logo, due colonne di link personalizzabili e
  riga copyright/link legali (stile Bootstrap "footers", primo esempio).
- Il blocco `footer_text` è **mantenuto** per compatibilità con chi già
  lo sovrascriveva dalla v1.
- Nuovi blocchi: `footer_brand_text`, `footer_columns`, `footer_col1_title`,
  `footer_col1_links`, `footer_col2_title`, `footer_col2_links`,
  `footer_copyright`.

**Componenti opzionali via templatetag**
- Nuovo modulo `{% load agesci_components %}` con 11 tag `inclusion_tag`:
  `ag_hero`, `ag_feature_card`, `ag_feature_grid`, `ag_jumbotron`,
  `ag_badge`, `ag_button`, `ag_breadcrumb`, `ag_dropdown`, `ag_list_group`,
  `ag_modal_trigger`, `ag_masonry_grid`.
- Template sovrascrivibili in `templates/agesci_theme/components/`.
- Supporto Masonry tramite CDN (istruzioni nel tag `ag_masonry_grid`).

**SCSS**
- Quattro nuovi partial: `_header.scss`, `_sidebar.scss`, `_footer.scss`,
  `_components.scss`.

---

## [1.2.4] — 2026-06-08

### Corretto
- `docs/conf.py`: versione letta dinamicamente da `pyproject.toml` via `tomllib` (non più hardcoded).
- `build.yml`: rimosso job publish duplicato (la pubblicazione è gestita da `publish.yml` su GitHub Release).

---

## [1.2.3] — 2026-06-08

### Modificato
- Layout mobile/tablet: breakpoint `body { height: 100vh }` e `main { overflow-y: auto }` alzato da md (768px) a lg (992px). Il footer ora scorre naturalmente con il contenuto su smartphone e tablet.
- `.footer-agesci`: padding ridotto da `2rem 0` a `0.5rem 0`.

---

## [1.2.2] — 2026-06-08

### Corretto
- Fix build PDF GitHub Actions: rimossi badge SVG da `index.md` (non supportati da rinohtype),
  aggiunto `rinoh_documents` in `conf.py`, rimosso `-W` dal comando sphinx-build.

---

## [1.2.1] — 2026-06-08

### Corretto
- Aggiunta dipendenza `Pillow>=10.0` in `docs/requirements.txt` (richiesta da rinohtype per la generazione PDF).

---

## [1.2.0] — 2026-06-08

### Aggiunto
- Suite di documentazione completa con Sphinx + MyST-Parser, pronta per ReadTheDocs.
- Generazione PDF automatica allegata a ogni release GitHub tramite GitHub Actions (`rinohtype`).
- `.readthedocs.yaml` con output PDF e HTMLzip abilitati.

### Corretto
- Layout mobile (< 768px): il footer ora segue il flusso normale del documento
  invece di rimanere incollato al bordo inferiore del viewport.

---

## [1.1.0] — 2025

### Aggiunto
- Layout a viewport fisso: `body { height: 100vh }` + `main { overflow-y: auto }`.
- Breadcrumb brandizzata (`breadcrumb-agesci`) attivabile via `breadcrumb_items`.
- Sub-navbar secondaria (`subnav-agesci`) attivabile via `subnav_items`.
- Integrazione icone Bootstrap Icons tramite `django-bootstrap-icons` (extra `[icons]`).
- Workflow GitHub Actions per pubblicazione automatica su PyPI via Trusted Publisher.
- Layout mobile responsive: sotto 768px il footer torna al flusso normale del documento.

### Modificato
- `base.html` espone tutti i blocchi di composizione (navbar, footer, breadcrumb, subnav).
- Context processor esteso con tutte le variabili `AGESCI_THEME_*`.

---

## [1.0.0] — 2024

### Aggiunto
- Prima versione pubblica del tema.
- Palette ufficiale AGESCI dal *Manuale Immagine Coordinata 2011*.
- Sistema branche via `[data-branca]` e CSS custom properties.
- Template `base.html`, partial navbar e footer.
- Template tag `emblema_zona`, `zone_disponibili`, `branca_bg`.
- Classi utility `bg-ag-*` e `text-ag-*`.
- Progetto Django di esempio (`example_project/`).
- Pacchetto pubblicato su PyPI come `django-agesci-campania-theme`.
