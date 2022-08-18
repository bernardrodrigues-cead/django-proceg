from django import template

register = template.Library()

@register.simple_tag
def navbar_list(user):
    menu = (
        {
            'page': 'Curso',
            'url_name': 'curso',
            'path': 'curso',
            'group': 'Acadêmico',
            'dropdown': []
        },
        {
            'page': 'Polo',
            'url_name': 'polo',
            'path': 'polo',
            'group': '',
            'dropdown': []
        },
        {
            'page': 'Financeiro',
            'url_name': 'denied',
            'path': 'financeiro',
            'group': 'Financeiro',
            'dropdown': []
        },
        {
            'page': 'Viagens',
            'url_name': 'viagem',
            'path': 'viagem',
            'group': '',
            'dropdown': []
        },
        {
            'page': 'Almoxarifado',
            'url_name': 'almoxarifado',
            'path': 'almoxarifado',
            'group': '',
            'dropdown': []
        },
        {
            'page': 'Solicitações',
            'url_name': 'ticket',
            'path': 'ticket',
            'group': '',
            'dropdown': []
        },
    )

    groups = [item.name for item in user.groups.all()]

    #TRANSFORMAR A SAÍDA NUM DICIONÁRIO PARA DAR BOM
    return menu