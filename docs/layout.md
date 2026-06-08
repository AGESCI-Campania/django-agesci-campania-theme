# Layout

## Modalità viewport fisso (desktop)

Su schermi di larghezza ≥ 768 px il tema applica un layout a **viewport fisso**:
navbar, breadcrumb, sub-navbar e footer rimangono sempre visibili; solo il
`<main>` scorre internamente quando il contenuto supera lo spazio disponibile.

```
┌──────────────────────────────────┐  ← 100vh
│ Navbar                           │  fisso
├──────────────────────────────────┤
│ Breadcrumb (opzionale)           │  fisso
├──────────────────────────────────┤
│ Sub-navbar (opzionale)           │  fisso
├──────────────────────────────────┤
│                                  │
│  <main> — scorre                 │  flex-grow-1, overflow-y: auto
│                                  │
├──────────────────────────────────┤
│ Footer                           │  fisso
└──────────────────────────────────┘
```

Questo comportamento è generato dal CSS:

```css
/* ≥ 768px */
body { height: 100vh; overflow: hidden; }
main { min-height: 0; overflow-y: auto; }
```

Il `body` usa `d-flex flex-column` (classe Bootstrap applicata nell'HTML);
`main` ha la classe `flex-grow-1` per occupare tutto lo spazio disponibile.

### Perché `min-height: 0` su `<main>`?

Senza di esso un flex-item non può scendere sotto la sua dimensione naturale:
il contenuto spingerebbe `<main>` oltre il viewport e `overflow-y: auto` non
partirebbe mai. `min-height: 0` rimuove questo vincolo e rende lo scroll
effettivo.

### Non usare `min-vh-100` sul body

Applicare `min-vh-100` al body farebbe crescere il body oltre 100vh: il footer
non sarebbe più fisso al fondo del viewport. Usa sempre `height: 100vh`.

---

## Layout mobile (< 768 px)

Su schermi stretti il tema ripristina il **flusso normale del documento**:

- Il body si estende con il contenuto.
- La pagina scorre per intero (non solo il `<main>`).
- Il footer si trova fisicamente in fondo al contenuto HTML, non incollato
  al bordo inferiore del viewport.

Questo è realizzato non applicando le regole di layout fisso:

```css
/* Le due regole seguenti non vengono applicate su mobile */
/* body { height: 100vh; overflow: hidden; }  */
/* main { min-height: 0; overflow-y: auto; }  */
```

Il risultato è un comportamento da "sito web tradizionale", più adatto a
schermi piccoli dove l'altezza disponibile è limitata.

---

## Personalizzare le classi di `<main>`

Il tag `<main>` ha per default le classi `container py-4` (contenuto centrato,
padding verticale). Per cambiarlo usa il blocco `main_class`:

```django
{# Tutta larghezza, nessun padding #}
{% block main_class %}container-fluid p-0{% endblock %}

{# Container normale con classe extra #}
{% block main_class %}container py-4 bg-light rounded{% endblock %}

{# Dashboard a due colonne: sidebar + contenuto #}
{% block main_class %}container-fluid py-3{% endblock %}
{% block content %}
  <div class="row h-100">
    <aside class="col-md-3 border-end">...</aside>
    <section class="col-md-9 overflow-y-auto">...</section>
  </div>
{% endblock %}
```

---

## Breakpoint utilizzati

Il tema usa il breakpoint `md` di Bootstrap (768 px) per distinguere desktop
da mobile. Questo è coerente con il sistema a breakpoint di Bootstrap 5.

| Larghezza | Comportamento |
|---|---|
| `< 768px` | Flusso normale, pagina scorre per intero, footer in fondo al contenuto |
| `≥ 768px` | Viewport fisso, solo `<main>` scorre, footer fisso in basso |
