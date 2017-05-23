import base64
import copy
import json
import uuid

import requests
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

from apiwrapper.endpoints.controller import Controller as EndpointController


class ApiClient:
    """Handles the communication with the Bunq API

    Can send HTTP requests and verify the response
    """

    __version_api = 1
    __agent_name = "complete-bunq-api-test"
    __agent_version = '0.1.0'
    _uri_production = "https://api.bunq.com/v%d" % __version_api
    _uri_sandbox = "https://sandbox.public.api.bunq.com/v%d" % __version_api

    __variables = ['installation_id', 'installation_token', 'api_key',
                   'server_token', 'server_pubkey', 'session_token']

    def __init__(self, privkey, use_sandbox=True, **kwargs):
        self.privkey = privkey
        self._uri = self._uri_sandbox if use_sandbox else self._uri_production
        self._handle_kwargs(kwargs)

        self.__endpoint_controller = EndpointController(self)

    def _handle_kwargs(self, kwargs):
        for k in self.__variables:
            if getattr(self, k, None) is None or kwargs.get(k) is not None:
                setattr(self, k, kwargs.get(k))

    def get(self, endpoint, verify=True):
        result = self.request('GET', endpoint)

        if verify and not self.verify(result):
            return None

        return result

    def post(self, endpoint, payload):
        return self.request('POST', endpoint, payload)

    def request(self, method, endpoint, payload=None):
        headers = self.create_headers(method, endpoint, payload)

        url = '%s%s' % (self._uri, endpoint)

        return requests.request(method, url, headers=headers, json=payload)

    def create_headers(self, method, endpoint, payload):
        action = '%s /v%d%s' % (method.upper(), self.__version_api, endpoint)
        headers_all = copy.deepcopy(self.headers)
        msg = self.create_message(action, headers_all, payload)

        if self.privkey is not None:
            headers_all['X-Bunq-Client-Signature'] = self.sign(msg)

        return headers_all

    @staticmethod
    def create_message(action, headers, payload):
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
            return True

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

    def request_parameters_are_set(self):
        return self.privkey is not None

    @property
    def endpoints(self):
        if self.request_parameters_are_set():
            return self.__endpoint_controller
        else:
            print('ApiClient is not yet properly set up! Variables missing!')
            return None

    @property
    def headers(self):
        request_id = str(uuid.uuid1())
        headers = {
            'Cache-Control':            'no-cache',
            'User-Agent':               '%s/%s' % (
                self.__agent_name, self.__agent_version),
            'X-Bunq-Client-Request-Id': request_id,
            'X-Bunq-Geolocation':       '0 0 0 0 NL',
            'X-Bunq-Language':          'en_US',
            'X-Bunq-Region':            'en_US'
        }
        if self.session_token is not None:
            headers['X-Bunq-Client-Authentication'] = self.session_token
        elif self.installation_token is not None:
            headers['X-Bunq-Client-Authentication'] = self.installation_token

        return headers

    @property
    def privkey_pem(self):
        if self.privkey is None:
            return None

        return self.convert_privkey_to_pem(self.privkey)

    @property
    def pubkey(self):
        if self.privkey_pem is None:
            return None

        return self.get_pubkey_from_privkey_pem(self.privkey_pem)

    @property
    def server_pubkey_pem(self):
        if self.server_pubkey is None:
            return None

        return self.convert_pubkey_to_pem(self.server_pubkey)

    @staticmethod
    def get_pubkey_from_privkey_pem(privkey_pem):
        return privkey_pem.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()

    @staticmethod
    def convert_pubkey_to_pem(key):
        key_bytes = ApiClient.convert_to_bytes(key)

        return serialization.load_pem_public_key(
            key_bytes,
            backend=default_backend()
        )

    @staticmethod
    def convert_privkey_to_pem(key):
        key_bytes = ApiClient.convert_to_bytes(key)

        return serialization.load_pem_private_key(
            key_bytes,
            password=None,
            backend=default_backend()
        )

    @staticmethod
    def convert_to_bytes(key):
        key_bytes = key
        if not isinstance(key_bytes, bytes):
            key_bytes = key_bytes.encode()

        return key_bytes
