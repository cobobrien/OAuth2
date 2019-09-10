from oauth2_provider.views import TokenView, RevokeTokenView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import requests
from .utils import convert_to_http_request
from .serializers import CreateUserSerializer
import logging
logger = logging.getLogger(__name__)

CLIENT_ID = 'Pwx8rU7pn8sIg1bERNVOXp8UBq9Ssx2CSUYfnjXh'
CLIENT_SECRET = 'w09cYxgLW4k4ix9njUeRi8YURP3EUHpzIRX9G0Xz8mbMYYCMfSpAqVTtoaMxZbUKTvKZLiykhVTh3mAv1UiWe0ZwxNyzypeOokWDDgyySqbPgbo24jMy1MjgT5LNG2aZ'


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    '''
    Register - registers user to the server. Input should be in the format:
    {"username": "username", "password": "1234abcd"}
    '''

    serializer = CreateUserSerializer(data=request.data)
    logger.info("Request Data: {}".format(request.data))
    if serializer.is_valid():
        serializer.save()
        data={
            'grant_type': 'password',
            'username': request.data['username'],
            'password': request.data['password'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        }
        http_request = convert_to_http_request(request, data)
        token_view = TokenView()
        view_response = token_view.post(request=http_request)
        logger.info("Register Response: {}".format(view_response.content))
        return view_response

    logger.info("Serializer Errors: {}".format(serializer.errors))
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    '''
    Login - get tokens with username and password. Input should be in the format:
    {"username": "username", "password": "1234abcd"}
    '''

    data={
        'grant_type': 'password',
        'username': request.data['username'],
        'password': request.data['password'],
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    http_request = convert_to_http_request(request, data)
    token_view = TokenView()
    view_response = token_view.post(request=http_request)
    logger.info("Login Response: {}".format(view_response.content))
    return view_response

@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    '''
    Get refresh-token for long-term access:
    {"refresh_token": "<token>"}
    '''

    data={
        'grant_type': 'refresh_token',
        'refresh_token': request.data['refresh_token'],
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    http_request = convert_to_http_request(request, data)
    token_view = TokenView()
    view_response = token_view.post(request=http_request)
    logger.info("Refresh Token Response: {}".format(view_response.content))
    return view_response


@api_view(['POST'])
@permission_classes([AllowAny])
def revoke_token(request):
    '''
    Logout - revoke tokens.
    {"token": "<token>"}
    '''

    data={
        'token': request.data['token'],
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    http_request = convert_to_http_request(request, data)
    revoke_token = RevokeTokenView()
    view_response = revoke_token.post(request=http_request)

    # return success message (would be empty otherwise)
    if view_response.status_code == requests.codes.ok:
        return Response({'message': 'token revoked'},view_response.status_code)
    # Return the error
    return view_response.content
