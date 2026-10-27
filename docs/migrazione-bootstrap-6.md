# Migrazione a Bootstrap 6 (tema 3.0)

La serie **3.x** del tema passa da Bootstrap 5.3 a **Bootstrap 6**. Bootstrap 6 è
ancora in alpha (`6.0.0-alpha.1`): il tema lo carica da CDN con versione e hash
SRI pinnati e viene rilasciato come **pre-release** (`3.0.0a1`, `a2`, …) finché
Bootstrap non è stabile. Questa pagina elenca cosa cambia per chi aggiorna da una 2.x.

```{note}
Bootstrap ha una guida ufficiale ([getbootstrap.com/docs/6.0/guides/migration](https://getbootstrap.com/docs/6.0/guides/migration/))
e una *skill* per assistenti AI (`npx skills add twbs/bootstrap`, skill
`bootstrap-v5-v6-migration`; indice per LLM in `https://getbootstrap.com/llms.txt`).
Qui sono riportati solo i cambiamenti che toccano i template e il CSS dei progetti che usano il tema.
```

## Cosa NON devi fare

Il tema si occupa da solo di: `base.html` e i suoi partial, i template tag
(`ag_*`), il renderer dei form, gli override di allauth, i CSS compilati, il
colore per branca. Se usi il tema "a scatola chiusa" (estendi `base.html`, usi
i tag e i blocchi) e non scrivi markup Bootstrap tuo, l'aggiornamento è quasi
trasparente: leggi solo [Requisiti](#requisiti) e [Rotture nell'API del tema](#rotture-nellapi-del-tema).

## Requisiti

- Browser: **Chrome/Edge ≥ 130, Firefox ≥ 132, Safari ≥ 18** (Bootstrap 6 usa
  `<dialog>`, `:has()`, container queries, `light-dark()`, `oklch()` e
  `color-mix()` senza fallback né polyfill).
- Installazione pre-release: `uv add --prerelease allow django-agesci-campania-theme`
  o `pip install --pre django-agesci-campania-theme`.
- Il tema forza `data-bs-theme="light"` su `<html>`: Bootstrap 6 segue altrimenti
  `prefers-color-scheme` e il tema AGESCI non ha una versione scura.

## Rotture nell'API del tema

| Cosa | Prima (2.x) | Ora (3.0) |
|---|---|---|
| Tag `{% ag_js %}` | prefisso `data-*` (`bs`/`coreui`) | **rimosso**: scrivi `data-bs-*` |
| `window.bootstrap` | oggetto globale | **non esiste più** (JS solo ESM): `import { Tooltip } from "…/bootstrap.bundle.min.js"` in un tuo `<script type="module">` |
| Blocchi di `base.html` | — | nuovi `bootstrap_css` e `bootstrap_js` (self-hosting / altra versione); gli altri sono invariati |
| `ag_modal_trigger` + `modal.html` | `.modal` | `<dialog class="dialog">`; parametro `centered` rimosso |
| `ag_dropdown` | `.dropdown-menu` | `.menu`; `direction` → `data-bs-placement` |
| Chiavi di contesto dei tag | `variant` | invariata; in più `theme` (`dark`→`inverse`, `light`→`secondary`) |
| `ag_feature_grid` / `ag_masonry_grid` | `row_cols_class`: `row-cols-md-3` | `md:row-cols-3` (e `col_class`: `md:col-4`) |
| `SelectMultiploADiscesa`, `ag_multiselect_dropdown` | `.dropdown` + `.form-select` | `.menu` + `.form-control form-control-caret` |
| Classe navbar scura | `.text-dark` (setting `AGESCI_THEME_NAVBAR_TESTO_SCURO`) | `.ag-navbar--testo-scuro` |
| SCSS: `_prefix.scss`, `--bs-primary-rgb`, `--bs-link-color-rgb` | presenti | rimossi (Bootstrap 6 non ha le varianti `-rgb`: usa `color-mix()`) |
| Breakpoint `lg` | 992 px | **1024 px** (anche `xl` 1280, `xxl` → `2xl` 1536) |

## Markup: cosa cambia nei tuoi template

Se sovrascrivi blocchi del tema (`sidebar`, `header_nav`, `offcanvas_nav`, …) o scrivi markup Bootstrap
nei tuoi template, applica queste conversioni.

### Classi responsive: da infisso a prefisso

`d-lg-none` → `lg:d-none`, `col-md-6` → `md:col-6`, `row-cols-md-3` → `md:row-cols-3`,
`ms-lg-auto` → `lg:ms-auto`, `text-md-end` → `md:text-end`, `flex-sm-row` → `sm:flex-row`, `g-md-3` → `md:g-3`.
Stack, griglie CSS, navbar, list group orizzontali e card group usano *container query*
(serve un contenitore `.contains-inline`); utility, colonne, container, drawer e tabelle responsive usano il viewport.

### Spaziature: la scala cambia

I valori dei numeri 2–5 non sono più gli stessi. A parità di rem:

| v5 | `1` | `2` | `3` | `4` | `5` |
|---|---|---|---|---|---|
| rem | .25 | .5 | 1 | 1.5 | 3 |
| **v6 (stesso rem)** | `1` | `3` | `5` | `7` | `12` |

Vale per `m*`, `p*`, `g*`, `gap`: `mb-3` → `mb-5`, `py-5` → `py-12`, `gap-2` → `gap-3`.
Valori più alti (6 e oltre) non esistevano in v5: la nuova scala arriva a `12` (3 rem).

### Colori, tipografia, bordi

| v5 | v6 |
|---|---|
| `text-primary`, `text-secondary`, `text-danger`… | `fg-primary`, `fg-secondary`, `fg-danger`… |
| `text-muted`, `text-body-secondary` | `fg-2` |
| `text-dark`, `text-white` | `fg-black`, `fg-white` |
| `text-bg-primary` | `bg-primary fg-contrast-primary` |
| `bg-light`, `bg-body-tertiary` | `bg-1` / `bg-2` |
| `lead`, `display-5` | `fs-lg fw-light`, `fs-4xl` |
| `fs-1` … `fs-6` | `fs-4xl`, `fs-3xl`, `fs-2xl`, `fs-xl`, `fs-lg`, `fs-md` |
| `lh-base` | `lh-md` |
| `rounded-1/2/3/4` | `rounded-3/4/5/9` (stesso raggio: la scala è 0–9) |
| `mw-100`, `mh-100` | `max-w-100`, `max-h-100` |

### Bottoni, badge, alert, close

| v5 | v6 |
|---|---|
| `btn btn-primary` | `btn-solid theme-primary` |
| `btn btn-outline-primary` | `btn-outline theme-primary` |
| `btn btn-light`, `btn-outline-light` | non esistono (`theme-light`/`theme-dark` neppure): usa `theme-inverse`, `btn-subtle` o le classi del tema `ag-btn-light` |
| `badge text-bg-success` | `badge theme-success` |
| `alert alert-danger alert-dismissible fade show` | `alert theme-danger` + `<button class="btn-close ms-auto" data-bs-dismiss="alert">` |
| `btn-close-white`, SVG dentro `btn-close` | rimossi: l'icona è una maschera CSS che eredita `currentColor` |

I temi disponibili sono `primary`, `accent`, `success`, `danger`, `warning`, `info`, `inverse`, `secondary`.

### Offcanvas → Drawer, Dropdown → Menu, Modal → Dialog

```html
<!-- v5 -->
<button data-bs-toggle="offcanvas" data-bs-target="#nav">…</button>
<div class="offcanvas offcanvas-start" id="nav"> <div class="offcanvas-body">…</div> </div>

