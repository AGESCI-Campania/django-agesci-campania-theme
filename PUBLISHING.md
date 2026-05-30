# Pubblicare su PyPI

Questa guida spiega come rilasciare `django-agesci-campania-theme` su
[PyPI](https://pypi.org) in modo che chiunque possa installarlo con
`pip install django-agesci-campania-theme` senza dipendere da GitHub.

---

## Prerequisiti

1. **Account PyPI** — registrati su <https://pypi.org/account/register/>.
2. **Account TestPyPI** (consigliato per prove) — registrati su
   <https://test.pypi.org/account/register/>.
3. **uv ≥ 0.4** — già usato nel progetto; gestisce build e upload.
   In alternativa puoi usare `twine` (vedi sotto).

---

## 1. Configura le credenziali

Il modo più sicuro è usare un **API token** per ciascun repository.

### Con uv

Il modo più diretto è passare il token esplicitamente al comando (uv non legge
il `credentials.toml` automaticamente fuori da ambienti CI):

```bash
uv publish --token pypi-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

In alternativa, esporta la variabile d'ambiente prima di lanciare `uv publish`:

```bash
export UV_PUBLISH_TOKEN=pypi-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
uv publish
```

Puoi conservare i token in `~/.config/uv/credentials.toml` come riferimento,
ma dovrai comunque passarli via `--token` o variabile d'ambiente:

```toml
[pypi]
token = "pypi-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

[testpypi]
token = "pypi-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

### Con twine (file `~/.pypirc`)

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username   = __token__
password   = pypi-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

[testpypi]
repository = https://test.pypi.org/legacy/
username   = __token__
password   = pypi-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

---

## 2. Aggiorna la versione

Prima di ogni rilascio modifica `version` in `pyproject.toml`:

```toml
[project]
version = "1.1.0"   # segue Semantic Versioning: MAJOR.MINOR.PATCH
```

Poi aggiorna il badge nel `README.md`:

```markdown
[![Version](https://img.shields.io/badge/version-1.1.0-informational.svg)](pyproject.toml)
```

---

## 3. Costruisci il pacchetto

```bash
# assicurati che il CSS compilato sia aggiornato
npm run build:css

# pulisci eventuali build precedenti
rm -rf dist/

# genera .whl e .tar.gz nella cartella dist/
uv build
```

Verifica il contenuto dell'archivio prima di pubblicare:

```bash
tar tzf dist/django_agesci_campania_theme-*.tar.gz | head -30
```

---

## 4. Prova su TestPyPI

```bash
# con uv
uv publish --publish-url https://test.pypi.org/legacy/ --token $UV_PUBLISH_TOKEN_TEST

# con twine
twine upload --repository testpypi dist/*
```

Installa dal TestPyPI per verificare:

```bash
pip install --index-url https://test.pypi.org/simple/ django-agesci-campania-theme
```

---

## 5. Pubblica su PyPI

```bash
# con uv
uv publish --token $UV_PUBLISH_TOKEN

# con twine
twine upload dist/*
```

Da quel momento chiunque può installarlo con:

```bash
pip install django-agesci-campania-theme
uv add django-agesci-campania-theme
```

---

## 6. Crea il tag e la release su GitHub

Dopo aver pubblicato su PyPI, tagga il commit e crea la release:

```bash
git tag v1.1.0
git push origin v1.1.0
gh release create v1.1.0 dist/* \
  --title "v1.1.0" \
  --notes "Vedere CHANGELOG per i dettagli."
```

Allegare i file `dist/*` alla release permette il download diretto degli
artefatti anche senza PyPI.

---

## Checklist rilascio

- [ ] Versione aggiornata in `pyproject.toml` e nel badge `README.md`
- [ ] CSS rigenerato con `npm run build:css` e committato
- [ ] `uv build` eseguito senza errori
- [ ] Testato su TestPyPI
- [ ] `uv publish` / `twine upload` su PyPI
- [ ] Tag git creato e pushato
- [ ] Release GitHub creata con gli artefatti `dist/*`
