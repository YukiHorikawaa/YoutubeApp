from django.urls import path
from . import views

app_name = 'app'
urlpatterns = [
    path(r'', views.SearchTAG, name='SearchTAG'),
    path("ajax/", views.call_write_word, name="call_write_word"),
    path("index/", views.index, name="index"),
    path("tag/", views.no_url, name="no_url_SearchTAG"),
    path("tag_out/", views.no_url, name="no_url_SearchTAG_out"),
]