# Generated by Django 2.1.3 on 2019-02-15 17:45

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('core', '0013_auto_20190215_1425'),
    ]

    operations = [
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=100, verbose_name='Descrição do Horário')),
                ('entrada', models.CharField(max_length=5, verbose_name='Entrada')),
                ('saida_almoco', models.CharField(max_length=5, verbose_name='Saída almoço')),
                ('volta_almoco', models.CharField(max_length=5, verbose_name='Volta almoço')),
                ('saida', models.CharField(max_length=5, verbose_name='Saída')),
            ],
            options={
                'verbose_name': 'Horário de Usuário',
                'verbose_name_plural': 'Horário de Usuários',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('nomecompleto', models.CharField(max_length=100, verbose_name='Nome Completo')),
                ('base', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='base', to='core.Client', verbose_name='Base ou Representação')),
            ],
            options={
                'verbose_name': 'Perfil de Usuário',
                'verbose_name_plural': 'Perfil de Usuários',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]