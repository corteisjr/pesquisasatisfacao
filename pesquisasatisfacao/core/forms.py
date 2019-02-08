from django import forms
from material import *

from pesquisasatisfacao.core.models import Client, Question, Search, SearchItem
from django.forms import inlineformset_factory

#
# class PersonForm(forms.ModelForm):
#
#     class Meta:
#         model = Person
#         fields = (
#             'cdalterdata',
#             'name',
#             'phone',
#         )
#
#     layout = Layout(
#         Fieldset("Inclua uma Pessoa",
#                  Row(Span4('cdalterdata'),Span8('name'), ),
#                  Row('phone')
#                  )
#     )


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = (
            'cdalterdata',
            'name',
            'phone',
            'cpf_cnpj',
            'email',
            'sistem',
            'zip_code',
            'public_place',
            'number',
            'neighborhood',
            'city',
            'state',
            'representative',
            'last_search',
        )

    layout = Layout(
        Fieldset("Inclua um Cliente",
                 Row(Span4('cdalterdata'), Span8('representative'), ),
                 Row(Span12('name'), ),
                 Row(Span4('phone'), Span8('cpf_cnpj')),
                 Row(Span9('email'), Span3('last_search'), ),
                 Row(Span12('sistem'), ),
                 ),
        Fieldset('Endereço',
                 Row(Span2('zip_code'), Span8('public_place'), Span2('number')),
                 Row(Span5('neighborhood'), Span5('city'), Span2('state')))
        )


class QuestionForm(forms.ModelForm):

    level = forms.ChoiceField(
        choices=(
            ('0', 'Dependencia'),
            ('1', 'Confianca'),
            ('2', 'Comprometimento'),
            ('3', 'Preditiva'),),

        label='Escolha o nível',

        widget=forms.RadioSelect)

    class Meta:
        model = Question
        fields = (
            'question',
            'level',
        )

    layout = Layout(
        Fieldset("Inclua uma Pergunta",
                 Row('question', ),
                 Row('level')
                 )
    )


class SearchFormCompleto(forms.ModelForm):

    class Meta:
        model = Search
        fields = (
            'search_key',
            'person',
            'researched',
        )


class SearchForm(forms.ModelForm):

    class Meta:
        model = Search
        fields = '__all__'
        exclude = ()

    layout = Layout(
        Fieldset("Responda com Calma.", Row('person', 'search_key'), Row('researched',),))


SearchItemFormSet = inlineformset_factory(Search, SearchItem,
                                          widgets={'question__name': forms.TextInput(attrs={'width': '110%'}), },
                                          exclude=('id',),
                                          can_delete=True,
                                          fields=('question', 'response'), extra=1)
