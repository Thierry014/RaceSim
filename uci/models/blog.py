from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    publish_date = models.DateField(null=True, blank=True)
    published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-publish_date']

    def __str__(self):
        return self.title
