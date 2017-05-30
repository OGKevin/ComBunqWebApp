from BunqAPI.encryption import AESCipher
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist
from apiwrapper.clients.api_client import ApiClient as API2
import requests
import json
import base64
import tempfile
import time
# from pprint import pprint


class callback(AESCipher):
    """docstring for sessoin.
        This class handles the callbacks to the bunq api.

        user_file = the contents of the users ecnrypted json.
        api_token = the api token from the bunq app.
        user = is the currently logged in user.
        init_api = is the API2 instance before session token
        userID = is the provided user id that can be used to retrieve data
                 of a specific user register to the API key.
        accountID = cardID = id's to retrieve a specific card or account
                    belonging to the user id.
        account_url = url used by most endpoints
        s = is the server session token stored in the django sessoin. The key
            for this session is sotred in the database, only logged in users
            can retreive their keys.
        bunq_api = is the API2 instace after the session token
                   is retrieved.
    """

    def __init__(self, user_file, user, password, userID=None, accountID=None):
        AESCipher.__init__(self, password)
        self.user_file = self.decrypt(user_file['secret'])
        self.user = user
        self._user_id = userID
        self._account_id = accountID
        self.init_api = self.user_file
        self.bunq_api = self.user_file

    def register(self):
        '''
        Registers the device
        https://doc.bunq.com/api/1/call/device-server/method/post
        '''

        r = self.init_api.endpoints.device_server.create_new_device_server('ComBunqWebApp')  # noqa
        return r

    def load_file(self):
        start_session = self.start_session()

        if 'Response' in start_session:
            self.user_id = self.get_user_id(start_session['Response'])

            time.sleep(1.5)

            accounts = self.accounts()

            time.sleep(.5)

            self.account_id = accounts['Response'][0]['MonetaryAccountBank']['id']  # noqa

            time.sleep(1.5)

            payments = self.payment()

            response = {
                'start_session': start_session['Response'],
                'accounts': accounts['Response'],
                'payments': payments['Response']
            }

        else:
            response = start_session

        return response

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
        r = self.init_api.endpoints.session_server.create_new_session_server()

        if r.status_code == 200:
            try:
                session_token = r.json()['Response'][1]['Token']['token']
            except KeyError:  # pragma: no cover
                return r.json()
            else:
                s = SessionStore()
                s['session_token'] = session_token
                s.create()
                self.user.profile.session_token = s.session_key
                self.user.save()

                avatar_uuid = self.get_avatar_id(r.json()['Response'],
                                                 'start_session')

                self.get_avatar(avatar_uuid)

                return r.json()
        else:
            error = {
                'Error': [{
                    'error_description_translated': 'Something went wrong starting the session'  # noqa
                }]
            }
            return error

    def users(self):
        '''
        Returns a list of all the users belonging to this API key.
        https://doc.bunq.com/api/1/call/user/
        If an id is given then the info of that specific user is retrieved.
        '''

        if self.user_id is None:
            r = self.bunq_api.endpoints.user.get_logged_in_user()
        else:
            r = self.bunq_api.endpoints.user.get_user_by_id(self.user_id)

        if 'Response' in r.json():
            avatar_id = self.get_avatar_id(r.json()['Response'])
            self.get_avatar(avatar_id)
        return r.json()

    def accounts(self):
        '''
        Returns a list of all accounts:
        https://doc.bunq.com/api/1/call/monetary-account/
        When usign a GET method a specific account can be returned.
        '''

        if self.account_id is not None:
            r = self.bunq_api.endpoints.monetary_account.get_account_by_id(
                self.user_id, self.account_id).json()
        else:
            r = self.bunq_api.endpoints.monetary_account.get_all_accounts_for_user(  # noqa
                self.user_id
                ).json()
        return r

    def payment(self, mode='normal', paymentID=''):
        '''
        Returns a list of all transactions from an account. If an payment id is
        given then a specific transaction will be returned.

        Via this callback payments can be made aswell.

        https://doc.bunq.com/api/1/call/payment
        '''
        if mode == 'normal':
            if self.account_id and self.user_id is not None:
                r = self.bunq_api.endpoints.payment.get_all_payments_for_account(  # noqa
                    self.user_id, self.account_id).json()
            else:
                r = {
                    'Error': [{
                        'error_description_translated': ('account or userd id '
                                                         'is not specified')
                    }]
                }
            return r

    def card(self):
        '''
        Return all the cards available to the user. Or a specific card if a
        cardID is given
        '''

        if self.account_id and self.user_id is not None:
            r = self.bunq_api.endpoints.card.get_card_for_user_by_id(
                self.user_id, self.account_id).json()
        elif self.account_id is None and self.user_id is not None:
            r = self.bunq_api.endpoints.card.get_all_cards_for_user(
                self.user_id
            ).json()
        else:
            r = {
                'Error': [{
                    'error_description_translated': 'user_id must be specified'
                }]
            }
        return r

    def invoice(self):
        '''
        Returns the invoice of the user
        '''
        if self.user_id is not None:
            r = self.bunq_api.endpoints.invoice.get_all_invoices_for_user(
                self.user_id
            ).json()

            try:
                invoice = r['Response'][0]['Invoice']
            except IndexError:
                error = {
                    'Error': [{
                        'error_description_translated': ('the response seems '
                                                         'to have no invoice '
                                                         'in it.')
                    }]
                }
                return error
            else:
                return self.get_pdf(json.dumps(invoice))

        else:
            error = {
                'Error': [{
                    'error_description_translated': 'There is no user id specified'  # noqa
                }]
            }

    def get_pdf(self, invoice):
        url = "https://api.sycade.com/btp-int/Invoice/Generate"
        headers = {
            'content-type':  "application/json",
            'cache-control': "no-cache",
        }
        r = requests.request("POST", url, data=invoice, headers=headers)
        if r.status_code == 200:
            pdf = base64.b64decode(
                json.loads(r.text)['Invoice']
            )
            temp_file = tempfile.NamedTemporaryFile(
                mode='wb',
                dir=None,
                suffix='.pdf',
                prefix='ComBunqWebApp',
                delete=False
            )
            temp_file.write(pdf)
            temp_file.close()

            s = SessionStore()
            s['invoice_pdf'] = temp_file.name
            s.create()
            self.user.profile.invoice_token = s.session_key
            self.user.save()

            r = {
                'Response': [{
                    'status': 'PDF Generated.....'
                }]
            }
            return r
        else:  # pragma: no cover
            r = {
                'Error': [{
                    'error_description_translated': 'PDF generator API returned an error'  # noqa
                }]
            }
            return r

    def get_avatar(self, avatar_id):
        r = self.init_api.endpoints.attachment_public.get_content_of_public_attachment(avatar_id)  # noqa

        png = r.content

        temp_file = tempfile.NamedTemporaryFile(
            mode='wb',
            dir=None,
            suffix='.png',
            prefix='ComBunqWebApp',
            delete=False
        )
        temp_file.write(png)
        temp_file.close()

        s = SessionStore()
        s['avatar_png'] = temp_file.name
        s.create()
        self.user.profile.avatar_token = s.session_key
        self.user.save()

    @property
    def init_api(self):
        return self._init_api

    @init_api.setter
    def init_api(self, value):
        API = API2(
            privkey=value['privateKey'],
            api_key=value['API'],
            installation_token=value['Token']['token'],
            server_pubkey=value['ServerPublicKey']['server_public_key']
        )
        self._init_api = API

    @property
    def bunq_api(self):
        return self._bunq_api

    @bunq_api.setter
    def bunq_api(self, value):
        try:
            session_token = Session.objects.get(
                session_key=self.user.profile.session_token
            ).get_decoded()['session_token']
        except ObjectDoesNotExist:
            return None
        else:
            API = API2(
                privkey=value['privateKey'],
                api_key=value['API'],
                session_token=session_token,
                server_pubkey=value['ServerPublicKey']['server_public_key']
            )
            self._bunq_api = API

    @property
    def user_id(self):
        if self._user_id is None or self._user_id is '':
            return None
        else:
            return self.to_int(self._user_id)

    @user_id.setter
    def user_id(self, value):
        self._user_id = value

    @property
    def account_id(self):
        if self._account_id is None or self._account_id is '':
            return None
        else:
            return self.to_int(self._account_id)

    @account_id.setter
    def account_id(self, value):
        self._account_id = value

    @staticmethod
    def to_int(string):
        return int(string)

    @staticmethod
    def get_avatar_id(response, mode=None):
        if mode == 'start_session':
            try:
                id = response[2]['UserCompany']['avatar']['image'][0]['attachment_public_uuid']  # noqa
            except KeyError:
                id = response[2]['UserPerson']['avatar']['image'][0]['attachment_public_uuid']  # noqa
            return id
        else:
            try:
                id = response[0]['UserCompany']['avatar']['image'][0]['attachment_public_uuid']  # noqa
            except KeyError:
                id = response[0]['UserPerson']['avatar']['image'][0]['attachment_public_uuid']  # noqa
            return id

    @staticmethod
    def get_user_id(response):
        try:
            id = response[2]['UserCompany']['id']
        except KeyError:
            id = response[2]['UserPerson']['id']

        return id
