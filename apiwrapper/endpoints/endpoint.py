

class Endpoint:
    """Base class for endpoints
    Implements generic functions to make HTTP requests
    """

    def __init__(self, api_client):
        self._api_client = api_client

    def _make_get_request(self, endpoint, verify=True):
        return self._api_client.get(endpoint, verify)

    def _make_post_request(self, endpoint, payload):
        return self._api_client.post(endpoint, payload)
