from django.urls import path
from . import views
# from django.conf import settings
# from django.contrib.staticfiles import views
# from django.urls import re_path

app_name = 'myapp'
urlpatterns = [
    # path(r'', views.index, name='index'),
    # path('seo/', views.YoutubeSEO, name='YoutubeSEO'),
    # 以下を追記(views.pyのcall_write_data()にデータを送信できるようにする)
    path("app/ajax/", views.call_write_data, name="call_write_data"),
    path("app/seo/", views.no_url, name="no_url_YoutubeSEO"),
    path("app/seo_out/", views.no_url, name="no_url_YoutubeSEO_out"),
    path("app/Terms_service/", views.Terms_service, name="Terms_service"),
]
# #for static method
# if settings.DEBUG:
#     urlpatterns += [
#         re_path(r'^static/(?P<path>.*)$', views.serve),
#     ]