<!-- v6: un <dialog> nativo -->
<button data-bs-toggle="drawer" data-bs-target="#nav">…</button>
<dialog class="drawer drawer-start" id="nav"> <div class="drawer-body">…</div> </dialog>
```

- `offcanvas-lg` (sidebar fissa da lg) → `<dialog class="lg:drawer drawer-start">`: da 1024px è un normale
  elemento in flusso (visibile anche senza `open`).
- `dropdown` → `menu`: niente più wrapper `.dropdown` né `.dropdown-toggle`; toggle e `.menu` sono fratelli;
  `dropdown-item` → `menu-item`, `dropdown-divider` → `menu-divider`, `dropdown-item-text` → `menu-text`;
  `dropup`/`dropstart`/`dropend` → `data-bs-placement="top-start|start-start|end-start"`;
  `dropdown-menu-dark` → `data-bs-theme="dark"`; la strategia `fixed` che prima si dava con
  `popperConfig` ora è `data-bs-strategy="fixed"`.
- `modal` → `<dialog class="dialog">` (senza `modal-dialog`/`modal-content`); eventi `show.bs.modal` → `show.bs.dialog`;
  `.modal-open` su `<body>` → `.dialog-open` su `<html>`.
- `data-bs-toggle="collapse"` nella navbar → `data-bs-toggle="drawer"`.
- Attributi e API cambiano nome: `data-bs-toggle="modal|offcanvas|dropdown"` → `"dialog|drawer|menu"`,
  `popperConfig` → `floatingConfig`; `show()`/`hide()`/`toggle()` restituiscono una `Promise`.
- Floating UI sostituisce Popper (`@floating-ui/dom`).

### Form

| v5 | v6 |
|---|---|
| `form-select` | `form-control` anche sul `<select>` |
| `form-check` + `form-check-input` + `form-check-label` | `.form-field` > `input.check` (o `.radio`) + `<label>`; `.switch` come wrapper |
| `mb-3` attorno a ogni campo | `.form-field` (griglia con `gap`) |
| `.was-validated` / `.needs-validation` | `data-bs-validate` sul `<form>` |
| `.has-validation` | rimossa |
| `form-range` su `<input>` | `.form-range` è un wrapper, l'input ha `.form-range-input` |

Con `AgesciFormRenderer` attivo i template del tema fanno già tutto questo (vedi [Form e validazione](forms.md)).

### Breadcrumb

```html
<li class="breadcrumb-item"><a class="breadcrumb-link" href="/">Home</a></li>
<li class="breadcrumb-divider"></li>
<li class="breadcrumb-item" aria-current="page"><span class="breadcrumb-link active">Pagina</span></li>
```

## CSS personalizzato

- **`@layer`**: Bootstrap 6 mette tutto in layer (`colors, config, root, reboot, layout, content, forms, components, custom, helpers, utilities`).
  Il tuo CSS fuori dai layer vince sempre sulle regole normali di Bootstrap (utile per gli override), ma un
  `display:` incondizionato annulla le utility `d-none`/`lg:d-none` del markup. Un `!important` *dentro* un layer batte
  un `!important` *fuori*: per sovrascrivere i pochi `!important` di Bootstrap serve un layer precedente
  (`@layer layout { … !important }`). Vedi [Sviluppo](sviluppo.md).
- **Token**: rimappa il colore con `--bs-primary-base/-bg/-fg/-border/-contrast…`, non con `--bs-primary` / `--bs-primary-rgb`.
- I token root sono su `:root, :host`.
- Il drawer sotto lg è un pannello "floating" (inset + angoli); il tema lo riporta a tutta altezza con
  `--bs-drawer-inset: 0; --bs-drawer-border-radius: 0`.

## Utenti del tema CoreUI

Il pacchetto `django-agesci-campania-coreui-theme` resta su **Bootstrap 5.3 / CoreUI 5** e non dipende dal
markup del tema base: ha copie proprie dei template dei componenti, dei form e di allauth, del JS dei form e dei
partial SCSS. Cosa cambia per te (CoreUI 0.2.0a1, che richiede il tema `>=3.0.0a1`):

- `FORM_RENDERER = "agesci_coreui.forms.AgesciCoreuiFormRenderer"` (non più `agesci_theme.forms.AgesciFormRenderer`).
- `agesci_coreui` deve stare **prima** di `agesci_theme` in `INSTALLED_APPS` (system check `agesci_coreui.E002`).
- Nei tuoi template scrivi direttamente `data-coreui-*`; `{% ag_js %}` non esiste più.

## Strumenti per trovare i residui v5

```bash
rg -n 'modal|offcanvas|dropdown' templates/                       # → dialog / drawer / menu
rg -nE '\b(d|col|row-cols|offset|g)-(sm|md|lg|xl|xxl)-' templates/  # → md:d-none, md:col-6…
rg -nE 'btn-(primary|secondary|outline-)|text-bg-|\btext-(primary|danger|muted)' templates/
rg -nE 'form-select|form-check|was-validated|needs-validation|popperConfig|window\.bootstrap' .
rg -nE 'ag_js|bs-primary-rgb|--bs-link-color-rgb' .
```
