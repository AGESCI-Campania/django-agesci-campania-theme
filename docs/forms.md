# Form e validazione

Il tema include, opzionalmente, uno styling Bootstrap 6 completo per i form
Django: classi `form-control` (anche per i `<select>`), `check`/`radio` per
checkbox e radio, wrapper `.form-field`, stato `is-invalid`, messaggi di
errore come `invalid-feedback`, e un campo password con pulsante
mostra/nascondi.

---

## Attivazione

Django non renderizza i widget dei form tramite le `TEMPLATES` di progetto:
usa un motore di template separato
(`django.forms.renderers.DjangoTemplates`), la cui `DIRS` punta di default
solo alla directory dei template di Django. Per questo lo styling non è
automatico: va attivato esplicitamente nelle settings del progetto
consumer, impostando il renderer del tema:

```python
FORM_RENDERER = "agesci_theme.forms.AgesciFormRenderer"
```

Vale per **tutti** i form Django del progetto — non solo per i form di
django-allauth (vedi [Integrazione con django-allauth](allauth.md)), è
utile anche a chi non usa affatto allauth.

---

## Cosa cambia visivamente

Con `AgesciFormRenderer` attivo:

- Ogni widget di input riceve `form-control` (anche i `<select>`: in
  Bootstrap 6 `form-select` non esiste più) e i checkbox/radio ricevono
  `check`/`radio` (non più `form-check-input`), più `is-invalid` quando il
  campo ha un errore di validazione.
- `{{ form.as_p }}` avvolge ogni campo in `<div class="form-field mb-5">`
  (la griglia label / controllo / aiuto / errore di Bootstrap 6) invece del
  `<p>` di default di Django. Per i `BooleanField` il controllo viene
  prima della label, che sta in `.form-field-content` insieme ad aiuto ed
  errore (layout a due colonne di Bootstrap 6).
- Gli errori di campo diventano `<div class="invalid-feedback">`; gli
  errori non di campo (`form.non_field_errors`) diventano
  `<div class="alert theme-danger">`.
- I campi `forms.PasswordInput` ricevono un pulsante mostra/nascondi con
  icona SVG inline, dentro un `.input-group`.

---

## Perché `<div class="form-field">` e non `<p>`

Il default `.as_p()` di Django mette gli errori dentro un `<p>` insieme al
campo. Un `<div>` (compreso `.invalid-feedback`) non è "phrasing content":
il parser HTML del browser chiude `</p>` **prima** del div, spostandolo
fuori dal genitore e rompendo silenziosamente l'adiacenza richiesta dal CSS
di Bootstrap (`.is-invalid ~ .invalid-feedback`). Per questo l'override di
`django/forms/p.html` nel tema usa `<div class="form-field mb-5">` al suo posto.
Verificato ispezionando il DOM renderizzato in un browser reale, non
deducibile dal solo sorgente del template.

---

## Perché `.invalid-feedback { display: block; }`

