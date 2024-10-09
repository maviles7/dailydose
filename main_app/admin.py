from django.contrib import admin
from .models import NewsSource, Dose, FavoriteDose, BookmarkDose

# Register your models here.
admin.site.register(NewsSource)
admin.site.register(Dose)
admin.site.register(FavoriteDose)
admin.site.register(BookmarkDose)
