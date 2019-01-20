from django.db import models
from django.urls import reverse


class Person(models.Model):
    cdalterdata = models.IntegerField('Cód. Alterdata', db_index=True, unique=True)
    name = models.CharField('Nome', max_length=100)
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



class Client(Person):
    last_search = models.CharField('Última pesquisa.', max_length=11, null=True, blank=True)
    created_on = models.DateField(
        'Criado em.',
        auto_now_add=True,
        auto_now=False
    )

    class Meta:
        ordering = ('created_on',)
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


class Search(models.Model):
    search_key = models.CharField(
        'Período', max_length=200, db_index=False)
    person = models.ForeignKey(
        'core.client', related_name='Cliente', on_delete=models.CASCADE)
    researched = models.CharField('Entrevistado', max_length=200)
    participation_on = models.DateField(
        'Período da pesquisa',
        auto_now_add=True,
        auto_now=False
    )
    created_on = models.DateTimeField(
        'Solicitado em',
        auto_now_add=True,
        auto_now=False
    )

    class Meta:
        verbose_name = 'Pesquisa'
        verbose_name_plural = 'Pesquisas'
        unique_together = (('search_key', 'person'),)
        ordering = ('-participation_on',)

    def get_absolute_url(self):
        return reverse('person_client_detail', args=[str(self.pk)])

    def __str__(self):
        return self.search_key


def post_save_search(sender, instance, created,  **kwargs):
    if created:
        questions = Question.objects.all()
        search = Search.objects.filter(pk=instance.pk)

        print(search)

        lista = []

        # print(worksheet.nrows)
        for question in questions:
            lista.append(
                SearchItem(search_id=instance.pk,
                           question_id=question.pk,
                           response=False,
                           )
            )

        SearchItem.objects.bulk_create(lista)


models.signals.post_save.connect(
    post_save_search, sender=Search, dispatch_uid='post_save_search'
)


class SearchItem(models.Model):
    RESPONSE_CHOICES = (
        ('V', 'Verdadeiro'),
        ('F', 'Falso'),
        ('I', 'Indefinido'),
    )

    search = models.ForeignKey(
        'core.search', related_name='Periodo', on_delete=models.CASCADE, verbose_name="Período da Pesquisa")
    question = models.ForeignKey(
        'core.question', related_name='Pergunta', on_delete=models.CASCADE, verbose_name="Pergunta")
    response = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Pesquisa Detalhe'
        verbose_name_plural = 'Pesquisas Detalhe'
        ordering = ('-question',)

    def __str__(self):
        return self.question.question
