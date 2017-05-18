from apiwrapper.endpoints.request_inquiry import RequestInquiry
from apiwrapper.tests.endpoints.test_endpoint import EndpointTest


class RequestInquiryTest(EndpointTest):
    __base_endpoint_url = "/user/%d/monetary-account/%d"

    @property
    def _base_endpoint(self):
        return self.__base_endpoint_url % (self.random_id, self.random_id)

    def setUp(self):
        super().setUp(RequestInquiry)

    def test_get_base_endpoint(self):
        endpoint_should_be = self._base_endpoint

        endpoint_to_check = self.test_class._get_base_endpoint(
            self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_all_inquiries_for_account(self):
        endpoint_should_be = self._base_endpoint
        endpoint_should_be += "/request-inquiry"

        endpoint_to_check = self.test_class.get_all_inquiries_for_account(
            self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_request_inquiry_by_id(self):
        endpoint_should_be = self._base_endpoint
        endpoint_should_be += "/request-inquiry/%d" % self.random_id

        endpoint_to_check = self.test_class.get_request_inquiry_by_id(
            self.random_id, self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_chat_for_request_inquiry(self):
        endpoint_should_be = self._base_endpoint
        endpoint_should_be += "/request-inquiry/%d/chat" % self.random_id

        endpoint_to_check = self.test_class.get_chat_for_request_inquiry(
            self.random_id, self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_all_batch_inquiries_for_account(self):
        endpoint_should_be = self._base_endpoint
        endpoint_should_be += "/request-inquiry-batch"

        endpoint_to_check = self.test_class.get_all_batch_inquiries_for_account(
            self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_batch_inquiry_by_id(self):
        endpoint_should_be = self._base_endpoint
        endpoint_should_be += "/request-inquiry-batch/%d" % self.random_id

        endpoint_to_check = self.test_class.get_batch_inquiry_by_id(
            self.random_id, self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_all_request_responses_for_account(self):
        endpoint_should_be = self._base_endpoint
        endpoint_should_be += "/request-response"

        endpoint_to_check = self.test_class.get_all_request_responses_for_account(
            self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_request_response_by_id(self):
        endpoint_should_be = self._base_endpoint
        endpoint_should_be += "/request-response/%d" % self.random_id

        endpoint_to_check = self.test_class.get_request_response_by_id(
            self.random_id, self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_chat_for_request_response(self):
        endpoint_should_be = self._base_endpoint
        endpoint_should_be += "/request-response/%d/chat" % self.random_id

        endpoint_to_check = self.test_class.get_chat_for_request_response(
            self.random_id, self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)
