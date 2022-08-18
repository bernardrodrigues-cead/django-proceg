# Proceg

## requirements
 
- wkhtmltopdf (binary) /usr/local/bin

## Funcionando
- Todo o menu de Curso
- Todo o menu de Oferta
- Todo o menu de Polo
- Todo o menu de IES
- Todo o menu de Mantenedor
- Todo o menu de Acesso Restrito

## Problema
- Não dá pra excluir campos que têm chaves estrangeiras (restrict)
- Não há tela para criaçao de FI_orgao_de_fomento, FI_fonte_pagadora
- Existem alguns limitantes no código atual no que diz respeito a cidade e estado (internacionalmente falando)
- Corrigir a tela de vincular etapas. Datas vindo errado. Achar outro meio de relacionar. Tudo nessa área tá meio zoado.
- Revisar o passo 2 da ficha UAB.
- Ver todos os arquivos que foram subidos num pedido de viagem
- PDF precisa atualizar

### Próximo passo
- Tela para vínculo de etapas
- Possibilidade de cadastrar novas cidades em todas as telas com CM - Cidade

#### Lista de permissões padrão
- admin.add_logentry
- admin.change_logentry
- admin.delete_logentry
- admin.view_logentryauth.add_group
- auth.add_permission
- auth.add_user
- auth.change_group
- auth.change_permission
- auth.change_user
- auth.delete_group
- auth.delete_permission
- auth.delete_user
- auth.view_group
- auth.view_permission
- auth.view_user
- contenttypes.add_contenttype
- contenttypes.change_contenttype
- contenttypes.delete_contenttype
- contenttypes.view_contenttype
- sessions.add_session
- sessions.change_session
- sessions.delete_session
- sessions.view_session

#### Modelo de permissões para o sistema
procead."action"_"model"

action = add, change, delete ou view
model = Ex.: si_curso_oferta, cm_pessoa (sempre minúsculo separado por underscore)

Ex.: add_si_curso_oferta, delete_cm_pessoa