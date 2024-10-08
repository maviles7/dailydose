from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('doses/', views.dose_list, name='dose-index'),
    path('doses/favorites', views.fav_dose_list, name='fav-dose-index'), 
    path('doses/bookmarks', views.bookmark_dose_list, name='bookmark-dose-index'), 
    path('doses/upload', views.upload, name='upload'), 
]
