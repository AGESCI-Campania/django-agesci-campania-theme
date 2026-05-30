# Pubblicare su PyPI

Questa guida spiega come rilasciare `django-agesci-campania-theme` su
[PyPI](https://pypi.org) in modo che chiunque possa installarlo con
`pip install django-agesci-campania-theme` senza dipendere da GitHub.

Il workflow `.github/workflows/publish.yml` **pubblica automaticamente su PyPI**
ogni volta che viene creata una release GitHub. La sezione 1 descrive la
configurazione iniziale necessaria (da fare una sola volta); le sezioni
successive coprono il rilascio manuale.

---

## 1. Configurazione iniziale — Trusted Publishing (da fare una volta sola)

Il workflow usa il **Trusted Publishing** di PyPI tramite OIDC: non servono
token nei secret di GitHub. PyPI verifica direttamente l'identità del workflow.

### 1a. Crea l'ambiente `pypi` su GitHub

1. Vai su **Settings → Environments → New environment** nel repository.
2. Chiamalo `pypi`.
3. (Facoltativo) Aggiungi *Required reviewers* per richiedere approvazione
   manuale prima di ogni pubblicazione.

### 1b. Configura il Trusted Publisher su PyPI

1. Accedi su <https://pypi.org> con l'account del progetto.
2. Vai su **Your projects → django-agesci-campania-theme → Settings →
   Publishing → Add a new publisher**.
3. Scegli **GitHub Actions** e compila:

   | Campo | Valore |
   |---|---|
   | Owner | `AGESCI-Campania` |
   | Repository | `django-agesci-campania-theme` |
   | Workflow filename | `publish.yml` |
   | Environment name | `pypi` |

4. Salva. Da questo momento il workflow è autorizzato a pubblicare senza token.

> Se il pacchetto non è ancora su PyPI, crea prima il Trusted Publisher nella
> sezione **Account Settings → Publishing → Add a pending publisher** (non
> serve un progetto esistente).

---

## 2. Flusso di rilascio automatico

Con il Trusted Publishing configurato, il flusso è:

```bash
# 1. aggiorna la versione
#    - pyproject.toml  →  version = "X.Y.Z"
#    - README.md       →  badge version

# 2. ricompila il CSS se hai modificato lo SCSS
npm run build:css

# 3. committa tutto
git add pyproject.toml README.md agesci_theme/static/agesci_theme/css/
git commit -m "Rilascio vX.Y.Z"
git push origin main

# 4. crea il tag e la release su GitHub
git tag vX.Y.Z
git push origin vX.Y.Z
gh release create vX.Y.Z --title "vX.Y.Z" --generate-notes
```

Alla creazione della release, GitHub Actions eseguirà automaticamente
`publish.yml`: build del pacchetto, check Django, upload su PyPI.

---

## 3. Rilascio manuale (senza GitHub Actions)

### Prerequisiti

- **uv ≥ 0.4** — già usato nel progetto.
- **API token PyPI** — generalo su <https://pypi.org/manage/account/token/>.

### Build

```bash
npm run build:css          # assicurati che il CSS sia aggiornato
rm -rf dist/
uv build                   # genera .whl e .tar.gz in dist/
```

Verifica il contenuto:

```bash
tar tzf dist/django_agesci_campania_theme-*.tar.gz | head -30
```

### Prova su TestPyPI

```bash
uv publish \
  --publish-url https://test.pypi.org/legacy/ \
  --token pypi-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

pip install --index-url https://test.pypi.org/simple/ django-agesci-campania-theme
```

### Pubblica su PyPI

`uv publish` non legge `credentials.toml` automaticamente fuori da CI:
passa il token via flag o variabile d'ambiente.

```bash
# con flag esplicito
uv publish --token pypi-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# oppure con variabile d'ambiente
export UV_PUBLISH_TOKEN=pypi-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
uv publish
```

Con twine:

```bash
# ~/.pypirc deve contenere username = __token__ e password = pypi-XXX
twine upload dist/*
```

---

## Checklist rilascio

- [ ] Versione aggiornata in `pyproject.toml` e nel badge `README.md`
- [ ] CSS rigenerato con `npm run build:css` e committato
- [ ] Commit pushato su `main`
- [ ] Tag `vX.Y.Z` pushato su GitHub
- [ ] Release GitHub creata → il workflow pubblica automaticamente su PyPI
- [ ] Verificare lo stato del workflow in **Actions → publish**
