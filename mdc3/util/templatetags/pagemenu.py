import itertools

from django.template import Node, Library, TemplateSyntaxError, Variable

register = Library()


    
class PageNode(Node):
    def __init__(self, var_name):
        self.var= Variable(var_name)

    def render(self, context):
        page_obj = self.var.resolve(context)
        page_menu="<ul>\n <li class=\"submenulegend\">Page:</li>\n"
        additional_query = context.get('paginator_query','')
        if additional_query:
            additional_query += "&amp;"
        for p in page_obj.paginator.page_range:
            if p == page_obj.number:
                page_menu+="<li class=\"submenuitem\"><a href=\"?%spage=%d\"><strong>%d</strong></a></li>\n"%(additional_query,p,p)
            else:
                page_menu+="<li class=\"submenuitem\"><a href=\"?%spage=%d\">%d</a></li>\n"%(additional_query,p,p)
        page_menu+="</ul>"
        return page_menu


@register.tag
def pagemenu(parser, token):
    args = token.split_contents()[1:]
    if len(args) != 1:
        raise TemplateSyntaxError("Usage: {% pages page_obj %}")
    return PageNode(args[0])



