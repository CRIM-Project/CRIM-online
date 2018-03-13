from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django import forms

from crim.constants import *
from crim.models.userprofile import CRIMUserProfile
from crim.models.person import CRIMPerson

from crim.models.document import CRIMDocument, CRIMTreatise, CRIMSource
from crim.models.piece import CRIMPiece
from crim.models.mass_movement import CRIMMassMovement
from crim.models.mass import CRIMMass
from crim.models.role import CRIMRole
from crim.models.relationship import CRIMRelationship

from crim.models.note import CRIMNote
from crim.models.comment import CRIMComment
from crim.models.discussion import CRIMDiscussion


class CRIMPersonAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(CRIMPersonAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'name_alternate_list':
            formfield.widget = forms.Textarea(attrs={'rows': 3, 'cols': 32})
        return formfield

    fields = [
        'name',
        'name_sort',
        'name_alternate_list',
        'birth_date',
        'death_date',
        'active_date',
        'remarks',
    ]

    list_display = (
        'sorted_name',
        'sorted_date',
    )
    
    list_filter = [
        'date_sort',
    ]
    
    search_fields = [
        'name',
        'name_alternate_list',
        'remarks',
    ]


class CRIMPieceAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.exclude(genre=MASS)

    fields = [
        'piece_id',
        'title',
        'genre',
        'pdf_link',
        'mei_link',
    ]

    list_display = (
        'piece_id',
        'title',
        'genre',
        'sorted_date',
    )
    
    list_filter = [
        'genre',
    ]


class CRIMMassMovementAdmin(admin.ModelAdmin):
    fields = [
        'piece_id',
        'mass',
        'title',
        'pdf_link',
        'mei_link',
    ]
    search_fields = (
        'piece_id',
        'mass__title',
        'title',
    )
    list_display = (
        'piece_id',
        'mass',
        'title',
    )
    ordering = ('piece_id',)


class UserProfileInline(admin.StackedInline):
    model = CRIMUserProfile
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )
    ordering = ['username',]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(CRIMPerson, CRIMPersonAdmin)

admin.site.register(CRIMMass)
admin.site.register(CRIMMassMovement, CRIMMassMovementAdmin)
admin.site.register(CRIMPiece, CRIMPieceAdmin)

admin.site.register(CRIMTreatise)
admin.site.register(CRIMSource)

admin.site.register(CRIMRole)
admin.site.register(CRIMRelationship)

admin.site.register(CRIMNote)
admin.site.register(CRIMComment)
admin.site.register(CRIMDiscussion)
