import itertools
from django.core.cache import cache
from django.template import Library
from django.template import Node, TemplateSyntaxError, Variable

register = Library()


page_offsets = [-20,-15,-10,-7,-5,-4,-3,-2,-1,0,1,2,3,4,5,7,10,15,20]

def pick_pages(curr,last):
    page_list = []
    if last <= 20:
        page_list = range(1,last+1)
    else:
        page_list = [curr+off for off in page_offsets
                        if curr+off > 1 and curr+off<last]
        page_list.insert(0,1)
        page_list.append(last)
    return page_list
           

    
class PageNode(Node):
    def __init__(self, var_name):
        self.var= Variable(var_name)

    def render(self, context):
        page_obj = self.var.resolve(context)
        page_menu="<ul>\n <li class=\"submenulegend\">Page:</li>\n"
        additional_query = context.get('paginator_query','')
        curr = page_obj.number
        last = page_obj.paginator.num_pages
        cache_key = "page_menu:%d:%d:%s" %(
                        curr,
                        last,
                        additional_query)
        page_menu = cache.get(cache_key, None)
        if page_menu is None:
            page_menu="<ul>\n <li class=\"submenulegend\">Page:</li>\n"
            if additional_query:
                additional_query += "&amp;"
            for p in pick_pages(page_obj.number,page_obj.paginator.num_pages):
                if p == page_obj.number:
                    page_menu+="<li class=\"submenuitem\"><a href=\"?%spage=%d\"><strong>%d</strong></a></li>\n"%(additional_query,p,p)
                else:
                    page_menu+="<li class=\"submenuitem\"><a href=\"?%spage=%d\">%d</a></li>\n"%(additional_query,p,p)
            page_menu+="</ul>"
            cache.set(cache_key,page_menu)

        return page_menu


@register.tag
def pagemenu(parser, token):
    """ Usage: {% pages page_obj %} 
        
        creates a page_menu for page_obj
    """
    args = token.split_contents()[1:]
    if len(args) != 1:
        raise TemplateSyntaxError("Usage: {% pages page_obj %}")
    return PageNode(args[0])



