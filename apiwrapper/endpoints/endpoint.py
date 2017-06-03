import logging

logger = logging.getLogger(name='raven')


class Endpoint:
    """Base class for endpoints
    Implements generic functions to make HTTP requests
    """

    def __init__(self, api_client):
        self._api_client = api_client

    def _make_get_request(self, endpoint, verify=True):
        res = self._api_client.get(endpoint, verify)
        if res.status_code is not 200:
            logger.error(res.json()['Error'][0]['error_description'])
        return res

    def _make_post_request(self, endpoint, payload):
        res = self._api_client.post(endpoint, payload)
        if res.status_code is not 200:
            logger.error(res.json()['Error'][0]['error_description'])
        return res
