from haystack import site
from mdc3.board.models import Post, Thread
from mdc3.board.search_indexes import PostIndex, ThreadIndex
from mdc3.events.models import Event
from mdc3.events.search_indexes import EventIndex

site.register(Post, PostIndex)
site.register(Thread, ThreadIndex)
site.register(Event, EventIndex)
