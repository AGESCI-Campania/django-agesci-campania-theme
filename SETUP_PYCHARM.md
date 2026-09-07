# Setup sviluppo — PyCharm + uv

Guida rapida per iniziare a sviluppare `django-agesci-theme` su PyCharm
usando **uv** come package manager e Claude Code.

## 1. Prerequisiti

- **Python 3.12** (il progetto fissa la versione in `.python-version`)
- **uv** — installalo se non presente:
  - macOS / Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
  - Windows (PowerShell): `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`
- **Node.js** (solo se modifichi lo SCSS) per `sass`
- **Git**

## 2. Primo avvio

Dalla cartella del progetto:

```bash
uv sync                 # crea .venv e installa il tema (editable) + Django
```

Avvia il progetto demo:

```bash
uv run python example_project/manage.py migrate
uv run python example_project/manage.py runserver
```

Apri http://127.0.0.1:8000 — vedrai la demo colorata secondo la branca
impostata in `example_project/config/settings.py` (`AGESCI_THEME_BRANCA`).
Cambia quel valore (`capi`, `lc`, `eg`, `rs`, `viola`, `generico`, `generico2`) e ricarica.

## 3. Configurare PyCharm

1. **Apri la cartella** del progetto come progetto PyCharm.
2. **Interprete**: Settings → Project → Python Interpreter → Add Interpreter →
   *Existing* → seleziona `.venv/bin/python` (creato da `uv sync`).
   PyCharm Professional 2024.1+ riconosce uv nativamente.
3. **Run configuration Django** (PyCharm Professional):
   - Settings → Languages & Frameworks → Django → Enable.
   - Django project root: `example_project`
   - Settings: `config/settings.py`
   - Manage script: `example_project/manage.py`
   - Crea una *Run config* "Django Server".
   In Community Edition: usa una config Python che lancia
   `example_project/manage.py runserver`.
4. **Marca** `example_project` come *Sources Root* (tasto destro → Mark Directory as).

## 4. Modificare i colori / SCSS

```bash
npm install
npm run watch:css       # ricompila agesci.css/agesci.min.css ad ogni salvataggio
```

## 5. Usare Claude Code

Il file `CLAUDE.md` nella root dà a Claude Code il contesto del progetto
(struttura, regole sulla palette, comandi). Lancia `claude` dalla root del repo.

## 6. Pubblicare su GitHub

```bash
git init
git add .
git commit -m "Initial commit: tema AGESCI Campania"
git branch -M main
git remote add origin https://github.com/AGESCI-Campania/django-agesci-campania-theme.git
git push -u origin main
```

Da quel momento, qualsiasi app potrà installarlo con:

```bash
# da PyPI (consigliato)
uv add django-agesci-campania-theme
pip install django-agesci-campania-theme
# da GitHub (ultima versione non rilasciata)
uv add "git+https://github.com/AGESCI-Campania/django-agesci-campania-theme.git"
pip install "git+https://github.com/AGESCI-Campania/django-agesci-campania-theme.git"
```
