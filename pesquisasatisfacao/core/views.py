from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView

from pesquisasatisfacao.core.forms import SearchForm, QuestionForm, ClientForm, PersonForm
from pesquisasatisfacao.core.models import Search, Question, Client, Person


def home(request):
    return render(request, 'base.html')

def person_create(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)

        if form.is_valid():
            print('<<<<==== FORM VALIDO ====>>>>')
            new = form.save(commit=False)
            new.save()
            #form.save_m2m()

            return HttpResponseRedirect('/pessoa/listar')
        else:
            print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
            print(form)
            return render(request, 'person_create.html', {'form':form})
    else:
        context = {'form': PersonForm()}
        return render(request, 'person_create.html', context)

def person_list(request):
    persons = Person.objects.all().order_by("cdalterdata")
    return render(request, 'person_list.html', {'persons': persons})


def person_client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)

        if form.is_valid():
            print('<<<<==== FORM VALIDO ====>>>>')
            new = form.save(commit=False)
            new.save()
            #form.save_m2m()

            return HttpResponseRedirect('/cliente/listar')
        else:
            print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
            print(form)
            return render(request, 'person_create.html', {'form':form})
    else:
        context = {'form': ClientForm()}
        return render(request, 'person_create.html', context)

def person_client_list(request):
    clients = Client.objects.select_related('person_ptr').all().order_by("cdalterdata")
    return render(request, 'person_client_list.html', {'clients': clients})


def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)

        if form.is_valid():
            print('<<<<==== FORM VALIDO ====>>>>')
            new = form.save(commit=False)
            new.save()
            #form.save_m2m()

            return HttpResponseRedirect('/perguntas/listar')
        else:
            print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
            print(form)
            return render(request, 'question_create.html', {'form':form})
    else:
        context = {'form': QuestionForm()}
        return render(request, 'question_create.html', context)

def question_list(request):
    questions = Question.objects.all().order_by("question")
    return render(request, 'question_list.html', {'questions': questions})


def person_client_detail(request, pk):
    clients = Client.objects.select_related('person_ptr').filter(person_ptr=pk)
    searchs = Search.objects.select_related('person').filter(person_id=pk).values('search_key', 'researched').distinct()

    context = {
        'clients':clients,
        'searchs':searchs
    }

    print(context)
    return render(request, 'person_client_detail.html', context)


def seach_create(request):
    # person_id = get_object_or_404(Client, person_id=person_id)
    # search_key = get_object_or_404(Client, search_key=search_key)

    template_name = 'seach_create.html'
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            data = dict(
                search_key=form.cleaned_data['search_key'],
                person=form.cleaned_data['person'],
                researched=form.cleaned_data['researched'],
                questions=Question.objects.all(),
            )
            #criar_pesquisa(**data)
            addQuestions(**data)
            # Não usar o método save().
            # form.save()
            #return HttpResponseRedirect('perguntas/listar/')
            return redirect('search_list')
    else:
        form = SearchForm()
    context = {'form': form}
    return render(request, template_name, context)


def addQuestions(**data):
    #person = Person.objects.get(pk=1)
    questions = Question.objects.all()

    for question in questions:
        try:
            Search.objects.get(
                search_key=data['search_key'],
                person=data['person'],
                researched=data['researched'],
                question=question
            )
            print('existe')
        except Search.DoesNotExist:
            Search.objects.get_or_create(
                search_key=data['search_key'],
                person=data['person'],
                researched=data['researched'],
                question=question
            )
            print('Não existe')

    return HttpResponseRedirect('/')


class SearchDetailWiew(TemplateView):
    template_name = 'search.html'

    def get_formset(self, clear=False):
        QuestionsFormSet = modelformset_factory(
            Search, fields=('response',), can_delete=False, extra=0
        )
        if clear:
            formset = QuestionsFormSet(
                queryset = Search.objects.filter(search_key='11/2017')
            )
        else:
            formset = QuestionsFormSet(
                queryset = Search.objects.filter(search_key='11/2017'),
                data=self.request.POST or None
            )

        return formset

    def get_context_data(self, **kwargs):
        context = super(SearchDetailWiew, self).get_context_data(**kwargs)
        context['formset'] = self.get_formset()
        return context

    def post(self, request, *args, **kwargs):
        formset = self.get_formset()
        context = self.get_context_data(**kwargs)
        if formset.is_valid():
            print('Formulário válido!')
            formset.save()
            print('Dados salvos!')
            context['formset'] = self.get_formset(clear=True)
        else:
            print(formset)
        return self.render_to_response(context)


search_list = SearchDetailWiew.as_view()






#
# def criar_pesquisa(**data):
#     # Pegando somente as perguntas
#     questions = data['questions']
#     pesquisas = []
#     for question in questions:
#         obj = Search(
#             search_key=data['search_key'],
#             person=data['person'],
#             researched=data['researched'],
#             question=question
#         )
#         pesquisas.append(obj)
#     Search.objects.bulk_create(pesquisas)
