from crim.models.userprofile import CRIMUserProfile


def get_or_create_profile(request):
    profile = None
    user = request.user
    try:
        profile = user.get_profile()
    except CRIMUserProfile.DoesNotExist:
        profile = CRIMUserProfile.objects.create(user=user)
    return profile
