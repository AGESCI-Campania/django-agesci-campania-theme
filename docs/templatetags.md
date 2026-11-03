# Template tag

Il tema fornisce due moduli di template tag.

---

## `agesci_tags`

Tag di utilità generale. Si caricano con:

```django
{% load agesci_tags %}
```

---

### `emblema_zona`

Restituisce un tag `<img>` con l'emblema di una Zona Scout della Campania.

```
{% emblema_zona zona [css_class=""] [alt=""] %}
```

**Parametri:**

| Parametro | Tipo | Obbligatorio | Descrizione |
|---|---|---|---|
| `zona` | `str` | Sì | Chiave della zona (vedi tabella) |
| `css_class` | `str` | No | Classi CSS aggiuntive all'`<img>` |
| `alt` | `str` | No | Testo alternativo (default: `"Zona <nome>"`) |

**Esempio:**

```django
{% load agesci_tags %}

{% emblema_zona "vesuvio" css_class="img-fluid" %}
{% emblema_zona "napoli" css_class="img-thumbnail" alt="Emblema Zona Napoli" %}
```

**Zone disponibili:**

| Chiave | Zona |
|---|---|
| `caserta` | Zona Caserta |
| `faito` | Zona Faito |
| `felix` | Zona Felix |
| `hirpinia` | Zona Hirpinia |
| `liternum` | Zona Liternum |
| `napoli` | Zona Napoli |
| `poseidonia` | Zona Poseidonia |
| `salerno` | Zona Salerno |
| `samnium` | Zona Samnium |
| `vesuvio` | Zona Vesuvio |
| `volturno` | Zona Volturno |

---

### `zone_disponibili`

Restituisce la lista ordinata alfabeticamente delle chiavi di zona.

```django
{% zone_disponibili as zone %}

<select name="zona" class="form-control">
  {% for zona in zone %}
    <option value="{{ zona }}">{{ zona|title }}</option>
  {% endfor %}
</select>
```

---

(branca-bg)=
### `branca_bg`

Restituisce la classe CSS di background corrispondente alla branca attiva.

```django
{% load agesci_tags %}

<span class="badge {% branca_bg %}">Branca corrente</span>
```

**Corrispondenza branca → classe:**

| Branca | Classe CSS |
|---|---|
| `generico` | `bg-ag-azzurro` |
| `capi` | `bg-ag-viola` |
| `viola` | `bg-ag-viola` |
| `generico2` | `bg-ag-generico-2` |
| `lc` | `bg-ag-giallo-lc` |
| `eg` | `bg-ag-verde-eg` |
| `rs` | `bg-ag-rosso-rs` |

---

(agesci-components)=
## `agesci_components`

Componenti UI opzionali implementati come `inclusion_tag`. Si caricano con:

```django
{% load agesci_components %}
```

I template dei componenti si trovano in `agesci_theme/components/` e sono
sovrascrivibili creando file con lo stesso percorso nel progetto figlio.

---

### `ag_hero`

Sezione hero di apertura pagina.

```
{% ag_hero [title=""] [subtitle=""] [cta_text=""] [cta_url="#"] [variant="subtle"] [image_url=""] %}
```

| Parametro | Default | Descrizione |
|---|---|---|
| `title` | `""` | Titolo principale (`<h1>`) |
| `subtitle` | `""` | Testo lead |
| `cta_text` | `""` | Testo pulsante call-to-action (non mostrato se vuoto) |
| `cta_url` | `"#"` | URL del pulsante |
| `variant` | `"subtle"` | `"subtle"` · `"primary"` · `"dark"` · `"centered"` |
| `image_url` | `""` | URL immagine (layout a due colonne se valorizzato) |

```django
{% ag_hero title="Benvenuti" subtitle="AGESCI Campania — Regione Campania"
           cta_text="Scopri di più" cta_url="/chi-siamo/" variant="subtle" %}
```

---

### `ag_feature_card`

Card singola per sezioni feature (icona + titolo + descrizione).

