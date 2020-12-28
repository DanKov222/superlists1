from django.db import models


class Item(models.Model):
    """Элементы списка"""
    text = models.TextField(default='')
    list = models.ForeignKey('List', default=None, on_delete=models.CASCADE)


class List(models.Model):
    """Списки"""
    pass