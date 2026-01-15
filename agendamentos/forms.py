from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime
from .models import Agendamento, Servico, Disponibilidade
from datetime import time

# =========================================================
class AgendamentoAdminForm(forms.ModelForm):
    data = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Data'
    )

    hora = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        label='Hora'
    )

    class Meta:
        model = Agendamento
        fields = ('cliente', 'servico', 'status')

    def clean(self):
        cleaned_data = super().clean()
        data = cleaned_data.get('data')
        hora = cleaned_data.get('hora')

        if not data or not hora:
            return cleaned_data

        #  Bloquear agendamento no passado
        data_hora = timezone.make_aware(
            datetime.combine(data, hora)
        )

        if data_hora < timezone.now():
            raise ValidationError(
                "Não é possível criar agendamento no passado."
            )

        #  Bloquear horário duplicado
        conflito = Agendamento.objects.filter(
            disponibilidade__data=data,
            disponibilidade__hora=hora
        ).exclude(pk=self.instance.pk)

        if conflito.exists():
            raise ValidationError(
                "Já existe um agendamento para esse dia e horário."
            )

        return cleaned_data



# ==========================================================
class AgendamentoPublicoForm(forms.Form):
    nome = forms.CharField(label="Nome", max_length=100)
    telefone = forms.CharField(label="Telefone", max_length=20)
    servico = forms.ModelChoiceField(
        queryset=Servico.objects.all(),
        label="Serviço"
    )
    data = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Data"
    )
    hora = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        label="Hora"
    )

    def clean(self):
        cleaned_data = super().clean()
        data = cleaned_data.get('data')
        hora = cleaned_data.get('hora')

        if data and hora:
            existe = Disponibilidade.objects.filter(
                data=data,
                hora=hora,
                ativo=False
            ).exists()

            if existe:
                raise ValidationError(
                    "⚠️ Este horário já está ocupado. Escolha outro."
                )

        return cleaned_data


class GerarDisponibilidadeForm(forms.Form):
    data = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Data'
    )

    hora_inicio = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        label='Hora inicial'
    )

    hora_fim = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        label='Hora final'
    )

    intervalo = forms.IntegerField(
        min_value=5,
        label='Intervalo (minutos)'
    )

    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get('hora_inicio')
        fim = cleaned_data.get('hora_fim')

        if inicio and fim and inicio >= fim:
            raise ValidationError(
                "A hora final deve ser maior que a hora inicial."
            )

        return cleaned_data
