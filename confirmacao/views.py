from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ConfirmacaoPresencaForm
from .models import ConfirmacaoPresenca
from django.core.paginator import Paginator
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def lista_convidados(request):
    convidados_list = ConfirmacaoPresenca.objects.filter(
        confirmado=True
    ).order_by('-criado_em')
    paginator = Paginator(
        convidados_list, 10
    )  # Mostra 10 convidados por página

    page_number = request.GET.get('page')
    convidados = paginator.get_page(page_number)

    return render(
        request,
        'confirmacao/lista_convidados.html',
        {'convidados': convidados},
    )


def confirmar_presenca(request):
    if request.method == 'POST':
        form = ConfirmacaoPresencaForm(request.POST)
        if form.is_valid():
            form.save()

            # Dados do email
            assunto = 'Bem-vindo(a) ao Fabirthday!'

            remetente = settings.EMAIL_HOST_USER

            # Obtém os emails dos usuários preenchidos no formulário
            destinatarios = [form.cleaned_data['email']]

            # Verifica se o email do acompanhante foi preenchido e adiciona à lista de destinatários
            if form.cleaned_data.get('email_acompanhante'):
                destinatarios.append(form.cleaned_data['email_acompanhante'])

                menssagem_fallback = f"""
                Olá, {form.cleaned_data['nome']} e {form.cleaned_data['acompanhante']}! Quero agradecer de coração por confirmar a presença de vocês. 
                Nos vemos no próximo sábado, dia 8, a partir das 17h! 
                Endereço: Av. Maria Rosa, 379, Manaíra.
                """
                menssagem_html = (
                    """
                <!DOCTYPE html>
                <html lang="pt-BR">
                <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Agradecimento pela Confirmação de Presença</title>
                <style>
                    body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f8f8f8;
                    color: #333;
                    }
                    .container {
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    }
                    h1 {
                    text-align: center;
                    color: #ff69b4;
                    }
                    p {
                    font-size: 16px;
                    line-height: 1.5;
                    color: #333;
                    }
                    .highlight {
                    color: #ff69b4;
                    font-weight: bold;
                    }
                    .footer {
                    text-align: center;
                    font-size: 14px;
                    color: #aaa;
                    margin-top: 20px;
                    }
                </style>
                </head>
                """
                    + f"""
                <body>
                <div class="container">
                    <h1>Obrigado pela Confirmação!</h1>
                    <p>Olá, <span class="highlight">{form.cleaned_data['nome']}</span> e <span class="highlight">{form.cleaned_data['acompanhante']}</span>!</p>
                    <p>Quero agradecer de coração por confirmar a presença de vocês na minha festa de aniversário! Estou super feliz que vocês vão estar lá para comemorar comigo esse momento tão especial. Com certeza vai ser inesquecível!</p>
                    <p>Nos vemos no <span class="highlight">próximo sábado, dia 8</span>, a partir das <span class="highlight">17h</span>, para curtirmos uma festa cheia de música pop dos anos 2000, karaoke, drink games e, claro, uma vibe bem rosa! 💖</p>
                    <p>Nos encontramos em: <span class="highlight">Av. Maria Rosa, 379, Manaíra</span>.</p>
                    <p>Vai ser incrível ter vocês lá! Preparem-se para muitos momentos divertidos e inesquecíveis. ✨</p>
                    <div class="footer">
                    <p>Até logo! 🎉</p>
                    </div>
                </div>
                </body>
                </html>
            """
                )

            else:
                menssagem_fallback = f"""
                    Olá, {form.cleaned_data['nome']}! Quero agradecer de coração por confirmar sua presença. 
                    Nos vemos no próximo sábado, dia 8, a partir das 17h! 
                    Endereço: Av. Maria Rosa, 379, Manaíra.
                """
                menssagem_html = (
                    """
                <!DOCTYPE html>
                <html lang="pt-BR">
                <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Agradecimento pela Confirmação de Presença</title>
                <style>
                    body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f8f8f8;
                    color: #333;
                    }
                    .container {
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    }
                    h1 {
                    text-align: center;
                    color: #ff69b4;
                    }
                    p {
                    font-size: 16px;
                    line-height: 1.5;
                    color: #333;
                    }
                    .highlight {
                    color: #ff69b4;
                    font-weight: bold;
                    }
                    .footer {
                    text-align: center;
                    font-size: 14px;
                    color: #aaa;
                    margin-top: 20px;
                    }
                </style>
                </head>
                """
                    + f"""
                <body>
                <div class="container">
                    <h1>Obrigado pela Confirmação!</h1>
                    <p>Oi, <span class="highlight">{form.cleaned_data['nome']}</span>!</p>
                    <p>Quero agradecer de coração por confirmar sua presença na minha festa de aniversário! Estou super feliz que você vai estar lá para comemorar comigo esse momento tão especial. Com certeza vai ser inesquecível!</p>
                    <p>Nos vemos no <span class="highlight">próximo sábado, dia 8</span>, a partir das <span class="highlight">17h</span>, para curtirmos uma festa cheia de música pop dos anos 2000, karaoke, drink games e, claro, uma vibe bem rosa! 💖</p>
                    <p>Nos encontramos em: <span class="highlight">Av. Maria Rosa, 379, Manaíra</span>.</p>
                    <p>Vai ser incrível ter você lá! Prepare-se para muitos momentos divertidos e inesquecíveis. ✨</p>
                    <div class="footer">
                    <p>Até logo! 🎉</p>
                    </div>
                </div>
                </body>
                </html>
                """
                )

            email = EmailMultiAlternatives(
                assunto, menssagem_fallback, remetente, destinatarios
            )

            # Enviar o email
            email.attach_alternative(menssagem_html, 'text/html')
            email.send()

            messages.success(
                request, 'Sua confirmação foi registrada com sucesso!'
            )
            return redirect('confirmacao_sucesso')
    else:
        form = ConfirmacaoPresencaForm()

    return render(
        request, 'confirmacao/confirmar_presenca.html', {'form': form}
    )


def confirmacao_sucesso(request):
    return render(request, 'confirmacao/sucesso.html')
