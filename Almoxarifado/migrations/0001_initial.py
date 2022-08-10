from django.db import migrations, models
import django.db.models.deletion
import procead.validators


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
                ('descricao', models.CharField(max_length=30, unique=True, verbose_name='Descrição')),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('codigo_siga', models.IntegerField(primary_key=True, serialize=False, verbose_name='Codigo')),
                ('descricao', models.CharField(max_length=30)),
                ('unidade', models.CharField(max_length=15)),
                ('tipo_produto', models.CharField(choices=[('C', 'Consumível'), ('P', 'Permanente')], max_length=1, verbose_name='Tipo de Produto')),
                ('quantidade_minima', models.PositiveIntegerField(validators=[procead.validators.validate_positive], verbose_name='Quantidade Mínima')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Almoxarifado.categoria', verbose_name='Categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Saida_Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade_saida', models.PositiveIntegerField(validators=[procead.validators.validate_positive], verbose_name='Quantidade Saída')),
                ('destino', models.TextField(max_length=25)),
                ('data_saida', models.DateTimeField(blank=True, null=True, verbose_name='Data de Saída')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Almoxarifado.produto')),
                ('responsavel', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Acesso_Restrito.cm_pessoa', verbose_name='Responsável')),
            ],
        ),
        migrations.CreateModel(
            name='Estoque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade_estoque', models.PositiveIntegerField(verbose_name='Quantidade em Estoque')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Almoxarifado.produto')),
            ],
        ),
        migrations.CreateModel(
            name='Entrada_Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade_entrada', models.PositiveIntegerField(validators=[procead.validators.validate_positive])),
                ('origem', models.CharField(max_length=25)),
                ('data_entrada', models.DateTimeField(blank=True, null=True, verbose_name='Data de Entrada')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Almoxarifado.produto')),
                ('responsavel', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Acesso_Restrito.cm_pessoa', verbose_name='Responsável')),
            ],
        ),
    ]
