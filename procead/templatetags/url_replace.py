# Reference: https://stackoverflow.com/a/62587351/802542
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.copy()
    print(query)
    query.pop('page', None)
    query.update(kwargs)
    print(query)
    return query.urlencode()