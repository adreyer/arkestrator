import itertools

from django.template import Node, Library, TemplateSyntaxError

register = Library()

class WithCycleNode(Node):
    def __init__(self, vars, var_name, nodelist):
        self.vars = vars
        self.var_name = var_name
        self.nodelist = nodelist

    def render(self, context):
        vars = [v.resolve(context) for v in self.vars]
        context.push()
        context[self.var_name] = self.CycleState(vars)
        result = self.nodelist.render(context)
        context.pop()
        return result

    class CycleState(object):
        def __init__(self, values):
            self.iter = itertools.cycle(values)
            self.next()

        def next(self):
            self.current = self.iter.next()

        def __unicode__(self):
            return self.current

class NextCycleNode(Node):
    def __init__(self, var_name):
        self.var_name = var_name

    def render(self, context):
        try:
            cn = context[self.var_name]
            cn.next()
        except KeyError:
            raise TemplateSyntaxError("cannot find cycle named '%s'" % self.var_name)

        return ""

@register.tag
def withcycle(parser, token):
    args = token.split_contents()[1:]

    if len(args) < 4:
        raise TemplateSyntaxError("Usage: {% withcycle foo bar as var_name %}")

    if args[-2] != 'as':
        raise TemplateSyntaxError("Usage: {% withcycle foo bar as var_name %}")
    
    nodelist = parser.parse(('endwithcycle',))
    parser.delete_first_token()

    vars = [parser.compile_filter(v) for v in args[:-2]]
    return WithCycleNode(vars, args[-1], nodelist)

@register.tag
def nextcycle(parser, token):
    args = token.split_contents()[1:]

    if len(args) != 1:
        raise TemplateSyntaxError("Usage: {% nextcycle var_name %}")

    return NextCycleNode(args[0])

