from apiwrapper.endpoints.credential_password_ip import CredentialPasswordIp
from apiwrapper.endpoints.endpoint import Endpoint


class PermittedIp(Endpoint):

    __endpoint_permitted_ip = "ip"

    @classmethod
    def _get_base_endpoint(cls, user_id, credential_id, ip_id=None):
        endpoint = CredentialPasswordIp._get_base_endpoint(user_id, credential_id)
        endpoint += "/%s" % cls.__endpoint_permitted_ip
        if ip_id is not None:
            endpoint += "/%d" % ip_id
        return endpoint

    def get_all_permitted_ip(self, user_id, credential_ip):
        endpoint = self._get_base_endpoint(user_id, credential_ip)

        return self._make_get_request(endpoint)

    def get_permitted_ip_by_id(self, user_id, credential_id, ip_id):
        endpoint = self._get_base_endpoint(user_id, credential_id, ip_id)

        return self._make_get_request(endpoint)
