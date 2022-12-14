# Generated by Django 4.0.4 on 2022-10-13 13:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import procead.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Acesso_Restrito', '0001_initial'),
        ('Polo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CM_curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('sigla', models.CharField(blank=True, max_length=10, null=True)),
                ('departamento', models.CharField(blank=True, max_length=100, null=True)),
                ('unidade', models.CharField(blank=True, max_length=100, null=True)),
                ('duracao_esperada', models.PositiveIntegerField(blank=True, help_text='(meses)', null=True, validators=[procead.validators.validate_positive], verbose_name='Duração esperada')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('telefone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Telefone')),
                ('status', models.CharField(choices=[('a', 'Ativo'), ('i', 'Inativo')], max_length=1)),
                ('descricao', models.TextField(max_length=2000, verbose_name='Descrição/Apresentação')),
                ('perfil_egresso', models.TextField(max_length=2000, verbose_name='Perfil do Egresso')),
                ('coordenador', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Acesso_Restrito.cm_pessoa')),
            ],
            options={
                'verbose_name': 'CM - Curso',
            },
        ),
        migrations.CreateModel(
            name='FI_fonte_pagadora',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('sigla', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'FI - Fonte Pagadora',
                'verbose_name_plural': 'FI - Fontes Pagadoras',
            },
        ),
        migrations.CreateModel(
            name='FI_orgao_fomento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'FI - Orgão de Fomento',
                'verbose_name_plural': 'FI - Orgãos de Fomento',
            },
        ),
        migrations.CreateModel(
            name='PR_associa_vaga_etapa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_final', models.DateField()),
                ('hora_final', models.TimeField(help_text='hh:mm')),
            ],
            options={
                'verbose_name': 'PR - Associa Vaga/Etapa',
                'verbose_name_plural': 'PR - Associa Vaga/Etapa',
            },
        ),
        migrations.CreateModel(
            name='PR_edital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_edital', models.PositiveIntegerField(unique=True, verbose_name='Edital número')),
                ('ano_edital', models.PositiveIntegerField(validators=[procead.validators.validate_edital_year], verbose_name='Ano')),
                ('edital_string', models.CharField(max_length=8)),
                ('multiplas_inscricoes', models.BooleanField(help_text='Este edital permite a inscrição em mais de uma vaga', verbose_name='Múltiplas Inscrições')),
                ('descricao', models.TextField(verbose_name='Descrição')),
                ('data_inicio', models.DateField(verbose_name='Data de início')),
                ('hora_inicio', models.TimeField(verbose_name='Hora de início')),
                ('data_cadastro', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'PR - Edital',
                'verbose_name_plural': 'PR - Editais',
            },
        ),
        migrations.CreateModel(
            name='PR_etapa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'PR - Etapa',
            },
        ),
        migrations.CreateModel(
            name='PR_modalidade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField()),
            ],
            options={
                'verbose_name': 'PR - Modalidade',
            },
        ),
        migrations.CreateModel(
            name='PR_setor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('sigla', models.CharField(max_length=15)),
            ],
            options={
                'verbose_name': 'PR - Setor',
                'verbose_name_plural': 'PR - Setores',
            },
        ),
        migrations.CreateModel(
            name='SI_associa_curso_oferta_polo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_vagas', models.PositiveIntegerField(validators=[procead.validators.validate_positive], verbose_name='Número de vagas')),
            ],
            options={
                'verbose_name': 'SI - Curso-Oferta-Polo',
                'verbose_name_plural': 'SI - Cursos-Ofertas-Polos',
            },
        ),
        migrations.CreateModel(
            name='SI_curso_projeto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=45)),
                ('denominacao_programa', models.CharField(max_length=500)),
                ('sigla_programa', models.CharField(max_length=20)),
                ('denominacao_secretaria', models.CharField(max_length=500)),
                ('sigla_secretaria', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'SI - Curso-Projeto',
                'verbose_name_plural': 'SI - Cursos-Projetos',
            },
        ),
        migrations.CreateModel(
            name='SI_curso_situacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=45)),
            ],
            options={
                'verbose_name': 'SI - Curso Situação',
                'verbose_name_plural': 'SI - Cursos Situação',
            },
        ),
        migrations.CreateModel(
            name='SI_tipo_curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=45)),
            ],
            options={
                'verbose_name': 'SI - Tipo de Curso',
                'verbose_name_plural': 'SI - Tipos de Curso',
            },
        ),
        migrations.CreateModel(
            name='SI_curso_oferta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_oferta', models.PositiveIntegerField(validators=[procead.validators.validate_is_zero_or_positive], verbose_name='Número da Oferta')),
                ('data_inicio', models.DateField(help_text='(Data do SISUAB que possibilita cálculo e geração da planilha)', verbose_name='Data de início')),
                ('data_fim', models.DateField(verbose_name='Data de término prevista')),
                ('periodos', models.PositiveIntegerField(validators=[procead.validators.validate_positive], verbose_name='Quantidade de Períodos')),
                ('num_vagas', models.PositiveIntegerField(default=0, help_text='(Cadastrar através da aba Vincular Oferta/Polo)', validators=[procead.validators.validate_is_zero_or_positive], verbose_name='Número de Vagas')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Curso.cm_curso')),
                ('polos_vinculados', models.ManyToManyField(through='Curso.SI_associa_curso_oferta_polo', to='Polo.cm_polo')),
            ],
            options={
                'verbose_name': 'SI - Curso-Oferta',
                'verbose_name_plural': 'SI - Cursos-Ofertas',
            },
        ),
        migrations.AddField(
            model_name='si_associa_curso_oferta_polo',
            name='oferta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Curso.si_curso_oferta'),
        ),
        migrations.AddField(
            model_name='si_associa_curso_oferta_polo',
            name='polo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Polo.cm_polo'),
        ),
        migrations.CreateModel(
            name='PR_vagas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField()),
                ('vaga_para_polo', models.BooleanField(verbose_name='Esta vaga é referente  um polo')),
                ('edital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Curso.pr_edital')),
                ('etapas', models.ManyToManyField(through='Curso.PR_associa_vaga_etapa', to='Curso.pr_etapa')),
                ('polo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='Polo.cm_polo')),
            ],
            options={
                'verbose_name': 'PR - Vagas',
                'verbose_name_plural': 'PR - Vagas',
            },
        ),
        migrations.AddField(
            model_name='pr_edital',
            name='modalidade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Curso.pr_modalidade'),
        ),
        migrations.AddField(
            model_name='pr_edital',
            name='setor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Curso.pr_setor'),
        ),
        migrations.AddField(
            model_name='pr_edital',
            name='usuario_vinculado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pr_associa_vaga_etapa',
            name='etapa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Curso.pr_etapa'),
        ),
        migrations.AddField(
            model_name='pr_associa_vaga_etapa',
            name='vaga',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Curso.pr_vagas'),
        ),
        migrations.CreateModel(
            name='FI_programa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('sigla', models.CharField(blank=True, max_length=50, null=True)),
                ('fonte_pagadora', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Curso.fi_fonte_pagadora')),
            ],
            options={
                'verbose_name': 'FI - Programa',
            },
        ),
        migrations.AddField(
            model_name='fi_fonte_pagadora',
            name='orgao_fomento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Curso.fi_orgao_fomento'),
        ),
        migrations.AddField(
            model_name='cm_curso',
            name='curso_situacao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Curso.si_curso_situacao', verbose_name='Situação'),
        ),
        migrations.AddField(
            model_name='cm_curso',
            name='programa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Curso.fi_programa'),
        ),
        migrations.AddField(
            model_name='cm_curso',
            name='tipo_curso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Curso.si_tipo_curso', verbose_name='Tipo'),
        ),
    ]
