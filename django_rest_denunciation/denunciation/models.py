from singleton_model import SingletonModel
from django.db import models
from domain.models import Domain


class DenunciationState(SingletonModel):

    _not_implemented_exception = NotImplementedError(
        'This method must be implemented at all children classes'
    )

    @property
    def name(self):
        return self.__class__.__name__.lower()

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

    denunciable_id = models.IntegerField()

    denunciable_type = models.CharField(max_length=100)

    denunciable_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('denunciable_id', 'denunciable_type')


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

    domain = models.ForeignKey(
        Domain,
        on_delete=models.SET_NULL,
        null=True
    )

    justification = models.CharField(max_length=500)

    created_at = models.DateField(auto_now_add=True)

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
        initial_state = self._initial_state.objects.create()
        self.current_state = initial_state

        super(Denunciation, self).save(*args, **kwargs)


class DenunciationCategory(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    ## Cannot use this because gambiarra on serializers and here
    #GRAVITY_CHOICES = (
    #    (2, 2),  # High
    #    (1, 1),  # Medium
    #    (0, 0)   # Low
    #)

    gravity = models.CharField(max_length=10)

    gravity_map = {
        'High': '2',
        'Medium': '1',
        'Low': '0'
    }

    def save(self, *args, **kwargs):
        if self.gravity in ('High', 'Medium', 'Low'):
            self.gravity = self.gravity_map[self.gravity]

        super(DenunciationCategory, self).save(*args, **kwargs)
