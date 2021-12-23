from django.shortcuts import render
from django.core.mail import send_mail


def index(request):
    send_mail(
        'Pokus',
        'Text mailu',
        'prebalovanie@gefcoslovakia.sk',
        ['palaj.marcel@gmail.com'],
        fail_silently=False,
    )
    return render(request, 'mails/index.html')
