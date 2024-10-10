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
    path('dose/<int:dose_id>/add-comment/', views.add_comment, name='add-comment'),
    path('dose/<int:dose_id>/delete-comment/<int:comment_id>/', views.delete_comment, name='delete-comment'),
    path('doses/upload', views.upload, name='upload'),
]