from django.contrib import admin

from pesquisasatisfacao.accounts.models import (UserInfo,
                                                Horario,
                                                WorkSchedule,
                                                WorkScheduleItem,
                                                Feriado)


@admin.register(UserInfo)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    # search_fields = ('cdalterdata', 'name', 'email')


@admin.register(Horario)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__',)


@admin.register(WorkSchedule)
class WorkScheduleAdmin(admin.ModelAdmin):
    list_display = ('__str__',)


@admin.register(WorkScheduleItem)
class WorkScheduleItemAdmin(admin.ModelAdmin):
    list_display = ('day', 'entrance', 'lunch_entrance', 'lunch_out', 'exit')
    search_fields = ('day', 'entrance', 'lunch_entrance', 'lunch_out', 'exit')


# @admin.register(Feriado)
# class FeriadoAdmin(admin.ModelAdmin):
#     list_display = ('description', 'date', 'abbreviated_date', 'permanent', 'kind')
#     search_fields = ('description', 'date', 'abbreviated_date', 'permanent', 'kind')

