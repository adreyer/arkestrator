import StringIO
import string

from django.template.loader import get_template
from django.conf import settings
from django.template import defaultfilters
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape

from bbking import parser
from bbking.errors import CompilationError, TagDoesNotExist, UnnamedTagException
from bbking.templatetags.wordfilter import wordfilter

DEFAULT_TAG_LIBRARIES = (
    'bbking.bbtags.text',
    'bbking.bbtags.hrefs',
    'bbking.bbtags.quote',
    'bbking.bbtags.code',
)

NON_PRINTING = string.whitespace + \
u'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f \x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xad\u0600\u0601\u0602\u0603\u06dd\u070f\u1680\u17b4\u17b5\u180e\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a\u200b\u200c\u200d\u200e\u200f\u202a\u202b\u202c\u202d\u202e\u202f\u205f\u2060\u2061\u2062\u2063\u2064\u206a\u206b\u206c\u206d\u206e\u206f\u3000\ufeff\ufff9\ufffa\ufffb\U0001d173\U0001d174\U0001d175\U0001d176\U0001d177\U0001d178\U0001d179\U0001d17a\U000e0001\U000e0020\U000e0021\U000e0022\U000e0023\U000e0024\U000e0025\U000e0026\U000e0027\U000e0028\U000e0029\U000e002a\U000e002b\U000e002c\U000e002d\U000e002e\U000e002f\U000e0030\U000e0031\U000e0032\U000e0033\U000e0034\U000e0035\U000e0036\U000e0037\U000e0038\U000e0039\U000e003a\U000e003b\U000e003c\U000e003d\U000e003e\U000e003f\U000e0040\U000e0041\U000e0042\U000e0043\U000e0044\U000e0045\U000e0046\U000e0047\U000e0048\U000e0049\U000e004a\U000e004b\U000e004c\U000e004d\U000e004e\U000e004f\U000e0050\U000e0051\U000e0052\U000e0053\U000e0054\U000e0055\U000e0056\U000e0057\U000e0058\U000e0059\U000e005a\U000e005b\U000e005c\U000e005d\U000e005e\U000e005f\U000e0060\U000e0061\U000e0062\U000e0063\U000e0064\U000e0065\U000e0066\U000e0067\U000e0068\U000e0069\U000e006a\U000e006b\U000e006c\U000e006d\U000e006e\U000e006f\U000e0070\U000e0071\U000e0072\U000e0073\U000e0074\U000e0075\U000e0076\U000e0077\U000e0078\U000e0079\U000e007a\U000e007b\U000e007c\U000e007d\U000e007e\U000e007f'
# How this line was generated:
# NON_PRINTING = u"".join(c for c in map(unichr, xrange(0x110000)) if unicodedata.category(c) in set(['Cc', 'Cf', 'Zs']))
TAG_LIBRARIES = getattr(settings, "BBKING_TAG_LIBRARIES", DEFAULT_TAG_LIBRARIES)

_TAGS = {}

def _load_tags():
    for lib in TAG_LIBRARIES:
        lib_module = __import__(lib, fromlist = ['__all__'])
        for cls_name in lib_module.__all__:
            tag = getattr(lib_module, cls_name)
            _TAGS[tag.tag_name] = tag

def get_tag(name):
    if not _TAGS:
        _load_tags()
    
    if name not in _TAGS:
        raise TagDoesNotExist, "%s is not a valid tag name" % name

    return _TAGS[name]

class BlockTag(object):
    def __init__(self, contents):
        self.contents = contents
        self.length = sum(map(len,contents))

    def render(self, context):
        output = StringIO.StringIO()
        for item in self.contents:
            output.write(item.render(context))
        return mark_safe(output.getvalue())

    @property
    def raw(self):
        return "".join(item.raw for item in self.contents)

    def __len__(self):
        return self.length

class LiteralTag(object):
    def __init__(self, value):
        self.value = value
        self.length = len(self.value.strip(NON_PRINTING))

    def render(self, context):
        if getattr(settings, 'BBKING_USE_WORDFILTERS', False):
            return defaultfilters.linebreaksbr(
                    conditional_escape(wordfilter(self.value)))
        return defaultfilters.linebreaksbr(conditional_escape(self.value))

    @property
    def raw(self):
        return self.value

    def __len__(self):
        return self.length

class BBTag(object):
    
    default_arg = None

    def __init__(self, contents, raw, arg=None, **kwargs):
        if not self.tag_name:
            raise UnnamedTagException

        self.contents = contents
        self.raw = raw
        if arg:
            self.arg = arg
        else:
            self.arg = self.default_arg
        self.kwargs = kwargs

        self.length = len(contents)

    @classmethod
    def get_template(cls):
        template = getattr(cls, 'template', None)
        if not template:
            template = get_template("bbking/tags/%s.html" % cls.tag_name)
            cls.template = template
        return template

    @classmethod
    def usage(cls):
        return ["[%s]Example Text[/%s]"%(cls.tag_name, cls.tag_name)]

    def update_context(self, context):
        pass

    def render(self, context):
        try:
            context.push()
            context['contents'] = self.contents.render(context)
            context['raw_contents'] = self.contents.raw
            context['raw'] = self.raw
            if self.arg:
                context['arg'] = self.arg
            for key,value in self.kwargs.items():
                            context[key] = value
            self.update_context(context)
            return self.get_template().render(context)
        finally:
            context.pop()

    def __len__(self):
        return self.length

def load_tags(contents):
    tags = []

    for item in contents:
        if isinstance(item, parser.Tagged):
            tag = get_tag(item.name)
            children = load_tags(item.contents)
            if item.arg:
                tags.append(tag(children, item.raw, item.arg))
            elif item.kwargs:
                tags.append(tag(children, item.raw, **item.kwargs)) 
            else:
                tags.append(tag(children, item.raw))
        else:
            tags.append(LiteralTag(item))

    if len(tags) == 1:
        return tags[0]

    return BlockTag(tags)
                
def compile(raw):
    parsed = parser.parser.parse(raw)
    if not parsed:
        raise CompilationError

    return load_tags(parsed)
