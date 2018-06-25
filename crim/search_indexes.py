from haystack import indexes
from crim.models.piece import CRIMPiece


class CRIMPieceIndex(indexes.SearchIndex, indexes.Indexable):
    '''This indexes all the CRIMPiece objects. However, it is
    not used in production because we search for CRIMRelationship
    objects instead. It was used as a simpler text case and
    is left here in case searching for pieces directly ends
    up being useful.
    '''
    text = indexes.CharField(document=True, use_template=True)
    piece_id = indexes.CharField(model_attr='piece_id')
    title = indexes.CharField(model_attr='title')
    mass_title = indexes.CharField(model_attr='mass__title', null=True)
    composer = indexes.CharField(model_attr='composer__name_sort', faceted=True, null=True)
    genre = indexes.CharField(model_attr='genre__name', faceted=True)
    date = indexes.IntegerField(model_attr='date_sort', faceted=True, null=True)
    pdf_links = indexes.CharField(model_attr='pdf_links', null=True, indexed=False)
    mei_links = indexes.CharField(model_attr='mei_links', null=True, indexed=False)
    remarks = indexes.CharField(model_attr='remarks', null=True, indexed=False)

    def get_model(self):
        return CRIMPiece
