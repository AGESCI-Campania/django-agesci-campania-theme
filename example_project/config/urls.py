from django.contrib import admin
from django.urls import path
from app.views import home, components

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("components/", components, name="components"),
]
