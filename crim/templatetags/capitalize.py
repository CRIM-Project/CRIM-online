from django.template.defaultfilters import register


# Hack so that "non-imitative" etc. display correctly:
# besides capitalizing, replace "non " with "non-"
@register.filter(name='capitalize')
def capitalize(s):
    s_hyphen = s.replace('non ', 'non-')
    return s_hyphen.capitalize()
