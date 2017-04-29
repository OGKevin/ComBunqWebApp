from Crypto.Cipher import AES
# from Crypto.PublicKey import RSA
from Crypto import Random
# import json
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
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(
            cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (
            self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
# def decrypt(enc, key):
#     decoded = base64.decodestring(enc.encode())
#     # pprint(decoded)
#     IV = 16 * '\x00'
#     cipher = AES.new(key, AES.MODE_CBC, IV)
#     message = cipher.decrypt(decoded)
#     decodedMsg = message.decode()
#     # print (decodedMsg)
#     # print (type(decodedMsg))
#     print ('decrypted')
#     pprint(json.loads(str(decodedMsg) / 16))
#     # pprint(decodedMsg)
#     # print (type(json.loads(decodedMsg)))
#
#
# def encrypt(data, userID):
#     user = User.objects.get(username=userID)
#     print (user)
#     if user.profile.private_key == '':
#         random_generator = Random.new().read
#         key = RSA.generate(8192, random_generator)
#         user.profile.private_key = key.exportKey('PEM').decode()
#         user.save()
#     else:
#         key = RSA.importKey(user.profile.private_key)
#     IV = 16 * '\x00'
#     k = '0123456789abcdef'
#     cipher = AES.new(k, AES.MODE_CBC, IV)
#     # pprint(key.exportKey('PEM').decode())  # NOTE: need to save this
#     # private_key = key.exportKey('PEM').decode()
#     toBeEncypted = str(data * 16).encode('utf8')
#     # pprint(toBeEncypted)
#     ciphertext = cipher.encrypt(toBeEncypted)
#     encb64 = base64.encodestring(ciphertext)
#     print ('encrypted')
#     pprint(encb64.decode())
#     decrypt(encb64.decode(), k)  # NOTE: need to store it decoded
#     return encb64.decode()
#     # pprint(json.dumps({'test': encb64.decode()}))
#
#
# # encrypt(json.dumps({'test': 'test', 'tes2': 'fisd'}))
