from django.db import models
from .race import Race


class Course(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField(max_length=200)
    start = models.CharField(max_length=120, null=True, blank=True)
    end = models.CharField(max_length=120, null=True, blank=True)
    distance_km = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    elevation_gain_m = models.IntegerField(null=True, blank=True)
    note = models.CharField(max_length=500, null=True, blank=True)
    key_point = models.CharField(max_length=500, null=True, blank=True)
    profile_score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.race.name} - {self.start} ~ {self.end}"
