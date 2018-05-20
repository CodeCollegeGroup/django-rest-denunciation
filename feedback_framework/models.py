from django.db import models


class FeedbackFeature(models.Model):

    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE
    )

    author = models.ForeignKey(
        'users.OrdinaryUser',
        on_delete=models.CASCADE
    )

    comments = models.ForeignKey(
       'Comment',
       on_delete=models.SET_NULL,
       null=True
    )

    date_time = models.DateTimeField()


class Comment(FeedbackFeature):

    message = models.CharField(max_length=400)

    def answer(self):
        pass

    def dennounce(self):
        pass

    def like(self):
        pass

    def delete_denouncement(self):
        pass

    def change(self):
        pass

    def __str__(self):
        return self.message


class Rating(FeedbackFeature):

    like = models.BooleanField()

    def change(self):
        pass

    def __str__(self):
        return "{like}".format(**self.__dict__)


class DenouncementState(models.Model):

    denouncement = models.OneToOneField(
        'Denouncement',
        related_name='current_state',
        on_delete=models.SET_NULL,
        null=True
    )

    _not_implemented_exception = NotImplementedError(
        'This method must be implemented at all children classes'
    )

    def specific_delete(self):
        raise self._not_implemented_exception

    def specific_notify_denouncer(self):
        raise self._not_implemented_exception


class NullState(DenouncementState):
    # Exceptions to detect if void methods are being called

    def specific_delete(self):
        raise Exception('Specific deletion')

    def specific_notify_denouncer(self):
        raise Exception('Specific notifier')


class SolvedState(DenouncementState):

    def specific_delete(self):
        pass

    def specific_notify_denouncer(self):
        pass


class WaitingState(DenouncementState):

    def specific_delete(self):
        pass

    def specific_notify_denouncer(self):
        pass


class DoneState(DenouncementState):

    def specific_delete(self):
        pass

    def specific_notify_denouncer(self):
        pass


class Denouncement(FeedbackFeature):

    justification = models.CharField(max_length=500)

    current_state = FeedbackFeature

    _default_state = WaitingState

    def delete_denouncement(self):
        self.current_state.specific_delete()

    def notify_denouncer(self):
        self.current_state.specific_notify_denouncer()

    def set_state(self, state):
        self.current_state = state

        if not isinstance(state, NullState):
            self.notify_denouncer()

    def __str__(self):
        return self.justification

    def save(self, *args, **kwargs):
        # pylint: disable=arguments-differ
        super(Denouncement, self).save(*args, **kwargs)
        self._set_default_state()

    def _set_default_state(self):
        initial_state = self._default_state.objects.create()
        self.set_state(initial_state)
