from apiwrapper.endpoints.endpoint import Endpoint


class TabAttachment(Endpoint):

    __endpoint_tab = "tab"
    __endpoint_tab_attachment = "attachment"
    __endpoint_tab_attachment_content = "content"

    @classmethod
    def _get_base_endpoint(cls, tab_id, attachment_id):
        return "/%s/%s/%s/%d" % (
            cls.__endpoint_tab,
            tab_id,
            cls.__endpoint_tab_attachment,
            attachment_id
        )

    def get_tab_attachment_by_id(self, tab_id, attachment_id):
        endpoint = self._get_base_endpoint(tab_id, attachment_id)

        return self._make_get_request(endpoint)

    def get_content_of_tab_attachment(self, tab_id, attachment_id):
        endpoint = self._get_base_endpoint(tab_id, attachment_id)
        endpoint += "/%s" % self.__endpoint_tab_attachment_content

        return self._make_get_request(endpoint)
