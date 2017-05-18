from apiwrapper.endpoints.endpoint import Endpoint

from apiwrapper.endpoints.monetary_account import MonetaryAccount


class RequestInquiry(Endpoint):
    __endpoint_request_inquiry = "request-inquiry"
    __endpoint_request_inquiry_batch = "request-inquiry-batch"
    __endpoint_request_response = "request-response"
    __endpoint_request_chat = "chat"

    @classmethod
    def _get_base_endpoint(cls, user_id, account_id):
        endpoint = MonetaryAccount._get_base_endpoint(user_id)
        endpoint += "/%d" % account_id
        return endpoint

    # Request Inquiry Logic
    def get_all_inquiries_for_account(self, user_id, account_id):
        endpoint = self._get_base_endpoint(user_id, account_id)
        endpoint += "/%s" % self.__endpoint_request_inquiry

        return self._make_get_request(endpoint)

    def get_request_inquiry_by_id(self, user_id, account_id, request_id):
        endpoint = self._get_base_endpoint(user_id, account_id)
        endpoint += "/%s/%d" % (self.__endpoint_request_inquiry, request_id)

        return self._make_get_request(endpoint)

    def get_chat_for_request_inquiry(self, user_id, account_id, request_id):
        endpoint = self._get_base_endpoint(user_id, account_id)
        endpoint += "/%s/%d/%s" % (
            self.__endpoint_request_inquiry,
            request_id,
            self.__endpoint_request_chat
        )

        return self._make_get_request(endpoint)

    # Request Inquiry Batch Logic
    def get_all_batch_inquiries_for_account(self, user_id, account_id):
        endpoint = self._get_base_endpoint(user_id, account_id)
        endpoint += "/%s" % self.__endpoint_request_inquiry_batch

        return self._make_get_request(endpoint)

    def get_batch_inquiry_by_id(self, user_id, account_id, inquiry_id):
        endpoint = self._get_base_endpoint(user_id, account_id)
        endpoint += "/%s/%d" % (
            self.__endpoint_request_inquiry_batch, inquiry_id)

        return self._make_get_request(endpoint)

    # Request Response Logic
    def get_all_request_responses_for_account(self, user_id, account_id):
        endpoint = self._get_base_endpoint(user_id, account_id)
        endpoint += "/%s" % self.__endpoint_request_response

        return self._make_get_request(endpoint)

    def get_request_response_by_id(self, user_id, account_id, response_id):
        endpoint = self._get_base_endpoint(user_id, account_id)
        endpoint += "/%s/%d" % (self.__endpoint_request_response, response_id)

        return self._make_get_request(endpoint)

    def get_chat_for_request_response(self, user_id, account_id, request_id):
        endpoint = self._get_base_endpoint(user_id, account_id)
        endpoint += "/%s/%d/%s" % (
            self.__endpoint_request_response,
            request_id,
            self.__endpoint_request_chat
        )

        return self._make_get_request(endpoint)
