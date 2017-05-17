from apiwrapper.endpoints.monetary_account import MonetaryAccount


class Invoice(MonetaryAccount):

    endpoint_invoice = "invoice"

    @classmethod
    def get_base_endpoint(cls, user_id, account_id, invoice_id=None):
        endpoint = MonetaryAccount.get_base_endpoint(user_id, account_id)
        endpoint += "/%s" % cls.endpoint_invoice
        if invoice_id is not None:
            endpoint += "/%d" % invoice_id
        return endpoint

    def get_all_invoices_for_account(self, user_id, account_id):
        endpoint = self.get_base_endpoint(user_id, account_id)

        return self._make_get_request(endpoint)

    def get_invoice_by_id(self, user_id, account_id, invoice_id):
        endpoint = self.get_base_endpoint(user_id, account_id, invoice_id)

        return self._make_get_request(endpoint)
