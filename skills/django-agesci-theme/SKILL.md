---
name: django-agesci-theme
description: Use and migrate the django-agesci-campania-theme package (Bootstrap 6 theme for AGESCI Campania Django apps, plus the CoreUI variant). Use when writing or editing templates, forms, django-allauth overrides, SCSS or settings in a project that depends on django-agesci-campania-theme or django-agesci-campania-coreui-theme, when upgrading it from 2.x to 3.x, or when a page using the theme renders unstyled or with dead buttons, modals or menus.
---

# django-agesci-campania-theme

Tema **Bootstrap 6 (alpha, 6.0.0-alpha.1)** per le app Django AGESCI Campania. I modelli conoscono Bootstrap 5:
la maggior parte degli errori su questo tema è markup v5 che non dà errori ma non funziona.

Documentazione completa: https://django-agesci-campania-theme.readthedocs.io/it/latest/llms-full.txt
(indice: `.../llms.txt`). Classi e componenti di Bootstrap 6: https://getbootstrap.com/llms.txt

## Prima di scrivere codice

1. Capisci quale tema usa il progetto: `agesci_theme` (Bootstrap 6) o anche `agesci_coreui` (CoreUI 5 su Bootstrap 5.3).
   Sono markup diversi e NON intercambiabili. Con CoreUI gli attributi sono `data-coreui-*`.
2. Leggi il `templates/base.html` del progetto e le `settings.py` (`INSTALLED_APPS`, `FORM_RENDERER`, `AGESCI_THEME_*`).
3. Per classi che non conosci, controlla il CSS di Bootstrap 6 o la tabella in
   `docs/migrazione-bootstrap-6.md`: non dedurle da Bootstrap 5.

## Bootstrap 6 al posto di 5 (tema base)

| Non scrivere (v5) | Scrivi (v6) |
|---|---|
| `d-lg-none`, `col-md-6`, `row-cols-md-3`, `xxl` | `lg:d-none`, `md:col-6`, `md:row-cols-3`, `2xl` (prefisso; `lg` = 1024px) |
| `btn btn-primary` / `btn-outline-primary` | `btn-solid theme-primary` / `btn-outline theme-primary` |
| `badge text-bg-success`, `alert alert-danger` | `badge theme-success`, `alert theme-danger` (+ `btn-close ms-auto`) |
| `btn-light`, `theme-light`, `theme-dark` | non esistono: `theme-inverse`, `btn-subtle`, `ag-btn-light` |
| `text-muted`, `text-primary`, `text-dark`, `lead`, `display-5` | `fg-2`, `fg-primary`, `fg-black`, `fs-lg fw-light`, `fs-4xl` |
| `mb-3`, `py-5`, `gap-2` (stesso rem) | `mb-5`, `py-12`, `gap-3` (scala spacer cambiata) |
| `data-bs-toggle="modal"` / `"offcanvas"` / `"dropdown"` | `"dialog"` / `"drawer"` / `"menu"` |
| `.modal > .modal-dialog > .modal-content` | `<dialog class="dialog">` |
| `.offcanvas` | `<dialog class="drawer drawer-start">` (`offcanvas-lg` → `lg:drawer`) |
| `.dropdown` + `.dropdown-menu` + `.dropdown-item` | toggle + `.menu` fratelli, `.menu-item`; `dropup` → `data-bs-placement="top-start"`; `popperConfig` → `data-bs-strategy="fixed"` |
| `form-select`, `form-check-input` | `form-control` (anche sul select), `input.check` / `input.radio` dentro `.form-field` |
| `window.bootstrap.Modal…` | non esiste: JS solo ESM, `import { … } from "<URL bundle>"` in `<script type="module">` |
| `{% ag_js %}` | rimosso: scrivi `data-bs-*` |

## Regole del tema (violarle non dà errori)

- `INSTALLED_APPS`: `agesci_theme` PRIMA di `allauth`, altrimenti i template allauth del tema restano inapplicati in silenzio.
  Con CoreUI: `agesci_coreui` PRIMA di `agesci_theme` (check `agesci_coreui.E002`).
- `FORM_RENDERER = "agesci_theme.forms.AgesciFormRenderer"` (CoreUI: `agesci_coreui.forms.AgesciCoreuiFormRenderer`).
  È un motore isolato: `templates/django/forms/` del progetto non sovrascrive i suoi widget; si sottoclassa il renderer.
- Un override di `allauth/layouts/base.html` deve estendere `"base.html"` (letterale), mai `"agesci_theme/base.html"`.
- I blocchi del header (`header_nav`, `offcanvas_nav`, `header_search`, `header_actions`) funzionano solo se definiti nel
  template figlio di `base.html`, non dentro un `{% include %}`.
- Commenti Django `{# … #}` su UNA riga: su più righe finiscono nell'HTML.
- Niente link `"/…"` fissi: `{% url %}` o `{% ag_home_url %}`.
- Form: i campi sono avvolti in `<div class="form-field">`, mai `<p>` (il browser chiude il `<p>` e rompe `.invalid-feedback`).
- Colori: niente esadecimali. Il colore segue la branca (`AGESCI_THEME_BRANCA`: `generico, capi, lc, eg, rs, viola, generico2`, scritta in
  `data-branca` su `<html>`): usa `var(--ag-primary)`, `bg-ag-*`/`text-ag-*` o `theme-primary`.
- Il CSS del progetto è fuori dai `@layer` di Bootstrap 6 e li batte: un `display:` incondizionato annulla `d-none`/`lg:d-none`.
- Tema solo chiaro (`data-bs-theme="light"`). Browser minimi: Chrome/Edge 130, Firefox 132, Safari 18.
- Pre-release: `uv add --prerelease allow django-agesci-campania-theme`.

## Componenti

`{% load agesci_components %}`: `ag_hero`, `ag_feature_card`, `ag_feature_grid`, `ag_jumbotron`, `ag_badge`, `ag_button`,
`ag_breadcrumb`, `ag_dropdown`, `ag_list_group`, `ag_modal_trigger`, `ag_masonry_grid`, `ag_password_field`, `ag_multiselect_dropdown`.
`{% load agesci_tags %}`: `emblema_zona`, `zone_disponibili`, `branca_bg`, `ag_home_url`. CoreUI aggiunge `ag_nav_item`, `ag_nav_title`,
`ag_callout`, `ag_avatar`, `ag_chip` (`{% load agesci_coreui %}`). Parametri in `docs/templatetags.md` e `docs/componenti.md`.

## Migrare da 2.x a 3.x

Segui `docs/migrazione-bootstrap-6.md`, nell'ordine:

1. Aggiorna dipendenze e controlla `INSTALLED_APPS`, `FORM_RENDERER`; rimuovi `{% ag_js %}`.
2. Template overridden del progetto (`base.html`, sidebar, header…): applica la tabella sopra. Cerca i residui, per esempio:
   `rg -n '\b(d|col|row-cols|g|ms|me|text)-(sm|md|lg|xl|xxl)-|btn-(primary|outline|light)|text-(muted|bg-)|form-select|form-check|data-bs-toggle="(modal|offcanvas|dropdown|collapse)"|window\.bootstrap|popperConfig' templates/`
3. CSS/SCSS del progetto: niente `--bs-*-rgb` (usa `color-mix()`), breakpoint `lg` 992 → 1024px.
4. Verifica nel browser (desktop e 390px): sidebar, drawer, menu, dialog, form con errori, console senza errori. Le conversioni
   meccaniche delle classi sono sicure; Modal→Dialog, Dropdown→Menu e le spaziature vanno controllate a occhio.
