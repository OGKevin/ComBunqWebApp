from apiwrapper.endpoints.endpoint import Endpoint


class Installation(Endpoint):

    __endpoint_installation = "installation"

    @classmethod
    def _get_base_endpoint(cls, installation_id=None):
        endpoint = "/%s" % cls.__endpoint_installation
        if installation_id is not None:
            endpoint += "/%d" % installation_id
        return endpoint

    def get_id_for_installation(self):
        endpoint = self._get_base_endpoint()

        return self._make_get_request(endpoint)

    def check_installation_id(self, installation_id):
        endpoint = self._get_base_endpoint(installation_id)

        return self._make_get_request(endpoint)

    def create_installation(self):
        endpoint = self._get_base_endpoint()
        payload = {"client_public_key": self._api_client.pubkey}

        return self._make_post_request(endpoint, payload)


