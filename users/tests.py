import logging
from django.urls import reverse
from oauth2_provider.models import get_application_model
from oauth2_provider.settings import oauth2_settings
from django.test import TestCase
import json

logger = logging.getLogger(__name__)
from rest_framework import status
from .utils import get_basic_auth_header

Application = get_application_model()

class BaseTest(TestCase):
    def setUp(self):
        self.application = Application(
            name="Test Password Application",
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
        )
        self.application.save()

    def tearDown(self):
        self.application.delete()

class TestUserTokenView(BaseTest):

    def test_get_token(self):
        """
        Register User and get initial access token
        """
        token_request_data = {
            "username": "test_user",
            "password": "123456",
        }
        auth_headers = get_basic_auth_header(self.application.client_id, self.application.client_secret)

        response = self.client.post(reverse("register"), data=token_request_data, **auth_headers)
        logger.info("Test Response: {}".format(response))
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content.decode("utf-8"))

        self.assertEqual(content["token_type"], "Bearer")
        self.assertEqual(content["scope"], "read write")
        self.assertEqual(content["expires_in"], oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)

    def test_invalid_credentials(self):
        """
        Login user request with invalid password
        """
        token_request_data = {
            "username": "test_user",
            "password": "123456",
        }
        auth_headers = get_basic_auth_header(self.application.client_id, self.application.client_secret)

        response = self.client.post(reverse("register"), data=token_request_data, **auth_headers)

        token_request_data = {
            "username": "test_user",
            "password": "NOT_MY_PASS",
        }
        auth_headers = get_basic_auth_header(self.application.client_id, self.application.client_secret)

        response = self.client.post(reverse("login"), data=token_request_data, **auth_headers)
        self.assertEqual(response.status_code, 400)

    def test_valid_credentials(self):
        """
        Login user request with valid password
        """
        token_request_data = {
            "username": "test_user",
            "password": "123456",
        }
        auth_headers = get_basic_auth_header(self.application.client_id, self.application.client_secret)

        response = self.client.post(reverse("register"), data=token_request_data, **auth_headers)

        token_request_data = {
            "username": "test_user",
            "password": "123456",
        }
        auth_headers = get_basic_auth_header(self.application.client_id, self.application.client_secret)

        response = self.client.post(reverse("login"), data=token_request_data, **auth_headers)
        self.assertEqual(response.status_code, 200)

    def test_refresh_token(self):
        """
        Test refresh token view
        """
        token_request_data = {
            "username": "test_user",
            "password": "123456",
        }
        auth_headers = get_basic_auth_header(self.application.client_id, self.application.client_secret)

        response = self.client.post(reverse("register"), data=token_request_data, **auth_headers)
        content = json.loads(response.content.decode("utf-8"))
        refresh_token = content['refresh_token']
        logger.info("ACCESS TOKEN: {}".format(refresh_token))
        token_request_data = {
            "refresh_token": refresh_token,
        }
        auth_headers = get_basic_auth_header(self.application.client_id, self.application.client_secret)

        response = self.client.post(reverse("refresh"), data=token_request_data, **auth_headers)
        logger.info("Test Response: {}".format(response))
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content.decode("utf-8"))

        self.assertEqual(content["token_type"], "Bearer")
        self.assertEqual(content["scope"], "read write")
        self.assertEqual(content["expires_in"], oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)

    def test_refresh_token_with_acess_token(self):
        """
            Test refresh token view with incorrect token
        """
        token_request_data = {
            "username": "test_user",
            "password": "123456",
        }
        auth_headers = get_basic_auth_header(self.application.client_id, self.application.client_secret)

        response = self.client.post(reverse("register"), data=token_request_data, **auth_headers)
        content = json.loads(response.content.decode("utf-8"))
        access_token = content['access_token']
        logger.info("ACCESS TOKEN: {}".format(access_token))
        token_request_data = {
            "refresh_token": access_token,
        }
        auth_headers = get_basic_auth_header(self.application.client_id, self.application.client_secret)

        response = self.client.post(reverse("refresh"), data=token_request_data, **auth_headers)
        logger.info("Test Response: {}".format(response))
        self.assertEqual(response.status_code, 400)

    def test_revoke_token(self):
        """
           Test revoke token view
        """
        token_request_data = {
            "username": "test_user",
            "password": "123456",
        }
        auth_headers = get_basic_auth_header(self.application.client_id, self.application.client_secret)

        response = self.client.post(reverse("register"), data=token_request_data, **auth_headers)
        content = json.loads(response.content.decode("utf-8"))
        access_token = content['access_token']
        token_request_data = {
            "token": access_token,
        }
        auth_headers = get_basic_auth_header(self.application.client_id, self.application.client_secret)

        response = self.client.post(reverse("revoke"), data=token_request_data, **auth_headers)
        reponseJSON = response.json()
        logger.info("Test Response: {}".format(reponseJSON))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(reponseJSON['message'], "token revoked")

