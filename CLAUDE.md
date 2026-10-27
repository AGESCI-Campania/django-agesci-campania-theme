# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

Questo repository è **django-agesci-theme**: un tema Bootstrap 6 riusabile (serie 3.x, pre-release finché Bootstrap 6 è in alpha),
distribuito come pacchetto Python (`django-agesci-campania-theme`), per le app
Django dell'AGESCI Campania.

È un **workspace uv con due pacchetti PyPI**: il tema Bootstrap 6 (root,
`agesci_theme/`) e il tema **CoreUI 5** (`coreui/`, pacchetto
`django-agesci-campania-coreui-theme`, app `agesci_coreui`). CoreUI è basato su
Bootstrap **5.3** (non esiste un CoreUI su Bootstrap 6): dal tema base usa solo
Python (template tag, context processor), immagini e `_palette.scss`, mentre il
**markup è duplicato** nel pacchetto CoreUI (vedi sotto). Dettagli in
`docs/coreui.md`; guida per chi migra da 2.x in `docs/migrazione-bootstrap-6.md`.

## Cosa NON rompere

- **La palette** (`agesci_theme/static/agesci_theme/scss/_palette.scss`) è
  ufficiale, presa dal Manuale Immagine Coordinata AGESCI 2011. Non inventare
  colori: se servono modifiche, parti da quei valori Pantone.
- **Il meccanismo per branca**: il colore primario è una CSS custom property
  rimappata da `[data-branca]` in `_branche.scss`. L'attributo `data-branca`
  va sul tag `<html>` (vedi `base.html:4`). NON hardcodare colori nei
  componenti — usa `var(--ag-primary)` e derivati.
- Il **CSS compilato è committato** (`css/agesci.css` e `css/agesci.min.css`,
  più `coreui/.../css/agesci-coreui(.min).css`). Dopo ogni modifica allo SCSS
  rigeneralo con `npm run build:css` (compila ENTRAMBI i temi) e committa.
- **Bootstrap 6 (3.x) e CoreUI 5 hanno markup diverso e vivono separati**:
  Modal/Offcanvas/Dropdown → `dialog`/`drawer`/`menu`, classi `theme-*`, prefissi
  responsive (`lg:d-none`), `form-control` sui select, `.check`/`.radio`… Il tema
  base scrive `data-bs-*` fissi (nessun `{% ag_js %}`, rimosso nella 3.0). CoreUI legge
  SOLO `data-coreui-*` (verificato su CoreUI 5.9.0: `data-bs-*` non apre il modal)
  e ha **copie proprie** con lo stesso percorso dei template del tema
  (`coreui/agesci_coreui/templates/agesci_theme/components/…`, `…/forms/…`,
  `django/forms/…`, `allauth/…`), del JS dei form (`password-toggle.js`,
  `multiselect-dropdown.js`) e dei partial SCSS (`_prefix` con `cui-`, `_branche`,
  `_bootstrap-overrides`, `_forms`, `_components`; solo `_palette` è condiviso via
  `--load-path`). Le copie vincono perché `agesci_coreui` precede `agesci_theme` in
  `INSTALLED_APPS` (system check `agesci_coreui.E002`: nell'ordine sbagliato non c'è
  errore, escono pagine col markup sbagliato). Nei form CoreUI usa
  `agesci_coreui.forms.AgesciCoreuiFormRenderer`. **Una modifica a un componente va
  fatta nel tema (BS6) e, se serve, anche nella copia CoreUI (BS5)**; i tag Python
  passano contesto neutro (es. `cols`, `variant`) e le classi si scelgono nel template.
  Il layout viewport fisso sta in `_layout.scss`, solo `agesci.scss`: CoreUI usa
  `.wrapper`/`.sidebar`/`.header` nativi e scorre la pagina intera.
- **Bootstrap 6 usa i `@layer` CSS** (`colors, config, root, reboot, layout, content,
  forms, components, custom, helpers, utilities`) e il CSS del tema è FUORI dai
  layer. Due trappole verificate nel browser: (1) un `display:` incondizionato nel
  tema batte le utility del markup (`d-none`, `lg:d-none`): dichiaralo solo nella
  media query in cui l'elemento va mostrato (vedi `.ag-sidebar__close`);
  (2) un `!important` DENTRO un layer batte un `!important` FUORI: `.lg:drawer` da
  1024px forza `width:auto`, sfondo trasparente, `border:0`, `transition:none` con
  `!important` in `components`, quindi larghezza/sfondo/transizione della sidebar
  stanno in `@layer layout { @media (min-width:1024px) { … !important } }` alla fine
  di `_sidebar.scss`. NON spostarle fuori dal `@layer`.
