from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.conf import settings

# Create your views here.
from pesquisasatisfacao.accounts.forms import RegistrationForm, ScheduleForm


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

