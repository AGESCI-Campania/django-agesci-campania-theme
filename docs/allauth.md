# Integrazione con django-allauth

Il tema include override Bootstrap 5 opzionali per le pagine generate da
[django-allauth](https://docs.allauth.org/) (login, logout, registrazione,
reset password, MFA...), che di default ignorano completamente lo styling
Bootstrap.

Questi override condividono il meccanismo `FORM_RENDERER` descritto in
[Form e validazione](forms.md): se non l'hai ancora letto, parti da lì per
capire cosa cambia nei form Django in generale (incluso il perché
`.invalid-feedback { display: block; }` è deliberato).

---

## Cosa viene sovrascritto e come si attiva

Il tema fornisce due template, sotto `agesci_theme/templates/allauth/`:

- `allauth/layouts/base.html` — il layout base di allauth.
- `allauth/elements/button.html` — mappa i `tags` che allauth passa ai
  bottoni (`prominent`, `outline`, `secondary`, `danger`, `link`) sulle
  classi Bootstrap `btn btn-*`.

Questi due file **non richiedono alcuna configurazione**: `agesci_theme` è
già un'app installata (requisito documentato per usare il tema), quindi
Django li trova automaticamente via `APP_DIRS`, allo stesso modo in cui
allauth trova i propri template di default — non c'entra il motore isolato
di `AgesciFormRenderer`.

:::{important}
`agesci_theme` deve comparire in `INSTALLED_APPS` **prima** di `allauth`,
`allauth.account`, `allauth.mfa` (o qualunque altra app allauth). Il loader
`APP_DIRS` di Django scorre i template dir delle app nell'ordine di
`INSTALLED_APPS`: se le app allauth vengono prima, i loro template bundled
vengono trovati per primi e gli override del tema restano silenziosamente
inapplicati — nessun errore, le pagine appaiono semplicemente senza stile.
:::

Per applicare anche lo styling `is-invalid`/`invalid-feedback` ai form di
allauth (login, registrazione, reset password), attiva `FORM_RENDERER`
come per qualsiasi altro form Django del progetto — vedi
[Form e validazione](forms.md#attivazione):

```python
FORM_RENDERER = "agesci_theme.forms.AgesciFormRenderer"
```

---

## Requisito: un `templates/base.html` nel progetto consumer

`allauth/layouts/base.html` estende letteralmente `"base.html"`:

```django
{% extends "base.html" %}
```

**Non** `"agesci_theme/base.html"` — di proposito. Se estendesse
direttamente il `base.html` del tema, le pagine allauth perderebbero le
personalizzazioni del progetto consumer (nav, breadcrumb, sidebar, ecc.).
`{% extends "base.html" %}` invece risolve, tramite la risoluzione standard
dei template dir di Django, al `base.html` del progetto consumer — che è
già la convenzione richiesta dal tema ("template base da estendere", vedi
[Template](template.md)):

```django
{# templates/base.html del progetto consumer #}
{% extends "agesci_theme/base.html" %}
```

Se il progetto consumer non ha un proprio `templates/base.html`, le pagine
allauth non troveranno alcun template da estendere.

---

## Versione testata

Il tema è stato verificato con **django-allauth 65.19.1** (extra `[mfa]`).
Il sistema `{% element %}` / `allauth/layouts/*` di allauth è interno e può
cambiare tra versioni major — se aggiorni allauth a una major diversa,
riverifica manualmente (login, registrazione, reset password, eventuale
MFA) in un browser reale prima di considerare l'integrazione valida.

`django-allauth` **non è** una dipendenza del tema: gli override sono file
di template inerti se allauth non è installato o non è agganciato nelle
URL del progetto. È disponibile come extra opzionale, solo per
documentazione/test:

```bash
uv add "django-agesci-campania-theme[allauth]"
```

---

## Esempio minimo di attivazione

```python
# settings.py

INSTALLED_APPS = [
    ...,
    "django.contrib.sites",
    "agesci_theme",        # PRIMA delle app allauth — vedi nota sopra
    "allauth",
    "allauth.account",
    ...,
]

MIDDLEWARE = [
    ...,
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    ...,
]

SITE_ID = 1
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

FORM_RENDERER = "agesci_theme.forms.AgesciFormRenderer"
```

```python
# urls.py
urlpatterns = [
    ...,
    path("accounts/", include("allauth.urls")),
]
```

Un esempio funzionante completo (incluso `ACCOUNT_LOGIN_METHODS` e le altre
settings di allauth 65.x) è nel progetto demo, in
`example_project/config/settings.py`.
