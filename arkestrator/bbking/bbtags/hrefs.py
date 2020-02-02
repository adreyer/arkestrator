import re
from urllib.parse import urlparse
from django.utils.safestring import mark_safe

from bbking.tags import BBTag

__all__ = ['BBTagURL', 'BBTagImg', 'BBTagYouTube']

class BBTagURL(BBTag):
    tag_name = 'url'

    def update_context(self, context):
        if self.arg:
            context['url'] = self.arg
        else:
            context['url'] = context['raw_contents']
        context['domain'] = urlparse(context['url'])[1]    
    
    @classmethod
    def usage(cls):
        return [
            '[url=http://example.com/]Example link text[/url]',
            '[url]http://example.com/[/url]',
        ]

class BBTagImg(BBTag):
    tag_name = 'img'

    @classmethod
    def usage(cls):
        return [
            '[img]http://example.com/blam.gif[/img]',
        ]

class BBTagYouTube(BBTag):
    tag_name = 'youtube'

    _video_re = re.compile(r"(v=|http://youtu.be/)([\w-]+)")
    _base_url = 'https://www.youtube.com/embed/%s'

    def update_context(self, context):
        url = context['raw_contents']

        match = self._video_re.search(url)
        if not match:
            context['valid_url'] = False
            return
        
        context['valid_url'] = True
        context['url'] = mark_safe(self._base_url % match.group(2))

    @classmethod
    def usage(cls):
        return [
            '[youtube]http://example.com/blam.gif[/youtube]',
        ]

