from django.db import models
from django.urls import reverse


class Product(models.Model):
    name = models.CharField('Nome', max_length=100)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('person_client_detail', args=[str(self.pk)])


class Client(models.Model):
    cdalterdata = models.IntegerField('Cód. Alterdata', db_index=True, unique=True)
    name = models.CharField('Nome', max_length=100)
    phone = models.CharField('Telefone', max_length=50, null=True, blank=True)
    cpf_cnpj = models.CharField('CPF/CNPJ', max_length=18, null=True, blank=True)
    email = models.CharField('E-Mail', max_length=50, null=True, blank=False)
    # system = models.CharField('Sistema', max_length=10, null=True, blank=False)
    cep = models.CharField('Cep', max_length=10, null=True, blank=False)
    logradouro = models.CharField('Logradouro', max_length=100)
    numero = models.CharField('Número', max_length=10, null=False, blank=False)
    bairro = models.CharField('Bairro', max_length=50, null=False, blank=False)
    cidade = models.CharField('Cidade', max_length=50, null=False, blank=False)
    estado = models.CharField('Estado', max_length=10, null=False, blank=False)
    is_representative = models.BooleanField('É representante?', default=False)
    representative = models.ForeignKey("self", null=True, blank=True, related_name="children", on_delete=models.CASCADE,
                                       verbose_name="Representante")
    products = models.ManyToManyField('core.product', related_name="products", verbose_name="Produtos")
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

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        self.logradouro = self.logradouro.upper()
        self.bairro = self.bairro.upper()
        self.cidade = self.cidade.upper()
        self.estado = self.estado.upper()

        super(Client, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

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

    def get_absolute_url(self):
        return reverse('question_update', args=[str(self.pk)])


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
        return reverse('pesquisa_update', args=[str(self.pk)])

    # def get_absolute_url(self):
    #     return reverse('catalog:category_list', kwargs={'slug': self.slug})

    def __str__(self):
        return self.search_key


# def post_save_search(sender, instance, created,  **kwargs):
#     if created:
#         questions = Question.objects.all()
#         # search = Search.objects.filter(pk=instance.pk)
#
#         lista = []
#
#         # print(worksheet.nrows)
#         for question in questions:
#             print('search_id=', instance.pk, 'question_id=', question.pk)
#             lista.append(
#                 SearchItem(search_id=instance.pk,
#                            question_id=question.pk,
#                            response=False,
#                            )
#             )
#
#         SearchItem.objects.bulk_create(lista)
#
#
# models.signals.post_save.connect(
#     post_save_search, sender=Search, dispatch_uid='post_save_search'
# )


class SearchItem(models.Model):
    search = models.ForeignKey(
        'core.search', related_name='Periodo', on_delete=models.CASCADE, verbose_name="Período da Pesquisa")
    question = models.ForeignKey(
        'core.question', related_name='Pergunta', on_delete=models.CASCADE, verbose_name="Pergunta")
    response = models.BooleanField('Resposta')

    class Meta:
        verbose_name = 'Pesquisa Detalhe'
        verbose_name_plural = 'Pesquisas Detalhe'
        unique_together = (('search', 'question'),)
        ordering = ('-question',)

    def __str__(self):
        return self.question.question

