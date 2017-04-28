from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from .pythonbunq.bunq import API
from .encryption import encrypt
# from django.contrib.auth.models import User
# from django.http import HttpResponse
import json
# import tempfile
# from pprint import pprint
# NOTE: generating private key and installation token


def getToken(privateKey, userID):
    # tmpDir = tempfile.mkdtemp(dir='./BunqAPI/tmp')
    rsa_key = privateKey.decode()
    bunq_api = API(rsa_key, None)

    # using the pubkey() helper function to get public part of key pair
    public_key = bunq_api.pubkey().decode()

    r = bunq_api.query('installation', {'client_public_key': public_key})

    response = r.json()
    try:
        response['Response'][1]['Token']
    except KeyError:
        print (json.dumps(response, indent=4))
        # IDEA: need to return error html page
    else:
        d = {
            'Token': response['Response'][1]['Token'],
            # 'privateKey': privateKey.decode()
            }
        print ('\n\nFiles generated\n\n')
        # pprint(d)
        secret = encrypt(json.dumps(d), userID)
        d2 = {
            'userID': userID,
            'secret': secret,
            'privateKey': privateKey.decode()
        }
        # pprint(json.dumps(d2, indent=4, sort_keys=True))
        return(json.dumps(d2, indent=4, sort_keys=True))


def createJSON(userID):
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

    return getToken(privateKey, userID)
