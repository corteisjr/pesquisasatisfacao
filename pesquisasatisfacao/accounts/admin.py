from django.contrib import admin

# Register your models here.
from pesquisasatisfacao.accounts.models import UserInfo, Horario


@admin.register(UserInfo)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    #search_fields = ('cdalterdata', 'name', 'email')


@admin.register(Horario)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    #search_fields = ('cdalterdata', 'name', 'email')