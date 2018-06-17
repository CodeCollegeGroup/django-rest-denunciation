from json import dumps
from django import test
from django.urls import reverse
from rest_framework import status
from .models import (
    Denunciation,
    NullState,
    Denunciable,
    DenunciationCategory
)


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


class TestDenunciationComplete(test.TestCase):

    def setUp(self):
        DenunciationCategory.objects.create(name='Racismo',
                                            gravity='High')
        DenunciationCategory.objects.create(name='Plágio',
                                            gravity='Medium')

        self.client = test.Client()

    def test_create(self):
        response = self.client.post(
            '/api/denunciations/denunciation-complete/',
            dumps({"denunciable": {
                       "denunciable_id": 30,
                       "denunciable_type": "imagem"
                  },
                   "denunciation": {
                       "categories": ["Racismo", "Plágio"],
                       "justification": "copiou imagem racista"
                  },
            }),
            content_type='application/json'
        )

        denunciation = Denunciation.objects.last()
        denunciable = Denunciable.objects.last()

        self.assertEqual(denunciation.denunciable, denunciable)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestDenunciationQueue(test.TestCase):

    def setUp(self):
        self.denunciable = Denunciable.objects.create(
            denunciable_id=1,
            denunciable_type='type'
        )

        self.denunciation = Denunciation.objects.create(
            justification='justification',
            denunciable=self.denunciable
        )
        self.denunciation_url = self._get_detail_url(self.denunciation.pk)
        self.client = test.Client()

    def test_get_queue(self):
        response = self.client.get('/api/denunciations/denunciation-queue/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, 
            ("{{'denunciation_queue': ['{}']}}").format(self.denunciation_url)
        )

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
