from django.db import models
from datetime import date

from .rider import Rider


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
    winner = models.ForeignKey(Rider, on_delete=models.CASCADE, null=True, blank=True, related_name='race_winner')
    predict_winner = models.ForeignKey(Rider, on_delete=models.CASCADE, null=True, blank=True, related_name='race_predict_winner')
    one_day_race = models.BooleanField(default=False)
    note = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        from .course import Course
        if is_new and self.one_day_race:
            Course.objects.create(race=self, name=self.name + str(date.today().year))
        elif self.one_day_race:
            course = Course.objects.filter(race=self).first()
            if course:
                course.winner = self.winner
                course.predict_winner = self.predict_winner
                course.save()

    def __str__(self):
        return f"{self.name} - {self.date}"
