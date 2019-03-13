from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory

from pesquisasatisfacao.accounts.models import UserInfo, Horario, WorkSchedule, WorkScheduleItem
from material import *

from pesquisasatisfacao.core.models import Client


class RegistrationForm(forms.Form, UserCreationForm):
    base = forms.ModelChoiceField(queryset=Client.objects.filter(is_representative=True), required=False,
                                  label="Representante (Matriz ou Filial)", )

    class Meta:
        model = UserInfo
        fields = (
            'username',
            'nomecompleto',
            'base',
            'horario',
            'funcao',
        )

    layout = Layout(
        Fieldset('Faça seu cadastro agora.', 'username',
                 Row('password1', 'password2')),
        Fieldset('Dados Pessoais', 'nomecompleto',
                 Row(Span12('base'),),
                 Row(Span12('horario'), ),
                 Row(Span12('funcao'), ),
                 ))


class ScheduleForm(forms.ModelForm):

    class Meta:
        model = Horario
        fields = (
            'description',
            'entrance',
            'lunch_entrance',
            'lunch_out',
            'exit',
        )

    layout = Layout(
        Fieldset('Registro de horário.', 'description',
                 Row('entrance', 'lunch_entrance', 'lunch_out', 'exit')),)


class WorkScheduleForm(forms.ModelForm):

    class Meta:
        model = WorkSchedule
        fields = '__all__'
        exclude = ('user',)

    layout = Layout(
        Fieldset("Preencha com o Período",
                 Row('period'),),)


WorkScheduleItemFormSet = inlineformset_factory(WorkSchedule, WorkScheduleItem,
                                                exclude=('id',),
                                                can_delete=True,
                                                fields=('day', 'week_day', 'entrance', 'lunch_entrance', 'lunch_out', 'exit'),
                                                extra=0)
