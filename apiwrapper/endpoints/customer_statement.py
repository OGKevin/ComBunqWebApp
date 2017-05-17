from apiwrapper.endpoints.monetary_account import MonetaryAccount


class CustomerStatement(MonetaryAccount):

    endpoint_customer_statement = "customer-statement"
    endpoint_customer_statement_content = "content"

    @classmethod
    def get_base_endpoint(cls, user_id, account_id, statement_id=None):
        endpoint = MonetaryAccount.get_base_endpoint(user_id, account_id)
        endpoint += "/%s" % cls.endpoint_customer_statement
        if statement_id is not None:
            endpoint += "/%d" % statement_id
        return endpoint

    def get_all_customer_statements_for_account(self, user_id, account_id):
        endpoint = self.get_base_endpoint(user_id, account_id)

        return self._make_get_request(endpoint)

    def get_customer_statement_by_id(self, user_id, account_id, statement_id):
        endpoint = self.get_base_endpoint(user_id, account_id, statement_id)

        return self._make_get_request(endpoint)

    def get_content_of_customer_statement(self, user_id, account_id,
                                          statement_id):
        endpoint = self.get_base_endpoint(user_id, account_id, statement_id)
        endpoint += "/%s" % self.endpoint_customer_statement_content

        return self._make_get_request(endpoint)
