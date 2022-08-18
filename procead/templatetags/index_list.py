from django import template

register = template.Library()

@register.simple_tag
def index_list():
    menu = (
        {
            'page': 'Curso',
            'url_name': 'curso',
            'color': 'curso',
            'icon': 'curso'
        },
        {
            'page': 'Polo',
            'url_name': 'polo',
            'color': 'polo',
            'icon': 'polo'
        },
        {
            'page': 'Financeiro',
            'url_name': 'financeiro',
            'color': 'financeiro',
            'icon': 'financeiro'
        },
        {
            'page': 'Viagens',
            'url_name': 'viagem',
            'color': 'viagem',
            'icon': 'viagem'
        },
        {
            'page': 'Almoxarifado',
            'url_name': 'almoxarifado',
            'color': 'almoxarifado',
            'icon': 'almoxarifado'
        },
        {
            'page': 'Solicitações',
            'url_name': 'ticket',
            'color': 'ticket',
            'icon': 'ticket'
        },
    )

    menu_odd = [menu[i] for i in range(0, len(menu),2)]
    menu_even = [menu[i+1] for i in range(0, len(menu),2)]

    menu = zip(menu_odd, menu_even)

    return menu