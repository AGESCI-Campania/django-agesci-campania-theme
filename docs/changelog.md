# Changelog

Tutte le modifiche rilevanti al progetto sono documentate in questa pagina.
Il formato segue [Keep a Changelog](https://keepachangelog.com/it/1.0.0/).

---

## [1.2.3] — 2026-06-08

### Modificato
- Layout mobile/tablet: breakpoint `body { height: 100vh }` e `main { overflow-y: auto }` alzato da md (768px) a lg (992px). Il footer ora scorre naturalmente con il contenuto su smartphone e tablet.
- `.footer-agesci`: padding ridotto da `2rem 0` a `0.5rem 0`.

---

## [1.2.2] — 2026-06-08

### Corretto
- Fix build PDF GitHub Actions: rimossi badge SVG da `index.md` (non supportati da rinohtype),
  aggiunto `rinoh_documents` in `conf.py`, rimosso `-W` dal comando sphinx-build.

---

## [1.2.1] — 2026-06-08

### Corretto
- Aggiunta dipendenza `Pillow>=10.0` in `docs/requirements.txt` (richiesta da rinohtype per la generazione PDF).

---

## [1.2.0] — 2026-06-08

### Aggiunto
- Suite di documentazione completa con Sphinx + MyST-Parser, pronta per ReadTheDocs.
- Generazione PDF automatica allegata a ogni release GitHub tramite GitHub Actions (`rinohtype`).
- `.readthedocs.yaml` con output PDF e HTMLzip abilitati.

### Corretto
- Layout mobile (< 768px): il footer ora segue il flusso normale del documento
  invece di rimanere incollato al bordo inferiore del viewport.

---

## [1.1.0] — 2025

### Aggiunto
- Layout a viewport fisso: `body { height: 100vh }` + `main { overflow-y: auto }`.
- Breadcrumb brandizzata (`breadcrumb-agesci`) attivabile via `breadcrumb_items`.
- Sub-navbar secondaria (`subnav-agesci`) attivabile via `subnav_items`.
- Integrazione icone Bootstrap Icons tramite `django-bootstrap-icons` (extra `[icons]`).
- Workflow GitHub Actions per pubblicazione automatica su PyPI via Trusted Publisher.
- Layout mobile responsive: sotto 768px il footer torna al flusso normale del documento.

### Modificato
- `base.html` espone tutti i blocchi di composizione (navbar, footer, breadcrumb, subnav).
- Context processor esteso con tutte le variabili `AGESCI_THEME_*`.

---

## [1.0.0] — 2024

### Aggiunto
- Prima versione pubblica del tema.
- Palette ufficiale AGESCI dal *Manuale Immagine Coordinata 2011*.
- Sistema branche via `[data-branca]` e CSS custom properties.
- Template `base.html`, partial navbar e footer.
- Template tag `emblema_zona`, `zone_disponibili`, `branca_bg`.
- Classi utility `bg-ag-*` e `text-ag-*`.
- Progetto Django di esempio (`example_project/`).
- Pacchetto pubblicato su PyPI come `django-agesci-campania-theme`.
