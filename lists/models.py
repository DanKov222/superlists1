from django.db import models


class Item(models.Model):
    """Элементы списка"""
    text = models.TextField(default='')