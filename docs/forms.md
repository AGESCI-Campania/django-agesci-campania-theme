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

## Widget dei componenti form di Bootstrap 6

Bootstrap 6 introduce nuovi controlli per i form: datepicker, OTP input, indicatore di robustezza della
password, form adorn, combobox, chip input e range con bolla. `agesci_theme.forms` li espone come
widget Django. Valgono le stesse regole di `SelectMultiploADiscesa`: sono **opt-in per singolo campo**,
hanno template nel namespace proprio `agesci_theme/forms/...` e **non richiedono** `AgesciFormRenderer`
(il renderer serve solo per le classi e gli errori dei campi normali). Calcolano da soli le classi Bootstrap
e `is-invalid` quando il campo ha errori. Il comportamento è del JS di Bootstrap 6, caricato da `base.html`.

```{important}
Sono widget **solo Bootstrap 6**: il loro markup e il loro JS non esistono in CoreUI 5. Con il tema CoreUI
usa i widget di `agesci_coreui.forms` (es. `InputChip` / `CampoChip`).
```

| Widget | Campo tipico | Componente Bootstrap 6 |
|---|---|---|
| `SelettoreData` | `DateField` | Datepicker (Vanilla Calendar Pro, già nel bundle) |
| `CodiceOTP` | `CharField` | OTP input |
| `PasswordConRobustezza` | `CharField` | Password strength + toggle mostra/nascondi del tema |
| `InputConAdorno` | `CharField`, `DecimalField`, `EmailField`… | Form adorn |
| `Combobox` / `ComboboxMultiplo` | `ChoiceField` / `MultipleChoiceField` | Combobox |
| `InputChip` (con `CampoChip`) | `CampoChip` (lista di stringhe) | Chip input |
| `Cursore` | `IntegerField` | Range |

La demo li usa tutti in `/form-demo/` (`DemoFormBootstrap6` in `example_project/app/views.py`).

### `SelettoreData`

```python
from agesci_theme.forms import SelettoreData

data = forms.DateField(widget=SelettoreData(data_min="2026-01-01", data_max="2026-12-31"))
```

Parametri: `data_min`, `data_max` (`"AAAA-MM-GG"` o `date`) e `locale` (default `"it-IT"`: mesi in
italiano, settimana da lunedì). Il campo mostra `GG/MM/AAAA`. Il server scrive il valore in ISO e il
datepicker lo riformatta. Al submit `value_from_datadict` riconverte `GG/MM/AAAA` in ISO, quindi il
`DateField` lo accetta con qualunque `LANGUAGE_CODE`. Quando c'è già una data, il widget aggiunge
`data-bs-selected-dates`: senza, Bootstrap crea il datepicker solo al primo focus e il campo
mostrerebbe la data in ISO. Gestisce una sola data, non gli intervalli.

### `CodiceOTP`

```python
from agesci_theme.forms import CodiceOTP

codice = forms.CharField(min_length=6, max_length=6, widget=CodiceOTP(gruppi=[3, 3]))
```

Parametri: `lunghezza` (default 6), `tipo` (`"numeric"`, `"alphanumeric"`, `"alpha"`), `gruppi`
(es. `[3, 3]`), `maschera` e `connesso` (default `True`). È un solo `<input>` con
`autocomplete="one-time-code"`. Le caselle le disegna il JS, e incolla e autofill funzionano.
In caso di errore `is-invalid` va sul contenitore `.otp`.

### `PasswordConRobustezza`

```python
from agesci_theme.forms import PasswordConRobustezza

password1 = forms.CharField(widget=PasswordConRobustezza(attrs={"autocomplete": "new-password"}))
```

Ha il toggle mostra/nascondi del tema più la barra a 4 segmenti di Bootstrap 6 con il testo in
italiano (Debole / Sufficiente / Buona / Robusta; si cambia con `messaggi={...}`). `lunghezza_minima`
(default 8) è la soglia del primo segmento. L'indicatore è **solo un aiuto visivo**: la validazione
resta quella di `AUTH_PASSWORD_VALIDATORS`. Lo stesso indicatore c'è anche in `{% ag_password_field strength=True %}`.

### `InputConAdorno`

```python
from agesci_theme.forms import InputConAdorno

quota = forms.DecimalField(localize=True, widget=InputConAdorno(prefisso="€"))
utente = forms.CharField(widget=InputConAdorno(suffisso="@agesci.it"))
cerca = forms.CharField(widget=InputConAdorno(icona=bs_icon("search"), input_type="search"))
```

Accetta `prefisso` **oppure** `suffisso` (testo), oppure `icona` (markup SVG, es. il risultato di
`bs_icon` di `django-bootstrap-icons`). `input_type` imposta il tipo dell'input. L'adorno è
decorativo (`aria-hidden`): il nome del campo resta quello della label del form. Per i decimali con la
virgola usa `localize=True` sul campo.

### `Combobox` e `ComboboxMultiplo`

```python
from agesci_theme.forms import Combobox, ComboboxMultiplo

zona = forms.ChoiceField(choices=ZONE, widget=Combobox(placeholder="Scegli…", ricerca=True))
branche = forms.MultipleChoiceField(choices=BRANCHE, widget=ComboboxMultiplo(placeholder="Nessuna"))
```

`ricerca=True` aggiunge un campo che filtra le voci, e le `choices` raggruppate diventano intestazioni
del menu. Il JS di Bootstrap crea l'`<input type="hidden">` da inviare. Nella variante multipla i
valori sono uniti da virgola e `ComboboxMultiplo` li divide di nuovo. Le scelte con valore vuoto (es.
`"---------"` dei `ModelChoiceField`) sono omesse e al loro posto c'è il placeholder. Bootstrap 6 scrive
nel bottone "*N* selected" in inglese, senza un'opzione per cambiarlo: lo traduce in "*N* selezionate"
`agesci_theme/js/combobox.js`, caricato da `base.html`. Senza JS il campo non invia nulla.

### `InputChip` e `CampoChip`

```python
from agesci_theme.forms import CampoChip, InputChip

tag = CampoChip(required=False, max_chip=5, widget=InputChip(placeholder="Scrivi e premi Invio…"))
```

L'API è la stessa del `CampoChip` di CoreUI: `CampoChip` restituisce una lista di stringhe e
`max_chip` limita le voci sia nel browser sia nella validazione. Bootstrap 6 non crea un campo da
inviare col form: lo mantiene `agesci_theme/js/chip-input.js` (caricato da `base.html`) sull'evento
`change.bs.chips`.

### `Cursore`

```python
from agesci_theme.forms import Cursore

partecipanti = forms.IntegerField(
    min_value=0, max_value=100, step_size=5,
    widget=Cursore(tacche=[(0, "0"), (50, "50"), (100, "100")]),
)
```

È uno slider con la traccia riempita del colore della branca. `bolla` (default `True`) mostra il valore
sopra il cursore, `tacche` è una lista di `(valore, etichetta)` (etichetta vuota = solo tacca).
`min`/`max`/`step` vengono dal campo.
