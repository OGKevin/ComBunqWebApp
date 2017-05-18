import random

from apiwrapper.endpoints.tab_usage import TabUsage
from apiwrapper.tests.endpoints.test_endpoint import EndpointTest


class TabUsageTest(EndpointTest):
    __base_endpoint_url = "/user/%d/monetary-account/%d/cash-register/%d"
    __endpoint_tab_usage_single = "tab-usage-single"
    __endpoint_tab_usage_multiple = "tab-usage-multiple"

    @property
    def _base_endpoint(self):
        return self.__base_endpoint_url % (
            self.random_id,
            self.random_id,
            self.random_id
        )

    def setUp(self):
        super().setUp(TabUsage)
        self.random_endpoint = self.__endpoint_tab_usage_single if \
            random.randint(0, 1) else self.__endpoint_tab_usage_multiple

    def test_get_base_endpoint(self):
        endpoint_should_be = self._base_endpoint
        endpoint_should_be += "/%s" % self.random_endpoint

        endpoint_to_check = self.test_class._get_base_endpoint(
            self.random_id, self.random_id, self.random_id,
            self.random_endpoint)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_all_tab_usage_singles(self):
        endpoint_should_be = self._base_endpoint
        endpoint_should_be += "/%s" % self.__endpoint_tab_usage_single

        endpoint_to_check = self.test_class.get_all_tab_usage_singles(
            self.random_id, self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_cash_register_by_id(self):
        endpoint_should_be = self._base_endpoint
        endpoint_should_be += "/%s/%d" % (
            self.__endpoint_tab_usage_single,
            self.random_id
        )

        endpoint_to_check = self.test_class.get_tab_usage_single_by_id(
            self.random_id, self.random_id, self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_all_tab_usage_multiples(self):
        endpoint_should_be = self._base_endpoint
        endpoint_should_be += "/%s" % self.__endpoint_tab_usage_multiple

        endpoint_to_check = self.test_class.get_all_tab_usage_multiples(
            self.random_id, self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_tab_usage_multiple_by_id(self):
        endpoint_should_be = self._base_endpoint
        endpoint_should_be += "/%s/%d" % (
            self.__endpoint_tab_usage_multiple,
            self.random_id
        )

        endpoint_to_check = self.test_class.get_tab_usage_multiple_by_id(
            self.random_id, self.random_id, self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)
