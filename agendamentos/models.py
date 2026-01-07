from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime
from servicos.models import Servico
from clientes.models import Cliente


class Agendamento(models.Model):

    STATUS_CHOICES = (
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
        ('finalizado', 'Finalizado'),
    )

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='agendamentos'
    )

    servico = models.ForeignKey(
        Servico,
        on_delete=models.CASCADE,
        related_name='agendamentos'
    )

    data = models.DateField()
    hora = models.TimeField()
    criado_em = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente'
    )

    class Meta:
        ordering = ['data', 'hora']

    def __str__(self):
        return f'{self.cliente} - {self.servico} - {self.data} {self.hora}'

class Disponibilidade(models.Model):
    data = models.DateField()
    hora = models.TimeField()
    ativo = models.BooleanField(default=True)

    class Meta:
        unique_together = ('data', 'hora')
        ordering = ['data', 'hora']

    def __str__(self):
        return f"{self.data} - {self.hora}"
