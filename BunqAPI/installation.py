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


class installation(object):
    """docstring for installation.
    
    Genereating information to store in the encrypted JSON.
    Each generation will create a new GUID and store this in the user's profile.  # noqa
    
    'r': is the instalation token used https://doc.bunq.com/api/1/call/installation  # noqa
         and the publick server key.
    
    'password': is the password used to encrypted the JSON file
    
    'GUID': gets generated each time the user generates a new file. This is
            used to check if the file actually belogs to the logged in user
            
    'RSA_key': the RSA key used to make API calls"""
    def __init__(self, username, password, API_KEY):
        self.username = username
        self.user = User.objects.get(username=self.username)
        self.password = password
        self.API_KEY = API_KEY
        self.GUID = self.get_GUID()
        self.RSA_key = self.RSA()
        self.r = self.getToken()

    def get_GUID(self):
        url = 'https://www.uuidgenerator.net/api/guid'
        GUID = requests.get(url).content.decode()
        return GUID
        # using UUIDGenerator.net for GUID

    def getToken(self):
        rsa_key = self.RSA_key
        bunq_api = API(rsa_key, None)

        # using the pubkey() helper function to get public part of key pair
        public_key = bunq_api.pubkey().decode()

        r = bunq_api.query('installation', {'client_public_key': public_key})

        response = r.json()
        try:
            return {
                'token': response['Response'][1]['Token'],
                'ServerPublicKey': response['Response'][2]['ServerPublicKey']}
        except KeyError:
            print (json.dumps(response, indent=4))
            raise KeyError
        #     # IDEA: need to return error html page

    def encrypt(self):
        d = {
            'Token': self.r['token'],
            'privateKey': self.RSA_key,
            'API': self.API_KEY,
            'ServerPublicKey': self.r['ServerPublicKey']
            # NOTE: need to add this
            }
        # GUID = self.GUID
        # user = User.objects.get(username=self.username)
        self.user.profile.GUID = self.GUID
        self.user.save()
        k = AESCipher(self.password)
        secret = AESCipher.encrypt(k, json.dumps(d))
        d2 = {
            'username': self.username,
            'secret': secret,
            'userID': self.GUID
        }
        print ('\n\nFiles generated\n\n')
        return(json.dumps(d2, indent=4, sort_keys=True))

    def RSA(self):
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

        return privateKey.decode()


class session(object):
    """docstring for sessoin."""
    def __init__(self, f):
        self.token = f['Token']['token']
        self.rsa_key = f['privateKey']
        self.api_key = f['API']
        self.server_key = f['ServerPublicKey']['server_public_key']
        print (self)

    def register(self):
        '''
        Registers the device
        https://doc.bunq.com/api/1/call/device-server/method/post
        '''
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

    def start_session(self, user):
        '''
        Starts a server-session according to
        https://doc.bunq.com/api/1/call/session-server/method/post
        the response can also be seen via this link on the docs. This session
        token is needed to make future API calls to the API. Therefore its
        getting stored in the database in the user profile.

        From the docs:
        A session expires after the same amount of time you have set for auto
        logout in your user account. If a request is made 30 seconds before a
        session expires, it will automatically be extended.
        '''
        bunq_api = API(self.rsa_key, self.token, self.server_key)

        # r = bunq_api.query('session-server', {'secret': api_key}, verify=True)  # noqa
        r = bunq_api.query('session-server', {'secret': self.api_key})  # noqa

        # r.json()['Response'][1]['Token'] would work too, but I mistrust predefined  # noqa
        # order, never know when someone starts shuffling things around
        if r.status_code == 200:
            print('\n\n')
            pprint(r.json())
            session_token = r.json()['Response'][1]['Token']['token']
            user.profile.session_token = session_token
            user.save()
            return r.json()
        else:
            print('\n\n')
            pprint(r.json()['Error'][0])
            return r.json()
