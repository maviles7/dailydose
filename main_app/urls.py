from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('doses/', views.dose_list, name='dose-index'),
    path('doses/<int:dose_id>/', views.dose_detail, name='dose-detail'),
    path('favorite-doses/', views.favorite_doses_list, name='favorite-doses-list'), 
    path('doses/bookmarks', views.bookmark_doses_list, name='bookmark-dose-index'), 
    path('doses/upload', views.upload, name='upload'),
]