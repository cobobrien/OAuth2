import logging
from wsgiref import headers

from rest_framework.test import APITestCase, APIClient
from django.test import Client
from rest_framework.utils import json

logger = logging.getLogger(__name__)
from rest_framework import status

class OAuth2TestCase(APITestCase):

    def test_user_registration_valid_data(self):
        """Tests register view"""
        client = APIClient()
        response = client.post('/authentication/register/', {"username": "testuser157", "password": "1234abcd"},
                               header={"Content-Type": "application/json"})
        logger.info("Response {}".format(response))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_invalid_data(self):
        """Tests register view"""
        client = APIClient()
        response = client.post('/authentication/register/', {"username": "!!!!!", "password": "1234abcd"},
                               header={"Content-Type": "application/json"})
        logger.info("Response {}".format(response))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_registration_invalid_data2(self):
        """Tests register view"""
        client = APIClient()
        response = client.post('/authentication/register/', {"username": "testuser157", "random": "sfdfdfd"},
                               header={"Content-Type": "application/json"})
        logger.info("Response {}".format(response))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)








