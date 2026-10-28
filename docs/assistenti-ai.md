# Usare il tema con un assistente AI

Questa pagina raccoglie le regole che un assistente AI (Claude Code, Copilot, Cursor…)
deve conoscere per scrivere codice corretto con il tema. Il tema è su **Bootstrap 6**
(alpha), che i modelli conoscono poco: il loro istinto è scrivere Bootstrap 5, e il
risultato non dà errori ma esce rotto (classi che non fanno nulla, modal che non si aprono).

## Come darle all'assistente

- **Indice per LLM**: [`llms.txt`](https://django-agesci-campania-theme.readthedocs.io/it/latest/llms.txt)
  (elenco delle pagine) e [`llms-full.txt`](https://django-agesci-campania-theme.readthedocs.io/it/latest/llms-full.txt)
  (tutto il manuale in un file), generati dai sorgenti di questa documentazione.
- **Skill** per Claude Code e altri agenti compatibili, da installare nel *tuo* progetto:

  ```bash
  npx skills add AGESCI-Campania/django-agesci-campania-theme
  ```

- **Bootstrap 6**: per le classi e i componenti in sé c'è l'indice ufficiale
  [`getbootstrap.com/llms.txt`](https://getbootstrap.com/llms.txt).
- In alternativa copia le regole qui sotto nel `CLAUDE.md` / `AGENTS.md` del tuo progetto.

## Regole da rispettare

### Bootstrap 6, non 5

- Il tema carica `bootstrap@6.0.0-alpha.1` da CDN. Nessuna classe o attributo di Bootstrap 5
  va dato per buono: se non sei sicuro, controlla il [CSS](https://getbootstrap.com/llms.txt) o la
  [tabella di conversione](migrazione-bootstrap-6.md).
- Responsive **a prefisso**: `lg:d-none`, `md:col-6` (mai `d-lg-none`, `col-md-6`). Breakpoint: `lg` = 1024px, `2xl` (non `xxl`).
- Colori e bottoni con `theme-*`: `btn-solid theme-primary`, `btn-outline theme-secondary`,
  `badge theme-success`, `alert theme-danger`. Non esistono `btn-primary`, `text-bg-*`, `btn-light`.
- Testo: `fg-*` e `fs-*` (non `text-muted`, `text-primary`, `lead`, `display-*`).
- Spaziature: la scala è cambiata (`mb-3` di v5 è `mb-5`).
- Modal, offcanvas, dropdown sono ora `<dialog class="dialog">`, `<dialog class="drawer">` e `.menu`
  (`data-bs-toggle="dialog|drawer|menu"`). `data-bs-toggle="modal|offcanvas|dropdown"` non funziona.
- Il JavaScript è solo ESM (`<script type="module">`): **non esiste `window.bootstrap`**. Per l'API JS
  si fa `import { … } from "<URL del bundle>"`; la data API (`data-bs-*`) si attiva da sola.
- Form: il `<select>` ha `form-control` (non `form-select`); checkbox e radio sono `input.check` / `input.radio`
  dentro `.form-field` (non `form-check`).
- Browser minimi: Chrome/Edge 130, Firefox 132, Safari 18.

### Configurazione

- `INSTALLED_APPS`: **`agesci_theme` prima di `allauth`**, altrimenti i template di allauth vincono sugli
  override del tema, senza alcun errore (le pagine escono senza stile).
- Context processor: `agesci_theme.context_processors.agesci_theme`.
- Form Django e allauth: `FORM_RENDERER = "agesci_theme.forms.AgesciFormRenderer"`. È un motore di template
  isolato: un `templates/django/forms/…` del progetto NON sovrascrive i suoi widget (per farlo si sottoclassa il renderer).
- Pre-release: `uv add --prerelease allow django-agesci-campania-theme` / `pip install --pre …`.
- Con **CoreUI** (pacchetto separato, Bootstrap 5.3): `agesci_coreui` va **prima** di `agesci_theme`, gli attributi
  sono `data-coreui-*` e il renderer è `agesci_coreui.forms.AgesciCoreuiFormRenderer`. Il markup dei due temi non è intercambiabile.

### Template

- Estendi `base.html` (il tuo, che a sua volta estende `agesci_theme/base.html`) e usa i blocchi esistenti:
  `title`, `extra_head`, `header`, `header_nav`, `offcanvas_nav`, `header_search`, `header_actions`, `sidebar`,
  `sidebar_items`, `sidebar_user`, `main_class`, `messages`, `content`, `footer*`, `extra_js`, `bootstrap_css`, `bootstrap_js`.
- Un template di allauth che sovrascrivi deve estendere `"base.html"` (letterale), non `"agesci_theme/base.html"`.
- I commenti Django `{# … #}` stanno su **una riga sola**: su più righe il testo finisce nell'HTML, senza errori.
- Link interni con `{% url %}` o `{% ag_home_url %}`, mai `"/…"` fissi.
- Breadcrumb: `breadcrumb_items` nel contesto della view (lista di `{"label", "url"}`; l'ultimo senza link).

### Colore e stile

- Il colore dipende dalla branca (`AGESCI_THEME_BRANCA`: `generico`, `capi`, `lc`, `eg`, `rs`, `viola`, `generico2`)
  tramite `data-branca` su `<html>`. **Non scrivere colori esadecimali**: usa `var(--ag-primary)` e derivati,
  le utility `bg-ag-*` / `text-ag-*` o le classi `theme-primary`. La palette è ufficiale (Manuale Immagine Coordinata 2011).
- Il CSS del tema è fuori dai `@layer` di Bootstrap 6, quindi vince sulle sue regole normali: un `display:` incondizionato
  nel tuo CSS batte `d-none` e `lg:d-none`. Dichiaralo solo nella media query in cui serve.
- Il tema è solo chiaro: `<html data-bs-theme="light">`.

### Componenti

Per tabelle, card o altro che il tema non fornisce, usa i componenti di Bootstrap 6. Quelli del tema sono tag
(`{% load agesci_components %}`): `ag_hero`, `ag_feature_card`, `ag_feature_grid`, `ag_jumbotron`, `ag_badge`, `ag_button`,
`ag_breadcrumb`, `ag_dropdown`, `ag_list_group`, `ag_modal_trigger`, `ag_masonry_grid`, `ag_password_field`,
`ag_multiselect_dropdown`; in `agesci_tags`: `emblema_zona`, `zone_disponibili`, `branca_bg`, `ag_home_url`.
Parametri e esempi in [Template tag](templatetags.md) e [Componenti](componenti.md).

## Per chi aggiorna da una 2.x

Segui la [guida alla migrazione](migrazione-bootstrap-6.md): ha le tabelle di conversione v5 → v6 e i comandi `rg`
per trovare i residui. Un assistente può applicarla in modo meccanico, ma la scala delle spaziature e i
passaggi Modal→Dialog / Dropdown→Menu vanno ricontrollati nel browser.
