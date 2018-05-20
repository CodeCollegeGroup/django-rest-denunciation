import factory
import factory.fuzzy
import datetime
import pytz
from . import models
from users.factories import OrdinaryUserFactory
from projects.factories import ProjectFactory


class CommentFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Comment

    author = factory.SubFactory(
        OrdinaryUserFactory
    )

    project = factory.SubFactory(
        ProjectFactory
    )

    date_time = factory.fuzzy.FuzzyDateTime(
        datetime.datetime.now(tz=pytz.timezone('UTC'))
    )

    message = factory.Faker(
        'word'
    )


class FeedbackFeatureFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.FeedbackFeature

    author = factory.SubFactory(
        OrdinaryUserFactory
    )

    project = factory.SubFactory(
        ProjectFactory
    )

    comments = factory.SubFactory(
        CommentFactory
    )

    date_time = factory.fuzzy.FuzzyDateTime(
        datetime.datetime.now(tz=pytz.timezone('UTC'))
    )


class RatingFactory(FeedbackFeatureFactory):

    class Meta:
        model = models.Rating

    like = factory.Iterator(
        [True, False]
    )


class DenouncementFactory(FeedbackFeatureFactory):

    class Meta:
        model = models.Denouncement

    justification = factory.Faker(
        'word'
    )


class DenouncementStateFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.DenouncementState

    denouncement = factory.SubFactory(
        DenouncementFactory
    )


class NullStateFactory(DenouncementStateFactory):

    class Meta:
        model = models.NullState


class SolvedStateFactory(DenouncementStateFactory):

    class Meta:
        model = models.SolvedState


class WaitingStateFactory(DenouncementStateFactory):

    class Meta:
        model = models.WaitingState


class DoneStateFactory(DenouncementStateFactory):

    class Meta:
        model = models.DoneState
