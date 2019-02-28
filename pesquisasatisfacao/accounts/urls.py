from django.conf.urls import url, include
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.i18n import JavaScriptCatalog

from pesquisasatisfacao.accounts import views
from pesquisasatisfacao.accounts.views import GeneratePDF

app_name = 'accounts'


urlpatterns = [
    path('', include('django.contrib.auth.urls')),

    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('login/', auth_views.auth_login, {'template_name': 'registration/login.html'}, name='login'),

    path('accounts/registro/', views.register, name='register'),
    path('accounts/horario/', views.schedule, name='schedule'),
    path('accounts/ficha/listar/', views.work_schedule_list, name='work_schedule_list'),
    path('accounts/ficha/nova/', views.work_schedule_create, name='work_schedule_create'),
    path('accounts/ficha/<int:pk>/editar/', views.work_schedule_update, name='work_schedule_update'),

    path('<int:id>/', GeneratePDF.as_view(), name='generatepdf'),
    path('<int:id>/pdf/', views.admin_receipt_pdf, name='admin_receipt_pdf'),



    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]
