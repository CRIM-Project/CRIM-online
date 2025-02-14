from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django import forms

from crim.models.user import CRIMUserProfile
from crim.models.person import CRIMPerson

from crim.models.definition import CRIMDefinition
from crim.models.document import CRIMTreatise, CRIMSource
from crim.models.forum import CRIMForumPost
from crim.models.genre import CRIMGenre
from crim.models.group import CRIMGroup
from crim.models.part import CRIMPart
from crim.models.phrase import CRIMPhrase
from crim.models.piece import CRIMPiece, CRIMModel, CRIMMassMovement
from crim.models.mass import CRIMMass
from crim.models.role import CRIMRole, CRIMRoleType
from crim.models.observation import CRIMObservation, CJObservation
from crim.models.relationship import CRIMRelationship, CJRelationship
from crim.models.voice import CRIMVoice

from crim.models.note import CRIMNote


# This is to fix the annoying layout of the new Django admin interface
admin.sites.AdminSite.enable_nav_sidebar = False


class CRIMPieceMassForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    title = forms.CharField(widget=forms.Select(choices=CRIMPiece.MASS_MOVEMENTS))


class CRIMPieceMassInline(admin.TabularInline):
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in ('pdf_links', 'mei_links'):
            formfield.widget = forms.Textarea(attrs={'rows': 1, 'cols': 40})
        return formfield

    form = CRIMPieceMassForm
    model = CRIMPiece
    exclude = ('piece_id', 'genre', 'remarks', 'composer', 'date_sort', 'number_of_voices')
    extra = 5
    max_num = 5


class CRIMPartPieceInline(admin.TabularInline):
    model = CRIMPart
    exclude = ('part_id', 'remarks')
    extra = 1


class CRIMPhrasePieceInline(admin.TabularInline):
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in ('text', 'translation'):
            formfield.widget = forms.Textarea(attrs={'rows': 1, 'cols': 40})
        return formfield

    model = CRIMPhrase
    exclude = ('phrase_id', 'part_number', 'translation', 'remarks')
    extra = 1


class CRIMVoicePieceInline(admin.TabularInline):
    model = CRIMVoice
    exclude = ('voice_id', 'remarks')
    extra = 1


class CRIMRoleMassInline(admin.TabularInline):
    # For sorting by last name
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'person':
            kwargs['queryset'] = CRIMPerson.objects.order_by('name_sort')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    model = CRIMRole
    exclude = ('date_sort', 'piece', 'treatise', 'source', 'remarks')
    extra = 1


class CRIMRolePieceInline(admin.TabularInline):
    # For sorting by last name
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'person':
            kwargs['queryset'] = CRIMPerson.objects.order_by('name_sort')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    model = CRIMRole
    exclude = ('date_sort', 'mass', 'treatise', 'source', 'remarks')
    extra = 1


class CRIMRoleTreatiseInline(admin.TabularInline):
    # For sorting by last name
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'person':
            kwargs['queryset'] = CRIMPerson.objects.order_by('name_sort')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    model = CRIMRole
    exclude = ('date_sort', 'piece', 'mass', 'source', 'remarks')
    extra = 1


class CRIMRoleSourceInline(admin.TabularInline):
    # For sorting by last name
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'person':
            kwargs['queryset'] = CRIMPerson.objects.order_by('name_sort')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    model = CRIMRole
    exclude = ('date_sort', 'piece', 'mass', 'treatise', 'remarks')
    extra = 1


class CRIMPieceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['genre'].queryset = CRIMGenre.objects.filter(genre_id='mass')


class CRIMMassMovementForm(forms.ModelForm):
    title = forms.CharField(widget=forms.Select(choices=CRIMPiece.MASS_MOVEMENTS))


class CRIMPersonAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'name_alternate_list':
            formfield.widget = forms.Textarea(attrs={'rows': 3, 'cols': 32})
        return formfield

    # For sorting by last name
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'person':
            kwargs['queryset'] = CRIMPerson.objects.order_by('name_sort')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    fields = (
        'person_id',
        'name',
        'name_sort',
        'name_alternate_list',
        'birth_date',
        'death_date',
        'active_date',
        'remarks',
    )
    list_display = (
        'person_id',
        'sorted_name',
        'date_sort',
    )
    search_fields = (
        'person_id',
        'name',
        'name_alternate_list',
        'remarks',
    )
    ordering = (
        'person_id',
        'name_sort',
    )


class CRIMModelAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in ('pdf_links', 'mei_links'):
            formfield.widget = forms.Textarea(attrs={'rows': 2, 'cols': 60})
        if db_field.name == 'voices':
            formfield.widget = forms.Textarea(attrs={'rows': 4, 'cols': 30})
        return formfield

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(mass=None)

    fields = (
        'piece_id',
        'title',
        'composer',
        'genre',
        'pdf_links',
        'mei_links',
        'remarks',
    )
    inlines = (
        CRIMRolePieceInline,
        # CRIMVoicePieceInline,
        # CRIMPartPieceInline,
        # CRIMPhrasePieceInline,
    )
    search_fields = (
        'piece_id',
        'title',
        'remarks',
    )
    list_display = (
        'title_with_id',
        'composer',
        'genre',
        'date_sort',
    )
    ordering = (
        'piece_id',
    )
    list_filter = (
        'genre',
    )
    readonly_fields = (
        'composer',
    )


class CRIMMassMovementAdmin(admin.ModelAdmin):
    form = CRIMMassMovementForm

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.exclude(mass=None)

    fields = (
        'mass',
        'title',
        'pdf_links',
        'mei_links',
        'remarks',
    )
    inlines = (
        CRIMRolePieceInline,
        # CRIMVoicePieceInline,
        # CRIMPartPieceInline,
        # CRIMPhrasePieceInline,
    )
    search_fields = (
        'mass__mass_id',
        'mass__title',
        'piece_id',
        'title',
    )
    list_display = (
        'title_with_id',
        'composer',
        'date_sort',
    )
    ordering = (
        'piece_id',
    )


class CRIMMassAdmin(admin.ModelAdmin):
    fields = (
        'mass_id',
        'title',
        'genre',
        'remarks',
    )
    inlines = (
        CRIMPieceMassInline,
        CRIMRoleMassInline,
    )
    list_display = (
        'title_with_id',
        'composer',
        'date_sort',
    )
    search_fields = (
        'mass_id',
        'title',
        'remarks',
    )
    ordering = (
        'mass_id',
    )


class CRIMTreatiseAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'external_links':
            formfield.widget = forms.Textarea(attrs={'rows': 2, 'cols': 60})
        return formfield

    fields = (
        'document_id',
        'title',
        'remarks',
        'external_links',
    )
    inlines = (
        CRIMRoleTreatiseInline,
    )
    search_fields = (
        'document_id',
        'title',
        'remarks',
    )
    list_display = (
        'title_with_id',
        'author',
        'date_sort',
    )
    ordering = (
        'document_id',
    )


class CRIMSourceAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'external_links':
            formfield.widget = forms.Textarea(attrs={'rows': 2, 'cols': 60})
        return formfield

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'piece_contents':
            kwargs['queryset'] = CRIMPiece.objects.exclude(genre=None)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    fields = (
        'document_id',
        'title',
        'source_type',
        'mass_contents',
        'piece_contents',
        'treatise_contents',
        'external_links',
        'remarks',
    )
    inlines = (
        CRIMRoleSourceInline,
    )
    search_fields = (
        'document_id',
        'title',
        'remarks',
    )
    list_display = (
        'title_with_id',
        'publisher',
        'date_sort',
        'source_type',
    )
    ordering = (
        'document_id',
    )


class CRIMGenreAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'name_plural',
        'remarks',
    )
    list_display = (
        'name',
    )
    ordering = (
        'name',
    )


class CRIMPartAdmin(admin.ModelAdmin):
    fields = (
        'piece',
        'order',
        'name',
        'remarks',
    )
    list_display = (
        'part_id',
        'piece_title',
        'order',
        'name',
    )
    ordering = (
        'part_id',
    )
    search_fields = (
        'piece__piece_id',
        'piece__title',
        'name',
    )


class CRIMPhraseAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in ('text', 'translation'):
            formfield.widget = forms.Textarea(attrs={'rows': 1, 'cols': 60})
        return formfield

    fields = (
        'part',
        'number',
        'start_measure',
        'stop_measure',
        'text',
        'translation',
        'remarks',
    )
    list_display = (
        'phrase_id',
        'piece_title',
        'part_number',
        'text',
    )
    ordering = (
        'phrase_id',
    )
    search_fields = (
        'piece__piece_id',
        'piece__title',
        'text',
        'translation',
    )


class CRIMVoiceAdmin(admin.ModelAdmin):
    fields = (
        'piece',
        'order',
        'original_name',
        'regularized_name',
        'clef',
        'remarks',
    )
    list_display = (
        'voice_id',
        'piece_title',
        'order',
        'original_name',
        'regularized_name',
    )
    ordering = (
        'voice_id',
    )


