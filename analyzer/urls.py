from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),   # ✔ shows search form
    path("analyze/", views.analyze_github, name="analyze_github"),
    path("export/", views.export_pdf, name="export_pdf"),
]