Bootstrap nasconde di default `.invalid-feedback` e lo mostra solo in
posizioni precise rispetto a un controllo `.is-invalid` (fratello
successivo: `.is-invalid ~ .invalid-feedback`; per `.check`/`.radio` e per
l'`.input-group` basta un discendente dello stesso `.form-field`). Il
problema: un wrapper in più attorno al campo (ad es. il multiselect, che è
un `<div>` con dentro il pulsante `.form-control`) rende l'errore **non più
raggiungibile** da quei selettori, e Bootstrap lo nasconderebbe anche
quando presente.

Il tema risolve il problema diversamente da Bootstrap: il div dell'errore
(`django/forms/errors/list/default.html`) viene renderizzato SOLO quando il
campo ha davvero un errore — non serve quindi il meccanismo di occultamento
di Bootstrap. La regola, in `_forms.scss`:

```scss
.invalid-feedback {
  display: block;
}
```

**Non rimuovere questa regola** pensando sia superflua: senza, gli errori
spariscono silenziosamente ogni volta che il campo è avvolto in un wrapper.

---

## Precedenza degli override e come estenderli ulteriormente

`AgesciFormRenderer` usa `DIRS=[THEME_FORMS_DIR, DJANGO_FORMS_TEMPLATES_DIR]`
con `APP_DIRS=True`. `DIRS` è sempre controllata prima di `APP_DIRS`
(comportamento di `django.template.engine.Engine`): gli override del tema
vincono sempre sui template di default di Django.

Conseguenza pratica: un progetto consumer **non può** sovrascrivere questi
template mettendo un proprio `templates/django/forms/...` in un'app
qualsiasi — `APP_DIRS`, in questo motore isolato, non verrà mai interrogato
prima di `DIRS`, indipendentemente dalla posizione dell'app in
`INSTALLED_APPS`.

Per personalizzare ulteriormente, sottoclassare `AgesciFormRenderer` e
anteporre la propria directory a `engine.dirs` (letta dinamicamente dal
loader ad ogni render, quindi sicura da modificare dopo
l'inizializzazione):

```python
from pathlib import Path
from django.utils.functional import cached_property
from agesci_theme.forms import AgesciFormRenderer

class ProgettoFormRenderer(AgesciFormRenderer):
    @cached_property
    def engine(self):
        engine = super().engine
        engine.dirs.insert(0, Path(__file__).resolve().parent / "templates")
        return engine
```

```python
FORM_RENDERER = "config.forms.ProgettoFormRenderer"
```

---

## Il componente `{% ag_password_field %}`

Oltre all'override automatico via `FORM_RENDERER`, il tema espone un
inclusion tag standalone per un campo password con toggle, utilizzabile in
**qualsiasi** form scritto a mano — anche senza attivare `FORM_RENDERER`,
o in progetti che non usano affatto Django Forms per quel campo:

```django
{% load agesci_components %}
{% ag_password_field name="password" label="Password" required=True %}
```

Condivide lo stesso partial del pulsante toggle (icona, comportamento)
dell'override `django/forms/widgets/password.html`, così un campo
disegnato con questo tag e un campo renderizzato via `FORM_RENDERER` sono
visivamente identici. Riferimento completo dei parametri in
[Template tag → `ag_password_field`](templatetags.md).

---

## Icona del toggle password

Il pulsante mostra/nascondi usa un'icona SVG inline, non
`{% bs_icon %}` di `django-bootstrap-icons`. Motivo: il widget
`django/forms/widgets/password.html` è renderizzato dal motore di template
isolato di `AgesciFormRenderer`, che non può assumere disponibile l'extra
opzionale `[icons]` (e un `{% load bootstrap_icons %}` condizionale non è
gestibile in un template). L'SVG inline evita anche una differenza visiva
tra il widget renderizzato via `FORM_RENDERER` e il tag standalone
`{% ag_password_field %}`, che condividono lo stesso partial.

---

## Il widget `SelectMultiploADiscesa`

`agesci_theme.forms.SelectMultiploADiscesa` è un `CheckboxSelectMultiple`
renderizzato come tendina Bootstrap chiusa (bottone + menu con checkbox),
non come elenco checkbox sempre aperto:

```python
from agesci_theme.forms import SelectMultiploADiscesa

interessi = forms.MultipleChoiceField(
    choices=SCELTE,
    required=False,
    widget=SelectMultiploADiscesa(placeholder="Nessuno"),
)
```

A differenza degli altri override di questo documento, **non richiede**
`FORM_RENDERER = "agesci_theme.forms.AgesciFormRenderer"`: i suoi template
vivono in un namespace proprio (`agesci_theme/forms/...`, non
`django/forms/widgets/...`), quindi vengono trovati anche dal renderer di
default di Django, che ha già `APP_DIRS=True` — basta che `agesci_theme`
sia in `INSTALLED_APPS`. È un widget opt-in per singolo campo: le altre
`CheckboxSelectMultiple` del progetto non cambiano comportamento.

Il menu resta aperto durante la selezione di più checkbox
(`data-bs-auto-close="outside"`) e l'etichetta del bottone
si aggiorna via JS (`agesci_theme/static/agesci_theme/js/multiselect-dropdown.js`,
caricato globalmente da `base.html`): placeholder se nessuna opzione è
selezionata, l'etichetta della singola opzione se una sola, altrimenti
"N selezionati".

Il tema espone anche un inclusion tag standalone equivalente, per form
scritti a mano senza passare da `MultipleChoiceField`:

```django
{% load agesci_components %}
{% ag_multiselect_dropdown name="gruppo" label="Gruppo"
   choices=lista_gruppi placeholder="Tutti" %}
```

Il widget è un `<button class="form-control form-control-caret">` seguito da un
`.menu` (Bootstrap 6) con un `.form-field > input.check` per opzione.
Widget e tag condividono lo stesso partial di markup
(`components/_multiselect_dropdown_menu.html`), stessa dualità di
`ag_password_field`/`password.html`. Riferimento completo dei parametri in
[Template tag → `ag_multiselect_dropdown`](templatetags.md).
