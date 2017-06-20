from bunq_bot.automatic_messages.updates_.news_updates import NewsUpdates
from bunq_bot.automatic_messages.updates_.together_updates import \
                                                        TogetherUpdates


class Updates():
    def __init__(self, bot):
        self.bot = bot

    def send_updates(self):
        NewsUpdates(self._bot).send_updates()
        TogetherUpdates(self._bot).send_updates()
        # self.send_updates()
