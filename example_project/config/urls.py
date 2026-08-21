from django.contrib import admin
from django.urls import include, path
from app.views import components, form_demo, home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", home, name="home"),
    path("components/", components, name="components"),
    path("form-demo/", form_demo, name="form_demo"),
]
