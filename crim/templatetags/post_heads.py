from django.template.defaultfilters import register


@register.filter(name='get_heads')
def get_heads(list_of_posts):
    '''Takes a list of forum posts and returns the subset that are heads
    (or top-level discussion posts).
    '''
    # A post *is* a head if it doesn't *have* a head.
    return [post for post in list_of_posts if not post.head]
