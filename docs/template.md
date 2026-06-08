# Template e blocchi

## Ereditare `base.html`

Tutti i template della tua applicazione devono estendere il base template del tema:

```django
{% extends "agesci_theme/base.html" %}
```

Il `base.html` carica automaticamente Bootstrap 5 (via CDN), i font del Manuale
Immagine Coordinata (Montserrat e Open Sans), il CSS del tema AGESCI e i partial
di navbar e footer.

---

## Struttura HTML generata

```
<html data-branca="...">
  <head>
    Bootstrap CSS · Font · agesci.min.css · [extra_head]
  </head>
  <body class="d-flex flex-column">
    [navbar]
    [breadcrumb]
    [subnav]
    <main class="flex-grow-1 container py-4">
      [messages]
      [content]
    </main>
    [footer]
    Bootstrap JS · [extra_js]
  </body>
</html>
```

---

## Riferimento dei blocchi

### `title`

Testo del tag `<title>`. Il default è il valore di `AGESCI_THEME_NOME`.

```django
{% block title %}Home — {{ agesci_theme_nome }}{% endblock %}
```

---

### `extra_head`

Inserisce contenuto alla fine del `<head>`, prima di `</head>`.
Utile per CSS aggiuntivi, meta tag o script asincroni.

```django
{% block extra_head %}
  <link rel="stylesheet" href="{% static 'mia_app/css/custom.css' %}">
{% endblock %}
```

---

### `navbar`

Sostituisce l'intera barra di navigazione principale. Normalmente non si
sovrascrive questo blocco: si usano invece i sotto-blocchi `brand_url`,
`brand_text` e `nav_items`.

```django
{% block navbar %}
  {# navbar completamente custom #}
{% endblock %}
```

---

### `brand_url`

URL cliccabile del brand nella navbar. Default: `/`.

```django
{% block brand_url %}{% url 'home' %}{% endblock %}
```

---

### `brand_text`

Testo mostrato accanto al logo nella navbar. Default: `agesci_theme_nome`.

```django
{% block brand_text %}Zona Vesuvio — Intranet{% endblock %}
```

---

### `nav_items`

Voci `<li>` all'interno del menu di navigazione. Inserisci elementi Bootstrap
`nav-item`.

```django
{% block nav_items %}
  <li class="nav-item">
    <a class="nav-link {% if request.resolver_match.url_name == 'home' %}active{% endif %}"
       href="{% url 'home' %}">Home</a>
  </li>
  <li class="nav-item">
    <a class="nav-link" href="{% url 'eventi' %}">Eventi</a>
  </li>
{% endblock %}
```

---

### `breadcrumb`

Barra breadcrumb visualizzata sotto la navbar. Il modo consigliato è passare
`breadcrumb_items` dal contesto della view (vedi [Breadcrumb](componenti.md#breadcrumb)).
In alternativa si sovrascrive il blocco:

```django
{% block breadcrumb %}
  {# breadcrumb completamente custom o vuoto per nasconderla #}
{% endblock %}
```

---

### `subnav`

Barra di navigazione secondaria, visualizzata tra breadcrumb e main. Il modo
consigliato è passare `subnav_items` (vedi [Sub-navbar](componenti.md#sub-navbar)).

```django
{% block subnav %}{% endblock %}  {# sovrascrivere per nasconderla #}
```

---

### `main_class`

Classi CSS applicate al tag `<main>`. Il default è `container py-4`, che centra
il contenuto e aggiunge padding verticale.

```django
{# Layout a tutta larghezza senza padding #}
{% block main_class %}container-fluid p-0{% endblock %}

{# Main personalizzato con classe aggiuntiva #}
{% block main_class %}container py-4 mia-classe{% endblock %}
```

---

### `messages`

Mostra i messaggi Django come alert Bootstrap 5 con pulsante di chiusura.
Raramente va sovrascritto; se vuoi nascondere i messaggi:

```django
{% block messages %}{% endblock %}
```

---

### `content`

**Blocco principale**: qui va il contenuto della pagina.

```django
{% block content %}
  <h1>Titolo pagina</h1>
  <p>Contenuto...</p>
{% endblock %}
```

---

### `footer`

Sostituisce l'intero footer. Normalmente si usano i sotto-blocchi:

```django
{% block footer %}
  {# footer completamente custom #}
{% endblock %}
```

---

### `footer_text`

Testo al centro del footer (sotto l'emblema). Default: nome dell'associazione.

```django
{% block footer_text %}
  <p class="mb-0">Zona Vesuvio — AGESCI Campania</p>
{% endblock %}
```

---

### `footer_links`

Link visualizzati nella colonna destra del footer.

```django
{% block footer_links %}
  <ul class="list-unstyled mb-0">
    <li><a href="/privacy/">Privacy</a></li>
    <li><a href="/contatti/">Contatti</a></li>
  </ul>
{% endblock %}
```

---

### `extra_js`

Inserisce script prima di `</body>`, dopo Bootstrap JS.

```django
{% block extra_js %}
  <script src="{% static 'mia_app/js/custom.js' %}"></script>
{% endblock %}
```

---

## Tabella riepilogativa

| Blocco | Posizione | Caso d'uso tipico |
|---|---|---|
| `title` | `<title>` | Titolo pagina |
| `extra_head` | fine `<head>` | CSS, meta aggiuntivi |
| `navbar` | barra principale | Sostituzione completa navbar |
| `brand_url` | link brand navbar | URL homepage custom |
| `brand_text` | testo brand navbar | Nome sezione/zona |
| `nav_items` | voci menu `<li>` | Voci di navigazione |
| `breadcrumb` | sotto navbar | Override breadcrumb |
| `subnav` | sotto breadcrumb | Override sub-navbar |
| `main_class` | classi `<main>` | Layout a tutta larghezza |
| `messages` | sopra content | Nascondere i flash |
| `content` | corpo pagina | **Contenuto principale** |
| `footer` | fondo pagina | Sostituzione completa footer |
| `footer_text` | centro footer | Nome / slogan |
| `footer_links` | colonna destra footer | Link policy/contatti |
| `extra_js` | fine `<body>` | Script custom |

---

## Note sulla retrocompatibilità

I nomi dei blocchi sono stabili: applicazioni che già estendono `base.html`
continueranno a funzionare senza modifiche al passaggio a versioni successive
del tema.
