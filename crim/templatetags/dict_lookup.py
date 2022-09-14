from django.template.defaulttags import register
from django.utils.text import slugify

@register.filter(name='lookup')
def lookup(map, key):
    if key in map:
        return map.get(key)
    return ""

@register.filter(name='get_rel_details')
def rel_details(relationship, type_name):
    # Apparently certain values of the data are not sanitized properly and the types while equal do not match
    # in particular `non-mechanical transformation` is in the definition while many entries contain the value
    # `non mechanical transformation` so we must slugify the types to comapre them
    if slugify(type_name) == slugify(relationship.relationship_type):
        return relationship.details
    return {}

@register.filter(name='get_obs_details')
def obs_details(observation, type_name):
    if type_name == observation.musical_type:
        return observation.details
    return {}

@register.filter(name='rel_formatter')
def rel_formatter(value):
    if type(value) == list:
        return ','.join(str(item) for item in value)
    return value

@register.filter(name="obj_type")
def obj_type(value):
    return type(value)

