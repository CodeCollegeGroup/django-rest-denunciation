import factory
from factory.fuzzy import (
    FuzzyInteger,
    FuzzyChoice
)
from . import models


class DenunciableFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Denunciable

    denunciable_id = FuzzyInteger(0, 1000)

    denunciable_type = FuzzyChoice([
        'comment',
        'image',
        'document'
    ])


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
