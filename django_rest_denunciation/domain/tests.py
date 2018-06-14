from json import dumps
from django import test
from rest_framework import status
from .factories import DomainAdministratorFactory
from .models import Domain, KEY_LENGTH


class DomainAdministratorTest(test.TestCase):

    def setUp(self):
        self.admin = DomainAdministratorFactory.create()
        self.client_test = test.Client()

    def test_reset_password(self):
        response = self.client_test.put('/api/domains/admins/reset_password/',
                                        dumps({'email': self.admin.email}),
                                        'application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password_with_wrong_email(self):
        email = self.admin.email + 'teste'
        response = self.client_test.put('/api/domains/admins/reset_password/',
                                        dumps({'email': email}),
                                        'application/json')

        self.assertEqual(response.data, {'detail': 'user not found'})


class DomainModelsTests(test.TestCase):

    def test_create_domain_with_key(self):
        self.admin = DomainAdministratorFactory.create()
        domain = Domain.objects.create(
            administrator=self.admin,
            application_name='website',
            uri='http://mywebsite.com.br'
        )

        self.assertTrue(len(domain.key) == KEY_LENGTH)


class DomainViewsTests(test.TestCase):

    def setUp(self):
        self.admin = DomainAdministratorFactory.create()
        self.client_test = test.Client()

    def test_create_domain_ok(self):
        username = self.admin.username
        application_name = 'mywebsite'
        uri = 'http://www.mywebsite.com.br'

        response = self.client_test.post(
            '/api/domains/domains/',
            {'username': username,
             'application_name': application_name,
             'uri': uri}
        )
        last_saved = Domain.objects.last()

        self.assertEqual(application_name, last_saved.application_name)
        self.assertEqual(self.admin, last_saved.administrator)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
