from django.db import models


class cliente(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    email = models.CharField(blank= True,max_length=50)
    data_criacao =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
