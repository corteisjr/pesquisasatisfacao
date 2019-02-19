import calendar
import datetime

from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings

# Create your views here.
from pesquisasatisfacao.accounts.forms import RegistrationForm, ScheduleForm, WorkScheduleForm, WorkScheduleItemFormSet
from pesquisasatisfacao.accounts.models import WorkSchedule, WorkScheduleItem


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            print('<<<<==== FORM VALIDO ====>>>>')
            new = form.save(commit=False)
            new.save()
            #form.save_m2m()

            return redirect(settings.LOGIN_URL)
        else:
            print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
            print(form)
            return render(request, 'register.html', {'form': form})
    else:
        context = {'form': RegistrationForm()}
        return render(request, 'register.html', context)


def schedule(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)

        if form.is_valid():
            print('<<<<==== FORM VALIDO ====>>>>')
            new = form.save(commit=False)
            new.save()
            #form.save_m2m()

            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
            print(form)
            return render(request, 'schedule.html', {'form': form})
    else:
        context = {'form': ScheduleForm()}
        return render(request, 'schedule.html', context)


def add_work_schedule_item(period, key):
    year_month = str(period)
    m, y = year_month.split('/')
    first_weekday, num_days_in_month = calendar.monthrange(int(y), int(m))
    work_schedule = get_object_or_404(WorkSchedule, pk=key)

    for day_number in range(1, num_days_in_month + 1):
        # a = str(day_number) + period
        # m, y = a.split('/')
        strdate = datetime.datetime(int(y), int(m), day_number)
        WorkScheduleItem.objects.get_or_create(day=strdate, workschedule=work_schedule)


def work_schedule_create(request):
    # Cria variável na session
    request.session['person_id'] = 1

    if request.method == 'POST':
        form = WorkScheduleForm(request.POST)

        if form.is_valid():
            print('<<<<==== FORM VALIDO ====>>>>')
            new = form.save(commit=False)
            new.save()
            # form.save_m2m()

            return HttpResponseRedirect(new.get_absolute_url())
        else:
            print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
            # person_instance = Person.objects.get(pk=request.session["person_id"])
            return render(request, 'work_schedule_create.html', {'form': form})
    else:
        if 'person_id' in request.session:
            # Recupera variável da session
            pessoa_id = request.session['person_id']
            from datetime import date
            context = {'form': WorkScheduleForm(initial={'user': pessoa_id,
                                                         'period': date.today().strftime('%m/%Y')})}
            # Caso precise preencher mais de um campo no form.
            # context = {'form': SearchForm(initial={'person': pessoa_id, 'search_key': '11-2018'})}

            # Exclui variável da session
            del request.session['person_id']

            return render(request, 'work_schedule_create.html', context)
        else:
            # Caso person_id não exista na session ele redireciona para lista de clientes pesquisados.
            return HttpResponseRedirect('/cliente/listar')


def work_schedule_update(request, pk):
    # Pega a chave da URL acima com (request, pk)
    # joga na variável invoice na linha abaixo passando o modelo MESTRE e os parâmetros que desejo como filtro
    work_schedule = get_object_or_404(WorkSchedule, pk=pk)
    # print(request.method)
    if request.method == 'POST':
        # Os formulários InvoiceForm receberá o request.POST com os campos em branco
        form = WorkScheduleForm(request.POST, instance=work_schedule)
        formset = WorkScheduleItemFormSet(request.POST, instance=work_schedule)

        # Valida os formulários MESTRE(WorkScheduleForm) e DETALHE(WorkScheduleItemFormSet)
        print(form.errors, formset.errors)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
            return redirect('/cliente/listar/')
            # return redirect('/cliente/' + str(search.person.pk) + '/pesquisas')

            # if 'btn_submit_1' in request.POST:
            #     return redirect('/cliente/listar/')
            # else:
            #     return redirect('/cliente/' + str(work_schedule.person.pk) + '/pesquisas')
    else:
        # Caso não seja POST ele trará o formulário com as informações preenchidas do parâmetro invoice
        # que pegamos da URL quando passamos o request de pk na entrada da função acima.
        form = WorkScheduleForm(instance=work_schedule)
        # Recupera a instancia de form e chama a função add_work_schedule_item
        # para popular o detalhe com os dias do mês e o usuário poderá editar.
        add_work_schedule_item(period=work_schedule.period, key=work_schedule.pk)

        formset = WorkScheduleItemFormSet(instance=work_schedule)

    # Passamos os dois forms para uma variável com um nome qualquer (Neste caso usamos o nome "forms" afim de dar
    # a idéia
    # de mais de um formulário conforme abaixo:
    # Na linha context passamos também os dois contextos e
    # por fim na linha final passamos o retorno da função onde chamamos o template com o context.
    forms = [formset.empty_form] + formset.forms
    context = {'form': form, 'formset': formset, 'forms': forms}
    return render(request, 'visita_form.html', context)

