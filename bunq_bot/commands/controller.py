from bunq_bot.commands.commandos.start import start
from bunq_bot.commands.commandos.news import news
from bunq_bot.commands.commandos.stop import stop
from bunq_bot.commands.commandos.help import help


class Controller():

    def __init__(self):
        self._start = start
        self._news = news
        self._stop = stop
        self._help = help
