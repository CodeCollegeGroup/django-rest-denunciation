from json import dumps
import datetime
from django import test
from django.urls import reverse
from rest_framework import status
from domain.factories import (
    DomainFactory
)
from .models import (
    Denunciable,
    DenunciationCategory,
    Denunciation,
    NullState,
    WaitingState
)
from domain.models import Domain, DomainAdministrator


class TestDenunciationStates(test.TestCase):

    def setUp(self):
        self.null_state = NullState.objects.create()
        self.denunciable = Denunciable.objects.create(
            denunciable_id=1,
            denunciable_type='type'
        )

        self.denunciation = Denunciation(
            justification='justification',
            denunciable=self.denunciable
        )

        state = WaitingState.objects.create()
        self.denunciation.current_state = state

    def test_save_denunciation(self):
        self.denunciation.save()

    def test_set_state(self):
        self.denunciation.save()
        self.denunciation.set_state(self.null_state)

        self.assertTrue(isinstance(self.denunciation.current_state, NullState))

    def test_save(self):
        self.denunciation.save()

        # pylint: disable=protected-access
        self.assertTrue(isinstance(self.denunciation.current_state,
                        self.denunciation._initial_state))
        # pylint: disable=protected-access

    def test_delete_denunciation(self):
        self._test_method_state_method(
            'Specific deletion',
            self.denunciation.delete_denunciation
        )

    def test_notify_denunciator(self):
        self._test_method_state_method(
            'Specific notifier',
            self.denunciation.notify_denunciator
        )

    def _test_method_state_method(self, exception_message, tested_method):
        self.denunciation.save()
        self.denunciation.set_state(self.null_state)

        with self.assertRaisesMessage(Exception, exception_message):
            tested_method()


