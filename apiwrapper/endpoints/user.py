from apiwrapper.endpoints.endpoint import Endpoint


class User(Endpoint):

    __endpoint_user = "user"
    __endpoint_user_person = "user-person"
    __endpoint_user_company = "user-company"

    @classmethod
    def _get_base_endpoint(cls, user_id):
        return "/%s/%d" % (cls.__endpoint_user, user_id)

    def get_logged_in_user(self):
        return self._make_get_request("/" + self.__endpoint_user)

    def get_user_by_id(self, user_id):
        endpoint = self._get_base_endpoint(user_id)

        return self._make_get_request(endpoint)

    def get_user_person_by_id(self, user_id):
        endpoint = "/%s/%d" % (self.__endpoint_user_person, user_id)

        return self._make_get_request(endpoint)

    def get_user_company_by_id(self, user_id):
        endpoint = "/%s/%d" % (self.__endpoint_user_company, user_id)

        return self._make_get_request(endpoint)

