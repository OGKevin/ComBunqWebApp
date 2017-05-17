from apiwrapper.endpoints.user import User


class DraftShareInviteBank(User):

    endpoint_share_draft = "draft-share-invite-bank"
    endpoint_share_draft_qr = "qr-code-content"

    @classmethod
    def get_base_endpoint(cls, user_id, draft_id=None):
        endpoint = User.get_base_endpoint(user_id)
        endpoint += "/%s" % cls.endpoint_share_draft
        if draft_id is not None:
            endpoint += "/%d" % draft_id
        return endpoint

    def get_all_invite_drafts(self, user_id):
        endpoint = self.get_base_endpoint(user_id)

        return self._make_get_request(endpoint)

    def get_invite_draft_by_id(self, user_id, draft_id):
        endpoint = self.get_base_endpoint(user_id, draft_id)

        return self._make_get_request(endpoint)

    def get_qr_code_content_for_invite_draft(self, user_id, draft_id):
        endpoint = self.get_base_endpoint(user_id, draft_id)
        endpoint += "/%s" % self.endpoint_share_draft_qr

        return self._make_get_request(endpoint)
