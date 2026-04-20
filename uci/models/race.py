from django.db import models


class Race(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    location = models.CharField(max_length=200)
    category = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} - {self.date}"
