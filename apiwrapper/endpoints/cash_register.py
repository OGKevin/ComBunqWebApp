from apiwrapper.endpoints.endpoint import Endpoint
from apiwrapper.endpoints.monetary_account import MonetaryAccount


class CashRegister(Endpoint):

    __endpoint_cash_register = "cash-register"
    __endpoint_cash_register_qr = "qr-code"
    __endpoint_cash_register_qr_content = "content"

    @classmethod
    def _get_base_endpoint(cls, user_id, account_id, cash_id=None):
        endpoint = MonetaryAccount._get_base_endpoint(user_id, account_id)
        endpoint += "/%s" % cls.__endpoint_cash_register
        if cash_id is not None:
            endpoint += "/%d" % cash_id
        return endpoint

    # Cash Register Logic
    def get_all_cash_registers_for_account(self, user_id, account_id):
        endpoint = self._get_base_endpoint(user_id, account_id)

        return self._make_get_request(endpoint)

    def get_cash_register_by_id(self, user_id, account_id, cash_id):
        endpoint = self._get_base_endpoint(user_id, account_id, cash_id)

        return self._make_get_request(endpoint)

    # Cash Register QR Code Logic
    def get_all_qr_codes_for_cash_register(self, user_id, account_id, cash_id):
        endpoint = self._get_base_endpoint(user_id, account_id, cash_id)
        endpoint += "/%s" % self.__endpoint_cash_register_qr

        return self._make_get_request(endpoint)

    def get_qr_code_by_id(self, user_id, account_id, cash_id, code_id):
        endpoint = self._get_base_endpoint(user_id, account_id, cash_id)
        endpoint += "/%s/%d" % (
            self.__endpoint_cash_register_qr,
            code_id
        )

        return self._make_get_request(endpoint)

    # QR Code Content
    def get_content_for_qr_code(self, user_id, account_id, cash_id, code_id):
        endpoint = self._get_base_endpoint(user_id, account_id, cash_id)
        endpoint += "/%s/%d/%s" % (
            self.__endpoint_cash_register_qr,
            code_id,
            self.__endpoint_cash_register_qr_content
        )
        return self._make_get_request(endpoint)
