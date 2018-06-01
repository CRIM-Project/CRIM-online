from django.template.defaultfilters import register


@register.filter(name='format_role_types')
def format_role_types(role_type_list):
    '''Takes a list of role types and returns an HTML-formatted
    comma-separated list of the role types with URLS.'''
    formatted_list = []
    for rt in role_type_list:
        url = '/people/?role={}'.format(rt['role_type_id'])
        formatted_list.append('<a href="{}">{}</a>'.format(url, rt['name']))
    return ', '.join(formatted_list)
