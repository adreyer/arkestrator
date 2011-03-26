from haystack.indexes import RealTimeSearchIndex, CharField
from haystack import site
from mdc3.board.models import Post


class PostIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    creator = CharField(model_attr='creator')

class SubjectIndex(RealTimeSearchIndex):
    text = CharField(document=True, model_attr='subject')
    creator = CharField(model_attr='creator')

class ThreadIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    subject = CharField(model_attr='subject')
    creator = CharField(model_attr='creator')

#    def get_queryset(self):
#        """Used when the entire index for model is updated."""
#        return Note.objects.all()


#site.register(Post, PostIndex)
