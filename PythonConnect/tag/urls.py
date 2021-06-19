from django.urls import path
from . import views

app_name = 'tag'
urlpatterns = [
    path(r'', views.SearchTAG, name='SearchTAG'),
    path("ajax/", views.call_write_word, name="call_write_word"),
]