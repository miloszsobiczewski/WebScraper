from django.db import models


class Task(models.Model):
    url = models.CharField(max_length=100)
    status = models.CharField(max_length=30, default='idle')
    txt_ind = models.BooleanField(default=False)
    img_ind = models.BooleanField(default=False)
    txt_slug = models.CharField(max_length=100, blank=True)
    img_slug = models.TextField(blank=True)
    date = models.DateTimeField(auto_now=True, blank=True)