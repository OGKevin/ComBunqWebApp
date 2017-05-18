from apiwrapper.endpoints.endpoint import Endpoint
from apiwrapper.endpoints.user import User


class DraftShareInviteBank(Endpoint):

    __endpoint_share_draft = "draft-share-invite-bank"
    __endpoint_share_draft_qr = "qr-code-content"

    @classmethod
    def _get_base_endpoint(cls, user_id, draft_id=None):
        endpoint = User._get_base_endpoint(user_id)
        endpoint += "/%s" % cls.__endpoint_share_draft
        if draft_id is not None:
            endpoint += "/%d" % draft_id
        return endpoint

    def get_all_invite_drafts(self, user_id):
        endpoint = self._get_base_endpoint(user_id)

        return self._make_get_request(endpoint)

    def get_invite_draft_by_id(self, user_id, draft_id):
        endpoint = self._get_base_endpoint(user_id, draft_id)

        return self._make_get_request(endpoint)

    def get_qr_code_content_for_invite_draft(self, user_id, draft_id):
        endpoint = self._get_base_endpoint(user_id, draft_id)
        endpoint += "/%s" % self.__endpoint_share_draft_qr

        return self._make_get_request(endpoint)
