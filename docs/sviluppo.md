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
├── _branche.scss              ← genera i token --bs-primary-* e le --ag-* per branca
├── _layout.scss               ← layout viewport fisso (.ag-scroll-area)
├── _bootstrap-overrides.scss  ← navbar, breadcrumb, .ag-btn-light, utility palette
├── _forms.scss                ← validazione form (.invalid-feedback), label, multiselect
├── _header.scss               ← stili header a due barre e drawer mobile
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

Genera, per ciascuna branca (`@each` sulla mappa `$branche`, mixin
`tema-primario`), i **token primary di Bootstrap 6** (`--bs-primary-base`,
`-bg`, `-fg`, `-fg-emphasis`, `-bg-subtle`, `-bg-muted`, `-border`,
`-focus-ring`, `-contrast`) e le variabili `--ag-primary` e derivate.
Bootstrap 6 deriva da quei token bottoni `theme-primary`, link e focus ring:
non servono override per singolo componente.

La funzione `on-color()` calcola automaticamente se il testo sul primario
deve essere nero o bianco in base alla luminosità HSL (soglia 62%).

### `_bootstrap-overrides.scss`

- Stila navbar (`.navbar-agesci`, `.ag-navbar--testo-scuro`), breadcrumb, sub-navbar e footer con le custom properties del tema.
- Definisce `.ag-btn-light` (bottoni su header colorato) e le classi utility `bg-ag-*` e `text-ag-*`.
- Il **layout viewport fisso** (`.ag-scroll-area`, solo ≥ 1024px, breakpoint `lg`) sta in `_layout.scss`.

```{important}
**Bootstrap 6 usa i `@layer` CSS** (`colors, config, root, reboot, layout, content,
forms, components, custom, helpers, utilities`). Due conseguenze per chi scrive SCSS del tema:

1. Il CSS del tema è **fuori dai layer** e quindi vince sempre sulle regole normali
   di Bootstrap: un `display:` incondizionato su un elemento che nel markup ha
   `d-none` / `lg:d-none` annulla l'utility. Dichiara `display` solo nella media
   query in cui l'elemento deve comparire (vedi `.ag-sidebar__close` in `_sidebar.scss`).
2. Un `!important` **dentro** un layer batte un `!important` **fuori** dai layer.
   `.lg:drawer` da 1024px forza `width:auto`, sfondo trasparente, `border:0` e
   `transition:none` con `!important` nel layer `components`: per sovrascriverli
   (larghezza e colore della sidebar) servono regole `!important` in un layer
   **precedente**, `@layer layout { … }` — vedi la fine di `_sidebar.scss`. Non spostarle
   fuori dal blocco `@layer`.
```

### Aggiornare Bootstrap 6 (ad ogni alpha)

Bootstrap 6 è in alpha e le classi possono cambiare tra una versione e l'altra. Per aggiornare:

