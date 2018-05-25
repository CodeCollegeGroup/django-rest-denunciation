from django.test import TestCase
from .models import ConcreteSingleModel


class TestSingleModel(TestCase):

    def test_first_instance(self):
        ConcreteSingleModel.objects.create()
        ConcreteSingleModel.objects.all().delete()

        new_object = ConcreteSingleModel.objects.create()
        self.assertEqual(new_object.pk, 1)

    def test_many_instances(self):
        def test_for_instance(attr):
            new_object = ConcreteSingleModel.objects.create(attr=attr)
            self.assertEqual(new_object.attr, attr)
            self.assertEqual(new_object.pk, 1)

        test_for_instance('1')
        test_for_instance('2')
        test_for_instance('3')
        self.assertEqual(len(ConcreteSingleModel.objects.all()), 1)
