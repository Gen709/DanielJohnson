from django.shortcuts import render, redirect
from student.models import Action, StatusAction

# Create your views here.
from django.http import HttpResponse


def index(request):
    if request.user.is_authenticated:
        return redirect('home', pk=request.user.id)
    else:
        # return HttpResponse("Hello, world. You're NOT AUTHENTICATED.")
        return redirect('login')

def user_detail(request, pk):
    statusaction = StatusAction.objects.all()
    action_resp = Action.objects.filter(responsable__id=pk)
    context = {'id': pk, 
               'action_resp': action_resp,
               'statusaction': statusaction}
    
    return render(request, 'page/user_detail.html', context)

def user_task(request, pk):
    pass
    