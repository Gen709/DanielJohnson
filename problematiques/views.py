from django.shortcuts import render
from .models import Item
from urllib.parse import unquote
from django.http.response import JsonResponse, HttpResponse
# Create your views here.


def ajax_search_problematiques(request):
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # input_str = request.GET.get('term', '')
        data_list =[]
        input_str = unquote(request.GET['term'])
        data_list = [{x.id: {'description':x.nom}} for x in Item.objects.filter(nom__istartswith=input_str)]
    
        data = JsonResponse(data_list, safe=False)
        
        mimetype = 'application/json'
        
        if len(data_list) > 0 and input_str != '':
            return HttpResponse(data, mimetype)
        else:
            return HttpResponse('', mimetype)