from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

from riddles import SeaController
from .models import SeaState, GameModel


def gameview(request, playerid):
    boards = ['myboard', 'opboard']
    numbers = [['block' + str(i) + str(j) for j in range(10)] for i in range(10)]
    return render(request, 'GamePage.html', {'boards': boards, 'numbers': numbers, 'playerid': playerid})


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
