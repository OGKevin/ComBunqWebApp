from apiwrapper.endpoints.user import User


class Card(User):

    endpoint_card = "card"

    @classmethod
    def get_base_endpoint(cls, user_id, card_id=None):
        endpoint = User.get_base_endpoint(user_id)
        endpoint += "/%s" % cls.endpoint_card
        if card_id is not None:
            endpoint += "/%d" % card_id
        return endpoint

    def get_all_cards_for_user(self, user_id):
        endpoint = self.get_base_endpoint(user_id)

        return self._make_get_request(endpoint)

    def get_card_for_user_by_id(self, user_id, card_id):
        endpoint = self.get_base_endpoint(user_id, card_id)

        return self._make_get_request(endpoint)
