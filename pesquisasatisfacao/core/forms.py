from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from material import *

from pesquisasatisfacao.core.models import Client, Question, Search, SearchItem, Product
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
SYSTEM_CHOICES = (
    ('0', 'Pack'),
    ('1', 'Shop'),
    ('2', 'IShop'),
    ('3', 'Immobile'),
    ('4', 'Bimer'),
)


class ClientForm(forms.ModelForm):

    representative = forms.ModelChoiceField(queryset=Client.objects.filter(is_representative=True), required=False,
                                            label="Representante (Matriz ou Filial)", )

    class Meta:
        model = Client
        fields = (
            'cdalterdata',
            'name',
            'phone',
            'cpf_cnpj',
            'email',
            'cep',
            'logradouro',
            'numero',
            'bairro',
            'cidade',
            'estado',
            'representative',
            'last_search',
            'products',
        )
        exclude = ('is_representative',)

    layout = Layout(
        Fieldset("Cadastro de Cliente",
                 Row(Span3('cdalterdata'), Span9('name'), ),
                 Row(Span12('representative'), ),
                 Row(Span4('phone'), Span8('cpf_cnpj')),
                 Row(Span9('email'), Span3('last_search'), ),
                 Row(Span12('products'), ),
                 ),
        Fieldset('Endereço',
                 Row(Span2('cep'), Span8('logradouro'), Span2('numero')),
                 Row(Span5('bairro'), Span5('cidade'), Span2('estado')))
        )


class RepresentativeForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = (
            'cdalterdata',
            'name',
            'phone',
            'cpf_cnpj',
            'email',
            'cep',
            'logradouro',
            'numero',
            'bairro',
            'cidade',
            'estado',
            'products',
        )
        exclude = ('representative', 'is_representative', 'last_search',)

    layout = Layout(
        Fieldset("Cadastro de Filial ou Representação",
                 Row(Span3('cdalterdata'), Span9('name'), ),
                 Row(Span4('phone'), Span8('cpf_cnpj')),
                 Row(Span5('email'), Span7('products'), ),
                 ),
        Fieldset('Endereço',
                 Row(Span2('cep'), Span8('logradouro'), Span2('numero')),
                 Row(Span5('bairro'), Span5('cidade'), Span2('estado')))
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
