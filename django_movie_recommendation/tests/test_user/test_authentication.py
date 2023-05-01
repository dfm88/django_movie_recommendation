from django.urls import reverse
from rest_framework import status
from tests.base import BaseTest


class AuthenticationApiTest(BaseTest):
    @classmethod
    def setUpClass(cls):
        cls.api_login = 'user:user__token_obtain_pair'
        cls.api_get_movies = 'movie:movie__list'
        super().setUpClass()

    def test_correct_authentication(self):
        """
        GIVEN an existing user
        WHEN a login is performed with the given user with correct credentials
        THEN  response contains authentication tokens and user can do authenticated calls
        """
        url = reverse(self.api_login)
        user_data = {
            "username": self.user1.username,
            "password": 'test',
        }
        resp = self.client.post(url, data=user_data)
        resp_data = resp.json()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(resp_data.get('access'))
        self.assertIsNotNone(resp_data.get('refresh'))

        url = reverse(self.api_get_movies)
        headers = {"Authorization": f"Bearer {resp_data['access']}"}
        resp = self.client.get(url, headers=headers)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_wrong_authentication(self):
        """
        GIVEN an existing user
        WHEN a login is performed with the given user with correct credentials
        THEN  response contains authentication tokens and user can't do authenticated calls
        """
        url = reverse(self.api_login)
        user_data = {
            "username": self.user1.username,
            "password": 'wrong_password',
        }
        resp = self.client.post(url, data=user_data)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        resp_data = resp.json()
        self.assertIsNone(resp_data.get('access'))
        self.assertIsNone(resp_data.get('refresh'))

        url = reverse(self.api_get_movies)
        headers = {"Authorization": f"Bearer {resp_data.get('access')}"}
        resp = self.client.get(url, headers=headers)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
