from django.test import TestCase

# Create your tests here.
# from django.utils import timezone
# from Acesso_Restrito.models import CM_cidade, CM_pais, CM_pessoa
# from Curso.models import CM_curso, FI_fonte_pagadora, FI_orgao_fomento, FI_programa, SI_curso_oferta, SI_curso_situacao, SI_tipo_curso

# class OfertaDataFimSemprePosteriorTesteCase(TestCase):
#     def setUp(self):
#         tipo_curso = SI_tipo_curso.objects.create(nome='Teste')
#         orgao_fomento = FI_orgao_fomento.objects.create(nome='Teste')
#         fonte_pagadora = FI_fonte_pagadora.objects.create(nome='Teste', sigla='Teste', orgao_fomento=orgao_fomento)
#         programa = FI_programa.objects.create(nome='Teste', sigla='Teste', fonte_pagadora=fonte_pagadora)
#         situacao = SI_curso_situacao.objects.create(nome='Teste')
#         cidade = CM_cidade.objects.create(nome_cidade='Teste', uf_cidade='MG')
#         pais = CM_pais.objects.create(nome_pais='Teste')
#         pessoa = CM_pessoa.objects.create(
#             cpf='000.000.000-00',
#             nome='Teste',
#             sexo='O',
#             data_nascimento=(timezone.now()-timezone.timedelta(days=365*18)).date(),
#             cep='00000-000',
#             rua='Teste',
#             numero='0',
#             complemento='Teste',
#             bairro='Teste',
#             cidade=cidade,
#             uf='MG',
#             pais=pais,
#             ddd1 = '(00)',
#             telefone1 = '000000000',
#             ddd2 = '(00)',
#             telefone2 = '000000000',
#             email = 'teste@teste.com',
#         )
#         curso = CM_curso.objects.create(
#             nome='Teste',
#             tipo_curso=tipo_curso,
#             programa=programa,
#             curso_situacao=situacao,
#             coordenador=pessoa,
#             status='A',
#             descricao='Teste',
#             perfil_egresso='Teste'
#         )
#         SI_curso_oferta.objects.create(
#             curso=curso,
#             numero_oferta=1,
#             data_inicio=timezone.now().date(),
#             data_fim=timezone.now().date(),
#             periodos=1,
#             num_vagas=1
#         )

#     def test_data_fim_data_inicio(self):
#         oferta = SI_curso_oferta.objects.last()
#         self.assertEqual(oferta.data_inicio, oferta.data_fim)