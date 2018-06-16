from singleton_model import SingletonModel
from abstract_related_model.models import AbstractRelatedModel
from django.db import models


class DenunciationState(SingletonModel, AbstractRelatedModel):

    denunciation = models.OneToOneField(
        'Denunciation',
        related_name='current_state',
        on_delete=models.SET_NULL,
        null=True
    )

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


class EvaluatingState(DenunciationState):

    def specific_delete(self):
        pass

    def specific_notify_denunciator(self):
        pass


class WaitingState(DenunciationState):

    def specific_delete(self):
        pass

    def specific_notify_denunciator(self):
        pass


class DoneState(DenunciationState):

    def specific_delete(self):
        pass

    def specific_notify_denunciator(self):
        pass


class Denunciable(models.Model):

    denunciable_id = models.IntegerField(default=0)

    denunciable_type = models.CharField(max_length=500, default='')

    denunciable_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("denunciable_id", "denunciable_type"),)


class Denunciation(models.Model):

    categories = models.ManyToManyField('DenunciationCategory')

    justification = models.CharField(max_length=500)

    current_state = DenunciationState

    _initial_state = WaitingState

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
        self._set_initial_state()

    def _set_initial_state(self):
        initial_state = self._initial_state.objects.create()
        self.set_state(initial_state)


class DenunciationCategory(SingletonModel, AbstractRelatedModel):

    name = models.CharField(max_length=100)

    GRAVITY_CHOICES = (
        ('High', 'H'),
        ('Medium', 'M'),
        ('Low', 'L')
    )

    gravity = models.CharField(
        max_length=10,
        choices=GRAVITY_CHOICES,
    )
