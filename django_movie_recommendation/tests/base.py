from django.test import TestCase
from tests import factories


class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls):
        # create users
        cls.user1 = factories.UserFactory(username='user1')
        cls.user2 = factories.UserFactory(username='user2')
        cls.user3 = factories.UserFactory(username='user3')
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()
