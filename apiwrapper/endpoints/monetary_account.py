from apiwrapper.endpoints.user import User


class MonetaryAccount(User):

    endpoint_monetary_account = "monetary-account"
    endpoint_monetary_account_bank = "monetary-account-bank"

    @classmethod
    def get_base_endpoint(cls, user_id, account_id=None):
        endpoint = User.get_base_endpoint(user_id)
        endpoint += "/%s" % cls.endpoint_monetary_account
        if account_id is not None:
            endpoint += "/%d" % account_id
        return endpoint

    def get_all_accounts_for_user(self, user_id):
        endpoint = self.get_base_endpoint(user_id)

        return self._make_get_request(endpoint)

    def get_account_by_id(self, user_id, account_id):
        endpoint = self.get_base_endpoint(user_id, account_id)

        return self._make_get_request(endpoint)
