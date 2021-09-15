from django.db import models


class Visit(models.Model):
    domain = models.CharField(max_length=100)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.domain
