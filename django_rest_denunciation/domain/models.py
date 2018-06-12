from django.db import models
from django.contrib.auth.models import User
# from django.core.mail import EmailMessage


class DomainAdministrator(User):

    def recover_domain_key(self, domain_key=None):
        pass

    def recover_password(self):
        """Reset password sending in e-mail"""

        random_password = DomainAdministrator.objects.make_random_password()
        self.set_password(random_password)
        self.save()

        """
        message = ""Olá,\nSua senha foi resetada, acesse
                     a plataforma e troque a senha\n
                     Sua nova senha é:\n {}"".format(random_password)
        email = EmailMessage('Password reset',
                             message, to=[self.email])
        email.send()
        """

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
