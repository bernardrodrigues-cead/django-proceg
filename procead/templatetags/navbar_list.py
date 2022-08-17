from django import template

register = template.Library()

@register.inclusion_tag('base_generic.html')
def navbar_list():
    arroz = [1,2,3]
    return {
        'arroz': arroz,
    }