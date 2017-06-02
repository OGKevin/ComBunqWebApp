from apiwrapper.endpoints.endpoint import Endpoint
from apiwrapper.endpoints.monetary_account import MonetaryAccount


class CustomerStatement(Endpoint):

    __endpoint_customer_statement = "customer-statement"
    __endpoint_customer_statement_content = "content"

    @classmethod
    def _get_base_endpoint(cls, user_id, account_id, statement_id=None):
        endpoint = MonetaryAccount._get_base_endpoint(user_id, account_id)
        endpoint += "/%s" % cls.__endpoint_customer_statement
        if statement_id is not None:
            endpoint += "/%d" % statement_id
        return endpoint

    def get_all_customer_statements_for_account(self, user_id, account_id):
        endpoint = self._get_base_endpoint(user_id, account_id)

        return self._make_get_request(endpoint)

    def get_customer_statement_by_id(self, user_id, account_id, statement_id):
        endpoint = self._get_base_endpoint(user_id, account_id, statement_id)

        return self._make_get_request(endpoint)

    def get_content_of_customer_statement(self, user_id, account_id,
                                          statement_id):
        endpoint = self._get_base_endpoint(user_id, account_id, statement_id)
        endpoint += "/%s" % self.__endpoint_customer_statement_content

        return self._make_get_request(endpoint, verify=False)

    def create_customer_statement_pdf(self, user_id, account_id, date_start,
                                      date_end):
        endpoint = self._get_base_endpoint(user_id, account_id)
        payload = {
            'statement_format': 'PDF',
            'date_start': date_start,
            'date_end': date_end,
        }

        return self._make_post_request(endpoint, payload)

    def create_customer_statement_csv(self, user_id, account_id, date_start,
                                      date_end, regional_format='EUROPEAN'):
        endpoint = self._get_base_endpoint(user_id, account_id)
        payload = {
            'statement_format': 'CSV',
            'date_start': date_start,
            'date_end': date_end,
            'regional_format': regional_format
        }

        return self._make_post_request(endpoint, payload)

    def create_customer_statement_mt940(self, user_id, account_id, date_start,
                                        date_end):
        endpoint = self._get_base_endpoint(user_id, account_id)
        payload = {
            'statement_format': 'MT940',
            'date_start': date_start,
            'date_end': date_end,
        }

        return self._make_post_request(endpoint, payload)
