from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from .pythonBunq.bunq import API
from .encryption import AESCipher
import requests
from django.contrib.auth.models import User
# from django.http import HttpResponse
import json
# import tempfile
from pprint import pprint
# NOTE: generating private key and installation token


def get_GUID():
    url = 'https://www.uuidgenerator.net/api/guid'
    GUID = requests.get(url).content.decode()
    return GUID
    # using UUIDGenerator.net for GUID


def getToken(privateKey, username, encryption_password, API_KEY):
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
            'ServerPublicKey': response['Response'][2]['ServerPublicKey'],
            'privateKey': privateKey.decode(),
            'API': API_KEY
            }
        GUID = get_GUID()
        user = User.objects.get(username=username)
        user.profile.GUID = GUID
        user.save()
        # pprint(d)
        k = AESCipher(encryption_password)
        # print ('\n\n', k.key, '\n\n')
        secret = AESCipher.encrypt(k, json.dumps(d))
        # print ('decryt\n\n', AESCipher.decrypt(k, secret))
        # secretB = encrypt(json.dumps(privateKey.decode()), userID)
        d2 = {
            'username': username,
            'secret': secret,
            'userID': GUID
            # 'secretB': secretB
        }
        # pprint(json.dumps(d2, indent=4, sort_keys=True))
        print ('\n\nFiles generated\n\n')
        return(json.dumps(d2, indent=4, sort_keys=True))


def createJSON(username, encryption_password, API_KEY):
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

    return getToken(privateKey, username, encryption_password, API_KEY)


class session(object):
    """docstring for sessoin."""
    def __init__(self, f):
        self.token = f['Token']['token']
        self.rsa_key = f['privateKey']
        self.api_key = f['API']
        self.server_key = f['ServerPublicKey']['server_public_key']
        print (self)

    def register(self):
        bunq_api = API(self.rsa_key, self.token, self.server_key)

        # r = bunq_api.query('session-server', {'secret': api_key}, verify=True)  # noqa
        r = bunq_api.query('device-server', {'secret': self.api_key, 'description': 'dev-server'})  # noqa

        # r.json()['Response'][1]['Token'] would work too, but I mistrust predefined  # noqa
        # order, never know when someone starts shuffling things around
        if r.status_code == 200:
            print('\n\n')
            pprint(r.json())
            return 'device registered'
        else:
            print('\n\n')
            pprint(r.json()['Error'][0])
            return r.json()

    def start_session(self):
            bunq_api = API(self.rsa_key, self.token, self.server_key)

            # r = bunq_api.query('session-server', {'secret': api_key}, verify=True)  # noqa
            r = bunq_api.query('session-server', {'secret': self.api_key})  # noqa

            # r.json()['Response'][1]['Token'] would work too, but I mistrust predefined  # noqa
            # order, never know when someone starts shuffling things around
            if r.status_code == 200:
                print('\n\n')
                pprint(r.json())
                return r.json()
            else:
                print('\n\n')
                pprint(r.json()['Error'][0])
                return r.json()
