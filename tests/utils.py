from unittest import mock

from requests.models import Response


def patch_requests_get(response_json=None, status_code=200):
    response = Response()
    response.json = lambda: response_json
    response.status_code = status_code
    m_get = mock.Mock(return_value=response)
    return mock.patch("requests.get", m_get)
