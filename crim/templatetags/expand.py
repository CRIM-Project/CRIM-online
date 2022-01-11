from django.template.defaultfilters import register
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from crim.common import get_current_definition
from crim.models.definition import CRIMDefinition


@register.filter(name='expand', needs_autoescape=True)
def expand(obs_or_rel, kind, autoescape=True):
    '''Expands JSON observation details into human-readable list form,
    using the definition object as a template.
    '''
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x

    if kind == 'relationship':
        type_kind = 'relationship_type'
        try:
            definition = obs_or_rel.get('definition').get('relationship_definition')
        except:
            definition = get_current_definition().relationship_definition
    else:  # Observation
        type_kind = 'musical_type'
        try:
            definition = obs_or_rel.get('definition').get('observation_definition')
        except:
            definition = get_current_definition().observation_definition

    html = ''
    # If no definition is provided, use the most recent one
    if definition is None:
        return mark_safe('-')
    else:
        for type in definition:
            if type.get('name') == obs_or_rel.get(type_kind):
                if not type.get('subtypes'):
                    return mark_safe(f'No further details about this {kind}.')
                else:
                    for subtype in type.get('subtypes'):
                        subtype_name = subtype.get('name')
                        subtype_value = obs_or_rel.get('details').get(subtype_name)
                        subtype_value_html = ''
                        if isinstance(subtype_value, list):
                            for e in subtype_value:
                                subtype_value_html += '<br>' + esc(str(e).capitalize())
                        elif subtype_value is None:
                            subtype_value_html = '-'
                        else:
                            subtype_value_html = esc(str(subtype_value).capitalize())
                        html += ('<p class="hanging"><strong>' +
                                 esc(subtype_name.capitalize()) + ':' +
                                 '</strong>' + ' ' +
                                 subtype_value_html +
                                 '</p>'
                                )
    return mark_safe(html)
