from haystack.indexes import SearchIndex, CharField, DateTimeField
from haystack import site
from mdc3.events.models import Event


class EventIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    creator = CharField(model_attr='creator')
    datetime = DateTimeField(model_attr='time')
    created_at = DateTimeField(model_attr='created_at')
    market   = CharField()

    def prepare_market(self, obj):
        return Event.market.name
