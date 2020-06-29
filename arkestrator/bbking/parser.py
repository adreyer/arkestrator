from django.conf import settings

import io

import ply.yacc as yacc

from . import tags
from .lexer import tokens
from . import errors

def validate_tag_name(name):
    import bbking

    try:
        bbking.tags.get_tag(name.lower())
        return True
    except bbking.errors.TagDoesNotExist:
        return False

def flatten(items):
    if not isinstance(items, list):
        return items
    flattened = []
    for item in items:
        if isinstance(item, list):
            flattened += flatten(item)
        else:
            flattened.append(item)
    return flattened

def raw(item):
    return getattr(item, 'raw', getattr(item, 'value', item))

class Text(object):
    def __init__(self, value=""):
        self.value = value
        self.raw = value

class OpenTag(object):
    def __init__(self, name, raw, arg=None, **kwargs):
        self.name = name.lower()
        self.raw = raw
        self.arg = arg
        self.kwargs = kwargs

class Args(object):
    def __init__(self, args, raw):
        self.args = args
        self.raw = raw

    def add_arg(self, arg, raw):
        self.args[arg.key] = arg.value
        self.raw += raw
        return self

class Arg(object):
    def __init__(self, key, value, raw):
        self.key = key
        self.value = value
        self.raw = raw

class CloseTag(object):
    def __init__(self, name, raw):
        self.name = name.lower()
        self.raw = raw

class Tagged(object):
    def __init__(self, open_tag, contents, close_tag, raw):
        self.name = open_tag.name.lower()
        self.contents = contents
        self.arg = open_tag.arg
        self.kwargs = open_tag.kwargs
        self.raw = raw

class Block(object):
    def __init__(self, *contents):
        self.contents = []
        for item in contents:
            if isinstance(item, Block):
                if not self.contents:
                    self.contents = item.contents
                else:
                    self.contents.extend(item.contents)
            else:
                self.contents.append(item)

    @property
    def raw(self):
        return "".join(raw(item) for item in self.contents)

    def compress(self):
        compressed = []
        sio = None
        for item in self.contents:
            if isinstance(item, Tagged):
                if sio:
                    compressed.append(sio.getvalue())
                    sio = None
                compressed.append(item)
            else:
                if not sio:
                    sio = io.StringIO()
                sio.write(raw(item))
        if sio:
            compressed.append(sio.getvalue())

        return compressed

def p_main(p):
    '''main : content'''
    p[0] = p[1].compress()

def p_content(p):
    '''content : content tagged
               | content untagged
               | empty
    '''
    if len(p) == 3:
        p[0] = Block(p[1], p[2])
    else:
        p[0] = Block()

def p_tagged(p):
    '''tagged : opentag content closetag
    '''
    if getattr(p[1],'name',object()) != getattr(p[3],'name',object()):
        p[0] = Block(Text(p[1].raw), p[2], Text(p[3].raw))
        return
    p[0] = Tagged(p[1], p[2].compress(), p[3],
        "".join(raw(item) for item in p[1:]))

def p_untagged(p):
    '''untagged : SYMBOL
                | WHITESPACE
                | MISC
                | RBRACKET
                | EQ
                | SLASH
    '''
    p[0] = Text(p[1])

def p_empty(p):
    'empty :'
    pass

def p_text(p):
    '''text : text term
            | term
    '''
    if len(p) == 3:
        p[0] = Block(p[1],p[2])
    else:
        p[0] = p[1]

def p_term(p):
    '''
       term : WHITESPACE
            | SYMBOL
            | MISC
            | SLASH
            | LBRACKET
            | EQ
    '''
    p[0] = Text(p[1])

def p_text_no_ws(p):
    '''text_no_ws : text_no_ws term_no_ws
            | term_no_ws
    '''
    if len(p) == 3:
        p[0] = Block(p[1], p[2])
    else:
        p[0] = p[1]

