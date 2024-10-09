from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('doses/', views.dose_list, name='dose-index'),
    path('doses/<int:dose_id>/', views.dose_detail, name='dose-detail'),
    path('favorite-doses/', views.favorite_doses_list, name='favorite-doses-index'), 
    path('doses/favorites/<int:dose_id>/', views.favorite_dose, name='favorite-dose'),
    path('doses/unfavorite/<int:dose_id>/', views.unfavorite_dose, name='unfavorite-dose'),
    path('doses/bookmarks', views.bookmark_doses_list, name='bookmark-dose-index'),
    path('doses/bookmarks/<int:dose_id>/', views.bookmark_dose, name='bookmark-dose'),
    path('doses/unbookmark/<int:dose_id>/', views.unbookmark_dose, name='unbookmark-dose'),
    path('doses/upload', views.upload, name='upload'),
]