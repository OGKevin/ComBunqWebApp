import pdfkit
from django.template.loader import render_to_string
import csv
import tempfile
from django.contrib.sessions.backends.db import SessionStore
import requests
import base64
import json
import logging
import pathlib
import os
from django.core import signing

logger = logging.getLogger(name='raven')


# from pprint import pprint


class Creator(object):
    """docstring for Creator."""

    def __init__(self, user, extension=None):
        self.user = user
        self.extension = extension

    def payment(self, data, transaction_id=None):
        data['Payment']['amount']['value'] = float(
            data['Payment']['amount']['value'])

        if data['Payment']['amount']['value'] < 0:
            data['Payment']['amount']['out'] = True
            data['Payment']['amount']['value'] = (
                data['Payment']['amount']['value'] * -1)

        data['Payment']['amount']['value'] = ("%0.2f" % (
            data['Payment']['amount']['value']
        )).replace('.', ',')

        if self.extension == 'pdf':
            file_path = self.pdf(data['Payment'], 'payment.html',
                                 prefix=transaction_id)

        self.store_in_session(file_path)

        response = {
            'Response': [{
                'status': 'Payment file Generated'
            }]
        }

        return response

    def transactions(self, data):
        if self.extension == 'csv':
            headers = list(data[0].keys())
            rows = []

            [rows.append(list(x.values())) for x in data]

            file_path = self.csv(headers, rows)

        self.store_in_session(file_path)

        response = {
            'Response': [{
                'status': 'Transactions file Generated'
            }]
        }

        return response

    def avatar(self, data):
        temp_file = self.temp_file('.png')
        temp_file.write(data)
        temp_file.close()

        self.store_in_session(temp_file.name)

    def create_avatar_from_session(self):
        session_key = self.user.session.session_token
        s = SessionStore(session_key=session_key)

        dec_data = signing.loads(s['avatar'])
        png = base64.b64decode(dec_data.encode())

        temp_file = self.temp_file('.png')
        temp_file.write(png)
        temp_file.close()

        self.store_in_session(temp_file.name)

    def invoice(self, data):
        url = "https://api.sycade.com/btp-int/Invoice/Generate"
        headers = {
            'content-type': 'application/json',
            'cache-control': 'no-cache',
        }
        r = requests.request(method='POST', url=url, headers=headers,
                             data=data)

        if r.status_code == 200:
            pdf = base64.b64decode(
                json.loads(r.text)['Invoice']
            )
            temp_file = self.temp_file(extension='.pdf', bytes_=True)
            temp_file.write(pdf)
            temp_file.close()

            self.store_in_session(file_path=temp_file.name)

            response = {
                'Response': [{
                    'status': 'Invoice PDF generated.'
                }]
            }
            return response

        else:  # pragma: no cover
            error = {
                'Error': [{
                    'error_description_translated': ('PDF generator API'
                                                     ' returned an error.')
                }]
            }
            logger.error(r.json())
            return error

    def user_json(self, data):
        temp_file = self.temp_file(extension='.json', bytes_=False)
        temp_file.write(json.dumps(obj=data))

        self.store_in_session(file_path=temp_file.name)

    def path_check(self):  # pragma: no cover
        file_path = self.user.tokens.file_token
        if pathlib.Path(file_path).is_file():
            os.remove(file_path)

    def store_in_session(self, file_path):
        self.path_check()
        s = SessionStore()
        s['file_path'] = file_path
        s.create()
        self.user.tokens.file_token = s.session_key
        self.user.save()

    @staticmethod
    def csv(headers, rows):
        temp_file = Creator.temp_file('.csv', bytes_=False)

        csv_file = csv.writer(temp_file)
        csv_file.writerow(headers)

        [csv_file.writerow(x) for x in rows]

        temp_file.close()

        return temp_file.name

    @staticmethod
    def pdf(data, template, prefix=None):
        html_string = render_to_string(
            'filecreator/pdf/%s' % template, {'data': data}
        )

        options = {
            'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'dpi': 300,
            'quiet': '',
            # 'print-media-type': '',
        }

        pdf = pdfkit.from_string(html_string, False, options=options)

        temp_file = Creator.temp_file('.pdf', append_prefix=prefix)
        temp_file.write(pdf)
        temp_file.close()

        return temp_file.name

    @staticmethod
    def temp_file(extension, bytes_=True, append_prefix=None):
        if bytes_ is True:
            mode = 'wb'
        else:
            mode = 'w'

        if append_prefix is not None:
            prefix = "ComBunqWebApp-pr-%s-pr-" % append_prefix
        else:
            prefix = "ComBunqWebApp"

        temp_file = tempfile.NamedTemporaryFile(
            mode=mode,
            dir=None,
            suffix='%s' % extension,
            prefix=prefix,
            delete=False
        )
        return temp_file
