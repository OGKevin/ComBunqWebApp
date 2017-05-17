from apiwrapper.endpoints.endpoint import Endpoint


class Tab(Endpoint):

    endpoint_tab = "tab"
    endpoint_tab_attachment = "attachment"
    endpoint_tab_attachment_content = "content"

    @classmethod
    def get_base_endpoint(cls, tab_id, attachment_id):
        return "/%s/%s/%s/%d" % (
            cls.endpoint_tab,
            tab_id,
            cls.endpoint_tab_attachment,
            attachment_id
        )

    def get_tab_attachment_by_id(self, tab_id, attachment_id):
        endpoint = self.get_base_endpoint(tab_id, attachment_id)

        return self._make_get_request(endpoint)

    def get_content_of_tab_attachment(self, tab_id, attachment_id):
        endpoint = self.get_base_endpoint(tab_id, attachment_id)
        endpoint += "/%s" % self.endpoint_tab_attachment_content

        return self._make_get_request(endpoint)
