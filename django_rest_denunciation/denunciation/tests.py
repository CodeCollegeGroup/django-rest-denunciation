from json import dumps
from .models import Denunciation, NullState, WaitingState
from django import test
from rest_framework import status
from .models import (
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

        state = WaitingState.objects.create()
        self.denunciation.current_state = state

    def test_save_denunciation(self):
        self.denunciation.save()

    def test_set_state(self):
        self.denunciation.save()
        self.denunciation.set_state(self.null_state)

        self.assertTrue(
            isinstance(self.denunciation.current_state, NullState)
        )

    def test_save(self):
        self.denunciation.save()

        # pylint: disable=protected-access
        self.assertTrue(
            isinstance(self.denunciation.current_state,
                       self.denunciation._initial_state)
        )
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

    def setUp(self):
        DenunciationCategory.objects.create(name='Racismo', gravity='H')
        DenunciationCategory.objects.create(name='Plágio', gravity='M')

    def response_post(self, json):
        response = self.client.post(
            '/api/denunciation/',
            dumps(json),
            content_type='application/json'
        )

        return response

    def test_create(self):

        response = self.response_post(self.json1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get('/api/denunciation/1/evaluating/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        denunciation = Denunciation.objects.get(pk=1)
        self.assertEqual(denunciation.current_state.name, 'EvaluatingState')

        response = self.client.patch(
            '/api/denunciation/1/done/',
            dumps(self.json5),
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

        response = self.client.get('/api/denunciation/1/null/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        denunciation = Denunciation.objects.get(pk=1)
        self.assertEqual(denunciation.current_state.name, 'NullState')

        response = self.client.get('/api/denunciation/1/waiting/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_5(self):
        response = self.response_post(self.json4)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete(self):
        response = self.response_post(self.json1)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.delete(
            '/api/denunciation/1/',
            follow=False
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Denunciation.objects.count(), 0)
