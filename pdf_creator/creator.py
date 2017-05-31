import pdfkit
from django.template.loader import render_to_string


def payment(data):
    data['Payment']['amount']['value'] = float(data['Payment']['amount']['value'])  # noqa

    if data['Payment']['amount']['value'] < 0:
        data['Payment']['amount']['out'] = True
        data['Payment']['amount']['value'] = data['Payment']['amount']['value'] * -1  # noqa

    html_string = render_to_string(
        'pdf_creator/payment.html', {'Payment': data['Payment']}
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

    return pdf
