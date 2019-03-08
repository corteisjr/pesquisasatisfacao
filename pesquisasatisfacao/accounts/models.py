import calendar
from datetime import date

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse


class UserInfo(User):
    nomecompleto = models.CharField('Nome Completo', max_length=100, null=False, blank=False)
    base = models.ForeignKey('core.client', null=True, blank=True, related_name="base",
                             on_delete=models.CASCADE, verbose_name="Base ou Representação")
    horario = models.ForeignKey('accounts.horario', null=False, blank=False, related_name="horario",
                                on_delete=models.CASCADE, verbose_name="Escolha seu Horário")
    funcao = models.CharField('Função', max_length=50, null=False, blank=False)

    class Meta:
        verbose_name = 'Perfil de Usuário'
        verbose_name_plural = 'Perfil de Usuários'

    def save(self, *args, **kwargs):
        self.nomecompleto = self.nomecompleto.upper()
        self.funcao = self.funcao.upper()

        super(UserInfo, self).save(*args, **kwargs)

    def __str__(self):
        return self.nomecompleto


class Horario(models.Model):
    description = models.CharField('Descrição do Horário.', max_length=100, null=False, blank=False)
    entrance = models.TimeField('Entrada', max_length=5, null=False, blank=False)
    lunch_entrance = models.TimeField('Saída almoço', max_length=5, null=False, blank=False)
    lunch_out = models.TimeField('Volta almoço', max_length=5, null=False, blank=False)
    exit = models.TimeField('Saída', max_length=5, null=False, blank=False)

    class Meta:
        verbose_name = 'Horário de Usuário'
        verbose_name_plural = 'Horário de Usuários'

    def save(self, *args, **kwargs):
        self.description = self.description.upper()

        super(Horario, self).save(*args, **kwargs)

    def __str__(self):
        return self.description


class Feriado(models.Model):
    KIND_CHOICES = (
        ('7', 'Feriado'),
        ('9', 'Compensação'),)

    description = models.CharField('Descrição do Dia.', max_length=100, null=False, blank=False)
    date = models.DateField('Data',)
    abbreviated_date = models.CharField('Dia/Mês dd/mm', max_length=5, null=True, blank=True)
    permanent = models.BooleanField('Feriado fixo',)
    kind = models.CharField('Tipo', max_length=1, choices=KIND_CHOICES)

    class Meta:
        verbose_name = 'Feriado'
        verbose_name_plural = 'Feriados'

    def save(self, *args, **kwargs):
        self.description = self.description.upper()
        self.abbreviated_date = self.date.strftime('%d/%m')
        super(Feriado, self).save(*args, **kwargs)

    def __str__(self):
        return self.description


class WorkSchedule(models.Model):
    period = models.CharField(
        'Período', max_length=7, db_index=False)
    user = models.ForeignKey(
        User, related_name='Usuário', on_delete=models.CASCADE)
    created_on = models.DateTimeField(
        'Solicitado em',
        auto_now_add=True,
        auto_now=False
    )

    class Meta:
        verbose_name = 'Ficha de Visita'
        verbose_name_plural = 'Fichas de Visita'
        unique_together = (('period', 'user'),)
        ordering = ('created_on',)

    def get_absolute_url(self):
        return reverse('accounts:work_schedule_update', args=[str(self.id)])

    def __str__(self):
        return self.period


class WorkScheduleItem(models.Model):
    WEEKDAY_CHOICES = (
        ('6', 'Domingo'),
        ('0', 'Segunda'),
        ('1', 'Terça'),
        ('2', 'Quarta'),
        ('3', 'Quinta'),
        ('4', 'Sexta'),
        ('5', 'Sábado'),
        ('7', 'Feriado'),
        ('8', 'Faltou'),
        ('9', 'Compensação'),
    )

    workschedule = models.ForeignKey("accounts.workschedule", null=False, blank=False, related_name="children",
                                     on_delete=models.CASCADE,
                                     verbose_name="Ficha")
    day = models.DateField('Dt. Agenda', )
    week_day = models.CharField('Dia Semana', max_length=1, choices=WEEKDAY_CHOICES)
    entrance = models.TimeField('Entrada', max_length=5, null=True, blank=True)
    lunch_entrance = models.TimeField('Saída almoço', max_length=5, null=True, blank=True)
    lunch_out = models.TimeField('Volta almoço', max_length=5, null=True, blank=True)
    exit = models.TimeField('Saída', max_length=5, null=True, blank=True)

    class Meta:
        verbose_name = 'Ficha de Visita Detalhe'
        verbose_name_plural = 'Fichas de Visita Detalhe'
        unique_together = (('workschedule', 'day'),)

    @property
    def dia_semana(self):
        my_date = date.self.day
        return calendar.day_name[my_date.weekday()]

    def __str__(self):
        return self.workschedule.period
