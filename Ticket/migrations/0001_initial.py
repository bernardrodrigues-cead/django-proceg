# Generated by Django 4.0.4 on 2022-08-01 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Acesso_Restrito', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_coordenador', models.BooleanField(default=False, help_text='Marque caso o funcionário seja coordenador do setor', verbose_name='Coordenadoria')),
                ('pessoa', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Acesso_Restrito.cm_pessoa')),
            ],
            options={
                'verbose_name': 'Funcionário',
            },
        ),
        migrations.CreateModel(
            name='Setor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_setor', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Solicitacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_abertura', models.DateTimeField(blank=True, null=True, verbose_name='Data de Abertura')),
                ('anexo', models.ImageField(blank=True, null=True, upload_to='')),
                ('assunto', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('A', 'Em aberto'), ('E', 'Em andamento'), ('F', 'Fechado'), ('P', 'Pendente')], default='A', max_length=1)),
                ('ultima_alteracao', models.DateTimeField(blank=True, null=True, verbose_name='Última alteração')),
                ('data_recebimento', models.DateTimeField(blank=True, null=True, verbose_name='Data de Recebimento')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Ticket.categoria')),
                ('executante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='executante', to='Ticket.funcionario')),
                ('solicitante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='Ticket.funcionario', verbose_name='Solicitante')),
            ],
            options={
                'verbose_name': 'Solicitação',
                'verbose_name_plural': 'Solicitações',
            },
        ),
        migrations.CreateModel(
            name='MensagemSolicitacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_mensagem', models.DateTimeField(blank=True, null=True)),
                ('mensagem', models.TextField()),
                ('autor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='Ticket.funcionario')),
                ('solicitacao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='Ticket.solicitacao')),
            ],
            options={
                'verbose_name': 'Mensagem - Solicitção',
                'verbose_name_plural': 'Mensagens - Solicitção',
            },
        ),
        migrations.AddField(
            model_name='funcionario',
            name='setor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Ticket.setor'),
        ),
    ]