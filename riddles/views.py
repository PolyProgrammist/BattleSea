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
    t = ['m', 'o']  # me/opponent
    blocks = [[[t[board] + 'block' + str(row) + str(col) for col in range(10)] for row in range(10)] for board in
               range(2)]
    bcnt = ['m', 'o']
    lockcnt = range(10)
    return render(request, 'GamePage.html', {'blocks': blocks, 'playerid': playerid, 'bcnt' : bcnt, 'lockcnt' : lockcnt})


def hitview(request, row, col, playerid):
    t = SeaController.HitMaker(playerid, row, col)
    if (t.can_hit()):
        d = t.make_hit()
        state = SeaController.getstate(int(GameModel.otheridclass(playerid)))
        t = 'go' if SeaController.okfield(state) else 'win'
        if (t == 'win'):
            GameModel.change_turn(playerid)
        return JsonResponse({'result': 'ok', 'ships': d, 'gameend' : t})
    else:
        return JsonResponse({'result': 'fail'})


def testifopponentwent(request, playerid):
    state = SeaController.getstate(playerid)
    t = 'go' if SeaController.okfield(state) else 'lose'
    if not GameModel.get_client_turn(playerid) and t == 'go':
        return JsonResponse({'went': False})
    return JsonResponse({'went': True, 'ships': state, 'gameend' : t})


def testifplaying(request, playerid):
    t = SeaState.plays(playerid)
    return JsonResponse({'playing': t})


def createuserview(request):
    pk = SeaState.createuser()
    SeaController.creategames()
    return render(request, 'Flappy.html', {'playerid': pk})


@csrf_exempt
def thejsonevent(request):
    if request.is_ajax():
        if request.method == 'POST':
            data = json.loads(request.body)
            t = data['ships']
            b = SeaController.FieldValidation(t).is_valid()
            if b:
                SeaState.objects.filter(pk=data['pk']).update(playing=True)
                SeaState.objects.filter(pk=data['pk']).update(field=json.dumps(t))
            return JsonResponse({'result': 'ok' if b else 'bad'})
    return JsonResponse({'result': 'Not ajax or not GET'})


def testifopponentsubmitted(request, playerid):
    otherid = GameModel.otheridclass(playerid)
    submitted = SeaState.objects.get(pk=otherid).playing
    t = GameModel.get_client_turn(playerid)
    return JsonResponse({'submitted': submitted, 'turn': t})
