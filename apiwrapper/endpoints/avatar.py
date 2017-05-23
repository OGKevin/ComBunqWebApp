from apiwrapper.endpoints.endpoint import Endpoint


class Avatar(Endpoint):

    __endpoint_avatar = "avatar"

    @classmethod
    def _get_base_endpoint(cls, avatar_id):
        return "/%s/%s" % (cls.__endpoint_avatar, avatar_id)

    def get_avatar_by_id(self, avatar_id):
        endpoint = self._get_base_endpoint(avatar_id)

        return self._make_get_request(endpoint, verify=False)
