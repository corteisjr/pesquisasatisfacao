from django.urls import path, include
from material.frontend import urls as frontend_urls

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('', include(frontend_urls)),

    path('pessoa/novo/', views.person_create, name='person_create'),
    path('pessoa/listar/', views.person_list, name='person_list'),

    path('cliente/novo/', views.person_client_create, name='person_client_create'),
    path('cliente/listar/', views.person_client_list, name='person_client_list'),
    path('cliente/<int:pk>/', views.person_client_detail, name='person_client_detail'),

    path('pergunta/nova/', views.question_create, name='question_create'),
    path('perguntas/listar/', views.question_list, name='question_list'),
    path('pesquisa/nova/', views.seach_create, name='seach_create'),
    path('pesquisa/listar/', views.search_list, name='search_list'),
]