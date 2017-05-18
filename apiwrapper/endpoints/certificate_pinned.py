from apiwrapper.endpoints.endpoint import Endpoint
from apiwrapper.endpoints.user import User


class CertificatePinned(Endpoint):

    __endpoint_user_pinned_certificates = "certificate-pinned"

    @classmethod
    def _get_base_endpoint(cls, user_id, certificate_id=None):
        endpoint = User._get_base_endpoint(user_id)
        endpoint += "/%s" % cls.__endpoint_user_pinned_certificates
        if certificate_id is not None:
            endpoint += "/%d" % certificate_id
        return endpoint

    def get_all_pinned_certificates_for_user(self, user_id):
        endpoint = self._get_base_endpoint(user_id)

        return self._make_get_request(endpoint)

    def get_pinned_certificate_by_id(self, user_id, certificate_id):
        endpoint = self._get_base_endpoint(user_id, certificate_id)

        return self._make_get_request(endpoint)
