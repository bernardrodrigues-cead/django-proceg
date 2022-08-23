# Generated by Django 4.0.4 on 2022-08-23 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Acesso_Restrito', '0004_remove_cm_cidade_latitude_remove_cm_cidade_longitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cm_pessoa_documentacao',
            name='tipo_documento',
            field=models.CharField(choices=[('RG', 'Carteira de Identidade'), ('CNH', 'Carteira de Motorista'), ('CTPS', 'Carteira de Trabalho')], max_length=50, verbose_name='Tipo de Documento'),
        ),
    ]