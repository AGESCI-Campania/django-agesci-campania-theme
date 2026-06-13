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
│  <main> — scorre                     │  flex-grow-1, overflow-y: auto
│                                      │
├──────────────────────────────────────┤
│ Footer                               │  fisso
└──────────────────────────────────────┘
```

### Con sidebar attivata

```
┌──────────────────────────────────────┐  ← 100vh
│ Header                               │  fisso
├──────────┬───────────────────────────┤
│          │                           │
│ Sidebar  │  <main> — scorre          │
│ (240px)  │                           │
│          │                           │
├──────────┴───────────────────────────┤
│ Footer                               │  fisso
└──────────────────────────────────────┘
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
main { min-height: 0; overflow-y: auto; }
```

Il `body` usa `d-flex flex-column` nel markup HTML; `main` ha `flex-grow-1`
per occupare tutto lo spazio disponibile nella zona centrale.

### Perché `min-height: 0` su `<main>`?

Senza di esso un flex-item non può scendere sotto la sua dimensione naturale:
il contenuto spingerebbe `<main>` oltre il viewport e `overflow-y: auto` non
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
