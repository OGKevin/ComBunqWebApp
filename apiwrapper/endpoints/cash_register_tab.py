from apiwrapper.endpoints.cash_register import CashRegister
from apiwrapper.endpoints.endpoint import Endpoint
from apiwrapper.endpoints.monetary_account import MonetaryAccount


class CashRegisterTab(Endpoint):
    __endpoint_cash_register_tab = "tab"
    __endpoint_cash_register_tab_item = "tab-item"
    __endpoint_cash_register_tab_qr_code = "qr-code-content"
    __endpoint_cash_register_tab_result_inquiry = "tab-result-inquiry"
    __endpoint_cash_register_tab_result_response = "tab-result-response"

    @classmethod
    def _get_base_endpoint(cls, user_id, account_id, cash_id,
                           tab_uuid=None):
        endpoint = CashRegister._get_base_endpoint(user_id, account_id,
                                                   cash_id)
        endpoint += "/%s" % cls.__endpoint_cash_register_tab
        if tab_uuid is not None:
            endpoint += "/%s" % tab_uuid
        return endpoint

    # Cash Register Tab Logic
    def get_all_cash_register_tabs(self, user_id, account_id, cash_id):
        endpoint = self._get_base_endpoint(user_id, account_id, cash_id)

        return self._make_get_request(endpoint)

    def get_cash_register_tab_by_id(self, user_id, account_id, cash_id,
                                    tab_uuid):
        endpoint = self._get_base_endpoint(user_id, account_id, cash_id,
                                           tab_uuid)

        return self._make_get_request(endpoint)

    # Cash Register Tab Item Logic
    def get_all_tab_items_for_tab(self, user_id, account_id, cash_id, tab_id):
        endpoint = self._get_base_endpoint(user_id, account_id, cash_id,
                                           tab_id)
        endpoint += "/%s" % self.__endpoint_cash_register_tab_item

        return self._make_get_request(endpoint)

    def get_tab_item_by_id(self, user_id, account_id, cash_id, tab_uuid,
                           item_id):
        endpoint = self._get_base_endpoint(user_id, account_id, cash_id,
                                           tab_uuid)
        endpoint += "/%s/%d" % (self.__endpoint_cash_register_tab_item,
                                item_id)

        return self._make_get_request(endpoint)

    # Cash Register Tab QR Code Logic
    def get_qr_code_for_cash_register_tab(self, user_id, account_id, cash_id,
                                          tab_uuid):
        endpoint = self._get_base_endpoint(user_id, account_id, cash_id,
                                           tab_uuid)
        endpoint += "/%s" % self.__endpoint_cash_register_tab_qr_code

        return self._make_get_request(endpoint)

    # Cash Register Tab Result Inquiry Logic
    def get_all_inquiry_results_for_tab(self, user_id, account_id, cash_id,
                                        tab_uuid):
        endpoint = self._get_base_endpoint(user_id, account_id, cash_id,
                                           tab_uuid)
        endpoint += "/%s" % self.__endpoint_cash_register_tab_result_inquiry

        return self._make_get_request(endpoint)

    def get_inquiry_result_by_id(self, user_id, account_id, cash_id,
                                 tab_uuid, inquiry_id):
        endpoint = self._get_base_endpoint(user_id, account_id, cash_id,
                                           tab_uuid)
        endpoint += "/%s/%d" % (
            self.__endpoint_cash_register_tab_result_inquiry,
            inquiry_id
        )

        return self._make_get_request(endpoint)

    # Cash Register Tab Result Response Logic
    def get_response_result_for_tab(self, user_id, account_id):
        endpoint = MonetaryAccount._get_base_endpoint(user_id, account_id)
        endpoint += "/%s" % self.__endpoint_cash_register_tab_result_response

        return self._make_get_request(endpoint)

    def get_response_result_by_id(self, user_id, account_id, response_id):
        endpoint = MonetaryAccount._get_base_endpoint(user_id, account_id)

        endpoint += "/%s/%d" % (
            self.__endpoint_cash_register_tab_result_response,
            response_id
        )

        return self._make_get_request(endpoint)
