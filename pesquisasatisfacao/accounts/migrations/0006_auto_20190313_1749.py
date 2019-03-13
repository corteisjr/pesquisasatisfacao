# Generated by Django 2.1.3 on 2019-03-13 20:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20190313_1745'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='compensacao',
            name='permanent',
        ),
        migrations.AlterField(
            model_name='compensacao',
            name='users',
            field=models.ManyToManyField(related_name='Users', to=settings.AUTH_USER_MODEL, verbose_name='Usuário'),
        ),
    ]