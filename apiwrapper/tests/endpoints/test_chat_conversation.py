import unittest

from apiwrapper.endpoints.chat_conversation import ChatConversation
from apiwrapper.tests.endpoints.test_endpoint import EndpointTest


class ChatConversationTest(EndpointTest, unittest.TestCase):
    def setUp(self):
        super().setUp(ChatConversation)

    def test_get_base_endpoint(self):
        endpoint_should_be = "/user/%d/chat-conversation" % (
            self.random_id
        )
        endpoint_to_check = self.test_class.get_base_endpoint(
            self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_all_chat_conversations_for_user(self):
        endpoint_should_be = "/user/%d/chat-conversation" % (
            self.random_id
        )
        endpoint_to_check = self.test_class.get_all_chat_conversations_for_user(
            self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_chat_conversation_by_id(self):
        endpoint_should_be = "/user/%d/chat-conversation/%d" % (
            self.random_id,
            self.random_id
        )
        endpoint_to_check = self.test_class.get_chat_conversation_by_id(
            self.random_id, self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_all_messages_for_chat_conversation(self):
        endpoint_should_be = "/user/%d/chat-conversation/%d/message" % (
            self.random_id,
            self.random_id
        )
        endpoint_to_check = self.test_class.get_all_messages_for_chat_conversation(
            self.random_id, self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_attachment_by_id(self):
        endpoint_should_be = "/user/%d/chat-conversation/%d/attachment/%d" % (
            self.random_id,
            self.random_id,
            self.random_id
        )
        endpoint_to_check = self.test_class.get_attachment_by_id(
            self.random_id, self.random_id, self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_attachment_content(self):
        endpoint_should_be = "/user/%d/chat-conversation/%d/attachment/%d" \
                             "/content" % (
                                 self.random_id,
                                 self.random_id,
                                 self.random_id
                             )
        endpoint_to_check = self.test_class.get_attachment_content(
            self.random_id, self.random_id, self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)
