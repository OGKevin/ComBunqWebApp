from Crypto.Cipher import AES
# from Crypto.PublicKey import RSA
from Crypto import Random
import json
# from pprint import pprint
import base64
import hashlib
# from django.contrib.auth.models import User


class AESCipher(object):

    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw)).decode()

    def decrypt(self, enc):
        try:
            enc = base64.b64decode(enc)
        except base64.binascii.Error:
            return(
                json.dumps(
                    {'error': 'something went wrong, maybe u touched the secret?'}))  # noqa
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        try:
            return self._unpad(
                cipher.decrypt(enc[AES.block_size:])).decode('utf-8')
        except UnicodeDecodeError:
            return(
                json.dumps(
                    {'error': 'something went wrong, maybe wrong password?'}))

    def _pad(self, s):
        return s + (
            self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
