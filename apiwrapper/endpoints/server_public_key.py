from apiwrapper.endpoints.endpoint import Endpoint
from apiwrapper.endpoints.installation import Installation


class ServerPublicKey(Endpoint):

    __endpoint_server_public_key = "server-public-key"

    @classmethod
    def _get_base_endpoint(cls, installation_id):
        endpoint = Installation._get_base_endpoint(installation_id)
        endpoint += "/%s" % cls.__endpoint_server_public_key

        return endpoint

    def get_server_pubkey_for_installation(self, installation_id):
        endpoint = self._get_base_endpoint(installation_id)

        return self._make_get_request(endpoint)
