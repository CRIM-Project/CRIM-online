from django.template.defaultfilters import register
from crim.models.piece import CRIMPiece
from crim.models.mass import CRIMMass
from crim.models.document import CRIMSource, CRIMTreatise


@register.filter(name='workgenre')
def work_type_or_genre(work):
    '''Given an object, returns the string Source, Mass,
    Piece or Treatise as appropriate. May include the genre
    in parentheses after Work.
    '''
    if type(work) is CRIMMass:
        return 'Mass'
    elif type(work) is CRIMPiece:
        if work.genre:
            return 'Piece (' + work.genre.name + ')'
        else:
            return 'Piece'
    elif type(work) is CRIMTreatise:
        return 'Treatise'
    elif type(work) is CRIMSource:
        return 'Source'
    else:  # Fallback; should not occur
        return '-'
