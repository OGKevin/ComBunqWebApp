from apiwrapper.endpoints.customer_statement import CustomerStatement
from apiwrapper.tests.endpoints.test_endpoint import EndpointTest


class CustomerStatementTest(EndpointTest):
    __base_endpoint_url = "/user/%d/monetary-account/%d/customer-statement"

    @property
    def _base_endpoint(self):
        return self.__base_endpoint_url % (self.random_id, self.random_id)

    def setUp(self):
        super().setUp(CustomerStatement)

    def test_get_base_endpoint(self):
        endpoint_should_be = self._base_endpoint

        endpoint_to_check = self.test_class._get_base_endpoint(
            self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_all_customer_statements_for_account(self):
        endpoint_should_be = self._base_endpoint

        endpoint_to_check = self.test_class.get_all_customer_statements_for_account(
            self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_customer_statement_by_id(self):
        endpoint_should_be = self._base_endpoint
        endpoint_should_be += "/%d" % self.random_id

        endpoint_to_check = self.test_class.get_customer_statement_by_id(
            self.random_id, self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_content_of_customer_statement(self):
        endpoint_should_be = self._base_endpoint
        endpoint_should_be += "/%d/content" % self.random_id

        endpoint_to_check = self.test_class.get_content_of_customer_statement(
            self.random_id, self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)
