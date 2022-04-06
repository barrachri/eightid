from django.db import models

from src.gid import django


class AppModel(models.Model):
    id = django.GIDField(primary_key=True)
