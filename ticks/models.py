from django.db import models
from django.conf import settings


SYMBOL_CHOICES = ((symbol, symbol) for symbol in settings.SYMBOLS)


class Tick(models.Model):
    date = models.DateTimeField()
    symbol = models.CharField(max_length=3, choices=SYMBOL_CHOICES)
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.FloatField()
