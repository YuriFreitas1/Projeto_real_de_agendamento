from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime
from .models import Agendamento


class AgendamentoAdminForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()

        data = cleaned_data.get('data')
        hora = cleaned_data.get('hora')
        servico = cleaned_data.get('servico')

        if data and hora:
            data_hora = timezone.make_aware(
                datetime.combine(data, hora)
            )

            if data_hora < timezone.now():
                raise ValidationError(
                    "Não é possível criar agendamento no passado."
                )

        if data and hora and servico:
            conflito = Agendamento.objects.filter(
                data=data,
                hora=hora,
                servico=servico
            ).exclude(pk=self.instance.pk)

            if conflito.exists():
                raise ValidationError(
                    "Já existe um agendamento para esse horário."
                )

        return cleaned_data