1. `npm view bootstrap@next version` e rileggere `https://getbootstrap.com/llms.txt` e la
   [guida alla migrazione](https://getbootstrap.com/docs/6.0/guides/migration/) ufficiale
   (c'è anche una *skill* per assistenti AI: `npx skills add twbs/bootstrap`).
2. In `base.html` (blocchi `bootstrap_css` / `bootstrap_js`) cambiare versione e hash SRI:
   `curl -s https://cdn.jsdelivr.net/npm/bootstrap@VERSIONE/dist/css/bootstrap.min.css | openssl dgst -sha384 -binary | openssl base64 -A`
   (idem per `js/bootstrap.bundle.min.js`; prefisso `sha384-`).
3. Verificare nel browser (Chrome, desktop e 390 px, tutte le branche): sidebar fissa e collassata,
   drawer dell'header e della sidebar, menu utente e menu branche, dialog, multiselect, form con
   errori, console senza errori di integrità.
4. Controllare i residui con uno script che confronti le classi usate nei template con il
   CSS di Bootstrap (`rg` dei pattern v5, vedi [Migrazione a Bootstrap 6](migrazione-bootstrap-6.md)).

### `_forms.scss`

`.invalid-feedback { display: block; }` (vedi
[Form e validazione](forms.md#perche-invalid-feedback-display-block) per il
perché — **non rimuoverla** pensando sia superflua), il peso delle label nei
`.form-field` e `.ag-multiselect { position: relative }`.

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

La CI esegue anche questi controlli, utili da lanciare in locale prima del commit:

```bash
# smoke test: le pagine demo si renderizzano per tutte le 7 branche
uv run python example_project/manage.py test app
uv run python example_project/manage.py test app --settings=config.settings_coreui

# nessun residuo Bootstrap 5 nei template del tema base (CoreUI è escluso)
python3 scripts/check_bs5_residui.py

# il CSS compilato committato deve coincidere con lo SCSS
npm run build:css && git diff --exit-code -- agesci_theme/static coreui/agesci_coreui/static
```

---

## Demo statica su GitHub Pages

La demo online (<https://agesci-campania.github.io/django-agesci-campania-theme/>) è generata dal workflow `.github/workflows/pages.yml`
a ogni push su `main`. GitHub Pages ospita solo file statici, quindi il
comando `demo_statica` renderizza le pagine del progetto demo con il test
client di Django e le salva come HTML, insieme agli asset di `collectstatic`:

```bash
uv run python example_project/manage.py demo_statica \
    --output site/bootstrap --prefix /django-agesci-campania-theme/bootstrap/
uv run python example_project/manage.py demo_statica \
    --output site/coreui --prefix /django-agesci-campania-theme/coreui/ \
    --settings=config.settings_coreui
```

- `--prefix` è la sottocartella di pubblicazione: diventa `FORCE_SCRIPT_NAME`
  e `STATIC_URL`. Per questo i template non devono contenere link `"/..."`
  fissi: usa `{% url %}`, `reverse()` o `{% ag_home_url %}`.
- Il comando **fallisce** se una pagina contiene un link interno che su Pages
  sarebbe un 404 (fuori dal prefisso o verso una pagina non generata). La
  stessa verifica gira in `build.yml` su ogni PR.
- Le pagine generate sono elencate in `PAGINE`
  (`example_project/app/management/commands/demo_statica.py`): una nuova
  pagina della demo va aggiunta lì.
- L'invio dei form è bloccato da uno script iniettato nelle pagine; lo stato
  "con errori" del form è la pagina `/form-demo/errori/`.
- La pagina indice alla radice è `example_project/pages/index.html`.

Attivazione (una volta sola, da un amministratore del repository):
**Settings → Pages → Build and deployment → Source: GitHub Actions**.

---

## Aggiungere asset statici

Loghi, emblemi e favicon si trovano in `agesci_theme/static/agesci_theme/img/`.

- Gli emblemi di zona sono in `img/zone/` con il pattern `CAMPANIA_<ZONA>.png`.
- Se aggiungi una nuova zona, aggiorna anche `ZONE` in
  `agesci_theme/templatetags/agesci_tags.py`.

---

## Istruzioni per assistenti AI

Tre cose da tenere allineate al codice (vedi [Usare il tema con un assistente AI](assistenti-ai.md)):

- `docs/assistenti-ai.md`: le regole per i progetti che usano il tema. Aggiornala quando cambia una
  trappola nota, un blocco di `base.html` o un tag.
- `skills/django-agesci-theme/SKILL.md`: la skill installabile dai consumer (tabella v5 → v6 e regole del tema).
  Ad ogni alpha di Bootstrap 6 ricontrolla la tabella.
- `llms.txt` / `llms-full.txt`: generati da `scripts/build_llms_txt.py` (`python3 scripts/build_llms_txt.py`,
  output in `docs/_llms/`, non committato). Le pagine vengono dal toctree di `docs/index.md`; per una pagina
  nuova aggiungi la descrizione in `DESCRIZIONI` dello script.

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
