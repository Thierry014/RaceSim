from decimal import Decimal

from django.db import models
from .race import Race
from .rider import Rider

class Course(models.Model):

    DEFAULT_BET_AMOUNT = Decimal('1')

    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField(max_length=200)
    start = models.CharField(max_length=120, null=True, blank=True)
    end = models.CharField(max_length=120, null=True, blank=True)
    distance_km = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    elevation_gain_m = models.IntegerField(null=True, blank=True)
    note = models.TextField(max_length=500, null=True, blank=True)
    key_point = models.CharField(max_length=500, null=True, blank=True)
    profile_score = models.IntegerField(null=True, blank=True)
    profile_score_20k = models.IntegerField(null=True, blank=True)
    winner = models.ForeignKey(Rider, on_delete=models.CASCADE, null=True, blank=True, related_name='course_winner')
    predict_winner = models.ForeignKey(Rider, on_delete=models.CASCADE, null=True, blank=True, related_name='course_predict_winner')
    pre_analysis = models.TextField(max_length=500, null=True, blank=True)
    course_url = models.URLField(null=True, blank=True)
    is_won_by_breakaway = models.BooleanField(default=False)
    bingo_rate = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    settled = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_predict_winner_id = self.predict_winner_id

    def save(self, *args, **kwargs):
        predict_winner_changed = self.predict_winner_id != self.__original_predict_winner_id
        super().save(*args, **kwargs)
        if predict_winner_changed and self.predict_winner_id is not None and self.bingo_rate is not None:
            self._create_predict_bet()
        self.__original_predict_winner_id = self.predict_winner_id

    def _create_predict_bet(self):
        from django.contrib.auth.models import User
        from .bet import Bet

        admin = User.objects.filter(is_superuser=True).order_by('id').first()
        if admin is None:
            return

        # Replace any prior auto-bet this admin has on the course.
        Bet.objects.filter(course=self, user=admin).delete()
        Bet.objects.create(
            user=admin,
            rider=self.predict_winner,
            course=self,
            odd_rate=self.bingo_rate,
            bet_amount=self.DEFAULT_BET_AMOUNT,
        )

    def __str__(self):
        return f"{self.name}-{self.winner}"

    @property
    def bingo(self):
        return self.predict_winner == self.winner and self.winner is not None