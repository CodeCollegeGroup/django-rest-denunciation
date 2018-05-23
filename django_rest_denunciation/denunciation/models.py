from django.db import models


class DenunciationState(models.Model):

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


class SolvedState(DenunciationState):

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


class Denunciation(models.Model):

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
