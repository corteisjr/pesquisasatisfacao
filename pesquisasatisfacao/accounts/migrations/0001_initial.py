# Generated by Django 2.1.3 on 2019-03-09 15:13

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('core', '0013_auto_20190215_1425'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Feriado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100, verbose_name='Descrição do Dia.')),
                ('date', models.DateField(verbose_name='Data')),
                ('abbreviated_date', models.CharField(blank=True, max_length=5, null=True, verbose_name='Dia/Mês dd/mm')),
                ('permanent', models.BooleanField(verbose_name='Feriado fixo')),
                ('kind', models.CharField(choices=[('7', 'Feriado'), ('9', 'Compensação')], max_length=1, verbose_name='Tipo de data')),
            ],
            options={
                'verbose_name': 'Feriado',
                'verbose_name_plural': 'Feriados',
            },
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100, verbose_name='Descrição do Horário.')),
                ('entrance', models.TimeField(max_length=5, verbose_name='Entrada')),
                ('lunch_entrance', models.TimeField(max_length=5, verbose_name='Saída almoço')),
                ('lunch_out', models.TimeField(max_length=5, verbose_name='Volta almoço')),
                ('exit', models.TimeField(max_length=5, verbose_name='Saída')),
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
                ('funcao', models.CharField(max_length=50, verbose_name='Função')),
                ('base', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='base', to='core.Client', verbose_name='Base ou Representação')),
                ('horario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horario', to='accounts.Horario', verbose_name='Escolha seu Horário')),
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
        migrations.CreateModel(
            name='WorkSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.CharField(max_length=7, verbose_name='Período')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Solicitado em')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Usuário', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Ficha de Visita',
                'verbose_name_plural': 'Fichas de Visita',
                'ordering': ('created_on',),
            },
        ),
        migrations.CreateModel(
            name='WorkScheduleItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField(verbose_name='Dt. Agenda')),
                ('week_day', models.CharField(choices=[('6', 'Domingo'), ('0', 'Segunda'), ('1', 'Terça'), ('2', 'Quarta'), ('3', 'Quinta'), ('4', 'Sexta'), ('5', 'Sábado'), ('7', 'Feriado'), ('8', 'Faltou'), ('9', 'Compensação')], max_length=1, verbose_name='Dia Semana')),
                ('entrance', models.TimeField(blank=True, max_length=5, null=True, verbose_name='Entrada')),
                ('lunch_entrance', models.TimeField(blank=True, max_length=5, null=True, verbose_name='Saída almoço')),
                ('lunch_out', models.TimeField(blank=True, max_length=5, null=True, verbose_name='Volta almoço')),
                ('exit', models.TimeField(blank=True, max_length=5, null=True, verbose_name='Saída')),
                ('workschedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='children', to='accounts.WorkSchedule', verbose_name='Ficha')),
            ],
            options={
                'verbose_name': 'Ficha de Visita Detalhe',
                'verbose_name_plural': 'Fichas de Visita Detalhe',
            },
        ),
        migrations.AlterUniqueTogether(
            name='workscheduleitem',
            unique_together={('workschedule', 'day')},
        ),
        migrations.AlterUniqueTogether(
            name='workschedule',
            unique_together={('period', 'user')},
        ),
    ]
