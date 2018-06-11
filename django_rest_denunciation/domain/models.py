from django.db import models
from django.contrib.auth.models import User


class DomainAdministrator(User):

    def recover_domain_key(self, domain_key=None):
        pass

    def recover_password(self):
        pass

    def retrieve_denunciation_by_priority(self, priority_type=None):
        pass


class Domain(models.Model):

    administrator = models.ForeignKey(
        DomainAdministrator,
        on_delete=models.CASCADE,
        null=True
    )

    uri = models.URLField(max_length=150)

    key = models.CharField(max_length=50)

    def __str__(self):
        return self.uri
