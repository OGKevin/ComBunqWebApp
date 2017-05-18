from apiwrapper.endpoints.endpoint import Endpoint
from apiwrapper.endpoints.monetary_account import MonetaryAccount
from apiwrapper.endpoints.user import User


class Invoice(Endpoint):

    __endpoint_invoice = "invoice"

    @classmethod
    def _get_base_endpoint(cls, user_id, account_id, invoice_id=None):
        endpoint = MonetaryAccount._get_base_endpoint(user_id, account_id)
        endpoint += "/%s" % cls.__endpoint_invoice
        if invoice_id is not None:
            endpoint += "/%d" % invoice_id
        return endpoint

    def get_all_invoices_for_account(self, user_id, account_id):
        endpoint = self._get_base_endpoint(user_id, account_id)

        return self._make_get_request(endpoint)

    def get_all_invoices_for_user(self, user_id):
        endpoint = User._get_base_endpoint(user_id)
        endpoint += "/%s" % self.__endpoint_invoice

        return self._make_get_request(endpoint)

    def get_invoice_by_id(self, user_id, account_id, invoice_id):
        endpoint = self._get_base_endpoint(user_id, account_id, invoice_id)

        return self._make_get_request(endpoint)

