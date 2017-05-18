from apiwrapper.endpoints.cash_register import CashRegister
from apiwrapper.endpoints.endpoint import Endpoint


class TabUsage(Endpoint):
    __endpoint_tab_usage_single = "tab-usage-single"
    __endpoint_tab_usage_multiple = "tab-usage-multiple"

    @classmethod
    def _get_base_endpoint(cls, user_id, account_id, cash_id, tab_uri,
                           tab_id=None):
        endpoint = CashRegister._get_base_endpoint(user_id, account_id,
                                                   cash_id)
        endpoint += "/%s" % tab_uri
        if tab_id is not None:
            endpoint += "/%s" % tab_id
        return endpoint

    # Tab Usage Single Logic
    def get_all_tab_usage_singles(self, user_id, account_id, cash_id):
        endpoint = self._get_base_endpoint(user_id, account_id, cash_id,
                                           self.__endpoint_tab_usage_single)

        return self._make_get_request(endpoint)

    def get_tab_usage_single_by_id(self, user_id, account_id, cash_id, tab_id):
        endpoint = self._get_base_endpoint(user_id, account_id, cash_id,
                                           self.__endpoint_tab_usage_single,
                                           tab_id)

        return self._make_get_request(endpoint)

    # Tab Usage Multiple Logic
    def get_all_tab_usage_multiples(self, user_id, account_id, cash_id):
        endpoint = self._get_base_endpoint(user_id, account_id, cash_id,
                                           self.__endpoint_tab_usage_multiple)

        return self._make_get_request(endpoint)

    def get_tab_usage_multiple_by_id(self, user_id, account_id, cash_id,
                                     tab_id):
        endpoint = self._get_base_endpoint(user_id, account_id, cash_id,
                                           self.__endpoint_tab_usage_multiple,
                                           tab_id)

        return self._make_get_request(endpoint)
