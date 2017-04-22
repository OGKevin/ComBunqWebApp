#!/usr/bin/env python

# This code demonstrates how to register a new public key.
#
# Don't forget to store the returned Installation Token.
# The server public rsa key can always be retrieved as long
# as you have your private key and the token.
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
# from pprint import pprint
from tempfile import NamedTemporaryFile
from .pythonbunq.bunq import API
# import os
import json

# os.chdir(os.path.dirname(os.path.abspath(__file__)))

# NOTE: generating private key and installation token


# private part of RSA key pair

def getToken(privateKey):
    with open(privateKey, 'rb') as f:
            rsa_key = f.read()
    bunq_api = API(rsa_key, None)

    # using the pubkey() helper function to get public part of key pair
    public_key = bunq_api.pubkey().decode()

    # you will most probably want to store the token that is returned
    r = bunq_api.query('installation', {'client_public_key': public_key})
    # pprint(dict(r.request.headers))
    # print()
    # pprint(dict(r.headers))
    # print()
    # pprint(r.json())
    # NOTE: in production these shouldn't be printed

    response = r.json()

    f = NamedTemporaryFile(
        dir='BunqAPI/tmp', delete=True, suffix='.json', mode='w'
        )
    try:
        json.dump(response['Response'][1]['Token'], f, indent=4)
    except KeyError:
        print (json.dumps(response, indent=4))
    # NOTE: need to call some type of dowanload fuction before the tmp files
    #  are deleted
    print ('\n\nFiles generated\n\n')
    return {'privateKey': privateKey, 'token': f.name}
    f.close()


def createKey():
    # generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # output PEM encoded version of private key
    privateKey = private_key.private_bytes(
      encoding=serialization.Encoding.PEM,
      format=serialization.PrivateFormat.PKCS8,
      encryption_algorithm=serialization.NoEncryption()
    )

    # print(privateKey.decode())  # NOTE: should not be printed in production

    # output PEM encoded version public part of private key
    # publicKey = private_key.public_key().public_bytes(
    #   encoding=serialization.Encoding.PEM,
    #   format=serialization.PublicFormat.SubjectPublicKeyInfo
    # ).decode()

    # print(publicKey)  # NOTE: should not be printed in production
    p = NamedTemporaryFile(
        dir='BunqAPI/tmp', delete=True, suffix='.pem', mode='wb'
        )
    # print ('p.name', p.name)
    p.write(privateKey)
    p.seek(0)
    return getToken(p.name)
    p.close()  # NOTE: gets closed/deleted after its use now it just needs to
    #                  get downloaded


# createKey()  # TODO: needs to get called via views.py etc
