from singleton_model import SingletonModel
from django.db import models
from domain.models import Domain


class DenunciationState(SingletonModel):

    name = models.CharField(max_length=100, default='')

    _not_implemented_exception = NotImplementedError(
        'This method must be implemented at all children classes'
    )

    def specific_delete(self):
        raise self._not_implemented_exception

    def specific_notify_denunciator(self):
        raise self._not_implemented_exception


class NullState(DenunciationState):

    # Exceptions to detect if void methods are being called
    def specific_delete(self):
        raise Exception('Specific deletion')

    def specific_notify_denunciator(self):
        raise Exception('Specific notifier')

    def save(self, *args, **kwargs):
        # pylint: disable=arguments-differ
        self.name = 'NullState'
        super(DenunciationState, self).save(*args, **kwargs)


class EvaluatingState(DenunciationState):

    def specific_delete(self):
        pass

    def specific_notify_denunciator(self):
        pass

    def save(self, *args, **kwargs):
        # pylint: disable=arguments-differ
        self.name = 'EvaluatingState'
        super(DenunciationState, self).save(*args, **kwargs)


class WaitingState(DenunciationState):

    def specific_delete(self):
        pass

    def specific_notify_denunciator(self):
        pass

    def save(self, *args, **kwargs):
        # pylint: disable=arguments-differ
        self.name = 'WaitingState'
        super(DenunciationState, self).save(*args, **kwargs)


class DoneState(DenunciationState):

    def specific_delete(self):
        pass

    def specific_notify_denunciator(self):
        pass

    def save(self, *args, **kwargs):
        # pylint: disable=arguments-differ
        self.name = 'DoneState'
        super(DenunciationState, self).save(*args, **kwargs)


class Denunciable(models.Model):

    denunciable_id = models.IntegerField(default=0)

    denunciable_type = models.CharField(max_length=500, default='')

    denunciable_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("denunciable_id", "denunciable_type"),)


class Denouncer(models.Model):

    email = models.CharField(max_length=100, unique=True)

    fake_denunciation = models.IntegerField(default=0)


class Denunciation(models.Model):

    denunciable = models.ForeignKey(
        'Denunciable',
        on_delete=models.CASCADE
    )

    current_state = models.ForeignKey(
        'DenunciationState',
        on_delete=models.CASCADE,
    )

    categories = models.ManyToManyField('DenunciationCategory')

    justification = models.CharField(max_length=500, default='')

    current_state = models.ForeignKey(
        'DenunciationState',
        related_name='denunciations',
        on_delete=models.CASCADE
    )

    _initial_state = WaitingState

    domain = models.ForeignKey(Domain, on_delete=models.SET_NULL, null=True)

    denunciable = models.ForeignKey(
        'Denunciable',
        related_name='denunciations',
        on_delete=models.CASCADE
    )

    denouncer = models.ForeignKey(
        'Denouncer',
        related_name='denunciations',
        on_delete=models.CASCADE,
        null=True
    )

    evaluate = models.CharField(max_length=500, default='')

    fake = models.BooleanField(default=False)

    def delete_denunciation(self):
        self.current_state.specific_delete()

    def notify_denunciator(self):
        self.current_state.specific_notify_denunciator()

    def set_state(self, state):
        self.current_state = state

        if not isinstance(state, NullState):
            self.notify_denunciator()

    def __str__(self):
        return self.justification

    def save(self, *args, **kwargs):
        # pylint: disable=arguments-differ
        super(Denunciation, self).save(*args, **kwargs)


class DenunciationCategory(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    GRAVITY_CHOICES = (
        ('High', 'H'),
        ('Medium', 'M'),
        ('Low', 'L')
    )

    gravity = models.CharField(
        max_length=10,
        choices=GRAVITY_CHOICES,
    )
