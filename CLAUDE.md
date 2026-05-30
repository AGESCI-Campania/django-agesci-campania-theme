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
   link, pulsanti) alle variabili `--ag-*`.

## Struttura

```
agesci_theme/                  # il package Python distribuibile
  static/agesci_theme/scss/    # sorgenti SCSS (vedi sezione sopra)
  static/agesci_theme/css/     # CSS compilato (committato)
  static/agesci_theme/img/     # loghi, emblemi, zone, favicon
  templates/agesci_theme/      # base.html, navbar, footer (partials)
  templatetags/agesci_tags.py  # emblema_zona, branca_bg, zone_disponibili
  context_processors.py        # espone le settings AGESCI_THEME_* ai template
example_project/               # progetto Django demo per testare il tema
```

## Convenzioni

- Codice e commenti in italiano (è il contesto associativo).
- Branche valide: `generico, capi, lc, eg, rs, viola`. Se ne aggiungi una,
  aggiornala in TRE punti: `_branche.scss`, `context_processors.BRANCHE_VALIDE`,
  `agesci_tags._BRANCA_BG`, poi ricompila il CSS.
- Mantieni la retrocompatibilità dei blocchi template di `base.html`: altre app
  ne dipendono. Blocchi esposti: `title`, `extra_head`, `navbar`, `brand_url`,
  `brand_text`, `nav_items`, `main_class`, `messages`, `content`, `footer`,
  `footer_text`, `footer_links`, `extra_js`.

## Installazione del pacchetto

```bash
# con uv (consigliato)
uv add "git+https://github.com/AGESCI-Campania/django-agesci-campania-theme.git"
# con pip
pip install "git+https://github.com/AGESCI-Campania/django-agesci-campania-theme.git"
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
