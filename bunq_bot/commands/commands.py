from bunq_bot.commands.controller import Controller
from bunq_bot.models import ChatInfo
from django.core.exceptions import ObjectDoesNotExist
# import sqlite3
# from config import config


# config = config()
# from pprint import pprint


class Commands(Controller):

    def __init__(self, msg):
        super().__init__()
        self._msg = msg
        # self.db = sqlite3.connect(config.database.path)

    def start(self):
        if not self._check_chat_id():
            id = self._msg.message.chat.id
            c = ChatInfo(chat_id=id)
            c.save()
            return self._start()
        else:
            error = ('Im already working in this chat')
            return error

    def news(self):
        return self._news()

    def help(self):
        return self._help()

    def stop(self):
        self._remove_chat_id()
        return self._stop()

    def _remove_chat_id(self):
        id = self._msg.message.chat.id
        try:
            c = ChatInfo.objects.get(chat_id=id)
            c.delete()
        except ObjectDoesNotExist:
            pass

    def _check_chat_id(self):
        ids = list(ChatInfo.objects.all().values_list('chat_id', flat=True))
        id = str(self._msg.message.chat.id)

        if id in ids:
            return True
        else:
            return False
