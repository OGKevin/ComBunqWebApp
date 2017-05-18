from apiwrapper.endpoints.draft_share_invite_bank import DraftShareInviteBank
from apiwrapper.tests.endpoints.test_endpoint import EndpointTest


class DraftShareInviteBankTest(EndpointTest):
    __base_endpoint_url = "/user/%d/draft-share-invite-bank"

    @property
    def _base_endpoint(self):
        return self.__base_endpoint_url % self.random_id

    def setUp(self):
        super().setUp(DraftShareInviteBank)

    def test_get_base_endpoint(self):
        endpoint_should_be = self._base_endpoint

        endpoint_to_check = self.test_class._get_base_endpoint(
            self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_all_invite_drafts(self):
        endpoint_should_be = self._base_endpoint

        endpoint_to_check = self.test_class.get_all_invite_drafts(
            self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_invite_draft_by_id(self):
        endpoint_should_be = self._base_endpoint
        endpoint_should_be += "/%d" % self.random_id

        endpoint_to_check = self.test_class.get_invite_draft_by_id(
            self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_qr_code_content_for_invite_draft(self):
        endpoint_should_be = self._base_endpoint
        endpoint_should_be += "/%d/qr-code-content" % self.random_id

        endpoint_to_check = self.test_class.get_qr_code_content_for_invite_draft(
            self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)
