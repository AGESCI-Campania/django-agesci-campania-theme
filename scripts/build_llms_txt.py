#!/usr/bin/env python3
"""Genera `llms.txt` e `llms-full.txt` dai sorgenti Markdown di docs/.

- `llms.txt`: indice breve (formato llmstxt.org) con link ai sorgenti .md su GitHub.
- `llms-full.txt`: le pagine del manuale concatenate, in ordine di toctree.

Usato da docs/conf.py (pubblicati alla radice della documentazione su
ReadTheDocs) e da build.yml (verifica). L'ordine e l'elenco delle pagine
vengono dal toctree di docs/index.md: una pagina nuova va solo aggiunta là.

    python3 scripts/build_llms_txt.py [cartella_output]   # default: docs/_llms
"""

import re
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
DOCS = RADICE / "docs"

DOCS_URL = "https://django-agesci-campania-theme.readthedocs.io/it/latest"
RAW_URL = "https://raw.githubusercontent.com/AGESCI-Campania/django-agesci-campania-theme/main/docs"

# Pagine per chi sviluppa il tema o storiche: fuori da llms-full.txt (restano nell'indice).
ESCLUSE_DAL_FULL = {"changelog", "sviluppo"}

DESCRIZIONI = {
    "assistenti-ai": "regole da conoscere prima di scrivere codice con il tema (Bootstrap 6, non 5)",
    "installazione": "installazione da PyPI, pre-release, extra",
    "configurazione": "impostazioni AGESCI_THEME_* e INSTALLED_APPS",
    "quickstart": "primo progetto in pochi minuti",
    "migrazione-bootstrap-6": "tabelle di conversione Bootstrap 5 → 6 e rotture dell'API del tema",
    "template": "base.html, blocchi e come estenderlo",
    "componenti": "componenti opzionali (hero, badge, bottoni, modal, dropdown…)",
    "branche": "colore per branca e token --bs-primary-*",
    "templatetags": "riferimento dei template tag ag_*",
    "layout": "layout viewport fisso, sidebar, header e breadcrumb",
    "forms": "AgesciFormRenderer e validazione dei form",
    "allauth": "override dei template django-allauth",
    "coreui": "tema CoreUI 5 (secondo pacchetto, markup separato)",
    "palette": "palette ufficiale AGESCI",
    "sviluppo": "per chi modifica il tema (SCSS, layer, build, rilascio)",
    "changelog": "storico delle versioni",
}


def pagine():
    """Nomi delle pagine nell'ordine dei toctree di index.md."""
    testo = (DOCS / "index.md").read_text(encoding="utf-8")
    nomi = []
    for blocco in re.findall(r"```\{toctree\}\n(.*?)```", testo, flags=re.S):
        for riga in blocco.splitlines():
            riga = riga.strip()
            if riga and not riga.startswith(":"):
                nomi.append(riga)
    return nomi


def titolo(nome):
    m = re.search(r"^# (.+)$", (DOCS / f"{nome}.md").read_text(encoding="utf-8"), flags=re.M)
    return m.group(1).strip() if m else nome


def genera(uscita):
    uscita.mkdir(parents=True, exist_ok=True)
    nomi = pagine()

    righe = [
        "# django-agesci-campania-theme",
        "",
        "> Tema Bootstrap 6 (alpha) per le app Django dell'AGESCI Campania: base.html con header, sidebar e footer,",
        "> componenti `ag_*`, colore per branca (`AGESCI_THEME_BRANCA`), renderer dei form e override di django-allauth.",
        "> Non è Bootstrap 5: classi, JavaScript e browser minimi sono diversi. Leggi per prima la pagina sugli assistenti AI.",
        "",
        "Il testo completo del manuale in un solo file è in "
        f"[llms-full.txt]({DOCS_URL}/llms-full.txt).",
        "",
        "## Documentazione",
        "",
    ]
    for nome in nomi:
        desc = DESCRIZIONI.get(nome)
        voce = f"- [{titolo(nome)}]({RAW_URL}/{nome}.md)"
        righe.append(f"{voce}: {desc}" if desc else voce)
    righe += [
        "",
        "## Risorse correlate",
        "",
        "- [Skill per assistenti AI](https://github.com/AGESCI-Campania/django-agesci-campania-theme/tree/main/skills/django-agesci-theme): "
        "`npx skills add AGESCI-Campania/django-agesci-campania-theme`",
        "- [Indice LLM di Bootstrap 6](https://getbootstrap.com/llms.txt): classi e componenti di Bootstrap 6",
        "",
    ]
    (uscita / "llms.txt").write_text("\n".join(righe), encoding="utf-8")

    parti = [
        "# django-agesci-campania-theme — documentazione completa\n\n"
        f"Generato dai sorgenti in docs/ ({DOCS_URL}/). Esclusi changelog e guida allo sviluppo.\n"
    ]
    for nome in nomi:
        if nome in ESCLUSE_DAL_FULL:
            continue
        corpo = (DOCS / f"{nome}.md").read_text(encoding="utf-8").strip()
        parti.append(f"\n\n---\n\n<!-- docs/{nome}.md -->\n\n{corpo}\n")
    (uscita / "llms-full.txt").write_text("".join(parti), encoding="utf-8")
    return nomi


if __name__ == "__main__":
    destinazione = Path(sys.argv[1]) if len(sys.argv) > 1 else DOCS / "_llms"
    nomi = genera(destinazione)
    print(f"{len(nomi)} pagine -> {destinazione}")
