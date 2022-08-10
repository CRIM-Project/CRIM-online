from django.template.defaulttags import register

@register.filter(name='observation_type')
def observation_type(content):
    is_model = len(content['relationships_as_model']) > 0
    # is_deriv = len(content['relationships_as_derivative']) > 0
    return "model" if is_model else "derivative"
