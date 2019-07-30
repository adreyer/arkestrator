from django import template

import bbking

register = template.Library()

class BBCodeNode(template.Node):
    def __init__(self, varname):
        self.varname = template.Variable(varname)

    def render(self, context):
        try:
            compiled = self.varname.resolve(context)
        except template.VariableDoesNotExist:
            return ''

        return compiled.render(context)
        
@register.tag
def bbcode(parser, token):
    try:
        tagname, var = token.contents.split()
    except ValueError:
        raise template.TemplateSyntaxError, "bbcode tag requires one argument"
    return BBCodeNode(var)



