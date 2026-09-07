# django-agesci-campania-theme


Tema **Bootstrap 5** riusabile per le applicazioni **Django** dell'**AGESCI Campania**.

Fornisce un `base.html` pronto all'uso con **header a due barre**, footer,
sidebar collapsible e una libreria di **componenti opzionali** (`ag_hero`,
`ag_feature_grid`, `ag_jumbotron`, `ag_dropdown`, ecc.) — il tutto brandizzato
con la **palette ufficiale** del *Manuale Immagine Coordinata AGESCI 2011* e
con **personalizzazione per branca** tramite un singolo parametro di configurazione.

---

## In breve

```{list-table}
:header-rows: 1
:widths: 30 30 20

* - Branca / ambito
  - Colore dominante
  - `AGESCI_THEME_BRANCA`
* - Generico (default)
  - Azzurro istituzionale
  - `generico`
* - Capi / Comunità Capi
  - Viola
  - `capi`
* - Lupetti / Coccinelle (L/C)
  - Giallo
  - `lc`
* - Esploratori / Guide (E/G)
  - Verde
  - `eg`
* - Rover / Scolte (R/S)
  - Rosso
  - `rs`
* - Generico 2
  - Viola indaco
  - `generico2`
```

Il colore si applica rimappando le *CSS custom properties* di Bootstrap 5 in
funzione dell'attributo `data-branca` sul tag `<html>`.
**Nessun ricompilo Sass necessario**: basta cambiare una riga in `settings.py`.

---

## Contenuti

```{toctree}
:maxdepth: 2
:caption: Per iniziare

installazione
configurazione
quickstart
```

```{toctree}
:maxdepth: 2
:caption: Manuale d'uso

template
componenti
branche
templatetags
layout
forms
allauth
```

```{toctree}
:maxdepth: 2
:caption: Riferimento

palette
sviluppo
changelog
```
