from apiwrapper.endpoints.endpoint import Endpoint


class SessionServer(Endpoint):

    endpoint_session_server = "session-server"

    @classmethod
    def get_base_endpoint(cls):
        return "/%s" % cls.endpoint_session_server

    def create_new_session_server(self):
        endpoint = self.get_base_endpoint()
        payload = {"secret": self.api_client.api_key}

        return self._make_post_request(endpoint, payload)


