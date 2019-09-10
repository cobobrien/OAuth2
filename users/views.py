from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.debug import sensitive_post_parameters
from oauth2_provider.models import get_access_token_model
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.signals import app_authorized
from oauth2_provider.views import TokenView
from oauth2_provider.views.mixins import OAuthLibMixin
from rest_framework import status
from requests import Request
from django.http import HttpRequest

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.generic import View


import requests
from rest_framework.utils import json

from .serializers import CreateUserSerializer
import logging
logger = logging.getLogger(__name__)

CLIENT_ID = 'Pwx8rU7pn8sIg1bERNVOXp8UBq9Ssx2CSUYfnjXh'
CLIENT_SECRET = 'w09cYxgLW4k4ix9njUeRi8YURP3EUHpzIRX9G0Xz8mbMYYCMfSpAqVTtoaMxZbUKTvKZLiykhVTh3mAv1UiWe0ZwxNyzypeOokWDDgyySqbPgbo24jMy1MjgT5LNG2aZ'


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    '''
    Registers user to the server. Input should be in the format:
    {"username": "username", "password": "1234abcd"}
    '''

    serializer = CreateUserSerializer(data=request.data)
    logger.info("Request Data {}".format(request.data))
    if serializer.is_valid():

        serializer.save()

        data={
            'grant_type': 'password',
            'username': request.data['username'],
            'password': request.data['password'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        }
        test_request = HttpRequest()
        test_request.POST = request.POST.copy()
        test_request.POST = data
        test_request.method = 'POST'
        test_request.META = request.META
        logger.info("Test META {}".format(test_request.META))
        logger.info("Test Request {}".format(test_request.POST))

        logger.info("Test REQUEST HEADERS {}".format(test_request.headers))
        test = TokenView()
        test_response = test.post(request=test_request)
        logger.info("Test Response {}".format(test_response.content))
        return test_response

    logger.info("Serializer Errors {}".format(serializer.errors))
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @method_decorator(csrf_exempt, name="dispatch")
# class TokenView(OAuthLibMixin, View):
#
#     server_class = oauth2_settings.OAUTH2_SERVER_CLASS
#     validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
#     oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS
#
#     @method_decorator(sensitive_post_parameters("password"))
#     def post(self, request, *args, **kwargs):
#         url, headers, body, status = self.create_token_response(request)
#         if status == 200:
#             access_token = json.loads(body).get("access_token")
#             if access_token is not None:
#                 token = get_access_token_model().objects.get(
#                     token=access_token)
#                 app_authorized.send(
#                     sender=self, request=request,
#                     token=token)
#         response = HttpResponse(content=body, status=status)
#
#         for k, v in headers.items():
#             response[k] = v
#         return response


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    '''
    Gets tokens with username and password. Input should be in the format:
    {"username": "username", "password": "1234abcd"}
    '''
    r = requests.post(
    'http://127.0.0.1:8000/o/token/',
        data={
            'grant_type': 'password',
            'username': request.data['username'],
            'password': request.data['password'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    return Response(r.json())



@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    '''
    Registers user to the server. Input should be in the format:
    {"refresh_token": "<token>"}
    '''
    r = requests.post(
    'http://127.0.0.1:8000/o/token/',
        data={
            'grant_type': 'refresh_token',
            'refresh_token': request.data['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    return Response(r.json())


@api_view(['POST'])
@permission_classes([AllowAny])
def revoke_token(request):
    '''
    Method to revoke tokens.
    {"token": "<token>"}
    '''
    r = requests.post(
        'http://127.0.0.1:8000/o/revoke_token/',
        data={
            'token': request.data['token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    # If it goes well return sucess message (would be empty otherwise)
    if r.status_code == requests.codes.ok:
        return Response({'message': 'token revoked'}, r.status_code)
    # Return the error if it goes badly
    return Response(r.json(), r.status_code)
