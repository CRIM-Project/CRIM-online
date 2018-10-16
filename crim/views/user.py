from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.renderers import JSONRenderer

from crim.serializers.user import CRIMUserProfileDetailSerializer
from crim.models.user import CRIMUserProfile


class UserProfile(generics.RetrieveAPIView):
    model = CRIMUserProfile
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMUserProfileDetailSerializer
    renderer_classes = (
        JSONRenderer,
    )
    queryset = CRIMUserProfile.objects.all()

    def get_object(self):
        url_arg = self.kwargs['username']
        user = CRIMUserProfile.objects.filter(user__username=url_arg)

        obj = get_object_or_404(user)
        self.check_object_permissions(self.request, obj)
        return obj


class UserProfileData(UserProfile):
    pass


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
