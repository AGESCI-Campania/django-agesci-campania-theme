# Palette colori

## Fonte ufficiale

La palette è estratta dalla **sezione 7 "Colori"** del *Manuale Immagine
Coordinata AGESCI 2011*. I valori HEX usati nel tema corrispondono ai codici
Pantone riportati nel manuale, con un'eccezione documentata per il rosso R/S.

---

## Colori istituzionali

| Colore | Pantone | HEX | Variabile Sass | Uso |
|---|---|---|---|---|
| Viola | 527C | `#7A1E99` | `$agesci-viola` | Branca Capi, colore istituzionale |
| Viola scuro | 072C | `#622599` | `$agesci-viola-scuro` | Variante scura del viola |
| Giallo oro | 123C | `#FFCC1E` | `$agesci-giallo-oro` | Accenti, dettagli dorati |
| Azzurro | 279C | `#6689CC` | `$agesci-azzurro` | Colore generico/zona |

---

## Colori di branca

| Colore | Pantone | HEX | Variabile Sass | Branca |
|---|---|---|---|---|
| Giallo L/C | 109C | `#F9D616` | `$agesci-giallo-lc` | Lupetti / Coccinelle |
| Verde E/G | 363C | `#3D8E33` | `$agesci-verde-eg` | Esploratori / Guide |
| Rosso R/S | 032C | `#EF3340` | `$agesci-rosso-rs` | Rover / Scolte |

:::{note}
Il *Manuale 2011* riporta per il rosso R/S (Pantone 032C) un valore RGB
`80/15/17` che corrisponde a un marrone scuro: si tratta di un **refuso di
stampa** del PDF (confermato). Il tema usa il valore standard Pantone 032C
(`#EF3340`), coerente con l'uso associativo.
:::

---

## Neutri di supporto

| Colore | HEX | Variabile Sass | Uso |
|---|---|---|---|
| Nero | `#1A1A1A` | `$agesci-nero` | Testo su sfondi chiari |
| Grigio scuro | `#343A40` | `$agesci-grigio-scuro` | Sfondo footer, testo secondario |
| Grigio | `#6C757D` | `$agesci-grigio` | Testo placeholder, elementi disabilitati |
| Grigio chiaro | `#F4F4F6` | `$agesci-grigio-chiaro` | Sfondi sezioni, card alt |
| Bianco | `#FFFFFF` | `$agesci-bianco` | Testo su sfondi scuri |

---

(classi-utility)=
## Classi utility

Le classi utility permettono di applicare direttamente i colori della palette
a qualsiasi elemento HTML senza scrivere CSS custom.

### Classi di sfondo

| Classe | Colore di sfondo | Testo automatico |
|---|---|---|
| `bg-ag-viola` | `#7A1E99` (viola) | bianco |
| `bg-ag-azzurro` | `#6689CC` (azzurro) | bianco |
| `bg-ag-giallo-lc` | `#F9D616` (giallo L/C) | nero |
| `bg-ag-verde-eg` | `#3D8E33` (verde E/G) | bianco |
| `bg-ag-rosso-rs` | `#EF3340` (rosso R/S) | bianco |
| `bg-ag-giallo-oro` | `#FFCC1E` (giallo oro) | nero |

### Classi di testo

| Classe | Colore del testo |
|---|---|
| `text-ag-viola` | `#7A1E99` |
| `text-ag-azzurro` | `#6689CC` |
| `text-ag-verde-eg` | `#3D8E33` |
| `text-ag-rosso-rs` | `#EF3340` |

### Esempi d'uso

```django
{# Banner di branca #}
<div class="bg-ag-verde-eg p-3 rounded">
  <h3 class="mb-0">Esploratori e Guide</h3>
</div>

{# Badge colorato #}
<span class="badge bg-ag-rosso-rs">Rover/Scolte</span>

{# Testo colorato #}
<p class="text-ag-viola fw-bold">Nota importante</p>

{# Card con intestazione di branca #}
<div class="card">
  <div class="card-header bg-ag-giallo-lc">
    <strong>Attività L/C</strong>
  </div>
  <div class="card-body">
    Contenuto della card
  </div>
</div>
```

---

## Uso nelle view e nei template dinamici

Il template tag [`branca_bg`](templatetags.md#branca_bg) restituisce la classe
di sfondo corrispondente alla branca attiva, senza hardcodare il valore:

```django
{% load agesci_tags %}
<span class="badge {% branca_bg %}">Etichetta branca</span>
```

Per applicare colori fissi (non dipendenti dalla branca) usa le classi `bg-ag-*`
direttamente.
