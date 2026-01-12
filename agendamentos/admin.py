from django.contrib import admin
from .models import Agendamento, Disponibilidade
from .forms import AgendamentoAdminForm


@admin.action(description="Excluir agendamentos selecionados")
def excluir_agendamentos(modeladmin, request, queryset):
    queryset.delete()


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    form = AgendamentoAdminForm

    list_display = ('cliente', 'servico', 'get_data', 'get_hora', 'status')
    list_filter = ('status', 'disponibilidade__data')
    ordering = ('-disponibilidade__data',)

    # REMOVE o campo disponibilidade do admin
    exclude = ('disponibilidade',)

    def get_data(self, obj):
        return obj.disponibilidade.data
    get_data.short_description = 'Data'

    def get_hora(self, obj):
        return obj.disponibilidade.hora
    get_hora.short_description = 'Hora'

    def save_model(self, request, obj, form, change):
        data = form.cleaned_data.get('data')
        hora = form.cleaned_data.get('hora')

        disponibilidade, _ = Disponibilidade.objects.get_or_create(
            data=data,
            hora=hora,
            defaults={'ativo': False}
        )

        disponibilidade.ativo = False
        disponibilidade.save()

        obj.disponibilidade = disponibilidade

        super().save_model(request, obj, form, change)


@admin.register(Disponibilidade)
class DisponibilidadeAdmin(admin.ModelAdmin):
    list_display = ('data', 'hora', 'ativo')
    list_filter = ('data', 'ativo')
