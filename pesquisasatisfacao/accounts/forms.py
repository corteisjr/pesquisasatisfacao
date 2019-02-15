from django import forms
from django.contrib.auth.forms import UserCreationForm
from pesquisasatisfacao.accounts.models import UserInfo, Horario
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
        )

    layout = Layout(
        Fieldset('Faça seu cadastro agora.', 'username',
                 Row('password1', 'password2')),
        Fieldset('Dados Pessoais', 'nomecompleto',
                 Row(Span12('base'),),
                 Row(Span12('horario'), ),
                 ))


class ScheduleForm(forms.ModelForm):

    class Meta:
        model = Horario
        fields = (
            'descricao',
            'entrada',
            'saida_almoco',
            'volta_almoco',
            'saida',
        )

    layout = Layout(
        Fieldset('Registro de horário.', 'descricao',
                 Row('entrada', 'saida_almoco', 'volta_almoco', 'saida')),)
