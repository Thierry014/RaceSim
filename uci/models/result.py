from django.db import models

from .course import Course
from .rider import Rider

class Result(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    rank = models.IntegerField()
