from django.core import signing
from filecreator.creator import Creator
import arrow
from BunqAPI.callbacks import callback
import datetime


class Installation:
    def __init__(self, user, api_key, password, delete_user=True):
        self.user = user
        self.api_key = api_key
        self.password = password
        self._delete_user = delete_user

    def register_api_key(self):
        c = callback(api_key=self.api_key, user=self.user, decrypt=False)
        installation = c.installation()

        if installation['status']:
            enc_string = signing.dumps(obj=installation['data'],
                                       key=self.password)
            now = datetime.datetime.now()
            json = {
                'secret': enc_string,
                'username': self.user.username,
                'created': arrow.get(now).format(fmt='DD-MM-YYYY HH:mm:ss')
            }
            Creator(user=self.user).user_json(data=json)
            return True
        else:
            if self._delete_user:
                self.user.delete()
            return False

    @property
    def status(self):
        if self.register_api_key():
            return True
        else:
            return False
