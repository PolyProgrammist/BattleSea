from django.db import models


class GameModel(models.Model):
    player1 = models.IntegerField(default=0)
    player2 = models.IntegerField(default=0)
    turn = models.BooleanField(default=False)

    def otherid(self, playerid):
        if int(playerid) == int(self.player1):
            return self.player2
        else:
            return self.player1

    @classmethod
    def otheridclass(cls, playerid):
        t = cls.game_by_user(playerid).otherid(playerid)
        return t

    @classmethod
    def get_client_turn(cls, playerid):
        game = cls.game_by_user(playerid)
        t = (int(game.player1) == int(playerid)) == bool(game.turn)
        return t

    @classmethod
    def change_turn(cls, playerid):
        game = cls.game_by_user(playerid)
        game.turn = not game.turn
        game.save()

    @classmethod
    def game_by_user(cls, playerid):
        return GameModel.objects.get(pk=(SeaState.objects.get(pk=playerid).gameid))

class SeaState(models.Model):
    playing = models.BooleanField(default=False)
    customizing = models.BooleanField(default=False)
    gameid = models.IntegerField(default=0)
    field = models.CharField(max_length=512)

    @classmethod
    def plays(cls, playerid):
        return cls.objects.filter(pk=playerid, customizing=True).count() > 0
    @classmethod
    def createuser(cls):
        ss = cls()
        ss.save()
        return ss.pk
