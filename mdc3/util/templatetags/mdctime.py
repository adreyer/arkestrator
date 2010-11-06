from django.template import Library, Node, Variable, TemplateSyntaxError

register = Library()



time_fmt = { 'short':'%H:%M %p %d-%m-%y',
             'long':'%a, %d-%b-%Y at %H:%M:%S %p',
             'date'  : '%d-%b-%Y',}
class MDCTNode(Node):
    def __init__(self,var_name,fmt_name='long'):
        self.var_name = Variable(var_name)
        self.fmt_name = fmt_name

    def render(self, context):
        dt = self.var_name.resolve(context)
        fmt = time_fmt[self.fmt_name]
        tstring = dt.strftime(fmt)
        return tstring

@register.tag
def mdctime(parser, token):
    args = token.split_contents()[1:]
    if not (len(args) == 1 or len(args) == 2):
        raise TemplateSyntaxError(
            "Usage: {% mdctime datetime [format_name] %}")
    return MDCTNode(args[0], args[1])
