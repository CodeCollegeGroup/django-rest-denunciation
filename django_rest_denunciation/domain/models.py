from django.db import models


class Domain(models.Model):

    uri = models.URLField(max_length=150)

    key = models.CharField(max_length=50)

    def __str__(self):
        return self.uri
