from apiwrapper.endpoints.monetary_account import MonetaryAccount


class MasterCardAction(MonetaryAccount):

    endpoint_mastercard_action = "mastercard-action"

    @classmethod
    def get_base_endpoint(cls, user_id, account_id, action_id=None):
        endpoint = MonetaryAccount.get_base_endpoint(user_id, account_id)
        endpoint += "/%s" % cls.endpoint_mastercard_action
        if account_id is not None:
            endpoint += "/%d" % action_id
        return endpoint

    def get_all_master_card_actions_for_account(self, user_id, account_id):
        endpoint = self.get_base_endpoint(user_id, account_id)

        return self._make_get_request(endpoint)

    def get_master_card_action_by_id(self, user_id, account_id, action_id):
        endpoint = self.get_base_endpoint(user_id, account_id, action_id)

        return self._make_get_request(endpoint)
