from django.shortcuts import render, redirect
from clientes.models import Cliente
from .models import Agendamento
from .forms import AgendamentoPublicoForm


def criar_agendamento(request):
    if request.method == 'POST':
        form = AgendamentoPublicoForm(request.POST)

        if form.is_valid():
            nome = form.cleaned_data['nome']
            telefone = form.cleaned_data['telefone']
            servico = form.cleaned_data['servico']
            data = form.cleaned_data['data']
            hora = form.cleaned_data['hora']

            cliente, created = Cliente.objects.get_or_create(
                telefone=telefone,
                defaults={'nome': nome}
            )

            Agendamento.objects.create(
                cliente=cliente,
                servico=servico,
                data=data,
                hora=hora
            )

            return redirect('agendamento_sucesso')

    else:
        form = AgendamentoPublicoForm()

    return render(request, 'agendamentos/criar_agendamento.html', {'form': form})
