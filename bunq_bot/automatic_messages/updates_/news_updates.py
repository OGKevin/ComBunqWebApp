import feedparser
import telegram
from trender import TRender
from html.parser import HTMLParser
from bunq_bot.models import BunqNews, ChatInfo


class NewsUpdates():

    _url = 'https://www.bunq.com/en/news/feed.rss'
    _feed = feedparser.parse(_url)

    def __init__(self, bot):
        self._bot = bot

    def send_updates(self):
        titles = list(BunqNews.objects.all().values_list('title',
                                                         flat=True))
        for item in self._feed['items']:
            if not item['title'] in titles:
                self._send_upadte(item)
                self._save_in_database(item)

    def _save_in_database(self, item):
        c = BunqNews(title=item['title'], author=item['author'])
        c.save()

    def _send_upadte(self, item):
        chat_ids = list(ChatInfo.objects.all().values_list('chat_id',
                                                           flat=True))

        for chat_id in chat_ids:
            self._bot.send_message(
                chat_id=chat_id,
                text=self._text(item),
                parse_mode=telegram.ParseMode.MARKDOWN
            )

    def _text(self, item):
        s = MLStripper()
        s.feed(item['summary'])
        item['summary'] = s.get_data()

        with open('bunq_bot/responses/automatic_messages/news_feed.md',
                  'r') as f:
            return TRender(f.read()).render({'item': item})


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)
