from haystack.indexes import *
from haystack import site
from mdc3.board.models import Post


class PostIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    creator = CharField(model_attr='creator')

class SubjectIndex(SearchIndex):
    text = CharField(document=True, model_attr='subject')
    creator = CharField(model_attr='creator')

class ThreadIndex(SearchIndex):
    text = CharField(document=True, use_template=True)

#    def get_queryset(self):
#        """Used when the entire index for model is updated."""
#        return Note.objects.all()


#site.register(Post, PostIndex)
