from apiwrapper.endpoints.endpoint import Endpoint


class Session(Endpoint):

    __endpoint_session = 'session'

    @classmethod
    def _get_base_endpoint(cls, session_id):
        endpoint = '/%s/%d' % (cls.__endpoint_session, session_id)
        return endpoint

    def delete_session(self, session_id):
        endpoint = self._get_base_endpoint(session_id)

        return self._make_delete_request(endpoint)
