from django.db import models


class Race(models.Model):
    
    CATEGORY_CHOICES = [
        ('classic', 'Classic'),
        ('high_mountain', 'High Mountain'),
        ('flat', 'Flat'),
        ('tour', 'Tour'),
        ('weekly', 'Weekly'),
    ]

    name = models.CharField(max_length=200)
    date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='classic')

    def __str__(self):
        return f"{self.name} - {self.date}"
