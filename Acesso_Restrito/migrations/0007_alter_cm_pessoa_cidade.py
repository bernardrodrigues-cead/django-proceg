# Generated by Django 4.0.4 on 2022-08-23 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Acesso_Restrito', '0006_alter_cm_pessoa_documentacao_uf_nascimento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cm_pessoa',
            name='cidade',
            field=models.CharField(max_length=255),
        ),
    ]