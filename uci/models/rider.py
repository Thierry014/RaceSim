from django.db import models


class Rider(models.Model):
    name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    note = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"
