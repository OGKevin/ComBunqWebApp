from apiwrapper.endpoints.endpoint import Endpoint
from apiwrapper.endpoints.user import User


class CredentialPasswordIp(Endpoint):

    __endpoint_credential_password_ip = "credential-password-ip"

    @classmethod
    def _get_base_endpoint(cls, user_id, credential_id=None):
        endpoint = User._get_base_endpoint(user_id)
        endpoint += "/%s" % cls.__endpoint_credential_password_ip
        if credential_id is not None:
            endpoint += "/%d" % credential_id
        return endpoint

    def get_all_credentials_for_user(self, user_id):
        endpoint = self._get_base_endpoint(user_id)

        return self._make_get_request(endpoint)

    def get_credential_by_id(self, user_id, credential_id):
        endpoint = self._get_base_endpoint(user_id, credential_id)

        return self._make_get_request(endpoint)
