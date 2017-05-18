from apiwrapper.endpoints.payment import Payment
from apiwrapper.tests.endpoints.test_endpoint import EndpointTest


class PaymentTest(EndpointTest):
    __base_endpoint_url = "/user/%d/monetary-account/%d"

    @property
    def _base_endpoint(self):
        return self.__base_endpoint_url % (self.random_id, self.random_id)

    def setUp(self):
        super().setUp(Payment)

    def test_get_base_endpoint(self):
        endpoint_should_be = self._base_endpoint

        endpoint_to_check = self.test_class._get_base_endpoint(
            self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_all_payments_for_account(self):
        endpoint_should_be = self._base_endpoint
        endpoint_should_be += "/payment"

        endpoint_to_check = self.test_class.get_all_payments_for_account(
            self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_payment_by_id(self):
        endpoint_should_be = self._base_endpoint
        endpoint_should_be += "/payment/%d" % self.random_id

        endpoint_to_check = self.test_class.get_payment_by_id(
            self.random_id, self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_chat_for_payment(self):
        endpoint_should_be = self._base_endpoint
        endpoint_should_be += "/payment/%d/chat" % self.random_id

        endpoint_to_check = self.test_class.get_chat_for_payment(
            self.random_id, self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_all_payments_batches_for_account(self):
        endpoint_should_be = self._base_endpoint
        endpoint_should_be += "/payment-batch"

        endpoint_to_check = self.test_class.get_all_payments_batches_for_account(
            self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_payment_batch_by_id(self):
        endpoint_should_be = self._base_endpoint
        endpoint_should_be += "/payment-batch/%d" % self.random_id

        endpoint_to_check = self.test_class.get_payment_batch_by_id(
            self.random_id, self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)


