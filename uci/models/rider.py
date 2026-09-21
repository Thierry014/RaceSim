from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date


class Rider(models.Model):
    FORM_TREND_CHOICES = [
        ('high', '↑'),
        ('increase', '↗'),
        ('normal', '→'),
        ('decrease', '↘'),
        ('low', '↓'),
    ]

    FORM_TO_TREND = {1: 'low', 2: 'decrease', 3: 'normal', 4: 'increase', 5: 'high'}
    SCORE_VALIDATORS = [MinValueValidator(1), MaxValueValidator(100)]

    name = models.CharField(max_length=100, unique=True)
    nationality = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    note = models.TextField(max_length=500, null=True, blank=True)
    form = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    form_trend = models.CharField(max_length=10, choices=FORM_TREND_CHOICES, null=True, blank=True, default='normal')
    form_duration = models.IntegerField(null=True, blank=True, default=14)
    date_duration_start = models.DateField(null=True, blank=True)
    breakaway = models.BooleanField(default=False)
    breakaway_note = models.CharField(max_length=100, null=True, blank=True)
    attack_index = models.IntegerField(null=True, blank=True, default=0)

    score_climb = models.IntegerField(null=True, blank=True, default=1, validators=SCORE_VALIDATORS)
    score_wave = models.IntegerField(null=True, blank=True, default=1, validators=SCORE_VALIDATORS)
    score_punch = models.IntegerField(null=True, blank=True, default=1, validators=SCORE_VALIDATORS)
    score_tt = models.IntegerField(null=True, blank=True, default=1, validators=SCORE_VALIDATORS)
    score_sprint = models.IntegerField(null=True, blank=True, default=1, validators=SCORE_VALIDATORS)
    score_steep = models.IntegerField(null=True, blank=True, default=1, validators=SCORE_VALIDATORS)

    limit_distance = models.FloatField(null=True, blank=True, default=10)
    limit_slope = models.FloatField(null=True, blank=True, default=10)

    form_history_cache = models.JSONField(default=list, blank=True)
    watch_listed = models.BooleanField(default=False)

    FORM_HISTORY_CACHE_MAX = 10

    class Meta:
        ordering = ['name']  # for admin

    @property
    def age(self):
        if not self.date_of_birth:
            return None
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    @property
    def predict_form(self):
        # 2~5
        if not self.date_duration_start:
            return 3
        num_of_day = (date.today() - self.date_duration_start).days
        if num_of_day > self.form_duration: return 3
        peak = self.form_duration / 2
        if num_of_day <= peak:
            pf = round((num_of_day / peak) * 5)
        else:
            pf= round(5-(((num_of_day - peak)/peak) * 5))
        if pf<2:
            pf = 2
        return pf


    def save(self, *args, **kwargs):
        form_changed = False
        if self.form is not None and self.pk:
            previous = Rider.objects.filter(pk=self.pk).values_list('form', flat=True).first()
            if previous is not None:
                delta = self.form - previous
                if delta > 1:
                    self.form_trend = 'high'
                elif delta == 1:
                    self.form_trend = 'increase'
                elif delta == 0:
                    self.form_trend = 'normal'
                elif delta == -1:
                    self.form_trend = 'decrease'
                else:
                    self.form_trend = 'low'
                form_changed = delta != 0
            else:
                form_changed = True
        elif self.form is not None:
            form_changed = True

        if form_changed:
            history = list(self.form_history_cache or [])
            history.append(self.form)
            self.form_history_cache = history[-self.FORM_HISTORY_CACHE_MAX:]

        super().save(*args, **kwargs)
        if form_changed:
            RiderFormHistory.objects.create(rider=self, form=self.form)

    def __str__(self):
        return f"{self.name}"


class RiderFormHistory(models.Model):
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE, related_name='form_history')
    form = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.rider.name} at {self.updated_at}"
