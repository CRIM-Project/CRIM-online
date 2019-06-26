from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class CRIMRelationship(models.Model):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Relationship'
        verbose_name_plural = 'Relationships'

    observer = models.ForeignKey(
        'CRIMPerson',
        on_delete=models.SET_NULL,
        to_field='person_id',
        null=True,
        db_index=True,
        related_name='relationships',
    )

    model_observation = models.ForeignKey(
        'CRIMObservation',
        on_delete=models.CASCADE,
        db_index=True,
        related_name='observations_as_model',
    )
    derivative_observation = models.ForeignKey(
        'CRIMObservation',
        on_delete=models.CASCADE,
        db_index=True,
        related_name='observations_as_derivative',
    )
    # These next two fields are redundant, but make it easier
    # to access all relationships associated with a piece using
    # a reverse lookup.  Removing these fields will make the
    # piece/xxx/relationship template not work.
    model_piece = models.ForeignKey(
        'CRIMPiece',
        on_delete=models.CASCADE,
        to_field='piece_id',
        db_index=True,
        related_name='relationships_as_model',
    )
    derivative_piece = models.ForeignKey(
        'CRIMPiece',
        on_delete=models.CASCADE,
        to_field='piece_id',
        db_index=True,
        related_name='relationships_as_derivative',
    )

    # These fields provide redundant, easily accessible, human-readable
    # information about relationship type and musical type.
    # They are updated upon saving.
    relationship_type = models.CharField(max_length=128, blank=True)
    musical_type = models.CharField(max_length=128, blank=True)

    rt_q = models.BooleanField('quotation', default=False)
    rt_q_x = models.BooleanField('exact', default=False)
    rt_q_monnayage = models.BooleanField('monnayage', default=False)

    rt_tm = models.BooleanField('mechanical transformation', default=False)
    rt_tm_snd = models.BooleanField('sounding in different voice(s)', default=False)
    rt_tm_minv = models.BooleanField('melodically inverted', default=False)
    rt_tm_retrograde = models.BooleanField('retrograde', default=False)
    rt_tm_ms = models.BooleanField('metrically shifted', default=False)
    rt_tm_transposed = models.BooleanField('transposed', default=False)
    rt_tm_invertible = models.BooleanField('double or invertible counterpoint', default=False)

    rt_tnm = models.BooleanField('non-mechanical transformation', default=False)
    rt_tnm_embellished = models.BooleanField('embellished', default=False)
    rt_tnm_reduced = models.BooleanField('reduced', default=False)
    rt_tnm_amplified = models.BooleanField('amplified', default=False)
    rt_tnm_truncated = models.BooleanField('truncated', default=False)
    rt_tnm_ncs = models.BooleanField('new counter-subject', default=False)
    rt_tnm_ocs = models.BooleanField('old counter-subject shifted', default=False)
    rt_tnm_ocst = models.BooleanField('old counter-subject transposed', default=False)
    rt_tnm_nc = models.BooleanField('new combination', default=False)

    rt_nm = models.BooleanField('new material', default=False)
    rt_om = models.BooleanField('omission', default=False)

    remarks = models.TextField('remarks (supports Markdown)', blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    curated = models.BooleanField('curated', default=False)

    def id_in_brackets(self):
        return '<R' + str(self.id) + '>'
    id_in_brackets.short_description = 'ID'
    id_in_brackets.admin_order_field = 'id'

    def get_absolute_url(self):
        return '/relationships/{0}/'.format(self.pk)

    def __str__(self):
        return '<R{0}> {1}, {2}'.format(
            self.id,
            self.model_observation.piece_id,
            self.derivative_observation.piece_id
        )

    def save(self, *args, **kwargs):
        # Add the model pieces fields based on the observations
        self.model_piece = self.model_observation.piece
        self.derivative_piece = self.derivative_observation.piece

        # Set the parent relationship type field to true if any of the subtypes are
        self.rt_q = bool(self.rt_q_x or self.rt_q_monnayage)
        self.rt_tm = bool(self.rt_tm_snd or self.rt_tm_minv or self.rt_tm_retrograde or self.rt_tm_ms or self.rt_tm_transposed or self.rt_tm_invertible)
        self.rt_tnm = bool(self.rt_tnm_embellished or self.rt_tnm_reduced or self.rt_tnm_amplified or self.rt_tnm_truncated or self.rt_tnm_ncs or self.rt_tnm_ocs or self.rt_tnm_ocst or self.rt_tnm_nc)

        # Fill out the human-readable relationship type field.
        # There's only SUPPOSED to be one, but some data are dirty, so we
        # want to display these gracefully.
        relationship_type_list = []
        if self.rt_q:
            relationship_type_list.append('Quotation')
        if self.rt_tm:
            relationship_type_list.append('Mechanical transformation')
        if self.rt_tnm:
            relationship_type_list.append('Non-mechanical transformation')
        if self.rt_nm:
            relationship_type_list.append('New material')
        if self.rt_om:
            relationship_type_list.append('Omission')
        self.relationship_type = ', '.join(relationship_type_list)

        # For the musical type field, check if both observations use the same
        # musical type; otherwise, use whichever has a musical type if one of
        # them doesn't (e.g. omission), or include them both.
        if not self.model_observation.musical_type and not self.derivative_observation.musical_type:
            pass
        elif self.model_observation.musical_type:
            self.musical_type = self.model_observation.musical_type
        elif self.derivative_observation.musical_type:
            self.musical_type = self.derivative_observation.musical_type
        else:
            self.musical_type = '{0}; {1}'.format(
                self.model_observation.musical_type,
                self.derivative_observation.musical_type,
            )

        # Finalize changes
        super().save()


@receiver(post_save, sender=CRIMRelationship)
def solr_index(sender, instance, created, **kwargs):
    print('Indexing in Solr')
    from django.conf import settings
    import solr
    from solr_index import solr_index_single

    solrconn = solr.SolrConnection(settings.SOLR_SERVER)
    record = solrconn.query("id:{0}".format(instance.id))
    if record:
        # the record already exists, so we'll remove it first.
        print("Deleting {}".format(record.results[0]['id']))
        solrconn.delete(record.results[0]['id'])

    solr_index_single(instance, solrconn)


@receiver(post_delete, sender=CRIMRelationship)
def solr_delete(sender, instance, **kwargs):
    from django.conf import settings
    import solr

    solrconn = solr.SolrConnection(settings.SOLR_SERVER)
    record = solrconn.query("id:{0}".format(instance.id))
    if record:
        # the record already exists, so we'll remove it first.
        print("Deleting {0}".format(record.results[0]['id']))
        solrconn.delete_query('id:{0}'.format(instance.id))
        solrconn.commit()
