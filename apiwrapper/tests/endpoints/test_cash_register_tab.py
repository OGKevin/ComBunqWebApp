from apiwrapper.endpoints.cash_register_tab import CashRegisterTab
from apiwrapper.tests.endpoints.test_endpoint import EndpointTest


class CashRegisterTabTest(EndpointTest):
    __base_endpoint_url = "/user/%d/monetary-account/%d/cash-register/%d/tab"

    @property
    def _base_endpoint(self):
        return self.__base_endpoint_url % (
            self.random_id,
            self.random_id,
            self.random_id
        )

    def setUp(self):
        super().setUp(CashRegisterTab)

    def test_get_base_endpoint(self):
        endpoint_should_be = self._base_endpoint

        endpoint_to_check = self.test_class._get_base_endpoint(
            self.random_id, self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_all_cash_register_tabs(self):
        endpoint_should_be = self._base_endpoint

        endpoint_to_check = self.test_class.get_all_cash_register_tabs(
            self.random_id, self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_cash_register_tab_by_id(self):
        endpoint_should_be = self._base_endpoint
        endpoint_should_be += "/%s" % self.random_uuid

        endpoint_to_check = self.test_class.get_cash_register_tab_by_id(
            self.random_id, self.random_id, self.random_id, self.random_uuid)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_all_tab_items_for_tab(self):
        endpoint_should_be = self._base_endpoint
        endpoint_should_be += "/%s/tab-item" % self.random_uuid

        endpoint_to_check = self.test_class.get_all_tab_items_for_tab(
            self.random_id, self.random_id, self.random_id, self.random_uuid)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_tab_item_by_id(self):
        endpoint_should_be = self._base_endpoint
        endpoint_should_be += "/%s/tab-item/%d" % (self.random_uuid,
                                                   self.random_id)

        endpoint_to_check = self.test_class.get_tab_item_by_id(
            self.random_id, self.random_id, self.random_id,
            self.random_uuid, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_qr_code_for_cash_register_tab(self):
        endpoint_should_be = self._base_endpoint
        endpoint_should_be += "/%s/qr-code-content" % self.random_uuid

        endpoint_to_check = self.test_class.get_qr_code_for_cash_register_tab(
            self.random_id, self.random_id, self.random_id, self.random_uuid)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_inquiry_result_for_tab(self):
        endpoint_should_be = self._base_endpoint
        endpoint_should_be += "/%s/tab-result-inquiry" % self.random_uuid

        endpoint_to_check = self.test_class.get_all_inquiry_results_for_tab(
            self.random_id, self.random_id, self.random_id, self.random_uuid)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_inquiry_result_by_id(self):
        endpoint_should_be = self._base_endpoint
        endpoint_should_be += "/%s/tab-result-inquiry/%d" % (
            self.random_uuid,
            self.random_id
        )

        endpoint_to_check = self.test_class.get_inquiry_result_by_id(
            self.random_id, self.random_id, self.random_id,
            self.random_uuid, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_response_result_for_tab(self):
        endpoint_should_be = "/user/%d/monetary-account/%d" \
                             "/tab-result-response" % (
                                 self.random_id, self.random_id
                             )

        endpoint_to_check = self.test_class.get_response_result_for_tab(
            self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_response_result_by_id(self):
        endpoint_should_be = "/user/%d/monetary-account/%d" \
                             "/tab-result-response/%d" % (
                                 self.random_id,
                                 self.random_id,
                                 self.random_id
                             )

        endpoint_to_check = self.test_class.get_response_result_by_id(
            self.random_id, self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)
