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


class WidgetBootstrap6Tests(TestCase):
    """Logica lato server dei widget dei componenti form di Bootstrap 6
    (agesci_theme.forms); il comportamento nel browser è del JS di Bootstrap."""

    def _form(self, **campi):
        from django import forms

        return type("F", (forms.Form,), campi)

    def test_selettore_data_accetta_il_formato_italiano(self):
        from django import forms

        from agesci_theme.forms import SelettoreData

        F = self._form(data=forms.DateField(widget=SelettoreData()))
        for valore in ("26/10/2026", "2026-10-26", "5/1/2026"):
            with self.subTest(valore=valore):
                form = F({"data": valore})
                self.assertTrue(form.is_valid(), form.errors)
        # Ridisegnato in ISO e con data-bs-selected-dates, così il datepicker lo mostra subito.
        html = str(F({"data": "26/10/2026"})["data"])
        self.assertIn('value="2026-10-26"', html)
        self.assertIn("data-bs-selected-dates", html)

    def test_combobox_multiplo_divide_i_valori(self):
        from django import forms

        from agesci_theme.forms import ComboboxMultiplo

        F = self._form(b=forms.MultipleChoiceField(choices=[("lc", "L/C"), ("eg", "E/G")], widget=ComboboxMultiplo()))
        form = F({"b": "lc,eg"})
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["b"], ["lc", "eg"])

    def test_campo_chip(self):
        from agesci_theme.forms import CampoChip

        F = self._form(tag=CampoChip(max_chip=2))
        self.assertEqual(F({"tag": " a, b ,"}).is_valid(), True)
        self.assertFalse(F({"tag": "a,b,c"}).is_valid())
        self.assertIn('data-bs-max-chips="2"', str(F()["tag"]))

    def test_errori_su_contenitore(self):
        from django import forms

        from agesci_theme.forms import CodiceOTP, InputConAdorno

        F = self._form(codice=forms.CharField(widget=CodiceOTP()), quota=forms.CharField(widget=InputConAdorno(prefisso="€")))
        form = F({})
        form.is_valid()
        self.assertIn('class="otp otp-connected is-invalid"', str(form["codice"]))
        self.assertIn("form-adorn is-invalid", str(form["quota"]))
