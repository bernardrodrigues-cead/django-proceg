from django.urls import path

from Almoxarifado import views

urlpatterns = [
    path('', views.AlmoxarifadoView, name='almoxarifado'),
    path('novo_registro', views.AlmoxarifadoNovoView, name='almoxarifado_novo'),
    path('listar_registro', views.AlmoxarifadoListarView, name='almoxarifado_listar'),
    path('relatorios', views.AlmoxarifadoRelatorioView, name="almoxarifado_relatorio"),
    path('nova_categoria', views.CategoriaCreate, name="nova_categoria"),
    path('editar_categoria/<int:categoria_id>', views.CategoriaUpdate, name="editar_categoria"),
    path('deletar_categoria/<int:categoria_id>', views.CategoriaDelete, name="deletar_categoria"),
    path('categorias', views.CategoriaListView, name="list_categorias"),
    path('categorias/consulta=<str:consulta>', views.CategoriaListView, name="list_categorias"),
    path('novo_produto', views.ProdutoCreate, name="novo_produto"),
    path('editar_produto/<int:codigo_siga>', views.ProdutoUpdate, name="editar_produto"),
    path('produtos', views.ProdutoListView, name="list_produtos"),
    path('produtos/consulta=<str:consulta>', views.ProdutoListView, name="list_produtos"),
    path('produtos_faltantes', views.ProdutoFaltanteListView, name="list_produtos_faltantes"),
    path('produtos_acabaram', views.ProdutoAcabaramListView, name="list_produtos_acabaram"),
    path('entradas', views.EntradaListView, name="list_entradas"),
    path('entradas/consulta=<str:consulta>', views.EntradaListView, name="list_entradas"),
    path('entradas/data=<str:data>', views.EntradaListView, name="list_entradas"),
    
    path('saidas', views.SaidaListView, name="list_saidas"),
    path('saidas/consulta=<str:consulta>', views.SaidaListView, name="list_saidas"),
    path('nova_entrada', views.EntradaCreate, name="nova_entrada"),
    path('nova_saida', views.SaidaCreate, name="nova_saida"),
    path('estoque', views.EstoqueListView, name="estoque"),
    path('estoque/consulta=<str:consulta>', views.EstoqueListView, name="estoque"),

    
]