from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto import Random
import json
from pprint import pprint
import base64
from django.contrib.auth.models import User


def decrypt(enc, key):
    decoded = base64.decodestring(enc.encode())
    # pprint(decoded)
    cipher = PKCS1_OAEP.new(key)
    message = cipher.decrypt(decoded)
    decodedMsg = message.decode()
    # print (decodedMsg)
    # print (type(decodedMsg))
    print ('decrypted')
    pprint(json.loads(decodedMsg))
    # print (type(json.loads(decodedMsg)))


def encrypt(data, userID):
    random_generator = Random.new().read
    key = RSA.generate(2048, random_generator)
    cipher = PKCS1_OAEP.new(key)
    # pprint(key.exportKey('PEM').decode())  # NOTE: need to save this
    private_key = key.exportKey('PEM').decode()
    user = User.objects.get(username=userID)
    user.profile.private_key = private_key
    user.save()
    toBeEncypted = str(data).encode('utf8')
    # pprint(toBeEncypted)
    ciphertext = cipher.encrypt(toBeEncypted)
    encb64 = base64.encodestring(ciphertext)
    print ('encrypted')
    # pprint(encb64.decode())
    # decrypt(encb64.decode(), key)  # NOTE: need to store it decoded
    return encb64.decode()
    # pprint(json.dumps({'test': encb64.decode()}))


# encrypt(json.dumps({'test': 'test', 'tes2': 'fisd'}))
