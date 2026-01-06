from django.contrib import admin
from .models import Agendamento
from .forms import AgendamentoAdminForm

@admin.action(description="Excluir agendamentos selecionados")
def excluir_agendamentos(modeladmin, request, queryset):
    queryset.delete()


@admin.register(Agendamento)
class AgendamentosAdmin(admin.ModelAdmin):
    form = AgendamentoAdminForm
    
    list_display = ('cliente', 'servico', 'data','hora', 'status')
    list_filter = ('status', 'data')
    search_fields = ('cliente__nome', 'servico__nome')
    ordering = ('-data',)
    actions = ['excluir_agendamentos']









