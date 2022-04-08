from django.urls import path
from . import views

app_name = 'myapp'
urlpatterns = [
    path(r'', views.index, name='index'),
    path('seo/', views.YoutubeSEO, name='YoutubeSEO'),
    # 以下を追記(views.pyのcall_write_data()にデータを送信できるようにする)
    # path("ajax/", views.call_write_data, name="call_write_data"),
    path("seo_nourl/", views.no_url, name="no_url_YoutubeSEO"),
    path("seo_nourl_out/", views.no_url, name="no_url_YoutubeSEO_out"),
]