class TestDenunciation(test.TestCase):

    def setUp(self):
        DenunciationCategory.objects.create(name='Racismo', gravity='High')
        DenunciationCategory.objects.create(name='Plágio', gravity='Medium')
        self.adm = DomainAdministrator.objects.create(id=1)
        self.dom = Domain()
        self.dom.application_name = "www.test.com"
        self.dom.administrator = self.adm
        self.dom.save()

    json1 = {
        "denunciable": {
            "denunciable_id": 30,
            "denunciable_type": "imagem"
        },
        "denunciation": {
            "categories": ["Racismo", "Plágio"],
            "justification": "copiou imagem racista"
        }
    }

    json2 = {
        "denunciable": {
            "denunciable_id": 30,
            "denunciable_type": "imagem"
        },
        "denunciation": {
            "categories": ["oi", "oi2"],
            "justification": "copiou imagem racista"
        }
    }

    json3 = {
        "denunciable": {
            "denunciable_id": 30,
            "denunciable_type": "imagem"
        },
        "denunciation": {
            "justification": "copiou imagem racista"
        }
    }

    json4 = {
        "denunciable": {
            "denunciable_id": 50,
            "denunciable_type": "imagem"
        },
        "denunciation": {
            "categories": ["Racismo", "Plágio"],
            "justification": "copiou imagem racista",
            "denouncer": "joao@unb.br"
        }
    }

    json5 = {
        "evaluation": 'adfafdd',
        "fake": True
    }

    def format_dict(self, json):
        json['key'] = self.dom.key

        return json

    def response_post(self, json):
        response = self.client.post(
            '/api/denunciations/denunciation/',
            dumps(self.format_dict(json)),
            content_type='application/json'
        )

        return response

    def test_index(self):

        response = self.client.get(
            '/api/denunciations/denunciation/',
            format='json',
            **{'HTTP_KEY': self.dom.key}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show(self):

        response = self.response_post(self.json1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(
            '/api/denunciations/denunciation/1/',
            format='json',
            **{'HTTP_KEY': self.dom.key}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):

        response = self.response_post(self.json1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(
            '/api/denunciations/denunciation/1/evaluating/',
            format='json',
            **{'HTTP_KEY': self.dom.key}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        denunciation = Denunciation.objects.get(pk=1)
        self.assertEqual(denunciation.current_state.type_name, 'evaluatingstate')

        response = self.client.patch(
            '/api/denunciations/denunciation/1/done/',
            dumps(self.format_dict(self.json5)),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_2(self):
        response = self.response_post(self.json2)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_3(self):
        response = self.response_post(self.json3)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_4(self):

        response = self.response_post(self.json1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(
            '/api/denunciations/denunciation/1/null/',
            format='json',
            **{'HTTP_KEY': self.dom.key}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        denunciation = Denunciation.objects.get(pk=1)
        self.assertEqual(denunciation.current_state.type_name, 'nullstate')

        response = self.client.get(
            '/api/denunciations/denunciation/1/waiting/',
            format='json',
            **{'HTTP_KEY': self.dom.key}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_5(self):
        response = self.response_post(self.json4)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete(self):
        response = self.response_post(self.json1)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.delete(
            '/api/denunciations/denunciation/1/',
            follow=False
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Denunciation.objects.count(), 0)

class TestDenunciationQueue(test.TestCase):

    def setUp(self):
        self.denunciable = Denunciable.objects.create(
            denunciable_id=1,
            denunciable_type='type'
        )

        self.denunciation = Denunciation.objects.create(
            justification='justification_1',
            denunciable=self.denunciable
        )
        self.denunciation_url = self._get_detail_url(self.denunciation.pk)
        self.client = test.Client()

    def test_get_queue(self):
        response = self.client.get('/api/denunciations/denunciation-queue/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            ('{{"denunciation_queue": ["{}"]}}').format(self.denunciation_url)
        )

    def test_get_queue_filtering(self):
        today = str(datetime.date.today())
        response = self.client.get(
            '/api/denunciations/denunciation-queue/',
            {'start': today, 'end': today}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            ('{{"denunciation_queue": ["{}"]}}').format(self.denunciation_url)
        )

        response = self.client.get(
            '/api/denunciations/denunciation-queue/',
            {'start': '1980-06-12', 'end': today}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            ('{{"denunciation_queue": ["{}"]}}').format(self.denunciation_url)
        )

        response = self.client.get(
            '/api/denunciations/denunciation-queue/',
            {'start': '1980-06-12', 'end': '2018-06-16'}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, ('{"denunciation_queue": []}'))

    def test_get_queue_ordering(self):
        denunciation2 = Denunciation.objects.create(
            justification='justification_2',
            denunciable=self.denunciable
        )
        denunciation2.created_at = str(datetime.date(2018, 6, 12))
        denunciation2.save()
        category1 = DenunciationCategory.objects.create(name='Racismo',
                                                             gravity='High')
        category2 = DenunciationCategory.objects.create(name='Plágio',
                                                             gravity='High')
        self.denunciation.categories.add(category1)
        denunciation2.categories.add(category2)
        self.denunciation.save()
        denunciation2.save()

        response = self.client.get(
            '/api/denunciations/denunciation-queue/',
            {'queries': ['gravity', 'date']}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, (
            '{{"denunciation_queue": ["{}", "{}"]}}').format(
                self._get_detail_url(denunciation2.pk),
                self._get_detail_url(self.denunciation.pk),
        ))

        response = self.client.get(
            '/api/denunciations/denunciation-queue/',
            {'queries': ['-gravity', 'date']}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, (
            '{{"denunciation_queue": ["{}", "{}"]}}').format(
                self._get_detail_url(denunciation2.pk),
                self._get_detail_url(self.denunciation.pk)
        ))

        response = self.client.get(
            '/api/denunciations/denunciation-queue/',
            {'queries': ['-date', 'gravity']}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, (
            '{{"denunciation_queue": ["{}", "{}"]}}').format(
                self._get_detail_url(self.denunciation.pk),
                self._get_detail_url(denunciation2.pk),
        ))

        response = self.client.get(
            '/api/denunciations/denunciation-queue/',
            {'queries': ['-date', '-gravity']}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, (
            '{{"denunciation_queue": ["{}", "{}"]}}').format(
                self._get_detail_url(self.denunciation.pk),
                self._get_detail_url(denunciation2.pk)
        ))

    @staticmethod
    def _get_detail_url(pk):
        path = reverse('denunciation-detail', kwargs={'pk': pk})
        denunciation_url = 'http://testserver' + path

        return denunciation_url


class TestDenunciationCategory(test.TestCase):

    def setUp(self):
        self.category = DenunciationCategory.objects.create(name='Racismo',
                                                            gravity=2)
        self.client = test.Client()

    def test_get_gravity_representation(self):
        category_url = reverse('denunciationcategory-detail',
                               kwargs={'pk': self.category.pk})

        response = self.client.get(category_url)

        gravity_representation = 'High'
        saved_gravity = response.data['gravity']
        self.assertEqual(saved_gravity, gravity_representation)

    def test_post_gravity_representation(self):
        data = {'name': 'Plágio',
                'gravity': 'Medium'}

        response = self.client.post(
            '/api/denunciations/denunciation-category/',
            dumps(data),
            content_type='application/json'
        )

        saved_gravity = DenunciationCategory.objects.last().gravity

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(saved_gravity, 1)
