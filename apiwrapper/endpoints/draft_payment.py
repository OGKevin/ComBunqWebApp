from apiwrapper.endpoints.endpoint import Endpoint
from apiwrapper.endpoints.monetary_account import MonetaryAccount


class DraftPayment(Endpoint):

    __endpoint_draft_payment = "draft-payment"

    @classmethod
    def _get_base_endpoint(cls, user_id, account_id):
        endpoint = MonetaryAccount._get_base_endpoint(user_id)
        endpoint += "/%d/%s" % (
            account_id,
            cls.__endpoint_draft_payment
        )
        return endpoint

    def get_all_draft_payments_for_account(self, user_id, account_id):
        endpoint = self._get_base_endpoint(user_id, account_id)

        return self._make_get_request(endpoint)

    def get_draft_payment_by_id(self, user_id, account_id, draft_id):
        endpoint = self._get_base_endpoint(user_id, account_id)
        endpoint += "/%d" % draft_id

        return self._make_get_request(endpoint)
