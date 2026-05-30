# CLAUDE.md — Guida per Claude Code

Questo repository è **django-agesci-theme**: un tema Bootstrap 5 riusabile,
distribuito come pacchetto Python installabile, per le app Django dell'AGESCI
Campania.

## Cosa NON rompere

- **La palette** (`agesci_theme/static/agesci_theme/scss/_palette.scss`) è
  ufficiale, presa dal Manuale Immagine Coordinata AGESCI 2011. Non inventare
  colori: se servono modifiche, parti da quei valori Pantone.
- **Il meccanismo per branca**: il colore primario è una CSS custom property
  rimappata da `[data-branca]` in `_branche.scss`. NON hardcodare colori nei
  componenti — usa `var(--ag-primary)` e derivati.
- Il **CSS compilato è committato** (`css/agesci.css` e `css/agesci.min.css`).
  Dopo ogni modifica allo SCSS rigeneralo con `npm run build:css` e committa.

## Struttura

```
agesci_theme/                  # il package Python distribuibile
  static/agesci_theme/scss/    # sorgenti SCSS
  static/agesci_theme/css/     # CSS compilato (committato)
  static/agesci_theme/img/     # loghi, emblemi, zone, favicon
  templates/agesci_theme/      # base.html, navbar, footer
  templatetags/agesci_tags.py  # emblema_zona, branca_bg, zone_disponibili
  context_processors.py        # espone le settings AGESCI_THEME_* ai template
example_project/               # progetto Django demo per testare il tema
```

## Comandi (uv)

```bash
uv sync                        # crea .venv e installa tutto (tema editable + dev)
uv run python example_project/manage.py migrate
uv run python example_project/manage.py runserver
```

Per modificare i colori:

```bash
npm install
npm run watch:css              # ricompila lo SCSS in tempo reale
```

## Convenzioni

- Codice e commenti in italiano (è il contesto associativo).
- Branche valide: `generico, capi, lc, eg, rs, viola`. Se ne aggiungi una,
  aggiornala in TRE punti: `_branche.scss`, `context_processors.BRANCHE_VALIDE`,
  `agesci_tags._BRANCA_BG`, poi ricompila il CSS.
- Mantieni la retrocompatibilità dei blocchi template di `base.html`: altre app
  ne dipendono.
