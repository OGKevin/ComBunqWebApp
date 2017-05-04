from pprint import pprint
from .pythonBunq.bunq import API
from .encryption import AESCipher


class callback(AESCipher):
    """docstring for sessoin."""
    def __init__(self, f, user, password):
        AESCipher.__init__(self, password)
        f = self.decrypt(f['secret'])
        token = f['Token']['token']
        server_key = f['ServerPublicKey']['server_public_key']
        rsa_key = f['privateKey']
        self.api_key = f['API']
        self.user = user
        # NOTE: this triggers the jsonpickle/jsonpickle/#171 issue
        self.bunq_api = API(rsa_key, token, server_key)

        self.userID = ''
        self.accountID = ''
        self.account_url = 'user/%s/monetary-account/%s/' % (self.userID, self.accountID) # noqa

    def register(self):
        '''
        Registers the device
        https://doc.bunq.com/api/1/call/device-server/method/post
        '''

        r = self.bunq_api.query('device-server', {'secret': self.api_key, 'description': 'dev-server'})  # noqa

        return self.response(r)

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

        r = self.bunq_api.query('session-server', {'secret': self.api_key})  # noqa

        if r.status_code == 200:
            print('\n\n')
            session_token = r.json()['Response'][1]['Token']['token']
            self.user.profile.session_token = session_token
            self.user.save()
            self.bunq_api.token = self.user.profile.session_token

            print (self.bunq_api.token)
            return r.json()
        else:
            print('\n\n')
            pprint(r.json()['Error'][0])
            return r.json()['Error'][0]

    def set_up(self, userID='', accountID=''):
        '''
        This method can be called after device registration and starting a
        session. This will set a userID and accountID.
        '''
        self.userID = userID
        self.accountID = accountID

    def users(self, id=''):
        '''
        Returns a list of all the users belonging to this API key.
        https://doc.bunq.com/api/1/call/user/
        If an id is given then the info of that specific user is retrieved.
        '''
        r = self.bunq_api.query('user/%s' % id, verify=True)
        print('this is users')
        return self.response(r)

    def accounts(self):
        '''
        Returns a list of all accounts:
        https://doc.bunq.com/api/1/call/monetary-account/
        When usign a GET method a specific account can be returned.
        '''
        r = self.bunq_api.query(self.url, verify=True)

        return self.response(r)

    def payment(self, mode='normal', paymentID=''):
        '''
        Returns a list of all transactions from an account. If an payment id is
        given then a specific transaction will be returned.

        Via this callback payments can be made aswell.

        https://doc.bunq.com/api/1/call/payment
        '''
        url = self.url
        if mode == 'normal':
            r = self.bunq_api.query(
                '%s/payment/%s' % (
                    url, paymentID), verify=True
            )

            return self.response(r)
        elif mode == 'draft':
            r = self.bunq_api.query(
                '%s/draft-payment/%s' % (
                    url, paymentID), verify=True
            )
            return self.response(r)
        elif mode == 'schedule':
            r = self.bunq_api.query(
                '%s/schedule-payment/%s' % (
                    url, paymentID), verify=True
            )
            return self.response(r)

    def request(self, inquiryID=''):
        '''
        Retuns all request for a user's account
        https://doc.bunq.com/api/1/call/request-inquiry
        '''
        url = self.url
        r = self.bunq_api.query(
            '%s/rerequest-inquiry/%s' % (url, inquiryID)
        )
        return self.response(r)

    def card(self, cardID=''):
        '''
        Return all the cards available to the user. Or a specific card if a
        cardID is given
        '''
        url = 'user/%s/card' % self.userID
        r = self.bunq_api.query(
            '%s/card/%s' % (url, cardID)
        )
        return self.response(r)

    def mastercard_action(self, cardID=''):
        '''
        MasterCard transaction view. Will return all the transaction made with
        a specific card or from all cards.
        '''
        r = self.bunq_api.query(
            '%s/mastercard-action/%s' % (self.url, cardID)
        )
        return self.response(r)

    def response(self, response):
        if response.status_code == 200:
            print("succes")
            pprint(response.json())
            return response.json()
        else:
            # pprint(response.json()['Error'][0])
            return response.json()['Error'][0]
