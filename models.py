#-*- coding:UTF-8 -*-

from django.contrib.auth.models import User
from django.db import models


# Create your models here.


CHOOSE_CATEGOTIA_CLIENTE = (
    ('institucional', (
            ('interno', 'Interno'),
            ('externo', 'Externo')
        )
    ),
    ('privado', (
            ('fisica', 'Pessoa Física'),
            ('juridica', 'Pessoa Juridica')
        ),
    )
)


CHOOSE_CALENDARIO_STATUS = (
    ('reservado', 'Reservado'),
    ('confirmado', 'Confirmado'),
    ('cancelado', 'Cancelado')
)


class Usuario(models.Model):
    user = models.OneToOneField(User, related_name='usuario')
    profile = models.OneToOneField('Profile', related_name='profile')
    grupo = models.ManyToManyField('Grupo', related_name='grupos_usuarios')

    def __unicode__(self):
        return self.user.get_full_name

    @property
    def is_cliente(self):
        if self.grupo.filter(nome='Cliente').count() == 1:
            return True
        else:
            return False

    @property
    def is_gestor(self):
        if self.grupo.filter(nome='Gestor').count() == 1:
            return True
        else:
            return False

    @property
    def is_contador(self):
        if self.grupo.filter(nome='Contador').count() == 1:
            return True
        else:
            return False


class Grupo(models.Model):
    nome = models.CharField(max_length=50)

    def __unicode__(self):
        return self.nome


class EspacoFisico(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.TextField(null=None, blank=True)
    componente = models.ManyToManyField('Componente', through='EspacoFisico_Componente')
    imagens = models.ManyToManyField('Imagem')


class EspacoFisico_Componente(models.Model):
    componente = models.ForeignKey('Componente')
    espaco_fisico = models.ForeignKey('EspacoFisico')
    observacao = models.TextField(null=True, blank=True)
    valor = models.FloatField()


class Imagem(models.Model):
    imagem = models.ImageField(upload_to='gestorespaco/midias/imagens')
    status = models.BooleanField(default=True)


class Componente(models.Model):
    nome = models.CharField(max_length=100)
    status = models.BooleanField(default=True)


class Calendario(models.Model):
    espaco_fisico = models.ForeignKey('EspacoFisico')
    inicio_at = models.DateTimeField()
    termino_at = models.DateTimeField()
    cliente = models.ForeignKey('Usuario')


class Profile(models.Model):
    documento = models.CharField(max_length=30)
    categoria = models.CharField(max_length=30, choices=CHOOSE_CATEGOTIA_CLIENTE)
    outra_informacao = models.OneToOneField('OutraInformacao', null=True, blank=True)


class OutraInformacao(models.Model):
    endereco = models.TextField(null=True, blank=True)
    cep = models.TextField(max_length=15, null=True, blank=True)
    bairro = models.TextField(max_length=50, null=True, blank=True)
    telefone = models.TextField(max_length=50, null=True, blank=True)


class Reserva(models.Model):
    espaco_fisico = models.ForeignKey('EspacoFisico')
    inicio_at = models.DateTimeField()
    termino_at = models.DateTimeField()
    cliente = models.ForeignKey('Usuario')
    status = models.CharField(max_length=30, choices=CHOOSE_CALENDARIO_STATUS)


class Pagamento(models.Model):
    reserva = models.ForeignKey('Reserva')
    status = models.BooleanField(default=False)

