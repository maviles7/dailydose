# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class NewsSource(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Dose(models.Model):
    title = models.CharField(max_length=500)
    category = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField(max_length=10000,null=True, blank=True)
    description = models.TextField(max_length=500)
    url = models.URLField(max_length=1000)
    image = models.URLField(max_length=1000, null=True, blank=True)
    published_at = models.DateTimeField()
    source = models.ForeignKey(NewsSource, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )  # If tracking saved articles

    def __str__(self):
        return self.title


class FavoriteDose(models.Model):
    dose = models.ForeignKey(Dose, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    favorited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.dose.title}"


class BookmarkDose(models.Model):
    dose = models.ForeignKey(Dose, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bookmarked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.dose.title}"


class Comment(models.Model):
    dose = models.ForeignKey(Dose, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Change text field to comment field
    text = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} - {self.dose.title}"

    class Meta:
        ordering = ["-created_at"]
