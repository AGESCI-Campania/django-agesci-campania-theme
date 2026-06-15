# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

Questo repository è **django-agesci-theme**: un tema Bootstrap 5 riusabile,
distribuito come pacchetto Python (`django-agesci-campania-theme`), per le app
Django dell'AGESCI Campania.

## Cosa NON rompere

- **La palette** (`agesci_theme/static/agesci_theme/scss/_palette.scss`) è
  ufficiale, presa dal Manuale Immagine Coordinata AGESCI 2011. Non inventare
  colori: se servono modifiche, parti da quei valori Pantone.
- **Il meccanismo per branca**: il colore primario è una CSS custom property
  rimappata da `[data-branca]` in `_branche.scss`. L'attributo `data-branca`
  va sul tag `<html>` (vedi `base.html:4`). NON hardcodare colori nei
  componenti — usa `var(--ag-primary)` e derivati.
- Il **CSS compilato è committato** (`css/agesci.css` e `css/agesci.min.css`).
  Dopo ogni modifica allo SCSS rigeneralo con `npm run build:css` e committa.
- Bootstrap 5 è caricato da CDN in `base.html`; `agesci.min.css` va caricato
  **dopo** di esso e sovrascrive le sue custom properties.
- **Layout viewport fisso**: `body { height: 100vh; overflow: hidden }` è
  definito in `_bootstrap-overrides.scss`. Lo scroll avviene su `.ag-scroll-area`
  (il wrapper flex che contiene `<main>` + `<footer>` come fratelli), non su
  `main` direttamente. NON usare `min-vh-100` sul body. NON rimettere
  `overflow-y: auto` su `main` — lo scroll deve stare su `.ag-scroll-area`
  così il footer occupa tutta la larghezza del wrapper indipendentemente dal
  `.container` di `<main>`.
- **Header e breadcrumb full-width**: `ag-header-top`, `ag-header-bottom` e
  `breadcrumb.html` NON hanno più un `<div class="container">` annidato. Il
  contenuto si estende a tutta la larghezza; il padding laterale `px-3` è
  applicato direttamente sull'elemento esterno. Non reintrodurre `.container`
  dentro le barre dell'header.
- **L'HTML dell'header è in `base.html`, non in `header.html`**: i blocchi
  `header_nav`, `offcanvas_nav`, `header_search`, `header_actions` funzionano
  con l'ereditarietà Django solo perché sono definiti DIRETTAMENTE in `base.html`.
  `{% include %}` crea un `render_context` separato che NON eredita i blocchi del
  template figlio: non spostare mai questi blocchi in un file incluso via `{% include %}`.

## Comandi (uv)

```bash
uv sync                                          # crea .venv e installa tutto
uv run python example_project/manage.py migrate
uv run python example_project/manage.py runserver
uv run python example_project/manage.py check   # Django system check (usato anche in CI)
uv build                                         # produce il pacchetto .whl / .tar.gz
```

Modificare i colori (richiede Node.js):

```bash
npm install
npm run build:css    # rigenera agesci.css e agesci.min.css (da fare prima del commit)
npm run watch:css    # ricompila lo SCSS in tempo reale
```

## Architettura SCSS

`agesci.scss` è solo un entrypoint; l'ordine di inclusione è fisso:

1. `_palette.scss` — variabili Sass `$agesci-*` con i valori Pantone ufficiali.
2. `_branche.scss` — genera le CSS custom properties `--ag-primary` (e derivati)
   per ciascuna branca via `@each` + mixin `tema-primario`. La funzione
   `on-color()` sceglie testo nero/bianco in base alla luminosità del primario.
3. `_bootstrap-overrides.scss` — rimappa i token Bootstrap 5 (`--bs-primary`,
   link, pulsanti) alle variabili `--ag-*`; definisce `.ag-scroll-area`.
4. `_header.scss` — stili dell'header a due barre e del pannello offcanvas.
5. `_sidebar.scss` — sidebar collapsible con stato persistito in `localStorage`.
6. `_footer.scss` — footer con colonne e riga copyright.
7. `_components.scss` — componenti opzionali (hero, jumbotron, ecc.).

