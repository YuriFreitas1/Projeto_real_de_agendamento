from django.contrib import admin
from .models import Agendamento

@admin.register(Agendamento)
class AgendamentosAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'servico', 'data_hora', 'status')
    list_filter = ('status', 'data_hora')
    search_fields = ('cliente__nome', 'servico__nome')
    ordering = ('data_hora',)
