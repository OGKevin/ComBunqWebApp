from apiwrapper.endpoints.endpoint import Endpoint
from apiwrapper.endpoints.monetary_account import MonetaryAccount


class AttachmentTab(Endpoint):

    __endpoint_attachment_tab = "attachment-tab"
    __endpoint_attachment_tab_content = "content"

    @classmethod
    def _get_base_endpoint(cls, user_id, account_id, attachment_id):
        endpoint = MonetaryAccount._get_base_endpoint(user_id, account_id)
        endpoint += "/%s/%d" % (cls.__endpoint_attachment_tab, attachment_id)
        return endpoint

    def get_attachment_tab_by_id(self, user_id, account_id, attachment_id):
        endpoint = self._get_base_endpoint(user_id, account_id, attachment_id)

        return self._make_get_request(endpoint)

    def get_content(self, user_id, account_id, attachment_id):
        endpoint = self._get_base_endpoint(user_id, account_id, attachment_id)
        endpoint += "/%s" % self.__endpoint_attachment_tab_content

        return self._make_get_request(endpoint)
