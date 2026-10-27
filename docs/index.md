# django-agesci-campania-theme


Tema **Bootstrap 6** riusabile per le applicazioni **Django** dell'**AGESCI Campania**.

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

Il colore si applica rimappando i token *primary* di Bootstrap 6 (`--bs-primary-*`)
in funzione dell'attributo `data-branca` sul tag `<html>`.
**Nessun ricompilo Sass necessario**: basta cambiare una riga in `settings.py`.

```{note}
Esiste anche una variante **CoreUI 5** con layout nativo (sidebar + header),
distribuita come secondo pacchetto PyPI,
[`django-agesci-campania-coreui-theme`](https://pypi.org/project/django-agesci-campania-coreui-theme/),
che usa di questo tema template tag, context processor, immagini e palette, ma ha
il proprio markup (Bootstrap 5/CoreUI 5: dalla 3.0 il tema base è su Bootstrap 6).
Vedi [Tema CoreUI](coreui.md).

```{warning}
**Dalla 3.0 il tema passa a Bootstrap 6** (oggi alpha: 6.0.0-alpha.1) con markup, classi,
JavaScript e browser minimi diversi da Bootstrap 5. Se aggiorni da una 2.x leggi la
[guida alla migrazione](migrazione-bootstrap-6.md).
```
```

---

## Contenuti

```{toctree}
:maxdepth: 2
:caption: Per iniziare

installazione
configurazione
quickstart
migrazione-bootstrap-6
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
coreui
```

```{toctree}
:maxdepth: 2
:caption: Riferimento

palette
sviluppo
changelog
```
