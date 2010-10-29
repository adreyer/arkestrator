import itertools

from django.template import Node, Library, TemplateSyntaxError

register = Library()

class PageNode(Node):
    def __init__(self, var_name):
        self.var_name=var_name

    def render(self, context):
        page_obj = context[self.var_name]
        page_menu="<ul>\n <li class=\"submenulegend\">Page:</li>\n"
        for p in page_obj.paginator.page_range:
            if p == page_obj.number:
                page_menu+="<li class=\"submenuitem\"><a href=\"?page=%d\"><strong>%d</strong></a></li>\n"%(p,p)
            else:
                page_menu+="<li class=\"submenuitem\"><a href=\"?page=%d\">%d</a></li>\n"%(p,p)
        page_menu+="</ul>"
        return page_menu


@register.tag
def pagemenu(parser, token):
    args = token.split_contents()[1:]
    if len(args) != 1:
        raise TemplateSyntaxError("Usage: {% pages page_obj %}")
    return PageNode(args[0])
