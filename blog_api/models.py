from django.db import models
from django.conf import settings
import django


def get_user_model_fk_ref():
    if django.VERSION[:2] >= (1, 5):
        return settings.AUTH_USER_MODEL
    else:
        return 'auth.User'


class Category(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.title}"


class Blog(models.Model):
    author = models.ForeignKey(
        get_user_model_fk_ref(), on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    content = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    posted_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"
