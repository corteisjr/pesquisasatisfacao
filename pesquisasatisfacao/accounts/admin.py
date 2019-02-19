from django.contrib import admin

# Register your models here.
from pesquisasatisfacao.accounts.models import UserInfo, Horario, WorkSchedule, WorkScheduleItem


@admin.register(UserInfo)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    #search_fields = ('cdalterdata', 'name', 'email')


@admin.register(Horario)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__',)


@admin.register(WorkSchedule)
class WorkScheduleAdmin(admin.ModelAdmin):
    list_display = ('__str__',)


@admin.register(WorkScheduleItem)
class WorkScheduleItemAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'day', 'entrance', 'lunch_entrance', 'lunch_out', 'exit')
    search_fields = ('day', 'entrance', 'lunch_entrance', 'lunch_out', 'exit')

