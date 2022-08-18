from django import template

register = template.Library()

@register.simple_tag
def index_list():
    menu = (
        {
            'page': 'Curso',
            'url_name': 'curso',
            'color': 'curso',
            'icon': 'curso',
            'group': 'Acadêmico'
        },
        {
            'page': 'Polo',
            'url_name': 'polo',
            'color': 'polo',
            'icon': 'polo',
            'group': ''
        },
        {
            'page': 'Financeiro',
            'url_name': 'financeiro',
            'color': 'financeiro',
            'icon': 'financeiro',
            'group': 'Financeiro'
        },
        {
            'page': 'Viagens',
            'url_name': 'viagem',
            'color': 'viagem',
            'icon': 'viagem',
            'group': ''
        },
        {
            'page': 'Almoxarifado',
            'url_name': 'almoxarifado',
            'color': 'almoxarifado',
            'icon': 'almoxarifado',
            'group': ''
        },
        {
            'page': 'Solicitações',
            'url_name': 'ticket',
            'color': 'ticket',
            'icon': 'ticket',
            'group': ''
        },
    )

    menu_odd = [menu[i] for i in range(0, len(menu),2)]
    menu_even = [menu[i+1] for i in range(0, len(menu),2)]

    menu = zip(menu_odd, menu_even)

    return menu