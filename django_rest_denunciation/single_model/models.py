from django.db import models


class SingleModel(models.Model):

    def delete(self, *args, **kwargs):
        pass

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        if self.pk is not None:
            super(SingleModel, self).save(*args, **kwargs)
        else:
            self.pk = 1
            self.save()

    class Meta:
        abstract = True


class ConcreteSingleModel(SingleModel):

    attr = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )
