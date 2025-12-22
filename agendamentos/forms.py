from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime
from .models import Agendamento,Servico


class AgendamentoAdminForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()

        data = cleaned_data.get('data')
        hora = cleaned_data.get('hora')

        if data and hora:
            data_hora = timezone.make_aware(
                datetime.combine(data, hora)
            )

            if data_hora < timezone.now():
                raise ValidationError(
                    "Não é possível criar agendamento no passado."
                )

        if data and hora:
            conflito = Agendamento.objects.filter(
                data=data,
                hora=hora,
            ).exclude(pk=self.instance.pk)

            if conflito.exists():
                raise ValidationError(
                    "Já existe um agendamento para esse dia e horário."
                )

        return cleaned_data
    
#---------------------------------------------------

class AgendamentoPublicoForm(forms.Form):
    nome = forms.CharField(
        label="Nome",
        max_length=100
    )

    telefone = forms.CharField(
        label="Telefone",
        max_length=20
    )

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
