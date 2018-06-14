import factory
from . import models


class DomainAdministratorFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.DomainAdministrator

    first_name = factory.Faker(
        'first_name'
    )

    last_name = factory.Faker(
        'last_name'
    )

    username = factory.LazyAttribute(
        lambda a: '{0}_{1}'.format(a.first_name, a.last_name)
    )

    email = factory.LazyAttribute(
        lambda o: '%s@example.org' % o.first_name
    )
