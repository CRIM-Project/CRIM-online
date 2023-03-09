from django.template.defaultfilters import register
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from crim.common import get_current_definition, print_voice
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

    # If no definition is provided, use the most recent one

    singular_voice_fields = []
    plural_voice_fields = []

    if kind == 'relationship':
        type_kind = 'relationship_type'
        try:
            definition = obs_or_rel.get('definition').get('relationship_definition')
        except:
            definition = get_current_definition().relationship_definition
    else:  # Observation
        type_kind = 'musical_type'
        try:
            complete_definition = obs_or_rel.get('definition')
            definition = complete_definition.get('observation_definition')
            singular_voice_fields = complete_definition.get('voice_fields')['singular']
            plural_voice_fields = complete_definition.get('voice_fields')['plural']
        except:
            complete_definition = get_current_definition()
            definition = complete_definition.observation_definition
            try:
                singular_voice_fields = complete_definition.voice_fields['singular']
                plural_voice_fields = complete_definition.voice_fields['plural']
            except:
                pass

    html = ''
    if definition is None:
        return mark_safe('-')
    else:
        details = obs_or_rel.get('details')
        if obs_or_rel.get('piece'):
            piece_id = obs_or_rel.get('piece').get('piece_id')
        # If we have no details, we need to make this an empty dicionary
        # because we will query it for keys.
        if details is None:
            details = {}
        for type in definition:
            if type.get('name').replace('-', ' ') == obs_or_rel.get(type_kind).replace('-', ' '):
                if not type.get('subtypes'):
                    return mark_safe(f'No further details about this {kind}.')
                else:
                    for subtype in type.get('subtypes'):
                        subtype_name = subtype.get('name')
                        subtype_value = details.get(subtype_name)
                        subtype_value_html = ''
                        if subtype_name in plural_voice_fields:
                            for e in subtype_value:
                                subtype_value_html += '<br>' + print_voice(piece_id, e)
                        elif subtype_name in singular_voice_fields:
                            subtype_value_html = print_voice(piece_id, subtype_value)
                        elif isinstance(subtype_value, list):
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
