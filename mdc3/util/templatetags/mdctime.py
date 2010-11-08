import pytz
from django.conf import settings
from django.template import Library, Node, Variable, TemplateSyntaxError

register = Library()

class MDCTNode(Node):
    def __init__(self,var_name,fmt_name='long',tz_var=None):
        self.var_name = Variable(var_name)
        if tz_var is None:
            self.tz_var = None
        else:
            self.tz_var = Variable(tz_var)
        self.fmt_name = fmt_name

    def render(self, context):
        tz_name = settings.DEFAULT_TZ
        if self.tz_var is None:
            user = Variable('user').resolve(context)
            if user.is_authenticated():
                tz_name = user.get_profile().time_zone
        else:
            tz_name = self.tz_var.resolve(context)
            
        dt = self.var_name.resolve(context)
        
        utc = pytz.timezone('UTC')
        tz = pytz.timezone(tz_name)
        dt = utc.localize(dt)
        dt = dt.astimezone(tz)
        return dt.strftime(settings.TIME_FORMATS[self.fmt_name])

@register.tag
def mdctime(parser, token):
    args = token.split_contents()[1:]
    if args == [] or len(args) > 3 :
        raise TemplateSyntaxError(
            "Usage: {% mdctime datetime_var [format_name] [tz_var] %}")
    if  len(args) == 1:
        return MDCTNode(args[0])
    if len(args) == 2:
        return MDCTNode(args[0], args[1])
    if len(args) == 3:
        return MDCTNode(args[0], args[1], args[2])
