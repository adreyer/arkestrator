from haystack.indexes import RealTimeSearchIndex, CharField, DateTimeField
from haystack import site
from mdc3.board.models import Post


class PostIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    creator = CharField(model_attr='creator')
    datetime = DateTimeField(model_attr='created_at')

class ThreadIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    creator = CharField(model_attr='creator')
    datetime = DateTimeField()
    creation_date = DateTimeField()

    # TODO: this shit sucks and is could be done without touching 
    # the db most of the time... leave creation date alone and manually
    # update datetime
    def prepare_datetime(self, obj):
        return Post.objects.filter(thread=obj).order_by('-created_at')[0].created_at

    def prepare_creation_date(self,obj):
        return Post.objects.filter(thread=obj).order_by('created_at')[0].created_at
