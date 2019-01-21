from django import forms
from material import *

from pesquisasatisfacao.core.models import Person, Client, Question, Search, SearchItem
from django.forms import inlineformset_factory


class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = (
            'cdalterdata',
            'name',
            'phone',
        )

    layout = Layout(
        Fieldset("Inclua uma Pessoa",
                 Row(Span4('cdalterdata'),Span8('name'), ),
                 Row('phone')
                 )
    )


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = (
            'cdalterdata',
            'name',
            'phone',
            'last_search',
        )

    layout = Layout(
        Fieldset("Inclua um Cliente",
                 Row(Span4('cdalterdata'), Span8('name'), ),
                 Row(Span4('phone'), Span8('last_search'))
                 )
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
        exclude = ()

    layout = Layout(
        Fieldset("Responda com Calma.", Row('person', 'search_key'), Row('researched'),))


SearchItemFormSet = inlineformset_factory(Search, SearchItem,
                                          widgets={'response': forms.BooleanField(),},
                                          can_delete=True,
                                          fields=('question', 'response'), extra=3)
