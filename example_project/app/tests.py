"""Smoke test del progetto demo: ogni pagina si renderizza, per tutte le branche.

Girano sia col tema Bootstrap 6 sia con CoreUI:
    uv run python example_project/manage.py test app
    uv run python example_project/manage.py test app --settings=config.settings_coreui
"""
from django.test import TestCase, override_settings

from agesci_theme.context_processors import BRANCHE_VALIDE

PAGINE = ["/", "/components/", "/form-demo/", "/form-demo/?invalid=1", "/accounts/login/"]


class PagineDemoTests(TestCase):
    def test_tutte_le_pagine_per_tutte_le_branche(self):
        for branca in sorted(BRANCHE_VALIDE):
            with override_settings(AGESCI_THEME_BRANCA=branca):
                for url in PAGINE:
                    with self.subTest(branca=branca, url=url):
                        r = self.client.get(url)
                        self.assertEqual(r.status_code, 200)
                        self.assertContains(r, f'data-branca="{branca}"')

    def test_form_invalido_mostra_gli_errori(self):
        r = self.client.get("/form-demo/?invalid=1")
        self.assertContains(r, "invalid-feedback")

    def test_login_allauth_invalido_mostra_gli_errori(self):
        r = self.client.post("/accounts/login/", {"login": "x@example.com", "password": "sbagliata"})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "alert")