- **Il colore di branca passa dai token `--bs-primary-*`** (`_branche.scss`: base, bg,
  fg, fg-emphasis, bg-subtle, bg-muted, border, focus-ring, contrast): `.theme-primary`,
  link e focus ring li leggono da soli. NON riscrivere override per singolo componente
  (`--bs-btn-*`…), non esistono più le varianti `-rgb` (usa `color-mix()`), non
  ridefinire `--bs-fg-body` (i sottoalberi `data-bs-theme="dark"`, es. il menu utente,
  devono restare chiari) e NON mettere `a { color }` globale (ricolorerebbe i `.menu-item`).
- **Bootstrap 6 è pinnato e in alpha**: `base.html` carica `bootstrap@6.0.0-alpha.1`
  (CSS e bundle ESM) con SRI sha384, nei blocchi `bootstrap_css`/`bootstrap_js`. Il JS è
  `<script type="module">`: non esiste `window.bootstrap`. `<html>` ha
  `data-bs-theme="light"` (BS6 segue altrimenti `prefers-color-scheme`). Browser minimi:
  Chrome/Edge 130, Firefox 132, Safari 18. Ad ogni alpha: vedi `docs/sviluppo.md`
  ("Aggiornare Bootstrap 6").
- **Sidebar = `<dialog class="lg:drawer drawer-start">`** (non `<nav>`): da 1024px è
  in flusso e visibile senza `open`; sotto è un drawer a tutta altezza
  (`--bs-drawer-inset:0; --bs-drawer-border-radius:0`). Il menu utente è un `.menu`
  con `data-bs-strategy="fixed"`, `data-bs-placement="top-start"`.
- I tag che mappano varianti v5 passano anche `theme` (`_theme()` in
  `agesci_components.py`: `dark`→`inverse`, `light`→`secondary`; BS6 non ha
  `theme-light`/`theme-dark`) e restano retrocompatibili su `variant`.

