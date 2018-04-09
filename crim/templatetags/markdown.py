from django.template.defaultfilters import register
from markdown import markdown


@register.filter(name='markdown')
def eval_markdown(text):
    # safe_mode governs how the function handles raw HTML
    return markdown(text, safe_mode='escape')
