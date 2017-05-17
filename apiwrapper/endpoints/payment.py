from apiwrapper.endpoints.monetary_account import MonetaryAccount


class Payment(MonetaryAccount):

    endpoint_payment = "payment"
    endpoint_payment_batch = "payment-batch"
    endpoint_payment_response = "request-response"

    @classmethod
    def get_base_endpoint(cls, user_id, account_id):
        return MonetaryAccount.get_base_endpoint(user_id, account_id)

    # Payment Logic
    def get_all_payments_for_account(self, user_id, account_id):
        endpoint = self.get_base_endpoint(user_id, account_id)
        endpoint += "/%s" % self.endpoint_payment

        return self._make_get_request(endpoint)

    def get_payment_by_id(self, user_id, account_id, payment_id):
        endpoint = self.get_base_endpoint(user_id, account_id)
        endpoint += "/%s/%d" % (self.endpoint_payment, payment_id)

        return self._make_get_request(endpoint)

    def get_chat_for_payment(self, user_id, account_id, payment_id):
        endpoint = self.get_base_endpoint(user_id, account_id)
        endpoint += "/%s/%d/%s" % (
            self.endpoint_payment,
            payment_id,
            self.endpoint_chat
        )

        return self._make_get_request(endpoint)

    # Payment Batch Logic
    def get_all_payments_batches_for_account(self, user_id, account_id):
        endpoint = self.get_base_endpoint(user_id, account_id)
        endpoint += "/%s" % self.endpoint_payment_batch

        return self._make_get_request(endpoint)

    def get_payment_batch_by_id(self, user_id, account_id, batch_id):
        endpoint = self.get_base_endpoint(user_id, account_id)
        endpoint += "/%s/%d" % (self.endpoint_payment_batch, batch_id)

        return self._make_get_request(endpoint)
