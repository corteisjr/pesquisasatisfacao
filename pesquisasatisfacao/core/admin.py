from django.contrib import admin

# Register your models here.
from pesquisasatisfacao.core.models import Client, Search, Question, SearchItem, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'name')
    search_fields = ('id', 'name')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'phone', 'cdalterdata')
    search_fields = ('cdalterdata', 'name', 'city', 'last_search')


@admin.register(Search)
class SearchAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'search_key', 'person', 'researched')
    #search_fields = ('cdalterdata', 'name', 'email', 'last_search')


@admin.register(SearchItem)
class SearchItemAdmin(admin.ModelAdmin):
    list_display = ['search', 'question', 'response']

#DELETE FROM WFISCAL.IV00005


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'question', 'level')
    #search_fields = ('cdalterdata', 'name', 'email', 'last_search')
