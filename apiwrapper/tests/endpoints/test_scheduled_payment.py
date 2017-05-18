from apiwrapper.endpoints.scheduled_payment import ScheduledPayment
from apiwrapper.tests.endpoints.test_endpoint import EndpointTest


class ScheduledPaymentTest(EndpointTest):
    __base_endpoint_url = "/user/%d/monetary-account/%d/schedule-payment"

    @property
    def _base_endpoint(self):
        return self.__base_endpoint_url % (self.random_id, self.random_id)

    def setUp(self):
        super().setUp(ScheduledPayment)

    def test_get_base_endpoint(self):
        endpoint_should_be = self._base_endpoint

        endpoint_to_check = self.test_class._get_base_endpoint(
            self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_all_scheduled_payments_for_account(self):
        endpoint_should_be = self._base_endpoint

        endpoint_to_check = self.test_class.get_all_scheduled_payments_for_account(
            self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_scheduled_payment_by_id(self):
        endpoint_should_be = self._base_endpoint
        endpoint_should_be += "/%d" % self.random_id

        endpoint_to_check = self.test_class.get_scheduled_payment_by_id(
            self.random_id, self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)
