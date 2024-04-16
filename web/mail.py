from django.conf import settings
from django.template.loader import render_to_string

from povulo.mail import send_mail


def send_contact_form(context):
    subject = 'Povulo - Contact form'
    html_message = render_to_string('web/email/contact_form.html', context=context)
    return send_mail(subject, html_message, settings.DEFAULT_FROM_EMAIL, [settings.CONTACT_FORM_EMAIL])
