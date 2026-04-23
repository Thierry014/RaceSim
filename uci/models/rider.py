from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date


class Rider(models.Model):
    name = models.CharField(max_length=100, unique=True)
    nationality = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    note = models.CharField(max_length=500, null=True, blank=True)
    form = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)

    @property
    def age(self):
        if not self.date_of_birth:
            return None
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    def __str__(self):
        return f"{self.name}"
