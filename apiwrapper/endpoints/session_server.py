from apiwrapper.endpoints.endpoint import Endpoint


class SessionServer(Endpoint):

    __endpoint_session_server = "session-server"

    @classmethod
    def _get_base_endpoint(cls):
        return "/%s" % cls.__endpoint_session_server

    def create_new_session_server(self):
        endpoint = self._get_base_endpoint()
        payload = {"secret": self._api_client.api_key}

        return self._make_post_request(endpoint, payload)


