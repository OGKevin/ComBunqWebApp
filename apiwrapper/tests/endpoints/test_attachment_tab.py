from apiwrapper.endpoints.attachment_tab import AttachmentTab
from apiwrapper.tests.endpoints.test_endpoint import EndpointTest


class AttachmentTabTest(EndpointTest):
    __base_endpoint_url = "/user/%d/monetary-account/%d/attachment-tab/%d"

    @property
    def _base_endpoint(self):
        return self.__base_endpoint_url % (
            self.random_id,
            self.random_id,
            self.random_id
        )

    def setUp(self):
        super().setUp(AttachmentTab)

    def test_get_base_endpoint(self):
        endpoint_should_be = self._base_endpoint

        endpoint_to_check = self.test_class._get_base_endpoint(
            self.random_id, self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_attachment_tab_by_id(self):
        endpoint_should_be = self._base_endpoint

        endpoint_to_check = self.test_class.get_attachment_tab_by_id(
            self.random_id, self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_attachment_content(self):
        endpoint_should_be = self._base_endpoint
        endpoint_should_be += "/content"

        endpoint_to_check = self.test_class.get_content(
            self.random_id, self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)
