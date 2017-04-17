import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

from riddles import SeaController
from .models import SeaState, GameModel


def gameview(request, playerid):
    t = ['m', 'o'] #me/opponent
    blocks = [[[t[board] + 'block' + str(row) + str(col) for col in range(10)] for row in range(10)] for board in range(2)]
    return render(request, 'GamePage.html', {'blocks' : blocks, 'playerid': playerid})


def hitview(request, row, col, playerid):
    return JsonResponse({'result': 'ok', 'row' : row, 'col' : col})


def testifplaying(request, playerid):
    t = SeaState.objects.filter(pk=playerid, customizing=True).count()
    return JsonResponse({'playing': t > 0})


def createuserview(request):
    ss = SeaState()
    ss.save()
    SeaController.creategames()
    return render(request, 'Flappy.html', {'playerid' : ss.pk})

@csrf_exempt
def thejsonevent(request):
    if request.is_ajax():
        if request.method == 'POST':
            print(request)
            print(request.body)
            data = json.loads(request.body)
            print(data)
            t = data['ships']
            print(t)
            print(t[0][0])
            print('Ok table' if t[0][0] == 1 else 'Bad table')
            return JsonResponse({'result': 'Ok table' if t[0][0] == 1 else 'Bad table'})

    return JsonResponse({'Result': 'Not ajax or not GET'})
