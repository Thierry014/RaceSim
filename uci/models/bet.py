from django.db import models
from django.contrib.auth.models import User
from .rider import Rider
from .course import Course


class Bet(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('won', 'Won'),
        ('lost', 'Lost'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bets')
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE, related_name='bets')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='bets')
    odd_rate = models.DecimalField(max_digits=6, decimal_places=2)
    bet_amount = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    credit_return = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.rider} - {self.bet_amount} - ({self.status}) - ({self.credit_return})"
