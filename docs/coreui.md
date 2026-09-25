# Tema CoreUI

`django-agesci-campania-coreui-theme` è la variante **CoreUI 5** del tema:
un secondo pacchetto PyPI, sviluppato nello stesso repository (cartella
`coreui/`), che **estende** `django-agesci-campania-theme` invece di
duplicarlo.

CoreUI è una fork di Bootstrap 5: contiene tutte le classi e i componenti di
Bootstrap, più un layout "admin" nativo (sidebar e header) e componenti
aggiuntivi. Il tema usa solo la **versione free** di CoreUI (licenza MIT); i
componenti **PRO** (date picker, multi select, stepper, ecc.) richiedono una
licenza commerciale e non sono inclusi.

## Cosa viene dal tema base e cosa aggiunge

| Parte | Origine |
|---|---|
| Palette ufficiale, colore per branca (`data-branca`) | tema base, ricompilato sulle variabili `--cui-*` |
| `AgesciFormRenderer`, `SelectMultiploADiscesa`, override django-allauth | tema base, invariati |
| Template tag `agesci_tags` e `agesci_components` (`ag_hero`, `ag_modal_trigger`, …) | tema base: scrivono `data-coreui-*` grazie a `{% ag_js %}` |
| Layout `agesci_coreui/base.html` (sidebar + header nativi CoreUI) | **CoreUI** |
| `{% ag_nav_item %}`, `{% ag_nav_title %}`, `{% ag_callout %}`, `{% ag_avatar %}`, `{% ag_chip %}` | **CoreUI** |
| Widget `InputChip` / campo `CampoChip` (chip-input) | **CoreUI** |

## Installazione

```bash
uv add django-agesci-campania-coreui-theme
# con django-allauth
uv add "django-agesci-campania-coreui-theme[allauth]"
```

`settings.py`:

```python
INSTALLED_APPS = [
    ...,
    "agesci_coreui",
    "agesci_theme",   # obbligatoria (system check agesci_coreui.E001)
    # eventuali app allauth DOPO agesci_theme, come per il tema base
    ...,
]

TEMPLATES = [{"OPTIONS": {"context_processors": [
    ...,
    "agesci_theme.context_processors.agesci_theme",
]}}]

# opzionale, come per il tema base
FORM_RENDERER = "agesci_theme.forms.AgesciFormRenderer"
```

Le settings `AGESCI_THEME_*` (branca, nome, loghi, favicon) sono le stesse
del tema base.

```{important}
Installare `agesci_coreui` sposta **tutto il progetto** su CoreUI: il tag
`{% ag_js %}` fa scrivere ai componenti del tema base `data-coreui-*`
invece di `data-bs-*`, e CoreUI ignora gli attributi `data-bs-*`. Non
mescolare pagine che estendono `agesci_theme/base.html` (Bootstrap) con
pagine CoreUI nello stesso progetto.
```

## Layout

Il `templates/base.html` del progetto estende il layout CoreUI (serve anche
alle pagine allauth, che estendono letteralmente `"base.html"`):

```django
{% extends "agesci_coreui/base.html" %}
{% load agesci_coreui %}

{% block sidebar_items %}
  {% ag_nav_title "Gestione" %}
  {% ag_nav_item "Home" "/" icon="house-fill" %}
  {% ag_nav_item "Iscrizioni" "/iscrizioni/" icon="people-fill" badge="3" %}
{% endblock %}

{% block header_nav %}
  <li class="nav-item"><a class="nav-link" href="/">Home</a></li>
{% endblock %}
```

- **Sidebar** (`.sidebar.sidebar-fixed`): fissa da `lg` (992px) in su,
  comprimibile col pulsante in basso (stato salvato in `localStorage`);
  sotto `lg` è un overlay aperto dall'hamburger dell'header.
- **Header** (`.header.header-sticky`): hamburger, `header_nav`, poi
  `header_search` e `header_actions` a destra; la breadcrumb
  (`breadcrumb_items` nel contesto) appare in una seconda riga.
- Scorre la pagina intera: il layout viewport fisso del tema Bootstrap
  (`.ag-scroll-area`) non si applica.

### Blocchi

