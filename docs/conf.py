project = "django-agesci-campania-theme"
copyright = "AGESCI Campania"
author = "AGESCI Campania"
release = "1.2.0"

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
