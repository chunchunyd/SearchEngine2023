from django.db import models
from enum import Enum

WSZZDW = Enum(
    "法院"
)


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50)


class Index(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='indexes')#