from apiwrapper.endpoints.annual_overview import AnnualOverview
from apiwrapper.tests.endpoints.test_endpoint import EndpointTest


class AnnualOverviewTest(EndpointTest):
    __base_endpoint_url = "/user/%d/export-annual-overview"

    @property
    def _base_endpoint(self):
        return self.__base_endpoint_url % self.random_id

    def setUp(self):
        super().setUp(AnnualOverview)

    def test_get_base_endpoint(self):
        endpoint_should_be = self._base_endpoint

        endpoint_to_check = self.test_class._get_base_endpoint(
            self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_all_annual_overviews_for_user(self):
        endpoint_should_be = self._base_endpoint

        endpoint_to_check = self.test_class.get_all_annual_overviews_for_user(
            self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_annual_overview_by_id(self):
        endpoint_should_be = self._base_endpoint
        endpoint_should_be += "/%d" % self.random_id

        endpoint_to_check = self.test_class.get_annual_overview_by_id(
            self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_content_of_annual_overview(self):
        endpoint_should_be = self._base_endpoint
        endpoint_should_be += "/%d/content" % self.random_id

        endpoint_to_check = self.test_class.get_content_of_annual_overview(
            self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)