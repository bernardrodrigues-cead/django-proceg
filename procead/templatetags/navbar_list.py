from django import template

register = template.Library()

@register.simple_tag
def navbar_list():
    menu = (
        {
            'page': 'Curso',
            'url_name': 'curso',
            'path': 'curso',
            'dropdown': []
        },
        {
            'page': 'Polo',
            'url_name': 'polo',
            'path': 'polo',
            'dropdown': []
        },
        {
            'page': 'Financeiro',
            'url_name': 'denied',
            'path': 'financeiro',
            'dropdown': []
        },
        {
            'page': 'Viagens',
            'url_name': 'viagem',
            'path': 'viagem',
            'dropdown': []
        },
        {
            'page': 'Almoxarifado',
            'url_name': 'almoxarifado',
            'path': 'almoxarifado',
            'dropdown': []
        },
        {
            'page': 'Solicitações',
            'url_name': 'ticket',
            'path': 'ticket',
            'dropdown': []
        },
    )
    return menu