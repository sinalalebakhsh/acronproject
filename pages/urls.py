from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view() , name="home"),    
    path('sinalalebakhsh/', views.SinaLaleBakhshPhoto.as_view(), name="sinalalebakhsh_photo"),
    path('manifest/', views.Manifest.as_view(), name="manifest"),
]




