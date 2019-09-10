import logging

from django.contrib.auth import get_user_model
from django.urls import reverse
from oauth2_provider.models import get_application_model
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.views import ProtectedResourceView
from rest_framework.test import APITestCase, APIClient
from django.test import RequestFactory, TestCase
import json

logger = logging.getLogger(__name__)
from rest_framework import status
from .utils import get_basic_auth_header

Application = get_application_model()
UserModel = get_user_model()


# mocking a protected resource view
class ResourceView(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return "This is a protected resource"


class BaseTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.application = Application(
            name="Test Password Application",
            client_type=Application.CLIENT_PUBLIC,
            authorization_grant_type=Application.GRANT_PASSWORD,
        )
        self.application.save()
        oauth2_settings._SCOPES = ["read", "write"]
        oauth2_settings._DEFAULT_SCOPES = ["read", "write"]

    def tearDown(self):
        self.application.delete()

class TestPasswordTokenView(BaseTest):
    def test_get_token(self):
        """
        Request an access token using Resource Owner Password Flow
        """
        token_request_data = {
            "username": "test_user42",
            "password": "123456",
        }
        auth_headers = get_basic_auth_header(self.application.client_id, self.application.client_secret)

        response = self.client.post(reverse("register"), data=token_request_data, **auth_headers)
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content.decode("utf-8"))
        self.assertEqual(content["token_type"], "Bearer")
        self.assertEqual(content["scope"], "read write")
        self.assertEqual(content["expires_in"], oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)

# class OAuth2TestCase(APITestCase):
#
#     def test_user_registration_valid_data(self):
#         """Tests register view"""
#         client = APIClient()
#
#         response = client.post('/authentication/register/', {"username": "tesdsdstuser9", "password": "1234abcd"},
#                                header={"Content-Type": "application/x-www-form-urlencoded", "Accept":"application/json"})
#         logger.info("Response {}".format(response))
#         logger.info("Response Header: {}".format(response['WWW-Authenticate']))
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertNotEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_user_registration_invalid_data(self):
    #     """Tests register view"""
    #     client = APIClient()
    #     response = client.post('/authentication/register/', {"username": "!!!!!", "password": "1234abcd"},
    #                            header={"Content-Type": "application/json"})
    #     logger.info("Response {}".format(response))
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
    #
    # def test_user_registration_invalid_data2(self):
    #     """Tests register view"""
    #     client = APIClient()
    #     response = client.post('/authentication/register/', {"username": "testuser157", "random": "sfdfdfd"},
    #                            header={"Content-Type": "application/json"})
    #     logger.info("Response {}".format(response))
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)








