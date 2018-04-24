from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django import forms

from crim.models.userprofile import CRIMUserProfile
from crim.models.person import CRIMPerson

from crim.models.document import CRIMTreatise, CRIMSource
from crim.models.genre import CRIMGenre
from crim.models.piece import CRIMPiece, CRIMModel, CRIMMassMovement
from crim.models.mass import CRIMMass
from crim.models.role import CRIMRole, CRIMRoleType
from crim.models.observation import CRIMObservation
from crim.models.relationship import CRIMRelationship

from crim.models.note import CRIMNote
from crim.models.comment import CRIMComment


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
    exclude = ('piece_id', 'genre', 'remarks')
    extra = 5
    max_num = 5


class CRIMRolePersonInline(admin.TabularInline):
    model = CRIMRole
    exclude = ('date_sort', 'remarks')
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
    model = CRIMRole
    exclude = ('date_sort', 'piece', 'mass', 'source', 'remarks')
    extra = 1


class CRIMRoleSourceInline(admin.TabularInline):
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
    inlines = (
        CRIMRolePersonInline,
    )
    list_display = (
        'person_id',
        'sorted_name',
        'sorted_date',
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
        'date_sort',
    )


class CRIMModelAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in ('pdf_links', 'mei_links'):
            formfield.widget = forms.Textarea(attrs={'rows': 2, 'cols': 64})
        return formfield

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(mass=None)

    fields = (
        'piece_id',
        'title',
        'genre',
        'pdf_links',
        'mei_links',
        'remarks',
    )
    inlines = (
        CRIMRolePieceInline,
    )
    search_fields = (
        'piece_id',
        'title',
    )
    list_display = (
        'title_with_id',
        'composer',
        'genre',
        'date',
    )
    ordering = (
        'piece_id',
    )
    list_filter = (
        'genre',
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
        'date',
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
        'date',
    )
    search_fields = (
        'mass_id',
        'title',
    )
    ordering = (
        'mass_id',
    )


class CRIMTreatiseAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'external_links':
            formfield.widget = forms.Textarea(attrs={'rows': 2, 'cols': 64})
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
    )
    list_display = (
        'title_with_id',
        'author',
        'date',
    )
    ordering = (
        'document_id',
    )


class CRIMSourceAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'external_links':
            formfield.widget = forms.Textarea(attrs={'rows': 2, 'cols': 64})
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
    )
    list_display = (
        'title_with_id',
        'publisher',
        'date',
        'source_type',
    )
    ordering = (
        'document_id',
    )


class CRIMGenreAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'remarks',
    )
    list_display = (
        'name',
    )
    ordering = (
        'name',
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
        'sorted_date',
    )
    search_fields = (
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
        'name',
        'remarks',
    )
    list_display = (
        'name',
    )
    ordering = (
        'name',
    )


class CRIMObservationAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'ema':
            formfield.widget = forms.Textarea(attrs={'rows': 1, 'cols': 60})
        if db_field.name in ('mt_fp_comment', 'remarks'):
            formfield.widget = forms.Textarea(attrs={'rows': 3, 'cols': 40})
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
            'classes': ('collapse',),
            'fields': ('mt_cf_voice', ('mt_cf_dur', 'mt_cf_mel')),
        }),
        ('Soggetto', {
            'classes': ('collapse',),
            'fields': ('mt_sog_voice',
                       ('mt_sog_dur', 'mt_sog_mel',
                        'mt_sog_ostinato', 'mt_sog_periodic')),
        }),
        ('Counter-soggetto', {
            'classes': ('collapse',),
            'fields': ('mt_csog_voice', ('mt_csog_dur', 'mt_csog_mel')),
        }),
        ('Contrapuntal duo', {
            'classes': ('collapse',),
            'fields': ('mt_cd_voice1', 'mt_cd_voice2'),
        }),
        ('Fuga', {
            'classes': ('collapse',),
            'fields': ('mt_fg_voice1', 'mt_fg_voice2',
                       'mt_fg_voice3', 'mt_fg_voice4',
                       ('mt_fg_periodic', 'mt_fg_strict',
                        'mt_fg_flexed'), ('mt_fg_sequential',
                                          'mt_fg_inverted', 'mt_fg_retrograde'),
                       'mt_fg_int', 'mt_fg_tint'),
        }),
        ('Imitative duo', {
            'classes': ('collapse',),
            'fields': ('mt_id_voice1', 'mt_id_voice2',
                       'mt_id_voice3', 'mt_id_voice4',
                       ('mt_id_strict', 'mt_id_flexed',
                        'mt_id_flt'), ('mt_id_sequential',
                                       'mt_id_added', 'mt_id_invertible'),
                       'mt_id_int', 'mt_id_tint'),
        }),
        ('Periodic entry', {
            'classes': ('collapse',),
            'fields': ('mt_pe_voice1', 'mt_pe_voice2', 'mt_pe_voice3',
                       ('mt_pe_strict', 'mt_pe_flexed', 'mt_pe_flt'),
                       ('mt_pe_sequential', 'mt_pe_added',
                        'mt_pe_invertible'), 'mt_pe_int',
                       'mt_pe_tint'),
        }),
        ('Non-imitative duo', {
            'classes': ('collapse',),
            'fields': ('mt_nid_voice1', 'mt_nid_voice2', 'mt_nid_voice3',
                       ('mt_nid_strict', 'mt_nid_flexed', 'mt_nid_flt',
                        'mt_nid_sequential', 'mt_nid_invertible'),
                       'mt_nid_int', 'mt_nid_tint'),
        }),
        ('Homorhythm', {
            'classes': ('collapse',),
            'fields': ('mt_hr_voice1', 'mt_hr_voice2', 'mt_hr_voice3',
                       ('mt_hr_simple', 'mt_hr_staggered',
                        'mt_hr_sequential', 'mt_hr_fauxbourdon')),
        }),
        ('Cadence', {
            'classes': ('collapse',),
            'fields': ('mt_cad_voice1', 'mt_cad_voice2',
                       ('mt_cad_authentic', 'mt_cad_phrygian',
                        'mt_cad_plagal'), 'mt_cad_tone',
                       'mt_cad_dtv', 'mt_cad_dti'),
        }),
        ('Interval pattern', {
            'classes': ('collapse',),
            'fields': ('mt_int_voice1', 'mt_int_voice2',
                       ('mt_int_p6', 'mt_int_p3'),
                       ('mt_int_c35', 'mt_int_c83', 'mt_int_c65')),
        }),
        ('Form and Process', {
            'classes': ('collapse',),
            'fields': ('mt_fp_comment', 'mt_fp_ir', 'mt_fp_range'),
        }),
        ('Other', {
            'fields': ('remarks', 'needs_review'),
        }),
    )
    list_display = (
        'observer',
        'piece',
        'created',
        'updated',
        'needs_review',
    )
    ordering = (
        'piece__piece_id',
        'created',
    )


class CRIMRelationshipAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('observer', 'model_observation', 'derivative_observation'),
        }),
        ('Quotation', {
            'fields': ('rt_q', ('rt_q_exact', 'rt_q_monnayage')),
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
            'fields': ('remarks', 'needs_review'),
        }),
    )
    list_display = (
        'observer',
        'model_observation',
        'derivative_observation',
        'created',
        'updated',
        'needs_review',
    )
    ordering = (
        'model_observation__piece__piece_id',
        'derivative_observation__piece__piece_id',
        'created',
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

admin.site.register(CRIMRole, CRIMRoleAdmin)
admin.site.register(CRIMObservation, CRIMObservationAdmin)
admin.site.register(CRIMRelationship, CRIMRelationshipAdmin)

admin.site.register(CRIMGenre, CRIMGenreAdmin)
admin.site.register(CRIMRoleType, CRIMRoleTypeAdmin)

admin.site.register(CRIMNote)
admin.site.register(CRIMComment)
