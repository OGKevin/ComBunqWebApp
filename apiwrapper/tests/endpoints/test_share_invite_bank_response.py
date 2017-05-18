from apiwrapper.endpoints.share_invite_bank_response import \
    ShareInviteBankResponse
from apiwrapper.tests.endpoints.test_endpoint import EndpointTest


class ShareInviteBankResponseTest(EndpointTest):
    __base_endpoint_url = "/user/%d/share-invite-bank-response"

    @property
    def _base_endpoint(self):
        return self.__base_endpoint_url % self.random_id

    def setUp(self):
        super().setUp(ShareInviteBankResponse)

    def test_get_base_endpoint(self):
        endpoint_should_be = self._base_endpoint

        endpoint_to_check = self.test_class._get_base_endpoint(
            self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_all_invite_responses(self):
        endpoint_should_be = self._base_endpoint

        endpoint_to_check = self.test_class.get_all_invite_responses(
            self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_invite_response_by_id(self):
        endpoint_should_be = self._base_endpoint
        endpoint_should_be += "/%d" % self.random_id

        endpoint_to_check = self.test_class.get_invite_response_by_id(
            self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)