```
{% ag_feature_card [title=""] [description=""] [icon=""] [variant=""] %}
```

| Parametro | Descrizione |
|---|---|
| `icon` | Nome icona Bootstrap (es. `"star-fill"`) |
| `variant` | Classe colore icona (es. `"fg-primary"`; in Bootstrap 6 `text-primary` non esiste più) |

```django
{% ag_feature_card icon="people-fill" title="Comunità" description="Oltre 180.000 soci in Italia." %}
```

---

### `ag_feature_grid`

Griglia di feature card.

```
{% ag_feature_grid items [cols=3] %}
```

| Parametro | Descrizione |
|---|---|
| `items` | Lista di dict con chiavi `title`, `description`, `icon`, `variant` (opt.) |
| `cols` | Colonne su desktop: `2`, `3` (default) o `4` |

```python
# views.py
features = [
    {"icon": "people-fill", "title": "Comunità",   "description": "..."},
    {"icon": "geo-alt-fill","title": "Territorio", "description": "..."},
    {"icon": "star-fill",   "title": "Formazione", "description": "..."},
]
```

```django
{% ag_feature_grid items=features cols=3 %}
```

---

### `ag_jumbotron`

Jumbotron (rimosso da Bootstrap 6, riproposto come componente custom).

```
{% ag_jumbotron [title=""] [lead=""] [cta_text=""] [cta_url="#"] [variant=""] %}
```

| `variant` | Sfondo |
|---|---|
| `""` (default) | `--ag-primary-subtle` |
| `"primary"` | `--ag-primary` |

```django
{% ag_jumbotron title="Unisciti a noi" lead="Entra nel movimento scout più grande d'Italia."
                cta_text="Contattaci" cta_url="/contatti/" %}
```

---

### `ag_badge`

Badge Bootstrap con colori del tema (`badge theme-<variant>`). Bootstrap 6 non ha
`theme-light`/`theme-dark`: `variant="dark"` diventa `theme-inverse` e
`variant="light"` diventa `theme-secondary`; lo stesso vale per `ag_button`,
`ag_dropdown` e `ag_modal_trigger`.

```
{% ag_badge [text=""] [variant="primary"] [pill=False] %}
```

```django
{% ag_badge text="Nuovo" variant="primary" pill=True %}
{% ag_badge text="Attenzione" variant="warning" %}
```

---

### `ag_button`

Bottone Bootstrap 6 (`btn-solid`/`btn-outline` + `theme-<variant>`; renderizza
`<button>` o `<a>` se `href` è valorizzato).

```
{% ag_button [label=""] [variant="primary"] [size=""] [outline=False] [href=""] [type="button"] %}
```

```django
{% ag_button label="Salva" variant="primary" %}
{% ag_button label="Annulla" variant="secondary" outline=True %}
{% ag_button label="Apri sito" variant="primary" href="https://www.agesci.it" %}
{% ag_button label="Small" variant="success" size="sm" %}
```

---

### `ag_breadcrumb`

Breadcrumb con stile del tema.

```
{% ag_breadcrumb [items=None] %}
```

| Parametro | Descrizione |
|---|---|
| `items` | Lista di dict `{"label": "...", "url": "..."}`. L'ultimo elemento è sempre `active` (senza link). |

```python
# views.py
breadcrumb_items = [
    {"label": "Home",    "url": "/"},
    {"label": "Eventi",  "url": "/eventi/"},
    {"label": "Dettaglio"},
]
```

```django
{% ag_breadcrumb items=breadcrumb_items %}
```

:::{tip}
Se passi `breadcrumb_items` come variabile di contesto dalla view, l'header
la mostra automaticamente nella barra inferiore (`ag-header-bottom`), senza
bisogno del tag `{% ag_breadcrumb %}` nel contenuto. Usa questo tag solo se
preferisci posizionare la breadcrumb manualmente all'interno del blocco `content`.
:::

---

### `ag_dropdown`

