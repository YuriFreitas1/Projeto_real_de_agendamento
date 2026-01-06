from urllib import request
from django.shortcuts import render, redirect
from clientes.models import Cliente
from .models import Agendamento
from .forms import AgendamentoPublicoForm
from django.contrib import messages


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

            agendamento = Agendamento.objects.create(
                cliente=cliente,
                servico=servico,
                data=data,
                hora=hora
            )

            request.session['agendamento_id'] = agendamento.id
            request.session['cliente_nome'] = cliente.nome
            request.session['servico_nome'] = servico.nome
          

            messages.success(request, 'Agendamento criado com sucesso!')

            return redirect('agendamento_sucesso')

    else:
        form = AgendamentoPublicoForm()

    return render(request, 'agendamentos/criar_agendamento.html', {'form': form})


def agendamento_sucesso(request):

    if not request.session.get('agendamento_id'):
        return redirect('criar_agendamento')

    agendamento_id = request.session.get('agendamento_id')
    cliente_nome = request.session.get('cliente_nome')
    servico_nome = request.session.get('servico_nome')


    context = {
        'agendamento_id': agendamento_id,
        'cliente_nome': cliente_nome,
        'servico_nome': servico_nome,
        }
    
    request.session.pop('agendamento_id', None)
    request.session.pop('cliente_nome', None)
    request.session.pop('servico_nome', None)

    return render(request, 'agendamentos/agendamento_sucesso.html',context)

