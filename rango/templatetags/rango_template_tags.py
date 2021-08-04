from django import template
from rango.models import Category, Subcategory, Page

register = template.Library()


@register.inclusion_tag("rango/categories.html")
def get_category_list(current_category=None):
    return {"categories": Category.objects.all(),
            "current_category": current_category}

@register.inclusion_tag("rango/search_results.html")
def get_search_results():

    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    pages = Page.objects.all()

    return {"categories": categories,
            "subcategories": subcategories,
            "pages": pages}