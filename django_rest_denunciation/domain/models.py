from hashlib import sha256
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


KEY_LENGTH =  64  # 256 bits in hexadecimal


class DomainAdministrator(User):

    def recover_password(self):
        """
        Reset password sending in e-mail
        """

        random_password = DomainAdministrator.objects.make_random_password()
        self.set_password(random_password)
        self.save()

        message = """Olá,\nSua senha foi resetada, acesse
                     a plataforma e troque a senha.\n
                     Sua nova senha é:\n {}""".format(random_password)
        # self.send_email('Password Reset', message)

    def retrieve_denunciation_by_priority(self, priority_type=None):
        pass

    def send_email(self, title, message):
        email = EmailMessage(title, message, to=[self.email])
        email.send()


class Domain(models.Model):

    administrator = models.ForeignKey(
        'DomainAdministrator',
        on_delete=models.CASCADE,
    )

    application_name = models.CharField(
        max_length=50,
        unique=True
    )

    key = models.CharField(
        max_length=KEY_LENGTH,
        unique=True,
        editable=False
    )

    uri = models.URLField(max_length=150)

    def __str__(self):
        return self.uri

    def save(self, *args, **kwargs):
        self.key = self._generate_key(
            self.application_name,
            self.administrator.id
        )
        super(Domain, self).save(*args, **kwargs)

    @staticmethod
    def _generate_key(application_name, admin_id):
        microseconds = timezone.now().microsecond
        local_hash = abs(hash(application_name))

        key_seed = map(
            lambda c: str((ord(c)*microseconds)//admin_id + local_hash),
            list(application_name)
        )
        key_seed = '@'.join(key_seed)

        hash_obj = sha256(key_seed.encode())
        key = hash_obj.hexdigest()

        return key
