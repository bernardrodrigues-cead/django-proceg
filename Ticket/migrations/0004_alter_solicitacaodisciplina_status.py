# Generated by Django 4.0.4 on 2022-08-04 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ticket', '0003_remove_solicitacaodisciplina_ano_semestre_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitacaodisciplina',
            name='status',
            field=models.CharField(choices=[('A', 'Aberto'), ('E', 'Em Andamento'), ('P', 'Pendente'), ('F', 'Fechado')], max_length=1),
        ),
    ]