class CRIMRoleAdmin(admin.ModelAdmin):
    fields = (
        'person',
        'role_type',
        'mass',
        'piece',
        'treatise',
        'source',
        'date',
        'remarks',
    )
    list_display = (
        'person_with_role',
        'work',
        'date_sort',
    )
    search_fields = (
        'person__person_id',
        'person__name',
        'piece__piece_id',
        'mass__mass_id',
        'treatise__document_id',
        'source__document_id',
        'piece__title',
        'mass__title',
        'treatise__title',
        'source__title',
    )
    list_filter = (
        'role_type',
    )
    ordering = (
        'role_type__name',
        'person__name_sort',
        'source__document_id',
        'treatise__document_id',
        'mass__mass_id',
        'piece__piece_id',
    )


class CRIMRoleTypeAdmin(admin.ModelAdmin):
    fields = (
        'role_type_id',
        'name',
        'name_plural',
        'remarks',
    )
    list_display = (
        'name',
    )
    ordering = (
        'name',
    )
    readonly_fields = (
        'role_type_id',
    )


class CRIMObservationAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'ema':
            formfield.widget = forms.Textarea(attrs={'rows': 2, 'cols': 60})
        elif db_field.name in ('mt_fp_comment', 'remarks'):
            formfield.widget = forms.Textarea(attrs={'rows': 3, 'cols': 40})
        elif 'voice' in db_field.name:
            formfield.widget = forms.Textarea(attrs={'rows': 3, 'cols': 30})
        elif db_field.name in ('mt_cad_cantizans', 'mt_cad_tenorizans'):
            formfield.widget = forms.Textarea(attrs={'rows': 1, 'cols': 30})
        return formfield

    # For sorting by last name
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'observer':
            kwargs['queryset'] = CRIMPerson.objects.order_by('name_sort')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    fieldsets = (
        (None, {
            'fields': ('observer', 'piece', 'ema'),
        }),
        ('Cantus firmus', {
            'fields': ('mt_cf_voices', ('mt_cf_dur', 'mt_cf_mel')),
        }),
        ('Soggetto', {
            'fields': ('mt_sog_voices',
                       ('mt_sog_dur', 'mt_sog_mel',
                        'mt_sog_ostinato', 'mt_sog_periodic')),
        }),
        ('Counter-soggetto', {
            'fields': ('mt_csog_voices', ('mt_csog_dur', 'mt_csog_mel')),
        }),
        ('Contrapuntal duo', {
            'fields': ('mt_cd_voices',),
        }),
        ('Fuga', {
            'fields': ('mt_fg_voices', 'mt_fg_int', 'mt_fg_tint',
                       ('mt_fg_periodic', 'mt_fg_strict', 'mt_fg_flexed'),
                       ('mt_fg_sequential', 'mt_fg_inverted', 'mt_fg_retrograde'),
                      ),
        }),
        ('Periodic entry', {
            'fields': ('mt_pe_voices', 'mt_pe_int', 'mt_pe_tint',
                       ('mt_pe_strict', 'mt_pe_flexed', 'mt_pe_flt'),
                       ('mt_pe_sequential', 'mt_pe_added', 'mt_pe_invertible'),
                      ),
        }),
        ('Imitative duo', {
            'fields': ('mt_id_voices', 'mt_id_int', 'mt_id_tint',
                       ('mt_id_strict', 'mt_id_flexed', 'mt_id_flt', 'mt_id_invertible'),
                      ),
        }),
        ('Non-imitative duo', {
            'fields': ('mt_nid_voices', 'mt_nid_int', 'mt_nid_tint',
                       ('mt_nid_strict', 'mt_nid_flexed', 'mt_nid_flt',
                        'mt_nid_sequential', 'mt_nid_invertible'),
                       ),
        }),
        ('Homorhythm', {
            'fields': ('mt_hr_voices',
                       ('mt_hr_simple', 'mt_hr_staggered',
                        'mt_hr_sequential', 'mt_hr_fauxbourdon')),
        }),
        ('Cadence', {
            'fields': ('mt_cad_cantizans', 'mt_cad_tenorizans',
                       'mt_cad_type', 'mt_cad_tone',
                       'mt_cad_dtv', 'mt_cad_dti'),
        }),
        ('Interval pattern', {
            'fields': ('mt_int_voices',
                       ('mt_int_p6', 'mt_int_p3'),
                       ('mt_int_c35', 'mt_int_c83', 'mt_int_c65')),
        }),
        ('Form and Process', {
            'fields': ('mt_fp_ir', 'mt_fp_range', 'mt_fp_comment'),
        }),
        ('Other', {
            'fields': ('remarks', 'curated'),
        }),
    )
    list_display = (
        'id_in_brackets',
        'curated',
        'observer',
        'piece',
        'created',
        'updated',
    )
    ordering = (
        'id',
    )
    search_fields = (
        'piece__piece_id',
        'piece__title',
        'piece__mass__title',
        'observer__person_id',
        'observer__name',
    )


class CRIMRelationshipAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('observer', 'model_observation', 'derivative_observation'),
        }),
        ('Quotation', {
            'fields': ('rt_q', ('rt_q_x', 'rt_q_monnayage')),
        }),
        ('Mechanical transformation', {
            'fields': ('rt_tm',
                       ('rt_tm_snd', 'rt_tm_minv',
                        'rt_tm_retrograde', 'rt_tm_ms',
                        'rt_tm_transposed', 'rt_tm_invertible')),
        }),
        ('Non-mechanical transformation', {
            'fields': ('rt_tnm',
                       ('rt_tnm_embellished', 'rt_tnm_reduced',
                        'rt_tnm_amplified', 'rt_tnm_truncated', 'rt_tnm_ncs'),
                       ('rt_tnm_ocs', 'rt_tnm_ocst', 'rt_tnm_nc')),
        }),
        ('New Material', {
            'fields': ('rt_nm',),
        }),
        ('Omission', {
            'fields': ('rt_om',),
        }),
        ('Other', {
            'fields': ('remarks', 'curated'),
        }),
    )
    list_display = (
        'id_in_brackets',
        'curated',
        'observer',
        'model_observation',
        'derivative_observation',
        'created',
        'updated',
    )
    ordering = (
        'id',
    )
    search_fields = (
        'model_observation__piece__piece_id',
        'model_observation__piece__title',
        'model_observation__piece__mass__title',
        'derivative_observation__piece__piece_id',
        'derivative_observation__piece__title',
        'derivative_observation__piece__mass__title',
        'observer__person_id',
        'observer__name',
    )


class CRIMDefinitionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'updated',
    )


class CJObservationAdmin(admin.ModelAdmin):
    # Including the commented-out fields slows performance considerably
    list_display = [
        'id_in_brackets',
        'curated',
        # 'observer',
        'musical_type',
        # 'model_observation',
        # 'derivative_observation',
        'created',
        'updated',
    ]
    search_fields = (
        'observer__person_id',
        'observer__name',
        'musical_type',
        'piece__piece_id',
        'piece__title',
        'piece__mass__title',
    )


class CJRelationshipAdmin(admin.ModelAdmin):
    readonly_fields = ['musical_type']
    # Including the commented-out fields slows performance considerably
    list_display = [
        'id_in_brackets',
        'curated',
        # 'observer',
        'relationship_type',
        # 'model_observation',
        # 'derivative_observation',
        'created',
        'updated',
    ]
    search_fields = (
        'observer__person_id',
        'observer__name',
        'relationship_type',
        'model_observation__piece__piece_id',
        'model_observation__piece__title',
        'model_observation__piece__mass__title',
        'derivative_observation__piece__piece_id',
        'derivative_observation__piece__title',
        'derivative_observation__piece__mass__title',
    )


class CRIMForumPostAdmin(admin.ModelAdmin):
    fields = (
        'author',
        'title',
        'text',
        'parent',
        'edited',
        'alive',
    )
    list_display = (
        'author',
        'title',
        'created_at',
        'updated_at',
        'alive',
    )


class UserProfileInline(admin.StackedInline):
    model = CRIMUserProfile
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(UserAdmin):
    inlines = (
        UserProfileInline,
    )
    ordering = (
        'username',
    )




admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(CRIMPerson, CRIMPersonAdmin)

admin.site.register(CRIMMass, CRIMMassAdmin)
admin.site.register(CRIMModel, CRIMModelAdmin)
admin.site.register(CRIMMassMovement, CRIMMassMovementAdmin)
admin.site.register(CRIMTreatise, CRIMTreatiseAdmin)
admin.site.register(CRIMSource, CRIMSourceAdmin)

admin.site.register(CRIMPart, CRIMPartAdmin)
admin.site.register(CRIMPhrase, CRIMPhraseAdmin)
admin.site.register(CRIMVoice, CRIMVoiceAdmin)

admin.site.register(CRIMRole, CRIMRoleAdmin)
admin.site.register(CRIMObservation, CRIMObservationAdmin)
admin.site.register(CRIMRelationship, CRIMRelationshipAdmin)

admin.site.register(CRIMGenre, CRIMGenreAdmin)
admin.site.register(CRIMRoleType, CRIMRoleTypeAdmin)

admin.site.register(CRIMDefinition, CRIMDefinitionAdmin)
admin.site.register(CJObservation, CJObservationAdmin)
admin.site.register(CJRelationship, CJRelationshipAdmin)

admin.site.register(CRIMNote)

admin.site.register(CRIMGroup)
admin.site.register(CRIMForumPost, CRIMForumPostAdmin)
