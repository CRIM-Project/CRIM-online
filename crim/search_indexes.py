from haystack import indexes
from crim.models.piece import CRIMPiece


class CRIMPieceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    piece_id = indexes.CharField(model_attr='piece_id', faceted=True)
    title = indexes.CharField(model_attr='title', faceted=True)
    mass = indexes.CharField(model_attr='mass__title', faceted=True)
    composer = indexes.CharField(model_attr='composer__name', faceted=True)
    genre = indexes.CharField(model_attr='genre__name', faceted=True)
    date = indexes.IntegerField(model_attr='date_sort', faceted=True)

    def get_model(self):
        return CRIMPiece
