import feedparser
from trender import TRender
# from pprint import pprint
from html.parser import HTMLParser


def news():
    url = 'https://www.bunq.com/en/news/feed.rss'
    feed = feedparser.parse(url)

    data = []
    for item in feed['items']:
        s = MLStripper()
        s.feed(item['summary'])
        obj = {
            'title': item['title'],
            'date': item['published'],
            'summary': s.get_data(),
            'link': item['link'],
            'author': item['author']
        }
        data.append(obj)
    with open('bunq_bot/responses/commands/news.md', 'r') as f:
        return TRender(f.read()).render({'data': data[:5]})


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)
