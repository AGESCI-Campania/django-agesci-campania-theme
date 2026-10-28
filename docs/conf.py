import tomllib
from pathlib import Path

_pyproject = tomllib.loads((Path(__file__).parent.parent / "pyproject.toml").read_text())
release = _pyproject["project"]["version"]
version = ".".join(release.split(".")[:2])

project = "django-agesci-campania-theme"
copyright = "AGESCI Campania"
author = "AGESCI Campania"

extensions = [
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_design",
    "rinoh.frontend.sphinx",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "furo"
html_title = "django-agesci-campania-theme"

html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#7a1e99",
        "color-brand-content": "#7a1e99",
    },
    "dark_css_variables": {
        "color-brand-primary": "#b06dd0",
        "color-brand-content": "#b06dd0",
    },
}

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "tasklist",
]

myst_heading_anchors = 3

rinoh_documents = [
    {
        "doc": "index",
        "target": "django-agesci-campania-theme",
        "title": project,
        "author": author,
    }
]

# llms.txt e llms-full.txt, generati dai sorgenti e pubblicati alla radice del sito.
# Generati subito (non in builder-inited): Sphinx controlla html_extra_path prima.
def _genera_llms():
    import importlib.util

    percorso = Path(__file__).parent.parent / "scripts" / "build_llms_txt.py"
    spec = importlib.util.spec_from_file_location("build_llms_txt", percorso)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    modulo.genera(Path(__file__).parent / "_llms")


_genera_llms()
html_extra_path = ["_llms"]
