# Sistema delle branche

## Come funziona

Il tema supporta cinque branche/ambiti, ciascuno con il proprio colore primario
tratto dal *Manuale Immagine Coordinata AGESCI 2011*. Il meccanismo funziona
interamente via **CSS custom properties**: nessun file Sass va ricompilato per
cambiare branca.

Il flusso è:

1. `settings.py` definisce `AGESCI_THEME_BRANCA = "eg"`.
2. Il context processor lo espone come variabile `agesci_theme_branca`.
3. `base.html` scrive `<html data-branca="eg">`.
4. `_branche.scss` ha generato (a build time) un blocco CSS per ogni valore:
   ```css
   [data-branca="eg"] {
     --ag-primary: #3D8E33;
     --ag-primary-hover: #2e6c26;
     /* ... */
   }
   ```
5. Tutti i componenti Bootstrap (pulsanti, link, badge…) usano `--bs-primary`
   che è rimappato su `--ag-primary` da `_bootstrap-overrides.scss`.

---

## Tabella branche

| `data-branca` | Colore | Pantone | HEX | Uso |
|---|---|---|---|---|
| `generico` | Azzurro | 279C | `#6689CC` | Default, uffici, zone |
| `capi` | Viola | 527C | `#7A1E99` | Capi / Comunità Capi |
| `lc` | Giallo | 109C | `#F9D616` | Lupetti / Coccinelle |
| `eg` | Verde | 363C | `#3D8E33` | Esploratori / Guide |
| `rs` | Rosso | 032C | `#EF3340` | Rover / Scolte |
| `viola` | Viola | 527C | `#7A1E99` | Alias di `capi` |

---

## Variabili CSS generate

Per ogni branca `_branche.scss` genera queste custom properties:

| Variabile | Descrizione |
|---|---|
| `--ag-primary` | Colore primario della branca |
| `--ag-primary-hover` | Versione più scura per hover (`-8% lightness`) |
| `--ag-primary-active` | Versione ancora più scura per stato active (`-14%`) |
| `--ag-primary-subtle` | Versione molto chiara per sfondi (`+42%`) |
| `--ag-on-primary` | Colore del testo sul primario (nero o bianco, calcolato automaticamente) |
| `--bs-primary` | Ridirezione Bootstrap verso `--ag-primary` |
| `--bs-link-color` | Colore dei link Bootstrap |
| `--bs-link-hover-color` | Hover dei link Bootstrap |

---

## Usare `--ag-primary` nei componenti custom

Nei tuoi SCSS o CSS inline usa sempre le variabili del tema invece di colori
hardcoded: in questo modo il componente risponde automaticamente alla branca.

```css
/* Nel tuo CSS custom */
.mio-componente {
  background-color: var(--ag-primary);
  color: var(--ag-on-primary);
  border: 2px solid var(--ag-primary-hover);
}

.mio-componente:hover {
  background-color: var(--ag-primary-hover);
}

.mio-pannello {
  background-color: var(--ag-primary-subtle);
  border-left: 4px solid var(--ag-primary);
}
```

---

## Navbar con branca a colore chiaro

Per la branca `lc` (giallo), il testo bianco della navbar è illeggibile.
Imposta:

```python
AGESCI_THEME_NAVBAR_TESTO_SCURO = True
```

Questo aggiunge la classe `.text-dark` alla navbar, che sovrascrive le
variabili `--bs-navbar-*` con toni scuri.

---

## Aggiungere una nuova branca

Se in futuro servisse una nuova branca, occorre intervenire in **tre punti**:

1. **`_branche.scss`** — aggiungi una voce alla mappa `$branche`:
   ```scss
   $branche: (
     // ... branche esistenti ...
     "nuova": p.$agesci-nuovo-colore,
   );
   ```

2. **`context_processors.py`** — aggiungi alla costante `BRANCHE_VALIDE`:
   ```python
   BRANCHE_VALIDE = {"generico", "capi", "lc", "eg", "rs", "viola", "nuova"}
   ```

3. **`templatetags/agesci_tags.py`** — aggiungi alla mappa `_BRANCA_BG`:
   ```python
   _BRANCA_BG = {
       # ... voci esistenti ...
       "nuova": "bg-ag-nuovo-colore",
   }
   ```

4. Aggiungi la classe utility in `_bootstrap-overrides.scss`:
   ```text
   .bg-ag-nuovo-colore { background-color: p.$agesci-nuovo-colore !important; color: ...; }
   ```

5. Esegui `npm run build:css` e committa i CSS compilati.
