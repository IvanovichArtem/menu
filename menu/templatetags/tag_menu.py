from django import template
from django.template import RequestContext

from ..models import MenuBar

register = template.Library()


def have_children(query):
    menuChildList = []
    lastItem = ""
    for item in query:
        if str(item.parent) == lastItem:
            menuChildList.append(str(item.parent))
        lastItem = item.title
    return menuChildList


@register.inclusion_tag("menu/menu_pattern.html", takes_context=True)
def show_menu(context=RequestContext, menu_name=""):
    path = (context.request.path).replace("/", "")
    menuQuerySet = MenuBar.objects.filter(
        category__name=menu_name
    ).select_related("parent")
    haveChild = have_children(menuQuerySet)
    return {"menu": menuQuerySet, "haveChild": haveChild, "url_path": path}
