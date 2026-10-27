"""Fallisce se nei template del tema base compaiono pattern Bootstrap 5.

Uso (dalla root del repo): python scripts/check_bs5_residui.py
I template CoreUI (coreui/) restano volutamente su Bootstrap 5 e non vengono controllati.
"""
import pathlib
import re
import sys

RADICE = pathlib.Path(__file__).resolve().parent.parent
CARTELLE = [
    RADICE / "agesci_theme" / "templates",
    RADICE / "example_project" / "app" / "templates",
]

# (descrizione, regex applicata al testo dell'attributo class="...")
CLASSI = [
    ("prefisso responsive v5 (usa lg:d-none)", re.compile(r"(?<![\w:-])(?:d|col|row-cols|g|gx|gy|ms|me|mt|mb|p[xy]?|m[xy]?|order|offset|text|float|flex)-(?:sm|md|lg|xl|xxl)-[\w-]+")),
    ("btn-primary & co. (usa btn-solid theme-*)", re.compile(r"(?<![\w-])btn-(?:primary|secondary|success|danger|warning|info|light|dark)(?![\w-])")),
    ("btn-outline-* (usa btn-outline theme-*)", re.compile(r"(?<![\w-])btn-outline-[\w-]+")),
    ("text-bg-* (usa theme-*)", re.compile(r"(?<![\w-])text-bg-[\w-]+")),
    ("alert-<variante> (usa alert theme-*)", re.compile(r"(?<![\w-])alert-(?:primary|secondary|success|danger|warning|info|light|dark|dismissible)(?![\w-])")),
    ("text-muted / text-body-secondary (usa fg-2)", re.compile(r"(?<![\w-])text-(?:muted|body-secondary)(?![\w-])")),
    ("form-select / form-check (usa form-control, check, radio)", re.compile(r"(?<![\w-])form-(?:select|check[\w-]*)(?![\w-])")),
    ("offcanvas* (usa drawer)", re.compile(r"(?<![\w-])offcanvas[\w-]*")),
    ("modal* (usa dialog)", re.compile(r"(?<![\w-])modal(?:-[\w-]+)?(?![\w-])")),
    ("dropdown* (usa menu)", re.compile(r"(?<![\w-])(?:dropdown[\w-]*|dropup|dropstart|dropend)(?![\w-])")),
    ("navbar-expand-* / navbar-light / navbar-dark", re.compile(r"(?<![\w-])navbar-(?:expand-[\w]+|light|dark)(?![\w-])")),
    ("lead / display-N (usa fs-*)", re.compile(r"(?<![\w-])(?:lead|display-\d)(?![\w-])")),
]

ATTRIBUTI = [
    ("data-bs-toggle v5", re.compile(r'data-bs-toggle="(?:modal|offcanvas|dropdown|collapse)"')),
    ("data-bs-dismiss v5", re.compile(r'data-bs-dismiss="(?:modal|offcanvas)"')),
    ("tag {% ag_js %} (rimosso nella 3.0)", re.compile(r"\{%\s*ag_js\s*%\}")),
    ("popperConfig / window.bootstrap", re.compile(r"popperConfig|window\.bootstrap")),
]


def senza_commenti(testo):
    testo = re.sub(r"\{#.*?#\}", lambda m: re.sub(r"[^\n]", " ", m.group(0)), testo)
    return re.sub(
        r"\{% comment %\}.*?\{% endcomment %\}",
        lambda m: re.sub(r"[^\n]", " ", m.group(0)),
        testo,
        flags=re.S,
    )


def main():
    errori = []
    for cartella in CARTELLE:
        for file in sorted(cartella.rglob("*.html")):
            testo = senza_commenti(file.read_text())
            for m in re.finditer(r'class="([^"]*)"', testo):
                valore = re.sub(r"\{%.*?%\}|\{\{.*?\}\}", " ", m.group(1))
                riga = testo.count("\n", 0, m.start()) + 1
                for descr, rx in CLASSI:
                    trovato = rx.search(valore)
                    if trovato:
                        errori.append(f"{file.relative_to(RADICE)}:{riga}: {descr}: {trovato.group(0)!r}")
            for descr, rx in ATTRIBUTI:
                for m in rx.finditer(testo):
                    riga = testo.count("\n", 0, m.start()) + 1
                    errori.append(f"{file.relative_to(RADICE)}:{riga}: {descr}: {m.group(0)!r}")
    for sorgente in (RADICE / "agesci_theme" / "static" / "agesci_theme" / "js").glob("*.js"):
        testo = sorgente.read_text()
        for descr, rx in ATTRIBUTI[2:]:
            for m in rx.finditer(testo):
                riga = testo.count("\n", 0, m.start()) + 1
                errori.append(f"{sorgente.relative_to(RADICE)}:{riga}: {descr}: {m.group(0)!r}")
    for e in errori:
        print(e)
    print(f"-- {len(errori)} residui Bootstrap 5")
    return 1 if errori else 0


if __name__ == "__main__":
    sys.exit(main())
