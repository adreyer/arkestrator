from haystack import site
from arkestrator.board.models import Post, Thread
from arkestrator.board.search_indexes import PostIndex, ThreadIndex
from arkestrator.events.models import Event
from arkestrator.events.search_indexes import EventIndex

site.register(Post, PostIndex)
site.register(Thread, ThreadIndex)
site.register(Event, EventIndex)