def p_term_no_ws(p):
    ''' term_no_ws : SYMBOL
                   | MISC
                   | SLASH
    '''
    p[0] = Text(p[1])

def p_close_tag(p):
    'closetag : LBRACKET SLASH SYMBOL seen_SYMBOL RBRACKET'
    p[0] = CloseTag(p[3], "".join(raw(item) for item in p[1:]))

def p_identify_open_tag(p):
    "seen_SYMBOL : "
    if not validate_tag_name(p[-1]):
        p[0] = p[-1]
        raise SyntaxError
    p[0] = Text("")

def p_simple_tag(p):
    'opentag : LBRACKET SYMBOL seen_SYMBOL RBRACKET'
    p[0] = OpenTag(p[2], "".join(raw(item) for item in p[1:]))

def p_single_arg_tag(p):
    'opentag : LBRACKET SYMBOL seen_SYMBOL EQ text RBRACKET'
    p[0] = OpenTag(p[2], "".join(raw(item) for item in p[1:]), p[5].raw)

def p_multi_arg_tag(p):
    'opentag : LBRACKET SYMBOL WHITESPACE args RBRACKET'
    args = p[4]
    p[0] = OpenTag(p[2], "".join(raw(item) for item in p[1:]),
        **args.args)

def p_tag_args(p):
    '''args : args WHITESPACE arg
            | arg
    '''
    if len(p) == 4:
        p[0] = p[1].add_arg(p[3],"".join(raw(item) for item in p[2:]))
    else:
        p[0] = Args({}, "").add_arg(p[1], p[1].raw)

def p_tag_arg(p):
    'arg  : SYMBOL EQ text_no_ws'
    p[0] = Arg(p[1], p[3].raw, "".join(raw(item) for item in p[1:]))

#Error Handling

def p_malformed_open_tag(p):
    '''malformed_opentag : LBRACKET SYMBOL WHITESPACE RBRACKET
               | LBRACKET MISC RBRACKET
               | LBRACKET SYMBOL WHITESPACE malformed_args RBRACKET
               | LBRACKET RBRACKET
               | LBRACKET error RBRACKET
               | LBRACKET malformed_opentag
    '''
    p[0] = Text("".join(raw(item) for item in p[1:]))

def p_malformed_args(p):
    '''malformed_args : EQ errors
                      | MISC errors
                      | LBRACKET errors
                      | SLASH errors
    '''
    p[0] = Text("".join(raw(item) for item in p[1:]))

def p_malformed_args_symbol(p):
    '''malformed_args : SYMBOL SYMBOL errors
                      | SYMBOL SLASH errors
                      | SYMBOL WHITESPACE errors
                      | SYMBOL MISC errors
                      | SYMBOL LBRACKET errors
    '''
    p[0] = Text("".join(raw(item) for item in p[1:]))

def p_malformed_args_symbol_only(p):
    '''malformed_args : SYMBOL'''
    p[0] = Text(p[1])

def p_malformed_close_tag(p):
    '''malformed_closetag : LBRACKET SLASH errors RBRACKET
    '''
    p[0] = Text("".join(raw(item) for item in p[1:]))

def p_errors(p):
    '''errors : SYMBOL errors error
              | SLASH errors error
              | WHITESPACE errors error
              | EQ errors error
              | MISC errors error
              | LBRACKET errors error
              | error
    '''
    if len(p) == 4:
        p[0] = Block(*p[1:])
    else:
        p[0] = Block()

def p_malformed_tags(p):
    '''untagged : malformed_opentag
                | malformed_closetag
    '''
    p[0] = p[1]

def p_error(p):
    # ignore errors for now simply don't run bbcode if it does not parse
    return Text(p)


outputdir = getattr(settings, 'PARSER_DIR', None)
if outputdir:
    parser = yacc.yacc(debug=0, outputdir=outputdir)
else:
    parser = yacc.yacc(debug=0)

