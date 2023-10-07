from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import TiposExames, PedidosExames, SolicitacaoExame
from datetime import datetime
from django.contrib.messages import constants
from django.contrib import messages

@login_required
def solicitar_exames(request):
    tipos_exames = TiposExames.objects.all()
    if request.method == 'GET':
        return render(request, 'solicitar_exames.html', {'tipos_exames': tipos_exames})
    else:
        exames_id = request.POST.getlist('exames')
        solicitacao_exames = tipos_exames.filter(id__in = exames_id)

        preco_total = 0
        for exame in solicitacao_exames:
            if exame.disponivel:
                preco_total += exame.preco

        return render(request, 'solicitar_exames.html', {'tipos_exames': tipos_exames, 'solicitacao_exames': solicitacao_exames, 'preco_total': preco_total, 'now': datetime.now()})

@login_required
def fechar_pedido(request):
    exames_id = request.POST.getlist('exames')
    solicitacao_exames = TiposExames.objects.filter(id__in=exames_id)

    pedido_exame = PedidosExames(
        usuario = request.user,
        data = datetime.now()
    )

    pedido_exame.save()

    for exame in solicitacao_exames:
        solicitacao_exames_temp = SolicitacaoExame(
            usuario=request.user,
            exame=exame,
            status="E"
        )
        solicitacao_exames_temp.save()
        pedido_exame.exames.add(solicitacao_exames_temp)
        
    pedido_exame.save()

    messages.add_message(request, constants.SUCCESS, 'Pedido de exame concluído com sucesso')
    return redirect('/exames/gerenciar_pedidos/')


@login_required
def gerenciar_pedidos(request):
    pedidos_exames = PedidosExames.objects.filter(usuario = request.user)
    if request.method == 'GET':
        return render(request, 'gerenciar_pedidos.html', {'pedidos_exames': pedidos_exames})


@login_required
def cancelar_pedido(request, pedido_id):
    pedido = PedidosExames.objects.get(id = pedido_id)

    if not pedido.usuario == request.user:
        messages.add_message(request, constants.ERROR, 'Esse pedido não é seu')
        return redirect('/exames/gerenciar_pedidos/')

    pedido.agendado = False
    pedido.save()

    messages.add_message(request, constants.SUCCESS, 'Pedido cancelado com sucesso')
    return redirect('/exames/gerenciar_pedidos/')


@login_required
def gerenciar_exames(request):
    exames = SolicitacaoExame.objects.filter(usuario = request.user)

    return render(request, 'gerenciar_exames.html', {'exames': exames})


@login_required
def permitir_abrir_exame(request, exame_id):
    exame = SolicitacaoExame.objects.get(id = exame_id)
    if not exame.usuario == request.user:
        messages.add_message(request, constants.ERROR, 'O exame não é seu')
        return redirect('/exames/gerenciar_exames/')
    
    if not exame.requer_senha:
        if exame.resultado:
            return redirect(exame.resultado.url)
        else:
            messages.add_message(request, constants.ERROR, 'O exame não possui resultado')
            return redirect('/exames/gerenciar_exames/')

    return redirect(f'/exames/solicitar_senha_exame/{exame_id}')


@login_required
def solicitar_senha_exame(request, exame_id):
    exame = SolicitacaoExame.objects.get(id = exame_id)
    if not exame.usuario == request.user:
        messages.add_message(request, constants.ERROR, 'O exame não é seu')
        return redirect('/exames/gerenciar_exames/')

    if request.method == 'GET':
        return render(request, 'solicitar_senha_exame.html', {'exame': exame})
    else:
        senha = request.POST.get('senha')
        if not exame.senha == senha:
            messages.add_message(request, constants.ERROR, 'Senha incorreta')
            return redirect(f'/exames/solicitar_senha_exame/{exame_id}')
        
        if not exame.resultado:
            messages.add_message(request, constants.ERROR, 'O exame não possui resultado')
            return redirect('/exames/gerenciar_exames/')
        
        return redirect(exame.resultado.url)
