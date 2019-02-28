import calendar
import datetime

import weasyprint
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings

# Create your views here.
from django.template.loader import render_to_string, get_template
from django.views import View

from pesquisasatisfacao.accounts.forms import RegistrationForm, ScheduleForm, WorkScheduleForm, WorkScheduleItemFormSet
from pesquisasatisfacao.accounts.models import WorkSchedule, WorkScheduleItem
from pesquisasatisfacao.utils import render_to_pdf


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
        strdate = datetime.datetime(int(y), int(m), day_number)
        my_date = calendar.weekday(int(y), int(m), day_number)
        # my_date = calendar.day_name[strdate.weekday()]
        WorkScheduleItem.objects.get_or_create(day=strdate,
                                               week_day=my_date,
                                               workschedule=work_schedule,
                                               entrance='09:00',
                                               lunch_entrance='12:00',
                                               lunch_out='13:00',
                                               exit='18:00')


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


def admin_receipt_pdf(request, id=id):
    work_schedule = WorkSchedule.objects.select_related('user__userinfo').get(id=id)
    work_schedule_itens = WorkScheduleItem.objects.select_related('workschedule').filter(workschedule_id=id)\
        .order_by('day')

    print(work_schedule_itens.query)

    context = {
        'work_schedule': work_schedule,
        'work_schedule_itens': work_schedule_itens
    }

    html = render_to_string('schedule_report.html', context)
    response = HttpResponse(content_type='recibo/pdf')
    response['Content-Disposition'] = 'filename="recibo_{}.pdf"'.format(work_schedule.id)
    weasyprint.HTML(string=html,
                    base_url=request.build_absolute_uri()).write_pdf(response,
                                                                     stylesheets=[weasyprint.CSS(settings.STATIC_ROOT +
                                                                                                 '/css/pdf.css')])
    return response


class GeneratePDF(View):
    def get(self, request, id, *args, **kwargs):
        template = get_template('schedule_report.html')

        work_schedule = WorkSchedule.objects.get(id=id)
        work_schedule_item = WorkScheduleItem.objects.filter(workschedule_id=id)

        from django.db import connection
        print(connection.queries.work_schedule_item)

        context = {
            'work_schedule': work_schedule,
            'work_schedule_item': work_schedule_item
        }

        html = template.render(context)
        pdf = render_to_pdf('schedule_report.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" % "12341231"
            content = "inline; filename='%s'" % filename
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % filename
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


def work_schedule_list(request):
    q = request.GET.get('searchInput')
    if q:
        work_schedules = WorkSchedule.objects.filter(Q(user__icontains=q) | Q(period__icontains=q))
    else:
        work_schedules = WorkSchedule.objects.all()
    context = {'work_schedules': work_schedules}
    return render(request, 'schedule_list.html', context)
