from django.db import models

from src.eightid import django


class AppModel(models.Model):
    id = django.EightIDField(primary_key=True)
