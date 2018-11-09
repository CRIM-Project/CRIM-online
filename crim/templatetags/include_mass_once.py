from django.template.defaultfilters import register


@register.filter(name='include_mass_once')
def include_mass_once(piece_list):
    '''Takes a list of pieces, removes the mass movements, and
    adds the parent masses as appropriate (without duplication).
    '''
    pieces = []
    masses = []
    for piece in piece_list:
        if not piece['mass']:
            pieces.append(piece)
        else:
            if piece['mass'] not in masses:
                masses.append(piece['mass'])
    return pieces + masses
