# Generated by Django 4.0.4 on 2022-08-23 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Acesso_Restrito', '0002_delete_cm_associa_grupo_permissao'),
    ]

    operations = [
        migrations.AddField(
            model_name='cm_cidade',
            name='latitude',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cm_cidade',
            name='longitude',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]