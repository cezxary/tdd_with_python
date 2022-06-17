from django.db import models


# Create your models here.
# TODO: Adjust model so that items are associated with different lists
class Item(models.Model):
    text = models.TextField(default='')
