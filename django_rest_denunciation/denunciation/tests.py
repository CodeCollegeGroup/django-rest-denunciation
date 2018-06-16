from json import dumps
from django.test import TestCase
from .models import Denunciation, NullState
from django import test
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

    def test_create(self):
        response = self.client.post('/api/denunciation/', dumps({"id":1,"justification":"comentário ofencivo","denunciable_id":1,"denunciable_type":"Comment"}) ,content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
