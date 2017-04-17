from django.db import models


class GameModel(models.Model):
    player1 = models.IntegerField(default=0)
    player2 = models.IntegerField(default=0)
    turn = models.BooleanField(default=False)

    def otherid(self, playerid):
        print('otherid object method')
        if playerid == self.player1:
            return  self.player2
        else:
            return self.player1
    @classmethod
    def otheridclass(cls, playerid):
        print('otherid class method')
        t = SeaState.objects.get(pk=playerid)
        print(t)
        print('this seastate defined')
        tmp = t.gameid
        print(tmp)
        print('game id defined')
        tmp2 = GameModel.objects.get(pk=tmp)
        print(tmp2)
        print('gamemodel defined')
        tmp3 = tmp2.otherid(playerid)
        print(tmp3)
        print('otherid defined, ending class method')
        return tmp3


class SeaState(models.Model):
    playing = models.BooleanField(default=False)
    customizing = models.BooleanField(default=False)
    gameid = models.IntegerField(default=0)
    field = models.CharField(max_length=255)

    @classmethod
    def plays(cls, playerid):
        return cls.objects.filter(pk=playerid, customizing=True).count() > 0
    @classmethod
    def createuser(cls):
        ss = cls()
        ss.save()
        return ss.pk
