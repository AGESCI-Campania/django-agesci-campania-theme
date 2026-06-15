# Layout

## Modalità viewport fisso (desktop)

Su schermi di larghezza ≥ 992 px (breakpoint `lg` di Bootstrap) il tema
applica un layout a **viewport fisso**: header e footer rimangono sempre
visibili; solo il `<main>` scorre internamente.

### Senza sidebar (default)

```
┌──────────────────────────────────────┐  ← 100vh
│ Header (barra sup. + barra inf.)     │  fisso
├──────────────────────────────────────┤
│                                      │
│  .ag-scroll-area — scorre ↕          │  flex-grow-1, overflow-y: auto
│    <main class="container …">        │  larghezza max limitata da .container
│    <footer>                          │  larghezza completa dell'area
│                                      │
└──────────────────────────────────────┘
```

### Con sidebar attivata

```
┌──────────────────────────────────────┐  ← 100vh
│ Header                               │  fisso
├──────────┬───────────────────────────┤
│          │                           │
│ Sidebar  │  .ag-scroll-area — scorre │
│ (240px)  │    <main>                 │
│  fisso   │    <footer>               │
│          │                           │
└──────────┴───────────────────────────┘
```

La sidebar è attivata sovrascrivendo il blocco `sidebar` (vuoto di default).
Vedi [Sidebar](componenti.md#sidebar).

---

## Layout mobile (< 992 px)

Su schermi stretti il tema ripristina il **flusso normale del documento**:

- Il body si estende con il contenuto.
- La pagina scorre per intero (non solo il `<main>`).
- Il footer si trova fisicamente in fondo al contenuto HTML.
- La sidebar (se presente) si integra nel flusso verticale.
- L'hamburger sostituisce il menu desktop con un pannello offcanvas.

---

## Come funziona il layout fisso

Il CSS in `_bootstrap-overrides.scss` applica le regole di viewport solo da lg:

```css
/* ≥ 992px */
body { height: 100vh; overflow: hidden; }
.ag-scroll-area { min-height: 0; overflow-y: auto; }
```

Il `body` usa `d-flex flex-column` nel markup HTML. La `<div class="d-flex flex-grow-1">` interna
affianca sidebar e area contenuto; `.ag-scroll-area` usa `flex-grow-1` per occupare tutto lo
spazio disponibile. `<main>` e `<footer>` sono fratelli all'interno di `.ag-scroll-area`: il
footer occupa tutta la larghezza dell'area (viewport − sidebar) indipendentemente dal `max-width`
del `.container` applicato solo a `<main>`.

### Perché `min-height: 0` su `.ag-scroll-area`?

Senza di esso un flex-item non può scendere sotto la sua dimensione naturale:
`.ag-scroll-area` supererebbe il viewport e `overflow-y: auto` non
partirebbe mai. `min-height: 0` rimuove questo vincolo.

### Non usare `min-vh-100` sul body

Applicare `min-vh-100` al body farebbe crescere il body oltre 100vh: il footer
non sarebbe più fisso al fondo del viewport. Usa sempre `height: 100vh`.

---

## Personalizzare le classi di `<main>`

Il tag `<main>` ha per default le classi `container py-4`. Per cambiarlo usa
il blocco `main_class`:

```django
{# Tutta larghezza, nessun padding (es. mappa, canvas) #}
{% block main_class %}container-fluid p-0{% endblock %}

{# Container normale con classe extra #}
{% block main_class %}container py-4 bg-light rounded{% endblock %}
```

---

## Breakpoint utilizzati

| Larghezza | Comportamento |
|---|---|
| `< 992px` | Flusso normale; pagina scorre per intero; footer in fondo al contenuto; hamburger → offcanvas |
| `≥ 992px` | Viewport fisso; solo `<main>` scorre; header e footer fissi; sidebar affiancata al main |