Menu Bootstrap 6 (ex dropdown: `data-bs-toggle="menu"` + `.menu`). Il nome del tag è
rimasto `ag_dropdown`.

```
{% ag_dropdown [label=""] [items=None] [variant="primary"] [split=False] [direction=""] %}
```

| Parametro | Descrizione |
|---|---|
| `items` | Lista di dict con `label`, `url`, `active` (opt.), `disabled` (opt.). Usa `{"divider": True}` per un separatore. |
| `split` | `True` per bottone split (freccia separata) |
| `direction` | `""` · `"dropup"` · `"dropstart"` · `"dropend"` (diventano `data-bs-placement` `top-start` · `start-start` · `end-start`) |

```python
voci = [
    {"label": "Profilo",     "url": "/profilo/"},
    {"label": "Impostazioni","url": "/impostazioni/"},
    {"divider": True},
    {"label": "Esci",        "url": "/logout/"},
]
```

```django
{% ag_dropdown label="Account" items=voci variant="primary" %}
```

---

### `ag_list_group`

List group Bootstrap.

```
{% ag_list_group [items=None] [flush=False] [numbered=False] %}
```

| Parametro | Descrizione |
|---|---|
| `items` | Lista di dict con `label`, `url` (opt.), `active` (opt.), `disabled` (opt.), `badge` (opt.) |
| `flush` | `True` per rimuovere i bordi laterali |
| `numbered` | `True` per lista numerata |

```python
voci = [
    {"label": "Branca L/C", "badge": "12"},
    {"label": "Branca E/G", "badge": "8", "active": True},
    {"label": "Branca R/S", "badge": "5"},
]
```

```django
{% ag_list_group items=voci %}
{% ag_list_group items=voci flush=True %}
```

---

### `ag_modal_trigger`

Bottone che apre un dialog Bootstrap 6 (ex modal: `<dialog class="dialog">`,
`data-bs-toggle="dialog"`). Il nome del tag è rimasto `ag_modal_trigger`.

```
{% ag_modal_trigger modal_id [label="Apri"] [variant="primary"] [size=""] %}
```

Va accoppiato con il template `agesci_theme/components/modal.html` tramite `{% include %}`:

```django
{# Pulsante trigger #}
{% ag_modal_trigger modal_id="conferma" label="Conferma" %}

{# Shell del dialog (in fondo alla pagina, fuori dal flusso) #}
{% include "agesci_theme/components/modal.html" with
    modal_id="conferma"
    title="Conferma operazione"
    body="<p>Sei sicuro di voler procedere?</p>"
    size="sm" %}
```

Per contenuto più complesso, prepara il corpo nella view come stringa `mark_safe`:

```python
from django.utils.safestring import mark_safe

context["modal_body"] = mark_safe("<p>Contenuto <strong>HTML</strong>.</p>")
```

```django
{% include "agesci_theme/components/modal.html" with
    modal_id="info" title="Informazioni" body=modal_body %}
```

**Parametri di `modal.html`:**

| Parametro | Default | Descrizione |
|---|---|---|
| `modal_id` | — | ID univoco (obbligatorio) |
| `title` | `""` | Titolo nell'intestazione |
| `body` | `""` | Corpo (HTML come `mark_safe`) |
| `size` | `""` | `"sm"` · `"lg"` · `"xl"` · `"fullscreen"` |
| `centered` | — | **Rimosso nella 3.0**: il `<dialog>` nativo è già centrato |

---

### `ag_masonry_grid`

Griglia Masonry a cascata.

```
{% ag_masonry_grid [items=None] [cols=3] %}
```

**Requisito:** la libreria JavaScript Masonry deve essere caricata nel blocco
`extra_js` del template che usa il componente:

```django
{% block extra_js %}{{ block.super }}
<script src="https://cdn.jsdelivr.net/npm/masonry-layout@4/dist/masonry.pkgd.min.js" defer></script>
{% endblock %}
```

**Parametri:**

| Parametro | Descrizione |
|---|---|
| `items` | Lista di dict con chiave `content` (HTML come `mark_safe`) |
| `cols` | Colonne su desktop: `2`, `3` (default) o `4` |

