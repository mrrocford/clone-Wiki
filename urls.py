from django.urls import include, path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>/", views.page, name="page"),
    path("search/", views.search, name="search"),
    path("new/", views.new, name="new"),
    path("edit/", views.edit, name="edit"),
    path("random/", views.random_page, name="random_page")
]