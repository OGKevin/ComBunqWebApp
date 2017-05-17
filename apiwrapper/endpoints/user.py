from apiwrapper.endpoints.endpoint import Endpoint


class User(Endpoint):

    endpoint_user = "user"
    endpoint_user_person = "user-person"
    endpoint_user_company = "user-company"

    @classmethod
    def get_base_endpoint(cls, user_id):
        return "/%s/%d" % (cls.endpoint_user, user_id)

    def get_all_users(self):
        return self._make_get_request("/" + self.endpoint_user)

    def get_user_by_id(self, user_id):
        endpoint = self.get_base_endpoint(user_id)

        return self._make_get_request(endpoint)

    def get_user_person_by_id(self, user_id):
        endpoint = "/%s/%d" % (self.endpoint_user_person, user_id)

        return self._make_get_request(endpoint)

    def get_user_company_by_id(self, user_id):
        endpoint = "/%s/%d" % (self.endpoint_user_company, user_id)

        return self._make_get_request(endpoint)
