# Sviluppo del tema

Questa sezione è rivolta a chi vuole **modificare il tema stesso** (colori,
componenti, layout), non semplicemente usarlo in un'app Django.

---

## Prerequisiti

- **Python 3.12+** con [uv](https://github.com/astral-sh/uv)
- **Node.js** (qualsiasi versione LTS recente) con npm — necessario solo per
  modificare lo SCSS

---

## Setup dell'ambiente di sviluppo

```bash
# 1. Clona il repository
git clone https://github.com/AGESCI-Campania/django-agesci-campania-theme.git
cd django-agesci-campania-theme

# 2. Crea il virtualenv e installa le dipendenze Python
uv sync

# 3. Installa le dipendenze Node (Sass)
npm install

# 4. Avvia il progetto demo
uv run python example_project/manage.py migrate
uv run python example_project/manage.py runserver
```

---

## Struttura SCSS

I sorgenti si trovano in `agesci_theme/static/agesci_theme/scss/`.
L'entrypoint è `agesci.scss`, che include i file nell'ordine fisso seguente:

```
agesci.scss
├── _palette.scss              ← variabili $agesci-* (Pantone ufficiali)
├── _branche.scss              ← genera le --ag-* custom properties per branca
├── _bootstrap-overrides.scss  ← rimappa i token Bootstrap, layout (.ag-scroll-area), utility
├── _header.scss               ← stili header a due barre e offcanvas
├── _sidebar.scss              ← sidebar collapsible
├── _footer.scss               ← footer
└── _components.scss           ← componenti opzionali (hero, jumbotron, ecc.)
```

### `_palette.scss`

Contiene **solo variabili Sass** `$agesci-*` con i valori HEX del Manuale
Immagine Coordinata. Non generano CSS da soli.

**Non inventare colori**: se servono nuovi valori, parti sempre dai Pantone
ufficiali.

### `_branche.scss`

Genera le CSS custom properties `--ag-primary` e derivati per ciascuna branca
tramite `@each` sulla mappa `$branche` e il mixin `tema-primario`.

La funzione `on-color()` calcola automaticamente se il testo sul primario
deve essere nero o bianco in base alla luminosità HSL (soglia 62%).

### `_bootstrap-overrides.scss`

- Rimappa `--bs-primary` e i token dei componenti Bootstrap verso `--ag-*`.
- Definisce il **layout viewport fisso** via `.ag-scroll-area` (solo su desktop ≥ 992px, breakpoint `lg`).
- Stila navbar, breadcrumb, sub-navbar, footer con le custom properties del tema.
- Definisce le classi utility `bg-ag-*` e `text-ag-*`.

---

## Workflow SCSS

Durante lo sviluppo usa la modalità watch per ricompilare automaticamente:

```bash
npm run watch:css
```

Prima di ogni commit, rigenera i file CSS compilati:

```bash
npm run build:css
```

Questo produce **due file** che vanno committati insieme alle modifiche SCSS:

- `agesci_theme/static/agesci_theme/css/agesci.css` (expanded, per debug)
- `agesci_theme/static/agesci_theme/css/agesci.min.css` (compressed, usato in produzione)

:::{important}
Il CSS compilato è committato appositamente: chi installa il pacchetto da PyPI
non ha bisogno di Sass o Node.js.
:::

---

## Verificare le modifiche

Il progetto demo copre tutti i componenti. Testa le branche una per una:

```python
# example_project/config/settings.py
AGESCI_THEME_BRANCA = "lc"   # cambia qui e ricarica il browser
```

Per una verifica Django:

```bash
uv run python example_project/manage.py check
```

---

## Aggiungere asset statici

Loghi, emblemi e favicon si trovano in `agesci_theme/static/agesci_theme/img/`.

- Gli emblemi di zona sono in `img/zone/` con il pattern `CAMPANIA_<ZONA>.png`.
- Se aggiungi una nuova zona, aggiorna anche `ZONE` in
  `agesci_theme/templatetags/agesci_tags.py`.

---

## Rilascio

Il tema usa [Hatchling](https://hatch.pypa.io/) come build backend. La
pubblicazione su PyPI avviene tramite GitHub Actions al push di un tag `v*`:

```bash
git tag v1.2.0
git push --tags
```

Il workflow `.github/workflows/build.yml` esegue `uv build` e pubblica su PyPI
tramite Trusted Publisher. Vedi `PUBLISHING.md` per i dettagli.

---

## Linee guida per contribuire

1. Apri un'issue per descrivere la modifica prima di implementarla.
2. Codice e commenti in **italiano** (convenzione del progetto).
3. Non hardcodare colori nei componenti: usa sempre `var(--ag-primary)` e
   derivati.
4. Rigenera il CSS con `npm run build:css` e includi i file compilati nel
   commit.
5. Aggiungi o aggiorna la documentazione in `docs/` se la modifica riguarda
   comportamenti visibili agli utenti.
