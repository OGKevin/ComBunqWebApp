from apiwrapper.endpoints.endpoint import Endpoint
from apiwrapper.endpoints.monetary_account import MonetaryAccount


class Payment(Endpoint):

    __endpoint_payment = "payment"
    __endpoint_payment_batch = "payment-batch"
    __endpoint_payment_response = "request-response"
    __endpoint_payment_chat = "chat"

    @classmethod
    def _get_base_endpoint(cls, user_id, account_id):
        return MonetaryAccount._get_base_endpoint(user_id, account_id)

    # Payment Logic
    def get_all_payments_for_account(self, user_id, account_id):
        endpoint = self._get_base_endpoint(user_id, account_id)
        endpoint += "/%s" % self.__endpoint_payment

        return self._make_get_request(endpoint)

    def get_payment_by_id(self, user_id, account_id, payment_id):
        endpoint = self._get_base_endpoint(user_id, account_id)
        endpoint += "/%s/%d" % (self.__endpoint_payment, payment_id)

        return self._make_get_request(endpoint)

    def get_chat_for_payment(self, user_id, account_id, payment_id):
        endpoint = self._get_base_endpoint(user_id, account_id)
        endpoint += "/%s/%d/%s" % (
            self.__endpoint_payment,
            payment_id,
            self.__endpoint_payment_chat
        )

        return self._make_get_request(endpoint)

    # Payment Batch Logic
    def get_all_payments_batches_for_account(self, user_id, account_id):
        endpoint = self._get_base_endpoint(user_id, account_id)
        endpoint += "/%s" % self.__endpoint_payment_batch

        return self._make_get_request(endpoint)

    def get_payment_batch_by_id(self, user_id, account_id, batch_id):
        endpoint = self._get_base_endpoint(user_id, account_id)
        endpoint += "/%s/%d" % (self.__endpoint_payment_batch, batch_id)

        return self._make_get_request(endpoint)
