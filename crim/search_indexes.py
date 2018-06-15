from haystack import indexes
from crim.models.piece import CRIMPiece


class CRIMPieceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    composer = indexes.CharField(use_template=True, faceted=True)
    # author = indexes.CharField(model_attr='user')
    # pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return CRIMPiece
