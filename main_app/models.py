# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class NewsSource(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Dose(models.Model):
    source = models.ForeignKey(NewsSource, on_delete=models.CASCADE)
    author = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField()
    url_to_image = models.URLField(null=True, blank=True)
    published_at = models.DateTimeField()
    content = models.TextField(null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )  # If tracking saved articles
    category = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("dose-detail", kwargs={"dose_id": self.id})
    

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
    dose = models.ForeignKey(Dose, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Change text field to comment field
    text = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} - {self.dose.title}'
    
    class Meta:
        ordering = ['-created_at']
