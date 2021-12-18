from django.conf import settings
from django.template.defaultfilters import register

@register.simple_tag
def admin_email():
    return settings.ADMIN_EMAIL
