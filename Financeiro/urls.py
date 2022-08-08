from django.urls import path

from Financeiro import views

urlpatterns = [
    path('', views.FinanceiroView, name='financeiro'),
    
    path('fichauab', views.passo1View, name='passo1'),
    path('fichauab/2/<uuid:pessoa_uuid>', views.passo2View, name='passo2'),
    path('fichauab/3/<uuid:pessoa_uuid>', views.passo3View, name='passo3'),
    path('fichauab/4/<uuid:pessoa_uuid>', views.passo4View, name='passo4'),
    path('fichauab/5/<uuid:pessoa_uuid>', views.passo5View, name='passo5'),
    path('fichauab/6/<uuid:pessoa_uuid>', views.passo6View, name='passo6'),
    path('fichauab/imprimir_ficha/<str:file_name>', views.show_pdf, name='imprimir-ficha'),
]