## Struttura

```
agesci_theme/                  # il package Python distribuibile
  static/agesci_theme/scss/    # sorgenti SCSS (vedi sezione sopra)
  static/agesci_theme/css/     # CSS compilato (committato)
  static/agesci_theme/js/      # script JS (sidebar.js)
  static/agesci_theme/img/     # loghi, emblemi, zone, favicon
  templates/agesci_theme/
    base.html                  # template base da estendere
    partials/                  # header.html, sidebar.html, footer.html, breadcrumb.html
    components/                # 11 template dei componenti opzionali
  templatetags/
    agesci_tags.py             # emblema_zona, branca_bg, zone_disponibili
    agesci_components.py       # 11 inclusion tag (ag_hero, ag_feature_grid, ecc.)
  context_processors.py        # espone le settings AGESCI_THEME_* ai template
example_project/               # progetto Django demo (/, /components/)
```

## Convenzioni

- Codice e commenti in italiano (è il contesto associativo).
- Branche valide: `generico, capi, lc, eg, rs, viola`. Se ne aggiungi una,
  aggiornala in TRE punti: `_branche.scss`, `context_processors.BRANCHE_VALIDE`,
  `agesci_tags._BRANCA_BG`, poi ricompila il CSS.
- Mantieni la retrocompatibilità dei blocchi template di `base.html`: altre app
  ne dipendono. Blocchi esposti: `title`, `extra_head`, `header`, `brand_url`,
  `brand_text`, `header_nav`, `offcanvas_nav`, `header_search`, `header_actions`,
  `sidebar`, `sidebar_items`, `sidebar_user`, `main_class`, `messages`, `content`,
  `footer`, `footer_brand_text`, `footer_columns`, `footer_col1_title`,
  `footer_col1_links`, `footer_col2_title`, `footer_col2_links`, `footer_text`,
  `footer_copyright`, `footer_links`, `extra_js`.
- `breadcrumb_items` nel contesto della view attiva la breadcrumb automaticamente
  nella barra inferiore dell'header (`ag-header-bottom`). Lista di dict
  `{"label": "...", "url": "..."}` — l'ultimo elemento è `active` senza link.
  In alternativa usa `{% ag_breadcrumb %}` nel blocco `content`.
- **Icone Bootstrap (opzionale)**: `django-bootstrap-icons` è una dipendenza
  opzionale (`[icons]`). App name: `django_bootstrap_icons`. Templatetag:
  `{% load bootstrap_icons %}` poi `{% bs_icon "nome" %}`. Raccomandare sempre
  `BS_ICONS_CACHE` in settings per le prestazioni.

## Installazione del pacchetto

Il pacchetto è pubblicato su PyPI:

```bash
# con uv (consigliato)
uv add django-agesci-campania-theme
# con pip
pip install django-agesci-campania-theme
```

## Integrazione in un progetto Django

`settings.py` richiede due aggiunte:

```python
INSTALLED_APPS = [..., "agesci_theme"]

TEMPLATES = [{"OPTIONS": {"context_processors": [
    ...,
    "agesci_theme.context_processors.agesci_theme",
]}}]
```

Il context processor espone in ogni template le variabili `agesci_theme_*`
(nomi lowercase delle settings `AGESCI_THEME_*`). Settings sovrascrivibili:
`AGESCI_THEME_BRANCA`, `AGESCI_THEME_NOME`, `AGESCI_THEME_LOGO`,
`AGESCI_THEME_LOGO_NAVBAR`, `AGESCI_THEME_EMBLEMA`, `AGESCI_THEME_FAVICON_32`,
`AGESCI_THEME_FAVICON_16`, `AGESCI_THEME_NAVBAR_TESTO_SCURO`.

## Classi utility palette

`bg-ag-viola`, `bg-ag-azzurro`, `bg-ag-giallo-lc`, `bg-ag-verde-eg`,
`bg-ag-rosso-rs`, `bg-ag-giallo-oro` e i corrispettivi `text-ag-*`.