```python
from django.utils.safestring import mark_safe

items = [
    {"content": mark_safe('<div class="card"><div class="card-body">Contenuto 1</div></div>')},
    {"content": mark_safe('<div class="card"><div class="card-body">Contenuto 2<br>più alto</div></div>')},
]
```

```django
{% ag_masonry_grid items=masonry_items cols=3 %}
```

---

### `ag_password_field`

Campo password con pulsante mostra/nascondi (icona SVG inline, nessuna
dipendenza da `[icons]`). Utilizzabile in qualsiasi form scritto a mano,
**senza** bisogno di attivare `FORM_RENDERER` — vedi
[Form e validazione](forms.md) per il meccanismo `AgesciFormRenderer`, di
cui questo componente condivide il markup del toggle.

```
{% ag_password_field [name="password"] [id=""] [label=""] [value=""]
                      [placeholder=""] [help_text=""] [errors=None]
                      [required=False] [autocomplete="current-password"]
                      [strength=False] [min_length=8] %}
```

| Parametro | Default | Descrizione |
|---|---|---|
| `name` | `"password"` | Attributo `name` dell'`<input>` |
| `id` | `"id_" + name` | Attributo `id`, per l'associazione con `<label>` |
| `label` | `""` | Etichetta (non mostrata se vuota) |
| `errors` | `None` | Lista di messaggi d'errore: se non vuota, mostra `is-invalid` + `invalid-feedback` |
| `required` | `False` | Aggiunge `required` all'`<input>` e `*` all'etichetta |
| `autocomplete` | `"current-password"` | Usa `"new-password"` in un form di registrazione |
| `strength` | `False` | Aggiunge l'indicatore di robustezza di Bootstrap 6 (come il widget `PasswordConRobustezza`; solo tema Bootstrap 6) |
| `min_length` | `8` | Con `strength`: lunghezza minima per il primo segmento |

```django
{% load agesci_components %}
{% ag_password_field name="password" label="Password" required=True %}
```

Con un form Django, passa i valori dal campo esplicitamente:

```django
{% ag_password_field name=form.password.html_name id=form.password.id_for_label
   label=form.password.label value=form.password.value
   errors=form.password.errors required=form.password.field.required %}
```

---

### `ag_multiselect_dropdown`

Tendina Bootstrap chiusa con checkbox multiple (bottone `form-control` + `.menu`,
`data-bs-auto-close="outside"`). Utilizzabile in qualsiasi form scritto a
mano, **senza** bisogno di attivare `FORM_RENDERER` — vedi
[Form e validazione](forms.md) per il widget equivalente
`SelectMultiploADiscesa`, di cui questo componente condivide il markup del
menu.

```
{% ag_multiselect_dropdown name [id=""] [label=""] [choices=None]
                            [selected=None] [placeholder=""]
                            [help_text=""] [errors=None] [required=False] %}
```

| Parametro | Default | Descrizione |
|---|---|---|
| `name` | — | Attributo `name` di ogni `<input type="checkbox">` |
| `id` | `"id_" + name` | Id del bottone, per l'associazione con `<label>` |
| `label` | `""` | Etichetta (non mostrata se vuota) |
| `choices` | `None` | Lista di tuple `(value, label)`, come le `choices` di Django |
| `selected` | `None` | Lista di `value` già selezionati |
| `placeholder` | `""` | Testo del bottone quando nessuna opzione è selezionata |
| `errors` | `None` | Lista di messaggi d'errore: se non vuota, mostra `is-invalid` + `invalid-feedback` |
| `required` | `False` | Aggiunge `*` all'etichetta |

```django
{% load agesci_components %}
{% ag_multiselect_dropdown name="gruppo" label="Gruppo"
   choices=lista_gruppi placeholder="Tutti" %}
```

---

## Componenti nuovi di Bootstrap 6

