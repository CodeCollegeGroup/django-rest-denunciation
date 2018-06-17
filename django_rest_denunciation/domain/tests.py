from json import dumps
from django import test
from rest_framework import status
from .factories import DomainAdministratorFactory, DomainFactory
from .models import Domain, DomainAdministrator, KEY_LENGTH


class DomainAdministratorTest(test.TestCase):

    def setUp(self):
        self.admin = DomainAdministratorFactory.create()
        self.domain = DomainFactory.create(administrator=self.admin)
        self.client_test = test.Client()

    def test_reset_password(self):
        response = self.client_test.put(
            '/api/domains/admins/reset_password/',
            dumps({'email': self.admin.email}),
            'application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password_with_wrong_email(self):
        email = self.admin.email + 'teste'
        response = self.client_test.put(
            '/api/domains/admins/reset_password/',
            dumps({'email': email}),
            'application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_recover_domain_key(self):
        response = self.client_test.get(
            '/api/domains/admins/recover_domain_key/',
            {'application_name': self.domain.application_name},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_recover_domain_key_with_wrong_application_name(self):
        application_name = self.domain.application_name + 'teste'
        response = self.client_test.get(
            '/api/domains/admins/recover_domain_key/',
            {'application_name': application_name},
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_domain_administrator_ok(self):
        data = {'username': 'test_user', 'email': 'test@foo.com',
                'password': 'test_123', 'first_name': 'Tester',
                'last_name': 'The Greater'}

        response = self.client_test.post(
            '/api/domains/admins/',
            dumps(data),
            'application/json'
        )
        last_saved = DomainAdministrator.objects.last()

        self.assertEqual(data['username'], last_saved.username)
        self.assertEqual(data['first_name'], last_saved.first_name)
        self.assertEqual(data['last_name'], last_saved.last_name)
        self.assertEqual(data['email'], last_saved.email)
        self.assertTrue(last_saved.check_password(data['password']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_domain_administrator_wrong(self):
        data = {'username': '', 'email': 'test@foo.com',
                'password': '', 'first_name': 'Tester',
                'last_name': 'The Greater'}

        response = self.client_test.post(
            '/api/domains/admins/',
            dumps(data),
            'application/json'
        )
        last_saved = DomainAdministrator.objects.last()

        self.assertNotEqual(data['username'], last_saved.username)
        self.assertNotEqual(data['first_name'], last_saved.first_name)
        self.assertNotEqual(data['last_name'], last_saved.last_name)
        self.assertNotEqual(data['email'], last_saved.email)
        self.assertFalse(last_saved.check_password(data['password']))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DomainModelsTests(test.TestCase):

    def test_create_domain_with_key(self):
        admin = DomainAdministratorFactory.create()
        domain = Domain.objects.create(
            administrator=admin,
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
