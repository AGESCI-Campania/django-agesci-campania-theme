from django.contrib import admin
from django.urls import include, path
from app.views import components, form_demo, form_demo_errori, home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", home, name="home"),
    path("components/", components, name="components"),
    path("form-demo/", form_demo, name="form_demo"),
    # stesso form già validato a vuoto: mostra gli errori senza POST
    # (serve anche alla demo statica su GitHub Pages, che non ha un server)
    path("form-demo/errori/", form_demo_errori, name="form_demo_errori"),
]
