# Generated by Django 4.0.4 on 2022-08-04 19:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Curso', '0002_alter_cm_curso_duracao_esperada_and_more'),
        ('Ticket', '0005_remove_solicitacaodisciplina_responsavel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitacaodisciplina',
            name='curso_disciplina',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Curso.cm_curso', verbose_name='A qual curso pertence a disciplina'),
        ),
    ]