"""Genera la demo statica del tema per GitHub Pages.

GitHub Pages serve solo file statici: le pagine del progetto demo vengono
renderizzate una volta dal test client di Django e salvate come HTML,
insieme agli asset di ``collectstatic``. Va lanciato una volta per tema,
con le settings corrispondenti (vedi ``.github/workflows/pages.yml``)::

    manage.py demo_statica --output site/bootstrap \\
        --prefix /django-agesci-campania-theme/bootstrap/
    manage.py demo_statica --output site/coreui \\
        --prefix /django-agesci-campania-theme/coreui/ \\
        --settings=config.settings_coreui

``--prefix`` è il percorso in cui il sito sarà pubblicato: diventa
``FORCE_SCRIPT_NAME`` e ``STATIC_URL``, così ``{% url %}``, ``{% static %}``
e ``{% ag_home_url %}`` producono link validi sotto la sottocartella.

Cosa NON funziona nella versione statica: l'invio dei form (non c'è un
server). Nelle pagine generate viene iniettato uno script che blocca il
submit e lo spiega all'utente; lo stato "con errori" del form demo è una
pagina a sé (``/form-demo/errori/``).
"""
import re
import shutil
from pathlib import Path

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.test import Client, override_settings
from django.urls import get_script_prefix, set_script_prefix

# Pagine da generare (URL relativi al prefisso). Le pagine allauth usano il
# layout "base.html" del progetto: sono incluse per mostrarne lo stile.
PAGINE = [
    "/",
    "/components/",
    "/form-demo/",
    "/form-demo/errori/",
    "/accounts/login/",
    "/accounts/signup/",
    "/accounts/password/reset/",
]

# Iniettato prima di </body>: niente server, quindi niente invio dei form.
SCRIPT_DEMO_STATICA = """
<script>
/* Demo statica (GitHub Pages): l'invio dei form è disattivato. */
document.addEventListener('submit', function (e) {
  e.preventDefault();
  var box = document.getElementById('agDemoStatica');
  if (!box) {
    box = document.createElement('div');
    box.id = 'agDemoStatica';
    box.className = 'alert alert-info shadow position-fixed bottom-0 end-0 m-3';
    box.style.zIndex = 2000;
    box.setAttribute('role', 'status');
    box.textContent = "Demo statica su GitHub Pages: l'invio dei form è disattivato. "
      + "Per la validazione lato server avvia il progetto demo in locale.";
    document.body.appendChild(box);
  }
  clearTimeout(box._t);
  box.hidden = false;
  box._t = setTimeout(function () { box.hidden = true; }, 5000);
}, true);
</script>
"""


class Command(BaseCommand):
    help = "Genera la demo statica (HTML + static) per GitHub Pages."

    def add_arguments(self, parser):
        parser.add_argument("--output", required=True, help="Cartella di destinazione (viene svuotata).")
        parser.add_argument(
            "--prefix",
            default="/",
            help="Percorso di pubblicazione, es. /django-agesci-campania-theme/coreui/",
        )

    def handle(self, *args, output, prefix, **options):
        if not (prefix.startswith("/") and prefix.endswith("/")):
            raise CommandError("--prefix deve iniziare e finire con '/'.")
        out = Path(output).resolve()
        if out.exists():
            shutil.rmtree(out)
        out.mkdir(parents=True)

        with override_settings(
            FORCE_SCRIPT_NAME=prefix.rstrip("/") or None,
            STATIC_URL=f"{prefix}static/",
            STATIC_ROOT=out / "static",
            DEBUG=False,
            ALLOWED_HOSTS=["*"],
        ):
            call_command(
                "collectstatic",
                interactive=False,
                verbosity=0,
                ignore_patterns=["admin", "*.scss"],
            )
            # Il test client, a differenza del WSGIHandler, non imposta lo
            # script prefix da FORCE_SCRIPT_NAME: senza, {% url %} e
            # {% ag_home_url %} restituirebbero link senza sottocartella.
            prefisso_originale = get_script_prefix()
            set_script_prefix(prefix)
            client = Client()
            try:
                self._genera_pagine(client, out)
            finally:
                set_script_prefix(prefisso_originale)

        self._controlla_link(out, prefix)
        self.stdout.write(self.style.SUCCESS(f"Demo statica generata in {out}"))

    def _genera_pagine(self, client, out):
        for pagina in PAGINE:
            risposta = client.get(pagina)
            if risposta.status_code != 200:
                raise CommandError(f"{pagina}: HTTP {risposta.status_code}")
            html = risposta.content.decode()
            if "Failed to read icon" in html:
                self.stderr.write(f"ATTENZIONE {pagina}: icone Bootstrap non scaricate.")
            html = html.replace("</body>", SCRIPT_DEMO_STATICA + "</body>", 1)
            destinazione = out / pagina.strip("/") / "index.html"
            destinazione.parent.mkdir(parents=True, exist_ok=True)
            destinazione.write_text(html, encoding="utf-8")
            self.stdout.write(f"  {pagina} -> {destinazione.relative_to(out)}")

    def _controlla_link(self, out, prefix):
        """Fallisce se una pagina generata contiene link interni che su
        GitHub Pages sarebbero 404: fuori dal prefisso (es. "/" fisso nei
        template invece di {% url %}/{% ag_home_url %}) o verso pagine non
        generate."""
        errori = set()
        for file in out.rglob("index.html"):
            for href in re.findall(r'(?:href|src|action)="([^"#?]*)', file.read_text(encoding="utf-8")):
                if not href.startswith("/") or href.startswith("//"):
                    continue
                if not href.startswith(prefix):
                    errori.add(f"fuori dal prefisso: {href}")
                    continue
                relativo = href[len(prefix):]
                bersaglio = out / relativo
                if relativo == "" or relativo.endswith("/"):
                    bersaglio = bersaglio / "index.html"
                if not bersaglio.exists():
                    errori.add(f"pagina non generata: {href}")
        if errori:
            raise CommandError("Link non validi su GitHub Pages:\n  " + "\n  ".join(sorted(errori)))
