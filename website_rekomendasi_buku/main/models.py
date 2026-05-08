from django.db import models
from django.contrib.auth.models import User


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    book_key = models.CharField(max_length=100)   # dari Open Library
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover_id = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    logged_in_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email or self.user.username} @ {self.logged_in_at:%Y-%m-%d %H:%M}"


class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    query = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.query


class AIRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    input_text = models.TextField()
    result = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AI - {self.user.username}"