from django.db import models
from django.utils import timezone

ESCOLHA_CURSO = [
    ('Computação', 'Informática'),
    ('Elétrica', 'Eletrotécnica'),
    ('Superior - Computação', 'Superior - Computação'),
    ('Superior - Matemática', 'Superior - Matemática'),
]

class Estudante(models.Model):
    CAMISA = [
        ('P', 'P'),
        ('M', 'M'),
        ('G', 'G'),
    ]

    id = models.AutoField(primary_key=True)
    nome_estudante = models.CharField(max_length=45)
    matricula = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    bolsista_paae = models.BooleanField(default=False)
    curso = models.CharField(max_length=50, choices=ESCOLHA_CURSO)

    # Itens
    deseja_sapato = models.BooleanField(default=False)
    deseja_caderno = models.BooleanField(default=False)
    deseja_garrafa = models.BooleanField(default=False)
    deseja_camisa = models.BooleanField(default=False)
    tamanho_camisa = models.CharField(max_length=2, choices=CAMISA, null=True, blank=True)
    data_entrega_camisa = models.DateField(null=True, blank=True)
    data_entrega_garrafa = models.DateField(null=True, blank=True)
    data_entrega_sapato = models.DateField(null=True, blank=True)
    data_entrega_caderno = models.DateField(null=True, blank=True)

    
    # Novos campos adicionados
    pedido_entregue = models.BooleanField(default=False, verbose_name="Pedido Entregue")
    observacao = models.TextField(blank=True, null=True, verbose_name="Observações")

    # Campos de data
    created = models.DateTimeField(editable=False, blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Estudante, self).save(*args, **kwargs)

    def __str__(self):
        return self.nome_estudante