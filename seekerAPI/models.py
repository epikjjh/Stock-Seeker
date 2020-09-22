from django.db import models


class Stock(models.Model):
    code = models.CharField(max_length=10)
    date = models.DateField()
    price = models.FloatField()
