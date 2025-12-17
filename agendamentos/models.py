from django.db import models
from servicos.models import Servico
from clientes.models import Cliente

class Agendamento(models.Model):

    STATUS_CHOICES = (
        ('pendente','Pendente'),
        ('confirmado','Confirmado'),
        ('cancelado','Cancelado'),
        ('finalizado','Finalizado'),
    )

    cliente = models.ForeignKey(
        Cliente,
        on_delete = models.CASCADE,
        related_name = 'agendamentos'
    )

    servico = models.ForeignKey(
        Servico,
        on_delete=models.CASCADE,
        related_name='agendamentos'
        )
    
    data_hora = models.DateTimeField()
    criado_em = models.DateTimeField(auto_now_add=True)


    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente'
    )

    def __str__(self):
        return f'{self.cliente} - {self.servico} - {self.data_hora}'