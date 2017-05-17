import base64
import copy
import json
import uuid

import requests
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

from apiwrapper.config.configcontroller import ConfigController


class ApiClient:
    __version_api = 1
    __version = '0.1.0'
    # __uri = "https://api.bunq.com/v%d" % __version_api
    __uri = "https://sandbox.public.api.bunq.com/v%d" % __version_api

    def __init__(self, api_key=None):
        self.config = ConfigController()

        if api_key is None:
            self.api_key = self.config.get('api_key')
        else:
            self.api_key = api_key

    def get(self, endpoint):
        result = self.request('GET', endpoint)

        if self.verify(result):
            return result

        return None

    def post(self, endpoint, payload):
        return self.request('POST', endpoint, payload)

    def request(self, method, endpoint, payload=None):
        headers = self.create_headers(method, endpoint, payload)

        url = '%s%s' % (self.__uri, endpoint)

        return requests.request(method, url, headers=headers, json=payload)

    def create_headers(self, method, endpoint, payload):
        action = '%s /v%d%s' % (method.upper(), self.__version_api, endpoint)
        headers_all = copy.deepcopy(self.headers)
        msg = self.create_message(action, headers_all, payload)

        if self.privkey is not None:
            headers_all['X-Bunq-Client-Signature'] = self.sign(msg)

        return headers_all

    def create_message(self, action, headers, payload):
        headers_as_text = '\n'.join(['%s: %s' % (k, v) for k, v in sorted(
            headers.items())])
        msg = '%s\n%s\n\n' % (action, headers_as_text)

        if payload:
            msg += json.dumps(payload)

        return msg

    def sign(self, msg):
        """Create signature for message
        Taken from https://github.com/madeddie/python-bunq - Thanks!

        :param msg: data to be signed, usually action, headers and body
        :type msg: str

        """
        return base64.b64encode(
            self.privkey_pem.sign(
                msg.encode(),
                padding.PKCS1v15(),
                hashes.SHA256()
            )
        ).decode()

    def verify(self, res):
        """Verify response from server
        Taken from https://github.com/madeddie/python-bunq - Thanks!

        :param res: request to be verified
        :type res: requests.models.Response

        """
        if not self.server_pubkey:
            print('No server public key defined, skipping verification')
            return

        serv_headers = [
            'X-Bunq-Client-Request-Id',
            'X-Bunq-Client-Response-Id'
        ]

        msg = '%s\n%s\n\n%s' % (
            res.status_code,
            '\n'.join(
                ['%s: %s' % (k, v) for k, v in sorted(
                    res.headers.items()
                ) if k in serv_headers]
            ),
            res.text
        )

        signature = base64.b64decode(res.headers['X-Bunq-Server-Signature'])

        try:
            self.server_pubkey_pem.verify(
                signature,
                msg.encode(),
                padding.PKCS1v15(),
                hashes.SHA256()
            )
        except InvalidSignature:
            print('Message failed verification, data might be tampered with')
            return False
        else:
            return True

    @property
    def headers(self):
        request_id = str(uuid.uuid1())
        headers = {
            'Cache-Control': 'no-cache',
            'User-Agent': 'universal-bunq-api-python/' + self.__version,
            'X-Bunq-Client-Request-Id': request_id,
            'X-Bunq-Geolocation': '0 0 0 0 NL',
            'X-Bunq-Language': 'en_US',
            'X-Bunq-Region': 'en_US'
        }
        if self.session_token is not None:
            headers['X-Bunq-Client-Authentication'] = self.session_token
        elif self.installation_token is not None:
            headers['X-Bunq-Client-Authentication'] = self.installation_token

        return headers

    @property
    def installation_token(self):
        return self.config.get('installation_token')

    @installation_token.setter
    def installation_token(self, value):
        self.config.set('installation_token', value)

    @property
    def server_token(self):
        return self.config.get('server_token')

    @property
    def session_token(self):
        return self.config.get('session_token')

    @session_token.setter
    def session_token(self, value):
        self.config.set('session_token', value)

    @property
    def pubkey(self):
        return self.config.get('key_public')

    @property
    def privkey(self):
        return self.config.get('key_private')

    @property
    def privkey_pem(self):
        private_key_bytes = self.privkey
        if not isinstance(private_key_bytes, bytes):
            private_key_bytes = private_key_bytes.encode()

        return serialization.load_pem_private_key(
            private_key_bytes,
            password=None,
            backend=default_backend()
        )

    @property
    def api_key(self):
        return self.config.get('api_key')

    @api_key.setter
    def api_key(self, value):
        self.config.set('api_key', value)

    @property
    def server_pubkey(self):
        return self.config.get('server_pubkey')

    @server_pubkey.setter
    def server_pubkey(self, value):
        self.config.set('server_pubkey', value)

    @property
    def server_pubkey_pem(self):
        server_pubkey_bytes = self.server_pubkey
        if not isinstance(server_pubkey_bytes, bytes):
            server_pubkey_bytes = server_pubkey_bytes.encode()

        return serialization.load_pem_public_key(
            server_pubkey_bytes,
            backend=default_backend()
        )
