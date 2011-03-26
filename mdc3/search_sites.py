from haystack import site
from mdc3.board.models import Post, Thread
from mdc3.board.search_indexes import PostIndex, ThreadIndex, SubjectIndex

site.register(Post, PostIndex)
#site.register(Thread, SubjectIndex)
site.register(Thread, ThreadIndex)
