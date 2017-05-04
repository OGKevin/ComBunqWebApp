from Crypto.Cipher import AES
# from Crypto.PublicKey import RSA
from Crypto import Random
import json
# from pprint import pprint
import base64
import hashlib
# from django.contrib.auth.models import User


class AESCipher(object):
    """docstring for AESCipher.

    Copied this from a gist on GitHub need to research so i can link it.

    Passwords are encoded with sha256 before they are used to encrypt the
    contents. Encrypted contents are encoded in base64"""

    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def __repr__(self):
        # NOTE: this might not be configred right.
        return self.__name__

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw)).decode()

    def decrypt(self, enc):

        enc = base64.b64decode(enc)

        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)

        return json.loads(self._unpad(
            cipher.decrypt(enc[AES.block_size:])).decode('utf-8'))

    def _pad(self, s):
        return s + (
            self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
