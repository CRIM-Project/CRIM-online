from django.template.defaultfilters import register


@register.filter(name='include_mass_once')
def include_mass_once(piece_list):
    '''Takes a list of pieces, removes the mass movements, and
    adds the parent masses as appropriate (without duplication).
    '''
    new_list = []
    for piece in piece_list:
        if not piece['mass']:
            new_list.append(piece)
        else:
            if piece['mass'] not in new_list:
                new_list.append(piece['mass'])
    return new_list
