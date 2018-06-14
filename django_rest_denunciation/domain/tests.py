from json import dumps
from django.test import TestCase, Client
from rest_framework import status
from .factories import DomainAdministratorFactory


class DomainAdministratorTest(TestCase):

    def setUp(self):
        self.admin = DomainAdministratorFactory.create()
        self.client_test = Client()

    def test_reset_password(self):
        response = self.client_test.put('/api/domain/admins/reset_password/',
                                        dumps({'email': self.admin.email}),
                                        'application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password_with_wrong_email(self):
        email = self.admin.email + 'teste'
        response = self.client_test.put('/api/domain/admins/reset_password/',
                                        dumps({'email': email}),
                                        'application/json')

        self.assertEqual(response.data, {'detail': 'user not found'})
