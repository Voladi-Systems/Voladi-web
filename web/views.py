import json
import logging

from django.http import JsonResponse
from django.shortcuts import render

from web.forms import ContactForm
from web.mail import send_contact_form

log = logging.getLogger(__name__)


def index(request):
    data = None
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        pass

    form = ContactForm(data or None)
    if request.method == 'POST':
        if form.is_valid():
            try:
                send_contact_form(form.cleaned_data)
            except Exception as e:
                log.exception(e)
            return JsonResponse({
                'success': True
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors,
            })

    context = {
        'form': form
    }

    return render(request, 'web/index.html', context)
