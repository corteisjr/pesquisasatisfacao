from django.db import models
from django.urls import reverse


class Person(models.Model):
    cdalterdata = models.IntegerField('Cód. Alterdata', db_index=True)
    name = models.CharField('Nome', max_length=100)
    #email = models.EmailField(null=True, blank=True)
    phone = models.CharField('Telefone', max_length=11, null=True, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'

    def __str__(self):
        return self.name

    def to_dict_json(self):
        return {
            'cdalterdata': self.cdalterdata,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            # 'gender': self.get_gender_display(),
        }

    # def get_absolute_url(self):
    #     return reverse('pesquisa_alter:add_pesquisa', args=[str(self.id)])
#-----------------------------------------------------------------------------------------


class PersonEmail(models.Model):
    person = models.ForeignKey(
        'core.person', related_name='Pessoa', on_delete=models.CASCADE)
    email = models.EmailField(null=False, blank=False)

    class Meta:
        ordering = ('email',)
        verbose_name = 'Email da Pessoa'
        verbose_name_plural = 'Emails das Pessoas'

    def __str__(self):
        return self.email

#-----------------------------------------------------------------------------------------


class Client(Person):
    last_search = models.CharField('Última pesquisa.', max_length=11, null=True, blank=True)
    created_on = models.DateField(
        'Criado em.',
        auto_now_add=True,
        auto_now=False
    )


    class Meta:
        ordering = ('name',)
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def get_absolute_url(self):
        return reverse('person_client_detail', args=[str(self.pk)])


class Question(models.Model):
    LEVEL_CHOICES = (
        ('0', 'Dependencia'),
        ('1', 'Confianca'),
        ('2', 'Comprometimento'),
        ('3', 'Preditiva'),
    )
    question = models.CharField('Pergunta', max_length=200)
    level = models.CharField('Nível', max_length=15,
                             choices=LEVEL_CHOICES, default='0')

    class Meta:
        verbose_name = 'Questão'
        verbose_name_plural = 'Questões'
        ordering = ('-level',)

    def __str__(self):
        return self.question


class SearchManager(models.Manager):

    def add_question(self, search_key, person, researched, question):
        search, created = self.get_or_create(
            search_key=search_key, person=person, researched=researched, question=question)
        if not created:
            search.search_key = search.search_key
            search.person = search.person
            search.question = search.question
            search.researched = search.researched
            search.save()
        return search


class Search(models.Model):
    RESPONSE_CHOICES = (
        ('V', 'Verdadeiro'),
        ('F', 'Falso'),
        ('I', 'Indefinido'),
    )
    search_key = models.CharField(
        'Chave da pesquisa', max_length=200, db_index=False)
    person = models.ForeignKey(
        'core.client', related_name='Cliente', on_delete=models.CASCADE)
    researched = models.CharField('Entrevistado', max_length=200)
    question = models.ForeignKey(
        'core.question', related_name='Pergunta', on_delete=models.CASCADE,)
    response = models.CharField(
        'Resposta', max_length=1, choices=RESPONSE_CHOICES, default='I')
    participation_on = models.DateField(
        'período da pesquisa',
        auto_now_add=True,
        auto_now=False
    )
    created_on = models.DateTimeField(
        'solicitado em',
        auto_now_add=True,
        auto_now=False
    )

    objects = SearchManager()

    class Meta:
        verbose_name = 'Pesquisa'
        verbose_name_plural = 'Pesquisas'
        unique_together = (('search_key', 'person', 'question'),)
        ordering = ('-participation_on',)

    def __str__(self):
        return self.question.question