- **Tema CoreUI, varianti derivate del primario**: CoreUI colora chip,
  alert, list group ecc. con `--cui-primary-bg-subtle`/`-text-emphasis`/
  `-border-subtle`/`-contrast`, che `_branche.scss` non genera.
  `_coreui-components.scss` le rimappa sulle `--ag-*`: senza, restano sul
  viola di default di CoreUI (#5856d6) qualunque sia la branca.
- **`agesci_coreui/js/layout.js` va caricato PRIMA di `coreui.bundle.min.js`**:
  ripristina la classe `sidebar-narrow-unfoldable` prima che CoreUI crei
  l'istanza della sidebar (al `load`). Il salvataggio legge la classe con
  `setTimeout(0)` dopo il click: l'handler di CoreUI (delegato su `.sidebar`)
  la cambia PRIMA del listener sul bottone (verificato nel browser).
- `agesci.min.css` va caricato **dopo** `bootstrap.min.css` (vedi `base.html`);
  essendo fuori dai `@layer` di Bootstrap 6 vince comunque sulle sue regole normali.
- **Layout viewport fisso**: `body { height: 100vh; overflow: hidden }` è
  definito in `_layout.scss` (solo da 1024px). Lo scroll avviene su `.ag-scroll-area`
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
- **`AgesciFormRenderer` (`agesci_theme/forms.py`) è un motore di template
  isolato**, separato da `TEMPLATES` in `settings.py`. `DIRS` batte sempre
  `APP_DIRS` (verificato su `Engine.__init__`/`filesystem.Loader`): un
  progetto consumer NON può sovrascrivere `django/forms/widgets/*.html` del
  tema mettendo un file in un proprio `templates/django/forms/...`,
  indipendentemente dalla posizione in `INSTALLED_APPS`. L'unico modo
  supportato è sottoclassare `AgesciFormRenderer` e anteporre la propria
  directory a `engine.dirs` (vedi docstring in `forms.py`).
- **`django/forms/p.html` usa `<div class="form-field mb-5">`, non `<p>`**: i browser
  chiudono automaticamente un `<p>` quando incontrano un `<div>` annidato
  (es. `.invalid-feedback`), rompendo l'adiacenza CSS richiesta da Bootstrap
  (`.is-invalid ~ .invalid-feedback`; `.form-field:has(.check.is-invalid) .invalid-feedback`
  per checkbox/radio). Scoperto ispezionando il DOM renderizzato in un browser reale,
  non deducibile dal solo sorgente del template. NON tornare a `<p>`. Per i
  `BooleanField` il controllo va PRIMA della label (layout a due colonne di
  `.form-field`, label+aiuto+errore in `.form-field-content`).
- **`.invalid-feedback { display: block; }` (`_forms.scss`) è deliberato**:
  i nostri errori vengono renderizzati solo quando il campo ha davvero un
  errore (vedi `django/forms/errors/list/default.html`), quindi non serve —
  anzi è dannoso — il comportamento di default di Bootstrap che nasconde
  `.invalid-feedback` fuori da posizioni precise rispetto al controllo
  `.is-invalid`. NON rimuovere questa regola pensando sia superflua: senza, gli
  errori spariscono ogni volta che il campo è avvolto in un wrapper (es. il
  multiselect, un `<div>` con dentro il `button.form-control`).
- **`allauth/layouts/base.html` deve estendere `"base.html"` (letterale),
  MAI `"agesci_theme/base.html"`**: altrimenti le pagine allauth perdono le
  personalizzazioni (nav, breadcrumb) del progetto consumer, che ha il
  proprio `templates/base.html` per convenzione già documentata sotto.
- **`agesci_theme` deve precedere le app allauth in `INSTALLED_APPS`**: il
  loader `APP_DIRS` di Django scorre i template dir delle app nell'ordine
  di `INSTALLED_APPS`. Se `allauth`/`allauth.account`/`allauth.mfa`
  precedono `agesci_theme`, i loro template bundled (es.
  `allauth/layouts/base.html`) vengono trovati PRIMA degli override del
  tema, che restano silenziosamente inapplicati (nessun errore — le
  pagine allauth appaiono semplicemente senza stile). Verificato
  empiricamente in `example_project`.
- **Niente link `"/..."` fissi nei template e nelle view della demo**: la demo
  online su GitHub Pages vive in una sottocartella
  (`/django-agesci-campania-theme/bootstrap/` e `.../coreui/`). Usa
  `{% url %}`/`reverse()` nella demo e `{% ag_home_url %}` (radice con
  prefisso) nei template del tema. `manage.py demo_statica` FALLISCE se trova
  link interni fuori prefisso o verso pagine non generate (gira anche in
  `build.yml`). Nuove pagine della demo vanno aggiunte a `PAGINE` in
  `example_project/app/management/commands/demo_statica.py`. Il test client
  NON imposta lo script prefix da `FORCE_SCRIPT_NAME` (lo fa solo il
  `WSGIHandler`): il comando chiama `set_script_prefix()` a mano.
- **I commenti Django (`{# ... #}`) NON possono estendersi su più righe**
  (limite documentato di Django, non un bug): un commento che le occupa
  più righe non viene riconosciuto come tale e il testo, incluse le
  parentesi graffe, finisce letteralmente nell'HTML renderizzato — senza
  sollevare alcun errore. Un commento su più concetti va spezzato in più
  `{# ... #}` separati, uno per riga. Verificato empiricamente aprendo
  `/accounts/login/` nel browser: il commento multi-riga di `p.html`
  compariva come testo visibile nella pagina.

## Comandi (uv)

```bash
uv sync                                          # crea .venv e installa tutto
uv run python example_project/manage.py migrate
uv run python example_project/manage.py runserver
uv run python example_project/manage.py check   # Django system check (usato anche in CI)
uv run python example_project/manage.py runserver --settings=config.settings_coreui  # demo CoreUI
uv run python example_project/manage.py check --settings=config.settings_coreui     # usato anche in CI
uv run python example_project/manage.py test app        # smoke test pagine demo × 7 branche (anche con --settings=config.settings_coreui; usato in CI)
python3 scripts/check_bs5_residui.py                    # fallisce se i template del tema base hanno pattern Bootstrap 5 (usato in CI)
uv run python example_project/manage.py demo_statica --output site/coreui --prefix /x/coreui/ --settings=config.settings_coreui  # demo statica (Pages)
uv build --package django-agesci-campania-theme          # pacchetto Bootstrap
uv build --package django-agesci-campania-coreui-theme   # pacchetto CoreUI
```

Rilascio: tag `vX.Y.Z` → tema Bootstrap, tag `coreui-vX.Y.Z` → tema CoreUI
(stesso `publish.yml`, vedi `PUBLISHING.md`). La 3.x esce come pre-release
(`v3.0.0a1`, `gh release create --prerelease`) dal branch `bootstrap-6`.

Modificare i colori (richiede Node.js):

```bash
npm install
npm run build:css    # rigenera il CSS di entrambi i temi (da fare prima del commit)
npm run watch:css    # ricompila lo SCSS in tempo reale
```

## Architettura SCSS

`agesci.scss` è solo un entrypoint; l'ordine di inclusione è fisso:

1. `_palette.scss` — variabili Sass `$agesci-*` con i valori Pantone ufficiali
   (l'unico partial condiviso con CoreUI).
2. `_branche.scss` — per ciascuna branca (`@each` + mixin `tema-primario`) genera i
   token Bootstrap 6 `--bs-primary-*` e le `--ag-primary` (e derivati). La funzione
   `on-color()` sceglie testo nero/bianco in base alla luminosità del primario.
3. `_layout.scss` — layout viewport fisso (≥ 1024px) e `.ag-scroll-area`.
4. `_bootstrap-overrides.scss` — font, `.ag-btn-light`, navbar-agesci, breadcrumb,
   subnav, footer e utility `bg-ag-*`/`text-ag-*` (il colore dei componenti NON si
   override qui: vedi i token in `_branche.scss`).
5. `_forms.scss` — `.invalid-feedback`, label nei `.form-field`, `.ag-multiselect`.
6. `_header.scss` — header a due barre e drawer mobile.
7. `_sidebar.scss` — sidebar collapsible (stato in `localStorage`) con il blocco
   `@layer layout` finale.
8. `_footer.scss`, 9. `_components.scss` — footer e componenti opzionali.

`coreui/agesci_coreui/static/agesci_coreui/scss/agesci-coreui.scss` usa
`_prefix` (default `cui-`), `_branche`, `_bootstrap-overrides`, `_forms`,
`_components` **propri** (copie BS5 nella stessa cartella), `_palette` dal tema base
(la build passa `--load-path=agesci_theme/static/agesci_theme/scss`) e aggiunge
`_coreui-layout.scss` e `_coreui-components.scss`.

## Struttura

```
agesci_theme/                  # il package Python distribuibile
  static/agesci_theme/scss/    # sorgenti SCSS (vedi sezione sopra)
  static/agesci_theme/css/     # CSS compilato (committato)
  static/agesci_theme/js/      # script JS (sidebar.js, password-toggle.js)
  static/agesci_theme/img/     # loghi, emblemi, zone, favicon
  templates/agesci_theme/
    base.html                  # template base da estendere (blocchi bootstrap_css / bootstrap_js)
    partials/                  # header.html, sidebar.html, footer.html, breadcrumb.html
    components/                # 13 template dei componenti opzionali
  templates/django/forms/      # override Bootstrap 6 per AgesciFormRenderer (opt-in)
  templates/allauth/           # override Bootstrap 6 per django-allauth (opt-in)
  templatetags/
    agesci_tags.py             # emblema_zona, branca_bg, zone_disponibili, ag_js, ag_home_url
    agesci_components.py       # 13 inclusion tag (ag_hero, ag_feature_grid, ag_password_field, ag_multiselect_dropdown, ecc.)
  forms.py                     # AgesciFormRenderer — vedi docs/forms.md
  context_processors.py        # espone le settings AGESCI_THEME_* ai template
coreui/                        # secondo pacchetto: django-agesci-campania-coreui-theme
  pyproject.toml               # dipende da django-agesci-campania-theme (workspace)
  agesci_coreui/
    templates/agesci_coreui/base.html   # layout nativo CoreUI (sidebar + header)
    templates/agesci_theme/, django/, allauth/   # COPIE BS5 dei template del tema (stesso percorso: vincono)
    static/agesci_coreui/js/            # layout.js + copie di password-toggle / multiselect-dropdown
    static/agesci_coreui/scss/          # partial BS5 propri (_prefix, _branche, …) + _coreui-*
    templatetags/agesci_coreui.py       # ag_nav_item, ag_nav_title, ag_callout, ag_avatar, ag_chip
    forms.py                   # AgesciCoreuiFormRenderer, InputChip / CampoChip (chip-input)
    checks.py                  # E001: richiede agesci_theme; E002: agesci_coreui prima di agesci_theme
example_project/               # progetto Django demo (/, /components/, /accounts/, /form-demo/)
  config/settings_coreui.py    # stessa demo col tema CoreUI
  app/templates_coreui/        # template CoreUI, cercati PRIMA di app/templates/
  app/management/commands/demo_statica.py  # genera la demo statica per GitHub Pages
  pages/index.html             # indice della demo online (radice del sito Pages)
```

## Convenzioni

- Codice e commenti in italiano (è il contesto associativo).
- Branche valide: `generico, capi, lc, eg, rs, viola, generico2`. Se ne aggiungi
  una, aggiornala in CINQUE punti: `_branche.scss`
  (anche la copia in `coreui/.../scss/_branche.scss`),
  `context_processors.BRANCHE_VALIDE`, `agesci_tags._BRANCA_BG`,
  `_bootstrap-overrides.scss` (classe `.bg-ag-*`, anche la copia CoreUI), poi
  ricompila il CSS.
- Il `base.html` CoreUI (`agesci_coreui/base.html`) riusa gli stessi nomi di
  blocco dove esiste un equivalente e segue la stessa regola: i blocchi vanno
  definiti DIRETTAMENTE nel file, mai in un `{% include %}`.
- Mantieni la retrocompatibilità dei blocchi template di `base.html`: altre app
  ne dipendono. Blocchi esposti: `title`, `extra_head`, `header`, `brand_url`,
  `brand_text`, `header_nav`, `offcanvas_nav`, `header_search`, `header_actions`,
  `sidebar`, `sidebar_items`, `sidebar_user`, `main_class`, `messages`, `content`,
  `footer`, `footer_brand_text`, `footer_columns`, `footer_col1_title`,
  `footer_col1_links`, `footer_col2_title`, `footer_col2_links`, `footer_text`,
  `footer_copyright`, `footer_links`, `extra_js`, e dalla 3.0 `bootstrap_css`,
  `bootstrap_js`.
- `breadcrumb_items` nel contesto della view attiva la breadcrumb automaticamente
  nella barra inferiore dell'header (`ag-header-bottom`). Lista di dict
  `{"label": "...", "url": "..."}` — l'ultimo elemento è `active` senza link.
  In alternativa usa `{% ag_breadcrumb %}` nel blocco `content`.
- **Icone Bootstrap (opzionale)**: `django-bootstrap-icons` è una dipendenza
  opzionale (`[icons]`). App name: `django_bootstrap_icons`. Templatetag:
  `{% load bootstrap_icons %}` poi `{% bs_icon "nome" %}`. Raccomandare sempre
  `BS_ICONS_CACHE` in settings per le prestazioni.
- **Form Bootstrap 6 e django-allauth (opzionale)**: attivazione esplicita
  via `FORM_RENDERER = "agesci_theme.forms.AgesciFormRenderer"` (con CoreUI:
  `agesci_coreui.forms.AgesciCoreuiFormRenderer`) nelle
  settings del consumer — vale per tutti i form Django del progetto, non
  solo per allauth. `django-allauth` resta un extra opzionale (`[allauth]`,
  testato con `65.19.1`), mai una dipendenza hard. Dettagli in
  `docs/forms.md` e `docs/allauth.md`.

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

Passo opzionale, per lo styling Bootstrap 6 dei form Django (e di
django-allauth, se installato) — vedi `docs/forms.md`:

```python
FORM_RENDERER = "agesci_theme.forms.AgesciFormRenderer"
```

## Classi utility palette

`bg-ag-viola`, `bg-ag-azzurro`, `bg-ag-giallo-lc`, `bg-ag-verde-eg`,
`bg-ag-rosso-rs`, `bg-ag-giallo-oro`, `bg-ag-generico-2` e i corrispettivi `text-ag-*`.
