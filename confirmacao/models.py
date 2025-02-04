from django.db import models


class ConfirmacaoPresenca(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    acompanhante = models.CharField(max_length=100, blank=True, null=True)
    email_acompanhante = models.EmailField(blank=True, null=True, unique=True)
    mensagem = models.TextField(blank=True, null=True, max_length=125)
    confirmado = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - {'Confirmado' if self.confirmado else 'Não Confirmado'}"
