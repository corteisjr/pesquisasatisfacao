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


class ClientForm(forms.ModelForm):
    SYSTEM_CHOICES = (
        ('0', 'Pack'),
        ('1', 'Shop'),
        ('2', 'IShop'),
        ('3', 'Immobile'),
        ('4', 'Bimer'),
    )

    representative = forms.ModelChoiceField(queryset=Client.objects.filter(is_representative=True), required=False,
                                            label="Representante (Matriz ou Filial)", )

    # system = forms.MultipleChoiceField(label="Sistema(s)", widget=forms.CheckboxSelectMultiple(), choices=SYSTEM_CHOICES)
    # system = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
    #                                    required=False,
    #                                    choices=SYSTEM_CHOICES)

    # products = forms.ModelMultipleChoiceField(label='Produtos', queryset=Product.objects.all(),
    #                                               widget=FilteredSelectMultiple("Produtos", is_stacked=False,
    #                                                                             attrs={'class': 'material-ignore',
    #                                                                                    'multiple': 'True'}))

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
            'is_representative',
            'representative',
            'last_search',
            'products',
        )

    layout = Layout(
        Fieldset("Cadastro de Pessoa",
                 Row(Span3('cdalterdata'), Span9('name'), ),
                 Row(Span3('is_representative'), Span9('representative'), ),
                 Row(Span4('phone'), Span8('cpf_cnpj')),
                 Row(Span9('email'), Span3('last_search'), ),
                 Row(Span12('products'), ),
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
