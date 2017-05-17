# from pprint import pprint
from BunqAPI.encryption import AESCipher
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist
from apiwrapper.endpoints.endpointcontroller import EndpointController as Endpoints  # noqa
from apiwrapper.clients.api_client_non_persisting import ApiClientNonPersisting as API2  # noqa


class callback(AESCipher):
    """docstring for sessoin.
        This class handles the callbacks to the bunq api.

        f = the contents of the users ecnrypted json.
        api_token = the api token from the bunq app.
        user = is the currently logged in user.
        init_api = is the pythonBunq.bunq.api instance before session token
        userID = is the provided user id that can be used to retrieve data
                 of a specific user register to the API key.
        accountID = cardID = id's to retrieve a specific card or account
                    belonging to the user id.
        account_url = url used by most endpoints
        s = is the server session token stored in the django sessoin. The key
            for this session is sotred in the database, only logged in users
            can retreive their keys.
        bunq_api = is the pythonBunq.bunq.api instace after the session token
                   is retrieved.
    """
    def __init__(self, f, user, password, userID=None, accountID=None):
        AESCipher.__init__(self, password)
        f = self.decrypt(f['secret'])
        token = f['Token']['token']
        server_key = f['ServerPublicKey']['server_public_key']
        rsa_key = f['privateKey']
        api_key = f['API']
        self.user = user
        # self.init_api = API(rsa_key, token, server_key)
        self.init_api = API2(
            privkey=rsa_key, api_key=api_key, installation_token=token,
            server_pubkey=server_key)

        if userID:
            self.userID = int(userID)
        if accountID:
            self.accountID = int(accountID)

        # self.account_url = 'user/%s/monetary-account/%s' % (self.userID, self.accountID) # noqa

        try:
            s = Session.objects.get(session_key=user.profile.session_token)  # noqa
            session_token = s.get_decoded()['session_token']
            bunq_api = API2(
                privkey=rsa_key, api_key=api_key,
                session_token=session_token, server_pubkey=server_key)
            self.bunq_api = Endpoints(bunq_api)

        except ObjectDoesNotExist:
            print('Sessoin not created yet')

    def register(self):
        '''
        Registers the device
        https://doc.bunq.com/api/1/call/device-server/method/post
        '''

        endpoint = Endpoints(self.init_api)
        return endpoint.device_server.create_new_device_server('dev-server')

    def start_session(self):
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

        When the session expires the token will be unusbale.
        '''
        endpoint = Endpoints(self.init_api)
        r = endpoint.session_server.create_new_session_server()

        try:
            session_token = r['Response'][1]['Token']['token']
            s = SessionStore()
            s['session_token'] = session_token
            s.create()
            self.user.profile.session_token = s.session_key
            self.user.save()
        except KeyError:
            return r
        else:
            return r

    def users(self):
        '''
        Returns a list of all the users belonging to this API key.
        https://doc.bunq.com/api/1/call/user/
        If an id is given then the info of that specific user is retrieved.
        '''

        try:
            return self.bunq_api.user.get_user_by_id(self.userID)
        except AttributeError:
            return self.bunq_api.user.get_all_users()

    def accounts(self):
        '''
        Returns a list of all accounts:
        https://doc.bunq.com/api/1/call/monetary-account/
        When usign a GET method a specific account can be returned.
        '''
        try:
            return self.bunq_api.monetary_account.get_account_by_id(
                self.userID, self.accountID)
        except AttributeError:
            try:
                return self.bunq_api.monetary_account.get_all_accounts_for_user(  # noqa
                    self.userID
                    )
            except AttributeError as b:
                return {
                    'Error': [{'error_description_translated': '%s' % b}]
                }

    def payment(self, mode='normal', paymentID=''):
        '''
        Returns a list of all transactions from an account. If an payment id is
        given then a specific transaction will be returned.

        Via this callback payments can be made aswell.

        https://doc.bunq.com/api/1/call/payment
        '''
        if mode == 'normal':
            try:
                return self.bunq_api.payment.get_all_payments_for_account(
                    self.userID, self.accountID)
            except AttributeError as e:
                return {
                    'Error': [{'error_description_translated': '%s' % e}]
                }

    def card(self):
        '''
        Return all the cards available to the user. Or a specific card if a
        cardID is given
        '''
        try:
            return self.bunq_api.card.get_card_for_user_by_id(
                self.userID, self.accountID)
        except AttributeError:
            try:
                return self.bunq_api.card.get_all_cards_for_user(
                    self.userID
                )
            except AttributeError as b:
                return {
                    'Error': [{'error_description_translated': '%s' % b}]
                }
