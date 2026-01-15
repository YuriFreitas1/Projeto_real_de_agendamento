from django.shortcuts import render, redirect
from django.contrib import messages
from clientes.models import Cliente
from .models import Agendamento, Disponibilidade
from .forms import AgendamentoPublicoForm
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime, timedelta
from .forms import GerarDisponibilidadeForm
from django.utils import timezone


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

            disponibilidade, created = Disponibilidade.objects.get_or_create(
                data=data,
                hora=hora,
                defaults={'ativo': True}
            )

            agendamento = Agendamento.objects.create(
                cliente=cliente,
                servico=servico,
                disponibilidade=disponibilidade
            )

            request.session['agendamento_id'] = agendamento.id
            request.session['cliente_nome'] = cliente.nome
            request.session['servico_nome'] = servico.nome
            request.session['agendamento_data'] = str(disponibilidade.data)
            request.session['agendamento_hora'] = str(disponibilidade.hora)

            messages.success(request, 'Agendamento criado com sucesso!')

            return redirect('agendamento_sucesso')

    else:
        form = AgendamentoPublicoForm()

    return render(
        request,
        'agendamentos/criar_agendamento.html',
        {'form': form}
    )


def agendamento_sucesso(request):
    if not request.session.get('agendamento_id'):
        return redirect('criar_agendamento')

    context = {
        'agendamento_id': request.session.get('agendamento_id'),
        'cliente_nome': request.session.get('cliente_nome'),
        'servico_nome': request.session.get('servico_nome'),
        'data': request.session.get('agendamento_data'),
        'hora': request.session.get('agendamento_hora'),
    }

    for key in [
        'agendamento_id',
        'cliente_nome',
        'servico_nome',
        'agendamento_data',
        'agendamento_hora'
    ]:
        request.session.pop(key, None)

    return render(
        request,
        'agendamentos/agendamento_sucesso.html',
        context
    )



@staff_member_required
def gerar_disponibilidades(request):
    if request.method == 'POST':
        form = GerarDisponibilidadeForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data['data']
            hora_inicio = form.cleaned_data['hora_inicio']
            hora_fim = form.cleaned_data['hora_fim']
            intervalo = form.cleaned_data['intervalo']

            hora_atual = datetime.combine(data, hora_inicio)
            hora_limite = datetime.combine(data, hora_fim)

            criados = 0

            while hora_atual < hora_limite:
                data_hora = timezone.make_aware(hora_atual)

                if data_hora >= timezone.now():
                    _, created = Disponibilidade.objects.get_or_create(
                        data=data,
                        hora=hora_atual.time(),
                        defaults={'ativo': True}
                    )
                    if created:
                        criados += 1

                hora_atual += timedelta(minutes=intervalo)

            messages.success(
                request,
                f'{criados} horários criados com sucesso.'
            )

    else:
        form = GerarDisponibilidadeForm()

    return render(
        request,
        'agendamentos/gerar_disponibilidades.html',
        {'form': form}
    )
