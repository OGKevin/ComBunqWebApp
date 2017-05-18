from apiwrapper.clients.api_client import ApiClient
from apiwrapper.config.controller import Controller


class ApiClientPersisting(ApiClient):
    """A subclass of ApiClient which connects to the Bunq API,
    but persists (saves) the login parameters needed to communicate
    with the Bunq API to a config file.

    Make sure that the parameters are saved to the config file specified
    in config/configcontroller.
    """

    def __init__(self, api_key=None):
        self.config = Controller()
        self.api_key = self.config.get('api_key') if api_key is None else api_key
        self._uri = self._uri_sandbox if self._use_sandbox else \
            self._uri_production

    @property
    def api_key(self):
        return self.config.get('api_key')

    @api_key.setter
    def api_key(self, value):
        self.config.set('api_key', value)

    @property
    def installation_id(self):
        return self.config.get('installation_id')

    @installation_id.setter
    def installation_id(self, value):
        self.config.set('installation_id', value)

    @property
    def installation_token(self):
        return self.config.get('installation_token')

    @installation_token.setter
    def installation_token(self, value):
        self.config.set('installation_token', value)

    @property
    def privkey(self):
        return self.config.get('key_private')

    @property
    def server_pubkey(self):
        return self.config.get('server_pubkey')

    @server_pubkey.setter
    def server_pubkey(self, value):
        self.config.set('server_pubkey', value)

    @property
    def server_token(self):
        return self.config.get('server_token')

    @server_token.setter
    def server_token(self, value):
        self.config.set('server_token', value)

    @property
    def session_token(self):
        return self.config.get('session_token')

    @session_token.setter
    def session_token(self, value):
        self.config.set('session_token', value)


