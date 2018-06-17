import factory
from . import models


class DenunciationFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Denunciation

    justification = factory.Faker(
        'word'
    )


class DenunciationStateFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.DenunciationState

    denunciation = factory.SubFactory(
        DenunciationFactory
    )


class NullStateFactory(DenunciationStateFactory):

    class Meta:
        model = models.NullState


class SolvedStateFactory(DenunciationStateFactory):

    class Meta:
        model = models.DoneState


class WaitingStateFactory(DenunciationStateFactory):

    class Meta:
        model = models.WaitingState


class DoneStateFactory(DenunciationStateFactory):

    class Meta:
        model = models.DoneState