I tag che seguono producono markup **Bootstrap 6** e stanno sempre in `agesci_components`.
`ag_avatar` e `ag_chip` hanno la stessa firma degli omonimi CoreUI, e il tema CoreUI ha una copia
propria dei loro template: danno l'avatar e il chip di CoreUI. Accordion, stepper e carousel invece
sono **solo per il tema Bootstrap 6**.

### `ag_accordion`

È un accordion fatto con `<details>` nativi, senza JS.

```
{% ag_accordion items [id=""] [always_open=False] [flush=False] [gap=False] [size=""] [variant=""] %}
```

| Parametro | Default | Descrizione |
|---|---|---|
| `items` | — | Lista di dict `title`, `content` (HTML con `mark_safe`), `open` (opzionale) |
| `id` | generato | `name` comune dei `<details>`: rende le voci esclusive |
| `always_open` | `False` | `True` per lasciare aperte più voci insieme |
| `flush` / `gap` | `False` | Senza bordi esterni / voci separate |
| `size` | `""` | `"sm"` per la versione compatta |
| `variant` | `""` | Colore della voce aperta, es. `"primary"` (branca) |

```django
{% ag_accordion items=faq variant="primary" %}
```

### `ag_avatar`

```
{% ag_avatar [name=""] [image_url=""] [size="md"] [status=""] [variant="primary"] [subtle=False] %}
```

| Parametro | Default | Descrizione |
|---|---|---|
| `name` | `""` | Nome: dà le iniziali e il testo alternativo |
| `image_url` | `""` | Immagine al posto delle iniziali |
| `size` | `"md"` | `"xs"`, `"sm"`, `"md"`, `"lg"`, `"xl"` |
| `status` | `""` | `"online"`, `"away"`, `"busy"`, `"offline"` (o i nomi CoreUI `success`, `warning`, `danger`, `secondary`) |
| `variant` / `subtle` | `"primary"` / `False` | Colore delle iniziali; `subtle=True` per la versione tenue |

```django
{% ag_avatar name="Anna Bianchi" status="online" size="lg" %}
```

### `ag_chip`

```
{% ag_chip label [variant=""] [icon=""] [active=False] %}
```

È un chip statico. `variant` (`"primary"` = branca, `"success"`…) dà il colore tenue, `active=True` la
versione piena, `icon` un Bootstrap Icon (richiede l'extra `[icons]`). Per i chip modificabili in un
form usa il widget `InputChip` ([Form](forms.md#widget-dei-componenti-form-di-bootstrap-6)).

### `ag_stepper`

```
{% ag_stepper steps [current=1] [vertical=False] %}
```

| Parametro | Default | Descrizione |
|---|---|---|
| `steps` | — | Lista di stringhe, o di dict `label` + `url` (con un `url` i passi diventano link) |
| `current` | `1` | Numero (da 1) del passo corrente: i passi fino a lui sono colorati; `0` = nessuno |
| `vertical` | `False` | Elenco verticale (di default orizzontale, scorrevole se non ci sta) |

```python
# views.py
context = {"passi": ["Dati personali", "Gruppo", "Quota", "Conferma"]}
```

```django
{% ag_stepper steps=passi current=2 %}
```

### `ag_carousel`

```
{% ag_carousel items [id=""] [indicators=True] [autoplay=False] [interval=5000] [fade=False] %}
```

| Parametro | Default | Descrizione |
|---|---|---|
| `items` | — | Lista di dict `image_url`, `alt`, `title` e `text` (opzionali, didascalia in basso) |
| `id` | generato | `id` del carousel, usato da controlli e indicatori |
| `indicators` | `True` | Pallini di navigazione |
| `autoplay` / `interval` | `False` / `5000` | Scorrimento automatico, con il pulsante pausa/riproduci richiesto da WCAG 2.2.2 |
| `fade` | `False` | Dissolvenza invece dello scorrimento |

Il carousel di Bootstrap 6 usa lo scroll-snap del browser. Non ha più `.carousel-caption`: la
didascalia è `.ag-carousel-caption` del tema.
