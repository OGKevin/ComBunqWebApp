from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from apiwrapper.clients.api_client_non_persisting import ApiClientNonPersisting as API  # noqa
from apiwrapper.endpoints.endpointcontroller import EndpointController as Endpoints  # noqa
# from BunqAPI.pythonBunq.bunq import API
from BunqAPI.encryption import AESCipher
import requests
from django.contrib.auth.models import User
import json
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
        self.r = self.get_token()

    def get_GUID(self):
        url = 'https://www.uuidgenerator.net/api/guid'
        GUID = requests.get(url).content.decode()
        return GUID
        # using UUIDGenerator.net for GUID

    def get_token(self):
        rsa_key = self.RSA_key
        bunq_api = Endpoints(API(rsa_key, None))

        r = bunq_api.installation.create_installation()

        # NOTE: need to rewrite this to check status code...
        try:
            return {
                'token': r['Response'][1]['Token'],
                'ServerPublicKey': r['Response'][2]['ServerPublicKey']}
        except KeyError:  # pragma: no cover
            print (json.dumps(r, indent=4))
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
