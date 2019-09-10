import base64

from django.http import HttpRequest


def get_basic_auth_header(user, password):
    """
    Return a dict containg the correct headers to set to make HTTP Basic Auth request
    """
    user_pass = "{0}:{1}".format(user, password)
    auth_string = base64.b64encode(user_pass.encode("utf-8"))
    auth_headers = {
        "HTTP_AUTHORIZATION": "Basic " + auth_string.decode("utf-8"),
    }

    return auth_headers

def convert_to_http_request(request, data):
    http_request = HttpRequest()
    http_request.POST = request.POST.copy()
    http_request.POST = data
    http_request.method = 'POST'
    http_request.META = request.META

    return http_request