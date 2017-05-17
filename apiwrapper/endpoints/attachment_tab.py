from apiwrapper.endpoints.monetary_account import MonetaryAccount


class AttachmentTab(MonetaryAccount):

    endpoint_attachment_tab = "attachment-tab"
    endpoint_attachment_tab_content = "content"

    @classmethod
    def get_base_endpoint(cls, user_id, account_id, attachment_id):
        endpoint = MonetaryAccount.get_base_endpoint(user_id, account_id)
        endpoint += "/%s/%d" % (cls.endpoint_attachment_tab, attachment_id)
        return endpoint

    def get_attachment_tab_by_id(self, user_id, account_id, attachment_id):
        endpoint = self.get_base_endpoint(user_id, account_id, attachment_id)

        return self._make_get_request(endpoint)

    def get_attachment_content(self, user_id, account_id, attachment_id):
        endpoint = self.get_base_endpoint(user_id, account_id, attachment_id)
        endpoint += "/%s" % self.endpoint_attachment_tab_content

        return self._make_get_request(endpoint)
