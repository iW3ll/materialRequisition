from django.db import models
from django.utils import timezone

# Defina ESCOLHA_CURSO antes de usá-la no modelo
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

    id_estudante = models.AutoField(primary_key=True)
    nome_estudante = models.CharField(max_length=45)
    matricula = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    bolsista_paae = models.BooleanField(default=False)
    curso = models.CharField(max_length=50, choices=ESCOLHA_CURSO)

    # Itens
    deseja_caderno = models.BooleanField(default=False)
    deseja_garrafa = models.BooleanField(default=False)
    deseja_camisa = models.BooleanField(default=False)  # Campo adicionado
    tamanho_camisa = models.CharField(max_length=2, choices=CAMISA, null=True, blank=True)  # Campo adicionado

    # Campos de data
    created = models.DateTimeField(editable=False, blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """ Override o método save para gerenciar as datas de criação e modificação. """
        if not self.pk:  # Verifica se o objeto ainda não tem um 'pk' (que é o id, o campo chave primária)
            self.created = timezone.now()  # Define o timestamp de criação
        self.modified = timezone.now()  # Atualiza o timestamp de modificação
        return super(Estudante, self).save(*args, **kwargs)

    def __str__(self):
        return self.nome_estudante