from django.db import models
from .race import Race


class Course(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField(max_length=200)
    distance_km = models.DecimalField(max_digits=6, decimal_places=2)
    elevation_gain_m = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.race.name} - {self.name}"
