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
    return JsonResponse({'playing': SeaState.plays(playerid)})

def createuserview(request):
    pk = SeaState.createuser()
    SeaController.creategames()
    return render(request, 'Flappy.html', {'playerid' : pk})

@csrf_exempt
def thejsonevent(request):
    if request.is_ajax():
        if request.method == 'POST':
            data = json.loads(request.body)
            t = data['ships']
            b = SeaController.FieldValidation(t).is_valid()
            return JsonResponse({'result': 'Ok table' if b else 'Bad table'})
    return JsonResponse({'result': 'Not ajax or not GET'})
