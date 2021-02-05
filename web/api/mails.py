from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

def MailConfirmation(data):
    return render_to_string('email.html', data)
