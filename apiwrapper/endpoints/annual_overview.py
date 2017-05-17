from apiwrapper.endpoints.user import User


class AnnualOverview(User):

    endpoint_annual_overview = "export-annual-overview"
    endpoint_annual_overview_content = "content"

    @classmethod
    def get_base_endpoint(cls, user_id, overview_id=None):
        endpoint = User.get_base_endpoint(user_id)
        endpoint += "/%s" % cls.endpoint_annual_overview
        if overview_id is not None:
            endpoint += "/%d" % overview_id
        return endpoint

    def get_all_annual_overviews_for_user(self, user_id):
        endpoint = self.get_base_endpoint(user_id)

        return self._make_get_request(endpoint)

    def get_annual_overview_by_id(self, user_id, overview_id):
        endpoint = self.get_base_endpoint(user_id, overview_id)

        return self._make_get_request(endpoint)

    def get_content_of_annual_overview(self, user_id, overview_id):
        endpoint = self.get_base_endpoint(user_id, overview_id)
        endpoint += "/%s" % self.endpoint_annual_overview_content

        return self._make_get_request(endpoint)
