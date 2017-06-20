import feedparser
import telegram
from trender import TRender
from html.parser import HTMLParser
from bunq_bot.models import BunqTogether, ChatInfo


class TogetherUpdates():

    _url = 'https://together.bunq.com/rss'
    _feed = feedparser.parse(_url)

    def __init__(self, bot):
        self._bot = bot

    def send_updates(self):
        titles = list(BunqTogether.objects.all().values_list('title',
                                                             flat=True))
        for item in self._feed['items']:
            if not item['title'] in titles:
                try:
                    self._send_upadte(item)
                except telegram.error.BadRequest:
                    self._send_upadte(item, False)
                self._save_in_database(item['title'])

    def _save_in_database(self, title):
        c = BunqTogether(title=title)
        c.save()

    def _send_upadte(self, item, summary=True):
        chat_ids = list(ChatInfo.objects.all().values_list('chat_id',
                                                           flat=True))

        for chat_id in chat_ids:
            self._bot.send_message(
                chat_id=chat_id,
                text=self._text(item, summary),
                parse_mode=telegram.ParseMode.MARKDOWN
            )

    def _text(self, item, summary=True):
        s = MLStripper()
        s.feed(item['summary'])
        item['summary'] = s.get_data()

        with open('bunq_bot/responses/automatic_messages/together_feed.md',
                  'r') as f:
            return TRender(f.read()).render({'item': item,
                                             'summary': summary})


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)
