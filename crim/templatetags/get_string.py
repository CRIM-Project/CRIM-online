'''From https://djangosnippets.org/snippets/1243/'''


from django import template

register = template.Library()


def do_get_string(parser, token):
    try:
        tag_name, key, value = token.split_contents()
    except ValueError:
        return GetStringNode()

    return GetStringNode(key[1:-1], value)


class GetStringNode(template.Node):
    def __init__(self, key=None, value=None):
        self.key = key
        if value:
            self.value = template.Variable(value)

    def render(self, context):
        get = context.get('request').GET.copy()

        if self.key:
            actual_value = self.value.resolve(context)
            get.__setitem__(self.key, actual_value)

        return get.urlencode()


register.tag('get_string', do_get_string)
