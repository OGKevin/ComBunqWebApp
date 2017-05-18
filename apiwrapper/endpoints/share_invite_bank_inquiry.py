from apiwrapper.endpoints.endpoint import Endpoint
from apiwrapper.endpoints.monetary_account import MonetaryAccount


class ShareInviteBankInquiry(Endpoint):

    __endpoint_share_inquiry = "share-invite-bank-inquiry"

    @classmethod
    def _get_base_endpoint(cls, user_id, account_id, inquiry_id=None):
        endpoint = MonetaryAccount._get_base_endpoint(user_id, account_id)
        endpoint += "/%s" % cls.__endpoint_share_inquiry
        if inquiry_id is not None:
            endpoint += "/%d" % inquiry_id
        return endpoint

    def get_all_share_invite_bank_inquiries(self, user_id, account_id):
        endpoint = self._get_base_endpoint(user_id, account_id)

        return self._make_get_request(endpoint)

    def get_share_invite_bank_inquiry_by_id(self, user_id, account_id,
                                            inquiry_id):
        endpoint = self._get_base_endpoint(user_id, account_id, inquiry_id)

        return self._make_get_request(endpoint)
