import json

from .models import SeaState, GameModel


def creategames():
    q = SeaState.objects.filter(customizing=False, playing=False)
    for i in range(len(q)):
        if i + 1 < len(q):
            create_one_game(q[i], q[i + 1])


def create_one_game(a, b):
    game = GameModel(player1=a.pk, player2=b.pk, turn=0)
    game.save()
    a.customizing = True
    b.customizing = True
    a.gameid = game.pk
    b.gameid = game.pk
    a.save()
    b.save()

okdi = [0, 1, 0, -1]
okdj = [1, 0, -1, 0]
wrdi = [1, 1, -1, -1]
wrdj = [-1, 1, -1, 1]


def okpos(i, j):
    return i >= 0 and j >= 0 and i < 10 and j < 10


class FieldValidation:
    def __init__(self, ships):
        self.ships = ships

    def is_valid(self):
        self.was = [[False for i in range(10)] for j in range(10)]
        this_count = [0] * 4
        for i in range(10):
            for j in range(10):
                if self.ships[i][j] and not self.was[i][j]:
                    size = self.dfs(i, j)
                    if size == -1 or size > 4:
                        return False
                    this_count[size - 1] += 1
        return not any(t[0] != t[1] for t in list(zip(this_count, self.shipcounts)))

    shipcounts = [4, 3, 2, 1]



    def dfs(self, i, j):
        self.was[i][j] = True
        for k in range(4):
            ni, nj = i + wrdi[k], j + wrdj[k]
            if okpos(ni, nj) and self.ships[ni][nj]:
                return -1
        res = 1
        for k in range(4):
            ni, nj = i + okdi[k], j + okdj[k]
            if okpos(ni, nj) and self.ships[ni][nj] and not self.was[ni][nj]:
                size = self.dfs(ni, nj)
                if size == -1:
                    return -1
                res += size
        return res

        # [[0,0,1,1,1,0,0,1,1,0],[0,0,0,0,0,0,0,0,0,0],[0,1,0,0,1,0,0,1,0,1],[0,1,0,0,1,0,0,0,0,0],[0,1,0,0,1,0,0,1,1,0],[0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,1],[0,0,0,0,0,0,0,1,0,0]]


class HitMaker:
    def __init__(self, playerid, row, col):
        self.playerid = playerid
        self.row = row
        self.col = col

    def can_hit(self):
        self.stringchangestate = SeaState.objects.get(pk=GameModel.otheridclass(self.playerid)).field
        self.changestate = json.loads(self.stringchangestate)
        game = GameModel.objects.get(pk=self.changestate.gameid)
        return self.changestate[self.row][self.col] <= 1 and GameModel.get_client_turn(self.playerid)

    def make_hit(self):
        if self.changestate[self.row][self.col] == 0:
            self.changestate[self.row][self.col] = 4
        else:
            self.was = [[False for j in range(10)] for i in range(10)]
            if self.dfs_check_kill(self.row, self.col):
                self.dfs_killer(self.row, self.col)

        GameModel.change_turn(self.playerid)
        self.stringchangestate = json.dumps(self.changestate)
        SeaState.objects.filter(pk=GameModel.otheridclass(self.playerid)).update(field=self.stringchangestate)
        return self.changestate


    def dfs_check_kill(self, i, j):
        self.was[i][j] = True
        for k in range(4):
            ni, nj = i + wrdi[k], j + wrdj[k]
            if okpos(ni, nj):
                self.changestate[ni][nj] = 5
        res = True
        for k in range(4):
            ni, nj = i + okdi[k], j + okdj[k]
            if okpos(ni, nj) and not self.was[ni][nj]:
                res = res and self.changestate[ni][nj] == 1
                if self.changestate[ni][nj] == 2:
                    res = res and self.dfs_check_kill(self, ni, nj)
        return res

    def dfs_killer(self, i, j):
        self.was[i][j] = True
        self.changestate[i][j] = 3
        for k in range(4):
            ni, nj = i + wrdi[k], j + wrdj[k]
            if okpos(ni, nj):
                self.changestate[ni][nj] = 5

        for k in range(4):
            ni, nj = i + okdi[k], j + okdj[k]
            if okpos(ni, nj) and not self.was[ni][nj]:
                if self.changestate[ni][nj] == 0:
                    self.changestate[ni][nj] = 5
                if self.changestate[ni][nj] == 2:
                    self.dfs_killer(self, ni, nj)

