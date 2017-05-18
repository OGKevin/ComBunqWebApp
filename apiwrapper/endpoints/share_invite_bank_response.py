from apiwrapper.endpoints.endpoint import Endpoint
from apiwrapper.endpoints.user import User


class ShareInviteBankResponse(Endpoint):

    __endpoint_share_response = "share-invite-bank-response"

    @classmethod
    def _get_base_endpoint(cls, user_id, response_id=None):
        endpoint = User._get_base_endpoint(user_id)
        endpoint += "/%s" % cls.__endpoint_share_response
        if response_id is not None:
            endpoint += "/%d" % response_id
        return endpoint

    def get_all_invite_responses(self, user_id):
        endpoint = self._get_base_endpoint(user_id)

        return self._make_get_request(endpoint)

    def get_invite_response_by_id(self, user_id, response_id):
        endpoint = self._get_base_endpoint(user_id, response_id)

        return self._make_get_request(endpoint)
