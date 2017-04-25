from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from .pythonbunq.bunq import API
from .aescrypt import encrypt
# from django.http import HttpResponse
import json
import tempfile
from pprint import pprint
# NOTE: generating private key and installation token


def getToken(privateKey):
    tmpDir = tempfile.mkdtemp(dir='./BunqAPI/tmp')
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
    else:
        d = {
            'Token': response['Response'][1]['Token'],
            'privateKey': privateKey.decode()
            }
        print ('\n\nFiles generated\n\n')
        pprint(d)
        print ('%s/BunqWebApp.json' % tmpDir)
        f = open('%s/BunqWebApp.json' % tmpDir, 'w')
        json.dump(d, f, indent=4)
        f.close()
        f2 = open('%s/BunqWebApp.json' % tmpDir, 'rb')
        encFile = open('%s/BunqWebApp.json.enc' % tmpDir, 'wb')
        encrypt(f2, encFile, '12345')
        return '%s/BunqWebApp.json.enc' % tmpDir


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

    return getToken(privateKey)
