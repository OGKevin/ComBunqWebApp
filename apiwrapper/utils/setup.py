"""
DISCLAIMER: This code was partially taken from the example files in:

https://github.com/madeddie/python-bunq

Thanks for @madeddie for writing these examples and the API Wrapper
"""

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

import apiwrapper.config.controller as config
import apiwrapper.endpoints.controller as endpoints
from apiwrapper.clients.api_client import ApiClient
from apiwrapper.clients.api_client_persisting import ApiClientPersisting


class Setup:

    """A setup class that registers a connection with the Bunq Api

    :param api_key: A string, the api key of the user
    """
    def __init__(self, api_key):
        self.api_key = api_key
        self.config = config.Controller()
        self.api_client = None
        self.endpoints = None

    def setup_w_new_key_pair(self, save_to_config=True):
        private_key, _ = self.create_new_key_pair(save_to_config)
        self.setup_w_existing_private_key(private_key, save_to_config)

    def setup_w_existing_private_key(self, private_key, save_to_config=True):
        if save_to_config:
            self.api_client = ApiClientPersisting(self.api_key)
        else:
            self.api_client = ApiClient(private_key, self.api_key)

        self.endpoints = endpoints.Controller(self.api_client)

        if self.register_key_pair() \
                and self.create_new_device_server() \
                and self.create_new_session():
            print("Setup successful!")

    @staticmethod
    def convert_private_key_to_pem(private_key):
        private_key_bytes = private_key
        if not isinstance(private_key_bytes, bytes):
            private_key_bytes = private_key.encode()

        return serialization.load_pem_private_key(
            private_key_bytes,
            password=None,
            backend=default_backend()
        )

    def create_new_key_pair(self, save_to_config=True):
        """Creates a new public/private key pair and saves them to the config file
        
        :return: Prints out a success message
        """
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        private_key_decoded = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()

        public_key_decoded = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()

        print('New key pair was created')

        if save_to_config:
            self.config.set('key_private', private_key_decoded)
            self.config.set('key_public', public_key_decoded)
        else:
            print('\tNew Private Key: %s' % private_key_decoded)
            print('\tNew Public Key:  %s' % public_key_decoded)

        return private_key_decoded, public_key_decoded

    def register_key_pair(self):
        """Registers a public/private key pair with the Bunq API
        Ref: https://doc.bunq.com/api/1/call/installation/method/post
        
        Saves the installation (user) token and server public key to config
        
        KEY_PRIVATE needs to be set in the config for this method to run
        
        :return: Prints out either a success message or 
        the Error message of the API
        """

        r = self.endpoints.installation.create_installation()
        try:
            res = r['Response']

            id_entry = [x for x in res if list(x)[0] == 'Id'][0]
            token_entry = [x for x in res if list(x)[0] == 'Token'][0]
            server_entry = [x for x in res if
                            list(x)[0] == 'ServerPublicKey'][0]

            installation_id = id_entry['Id']['id']
            installation_token = token_entry['Token']['token']
            server_public_key = server_entry['ServerPublicKey'][
                'server_public_key']

            self.api_client.installation_id = installation_id
            self.api_client.installation_token = installation_token
            self.api_client.server_pubkey = server_public_key

            print('Key pair was registered successfully')
            print('\tInstallation Id: %s' % installation_id)
            print('\tInstallation Token: %s' % installation_token)
            print('\tServer Public Key: %s' % server_public_key)

            return True
        except KeyError:
            print('Register Key Pair Error: ' + str(r['Error'][0]))

            return False

    def create_new_device_server(self):
        """Creates a new device server at the Bunq API 
        Ref: https://doc.bunq.com/api/1/call/device-server/method/post
        
        API_KEY needs to be set in the config for this method to run
        
        :return: Prints out either a Success or the Error message of the API
        """
        r = self.endpoints.device_server.create_new_device_server(
            description="New Device")

        try:
            res = r['Response']

            print('New device server was created successfully.')
            return True
        except KeyError:
            print('New Device Server Error: ' + str(r['Error'][0]))
            return False

    def create_new_session(self):
        """Creates a new session at the Bunq API
        Ref: https://doc.bunq.com/api/1/call/session-server/method/post
        
        Saves the session token to config
        
        API_KEY needs to be set in the config for this method to run
        
        :return: Prints out either a success message or the Error 
        message of the API
        """

        r = self.endpoints.session_server.create_new_session_server()

        try:
            res = r["Response"]

            res = [x for x in res if list(x)[0] == 'Token'][0]
            session_token = res['Token']['token']

            self.api_client.session_token = session_token

            print('New session was created successfully.')
            print('\tNew Session Token: %s' % session_token)
            return True
        except KeyError:
            print('Create Session Error: ' + str(r['Error'][0]))
            return False
