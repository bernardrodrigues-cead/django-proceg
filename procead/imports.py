import requests, json, uuid
from django.db import models

from django.urls import reverse

from django.db.models.functions import Lower

from localflavor.br.models import BRPostalCodeField, BRCPFField, BRCNPJField
from localflavor.br.br_states import STATE_CHOICES

#opcoes para campos sim e não
SN = (
    (1, 'Sim'),
    (0, 'Não'),
)

STATE_CHOICES = list(STATE_CHOICES) + [('00', 'Estrangeiro (Foreign)')]


# def opcoes_pais():
#     """Retorna uma lista de opções contendo todos os países do mundo

#     Returns:
#         _type_: list of tuples (str: nome, str: nome)
#     """
#     OPCOES_PAIS = []
#     api = requests.get('https://servicodados.ibge.gov.br/api/v1/localidades/paises').content
#     api_json = json.loads(api)
#     for pais in api_json:
#         OPCOES_PAIS.append((pais['nome'], pais['nome']))
#     return OPCOES_PAIS