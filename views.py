#-*- coding:UTF-8 -*-

from django.shortcuts import render


def index(request):
    template = 'gestor_espaco/index.html'

    context = {
        'page_name': 'Pagina inicial',
        'detail_page_name': 'Detalhes da pagina inicial'
    }

    return render(request, template, context)