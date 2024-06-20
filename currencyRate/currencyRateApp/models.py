from django.db import models

class ExchangeRate(models.Model):
    date = models.DateField()
    rate = models.FloatField()
    
    # sets a tuple of fields that must be unique when considered together
    class Meta:
        unique_together = ('date', 'rate')

    def __str__(self):
        return f"{self.date}: {self.rate}"
