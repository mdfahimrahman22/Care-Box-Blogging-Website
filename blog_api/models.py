from django.db import models
from django.conf import settings
import django
from django.db.models.signals import pre_save
from django.dispatch import receiver
from blog_api.generate_summary import summarize_text


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
    summary = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    posted_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"


@receiver(pre_save, sender=Blog)
def generate_summary(sender, instance, **kwargs):
    numOfWords, summarizedText = summarize_text(instance.content)
    print("Total number of words in the blog post = ", numOfWords)
    instance.summary = summarizedText
