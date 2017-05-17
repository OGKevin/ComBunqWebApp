from apiwrapper.endpoints.endpoint import Endpoint


class AttachmentPublic(Endpoint):

    endpoint_attachment_public = "attachment-public"
    endpoint_attachment_public_content = "content"

    @classmethod
    def get_base_endpoint(cls, attachment_id):
        return "/%s/%s" % (cls.endpoint_attachment_public, attachment_id)

    def get_public_attachment_by_id(self, attachment_id):
        endpoint = self.get_base_endpoint(attachment_id)

        return self._make_get_request(endpoint)

    def get_content_of_public_attachment(self, attachment_id):
        endpoint = self.get_base_endpoint(attachment_id)
        endpoint += "/%s" % self.endpoint_attachment_public_content

        return self._make_get_request(endpoint)
