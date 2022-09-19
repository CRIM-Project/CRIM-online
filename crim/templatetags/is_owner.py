from django.template.defaulttags import register

@register.filter(name='is_owner')
def is_owner(request, user_id):
    curr_user = request.user
    # Check if the user is authenticated with the system (if not they cannot be the owner)
    if not curr_user.is_authenticated or not curr_user.profile.person:
        return False
    return (curr_user.is_superuser) or (curr_user.profile.person.id == user_id)
