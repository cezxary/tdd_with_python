from django.db import models


# Create your models here.
class List(models.Model):
    pass


# TODO: Adjust model so that items are associated with different lists
class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=0, on_delete=models.CASCADE)
