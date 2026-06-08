# Configurazione

Tutte le impostazioni del tema sono opzionali e si definiscono in `settings.py`
con il prefisso `AGESCI_THEME_`. Se omesse vengono usati i valori predefiniti
(quelli dell'AGESCI Campania).

---

## Riferimento completo

### `AGESCI_THEME_BRANCA`

**Tipo:** `str` — **Default:** `"generico"`

Determina il colore primario dell'intera applicazione. Il valore viene scritto
nell'attributo `data-branca` del tag `<html>` e rimappato via CSS custom
properties senza nessun ricompilo.

| Valore | Colore | Ambito |
|---|---|---|
| `"generico"` | Azzurro `#6689CC` | Default / ufficio / zone |
| `"capi"` | Viola `#7A1E99` | Capi / Comunità Capi |
| `"lc"` | Giallo `#F9D616` | Branca Lupetti/Coccinelle |
| `"eg"` | Verde `#3D8E33` | Branca Esploratori/Guide |
| `"rs"` | Rosso `#EF3340` | Branca Rover/Scolte |
| `"viola"` | Viola `#7A1E99` | Alias esplicito di `"capi"` |

Un valore non riconosciuto ricade silenziosamente su `"generico"`.

```python
AGESCI_THEME_BRANCA = "eg"
```

---

### `AGESCI_THEME_NOME`

**Tipo:** `str` — **Default:** `"AGESCI Campania"`

Nome mostrato nella navbar, nel footer e nel tag `<title>` quando non viene
sovrascritto dal blocco `{% block title %}`.

```python
AGESCI_THEME_NOME = "Zona Vesuvio"
```

---

### `AGESCI_THEME_NAVBAR_TESTO_SCURO`

**Tipo:** `bool` — **Default:** `False`

Forza i link della navbar su testo scuro anziché bianco. Utile quando la
branca ha un colore primario chiaro (es. `lc` = giallo): il testo bianco
risulterebbe illeggibile.

```python
AGESCI_THEME_NAVBAR_TESTO_SCURO = True   # consigliato per branca "lc"
```

Internamente aggiunge la classe `.text-dark` alla navbar, che sovrascrive le
variabili Bootstrap dei link via CSS.

---

### `AGESCI_THEME_LOGO`

**Tipo:** `str` (path relativo a `STATIC`) — **Default:** logo AGESCI Campania

Logo principale (usato eventualmente nel footer o in pagine custom).

```python
AGESCI_THEME_LOGO = "mia_app/img/logo_zona.svg"
```

---

### `AGESCI_THEME_LOGO_NAVBAR`

**Tipo:** `str` (path relativo a `STATIC`) — **Default:** emblema Campania (bianco SVG)

Logo visualizzato nella navbar accanto al nome. L'immagine viene ridimensionata
a 40 px di altezza.

```python
AGESCI_THEME_LOGO_NAVBAR = "mia_app/img/logo_navbar.svg"
```

---

### `AGESCI_THEME_EMBLEMA`

**Tipo:** `str` (path relativo a `STATIC`) — **Default:** emblema Campania PNG

Emblema usato nel footer e nelle view che lo richiamano esplicitamente.

```python
AGESCI_THEME_EMBLEMA = "mia_app/img/emblema_zona.png"
```

---

### `AGESCI_THEME_FAVICON_32` / `AGESCI_THEME_FAVICON_16`

**Tipo:** `str` (path relativo a `STATIC`) — **Default:** favicon AGESCI Campania

Favicon PNG nelle due dimensioni standard (32×32 e 16×16 pixel).

```python
AGESCI_THEME_FAVICON_32 = "mia_app/img/favicon32.png"
AGESCI_THEME_FAVICON_16 = "mia_app/img/favicon16.png"
```

---

## Variabili esposte ai template

Il context processor `agesci_theme.context_processors.agesci_theme` rende
disponibili queste variabili in **ogni template** (nomi in minuscolo):

| Variabile di template | Corrisponde a |
|---|---|
| `agesci_theme_branca` | `AGESCI_THEME_BRANCA` |
| `agesci_theme_nome` | `AGESCI_THEME_NOME` |
| `agesci_theme_logo` | `AGESCI_THEME_LOGO` |
| `agesci_theme_logo_navbar` | `AGESCI_THEME_LOGO_NAVBAR` |
| `agesci_theme_emblema` | `AGESCI_THEME_EMBLEMA` |
| `agesci_theme_favicon_32` | `AGESCI_THEME_FAVICON_32` |
| `agesci_theme_favicon_16` | `AGESCI_THEME_FAVICON_16` |
| `agesci_theme_navbar_testo_scuro` | `AGESCI_THEME_NAVBAR_TESTO_SCURO` |

---

## Esempio completo

```python
# settings.py — sezione tema

AGESCI_THEME_BRANCA              = "eg"
AGESCI_THEME_NOME                = "Zona Partenio"
AGESCI_THEME_NAVBAR_TESTO_SCURO  = False
AGESCI_THEME_LOGO_NAVBAR         = "zona/img/logo_navbar.svg"
AGESCI_THEME_EMBLEMA             = "zona/img/emblema_zona.png"
AGESCI_THEME_FAVICON_32          = "zona/img/favicon32.png"
AGESCI_THEME_FAVICON_16          = "zona/img/favicon16.png"
```
