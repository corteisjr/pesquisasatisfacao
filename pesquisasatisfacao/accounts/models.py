from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class UserInfo(User):
    nomecompleto = models.CharField('Nome Completo', max_length=100, null=False, blank=False)
    base = models.ForeignKey('core.client', null=True, blank=True, related_name="base",
                             on_delete=models.CASCADE, verbose_name="Base ou Representação")
    horario = models.ForeignKey('accounts.horario', null=True, blank=True, related_name="horario",
                                on_delete=models.CASCADE, verbose_name="Escolha seu Horário")

    class Meta:
        verbose_name = 'Perfil de Usuário'
        verbose_name_plural = 'Perfil de Usuários'

    def __str__(self):
        return self.nomecompleto


class Horario(models.Model):
    descricao = models.CharField('Descrição do Horário', max_length=100, null=False, blank=False)
    entrada = models.CharField('Entrada', max_length=5, null=False, blank=False)
    saida_almoco = models.CharField('Saída almoço', max_length=5, null=False, blank=False)
    volta_almoco = models.CharField('Volta almoço', max_length=5, null=False, blank=False)
    saida = models.CharField('Saída', max_length=5, null=False, blank=False)

    class Meta:
        verbose_name = 'Horário de Usuário'
        verbose_name_plural = 'Horário de Usuários'

    def __str__(self):
        return self.descricao
