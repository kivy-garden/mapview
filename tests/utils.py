from unittest import mock


def patch_requests_get(response_json=None):
    response = mock.Mock()
    response.return_value.json.return_value = response_json
    return mock.patch("requests.get", response)
