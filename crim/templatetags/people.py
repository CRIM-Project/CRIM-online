from django.template.defaultfilters import register

def people_list(roles, role_types=''):
    '''Returns a list of person names, with urls, based on a list
    of roles. Restricts names to those associated with the given
    role types. Does not restrict names if no role types are given.
    Returns empty string if no such role exists in the list.'''
    if not roles:
        return []
    else:
        if roles[0]['role_type']['role_type_id'] in role_types.split(',') or not role_types:
            name = roles[0]['person']['name']
            url = roles[0]['person']['url'].replace('/data/', '/')
            names_to_add = ['<a href="{0}">{1}</a>'.format(url, name)]
        else:
            names_to_add = []
        return names_to_add + people_list(roles[1:], role_types)

@register.filter(name='people')
def people(roles, role_types=''):
    '''Returns a list of names (see `people_list`) formatted as a string.'''
    return ', '.join(people_list(roles, role_types))


@register.filter(name='first_person')
def first_person(roles, role_types=''):
    '''Given a list of roles, returns the name of the first person
    (in HTML, along with the URL) with the given role type ID.'''
    list_of_people = people_list(roles, role_types)
    return list_of_people[0] if list_of_people else ''
