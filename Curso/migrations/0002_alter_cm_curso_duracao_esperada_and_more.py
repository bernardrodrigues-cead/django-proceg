# Generated by Django 4.0.4 on 2022-08-03 19:09

from django.db import migrations, models
import procead.validators


class Migration(migrations.Migration):

    dependencies = [
        ('Curso', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cm_curso',
            name='duracao_esperada',
            field=models.PositiveIntegerField(blank=True, help_text='(meses)', null=True, validators=[procead.validators.validate_positive], verbose_name='Duração esperada'),
        ),
        migrations.AlterField(
            model_name='pr_edital',
            name='hora_inicio',
            field=models.TimeField(verbose_name='Hora de início'),
        ),
        migrations.AlterField(
            model_name='si_associa_curso_oferta_polo',
            name='num_vagas',
            field=models.PositiveIntegerField(validators=[procead.validators.validate_positive], verbose_name='Número de vagas'),
        ),
        migrations.AlterField(
            model_name='si_curso_oferta',
            name='periodos',
            field=models.PositiveIntegerField(validators=[procead.validators.validate_positive], verbose_name='Quantidade de Períodos'),
        ),
    ]
