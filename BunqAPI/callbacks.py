from pprint import pprint
from .pythonBunq.bunq import API


class callback(object):
    """docstring for sessoin."""
    def __init__(self, f, user):
        self.token = f['Token']['token']
        self.rsa_key = f['privateKey']
        self.api_key = f['API']
        self.server_key = f['ServerPublicKey']['server_public_key']
        self.user = user
        self.bunq_api = API(self.rsa_key, self.token, self.server_key)

    def response(self, response):
        if response.status_code == 200:
            print("succes")
            pprint(response.json())
        else:
            pprint(response.json()['Error'])

    def register(self):
        '''
        Registers the device
        https://doc.bunq.com/api/1/call/device-server/method/post
        '''

        r = self.bunq_api.query('device-server', {'secret': self.api_key, 'description': 'dev-server'})  # noqa

        self.response(r)

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
        '''

        r = self.bunq_api.query('session-server', {'secret': self.api_key})  # noqa

        if r.status_code == 200:
            print('\n\n')
            # pprint(r.json())
            session_token = r.json()['Response'][1]['Token']['token']
            self.user.profile.session_token = session_token
            self.user.save()
            self.get_users()
            return r.json()
        else:
            print('\n\n')
            pprint(r.json()['Error'][0])
            return r.json()

    def get_users(self, id=''):
        '''
        Returns a list of all the users belonging to this API key.
        https://doc.bunq.com/api/1/call/user/
        If an id is given then the info of that specific user is retrieved.
        '''
        self.bunq_api.token = self.user.profile.session_token
        r = self.bunq_api.query('user/%s' % id, verify=True)

        self.response(r)

    def get_accounts(self, userID, accountID=''):
        '''
        Returns a list of all accounts:
        https://doc.bunq.com/api/1/call/monetary-account/
        When usign a GET method a specific account can be returned.
        '''
        self.bunq_api = self.user.profile.session_token
        r = self.bunq_api.query(
            '/user/%s/monetary-account/%s' % (userID, accountID), verify=True)

        self.response(r)

    def payment(self, userID, accountID, mode='normal', paymentID=''):
        '''
        Returns a list of all transactions from an account. If an payment id is
        given then a specific transaction will be returned.

        Via this callback payments can be made aswell.

        https://doc.bunq.com/api/1/call/payment
        '''
        self.bunq.ap = self.user.profile.session_token
        url = 'user/%s/monetary-account/%s/' % (userID, accountID)
        if mode == 'normal':
            r = self.bunq_api.query(
                '%s/payment/%s' % (
                    url, paymentID), verify=True
            )

            self.response(r)
        elif mode == 'draft':
            r = self.bunq_api.query(
                '%s/draft-payment/%s' % (
                    url, paymentID), verify=True
            )
            self.response(r)
        elif mode == 'schedule':
            r = self.bunq_api.query(
                '%s/schedule-payment/%s' % (
                    url, paymentID), verify=True
            )
            self.response(r)
