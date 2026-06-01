from django.shortcuts import render
from agesci_theme.templatetags.agesci_tags import ZONE


def home(request):
    return render(request, "home.html", {"zone_list": sorted(ZONE.keys())})
