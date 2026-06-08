# Template tag

I template tag del tema si caricano con:

```django
{% load agesci_tags %}
```

---

## `emblema_zona`

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

{# Emblema con dimensioni Bootstrap responsive #}
{% emblema_zona "vesuvio" css_class="img-fluid" %}

{# Emblema con alt custom e classe di dimensione #}
{% emblema_zona "napoli" css_class="img-thumbnail" alt="Emblema Zona Napoli" %}

{# Emblema inline piccolo #}
{% emblema_zona "salerno" css_class="d-inline" %}
<span>Zona Salerno</span>
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

Se la chiave non è riconosciuta il tag restituisce una stringa vuota (nessun
errore).

---

## `zone_disponibili`

Restituisce la lista ordinata alfabeticamente delle chiavi di zona disponibili.
Utile per costruire dinamicamente menu o select.

```
{% zone_disponibili as zone %}
```

**Esempio:**

```django
{% load agesci_tags %}
{% zone_disponibili as zone %}

<select name="zona" class="form-select">
  {% for zona in zone %}
    <option value="{{ zona }}">{{ zona|title }}</option>
  {% endfor %}
</select>
```

---

(branca-bg)=
## `branca_bg`

Restituisce la classe CSS di background corrispondente alla branca attiva nel
contesto corrente.

```
{% branca_bg %}
```

Il tag legge `agesci_theme_branca` dal contesto (iniettato dal context
processor): non richiede parametri.

**Esempio:**

```django
{% load agesci_tags %}

<span class="badge {% branca_bg %}">
  Branca corrente
</span>

<div class="card">
  <div class="card-header {% branca_bg %}">
    Intestazione colorata
  </div>
  <div class="card-body">
    Contenuto della card
  </div>
</div>
```

**Corrispondenza branca → classe:**

| Branca | Classe CSS |
|---|---|
| `generico` | `bg-ag-azzurro` |
| `capi` | `bg-ag-viola` |
| `viola` | `bg-ag-viola` |
| `lc` | `bg-ag-giallo-lc` |
| `eg` | `bg-ag-verde-eg` |
| `rs` | `bg-ag-rosso-rs` |

Vedi [Classi utility palette](palette.md#classi-utility) per l'elenco completo.
