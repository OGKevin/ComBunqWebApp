from django.core.management.base import BaseCommand, CommandError
from bunq_bot.main import MessagesHandler
import time


class Command (BaseCommand):

    help = ('Bot will run and check for updates, these updates will be send '
            'automaticly to the users. This command should run in the '
            'background. It will check for update every 5 min')

    _attribute_error = ('Something went wrong, is the TELEGRAM_TOKEN set in '
                        'settings?')

    def handle(self,  *args, **options):
        while True:
            try:
                MessagesHandler().send_updates()
            except AttributeError:
                raise CommandError(self._attribute_error)
            time.sleep(300)
