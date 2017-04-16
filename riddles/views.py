from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

def helloview(request):
    return render(request, 'Flappy.html')

def gameview(request):
    gameview.playerid += 1
    t = gameview.playerid
    boards = ['myboard', 'opboard']
    numbers = [['block' + str(i) + str(j) for j in range(10)] for i in range(10)]
    return render(request, 'GamePage.html', {'boards': boards, 'numbers': numbers, 'playerid': t})
gameview.playerid = 0

def hitview(request, row, col):
    return JsonResponse({'result' : 'ok'})

def testshowid(request, playerid):
    temp = str(-int(playerid))
    print(temp)
    return JsonResponse({'temp' : temp})