Stessi nomi del tema base dove hanno un equivalente: `title`, `extra_head`,
`sidebar`, `brand_url`, `brand_text`, `sidebar_items`, `sidebar_user`,
`header`, `header_nav`, `header_search`, `header_actions`, `main_class`,
`messages`, `content`, `footer`, `footer_copyright`, `footer_links`,
`extra_js`. Nuovo: `sidebar_class` (default `sidebar-dark`; vuoto per la sidebar
chiara di CoreUI).

Non esistono nel layout CoreUI (se definiti in un template figlio vengono
ignorati, senza errori): `offcanvas_nav` (su mobile il menu è la sidebar
stessa), `footer_brand_text`, `footer_columns`, `footer_col*`,
`footer_text`.

### Voci della sidebar

`{% ag_nav_item label url icon="" active=None badge="" badge_variant="primary" %}`
: voce di menu. Se `active` è omesso, la voce è attiva quando `url`
  coincide con `request.path`. `icon` è un nome Bootstrap Icon e richiede
  l'extra `[icons]` del tema base (senza, l'icona è omessa).

`{% ag_nav_title label %}`
: titolo di sezione.

I gruppi annidati usano il markup nativo di CoreUI:

```django
<li class="nav-group">
  <a class="nav-link nav-group-toggle" href="#">Branche</a>
  <ul class="nav-group-items compact">
    {% ag_nav_item "L/C" "/lc/" %}
    {% ag_nav_item "E/G" "/eg/" %}
  </ul>
</li>
```

## Componenti CoreUI

```django
{% load agesci_coreui %}

{% ag_callout title="Attenzione" text="Le iscrizioni chiudono venerdì." variant="warning" %}
{% ag_avatar name="Mario Rossi" status="success" %}
{% ag_avatar name="Anna Bianchi" image_url="/media/anna.jpg" size="lg" %}
{% ag_chip "E/G" variant="success" %}
```

`variant="primary"` (callout, chip) segue sempre il colore della branca. Il
tema rimappa anche le varianti derivate di CoreUI (`--cui-primary-bg-subtle`,
`-text-emphasis`, `-border-subtle`, `-contrast`), quindi alert, list group e
badge "subtle" `primary` seguono la branca invece del viola di default di
CoreUI.

Tutti gli altri componenti free di CoreUI (card, widget, progress, toast,
ecc.) si usano direttamente col markup della
[documentazione CoreUI](https://coreui.io/bootstrap/docs/), ricordando il
prefisso `data-coreui-*`.

## Form: chip-input

```python
from agesci_coreui.forms import CampoChip, InputChip

class EventoForm(forms.Form):
    tag = CampoChip(
        required=False,
        max_chip=5,
        widget=InputChip(placeholder="Scrivi e premi Invio…"),
    )
```

`CampoChip` restituisce una **lista di stringhe** (`cleaned_data["tag"]`).
Invio o la virgola creano un chip, Backspace o la "x" lo rimuovono; il JS di
CoreUI invia i valori in un campo nascosto con lo stesso `name`, separati da
virgola. Come `SelectMultiploADiscesa`, non richiede `AgesciFormRenderer`.

## Il prefisso `data-*`: `{% ag_js %}`

CoreUI legge solo gli attributi `data-coreui-*` (verificato su CoreUI 5.9.0:
un `data-bs-toggle="modal"` non apre il modal). I template condivisi del
tema base scrivono quindi:

```django
{% load agesci_tags %}
<button data-{% ag_js %}-toggle="modal" data-{% ag_js %}-target="#m">…</button>
```

`{% ag_js %}` restituisce `coreui` se `agesci_coreui` è in `INSTALLED_APPS`,
altrimenti `bs`. Non dipende dal contesto, quindi funziona anche negli
inclusion tag e nei template dei widget. Nei **propri** template, un progetto
CoreUI può scrivere direttamente `data-coreui-*`.

## Progetto demo

Demo online (statica): <https://agesci-campania.github.io/django-agesci-campania-theme/coreui/>.

```bash
uv run python example_project/manage.py runserver --settings=config.settings_coreui
```

`config/settings_coreui.py` aggiunge `agesci_coreui` e mette
`app/templates_coreui/` (base, home e componenti in versione CoreUI) prima
di `app/templates/`. La demo form aggiunge un campo `CampoChip`.
