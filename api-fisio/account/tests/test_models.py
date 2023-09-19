from django.test import TestCase
from account.models import User
from account.tests.factories.make_user import make_user


class UserTestCase(TestCase):

    def test_create_patient(self):
        user = make_user({'role': 1})

        self.assertEqual(user.role, 1)
        self.assertTrue(user.patient)

    def test_create_physiotherapist(self):
        user = make_user({'role': 2})

        self.assertEqual(user.role, 2)
        self.assertTrue(user.physiotherapist)

    def test_switch_relation_on_new_role(self):
        user = make_user({'role': 1})
        self.assertEqual(user.role, 1)
        self.assertTrue(user.patient)

        user.role = 2
        user.save()

        self.assertEqual(user.role, 2)
        self.assertTrue(user.physiotherapist)

        user.role = 1
        user.save()

        self.assertEqual(user.role, 1)
        self.assertTrue(user.patient)
