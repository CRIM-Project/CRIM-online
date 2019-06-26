from django.template.defaultfilters import register


@register.filter(name='get_heads')
def get_heads(list_of_posts):
    '''Takes a list of forum posts and returns a list of all those post's
    heads, including those posts in the original list that were already heads
    and excluding duplicates.
    '''
    # A post *is* a head if it doesn't *have* a head.
    post_heads = []
    for post in list_of_posts:
        this_post_head = post.head if post.head else post
        if not this_post_head in post_heads:
            post_heads.append(this_post_head)
    return post_heads
