from django.template.defaultfilters import register


@register.filter(name='shorten')
def shorten(text, limit=72):
    # remove <p></p> tags
    text = text.replace('<p>', '').replace('</p>', '')
    if len(text) <= limit:
        return text
    else:
        return text[:limit] + '…'
