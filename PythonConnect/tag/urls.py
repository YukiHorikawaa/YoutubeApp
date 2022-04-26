from django.urls import path
from . import views
# from django.conf import settings
# from django.contrib.staticfiles import views
# from django.urls import re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'app'
urlpatterns = [
    path(r'', views.SearchTAG, name='SearchTAG'),
    path("tag/ajax/", views.call_write_word, name="call_write_word"),
    path("index/", views.index, name="index"),
    path("tag/", views.no_url, name="no_url_SearchTAG"),
    path("tag_out/", views.no_url, name="no_url_SearchTAG_out"),
]
urlpatterns += staticfiles_urlpatterns()
# #for static method
# if settings.DEBUG:
#     urlpatterns += [
#         re_path(r'^static/(?P<path>.*)$', views.serve),
#     ]
