import telegram
from bunq_bot.automatic_messages.updates import Updates
from bunq_bot.commands.commands import Commands
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings


class MessagesHandler(Commands, Updates):

    _bot = telegram.Bot(token=settings.TELEGRAM_TOKEN)

    def __init__(self, msg=None):
        Commands.__init__(self, msg)
        Updates.__init__(self, self._bot)
        self._msg = msg

    def reply(self):
        if self._is_command():
            command = self._msg.message.text[0]
            if hasattr(self, command):
                text = getattr(self, self._msg.message.text[0])()
            else:
                text = 'This command does not exist.'
            self._bot.sendMessage(chat_id=self._msg.message.chat.id,
                                  text=text,
                                  parse_mode=telegram.ParseMode.MARKDOWN)

    def _is_command(self):
        if 'entities' in self._msg.message.keys():
            if self._msg.message.entities[0].type == 'bot_command':
                self._msg.message.text = self._msg.message.text.lstrip('/')
                self._msg.message.text = self._msg.message.text.split()
                return True
            else:
                return False
        else:
            return False

    def _check_for_updates(self):
        pass


scheduler = BackgroundScheduler()
scheduler.add_job(MessagesHandler().send_updates, 'interval', seconds=300)
scheduler.start()
