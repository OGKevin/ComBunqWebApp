

class Endpoint:
    """Base class for endpoints
    Implements generic functions to make HTTP requests
    """

    endpoint_chat = "chat"

    def __init__(self, api_client):
        self.api_client = api_client

    def _make_get_request(self, endpoint):
        res = self.api_client.get(endpoint)
        return res.json()

    def _make_post_request(self, endpoint, payload):
        res = self.api_client.post(endpoint, payload)
        return res.json()
