import unittest

from apiwrapper.endpoints.annual_overview import AnnualOverview
from apiwrapper.tests.endpoints.test_endpoint import EndpointTest


class AnnualOverviewTest(EndpointTest, unittest.TestCase):

    def setUp(self):
        super().setUp(AnnualOverview)

    def test_get_base_endpoint(self):
        endpoint_should_be = "/user/%d/export-annual-overview" % (
            self.random_id
        )
        endpoint_to_check = self.test_class.get_base_endpoint(
            self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_all_annual_overviews_for_user(self):
        endpoint_should_be = "/user/%d/export-annual-overview" % (
            self.random_id
        )
        endpoint_to_check = self.test_class.get_all_annual_overviews_for_user(
            self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_annual_overview_by_id(self):
        endpoint_should_be = "/user/%d/export-annual-overview/%d" % (
            self.random_id,
            self.random_id
        )
        endpoint_to_check = self.test_class.get_annual_overview_by_id(
            self.random_id, self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_content_of_annual_overview(self):
        endpoint_should_be = "/user/%d/export-annual-overview/%d/content" % (
            self.random_id,
            self.random_id
        )
        endpoint_to_check = self.test_class.get_content_of_annual_overview(
            self.random_id, self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)